#****************************************************************************
#* path_src_ivpm.py
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
from typing import List
from pytest_fv.path_src import PathSrc

class PathSrcIvpm(PathSrc):

    def __init__(self, test_srcdir):
        super().__init__()
        from ivpm.utils import find_project_root
        from ivpm.pkg_info_rgy import PkgInfoRgy
        from ivpm.proj_info import ProjInfo
        from ivpm.ivpm_yaml_reader import IvpmYamlReader
        from ivpm import load_project_package_info

        # Find the project
        project = find_project_root(test_srcdir)
#        print("project: %s" % project)
        self.pkg_info = load_project_package_info(project)

        self.pkg_info_rgy = PkgInfoRgy.inst()

    def getPaths(self, kind: str) -> List[str]:
        ret = []

        for i,pkg in enumerate(self.pkg_info):
            section = "project" if i == 0 else "export"
#            print("Section: %s %s %s" % (section, pkg.name, str(pkg.paths.keys())))
            if section in pkg.paths.keys():
#                print("  Kind: %s %s" % (kind, str(pkg.paths[section].keys())))
                if kind in pkg.paths[section].keys():
#                    print("  Paths: %s" % str(pkg.paths[section][kind]))
                    ret.extend(pkg.paths[section][kind])
        ret.extend(self.pkg_info_rgy.getPaths(kind))

        return ret

