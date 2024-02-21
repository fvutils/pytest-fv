#****************************************************************************
#* flow.py
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
import asyncio
from pytest_fv import DirConfig
from pytest_fv.impl.path_src_ivpm import PathSrcIvpm
from typing import List, Dict
from .phase_compound import PhaseCompound
from .fusesoc import FuseSoc
from .fs import FS

class Flow(PhaseCompound):

    def __init__(self, 
                 dirconfig : DirConfig,
                 pathsrc=None):
        super().__init__("")
        self.dirconfig = dirconfig
        self.fs = FuseSoc()

        if pathsrc is None:
            pathsrc = PathSrcIvpm(dirconfig.test_srcdir())
        
        for path in pathsrc.getPaths("lib-dirs"):
            print("Add-path %s" % path)
            self.fs.add_library(path)

        self._tool_m = {}
        self._ext_m = {}

    def getBuildDir(self):
        return self.dirconfig.builddir()

    def addTool(self, tool, kind):
        self._tool_m[kind] = tool

    def getTool(self, kind):
        return self._tool_m[kind]
    
    def addExt(self, ext, name):
        self._ext_m[name] = ext
    
    def addFileset(self, tool, fs : FS):
        if tool in self._tool_m.keys():
            self._tool_m[tool].addFileset(fs)
        else:
            raise Exception("No tool \"%s\" is registered" % tool)
        
    def run_all(self):
        loop = None

        try:
            loop = asyncio.get_running_loop()
        except Exception:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        loop.run_until_complete(self.run())





