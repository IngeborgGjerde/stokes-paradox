from fenics import *

def stokes(mesh, boundary_markers, params, gamma, u_bc, up_init, f, f_gamma):
    '''
    Solve the Stokes equations with slip boundary conditions using Nitsche's method

    Args:
        mesh (fenics mesh): domain mesh
        boundary markers (facetfunction): domain boundary markers 
        params (dict):
            beta (float): cylinder friction parameter
            nu (float): fluid viscosity
            normal choice (str): whether to use 'discrete normal' (i.e. from mesh) or 
                                'projected/exact normal' (which we know analytically)
            degree (int): poynomial degree of approximation space 
        u_bc (Pk function): flux boundary condition
        up_init (Pk-Pk-R function): initial guess for Newton solver
        f_gamma: right-hand side of momentum balance equation
        f (function): right-hand side of conservation equation

    Returns:
        u (P2 function): flux solution
        p (P1 function): pressure solution
        lamda (R function): Nitsche stabilization solution
        up (P2-P1-R function): full solution 
    '''

    
    ## Get parameters
    beta, nu, degree, normal_choice = [params[name] for name in ['beta', 'nu', 'degree', 'normal_choice']]

    # Make FE space with Taylor-Hood elements with given degree
    P2 = VectorElement("Lagrange", mesh.ufl_cell(), degree)
    P1 = FiniteElement("Lagrange", mesh.ufl_cell(), degree-1)
    LM = FiniteElement('R', mesh.ufl_cell(), 0)

    TH = MixedElement([P2, P1, LM])
    W = FunctionSpace(mesh, TH)

    # Set up initial guess for Newton solver
    if up_init is None: up = Function(W)
    else: up = interpolate(up_init, W)

    # We use either a "projected normal" (by taking the normal vector from the continuous flow domain) or
    # the "discrete normal" (by taking the normal vector from the discretized flow domain)

    if normal_choice == 'projected_normal':
        n = Expression(('-x[0]', '-x[1]'), degree=2)
    else:
        n = FacetNormal(mesh)
    tau = as_vector([n[1], -n[0]])

    # Define variational problem
    (u, p, rho) = split(up)
    (v, q, lamda) = TestFunctions(W)
    
    h = mesh.hmin()

    ds = Measure('ds', domain=mesh, subdomain_data=boundary_markers)

    a =  Constant(0.5*nu)*inner(D(u), D(v))*dx
    a += + beta * dot(u, tau) * dot(v, tau) * ds(1)
    a += - Constant(nu)*dot(D(u)*dot(v,n)*n, n)*ds(1)
    a += - Constant(nu)*dot(D(v)*dot(u,n)*n, n)*ds(1)
    a += + Constant(gamma) * Constant(1.0 / h) * dot(u, n) * dot(v, n) * ds(1)
    a += - div(v)*p*dx - q*div(u)*dx
    a +=  + rho*q*dx + lamda*p*dx
    a +=  + p*dot(v,n)*ds(1) + q*dot(u,n)*ds(1)

    L =  dot(f,v)*dx - f_gamma*dot(v, tau)*ds(1) # here f is forcing term in (1) and f_gamma is forcing term in the rhs of (3)


    # On the sides of the box, we use an essential boundary condition for velocity
    bc = DirichletBC(W.sub(0), u_bc, boundary_markers, 3)

    # Solve
    solve(a==L, up, bc)
    u, p, lamda = up.split()

    return u, p, lamda, up


def D(u):
    gradu = grad(u)
    return gradu + gradu.T
