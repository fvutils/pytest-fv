#****************************************************************************
#* hdl_config.py
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
import pytest
import configparser

class HdlConfig(object):
    DEFAULT_TOOL_SIM = "xsim"

    def __init__(self, pytestconfig):

        if pytestconfig.inipath is not None:
            self.ini = configparser.ConfigParser()
            self.ini.read(pytestconfig.inipath)
        else:
            self.ini = {}

        pass

    def _pytest_hdl(self):
        if "pytest-hdl" not in self.ini.keys():
            self.ini["pytest-hdl"] = {}
        return self.ini["pytest-hdl"]

    def getToolSim(self):
        pytest_hdl = self._pytest_hdl()

        if "PYTEST_HDL_SIM" in os.environ.keys() and os.environ["PYTEST_HDL_SIM"] != "":
            return os.environ["PYTEST_HDL_SIM"]
        elif "tool.sim" in pytest_hdl.keys():
            return pytest_hdl["tool.sim"]
        else:
            return HdlConfig.DEFAULT_TOOL_SIM
        

@pytest.fixture
def hdl_config(pytestconfig):
    return HdlConfig(pytestconfig)
    print("hdl_config")
    return "abc"
    pass
