
figure(1)
plot(RootMEdg3); hold on;
xlabel('Time series');
ylabel('Blade edgewise moment (KNm)');
% title('Blade edgewise moment vs Time');
max_edgewise_1=max(abs(RootMEdg1));
max_edgewise_2=max(abs(RootMEdg2));
max_edgewise_3=max(abs(RootMEdg3));
xlim([0 length(RootMFlp2)]);
figure(2)
plot(RootMFlp2); hold on;
xlabel('Time series');
ylabel('Blade flapwise moment (KNm)');
% title('Blade flapwise moment vs Time');
max_flapwise_1=max(RootMFlp1);
max_flapwise_2=max(RootMFlp2);
max_flapwise_3=max(RootMFlp3);
xlim([0 length(RootMFlp2)]);

%% Calculate stress at 3 points
% point 1 is max y for flapwise
% point 2 is max y for edgewise
% point 3 is at 45 degrees
I=0.579; %m^4 at first section of root
y=2.105; % max distance from neutral axes for point 1 and 2
y_45=y*sind(45); % max distance for point 3

Stress_1=RootMFlp3*y*10^3/I/(10^6); % same for 1 and 2
Stress_2=RootMEdg3*y*10^3/I/(10^6); 
Stress_3=Stress_1*y_45/y + Stress_2*y_45/y; 
Stress_flapwise=max(Stress_1);
Stress_edgewise=max(Stress_2);
Stress_45=max(Stress_3);

%% plot stresses
% plot(Stress_1,'b'); hold on;
%plot(Stress_2,'b');
plot(Stress_3,'b');

xlabel('Time series');
ylabel('Stress (MPa)');
% title('Stress vs Time');
%legend('Stress due to Flapwise Moment', 'Stress due to Edgewise moment',...
    %'Stress at 45 degree point');
legend('Stress due to Flapwise Moment'); 
xlim([0 length(RootMFlp2)]);
% %% calculate stress cycle for rainflow
% I=6.6; 
% y=1.7; 
% Stress_flapwise=RootMFlp3*y*1000/I/(10^6);
% plot(Stress_flapwise);

%% PLOT Delflection
oop1_max=max(OoPDefl1);
oop2_max=max(OoPDefl2);
oop3_max=max(OoPDefl3);
plot(OoPDefl3,'r');
xlabel('Time series');
ylabel('Tip Deflection (m)');
% title('Tip Delfection vs Time');
xlim([0 length(RootMFlp2)]);

%% rainflow
[Range,Mean]=rainflow(Stress_3);
Range(Range==0)=[];
upper=ceil(max(Range));
hist=histogram(Range,upper); 
ylabel('Number of Occurences');
xlabel('Stress Range (MPa)');

bincounts= histc(Range,0:upper-1);
abs_value=zeros(1,upper);
x=-0.5;
for i=1:upper
    abs_value(i)=x+i;
end

%% Determine cycles to failure from S-N
UCS=900; % ultimate compressive in MPa
N_failure=10.^(9*(log10(UCS)-log10(abs_value)));

Eq_damage=sum(bincounts./N_failure);

Total_damage=Eq_damage*PDF(23.5)*8760*6*20;

%% FFT mihir
A=Stress_1; %flapwise
B=Stress_2; %edgewise
C=Stress_3; % 45 degree
L=length(B);         % Length of signal
Fs = 125;            % Sampling frequency                    
T = 1/Fs;             % Sampling period       
Y = fft(B);

P2 = abs(Y);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);
n=1000; % plot first n points only
f = Fs*(0:L/2)/L;
semilogy(f(1:n),P1(1:n));
title('Single-Sided Amplitude Spectrum of X(t)')
xlabel('f (Hz)')
ylabel('|P1(f)|')             

%% FFT husain
A=Stress_3;
N=length(A);
fs=125; 
fnyquist=fs/2;
B=abs(fft(A));
plot(B)

bin_vals=0:N-1;
fax_hz=bin_vals*fs/N;
N_2=ceil(N/2);
plot(fax_hz(N_2:end)/60,B(N_2:end), 'r');
xlabel('Frequency (Hz) ');
ylabel('Magnitude');

%% fft sukanya
Fs= 600;            % Sampling frequency                    
T = 1/Fs;             % Sampling period       
L = 75001;             % Length of signal
t = (0:L-1)*T;% Time Vector
Y = fft(A);
P2 = abs(Y);
P1 = P2(1:L/2+1);
f=linspace(0,Fs/2,L/2+1);
% f = Fs*(0:(L/2))/L;
plot(P2);

% semilogy(f,P1,'linewidth',1);
title('Amplitude Spectrum for Out of Plane Root Moment')
xlabel('f (Hz)')
ylabel('|P1(f)|')

%% fft internet
Fs=125; %  
L=length(A);
N=ceil(log2(L));
FFTherm=fft(A,2^N);
f=(Fs/2^N)*(0:2^(N-1)-1);
Power=FFTherm.*conj(FFTherm);
figure(3);
plot(abs(Power))
figure,
semilogy(f,Power(1:2^(N-1)))
xlabel('  Frequency (Hz)'), ylabel(' Magnitude (w)'),
title('  Power Spectral Density'), grid on;


%% plot
plot S-N
N_new=fliplr(N_failure);
m=-1/9;
x=log10(N_new);
c=log10(900);
y=10.^(m*x+c);
plot(x,log10(y));

