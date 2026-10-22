% ****** Figure3.m ******
%
% Generates Figure 3 for  "IKD1D: an open source application tool for
% non-reductionist isokinetic dynamometry analysis of torque-angle profile
% analyses"

% Ensure folder is pointing to the path containing the following text files
WindowingAverage = load('AvgWdw.txt');
WindowingAverage_modified = load('AvgWdw_Mod.txt');
PolynomialAverage = load('PolyAvg.txt');
PolynomialAverage_modified = load('PolyAvg_Mod.txt');

% Generate figure 3a 
a1=subplot(2,1,1)
p1=plot(WindowingAverage(1:10,:)', 'k');
hold on
p2=plot(PolynomialAverage(11,:)', '--r', 'LineWidth', 3);
p3=plot(WindowingAverage(11,:)','b', 'LineWidth', 3);
xlabel('Joint Angle(degrees)');
ylabel('Torque (Nm)');
x = -10; y = 250;txt = 'A';
t = text(x,y,txt,'HorizontalAlignment','right')
t.FontSize=20;
l=legend([p3 p2],'Averaged window', 'Polynomial equation', 'Location' ,'northwest');

% Generate figure 3b 
a2=subplot(2,1,2)
p4=plot(WindowingAverage_modified(1:10,:)', 'k');
hold on
p5=plot(PolynomialAverage_modified(11,:)','--r', 'LineWidth', 3);
p6=plot(WindowingAverage_modified(11,:)', 'b', 'LineWidth', 3);
xlabel('Joint Angle(degrees)');
ylabel('Torque (Nm)');
x = -10; y = 250;txt = 'B';
t = text(x,y,txt,'HorizontalAlignment','right')
t.FontSize=20;
l=legend([p6 p5],'Averaged window', 'Polynomial equation', 'Location' ,'northwest');

%tidy up figure
f=gcf;
f.NumberTitle = 'off';
f.Name = 'Figure 3';
f.Position = [28 178 594 754];