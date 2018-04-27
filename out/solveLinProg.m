function [x] = solveLinProg()
    th = 0.00001;
    A = importdata('A.txt');
    b = importdata('b.txt');
    F = importdata('F.txt');
    s = importdata('s.txt');
    
    lb = zeros(size(s,1),1);
    ub = zeros(size(s,1),1);
    
    
    for i = 1:size(s,1)
       if s(i) <= 0 lb(i) = -Inf; else lb(i) = th; end
       if s(i) < 0 ub(i) = -th; else ub(i) = Inf; end
    end    
    
   

    lb = [lb; -Inf(size(A,2)-size(s,1),1); zeros(size(A,1),1)];
    ub = [ub; Inf(size(A,2)-size(s,1),1); Inf(size(A,1),1)];
    
    S = -eye(size(A,1));
    [x, fval] = linprog(F,[A, S],b,[],[],lb,ub);
    disp(fval)
    dlmwrite('x.txt',x);
    