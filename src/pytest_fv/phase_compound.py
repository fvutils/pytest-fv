#****************************************************************************
#* phase_compound.py
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
import inspect
from .phase import Phase

class PhaseCompound(Phase):

    def __init__(self, name):
        super().__init__(name)
        self._subphases = []
        self._subphase_m = {}

    async def run(self):
        for phase in self.getSubPhases():
            await phase.run()

    def getSubPhases(self):
        return self._subphases

    def hasSubPhase(self, name):
        return name in self._subphase_m.keys()

    def getSubPhase(self, name):
        return self._subphase_m[name]
    
    def addSubPhase(self, phase):
        self._subphases.append(phase)
        self._subphase_m[phase.name] = phase

    def addTaskToPhase(self, phase, task):
        from .task_delegator import TaskDelegator
        phase_elem_l = phase.split(".")

        curr_phase = self
        for i,name in enumerate(phase_elem_l):
            if not hasattr(curr_phase, "hasSubPhase"):
                raise Exception("Phase is not compound (looking for subphase %s)" % name)

            if curr_phase.hasSubPhase(name):
                curr_phase = curr_phase.getSubPhase(name)
            else:
                raise Exception("Failed to find subphase %s ; have %s" % (
                    name, str(curr_phase._subphase_m.keys())))
        if not hasattr(task, "run"):
            if inspect.iscoroutine(task):
                task = TaskDelegator(str(task), task)
            else:
                raise Exception("No 'run' attribute and not a coroutine")
        curr_phase.addTask(task)



