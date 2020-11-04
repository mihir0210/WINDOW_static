function Tower=Tower_pp
load([pwd,'\Tower.mat']);
%% Tower pre-processing
Tower.HubHeight=Tower_HubHeight;
Tower.BottomThickness=Tower_BottomThickness;
Tower.TopThickness=Tower_TopThickness;
Tower.Height=Tower_Height;
Tower.Mass=Tower_Mass;
Tower.Diameter=Tower_Diameter;
Tower.EI=Tower_EI;
Tower.WallThickness=Tower_WallThickness;
Tower.GJ=Tower_GJ;
Tower.EA=Tower_EA;
Tower.Iner=Tower_Iner;
Tower.ExtraMass=Tower_ExtraMass;
save([pwd,'\Tower.mat'],'Tower');
