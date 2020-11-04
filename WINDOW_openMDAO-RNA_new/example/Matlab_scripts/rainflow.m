function [RANGE, MEAN] = rainflow(A)

% This RAINFLOW counting function is to extract cycles from random data.
% It should be noticed that operating in real-time is not supported.
%
% INPUT
%   A: A column vector.
%
% OUTPUT
%   RAGNE: Cycles amplitudes vector;
%   MEAN:  Cycles mean values vector.
%
% REFERENCE
%   S.D. Downing and D. F. Socie, 'Simple rainflow algorithm',
%   International jounrnal of fatigue, Vol. 4, No. 1, 31-40, 1982.
%
% EXAMPLE 1
%   A = [8;6;3;2;5;10;7;5;6;7;8;10;8;4;2;3;6;0;-10];
%   The random vector is obtained from the above reference paper. It returns three minor
%   loops's with apmlitudes 5, 4 and 6 and one major loop with amplitude 20.
%
% EXAMPLE 2
%   A = [.0;.5;.6;.5;.3;.2;.6;.8;.7;.6;.8;.9;.7;.5;.8;.9;1;.8;.4;.3;.4;.5;.6;.7;.5;.4;.6;.2;.0];
%   The random vector is obtained from the paper: N. Sadowski, M. Lajoie-Mazenc, etc., 
%   'Evaluation and iron losses in electrical machines using the rain-flow method',
%   IEEE Transactions on Magnetics, Vol. 36, No. 4, 2000. 
%   Return five minor loops with amplitudes .2 .2 .4 .4 .4 and major loop with amplitude 1.
% 
% Author
%   Yu Gong ( ), gongyu2000@gmail.com.
% 
% Version
%   Last updated: 2012/2/25

clear RANGE MEAN;

valley = find(diff(sign(diff(A))) > 0) + 1;
peak = find(diff(sign(diff(A))) < 0) + 1;
Apv(1) = A(1);
Apv(2 : length(A(union(valley,peak))) + 1) = A(union(valley,peak));
Apv(end + 1) = A(end);
Apv = Apv';

if length(Apv) < 4
    RANGE = 0;
    MEAN = 0;
else
    [Cmax,Imax] = max(Apv); 
    if mod(length(Apv),2)
        if xor(Apv(1) > Apv(2), Apv(1) >= Apv(end))
            Apv(1) = [];
            Apv = circshift(Apv, 2 - Imax);
        else
            Apv(end) = [];
            Apv = circshift(Apv, 1 - Imax);
        end
    else
        if xor(Apv(1) > Apv(2), Apv(1) >= Apv(end))
            Apv(1) = [];
            Apv(end) = [];
            Apv = circshift(Apv, 2 - Imax);
        else
            Apv = circshift(Apv, 1 - Imax);
        end
    end
    Apv(end + 1) = Cmax;    

    mm = 0;
    nn = 0;
    while ~isempty(Apv)
        
        nn = nn + 1;
        E(nn) = Apv(1);
        Apv(1) = [];

        while nn >= 3
            XX = abs(E(nn) - E(nn - 1));
            YY = abs(E(nn - 1) - E(nn - 2));
            
            if XX < YY, break, end
            
            mm = mm + 1;
            RANGE(mm) = YY;
            MEAN(mm) = (E(nn - 1) + E(nn - 2))/2;
            nn = nn - 2;
            E(nn) = E(nn + 2);
        end
    end
end