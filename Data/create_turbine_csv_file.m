%% create reference turbine csv file

headers = {'r','mu','thickness','chord','twist','mass','flap_inertia','edge_inertia','flap_stiffness','edge_stiffness'};

num_nodes = length(Blade.Radius);
data = zeros(num_nodes, length(headers));


data(:,1) = Blade.Radius;
data(:,2) = Blade.Radius/Blade.Radius(end);
data(:,3) = Blade.Thickness;
data(:,4) = Blade.Chord;
data(:,5) = Blade.Twist;
data(:,6) = Blade.Mass;
data(:,7) = Blade.FlapIner;
data(:,8) = Blade.EdgeIner;
data(:,9) = Blade.EIflap;
data(:,10) = Blade.EIedge;

csvwrite_with_headers('Reference_turbine_15MW.csv', data, headers);

