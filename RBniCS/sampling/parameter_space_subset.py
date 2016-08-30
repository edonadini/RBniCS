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
## @file parameter_space_subset.py
#  @brief Type for parameter space subsets
#
#  @author Francesco Ballarin <francesco.ballarin@sissa.it>
#  @author Gianluigi Rozza    <gianluigi.rozza@sissa.it>
#  @author Alberto   Sartori  <alberto.sartori@sissa.it>

###########################     OFFLINE STAGE     ########################### 
## @defgroup OfflineStage Methods related to the offline stage
#  @{

# Parameter space subsets
from RBniCS.sampling.distributions import UniformDistribution
from RBniCS.utils.io import ExportableList
from RBniCS.utils.mpi import is_io_process
from RBniCS.utils.decorators import Extends, override
from numpy import zeros as array
from numpy import argmax
from mpi4py.MPI import MAX

@Extends(ExportableList)
class ParameterSpaceSubset(ExportableList): # equivalent to a list of tuples
    @override
    def __init__(self, box):
        ExportableList.__init__(self, "pickle")
        self.box = box
        self.mpi_comm = is_io_process.mpi_comm # default communicator
        self.distributed_max = True
    
    # Method for generation of parameter space subsets
    def generate(self, n, sampling):
        if is_io_process():
            if sampling is None:
                sampling = UniformDistribution()
            self._list = sampling.sample(self.box, n)
        self._list = is_io_process.mpi_comm.bcast(self._list, root=0)
        
    @override
    def load(self, directory, filename):
        result = ExportableList.load(self, directory, filename)
        if not result:
            return False
        # Also load the box
        assert self._FileIO.exists_file(directory, filename + "_box")
        box = self._FileIO.load_file(directory, filename + "_box")
        if len(box) != len(self.box):
            return False
        for (box_range, loaded_box_range) in zip(self.box, box):
            if box_range[0] != loaded_box_range[0] or box_range[1] != loaded_box_range[1]:
                return False
        return True
        
    @override
    def save(self, directory, filename):
        ExportableList.save(self, directory, filename)
        # Also save box
        self._FileIO.save_file(self.box, directory, filename + "_box")
        
    def max(self, generator, postprocessor=lambda value: value):
        if self.distributed_max:
            local_list_indices = range(self.mpi_comm.rank, len(self._list), self.mpi_comm.size) # start from index rank and take steps of length equal to size
        else:
            local_list_indices = range(len(self._list))
        values = array(len(local_list_indices))
        values_with_postprocessing = array(len(local_list_indices))
        for i in range(len(local_list_indices)):
            values[i] = generator(self._list[ local_list_indices[i] ], local_list_indices[i])
            values_with_postprocessing[i] = postprocessor(values[i])
        if self.distributed_max:
            local_i_max = argmax(values_with_postprocessing)
            local_value_max = values[local_i_max]
            global_value_max = self.mpi_comm.allreduce(local_value_max, op=MAX)
            global_value_processor_argmax = -1
            if global_value_max == local_value_max:
                global_value_processor_argmax = self.mpi_comm.rank
            global_value_processor_argmax = self.mpi_comm.allreduce(global_value_processor_argmax, op=MAX)
            global_i_max = self.mpi_comm.bcast(local_list_indices[local_i_max], root=global_value_processor_argmax)
        else:
            global_i_max = argmax(values_with_postprocessing)
            global_value_max = values[global_i_max]
        return (global_value_max, global_i_max)
        
#  @}
########################### end - OFFLINE STAGE - end ########################### 

