% This plots f'
% updated 12 oct 23
% b is the size of the circle domain
% tol should be 1+someps where someps>0 is small
function [r fp]=effprimestopar(b,tol)
jay=ceil(log(b)/log(tol));
kj=1;
for i=1:jay
    r(i)=kj;
    kj=tol*kj;
end
r(jay+1)=b;
C=1/(2+2*b^2*(log(b)-1)+ 2*log(b));
B=-2*(1+b^2)*C;
A=0.5*B+C;
D=1-0.5*B-2*C;
A_B_C_D=[A B C D];
fp=-A*r.^(-2) + B+B*log(r)+3*C*r.^2+D;
fp=(1+(1.5/(log(b)))*log(r)).*fp;
%fp=fp+(1/(log(b)))*(0.5+log(r));
%fp=(1/log(b))*fp;
%semilogx(r,fp)
