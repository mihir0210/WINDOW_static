%% Hard coded slopes

airfoil_change =logical([0; diff(Blade.NFoil)]); % Logical array of change in airfoil geometries
airfoil_transition_index = [1;find(airfoil_change)]; % Index where transition happens
span_airfoil_change = [Blade.Radius(1);Blade.Radius(airfoil_change)]; % Locations along blade where airfoil changes

airfoil_transition_index(find(airfoil_transition_index<J,1,'last'));

slope = zeros(7,399);

for i =1:7
    slope(i,:) = (Airfoil.Geometry{1,i+1}(2,:)- Airfoil.Geometry{1,i}(2,:))/...
        (span_airfoil_change(i+1)- span_airfoil_change(i));
end

delta_x =Blade.Radius(J) - Blade.Radius(airfoil_transition_index(find(airfoil_transition_index<J,1,'last')));
% First find where the particular point lies with respect to nearest
% airfoil change (previous) and take different of the radii of both to get8
% x distance between two and multiply by the respective section slope

previous_airfoilno = Blade.NFoil(airfoil_transition_index(find(airfoil_transition_index<J,1,'last')));

% Find the previous airfoil ID where transition occured
% slope of that number is the slope of that section 

naya_daur =[Airfoil.Geometry{1,previous_airfoilno}(1,:);(Airfoil.Geometry{1,previous_airfoilno}(2,:) + slope(previous_airfoilno,:)*delta_x)];
