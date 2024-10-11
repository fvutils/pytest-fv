#****************************************************************************
#* task_cmd.py
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
import subprocess
from typing import Dict, List
from .console import Console
from .env import Env
from .env_action import EnvAction
from .task import Task

class TaskCmd(Task):

    def __init__(self, 
                 name : str,
                 cmd : List[str],
                 cwd : str = None,
                 env : List[EnvAction] = None):
        super().__init__(name)
        self.cmd = cmd
        self.cwd = cwd
        self.env = env
        pass

    async def run(self):
        env = Env()

        if self.env is not None:
            for e in self.env:
                e.apply(env)

        if self.cwd is not None and not os.path.isdir(self.cwd):
            os.makedirs(self.cwd)

        Console.inst().write(None, "** Task: %s" % self.name)
        Console.inst().write(None, "** Command: %s" % str(self.cmd))
        res = Console.inst().run(
            None,
            self.cmd,
            env=env.env,
            cwd=self.cwd,
        )

        if res.returncode != 0:
            raise Exception("Command %s failed (%d)" % (str(self.cmd), res.returncode))

