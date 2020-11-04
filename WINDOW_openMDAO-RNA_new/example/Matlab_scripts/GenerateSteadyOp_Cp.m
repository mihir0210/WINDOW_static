%% Perform the calculations
function Cp=GenerateSteadyOp_Cp(fine_pitch, lambda)

%Turbine_properties=Preprocessing(1);
%load(Turbine_properties);
%Preprocessing_new(1);
% load([pwd,'NREL5MW (gain scheduled).mat', 'Airfoil']);
% load([pwd,'\Blade_Cp.mat']);

load('NREL5MW (gain scheduled).mat', 'Airfoil');
load('Blade_Cp.mat');


Blade.Radius = Blade_Radius;
Blade.Chord = Blade_Chord;
Blade.Twist = Blade_Twist;
Blade.NFoil = Blade_NFoil+1;
Blade.IFoil = Blade_IFoil+1;
Blade.Number = Blade_Number;


Pitchi = [];
% if get(handles.CalcPerformanceFine_checkbox, 'Value') == 1
Pitchi = [Pitchi, fine_pitch];


% Find rotor performance coefficients, when requested
if ~isempty(Pitchi)

    %disp('Calculating rotor performance...')

    %TSRj = 0:0.1:20;
    TSRj = 4:0.1:10;
    CPij = zeros(length(Pitchi), length(TSRj));
    CTij = zeros(length(Pitchi), length(TSRj));
    CQij = zeros(length(Pitchi), length(TSRj));
    lgd_label = cell(1, length(Pitchi));
    
    for i = 1:length(Pitchi)
        %disp(['Pitch angle = ', num2str(Pitchi(i))])
        lgd_label{i} = [num2str(Pitchi(i), '%.4f'), ' deg'];
        for j = 11:length(TSRj) % Tip speed ratios below 1 omitted to avoid problems in the performance calculations

%             if (TSRj(j) - ceil(TSRj(j))) == 0
%                 disp(['TSR = ', num2str(TSRj(j))])
%             end

            [CTij(i,j), CQij(i,j)] = PerformanceCoefficients(Blade, Airfoil, Pitchi(i), TSRj(j));
            CPij(i,j) = CQij(i,j)*TSRj(j);

            if CPij(i,j) < 0 && TSRj(j) > 1
                CPij(i,j) = 0;
                CQij(i,j) = 0;
                break
            end
        end        
    end
    
%     % Plot
%     disp('Drawing plots...')
%     Plot = figure();
%     set(Plot, 'Name', 'Power coefficient curve(s)')
%     plot(TSRj,CPij(1,:))
%     xlim([0 max(TSRj)])
%     ylim([0 ceil(20*max(max(CPij)))/20+0.05])
%     set(gca, ...
%         'XMinorTick', 'on', ...
%         'YMinorTick', 'on', ...
%         'Box', 'on', ...
%         'Layer', 'top', ...
%         'Fontsize', 8);
%     xlabel('Tip speed ratio [-]')
%     ylabel('Power coefficient [-]')
%     hold on
%     for i = 2:length(Pitchi)
%         plot(TSRj,CPij(i,:))
%     end
%     hold off
%     grid on
%     legend(lgd_label)
%     pause(0.1)
    
    % Send data to Matlab workspace
    assignin('base', 'Rotor_Pitch', Pitchi(:));
    assignin('base', 'Rotor_Lamda', TSRj(:));
    assignin('base', 'Rotor_cP', CPij);
    assignin('base', 'Rotor_cT', CTij);
    assignin('base', 'Rotor_cQ', CQij);
    diff = TSRj - lambda;
    [~,I] =min(abs(diff));
    %I = find(TSRj==lambda);
    Cp = CPij(I);
    
end

