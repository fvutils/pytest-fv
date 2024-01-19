#****************************************************************************
#* sim_xsim.py
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
import subprocess
import sys
from pytest_fv import HdlToolSimRgy
from .sim_vlog_base import SimVlogBase

class SimXsim(SimVlogBase):

    def __init__(self):
        super().__init__()
        pass

    def build(self):
        src_l, cpp_l, inc_s, def_m = self._getSrcIncDef()

        cmd = [
            'xvlog', "-sv"
        ]

        if self.hasFlag("sv-uvm"):
            cmd.extend(["-L", "uvm"])

        for inc in inc_s:
            cmd.append('-i')
            cmd.append(inc)

        for key,val in def_m.items():
            cmd.append("-d")
            if val is None or val == "":
                cmd.append(key)
            else:
                cmd.append("%s=%s" % (key, val))
        
        for vsrc in src_l:
            cmd.append(vsrc)

        print("cmd: %s" % str(cmd))
        subprocess.run(cmd, stdout=sys.stdout)

        cmd = [ 'xelab', '--relax',  '--snapshot', 'snap' ]

        if self.hasFlag("sv-uvm"):
            cmd.extend(["-L", "uvm"])
        
        cmd.extend(['hdl_top', 'hvl_top'])
        print("cmd: %s" % str(cmd))
        subprocess.run(cmd, stdout=sys.stdout)
        pass



HdlToolSimRgy.inst().addSimImpl("xsim", SimXsim)

