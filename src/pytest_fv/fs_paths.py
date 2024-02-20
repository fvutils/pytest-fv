#****************************************************************************
#* fs_paths.py
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

class FSPaths(FS):

    def __init__(self,
                 paths : List[str],
                 stype : str,
                 incs : List[str]=None,
                 defs : Dict[str,str]=None):
        self.paths = paths.copy()
        self.stype = stype
        self.incs = [] if incs is None else incs.copy()
        self.defs = {} if defs is None else defs.copy()

    def getFiles(self, cfg : FSConfig=None) -> List[str]:
        print("getFiles: stype=%s stypes=%s" % (self.stype, str(cfg.types)))
        if self.stype in cfg.types:
            return self.paths
        else:
            return []
    
    def getIncs(self, cfg : FSConfig=None) -> List[str]:
        return self.incs

    def getDefs(self, cfg : FSConfig=None) -> Dict[str,str]:
        return self.defs
    

