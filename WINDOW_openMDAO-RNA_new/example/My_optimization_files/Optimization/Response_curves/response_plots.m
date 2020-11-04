%% take data

chord_data = xlsread('Response.xlsx', 'Chord', 'B3:J9');
twist_data = xlsread('Response.xlsx', 'Twist', 'B3:J9');
tf_data = xlsread('Response.xlsx', 'Thickness_Factor', 'B3:J9');
tsr_data = xlsread('Response.xlsx','TSR','B3:J10');
pitch_data = xlsread('Response.xlsx', 'fine_pitch', 'B5:J10');

%% plot all chord curves
chord_coeff  = chord_data(:,1);
lcoe = chord_data(:,2);
tip_deflection = chord_data(:,4);
flapwise_ud = chord_data(:,6);
edgewise_skin = chord_data(:, 8);


figure(1)
plot(chord_coeff, lcoe); 
xlabel('Normalized Chord Coefficients', 'Interpreter', 'Latex'); 
ylabel('L.C.O.E.', 'Interpreter', 'Latex'); 
grid on;
set(gca,'GridLineStyle','--')

figure(2)
plot(chord_coeff, tip_deflection); 
xlabel('Normalized Chord Coefficients', 'Interpreter', 'Latex'); 
ylabel('Tip Deflection (m)', 'Interpreter', 'Latex'); 
grid on;
set(gca,'GridLineStyle','--')

figure(3)
plot(chord_coeff, flapwise_ud); 
xlabel('Normalized Chord Coefficients', 'Interpreter', 'Latex'); 
ylabel('Flapwise UD stress (MPa)', 'Interpreter', 'Latex'); 
grid on;
set(gca,'GridLineStyle','--')

figure(4)
plot(chord_coeff, edgewise_skin); 
xlabel('Normalized Chord Coefficients', 'Interpreter', 'Latex'); 
ylabel('Edgewise skin stress (MPa)', 'Interpreter', 'Latex'); 
grid on;
set(gca,'GridLineStyle','--')
ylim([0 120]);


%% plot all twist curves
twist_coeff  = twist_data(:,1);
lcoe = twist_data(:,2);
tip_deflection = twist_data(:,4);
flapwise_ud = twist_data(:,6);
edgewise_skin = twist_data(:, 8);


figure(1)
plot(twist_coeff, lcoe); 
xlabel('Normalized Twist Coefficients', 'Interpreter', 'Latex'); 
ylabel('L.C.O.E.', 'Interpreter', 'Latex'); 
grid on;
set(gca,'GridLineStyle','--')

figure(2)
plot(twist_coeff, tip_deflection); 
xlabel('Normalized Twist Coefficients', 'Interpreter', 'Latex'); 
ylabel('Tip Deflection (m)', 'Interpreter', 'Latex'); 
grid on;
set(gca,'GridLineStyle','--')
ylim([4 5])

figure(3)
plot(twist_coeff, flapwise_ud, '+'); 
xlabel('Normalized Twist Coefficients', 'Interpreter', 'Latex'); 
ylabel('Flapwise UD stress (MPa)', 'Interpreter', 'Latex'); 
grid on;
set(gca,'GridLineStyle','--')
ylim([350 450])

figure(4)
plot(twist_coeff, edgewise_skin); 
xlabel('Normalized Twist Coefficients', 'Interpreter', 'Latex'); 
ylabel('Edgewise skin stress (MPa)', 'Interpreter', 'Latex'); 
grid on;
set(gca,'GridLineStyle','--')
ylim([0 120]);

%% Plot all Thickness factor curves 

tf  = tf_data(:,1);
lcoe = tf_data(:,2);
tip_deflection = tf_data(:,4);
flapwise_ud = tf_data(:,6);
edgewise_skin = tf_data(:, 8);


figure(1)
plot(tf, lcoe); 
xlabel('Thickness Factor', 'Interpreter', 'Latex'); 
ylabel('L.C.O.E.', 'Interpreter', 'Latex'); 
grid on;
set(gca,'GridLineStyle','--')

figure(2)
plot(tf, tip_deflection); 
xlabel('Thickness Factor', 'Interpreter', 'Latex'); 
ylabel('Tip Deflection (m)', 'Interpreter', 'Latex'); 
grid on;
set(gca,'GridLineStyle','--')

figure(3)
plot(tf, flapwise_ud); 
xlabel('Thickness Factor', 'Interpreter', 'Latex'); 
ylabel('Flapwise UD stress (MPa)', 'Interpreter', 'Latex'); 
grid on;
set(gca,'GridLineStyle','--')

figure(4)
plot(tf, edgewise_skin); 
xlabel('Thickness Factor', 'Interpreter', 'Latex'); 
ylabel('Edgewise skin stress (MPa)', 'Interpreter', 'Latex'); 
grid on;
set(gca,'GridLineStyle','--')
ylim([0 120]);


%% Plot all fine pitch curves 
fine_pitch = pitch_data(:,1);
lcoe = pitch_data(:,2);
tip_deflection = pitch_data(:,4);
flapwise_ud = pitch_data(:,6);
edgewise_skin = pitch_data(:, 8);


figure(1)
plot(fine_pitch, lcoe); 
xlabel('Fine Pitch', 'Interpreter', 'Latex'); 
ylabel('L.C.O.E.', 'Interpreter', 'Latex'); 
grid on;
set(gca,'GridLineStyle','--')

figure(2)
plot(fine_pitch, tip_deflection); 
xlabel('Fine Pitch', 'Interpreter', 'Latex'); 
ylabel('Tip Deflection (m)', 'Interpreter', 'Latex'); 
grid on;
set(gca,'GridLineStyle','--')

figure(3)
plot(fine_pitch, flapwise_ud); 
xlabel('Fine Pitch', 'Interpreter', 'Latex'); 
ylabel('Flapwise UD stress (MPa)', 'Interpreter', 'Latex'); 
grid on;
set(gca,'GridLineStyle','--')

figure(4)
plot(fine_pitch, edgewise_skin); 
xlabel('Fine Pitch', 'Interpreter', 'Latex'); 
ylabel('Edgewise skin stress (MPa)', 'Interpreter', 'Latex'); 
grid on;
set(gca,'GridLineStyle','--')
ylim([0 120]);


%% Plot all TSR curves

tsr = tsr_data(:,1);
lcoe = tsr_data(:,2);
tip_deflection = tsr_data(:,4);
flapwise_ud = tsr_data(:,6);
edgewise_skin = tsr_data(:, 8);


figure(1)
plot(tsr, lcoe); 
xlabel('TSR', 'Interpreter', 'Latex'); 
ylabel('L.C.O.E.', 'Interpreter', 'Latex'); 
grid on;
set(gca,'GridLineStyle','--')

figure(2)
plot(tsr, tip_deflection); 
xlabel('TSR', 'Interpreter', 'Latex'); 
ylabel('Tip Deflection (m)', 'Interpreter', 'Latex'); 
grid on;
set(gca,'GridLineStyle','--')

figure(3)
plot(tsr, flapwise_ud); 
xlabel('TSR', 'Interpreter', 'Latex'); 
ylabel('Flapwise UD stress (MPa)', 'Interpreter', 'Latex'); 
grid on;
set(gca,'GridLineStyle','--')

figure(4)
plot(tsr, edgewise_skin); 
xlabel('TSR', 'Interpreter', 'Latex'); 
ylabel('Edgewise skin stress (MPa)', 'Interpreter', 'Latex'); 
grid on;
set(gca,'GridLineStyle','--')
ylim([0 120]);



