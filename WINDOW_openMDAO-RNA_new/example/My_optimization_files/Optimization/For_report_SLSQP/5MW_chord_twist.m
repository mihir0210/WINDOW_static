%% 
load('static_sp1_init.mat');

chord_profile_sp1_init = cell2mat(Chord_profile);
twist_profile_sp1_init = Twist_profile+0.098;

points_chord_sp1_init = [chord_profile_sp1_init(1:7:end), chord_profile_sp1_init(end)] ;
points_twist_sp1_init = [twist_profile_sp1_init(1:7:end), twist_profile_sp1_init(end)];

% for chord - root, 70 and 90%
normalized_blade = Blade_radius/63;
chord_root = chord_profile_sp1_init(1);

diff_70 = abs(normalized_blade-0.7);
diff_90 = abs(normalized_blade-0.9);
I = find(diff_70==min(diff_70));
J = find(diff_90==min(diff_90));

chord_70 = chord_profile_sp1_init(I);
chord_90 = chord_profile_sp1_init(J);

points_chord = [chord_root, chord_70, chord_90];
points_radius = [normalized_blade(1), normalized_blade(I), normalized_blade(J)];

figure(1)
plot(normalized_blade, chord_profile_sp1_init,'b-'); hold on;
%plot(normalized_blade, twist_profile_sp1_init); 
plot(points_radius, points_chord,'b*');


grid on
set(gca,'GridLineStyle','--')
set(gca,'GridAlpha',0.8)
set(gca,'TickDir','out');

%ax.GridAlpha = 1;
ylabel('Chord distribution (m)','Interpreter','latex');
xlabel('Normalized blade radius (-)','Interpreter','latex');

%% plot twist
transition = normalized_blade(8); 
diff_40 = abs(normalized_blade-0.4);
diff_70 = abs(normalized_blade-0.7);
I = find(diff_40==min(diff_40));
J = find(diff_70==min(diff_70));

twist_transition = twist_profile_sp1_init(8); 
twist_40 = twist_profile_sp1_init(I);
twist_70 = twist_profile_sp1_init(J);

points_twist = [twist_transition, twist_40, twist_70];
points_radius = [transition, normalized_blade(I), normalized_blade(J)];

figure(2)
plot(normalized_blade, twist_profile_sp1_init,'r-'); hold on;
%plot(normalized_blade, twist_profile_sp1_init); 
plot(points_radius, points_twist,'r*');


grid on
set(gca,'GridLineStyle','--')
set(gca,'GridAlpha',0.8)
set(gca,'TickDir','out');

%ax.GridAlpha = 1;
ylabel('Twist distribution ($^\circ$)','Interpreter','latex');
xlabel('Normalized blade radius (-)','Interpreter','latex');

