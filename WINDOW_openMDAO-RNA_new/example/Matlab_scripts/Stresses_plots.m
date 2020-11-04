%%%%%%%%% Plot Stress due to old and new methods
%% Plot Flapwise Skin stresses
x = [ 0.11, 0.3, 0.5, 0.75, 0.95]; 
SANDIA_flap_skin_nm = Stress_span_nm(:,1)*1.755/3.97; 
plot(x,Stress_span(:,1));
hold on; 
plot(x,Stress_span_nm(:,1));
plot(x, SANDIA_flap_skin_nm);
legend('Old method','Strain method', 'SANDIA strain method');
ylabel('Stress (MPa)');
xlabel('Span location'); 
title('Flapwise Skin Stresses');
grid on; 
%% Plot Flapwise spar stresses
SANDIA_flap_spar_nm = Stress_span_nm(:,2)*1.755/3.97; 
plot(x,Stress_span(:,2));
hold on; 
plot(x,Stress_span_nm(:,2));
plot(x, SANDIA_flap_spar_nm);
legend('Old method','Strain method', 'SANDIA strain method');
ylabel('Stress (MPa)');
xlabel('Span location'); 
title('Flapwise Spar Stresses');
grid on; 
%% Plot Edgewise skin stresses
SANDIA_edge_skin_nm = Stress_span_nm(:,3)*1.755/3.97; 
plot(x,Stress_span(:,3));
hold on; 
plot(x,Stress_span_nm(:,3));
plot(x, SANDIA_edge_skin_nm);
legend('Old method','Strain method', 'SANDIA strain method');
ylabel('Stress (MPa)');
xlabel('Span location'); 
title('Edgewise Skin Stresses');
grid on; 
%% Plot Edgewise TE REINF stresses
SANDIA_edge_te_reinf_nm = Stress_span_nm(:,4)*1.755/3.97; 
plot(x,Stress_span(:,4));
hold on; 
plot(x,Stress_span_nm(:,4));
plot(x, SANDIA_edge_te_reinf_nm);
legend('Old method','Strain method', 'SANDIA strain method');
ylabel('Stress (MPa)');
xlabel('Span location'); 
title('Edgewise TE Reinf Stresses');
grid on; 