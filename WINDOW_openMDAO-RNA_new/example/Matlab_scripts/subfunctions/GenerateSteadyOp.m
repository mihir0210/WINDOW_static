function [Cp,lambda]=GenerateSteadyOp(fine_pitch)
load('NREL5MW.mat')
Control.Pitch.Fine=fine_pitch;
Pitchi = [];
% if get(handles.CalcPerformanceFine_checkbox, 'Value') == 1
Pitchi = [Pitchi, Control.Pitch.Fine];

% Find rotor performance coefficients, when requested
if ~isempty(Pitchi)

    disp('Calculating rotor performance...')

    TSRj = 0:0.1:20;
    CPij = zeros(length(Pitchi), length(TSRj));
    CTij = zeros(length(Pitchi), length(TSRj));
    CQij = zeros(length(Pitchi), length(TSRj));
    lgd_label = cell(1, length(Pitchi));
    
    for i = 1:length(Pitchi)
        disp(['Pitch angle = ', num2str(Pitchi(i))])
        lgd_label{i} = [num2str(Pitchi(i), '%.4f'), ' deg'];
        for j = 11:length(TSRj) % Tip speed ratios below 1 omitted to avoid problems in the performance calculations

            if (TSRj(j) - ceil(TSRj(j))) == 0
                disp(['TSR = ', num2str(TSRj(j))])
            end

            [CTij(i,j), CQij(i,j)] = PerformanceCoefficients(Blade, Airfoil, Pitchi(i), TSRj(j));
            CPij(i,j) = CQij(i,j)*TSRj(j);

            if CPij(i,j) < 0 && TSRj(j) > 1
                CPij(i,j) = 0;
                CQij(i,j) = 0;
                break
            end
        end        
    end
    
    % Plot
    disp('Drawing plots...')
    Plot = figure();
    set(Plot, 'Name', 'Power coefficient curve(s)')
    plot(TSRj,CPij(1,:))
    xlim([0 max(TSRj)])
    ylim([0 ceil(20*max(max(CPij)))/20+0.05])
    set(gca, ...
        'XMinorTick', 'on', ...
        'YMinorTick', 'on', ...
        'Box', 'on', ...
        'Layer', 'top', ...
        'Fontsize', 8);
    xlabel('Tip speed ratio [-]')
    ylabel('Power coefficient [-]')
    hold on
    for i = 2:length(Pitchi)
        plot(TSRj,CPij(i,:))
    end
    hold off
    grid on
    legend(lgd_label)
    pause(0.1)
    
    % Send data to Matlab workspace
    assignin('base', 'Rotor_Pitch', Pitchi(:));
    assignin('base', 'Rotor_Lamda', TSRj(:));
    assignin('base', 'Rotor_cP', CPij);
    assignin('base', 'Rotor_cT', CTij);
    assignin('base', 'Rotor_cQ', CQij);
    [Cp,I]=max(CPij);
    lambda=TSRj(I);
end

% Find turbine operation conditions, when requested
% if get(handles.CalcOperation_checkbox, 'Value') == 1
% % Wind speed range
% U = str2double(get(handles.WindSpeed_From, 'String')):str2double(get(handles.WindSpeed_Step, 'String')):str2double(get(handles.WindSpeed_To, 'String'));
% if sum(U) == 0 || isnan(sum(U))
%     errordlg('Invalid wind speed range.', 'Error')
% else
%     disp('Generating steady operating curves...')
%     
%     % Determine steady state curves (external function, which is also used in 'Linearization.m'
%     [CT, CQ, OmegaU, PitchAngle] = SteadyState(Blade, Airfoil, Drivetrain, Control, U);
% 
%     TSR = OmegaU.*Blade.Radius(end)./U;
%     CP = CQ.*TSR;
%     TSR(1) = 0;
%     CP(1) = 0;
% 
%     P = 0.5*1.225*pi*Blade.Radius(end)^2 * U.^3 .* CP .* Drivetrain.Gearbox.Efficiency .* Drivetrain.Generator.Efficiency;
%     T = 0.5*1.225*pi*Blade.Radius(end)^2 * U.^2 .* CT;
%     Q = 0.5*1.225*pi*Blade.Radius(end)^3 * U.^2 .* CQ;
%     RPM = OmegaU * 60/(2*pi);
% 
%     Prated = max(P);
% 
%     % Plot
%     disp('Drawing plots...')
%     Plot = figure();
%     set(Plot, 'Name', 'Steady power curve')
%     plot(U,P/1e6)
%     xlim([0 max(U)])
%     ylim([0 ceil(Prated/1e6)+0.5])
%     set(gca, ...
%         'XMinorTick', 'on', ...
%         'YMinorTick', 'on', ...
%         'Box', 'on', ...
%         'Layer', 'top', ...
%         'Fontsize', 8);
%     xlabel('Wind speed [m/s]')
%     ylabel('Electrical power [MW]')
% 
%     % Send data to Matlab workspace
%     assignin('base', 'WindSpeed', U(:));
%     assignin('base', 'ElectricalPower', P(:));
%     assignin('base', 'RotorThrust', T(:));
%     assignin('base', 'RotorSpeed', RPM(:));
%     assignin('base', 'RotorTorque', Q(:));
%     assignin('base', 'PitchAngle', PitchAngle(:));
%     assignin('base', 'TipSpeedRatio', TSR(:));
%     assignin('base', 'PowerCoefficient', CP(:));
%     assignin('base', 'ThrustCoefficient', CT(:));
%     assignin('base', 'TorqueCoefficient', CQ(:));% Get geometry from handles
% end
% end






%{
% Unused functions
function CalcPerformanceFine_checkbox_Callback(hObject, eventdata, handles)
function PitchAngle_From_Callback(hObject, eventdata, handles)
function PitchAngle_To_Callback(hObject, eventdata, handles)
function PitchAngle_Step_Callback(hObject, eventdata, handles)
function WindSpeed_From_Callback(hObject, eventdata, handles)
function WindSpeed_To_Callback(hObject, eventdata, handles)
function WindSpeed_Step_Callback(hObject, eventdata, handles)
%}
