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

class SimVlogBase(HdlSim):

    def __init__(self, builddir):
        super().__init__(builddir)
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

        file_type = {'verilogSource', 'systemVerilogSource'}

        for flags,deps in self._files:
            print("flags: %s" % str(flags))
            print("deps: %s" % str(deps))
            file_flags = {'is_toplevel': True}

            if flags is not None:
                file_flags.update(flags)

            for dep in deps:
                d_files = dep.get_files(file_flags)

                for f in d_files:
                    print("f: %s" % str(f))
                    if file_type is None or f['file_type'] in file_type:
                        if 'include_path' in f.keys():
                            incdir = os.path.join(dep.core_root, f['include_path'])
                            inc_s.add(incdir)
                        else:
                            incdir = os.path.join(dep.core_root, os.path.dirname(f['name']))
                        inc_s.add(incdir)
                        path = os.path.join(dep.core_root, f['name'])

                        if path not in src_s:
                            src_s.add(path)
                            src_l.append(path)
                    else:
                        raise Exception("File-type %s not supported by sim %s" % (
                            f['file_type'], str(type(self))))

        return (src_l, cpp_l, inc_s, def_m)
