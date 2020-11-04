%%%% Plots stresses for static and dynamic %%%%
% Stress_loc1 = [Stress_span1_flapwise_skin_nm, Stress_span1_flapwise_spar_nm, Stress_span1_edgewise_skin_nm, Stress_span1_edgewise_te_reinf_nm];
% Stress_loc2 = [Stress_span2_flapwise_skin_nm, Stress_span2_flapwise_spar_nm, Stress_span2_edgewise_skin_nm, Stress_span2_edgewise_te_reinf_nm];
% Stress_loc3 = [Stress_span3_flapwise_skin_nm, Stress_span3_flapwise_spar_nm, Stress_span3_edgewise_skin_nm, Stress_span3_edgewise_te_reinf_nm];
% Stress_loc4 = [Stress_span4_flapwise_skin_nm, Stress_span4_flapwise_spar_nm, Stress_span4_edgewise_skin_nm, Stress_span4_edgewise_te_reinf_nm];
% Stress_loc5 = [Stress_span5_flapwise_skin_nm, Stress_span5_flapwise_spar_nm, Stress_span5_edgewise_skin_nm, Stress_span5_edgewise_te_reinf_nm];

%% plot for spar caps
load('Ultimate_Results_dynamic_opt.mat');
%stress_sparcap = [Stress_root; Stress_span(:,2)];
stress_sparcap = Stress_span(:,2);
plot(stress_sparcap, 'b'); hold on;
plot(stress_sparcap, 'bo');
grid on
    a = gca;
    % set box property to off and remove background color
    set(a,'box','off','color','none')
    % create new, empty axes with box but without ticks
    b = axes('Position',get(a,'Position'),'box','on','xtick',[],'ytick',[]);
    % set original axes as active
    axes(a)
    % link axes in case of zooming
    linkaxes([a b])
set(gca,'GridLineStyle','--')
set(gca,'GridAlpha',0.8)
set(gca,'TickDir','out');

axesH = gca;
axesH.XAxis.TickLabelInterpreter = 'latex';
axesH.XAxis.TickLabelFormat      = '\\textbf{%g}';
axesH.YAxis.TickLabelInterpreter = 'latex';
axesH.YAxis.TickLabelFormat      = '\\textbf{%g}';

xticks([1 2 3 4 5])
xticklabels({'\textbf{0.15}','\textbf{0.3}', '\textbf{0.5}','\textbf{0.75}', '\textbf{0.9}'})
xlim([0 6]);
ylim([250 650]);
ylabel('\textbf{$\sigma_{flap}$ in UD-C (MPa)}','Interpreter','latex');
xlabel('\textbf{Normalized blade radius (-)}','Interpreter','latex');

%% plot for TE REinf
load('Ultimate_Results_dynamic_opt.mat');
%stress_sparcap = [Stress_root; Stress_span(:,2)];
stress_tereinf = Stress_span(:,4);
plot(stress_tereinf, 'r'); hold on;
plot(stress_tereinf, 'ro');
grid on
    a = gca;
    % set box property to off and remove background color
    set(a,'box','off','color','none')
    % create new, empty axes with box but without ticks
    b = axes('Position',get(a,'Position'),'box','on','xtick',[],'ytick',[]);
    % set original axes as active
    axes(a)
    % link axes in case of zooming
    linkaxes([a b])
set(gca,'GridLineStyle','--')
set(gca,'GridAlpha',0.8)
set(gca,'TickDir','out');
axesH = gca;
axesH.XAxis.TickLabelInterpreter = 'latex';
axesH.XAxis.TickLabelFormat      = '\\textbf{%g}';
axesH.YAxis.TickLabelInterpreter = 'latex';
axesH.YAxis.TickLabelFormat      = '\\textbf{%g}';

xticks([1 2 3 4 5])
xticklabels({'\textbf{0.15}','\textbf{0.3}', '\textbf{0.5}','\textbf{0.75}', '\textbf{0.9}'})
xlim([0 6]);
ylim([0 120]);
ylabel('\textbf{$\sigma_{edge}$ in UD-G (MPa)}','Interpreter','latex');
xlabel('\textbf{Normalized blade radius (-)}','Interpreter','latex');
 
%% plot for  Skin
load('Ultimate_Results_dynamic_opt.mat');
%stress_sparcap = [Stress_root; Stress_span(:,2)];
stress_edgeskin = [Stress_root;Stress_span(:,3)]; 
stress_flapskin = [Stress_root;Stress_span(:,1)];
plot(stress_flapskin, 'b'); hold on;
plot(stress_edgeskin, 'r'); hold on;
plot(stress_edgeskin, 'ro');
plot(stress_flapskin, 'bo');



grid on
    a = gca;
    % set box property to off and remove background color
    set(a,'box','off','color','none')
    % create new, empty axes with box but without ticks
    b = axes('Position',get(a,'Position'),'box','on','xtick',[],'ytick',[]);
    % set original axes as active
    axes(a)
    % link axes in case of zooming
    linkaxes([a b])
set(gca,'GridLineStyle','--')
set(gca,'GridAlpha',0.8)
set(gca,'TickDir','out');
axesH = gca;
axesH.XAxis.TickLabelInterpreter = 'latex';
axesH.XAxis.TickLabelFormat      = '\\textbf{%g}';
axesH.YAxis.TickLabelInterpreter = 'latex';
axesH.YAxis.TickLabelFormat      = '\\textbf{%g}';

xticks([1 2 3 4 5 6])
xticklabels({'\textbf{0}','\textbf{0.15}','\textbf{0.3}', '\textbf{0.5}','\textbf{0.75}', '\textbf{0.9}'})
xlim([0.8 6.5]);
ylim([0 120]);
ylabel('\textbf{Stresses in SNL-Triax (MPa)}','Interpreter','latex');
xlabel('\textbf{Normalized blade radius (-)}','Interpreter','latex');
legend('\textbf{$\sigma_{flap}$}','\textbf{$\sigma_{edge}$}', 'Interpreter','latex');
 