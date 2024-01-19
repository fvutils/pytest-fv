#****************************************************************************
#* hdl_tool_sim.py
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

class HdlToolSim(object):

    def __init__(self):
#        self._files = []
#        self._incdirs = []
#        self._defines = {}

        self._files = []

    def addFiles(self, files, flags=None):
        self._files.append((flags,files))

    def hasFlag(self, flag):
        ret = False
        for flags,files in self._files:
            if flags is not None and flag in flags.keys():
                ret = True
                break
        return ret

    def build(self):
        raise NotImplementedError("HdlToolSim.build: %s" % str(self))

    def run(self):
        raise NotImplementedError("HdlToolSim.run: %s" % str(self))

    pass
    
class HdlToolSimRgy(object):
    _inst = None

    def __init__(self):
        self.impl = {}

    def addSimImpl(self, name, cls):
        print("addSimImpl")
        self.impl[name] = cls

    @classmethod
    def inst(cls):
        if cls._inst is None:
            cls._inst = HdlToolSimRgy()
        return cls._inst
    
    @staticmethod
    def get(sim):
        rgy = HdlToolSimRgy.inst()
        if sim in rgy.impl.keys():
            return rgy.impl[sim]()
        else:
            raise Exception("pytest-hdl: sim %s is not supported" % sim)

    @staticmethod
    def create(config):
        sim = config.getToolSim()
        rgy = HdlToolSimRgy.inst()
        if sim in rgy.impl.keys():
            return rgy.impl[sim]()
        else:
            raise Exception("pytest-hdl: sim %s is not supported" % sim)


@pytest.fixture
def hdl_tool_sim(hdl_config):
    return HdlToolSimRgy.create(hdl_config)

