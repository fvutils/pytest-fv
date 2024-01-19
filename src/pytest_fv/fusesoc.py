#****************************************************************************
#* fusesoc.py
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
import sys
import pytest
import fusesoc
from pytest_fv import project_info
from fusesoc.config import Config
from fusesoc.coremanager import CoreManager
from fusesoc.librarymanager import Library
from fusesoc.vlnv import Vlnv

@pytest.fixture
def fusesoc():
    print("fusesoc")
    return FuseSoc.inst(None)

class FuseSoc(object):
    _inst = None

    def __init__(self, project_info=None):
        self._cm = None
        self._libraries = []


        pass

    def _getCoreManager(self):
        if self._cm is None:
            python_bindir = os.path.dirname(sys.executable)
            project_dir = os.path.abspath(os.path.join(python_bindir, "../../.."))
        
            self.project_dir = project_dir
            print("Root: %s" % self.project_dir)
            cfg = Config()
            self._cm = CoreManager(cfg)
        return self._cm
    
    def add_library(
            self,
            path,
            name=None,
            ignore=None):
        if name == None:
            name = str(path)
        
        if ignore is None:
            ignore = set()

        cm = self._getCoreManager()
        cm.add_library(Library(name, path), ignore)

    def getFiles(self,
                 vlnv,
                 flags=None,
                 target=None):
        top_flags = { 'is_toplevel': True}

        if flags is None:
            flags = {}
        
        if target is not None:
            top_flags["target"] = target

        cm = self._getCoreManager()
        
        core_deps = cm.get_depends(
            Vlnv(vlnv),
            flags=top_flags)
        
        return core_deps

    def getFilePaths(self,
               Pathnv,
                 file_type=None,
                 target=None,
                 include=False,
                 flags=None):
        top_flags = { 'is_toplevel': True}

        if flags is None:
            flags = {}
        
        if target is not None:
            top_flags["target"] = target

        cm = self._getCoreManager()
        
        core_deps = cm.get_depends(
            Vlnv(vlnv),
            flags=top_flags)
        
        files = []
        file_s = set()
        
        for d in core_deps:
            file_flags = {'is_toplevel': True}

            file_flags.update(flags)
            d_files = d.get_files(file_flags)

            for f in d_files:
                print("f: %s" % str(f))
                if file_type is None or f['file_type'] in file_type:
                    if include:
                        if 'include_path' in f.keys():
                            incdir = os.path.join(d.core_root, f['include_path'])
                        else:
                            incdir = os.path.join(d.core_root, os.path.dirname(f['name']))
                        if not incdir in file_s:
                            file_s.add(incdir)
                            files.append(incdir)
                    elif 'is_include_file' not in f.keys() or not f['is_include_file']:
                        path = os.path.join(d.core_root, f['name'])
                        if path not in file_s:
                            file_s.add(path)
                            files.append(path)

        return files
    
    @classmethod
    def inst(cls, project_info):
        if cls._inst is None:
            cls._inst = FuseSoc(project_info)
        return cls._inst

