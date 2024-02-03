#****************************************************************************
#* hdl_tool_sim.py
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
import os
import pytest
from .fv_config import FvConfig
from .tool_rgy import ToolKind, ToolRgy
from .task import Task
from .task_delegator import TaskDelegator

class HdlSim(object):

    class RunArgs(object):
        def __init__(self, sim, rundir):
            self.sim = sim
            self.debug  = sim.debug
            self.rundir = rundir
            self.run_logfile = sim.run_logfile
            self.dpi_libs = sim.dpi_libs.copy()
            self.pli_libs = sim.pli_libs.copy()
            self.plusargs = sim.plusargs.copy()
            self.args = sim.args.copy()
            self.env  = None if sim.env is None else sim.env.copy()

        def setenv(self, var, val):
            if self.env is None:
                self.env = os.environ.copy()
            self.env[var] = val

    def __init__(self, builddir):
#        self._files = []
#        self._incdirs = []
#        self._defines = {}

        # Common
        self.env = None
        self.debug = False

        # Build
        self.builddir = builddir
        self._files = []
        self.top = set()
        self.build_logfile = "build.log"

        # Run
        self.run_logfile = "run.log"
        self.dpi_libs = []
        self.pli_libs = []
        self.plusargs = []
        self.args = []

    def setenv(self, var, val):
        if self.env is None:
            self.env = os.environ.copy()
        self.env[var] = val

    def addFiles(self, files, flags=None):
        self._files.append((flags,files))

    def hasFlag(self, flag):
        ret = False
        for flags,files in self._files:
            if flags is not None and flag in flags.keys():
                ret = True
                break
        return ret
    
    def mkRunArgs(self, rundir):
        return HdlSim.RunArgs(self, rundir)
    
    async def build(self):
        raise NotImplementedError("HdlToolSim.build: %s" % str(self))

    async def run(self, args : 'HdlSim.RunArgs'):
        raise NotImplementedError("HdlToolSim.run: %s" % str(self))
    
    def mkBuildTask(self) -> Task:
        return TaskDelegator("sim build", self.build())
    
    def mkRunTask(self, args : 'HdlSim.RunArgs') -> Task:
        return TaskDelegator("sim run", self.run(args))
    
    @staticmethod
    def create(builddir, cfg=None):
        cls = None
        if cfg is None:
            cfg = FvConfig.inst()
            cls = ToolRgy.inst().get(ToolKind.Sim, cfg.getHdlSim())
        elif type(cfg) == str:
            cls = ToolRgy.inst().get(ToolKind.Sim, cfg)
        else:
            raise Exception("Unknown config type %s" % str(cfg))
        return cls(builddir)
    

