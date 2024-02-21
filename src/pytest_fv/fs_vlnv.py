#****************************************************************************
#* fs_vlnv.py
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
from typing import List,Set,Dict
from .fs import FS
from .fs_config import FSConfig

class FSVlnv(FS):

    def __init__(self, 
                vlnv : str, 
                types : Set = None,
                flags : Set = None):
        super().__init__()
        self.vlnv = vlnv
        self.types = set() if types is None else types
        self.flags = set() if flags is None else flags
    
    def getFiles(self, cfg : FSConfig=None) -> List[str]:
        deps = []

        file_flags = {'is_toplevel': True}

#        if flags is not None:
#            file_flags.update(flags)

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
        return []
    
    def getIncs(self, cfg : FSConfig=None) -> List[str]:
        pass

    def getDefs(self, cfg : FSConfig=None) -> Dict[str,str]:
        pass

