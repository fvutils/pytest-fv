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
import json
import os
from pytest_fv import HdlSim
from pytest_fv.fs_config import FSConfig
import svdep

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
    
    def _checkUpToDate(self, timestamp) -> bool:
        ret = False
        src_l, cpp_l, inc_s, def_m = self._getSrcIncDef()
        if os.path.isfile(os.path.join(self.builddir, "svdep.json")):
            try:
                with open(os.path.join(self.builddir, "svdep.json"), "r") as fp:
                    svdep_json = json.load(fp)
                info = svdep.FileCollection.from_dict(svdep_json)
                ret = svdep.TaskCheckUpToDate(src_l, list(inc_s)).check(info, timestamp)
            except Exception as e:
                print("Failure while computing up-to-date: %s" % str(e))
        
        if not ret:
            info = svdep.TaskBuildFileCollection(src_l, list(inc_s)).build()
            with open(os.path.join(self.builddir, "svdep.json"), "w") as fp:
                json.dump(info.to_dict(), fp)
        return ret
