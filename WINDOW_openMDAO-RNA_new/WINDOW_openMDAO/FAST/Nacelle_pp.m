function Nacelle=Nacelle_pp
load([pwd,'\Nacelle.mat']);
%% Nacelle pre-processing
Nacelle.Hub.Length=Nacelle_Hub_Length;
Nacelle.Hub.Mass=Nacelle_Hub_Mass;
Nacelle.Hub.Overhang=Nacelle_Hub_Overhang;
Nacelle.Hub.Type=Nacelle_Hub_Type;
Nacelle.Hub.ShaftTilt=Nacelle_Hub_ShaftTilt;
Nacelle.Housing.Type=Nacelle_Housing_Type;
Nacelle.Housing.Diameter=Nacelle_Housing_Diameter;
Nacelle.Housing.Length=Nacelle_Housing_Length;
Nacelle.Housing.Mass=Nacelle_Housing_Mass;
save([pwd,'\Nacelle.mat'],'Nacelle');