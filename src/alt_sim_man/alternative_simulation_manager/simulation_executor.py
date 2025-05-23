"""

"""

import dill
import os
import logging
from typing import Callable, Dict, List, Optional

from .alternative import Alternative
from ..utils import create_dir



class SimulationExecutor:

    def __init__(self,alternative_list:List[Alternative],simulation_tree):
        """

        """
        self._alternative_list = alternative_list
        self._simulation_tree = simulation_tree
        # Config


    def run(self,path_simulation_folder:str, overwrite:bool=False,run_in_parallel:Optional[bool]=False,):
        """

        :param path_simulation_folder:
        :param overwrite: bool, True if all the alternative simulation folders should be overwritten. If False and some
            folder are already present (due to a simulation that was interrupted), the simulation will start again from
            where it stopped.
        :return:
        """

        # Check path
        if not os.path.isdir(path_simulation_folder):
            os.mkdir(path_simulation_folder)


    def init_simulation(self,path_simulation_folder):
        """

        :param path_simulation_folder:
        :return:
        """

        #
        # Make one folder per alternative

        # make one progress.json for the global simulation and one per alternative




    def alternative_

