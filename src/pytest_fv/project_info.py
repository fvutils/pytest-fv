#****************************************************************************
#* project_info.py
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
import pytest
import os
import sys

class ProjectInfo(object):

    def __init__(self):
        python_bindir = os.path.dirname(sys.executable)
        project_dir = os.path.abspath(os.path.join(python_bindir, "../.."))
        
        self.project_dir = project_dir

        pass

    @classmethod
    def inst(cls):
        if cls._inst is None:
            cls._inst = ProjectInfo()
        return cls._inst

