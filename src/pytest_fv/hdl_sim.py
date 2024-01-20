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
from .tool_rgy import ToolKind, ToolRgy

class HdlSim(object):
    class Args(object):
        def __init__(self, sim, builddir):
            self.sim = sim
            self.builddir = builddir
            self.logfile = None
            self.env = None

        def setenv(self, var, val):
            if self.env is None:
                self.env = os.environ.copy()
            self.env[var] = val

    class BuildArgs(Args):
        def __init__(self, sim, builddir):
            super().__init__(sim, builddir)
            self._files = []
            self.top = set()
            self.logfile = "build.log"

        def addFiles(self, files, flags=None):
            self._files.append((flags, files))

        @property
        def files(self):
            return self._files

    class RunArgs(Args):
        def __init__(self, sim, builddir, rundir):
            super().__init__(sim, builddir)
            self._rundir  = rundir
            self.logfile = "run.log"
            self.dpi_libs = []
            self.pli_libs = []
            self.plusargs = []
            self.args = []
            self.env = None
            self.cwd = None

    def __init__(self):
#        self._files = []
#        self._incdirs = []
#        self._defines = {}

        self._files = []
        self._builddir = None


    def addFiles(self, files, flags=None):
        self._files.append((flags,files))

    def hasFlag(self, flag):
        ret = False
        for flags,files in self._files:
            if flags is not None and flag in flags.keys():
                ret = True
                break
        return ret
    
    def mkBuildArgs(self, builddir):
        return HdlSim.BuildArgs(self, builddir)

    def mkRunArgs(self, builddir, rundir):
        return HdlSim.RunArgs(self, builddir, rundir)

    def build(self, args : BuildArgs):
        raise NotImplementedError("HdlToolSim.build: %s" % str(self))

    def run(self, args : RunArgs):
        raise NotImplementedError("HdlToolSim.run: %s" % str(self))
    
    @staticmethod
    def create(cfg=None):
        if cfg is None:
            # TODO: get global configuration
            pass
        elif type(cfg) == str:
            cls = ToolRgy.inst().get(ToolKind.Sim, cfg)
            return cls()
        else:
            raise Exception("Unknown config type %s" % str(cfg))
    
class HdlToolSimRgy(object):
    _inst = None

    def __init__(self):
        self.impl = {}

    def addSimImpl(self, name, cls):
        print("addSimImpl")
        self.impl[name] = cls

    @classmethod
    def inst(cls):
        if cls._inst is None:
            cls._inst = HdlToolSimRgy()
        return cls._inst
    
    @staticmethod
    def get(sim):
        rgy = HdlToolSimRgy.inst()
        if sim in rgy.impl.keys():
            return rgy.impl[sim]()
        else:
            raise Exception("pytest-hdl: sim %s is not supported" % sim)

    @staticmethod
    def create(config):
        sim = config.getToolSim()
        rgy = HdlToolSimRgy.inst()
        if sim in rgy.impl.keys():
            return rgy.impl[sim]()
        else:
            raise Exception("pytest-hdl: sim %s is not supported" % sim)


@pytest.fixture
def hdl_tool_sim(hdl_config):
    return HdlToolSimRgy.create(hdl_config)

