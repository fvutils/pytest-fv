#****************************************************************************
#* task_group.py
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
from .task import Task

class TaskGroup(Task):

    def __init__(self):
        super().__init__("")
        self._tasks = []

    async def run(self):
        from .console import Console
        for task in self._tasks:
            Console.inst().println("*********************************************************************")
            Console.inst().println("* Begin Task: %s" % task.name)
            Console.inst().println("*********************************************************************")
            await task.run()
            Console.inst().println("*********************************************************************")
            Console.inst().println("* End Task: %s" % task.name) 
            Console.inst().println("*********************************************************************")

    def addTask(self, task):
        self._tasks.append(task)

