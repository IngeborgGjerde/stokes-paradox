% This plots f'
% updated 12 oct 23
% tol should be 1+someps where someps>0 is small, e.g. 1.001

function ploteffpee(tol)
[ra fa]=effprimestopar(100,tol);
[rb fb]=effprimestopar(1000,tol);
[rc fc]=effprimestopar(10000,tol);
[rd fd]=effprimestopar(100000,tol);
[re fe]=effprimestopar(1000000,tol);
[rf ff]=effprimestopar(10000000,tol);
[rg fg]=effprimestopar(100000000,tol);
semilogx(ra,fa,"linewidth",2,rb,fb,"linewidth",2,rc,fc,"linewidth",2,rd,fd,"linewidth",2,re,fe,"linewidth",2,rf,ff,"linewidth",2,rg,fg,"linewidth",2)
title("plot of factor defining horizontal flow velocity")
xlabel("distance r from the origin")
ylabel("horizontal flow correction factor")
