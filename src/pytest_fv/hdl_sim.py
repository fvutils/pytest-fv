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
import platform
from typing import List,Set,Dict
from .fs import FS
from .fs_config import FSConfig
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
            self.env  = os.environ.copy() if sim.env is None else sim.env.copy()

        def setenv(self, var, val):
            if self.env is None:
                self.env = os.environ.copy()
            self.env[var] = val

        def append_pathenv(self, var, val):
            if self.env is None:
                self.env = os.environ.copy()
            if var not in self.env.keys():
                self.env[var] = val
            else:
                pathsep = ";" if platform.system() == "Windows" else ":"
                self.env[var] = self.env[var] + pathsep + val

        def prepend_pathenv(self, var, val):
            if self.env is None:
                self.env = os.environ.copy()
            if var not in self.env.keys():
                self.env[var] = val
            else:
                pathsep = ";" if platform.system() == "Windows" else ":"
                self.env[var] = val + pathsep + self.env[var]

    def addIncdir(self, dir):
        if dir not in self._incdirs:
            self._incdirs.append(dir)

    def __init__(self, builddir, fs_cfg : FSConfig):
        from .fv_config import FvConfig
#        self._files = []
#        self._incdirs = []
#        self._defines = {}
        
        self.fs_cfg = fs_cfg
        cfg = FvConfig.inst(None)

        # Common
        self.env = None
        self.debug = cfg.hdlsim_debug

        # Build
        self.builddir = builddir
        self._prefile_paths = []
        self._filesets : List[FS] = []
        self._incdirs : List[str] = []
        self.top = set()
        self.build_logfile = "build.log"

        # Run
        self.run_logfile = "run.log"
        self.dpi_libs = []
        self.pli_libs = []
        self.lib_dirs = []
        self.plusargs = []
        self.args = []

    def addLibDirs(self, dirs):
        new = ""
        pathsep = ";" if platform.system() == "Windows" else ":"
        if platform.system() == "Windows":
            libpath_var = "PATH"
        elif platform.system() == "Darwin":
            libpath_var = "DYLD_LIBRARY_PATH"
        else:
            libpath_var = "LD_LIBRARY_PATH"

        for d in dirs:
            if d not in self.lib_dirs:
                self.lib_dirs.append(d)
                if len(new) == 0:
                    new = d
                else:
                    new = new + pathsep + d

        
        if self.env is None:
            self.env = os.environ.copy()
        if libpath_var not in self.env.keys():
            self.env[libpath_var] = new
        else:
            self.env[libpath_var] = new + pathsep + self.env[libpath_var]

    def addLibDir(self, d):
        if d not in self.lib_dirs:
            self.lib_dirs.append(d)
            pathsep = ";" if platform.system() == "Windows" else ":"

            if platform.system() == "Windows":
                libpath_var = "PATH"
            elif platform.system() == "Darwin":
                libpath_var = "DYLD_LIBRARY_PATH"
            else:
                libpath_var = "LD_LIBRARY_PATH"

            if self.env is None:
                self.env = os.environ.copy()
            if libpath_var not in self.env.keys():
                self.env[libpath_var] = d
            else:
                self.env[libpath_var] = d + pathsep + self.env[libpath_var]

    def setenv(self, var, val):
        if self.env is None:
            self.env = os.environ.copy()
        self.env[var] = val
    
    def append_pathenv(self, var, val):
        if self.env is None:
            self.env = os.environ.copy()
        pathsep = ";" if platform.system() == "Windows" else ":"

        if var not in self.env.keys():
            self.env[var] = val
        else:
            self.env[var] = val + pathsep + self.env[var]

    def addPreFilePath(self, path):
        self._prefile_paths.append(path)

    def addFileset(self, fs : FS):
        self._filesets.append(fs)

    def hasFlag(self, flag):
        ret = False
        for flags,files in self._filesets:
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
    def create(dirconfig, cfg=None):
        cls = None
        if cfg is None:
            cfg = FvConfig.inst(dirconfig.request)
            cls = ToolRgy.inst().get(ToolKind.Sim, cfg.getHdlSim())
        elif type(cfg) == str:
            cls = ToolRgy.inst().get(ToolKind.Sim, cfg)
        else:
            raise Exception("Unknown config type %s" % str(cfg))
        return cls(dirconfig.builddir())
    

