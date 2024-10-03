#****************************************************************************
#* flow_sim.py
#*
#* Copyright 2023 Matthew Ballance and Contributors
#*
#* Licensed under the Apache License, Version 2.0 (the "License"); you may 
#* not use this file except in compliance with the License.  
#* You may obtain a copy of the License at:
#*
#*   http://www.apache.org/licenses/LICENSE-2.0
#*
#* Unless required by applicable law or agreed to in writing, software 
#* distributed under the License is distributed on an "AS IS" BASIS, 
#* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
#* See the License for the specific language governing permissions and 
#* limitations under the License.
#*
#* Created on:
#*     Author: 
#*
#****************************************************************************
from pytest_fv import HdlSim, DirConfig
from .flow import Flow
from .phase_pre_post import PhasePrePost

class FlowSim(Flow):

    def __init__(self, dirconfig : DirConfig, sim_id = None):
        super().__init__(dirconfig)
        self.addSubPhase(PhasePrePost("generate"))
        self.addSubPhase(PhasePrePost("build"))
        self.addSubPhase(PhasePrePost("run"))
        self.sim : HdlSim = HdlSim.create(dirconfig, sim_id)
        self.addTool(self.sim, "sim")
        self.addTaskToPhase("build.main", self.sim.mkBuildTask())

        # Connect the simulator config to FuseSoC
        self.sim.fs_cfg.init(self.fs)

