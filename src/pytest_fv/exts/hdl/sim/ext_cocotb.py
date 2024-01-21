#****************************************************************************
#* ext_cocotb.py
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
from pytest_fv import HdlSim, HdlSimExt

class ExtCocotb(HdlSimExt):

    def __init__(self):
        self._updatesRun = True
        self._modules = []
        self._testcases = []

    def addModule(self, module):
        self._modules.append(module)

    def addTestcase(self, testcase):
        self._testcases.append(testcase)

    def applyBuild(self, build_args : HdlSim.BuildArgs):
        pass

    def applyRun(self, run_args : HdlSim.RunArgs):
        if len(self._modules) == 0:
            raise Exception("No root module specified")

        modules = ",".join(self._modules)
        run_args.setenv("MODULE", modules)

        if len(self._testcases):
            testcases = ",".join(self._testcases)
            run_args.setenv("TESTCASE", modules)

        try:
            import cocotb.config as ccfg
            ccfg.libs_dir
        except Exception as e:
            raise e



