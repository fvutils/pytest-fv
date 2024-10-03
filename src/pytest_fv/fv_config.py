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

class FvConfig(object):
    DEFAULT_TOOL_HDLSIM = "vlt"

    _inst = None

    def __init__(self, request : pytest.FixtureRequest, pytestconfig):

        self._have_ini = False
        self.request = request
        if pytestconfig is not None and pytestconfig.inipath is not None:
            self.ini = configparser.ConfigParser()
            self.ini.read(pytestconfig.inipath)
            self._have_ini = True
            self._rootdir = pytestconfig.rootpath
        else:
            self._rootdir = os.getcwd()
            self.ini = {}

        pass

    @property
    def rootdir(self):
        return self._rootdir
    
    @property
    def hdlsim_debug(self):
        return self.request.config.getoption("hdlsim-debug", default=False)

    def _pytest_hdl(self):
        if "pytest.fv" not in self.ini.keys():
            self.ini["pytest.fv"] = {}
        return self.ini["pytest.fv"]

    def getHdlSim(self):
        pytest_hdl = self._pytest_hdl()

        if self.request.config.getoption("hdlsim", default=None) is not None:
            return self.request.config.getoption("hdlsim")
        elif "PYTEST_FV_HDLSIM" in os.environ.keys() and os.environ["PYTEST_FV_HDLSIM"] != "":
            return os.environ["PYTEST_FV_HDLSIM"]
        elif "hdlsim" in pytest_hdl.keys():
            return pytest_hdl["hdlsim"]
        else:
            return self.request.config.getini("hdlsim")
    
    @classmethod
    def inst(cls, request, pytestconfig=None):
        if cls._inst is None:
            cls._inst = FvConfig(request, pytestconfig)
        elif pytestconfig is not None and not cls._inst._have_ini:
            cls._inst = FvConfig(request, pytestconfig)
        return cls._inst
        

@pytest.fixture
def hdl_config(pytestconfig):
    return FvConfig.inst(pytestconfig)
