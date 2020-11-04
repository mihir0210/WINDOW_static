%% Set file names9
function LinModel=Linearization_new_parallel(rated_windspeed,Airfoil,Blade,Control,Drivetrain,Nacelle,Tower)


LinModel=[pwd,'\Linearized_model.mat'];


%% Linearization
%WindSpeeds=[rated_windspeed,ceil(rated_windspeed):25];
WindSpeeds=[5:floor(rated_windspeed),rated_windspeed,ceil(rated_windspeed):25];
I=find(WindSpeeds==rated_windspeed);
%WindSpeeds=5:25;
LinAmount=1;
LinRotations=1;

disp('Starting linearization...')
disp(' ')

% Run modal analysis for 0 rpm
disp('Finding non-rotating mode shapes...')

% Run BModes for tower
evalc([...
'[y11_shape, y11_coeff, y11_freq,', ...
' y12_shape, y12_coeff, y12_freq,', ...
' y21_shape, y21_coeff, y21_freq,', ...
' y22_shape, y22_coeff, y22_freq] = BModes(Blade,Tower,Nacelle,Control,2,0);']);

% Store in handles
Tower.ForeAft1_coeff = y21_coeff;
Tower.ForeAft2_coeff = y22_coeff;
Tower.SideSide1_coeff = y11_coeff;
Tower.SideSide2_coeff = y12_coeff;

% Run BModes for blade
evalc([...
'[y11_shape, y11_coeff, y11_freq,', ...
' y12_shape, y12_coeff, y12_freq,', ...
' y21_shape, y21_coeff, y21_freq,', ...
' y22_shape, y22_coeff, y22_freq] = BModes(Blade,Tower,Nacelle,Control,1,0);']);

% Store in handles
Blade.Flap1_coeff = y11_coeff;
Blade.Flap2_coeff = y12_coeff;
Blade.Edge1_coeff = y21_coeff;
Blade.Edge2_coeff = y22_coeff;

% Steady state curves
disp('Determining steady state rotational speeds and pitch angles...')
[~, ~, OmegaU, PitchAngle] = SteadyState(Blade, Airfoil, Drivetrain, Control, WindSpeeds);
RPM = OmegaU * 60/(2*pi);

Lin.V = WindSpeeds;
Lin.Pitch =  PitchAngle*pi/180;
Lin.RSpeed = OmegaU;


% Avoid some common errors with linearization
% (1) Set the gearbox efficiency (to avoid error that ADAMS cannot handle
% nonideal gearboxes) and remember the true efficiency to reset later
TrueGearboxEfficiency = Drivetrain.Gearbox.Efficiency;
Drivetrain.Gearbox.Efficiency = 1;

%{
% (2) Scale the HSS inertia from the reference machine (to avoid issues
% with reaching very high rotor speeds during the linearization of some
% direct-drive machines). Assuming that P ~ Mass, Radius? ~ P^(2/3), we get
% a relation in the shape of I/Iref = (P/Pref)^(5/3) * (RPM_ref/RPM)^2.
Prated = Control.Torque.SpeedC*(2*pi/60) *  Control.Torque.Demanded * Drivetrain.Generator.Efficiency;
Drivetrain.Generator.HSSInertia = 534.116 * (Prated/(5e6))^(5/3) * (12.1*97/Control.Torque.SpeedC)^2;
%}

% Turbine input file
disp('Writing input files...')

% Simulink settings
TSim = 10;
FAST_InputFileName = [pwd, '\subfunctions\inputfiles\FAST.fst'];

% Turbine input files
AeroDyn(Blade,Airfoil,Tower,'Linearize');
ServoDyn(Drivetrain,Control,'Linearize');

% Preload the OutList
load([pwd '\subfunctions\OutList.mat'])
assignin('base', 'OutList', OutList);

% Run linearization
sysm = cell(length(WindSpeeds),1);
data = cell(length(WindSpeeds),1);

Wind.Type = 1;
model ='OpenLoop'; 
load_system(model); 


parfor j = I:length(WindSpeeds)
        
    % Status update
    disp(['Linearizing at U = ', num2str(WindSpeeds(j), '%5.2f'), ' m/s, ', num2str(RPM(j), '%5.2f'), ' rpm, ', num2str(PitchAngle(j), '%5.2f'), ' deg pitch'])
    
    % Set initial RPM and pitch angle in ElastoDyn input file
    ElastoDyn(Blade,Tower,Nacelle,Drivetrain,Control,'Linearize',RPM(j),PitchAngle(j));
    
    % Set linearization times for 10 deg azimuth step (after 30 s)
    LinAziPositions = linspace(0,360*LinRotations,LinAmount+1);
    LinTimes = TSim + Control.DT * round(LinAziPositions(2:end)/(RPM(j)*6) / Control.DT);
    TMax = max(LinTimes)+1.0;
    
    FASTinput(Control.DT, TMax, 'Linearize', LinTimes);

    % Wind input file
 
    InflowWind(Wind,WindSpeeds(j),Tower.HubHeight,Blade.Radius(end))
        
    % Run FAST and prevent console output
    assignin('base', 'TMax', TMax);
    assignin('base', 'FAST_InputFileName', FAST_InputFileName);
    %evalc('sim(''OpenLoop'',TMax);');
    simOut{j} = sim(model);
    
    
% Extract steady state solution after 60 seconds and average over 36
% steps
    A = [];
    B = [];
    C = [];
    D = 0;
 
    for i = 1:LinAmount
        LinName = [pwd, '\subfunctions\inputfiles\FAST.SFunc.', int2str(i), '.lin'];
        data{j} = ReadFASTLinear(LinName);
        
%         A = A + 1/LinAmount * data{j}.A;
%         B = B + 1/LinAmount * data{j}.B;
%         C = C + 1/LinAmount * data{j}.C;
        D = D + 1/LinAmount * data{j}.D;
    end
     sysm{j} = ss(A, B, C, D); %, 'InputName', data{j}.u_desc,'Outputname', data{j}.y_desc, 'StateName', data{j}.x_desc);
    
%     Lin.V(j) = data{j}.y_op{1};
%     Lin.Torque(j) = data{j}.y_op{5};
%     Lin.Pitch(j) =  data{j}.y_op{34}*pi/180;
%     Lin.GSpeed(j) = data{j}.y_op{33}*pi/30;
%     Lin.RSpeed(j) = data{j}.y_op{38}*pi/30;
end

% Reset the gearbox efficiency
Drivetrain.Gearbox.Efficiency = TrueGearboxEfficiency;

% save(handles.LinModel, 'sysm', 'Lin');
%save(LinModel, 'sysm', 'Lin','data');
%save(LinModel,'data','Lin','sysm');
disp(' ')
disp(' ')
disp('... Linearization complete!')
%assignin('base', 'data', data)
end
