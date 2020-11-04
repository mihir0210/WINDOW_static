%% plot SANDIA layup 

%%%% number of layers %%%
load('Internal_layup.mat');

section = span_radius/61.5;
le_core = le_core_span/1;
te_core = te_core_span/1;
spar_thickness = spar_span/0.47;
te_reinf_thickness = te_reinf_span/0.47;
skin = skin_span/0.94;
root_skin = root_span/0.94;

root_skin = [root_skin(1) root_skin];
skin = [skin(1) skin skin(end)];

section_root = [0 section];
section_skin = [0 section 1];
%% plot
plot( section, le_core, 'LineWidth', 0.8); hold on;
plot( section, te_core, 'LineWidth', 0.8);
plot( section, spar_thickness, 'LineWidth', 0.8);
plot( section, te_reinf_thickness, 'LineWidth', 0.8);
plot( section_skin, skin, 'LineWidth', 0.8);
plot( section_root, root_skin, 'LineWidth', 0.8);


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

%ax.GridAlpha = 1;
ylabel('\textbf{Number of layers}','Interpreter','latex');
xlabel('\textbf{Normalized blade radius (-)}','Interpreter','latex');
legend('\textbf{LE foam}','\textbf{TE foam}', '\textbf{UD-C}', '\textbf{UD-G}', '\textbf{Triax-skin}', '\textbf{Triax-root}');

ylim([0 100]);