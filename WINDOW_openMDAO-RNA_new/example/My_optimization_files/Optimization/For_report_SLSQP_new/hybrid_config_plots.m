%%% plots for Hybrid config %%%%

%% Static model

load('GA_mutation0.5_opt.mat');

chord_profile_GA_opt = cell2mat(Chord_profile);
twist_profile_GA_opt = Twist_profile+ 2.774201605;

points_chord_GA_opt = [chord_profile_GA_opt(1:7:end), chord_profile_GA_opt(end)] ;
points_twist_GA_opt = [twist_profile_GA_opt(1:7:end), twist_profile_GA_opt(end)];

load('hybrid_opt_static.mat');

chord_profile_hybrid = cell2mat(Chord_profile);
twist_profile_hybrid = Twist_profile+2.70045341;

points_chord_hybrid = [chord_profile_hybrid(1:7:end), chord_profile_hybrid(end)] ;
points_twist_hybrid = [twist_profile_hybrid(1:7:end), twist_profile_hybrid(end)];

normalized_radius = Blade_radius/63;
points_radius = [normalized_radius(1:7:end), normalized_radius(end)];

%% plot comparing chord : static GA vs hybrid
plot(normalized_radius, chord_profile_GA_opt, 'b-', 'LineWidth', 0.8); hold on;
plot(normalized_radius, chord_profile_hybrid, 'r-', 'LineWidth', 0.8);
plot(points_radius, points_chord_GA_opt, 'b*', 'MarkerSize',4);
plot(points_radius, points_chord_hybrid, 'r*', 'MarkerSize',4);

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

%ax.GridAlpha = 1;
ylabel('Chord distribution (m)','Interpreter','latex');
xlabel('Normalized blade radius (-)','Interpreter','latex');
legend('GA', 'Hybrid','Interpreter','latex'); 


%% plot comparing Twist : static GA vs hybrid
plot(normalized_radius, twist_profile_GA_opt, 'b-', 'LineWidth', 0.8); hold on;
plot(normalized_radius, twist_profile_hybrid, 'r-', 'LineWidth', 0.8);
plot(points_radius, points_twist_GA_opt, 'b*', 'MarkerSize',4);
plot(points_radius, points_twist_hybrid, 'r*', 'MarkerSize',4);

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

%ax.GridAlpha = 1;
ylabel('Twist distribution ($^\circ$)','Interpreter','latex');
xlabel('Normalized blade radius (-)','Interpreter','latex');
legend('GA', 'Hybrid','Interpreter','latex'); 

ylim([0 18]);




%% Dynamic model

load('dynamic_GA_opt.mat');

chord_profile_GA_opt = cell2mat(Chord_profile);
twist_profile_GA_opt = Twist_profile+ 1.17744515;

points_chord_GA_opt = [chord_profile_GA_opt(1:7:end), chord_profile_GA_opt(end)] ;
points_twist_GA_opt = [twist_profile_GA_opt(1:7:end), twist_profile_GA_opt(end)];

load('hybrid_opt_dynamic.mat');

chord_profile_hybrid = cell2mat(Chord_profile);
twist_profile_hybrid = Twist_profile+1.16654105	;

points_chord_hybrid = [chord_profile_hybrid(1:7:end), chord_profile_hybrid(end)] ;
points_twist_hybrid = [twist_profile_hybrid(1:7:end), twist_profile_hybrid(end)];

normalized_radius = Blade_radius/63;
points_radius = [normalized_radius(1:7:end), normalized_radius(end)];

%% plot comparing chord : dynamic GA vs hybrid
plot(normalized_radius, chord_profile_GA_opt, 'b-', 'LineWidth', 0.8); hold on;
plot(normalized_radius, chord_profile_hybrid, 'r-', 'LineWidth', 0.6);
plot(points_radius, points_chord_GA_opt, 'b*', 'MarkerSize',4);
plot(points_radius, points_chord_hybrid, 'r*', 'MarkerSize',4);

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

%ax.GridAlpha = 1;
ylabel('Chord distribution (m)','Interpreter','latex');
xlabel('Normalized blade radius (-)','Interpreter','latex');
legend('GA', 'Hybrid','Interpreter','latex'); 


%% plot comparing Twist : dynamic GA vs hybrid
plot(normalized_radius, twist_profile_GA_opt, 'b-', 'LineWidth', 0.8); hold on;
plot(normalized_radius, twist_profile_hybrid, 'r-', 'LineWidth', 0.8);
plot(points_radius, points_twist_GA_opt, 'b*', 'MarkerSize',4);
plot(points_radius, points_twist_hybrid, 'r*', 'MarkerSize',4);

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

%ax.GridAlpha = 1;
ylabel('Twist distribution ($^\circ$)','Interpreter','latex');
xlabel('Normalized blade radius (-)','Interpreter','latex');
legend('GA', 'Hybrid','Interpreter','latex'); 

ylim([0 20]);

