function Preprocessing_new(type)
%For linearization
if type==1
    Airfoil=Airfoil_pp;
    Blade=Blade_pp;
    Control=Control_pp;
    Drivetrain=Drivetrain_pp;
    Nacelle=Nacelle_pp;
    Tower=Tower_pp;
end

%Before Certification
if type==3
    CertificationSettings=CertificationSettings_pp;
    save([pwd,'CertificationSettings.mat','CertificationSettings']);
    Turbine_properties=[pwd,'\WT_design.mat'];
    load([pwd,'\Airfoil.mat']);
    load([pwd,'\Blade.mat']);
    load([pwd,'\CertificationSettings.mat']);
    load([pwd,'\Control.mat']);
    load([pwd,'\Drivetrain.mat']);
    load([pwd,'\Nacelle.mat']);
    load([pwd,'\Tower.mat']);
    save(Turbine_properties,'Airfoil','Blade','CertificationSettings','Control','Drivetrain','Nacelle','Tower');
    
end
