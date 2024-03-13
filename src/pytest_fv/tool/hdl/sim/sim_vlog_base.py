#****************************************************************************
#* sim_vlog_base.py
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
from pytest_fv import HdlSim
from pytest_fv.fs_config import FSConfig

class SimVlogBase(HdlSim):

    def __init__(self, builddir, fs_config : FSConfig):
        super().__init__(builddir, fs_config)
        self._dpi_lib = []
        self._pli_lib = []
        pass

    def _getSrcIncDef(self):
        src_l = []
        src_s = set()
        cpp_l = []
        cpp_s = set()
        inc_s = set()
        def_m = {}

        for inc in self._incdirs:
            inc_s.add(inc)

        for fs in self._filesets:
            files = fs.getFiles(self.fs_cfg)
            src_l.extend(files)

            incs = fs.getIncs(self.fs_cfg)
            inc_s.update(incs)

            defs = fs.getDefs(self.fs_cfg)
            def_m.update(defs)

        return (src_l, cpp_l, inc_s, def_m)
