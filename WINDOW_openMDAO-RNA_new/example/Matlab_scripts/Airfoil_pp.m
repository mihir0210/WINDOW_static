function Airfoil=Airfoil_pp
load([pwd,'\Airfoil.mat']);
%% Airfoil pre-processing
Airfoil.Name=cell(8,1);
% Airfoil.Name{1,1}=convertCharsToStrings('Cylinder 1');
% Airfoil.Name{2,1}=convertCharsToStrings('Cylinder 2');
% Airfoil.Name{3,1}=convertCharsToStrings('DU 99-W-405');
% Airfoil.Name{4,1}=convertCharsToStrings('DU 99-W-350');
% Airfoil.Name{5,1}=convertCharsToStrings('DU 97-W-300');
% Airfoil.Name{6,1}=convertCharsToStrings('DU 91-W2-250');
% Airfoil.Name{7,1}=convertCharsToStrings('DU 93-W-210');
% Airfoil.Name{8,1}=convertCharsToStrings('NACA 64-618');

Airfoil.Name{1,1}='Cylinder 1';
Airfoil.Name{2,1}='Cylinder 2';
Airfoil.Name{3,1}='DU 99-W-405';
Airfoil.Name{4,1}='DU 99-W-350';
Airfoil.Name{5,1}='DU 97-W-300';
Airfoil.Name{6,1}='DU 91-W2-250';
Airfoil.Name{7,1}='DU 93-W-210';
Airfoil.Name{8,1}='NACA 64-618';


Airfoil.Geometry=cell(1,8);
Airfoil.Geometry{1,1}=Airfoil_Geometry1;
Airfoil.Geometry{1,2}=Airfoil_Geometry2;
Airfoil.Geometry{1,3}=Airfoil_Geometry3;
Airfoil.Geometry{1,4}=Airfoil_Geometry4;
Airfoil.Geometry{1,5}=Airfoil_Geometry5;
Airfoil.Geometry{1,6}=Airfoil_Geometry6;
Airfoil.Geometry{1,7}=Airfoil_Geometry7;
Airfoil.Geometry{1,8}=Airfoil_Geometry8;

Airfoil.Alpha=cell(1,8);
Airfoil.Alpha{1,1}=Airfoil_Alpha1;
Airfoil.Alpha{1,2}=Airfoil_Alpha2;
Airfoil.Alpha{1,3}=Airfoil_Alpha3;
Airfoil.Alpha{1,4}=Airfoil_Alpha4;
Airfoil.Alpha{1,5}=Airfoil_Alpha5;
Airfoil.Alpha{1,6}=Airfoil_Alpha6;
Airfoil.Alpha{1,7}=Airfoil_Alpha7;
Airfoil.Alpha{1,8}=Airfoil_Alpha8;

Airfoil.Cl=cell(1,8);
Airfoil.Cl{1,1}=Airfoil_Cl1;
Airfoil.Cl{1,2}=Airfoil_Cl2;
Airfoil.Cl{1,3}=Airfoil_Cl3;
Airfoil.Cl{1,4}=Airfoil_Cl4;
Airfoil.Cl{1,5}=Airfoil_Cl5;
Airfoil.Cl{1,6}=Airfoil_Cl6;
Airfoil.Cl{1,7}=Airfoil_Cl7;
Airfoil.Cl{1,8}=Airfoil_Cl8;

Airfoil.Cd=cell(1,8);
Airfoil.Cd{1,1}=Airfoil_Cd1;
Airfoil.Cd{1,2}=Airfoil_Cd2;
Airfoil.Cd{1,3}=Airfoil_Cd3;
Airfoil.Cd{1,4}=Airfoil_Cd4;
Airfoil.Cd{1,5}=Airfoil_Cd5;
Airfoil.Cd{1,6}=Airfoil_Cd6;
Airfoil.Cd{1,7}=Airfoil_Cd7;
Airfoil.Cd{1,8}=Airfoil_Cd8;

Airfoil.Cm=cell(1,8);
Airfoil.Cm{1,1}=Airfoil_Cm1;
Airfoil.Cm{1,2}=Airfoil_Cm2;
Airfoil.Cm{1,3}=Airfoil_Cm3;
Airfoil.Cm{1,4}=Airfoil_Cm4;
Airfoil.Cm{1,5}=Airfoil_Cm5;
Airfoil.Cm{1,6}=Airfoil_Cm6;
Airfoil.Cm{1,7}=Airfoil_Cm7;
Airfoil.Cm{1,8}=Airfoil_Cm8;


Airfoil.CnSlope=Airfoil_CnSlope;
Airfoil.StallAngle1=Airfoil_StallAngle1;
Airfoil.StallAngle2=Airfoil_StallAngle2;
Airfoil.CritCn1=Airfoil_CritCn1;
Airfoil.CritCn2=Airfoil_CritCn2;
save([pwd,'\Airfoil.mat'],'Airfoil');
