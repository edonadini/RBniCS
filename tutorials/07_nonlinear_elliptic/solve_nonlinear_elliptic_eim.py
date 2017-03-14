# Copyright (C) 2015-2017 by the RBniCS authors
#
# This file is part of RBniCS.
#
# RBniCS is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RBniCS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with RBniCS. If not, see <http://www.gnu.org/licenses/>.
#
## @file solve_tblock.py
#  @brief Example 7: nonlinear elliptic problem
#
#  @author Francesco Ballarin <francesco.ballarin@sissa.it>
#  @author Gianluigi Rozza    <gianluigi.rozza@sissa.it>
#  @author Alberto   Sartori  <alberto.sartori@sissa.it>

from dolfin import *
from RBniCS import *

#~~~~~~~~~~~~~~~~~~~~~~~~~     EXAMPLE 7: NONLINEAR PROBLEM CLASS     ~~~~~~~~~~~~~~~~~~~~~~~~~# 
@EIM()
class NonlinearElliptic(NonlinearEllipticProblem):
    
    ###########################     CONSTRUCTORS     ########################### 
    ## @defgroup Constructors Methods related to the construction of the reduced order model object
    #  @{
    
    ## Default initialization of members
    def __init__(self, V, **kwargs):
        # Call the standard initialization
        NonlinearEllipticProblem.__init__(self, V, **kwargs)
        # ... and also store FEniCS data structures for assembly
        assert "subdomains" in kwargs
        assert "boundaries" in kwargs
        self.subdomains, self.boundaries = kwargs["subdomains"], kwargs["boundaries"]
        self.du = TrialFunction(V)
        self.u = self._solution
        self.v = TestFunction(V)
        self.dx = Measure("dx")(subdomain_data=self.subdomains)
        self.ds = Measure("ds")(subdomain_data=self.boundaries)
        # Store the forcing term expression
        self.f = Expression("sin(2*pi*x[0])*sin(2*pi*x[1])", element=self.V.ufl_element())
        # Customize nonlinear solver parameters
        self._nonlinear_solver_parameters = {
            "linear_solver": "mumps",
            "maximum_iterations": 20,
            "report": True,
            "error_on_nonconvergence": True
        }
        
    #  @}
    ########################### end - CONSTRUCTORS - end ########################### 
    
    ###########################     PROBLEM SPECIFIC     ########################### 
    ## @defgroup ProblemSpecific Problem specific methods
    #  @{
    
    ## Return the alpha_lower bound.
    def get_stability_factor(self):
        return 1.
    
    ## Return theta multiplicative terms of the affine expansion of the problem.
    def compute_theta(self, term):
        mu1 = self.mu[0]
        if term == "a" or term == "da":
            theta_a0 = 1.
            theta_a1 = mu1
            return (theta_a0, theta_a1)
        elif term == "f":
            theta_f0 = 100.
            return (theta_f0,)
        else:
            raise ValueError("Invalid term for compute_theta().")
    
    ## Return forms resulting from the discretization of the affine expansion of the problem operators.
    def assemble_operator(self, term):
        v = self.v
        dx = self.dx
        if term == "a" or term == "da":
            u = self.u
            mu2 = self.mu[1]
            a0 = inner(grad(u), grad(v))*dx
            a1 = (exp(mu2*u) - 1)/mu2*v*dx
            if term == "a":
                return (a0, a1)
            else:
                du = self.du
                return tuple(derivative(ai, u, du) for ai in (a0, a1))
        elif term == "f":
            f = self.f
            f0 = f*v*dx
            return (f0,)
        elif term == "dirichlet_bc":
            bc0 = [DirichletBC(self.V, Constant(0.0), self.boundaries, 1)]
            return (bc0,)
        elif term == "inner_product":
            du = self.du
            x0 = inner(grad(du),grad(v))*dx
            return (x0,)
        else:
            raise ValueError("Invalid term for assemble_operator().")
        
    #  @}
    ########################### end - PROBLEM SPECIFIC - end ########################### 

#~~~~~~~~~~~~~~~~~~~~~~~~~     EXAMPLE 7: MAIN PROGRAM     ~~~~~~~~~~~~~~~~~~~~~~~~~# 

# 1. Read the mesh for this problem
mesh = Mesh("data/square.xml")
subdomains = MeshFunction("size_t", mesh, "data/square_physical_region.xml")
boundaries = MeshFunction("size_t", mesh, "data/square_facet_region.xml")

# 2. Create Finite Element space (Lagrange P1)
V = FunctionSpace(mesh, "Lagrange", 1)

# 3. Allocate an object of the NonlinearElliptic class
nonlinear_elliptic_problem = NonlinearElliptic(V, subdomains=subdomains, boundaries=boundaries)
mu_range = [(0.01, 10.0), (0.01, 10.0)]
nonlinear_elliptic_problem.set_mu_range(mu_range)

# 4. Prepare reduction with a reduced basis method
reduced_basis_method = PODGalerkin(nonlinear_elliptic_problem)
reduced_basis_method.set_Nmax(20, EIM=21)

# 5. Perform the offline phase
reduced_basis_method.initialize_training_set(50, EIM=60)
reduced_nonlinear_elliptic_problem = reduced_basis_method.offline()

# 6. Perform an online solve
online_mu = (0.01, 1.0)
reduced_nonlinear_elliptic_problem.set_mu(online_mu)
reduced_nonlinear_elliptic_problem.solve()
reduced_nonlinear_elliptic_problem.export_solution("NonlinearElliptic", "online_solution")

# 7. Perform an error analysis
reduced_basis_method.initialize_testing_set(50, EIM=60)
reduced_basis_method.error_analysis()

# 8. Perform a speedup analysis
reduced_basis_method.speedup_analysis()