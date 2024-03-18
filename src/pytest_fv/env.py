#****************************************************************************
#* env.py
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
import platform
from .env_action import EnvAction

class Env(object):

    def __init__(self, env=None):
        if env is None:
            self._env = os.environ.copy()
        else:
            if isinstance(env, Env):
                self._env = env._env.copy()
            else:
                self._env = env.copy()

    @property
    def env(self):
        return self._env
    
    def append_path(self, var, val):
        ps = ";" if platform.system() == "Windows" else ":"

        if var not in self._env.keys():
            self._env[var] = val
        else:
            self._env[var] = self._env[var] + ps + val

    def prepend_path(self, var, val):
        ps = ";" if platform.system() == "Windows" else ":"

        if var not in self._env.keys():
            self._env[var] = val
        else:
            self._env[var] = val + ps + self._env[var]

    def setenv(self, var, val):
        self._env[var] = val

    def append(self, var, val):
        if var not in self._env.keys():
            self._env[var] = val
        else:
            self._env[var] = self._env[var] + val



