#****************************************************************************
#* task_create_file.py
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
from pytest_fv.task import Task

class TaskCreateFile(Task):

    def __init__(self, path, content):
        super().__init__("create file")
        self._path = path
        self._content = content

    async def run(self):
        file_dir = os.path.dirname(self._path)

        if not os.path.isdir(file_dir):
            os.makedirs(file_dir)

        with open(self._path, "w") as fp:
            fp.write(self._content)

