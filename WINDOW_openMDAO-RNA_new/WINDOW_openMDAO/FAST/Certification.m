
%% Initialization code
%  Preprocessing_new(3);
% % 
  load([pwd,'\WT_design.mat']);
  load([pwd,'\Linearized_model.mat']);

%  load('NREL5MW (gain scheduled).mat');
%%% Nodes for sections 0.15, 0.3, 0.5, 0.75, 0.95 : 
%%%                      7 , 15, 24, 37 , 47 
%  load('NREL5MW_linear.mat');

U = num2str(CertificationSettings.Run.WindSpeed(1));
if length(CertificationSettings.Run.WindSpeed) > 1
    for i = 2:length(CertificationSettings.Run.WindSpeed)
        U = [U, ', ', num2str(CertificationSettings.Run.WindSpeed(i))];
    end
end

%% Open Simulink interface
%function Simulink_Callback %(hObject, eventdata, handles)
open_system('FAST')

%% View output signals
 %   function Output_Callback %(hObject, eventdata, handles)
        load_system('FAST')
        open_system('FAST/Scope')
        
        %% Set output file name
        %function SetOutputName_Callback(hObject, eventdata, handles)
%             [FileName,PathName] = uiputfile('*.mat', 'Set output file name(s)');
%             if FileName
                PathName=[pwd,'\'];
                FileName='DLC.mat';
                % Store in handles
                 initial_OutputFile = {PathName, FileName(1:end-4)};
                 OutputFiles={};
               
              
if ~isempty(initial_OutputFile)
    
    i = 1;
    if length(CertificationSettings.Run.WindSpeed) * CertificationSettings.Run.Seeds <= 4
        for U = CertificationSettings.Run.WindSpeed
            for seed  = 1:CertificationSettings.Run.Seeds
                
                OutputFile = ['../', initial_OutputFile{2}];
                if length(CertificationSettings.Run.WindSpeed) > 1
                    OutputFile = [OutputFile, '_U=', num2str(U,'%2.2f')];
                end
                if CertificationSettings.Run.Seeds > 1
                    OutputFile = [OutputFile, '_seed=', int2str(seed)];
                end
                OutputFiles{i} = [OutputFile, '.mat'];
                i = i + 1;
                
            end
        end
    else
        for U = CertificationSettings.Run.WindSpeed
            for seed  = 1:CertificationSettings.Run.Seeds
                
                OutputFile = ['../',initial_OutputFile{2}];
                if length(CertificationSettings.Run.WindSpeed) > 1
                    OutputFile = [OutputFile, '_U=', num2str(U,'%2.2f')];
                end
                if CertificationSettings.Run.Seeds > 1
                    OutputFile = [OutputFile, '_seed=', int2str(seed)];
                end
                OutputFiles{i} = [OutputFile, '.mat'];
                i = i + 1;
                
                if i == 3
                    break
                end
                
            end
            
            if i == 3
                break
            end
        end
    end
    
    OutputFiles{3} = '  ...';
    OutputFile = ['../', initial_OutputFile{2}];
    if length(CertificationSettings.Run.WindSpeed) > 1
        OutputFile = [OutputFile, '_U=', num2str(CertificationSettings.Run.WindSpeed(end),'%2.2f')];
    end
    if CertificationSettings.Run.Seeds > 1
        OutputFile = [OutputFile, '_seed=', int2str(CertificationSettings.Run.Seeds)];
    end
    OutputFiles{4} = [OutputFile, '.mat'];
    
end
       
            
           
        
        %% Start simulation
        %function Start_Callback %(hObject, eventdata, handles)
        
%          % Set output filename
%          if isempty(OutputFile)
%             OutputFile = [pwd, '\output'];
%         end
        
        % Temporarily turn off warnings
        % warning('off','all')
        
        % % Load parameters from handles
        % Blade = handles.Blade;
        % Airfoil = handles.Airfoil;
        % Tower = handles.Tower;
        % Nacelle = handles.Nacelle;
        % Drivetrain = handles.Drivetrain;
        % Control = handles.Control;
        % CertificationSettings = handles.CertificationSettings;
        % U = CertificationSettings.Run.WindSpeed;
        % TMax = CertificationSettings.Run.Time;
        % T = CertificationSettings.Wind.T;
        % Ly = CertificationSettings.Wind.Ly;
        % Lz = CertificationSettings.Wind.Lz;
        % dt = CertificationSettings.Wind.dt;
        % Ny = CertificationSettings.Wind.Ny;
        % Nz = CertificationSettings.Wind.Nz;
        
        % Run modal analysis for 0 rpm
        %disp('Preparing input files...')
        
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
        
        % Load linearized model
        %load(handles.LinModel)
        
        % Initialize controller
        disp('Setting controller parameters...')
        %assignin('base', 'Drivetrain', Drivetrain)
        %assignin('base', 'Control', Control)
        ControllerDesign(Control);
        
        % Turbine input files
        TMax = CertificationSettings.Run.Time;
        FASTinput(Control.DT, TMax);
        AeroDyn(Blade,Airfoil,Tower,CertificationSettings.Mode.Type);
        
        % Send to base workspace and make structures available for Simulink and run the simulation
         assignin('base', 'FAST_InputFileName', [pwd, '\subfunctions\inputfiles\FAST.fst']);
 %assignin('base', 'FAST_InputFileName', [pwd, '\inputfiles\FAST.fst']);
        assignin('base', 'TMax', TMax);
        %assignin('base', 'Lin', Lin);
        %disp('')
        
        
        % Loop over wind speeds and seeds
        for U = CertificationSettings.Run.WindSpeed
            for seed = 1:CertificationSettings.Run.Seeds
                
                % Output file name
                OutputFile = [initial_OutputFile{1},initial_OutputFile{2}];
                if length(CertificationSettings.Run.WindSpeed) > 1
                    OutputFile = [OutputFile, '_U=', num2str(U,'%2.2f')];
                end
                if CertificationSettings.Run.Seeds > 1
                    OutputFile = [OutputFile, '_seed=', int2str(seed)];
                end
                OutputFile = [OutputFile, '.mat'];
                
                % Find initial RPM and pitch angle
                if CertificationSettings.Wind.Type == 2
                    Ui = CertificationSettings.Wind.Step;
                else
                    Ui = U;
                end
                
                if Ui < Control.WindSpeed.Cutin || Ui > Control.WindSpeed.Cutout
                    RPM_Init = 0;
                    P_InitAngle = Control.Pitch.Max;
                else
                    RPM_Init = (30/pi) * interp1(Lin.V,Lin.RSpeed,Ui,'pchip');
                    P_InitAngle = 180/pi * interp1(Lin.V,Lin.Pitch,Ui,'pchip');
                end
                
                if CertificationSettings.Mode.Type == 3     % Startup
                    RPM_Init = 0;
                    P_InitAngle = Control.Pitch.Max;
                elseif CertificationSettings.Mode.Type == 6 % Idling
                    RPM_Init = 0;
                    P_InitAngle = Control.Pitch.Max;
                elseif CertificationSettings.Mode.Type == 7	% Parked
                    RPM_Init = 0;
                    P_InitAngle = Control.Pitch.Max;
                end
                
                assignin('base', 'RPM_Init', RPM_Init);
                assignin('base', 'T_GenSpeedInit', RPM_Init*Drivetrain.Gearbox.Ratio);
                assignin('base', 'P_InitAngle', P_InitAngle);
                
                % Set operation mode in ElastoDyn file
                ElastoDyn(Blade,Tower,Nacelle,Drivetrain,Control,CertificationSettings.Mode.Type,RPM_Init,P_InitAngle);
                
                % Set operation mode in ServoDyn file
                ServoDyn(Drivetrain,Control,CertificationSettings.Mode.Type,CertificationSettings.Mode.Actiontime);
                
                % Wind input file
                %         disp('Generating wind file...')
                InflowWind(CertificationSettings.Wind,U,Tower.HubHeight,Blade.Radius(end))
                
                %Preload the OutList
                load([pwd '\subfunctions\OutList.mat'])
                assignin('base', 'OutList', OutList);
                assignin('base', 'CertificationSettings', CertificationSettings);
                
                % Call Simulink
                disp(['Running FAST (U = ', num2str(U,'%5.2f'), ' m/s, seed ', int2str(seed), '/', int2str(CertificationSettings.Run.Seeds), ')'])
                evalc('sim(''FAST'',TMax);');
                
                 %% Extract output
                filename = [pwd '\subfunctions\inputfiles\FAST.SFunc.out'];
                delimiter = '\t';
                startRow = 6;
                formatSpec = '%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%[^\n\r]';
                fileID = fopen(filename,'r');
                textscan(fileID, '%[^\n\r]', startRow-1, 'ReturnOnError', false);
                Output = textscan(fileID, formatSpec, 'Delimiter', delimiter, 'EmptyValue' ,NaN,'ReturnOnError', false);
                fclose(fileID);
                
                %Rename and save vectors
                save(OutputFile, 'Legend')
                for i = 1:length(OutList)
                    eval([OutList{i}, ' = Output{i};']);
                    eval(['save(OutputFile, ''', OutList{i}, ''', ''-append'');']);
                end
                
            end
        end
    
disp('Completed!')




