# Copyright (C) 2015-2016 by the RBniCS authors
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
## @file __init__.py
#  @brief Init file for auxiliary I/O module
#
#  @author Francesco Ballarin <francesco.ballarin@sissa.it>
#  @author Gianluigi Rozza    <gianluigi.rozza@sissa.it>
#  @author Alberto   Sartori  <alberto.sartori@sissa.it>

from RBniCS.utils.io.error_analysis_table import ErrorAnalysisTable
from RBniCS.utils.io.exportable_list import ExportableList
from RBniCS.utils.io.folders import Folders
from RBniCS.utils.io.greedy_error_estimators_list import GreedyErrorEstimatorsList
from RBniCS.utils.io.greedy_selected_parameters_list import GreedySelectedParametersList
from RBniCS.utils.io.numpy_io import NumpyIO
#from RBniCS.utils.io.performance_table import PerformanceTable # not needed, only used internally inside this module
from RBniCS.utils.io.pickle_io import PickleIO
from RBniCS.utils.io.speedup_analysis_table import SpeedupAnalysisTable
from RBniCS.utils.io.text_io import TextIO

# Alias FEniCS functions
from dolfin import plot, File, log, DEBUG, PROGRESS

__all__ = [
    'ErrorAnalysisTable',
    'ExportableList',
    'File',
    'Folders',
    'GreedyErrorEstimatorsList',
    'GreedySelectedParametersList',
    'NumpyIO',
    'ParametrizedExpression',
    'plot',
    'PickleIO',
    'SpeedupAnalysisTable',
    'TextIO'
]
