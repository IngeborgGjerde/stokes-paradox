% updated 12 oct 23
t=[
%radius    ten    twenty  thirty  meshsize
1.00e+02  0.5340  0.3711  0.2847    64
2.00e+02  0.6008  0.4553  0.3711    64
%4.00e+02  0.6497  0.5248  0.4474    64
4.00e+02  0.6519  0.5220  0.4476    128
8.00e+02  0.6942  0.5760  0.5094    128
1.60e+03  0.7267  0.6208  0.5584    128
3.20e+03  0.7529  0.6553  0.6014    128
1.00e+04  0.7950  0.7162  0.6636    128
];
r=t(:,1);
a=t(:,2);
b=t(:,3);
c=t(:,4);
semilogx(r,a,"linewidth",3,r,b,"linewidth",3,r,c,"linewidth",3)
set(gca, "linewidth", 1, "fontsize", 16)
title("Fraction (17) versus box size")
xlabel("box size b")
ylabel("recirculation zone fraction")
text(200,0.69,"d=10","fontsize",16)
text(500,0.63,"d=20","fontsize",16)
text(1200,0.5,"d=30","fontsize",16)
