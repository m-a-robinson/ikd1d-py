% Generates golden loader output from the ORIGINAL MATLAB logic (legacy/matlab/LJMU_IKD_analyserGUI.m,
% loadButton_Callback). The data-handling statements below are copied from that function; only the
% GUI handling is removed and xlsread (needs Octave's io package) is replaced by a plain CSV read.
%
% Usage: octave --no-gui tools/octave/golden_load.m   (run from the repository root)
% Output columns: time(ms), torque, angle, velocity -- i.e. MATLAB's d(:,[TIMECOL TORQUECOL ANGLECOL VELCOL]).

data = 'tests/data/';
out  = 'tests/golden/';

% ---- Biodex (older layout; line 4 blank) ---------------------------------
for f = {'Biodex_system3_Qcon120-Hcon120', 'Biodex_system3_QNaN-Hecc120'}
    name = f{1};
    TIMECOL = 1; TORQUECOL = 2; ANGLECOL = 3; VELCOL = 4;
    d = dlmread([data name '.txt'], '', 6, 0);
    d(:,3) = [];
    csvwrite([out name '.csv'], d(:, [TIMECOL TORQUECOL ANGLECOL VELCOL]), 'precision', '%.10g');
end

% ---- Cybex ---------------------------------------------------------------
TIMECOL = 1; TORQUECOL = 3; ANGLECOL = 2; VELCOL = 4;
txt = strrep(fileread([data 'Cybex_Qcon60-Hcon60.CSV']), '"', '');
tmp = [tempname() '.csv']; fid = fopen(tmp, 'w'); fputs(fid, txt); fclose(fid);
d = dlmread(tmp, ',', 1, 0);   % stands in for xlsread's numeric block (status column is col 1)
delete(tmp);
d(:,1) = [];
d(:,1) = d(:,1)*1000;
for i = 1:length(d(:,1))-1
    if d(i,ANGLECOL) < d(i+1,ANGLECOL)
        d(i,TORQUECOL) = -d(i,TORQUECOL);
    end
end
csvwrite([out 'Cybex_Qcon60-Hcon60.csv'], d(:, [TIMECOL TORQUECOL ANGLECOL VELCOL]), 'precision', '%.10g');
