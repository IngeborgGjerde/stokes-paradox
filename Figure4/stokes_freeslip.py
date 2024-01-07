"""This program solves Stokes' paradox
on a domain defined by a big disk having a unit disc removed,  
with Navier boundary conditions with beta=0 given by u=(1,0) on the circle.
"""

from mshr import *
from dolfin import *
import sys, math
from timeit import default_timer as timer
startime=timer()


set_log_active(False)

pdeg=4
meshsize=int(sys.argv[1])
rad=float(sys.argv[2])
hafrad=0.5*(rad+1.0)
hrs=hafrad*hafrad
#hrt=teerad*teerad
segs=meshsize
#segs=2*meshsize
h=1.0/float(meshsize)
Kluge=100000
row=10000.0

# Create mesh and define function space
domain = Rectangle(dolfin.Point(-rad,-rad),dolfin.Point(rad,rad)) \
        -Circle(dolfin.Point(0.0, 0.0),1.0,segs) 

# Create mesh and define function space
mesh   = generate_mesh(domain, meshsize)
hmax=mesh.hmax()
x = SpatialCoordinate(mesh)

n = FacetNormal(mesh)
V = VectorFunctionSpace(mesh, "Lagrange", pdeg)
W = FunctionSpace(mesh, "Lagrange", pdeg)

def outboundary(x):
    return x[0] < -rad*(1.0-100.0*DOLFIN_EPS) or x[0] > rad*(1.0-100.0*DOLFIN_EPS) \
        or x[1] < -rad*(1.0-100.0*DOLFIN_EPS) or x[1] > rad*(1.0-100.0*DOLFIN_EPS) 
uf = Expression(("0.5*(1.0-tanh((3.0/hr)*(x[0]*x[0]+x[1]*x[1]-hr)))","0.0"),hr=hrs,degree=6)
uff=project(uf,V)
#plot(uff[0], interactive=True)
nucut = Expression("0.5*(1.0-tanh(20.0*(x[0]*x[0]+x[1]*x[1]-hr*hr)))",hr=10.0,degree=6)
nuctf=project(nucut,W)
nucuta = Expression("0.5*(1.0-tanh(20.0*(x[0]*x[0]+x[1]*x[1]-hr*hr)))",hr=20.0,degree=6)
nuctfa=project(nucuta,W)
nucutb = Expression("0.5*(1.0-tanh(20.0*(x[0]*x[0]+x[1]*x[1]-hr*hr)))",hr=30.0,degree=6)
nuctfb=project(nucutb,W)
#cutof = Expression("0.5*(1.0+tanh((20.0/hr)*(x[0]*x[0]+x[1]*x[1]-hr)))",hr=hrt,degree=6)
#ctoff=project(cutof,W)
#plot(ctoff, interactive=True)
#mass=assemble(nuctf*dx)
masq=assemble(nuctf*nuctf*dx)
masqa=assemble(nuctfa*nuctfa*dx)
masqb=assemble(nuctfb*nuctfb*dx)
uz = Expression(("0.0","0.0"),degree=6)
ui = Expression(("1.0","0.0"),degree=6)
uif=project(ui,V)

# Define boundary condition
bco= DirichletBC(V, uz, outboundary)
bcz= DirichletBC(V, uz, "on_boundary")

# Define variational problem
u = TrialFunction(V)
v = TestFunction(V)
f = Expression(("0.0","0.0"))
nn = Expression(("x[0]","x[1]"),degree=6)

a = inner(grad(u),grad(v))*dx + (0.5*(1.0-tanh(Kluge*(inner(x,x)-2.0))) \
    /(-inner(n,x)-sqrt(abs(1.0-inner(x,x)+inner(n,x)*inner(n,x)))))*inner(u,nn)*inner(nn,v)*ds

L = -inner(grad(uff),grad(v))*dx 

# Compute solution equal to zero on cylinder
u = Function(V)
solve(a == L, u, bco)
#plot(u[0], interactive=True)
u.vector().axpy(1.0, uff.vector())
# Plot solution
#plot(u[0], interactive=True)

us = TrialFunction(V)
vs = TestFunction(V)
w = Function(V)
    
#print "   starting Helmholtz projection   "
ast = inner(grad(us), grad(vs))*dx + row*div(us)*div(vs)*dx 
bs = row*div(u)*div(vs)*dx - div(w)*div(vs)*dx
#F = inner(grad(uold), grad(v))*dx+reno*inner(grad(uold)*uold,v)*dx
us = Function(V)
pde = LinearVariationalProblem(ast, bs, us, bcz)
solver = LinearVariationalSolver(pde)
# Scott-Vogelius iterated penalty method
iters = 0; max_iters = 10; div_u_norm = 1
while iters < max_iters and div_u_norm > 1e-7:
# solve and update w
    solver.solve()
#   plot(us[0], interactive=True)
    us.vector().axpy(-1.0, u.vector())
    w.vector().axpy(row, us.vector())
# find the L^2 norm of div(us) to check stopping condition
    div_u_norm = sqrt(assemble(div(us)*div(us)*dx(mesh)))
#       print "   IPM iter_no=",iters,"div_u_norm="," %.2e"%div_u_norm
#   print "   IPM iter_no=",iters,"div_u_norm="," %.6e"%div_u_norm
    iters += 1

masu =sqrt(assemble(nuctf*nuctf*(us[0]*us[0]+us[1]*us[1])*dx))
masua=sqrt(assemble(nuctfa*nuctfa*(us[0]*us[0]+us[1]*us[1])*dx))
masub=sqrt(assemble(nuctfb*nuctfb*(us[0]*us[0]+us[1]*us[1])*dx))
masrat =masu/sqrt(masq)
masrata=masua/sqrt(masqa)
masratb=masub/sqrt(masqb)
print " radius "," ten  ","  twenty","  thirty ","   meshsize"
print "%.2e"%rad," %.4f"%masrat," %.4f"%masrata," %.4f"%masratb,"  ",meshsize
aftersolveT=timer()
totime=aftersolveT-startime

print "method","pdeg","  segs"," mesh","  hmax "," IPM iters","end div u"," time"
print "polygon","&",pdeg," & ",segs," & ",meshsize," & %.3f"%hmax, \
  " & ",iters," & %.2e"%div_u_norm," & %.2f"%totime,"\\\\"
# Plot solution
#plot(-us[0]-ui[0], interactive=True)
plot(-us[0], interactive=True)
uplus = Function(V)
uplus.vector().axpy(-1.0, us.vector())
plot(uplus, interactive=True)
File("ub4.pvd") << uplus

#plot(-nuctf*us[0], interactive=True)
