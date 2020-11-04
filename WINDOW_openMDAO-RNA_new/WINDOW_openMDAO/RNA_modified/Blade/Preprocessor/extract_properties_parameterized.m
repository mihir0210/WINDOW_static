
%%%%%%% Code for extracting blade STIFFNESS and MASS properties %%%%%%%%
%[EI_flap, EI_edge, M_L] = extract_properties_parameter(1.5, 43.5, 2.82, 3.17, 6.71, 14.29, 1.11, 0.1);

load('Internal_layup.mat');

for i=1:length(le_core_span)
    [EI_flap(i), EI_edge(i), G_stiffness(i), EA(i), M_L(i),~,~,~,~,~,~]= extract_properties_parameterize(...
        span_radius(i), root_span(i), skin_span(i), le_core_span(i),...
    spar_span(i), te_core_span(i), te_reinf_span(i), web_span(i));
end

save('Preprocessor.mat','EI_flap','EI_edge','EA','G_stiffness','M_L');


