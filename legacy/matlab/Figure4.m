% ****** Figure4.m ****** Generates Figure 4 for 
% "IKD1D: an open source application tool for non-reductionist isokinetic 
% dynamometry analysis of torque-angle profile analyses"

% This matlab script uses Mean/Standard Devation and independent t-test 
% functions using SPM1D toolkit - download Matlab source code from
% www.SPM1D.org and ensure it is on Matlab path.

% Ensure folder is pointing to the path containing the following text file
data = load('MalesFemales_IKD_Polynomials.txt');

% Generate figure 4a using SPM1D plot_meanSD function
a1=subplot(2,1,1);
p1 =spm1d.plot.plot_meanSD(data(1:10,:),'color','c'); %Female data
xlabel('Joint Angle(degrees)');
ylabel('Torque (Nm)');
xlim([0 65]);
a1.XTickMode = ' manual';
a1.XTick = [0 15 30 45 60];
a1.XTickLabel ={'25', '40', '55', '70', '85'};
hold on
p2  = spm1d.plot.plot_meanSD(data(11:20,:),'color','b'); %Male data
x = -6; y = 250;txt = 'A';
t = text(x,y,txt,'HorizontalAlignment','right')
t.FontSize=20;
l=legend([p2 p1],'Mean Males', 'Mean Females', 'Location' ,'northwest');

% Do independent t-test using SPM1D toolkit
alpha = 0.05;
t  = spm1d.stats.ttest2(data(11:20,:),data(1:10,:)); % Females vs Males
ti = t.inference(alpha);
% and plot as Figure 4 b
a2=subplot(2,1,2)
p3=ti.plot();
xlabel('Joint Angle(degrees)');
xlim([0 65]);
a2.XTickMode = ' manual';
a2.XTick = [0 15 30 45 60];
a2.XTickLabel ={'25', '40', '55', '70', '85'};
a2.Box ='on';
x = 57; y = 3.2; txt = 'p = 0.0076';
text(x,y,txt,'HorizontalAlignment','right');
x = -6; y = 4;txt = 'B';
t = text(x,y,txt,'HorizontalAlignment','right')
t.FontSize=20;

%tidy up figure
f=gcf;
f.NumberTitle = 'off';
f.Name = 'Figure 4';
f.Position = [28 178 594 754];


