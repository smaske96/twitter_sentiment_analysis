function [x] = solveLinProg()
    A = importdata('A.txt');
    b = importdata('b.txt');
    F = importdata('F.txt');

    lb = [-Inf(size(A,2),1); zeros(size(A,1),1)];
    ub = Inf(size(A,2)+size(A,1),1);
    
    S = -eye(size(A,1));
    [x, fval] = linprog(F,[A, S],b,[],[],lb,ub);
    disp(fval)
    dlmwrite('x.txt',x);
    