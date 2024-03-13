#****************************************************************************
#* env_action.py
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
from enum import Enum, auto

class EnvAction(object):

    class Type(Enum):
        PathAppend = auto()
        PathPrepend = auto()
        Set = auto()
        Append = auto()

    def __init__(self, 
                 kind : Type, 
                 var : str,
                 val : str):
        self._kind = kind
        self._var = var
        self._val = [*val]

    def apply(self, env):
        if not isinstance(self._val, list):
            val = [self._val]
        else:
            val = self._val

        for v in val:
            if self._kind == EnvAction.Type.PathAppend:
                env.append_path(self._var, v)
            elif self._kind == EnvAction.Type.PathPrepend:
                env.prepend_path(self._var, v)
            elif self._kind == EnvAction.Type.Set:
                env.setenv(self._var, v)
            elif self._kind == EnvAction.Type.Append:
                env.append(self._var, v)

    @staticmethod
    def append_path(var, *path) -> 'EnvAction':
        return EnvAction(
            EnvAction.Type.PathAppend,
            var,
            path)

    @staticmethod
    def prepend_path(var, *path) -> 'EnvAction':
        return EnvAction(
            EnvAction.Type.PathPrepend,
            var,
            path)

    @staticmethod
    def setenv(var, val) -> 'EnvAction':
        return EnvAction(
            EnvAction.Type.Set,
            var,
            val)

    @staticmethod
    def append(var, *val) -> 'EnvAction':
        return EnvAction(
            EnvAction.Type.Append,
            var,
            val)
