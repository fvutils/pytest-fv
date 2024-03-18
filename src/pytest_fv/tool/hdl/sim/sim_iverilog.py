#****************************************************************************
#* sim_i_verilog.py
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
from pytest_fv import HdlSim, ToolRgy, ToolKind
from pytest_fv.fs_config import FSConfig
from .sim_vlog_base import SimVlogBase

class SimIVerilog(SimVlogBase):

    def __init__(self, builddir):
        super().__init__(builddir, FSConfig({"verilogSource"}, {}))

    async def build(self):
        src_l, cpp_l, inc_s, def_m = self._getSrcIncDef()

        cmd = [
            'iverilog', "-g2012"
        ]

        for inc in inc_s:
            cmd.append('-I')
            cmd.append(inc)

        for key,val in def_m.items():
            cmd.append("-D")
            if val is None or val == "":
                cmd.append(key)
            else:
                cmd.append("%s=%s" % (key, val))

        for top in self.top:
            cmd.append('-s')
            cmd.append(top)
        
        cmd.extend(['-o', 'simv.vvp'])

        if len(src_l) == 0:
            raise Exception("No source files specified")

        for vsrc in src_l:
            cmd.append(vsrc)


        logfile = self.build_logfile
        if not os.path.isabs(logfile):
            logfile = os.path.join(self.builddir, logfile)

        if not os.path.isdir(os.path.dirname(logfile)):
            os.makedirs(os.path.dirname(logfile))

        print("cmd: %s" % str(cmd))
        with open(logfile, "w") as log:
            log.write("** Compile\n")
            log.write("** Command: %s\n" % str(cmd))
            log.flush()
            res = subprocess.run(
                cmd, 
                cwd=self.builddir,
                stderr=subprocess.STDOUT,
                stdout=log)
            
            if res.returncode != 0:
                raise Exception("Compilation failed")

        if len(cpp_l) > 0:
            print("TODO: need to compile DPI")

    async def run(self, run_args : HdlSim.RunArgs):
        cmd = [ 'vvp' ]

        for pli in run_args.pli_libs:
            cmd.extend(['-m', pli])

        cmd.append(os.path.join(self.builddir, 'simv.vvp'))

        for pl in run_args.plusargs:
            cmd.append("+%s" % pl)

        logfile = run_args.run_logfile
        if not os.path.isabs(logfile):
            logfile = os.path.join(run_args.rundir, logfile)

        if not os.path.isdir(os.path.dirname(logfile)):
            os.makedirs(os.path.dirname(logfile))

        with open(logfile, "w") as log:
            log.write("** Command: %s\n" % str(cmd))
            log.write("** CWD: %s\n" % run_args.rundir)
            log.flush()
            res = subprocess.run(
                cmd,
                cwd=run_args.rundir,
                env=run_args.env,
                stderr=subprocess.STDOUT,
                stdout=log)
            
            if res.returncode != 0:
                raise Exception("Run failed")

        pass


ToolRgy.register(ToolKind.Sim, "ivl", SimIVerilog)

