t=[
%radius     ten   twenty  thirty  meshsize
1.00e+02  0.4820  0.3355  0.2574    64
2.00e+02  0.5504  0.4168  0.3397    64
%4.00e+02  0.6069  0.4837  0.4129    64
4.00e+02  0.6023  0.4826  0.4127    128
8.00e+02  0.6443  0.5347  0.4742    128
1.60e+03  0.6785  0.5830  0.5272    128
3.20e+03  0.7108  0.6186  0.5676    128
1.00e+04  0.7779  0.7014  0.6498    128
];
r=t(:,1);
a=t(:,2);
b=t(:,3);
c=t(:,4);
semilogx(r,a,"linewidth",3,r,b,"linewidth",3,r,c,"linewidth",3)
set(gca, "linewidth", 1, "fontsize", 16)
%title("Growth of (17) as a function of box size")
title("Fraction (17) versus box size")
xlabel("box size b")
ylabel("recirculation zone fraction")
text(200,0.64,"d=10","fontsize",16)
text(500,0.585,"d=20","fontsize",16)
text(1200,0.48,"d=30","fontsize",16)

