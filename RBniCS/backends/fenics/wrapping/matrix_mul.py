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
## @file functions_list.py
#  @brief Type for storing a list of FE functions.
#
#  @author Francesco Ballarin <francesco.ballarin@sissa.it>
#  @author Gianluigi Rozza    <gianluigi.rozza@sissa.it>
#  @author Alberto   Sartori  <alberto.sartori@sissa.it>

from petsc4py import PETSc
from ufl.core.operator import Operator
from dolfin import as_backend_type
import RBniCS.backends # avoid circular imports when importing fenics backend
from RBniCS.backends.fenics.wrapping import function_from_ufl_operators

def matrix_mul_vector(matrix, vector):
    if isinstance(vector, (RBniCS.backends.fenics.Function.Type(), Operator)):
        vector = function_from_ufl_operators(vector).vector()
    return matrix*vector

def vectorized_matrix_inner_vectorized_matrix(matrix, other_matrix):
    assert isinstance(matrix, RBniCS.backends.fenics.Matrix.Type())
    assert isinstance(other_matrix, RBniCS.backends.fenics.Matrix.Type())
    matrix = as_backend_type(matrix).mat()
    other_matrix = as_backend_type(other_matrix).mat()
    mat = matrix.transposeMatMult(other_matrix)
    # petsc4py does not expose MatGetTrace, we do this by hand
    return mat.getDiagonal().sum()
