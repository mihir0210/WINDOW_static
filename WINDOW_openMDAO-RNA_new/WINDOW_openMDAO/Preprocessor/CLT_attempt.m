%%%%%%% Implement CLT for post processing of Root Skin %%%%%%
%% skin properties
E11=27700*1e6; % Along Fibre direction
E22=13650*1e6; % Perpendicular to fibre direction 
G12=7200*1e6; 
v12=0.39; 


%% Reduced Stiffness Matrix
Q11= E11^2/(E11-v12*E22);
Q12=v12*E11*E22/(E11-v12^2*E22);
Q22=E11*E22/(E11-v12^2*E22);
Q66=G12;

%%%% TRIAX SKINS ARE MADE UP OF +45, -45 AND 0 
% For the +45 ply 
theta = 0;
c=cosd(theta);
s=sind(theta);
Q11_= Q11*c^4+2*(Q12+2*Q66)*c^2*s^2+Q22*s^4;
Q12_= Q12*c^4+s^4+(Q11+Q22-4*Q66)*c^2*s^2;
Q16_= (Q11-Q12-2*Q66)*c^3*s - (Q22-Q12-2*Q66)*c*s^3;
Q22_= Q11*s^4+2*(Q12+2*Q66)*c^2*s^2 + Q22*c^4;
Q26_= (Q11-Q12-2*Q66)*c*s^3 - (Q22-Q12-2*Q66)*c^3*s;
Q66_= (Q11+Q22-2*Q12-2*Q66)*c^2*s^2 + Q66*(c^4+s^4);

Q_=[Q11_ Q12_ Q16_; Q12_ Q22_ Q26_; Q16_ Q26_ Q66_];

t_eq_sc=0.0577; %in m
zk=t_eq_sc;
z_k_1=zk-0.94; 

A = Q_*(zk-z_k_1);
B = 0.5*Q_*(zk^2-z_k_1^2);
D = (1/3)*Q_*(zk^3-z_k_1^3);


ABD = [A B; B D];
abd = inv(ABD);

%% MULTIPLY abd with force and moment matrix to get mid plain strains and laminate curvature for each ply
Nxx=0;
Nyy=0;
Nxy=0;
Mxx=0;
Myy=13600*1e3; % Max flapwise moment in Nm
Mxy=0;
f_m = [Nxx; Nyy; Nxy; Mxx; Myy; Mxy]; %%% Force & Moment matrix

s_k = abd*f_m; %% Strain and curvature matrix 


%% Ply strains in the x-y co-ordinate system

strain = [s_k(1); s_k(2); s_k(3)] + zk*[s_k(4);s_k(5); s_k(6)]; 


%% Ply Stresses in the x-y co-ordinate system

stess = Q_*strain;