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

from rbnics.problems.navier_stokes.navier_stokes_reduced_problem import NavierStokesReducedProblem
from rbnics.backends import product, sum
from rbnics.utils.decorators import Extends

def NavierStokesTensor3ReducedProblem(NavierStokesReducedProblem_DerivedClass):
    
    NavierStokesTensor3ReducedProblem_Base = NavierStokesReducedProblem(NavierStokesReducedProblem_DerivedClass)
    
    @Extends(NavierStokesTensor3ReducedProblem_Base)
    class NavierStokesTensor3ReducedProblem_Class(NavierStokesTensor3ReducedProblem_Base):
        
        class ProblemSolver(NavierStokesTensor3ReducedProblem_Base.ProblemSolver):
            def residual_eval(self, solution):
                self.store_solution(solution)
                problem = self.problem
                N = self.N
                assembled_operator = dict()
                for term in ("a", "b", "bt", "c", "f", "g"):
                    assert problem.terms_order[term] in (1, 2)
                    if problem.terms_order[term] == 2:
                        assembled_operator[term] = sum(product(problem.compute_theta(term), problem.operator[term][:N, :N]))
                    elif problem.terms_order[term] == 1:
                        assembled_operator[term] = sum(product(problem.compute_theta(term), problem.operator[term][:N]))
                    else:
                        raise AssertionError("Invalid value for order of term " + term)
                return (
                     (assembled_operator["a"] + assembled_operator["b"] + assembled_operator["bt"])*solution
                    + assembled_operator["c"]
                    - assembled_operator["f"] - assembled_operator["g"]
                )
                
            def jacobian_eval(self, solution):
                self.store_solution(solution)
                problem = self.problem
                N = self.N
                assembled_operator = dict()
                for term in ("a", "b", "bt", "dc"):
                    assert problem.terms_order[term] is 2
                    assembled_operator[term] = sum(product(problem.compute_theta(term), problem.operator[term][:N, :N]))
                return (
                      assembled_operator["a"] + assembled_operator["b"] + assembled_operator["bt"]
                    + assembled_operator["dc"]
                )
        
    # return value (a class) for the decorator
    return NavierStokesTensor3ReducedProblem_Class
