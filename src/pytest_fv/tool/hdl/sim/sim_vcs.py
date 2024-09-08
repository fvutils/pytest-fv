#****************************************************************************
#* sim_vcs.py
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
from pytest_fv import HdlSim, ToolRgy, ToolKind, FSConfig
from .sim_vlog_base import SimVlogBase

class SimVCS(SimVlogBase):

    def __init__(self, builddir):
        super().__init__(builddir, FSConfig({
            "systemVerilogSource", "verilogSource"}, {
                "sv-uvm": True}))
        pass

    async def build(self):
        src_l, cpp_l, inc_s, def_m = self._getSrcIncDef()

        logfile = self.build_logfile
        if not os.path.isabs(logfile):
            logfile = os.path.join(self.builddir, logfile)

        if not os.path.isdir(os.path.dirname(logfile)):
            os.makedirs(os.path.dirname(logfile))
            
        with open(logfile, "w") as log:
            pass

#        if self.hasFlag("sv-uvm"):
        if True:
            cmd = ['vlogan', "-sverilog", '-ntb_opts', 'uvm']
            cmd.append("-timescale=1ns/1ps")

            with open(logfile, "a") as log:
                log.write("** Compile UVM: %s\n" % str(cmd))
                log.flush()
                res = subprocess.run(
                    cmd, 
                    cwd=self.builddir,
                    stderr=subprocess.STDOUT,
                    stdout=log)

                log.write("return-code: %d\n" % res.returncode)

                if res.returncode != 0:
                    raise Exception("UVM compilation failed")

        cmd = [
            'vlogan', "-sverilog"
        ]

#        if self.hasFlag("sv-uvm"):
        if True:
            cmd.extend(["-ntb_opts", "uvm"])

        for inc in inc_s:
            cmd.append('+incdir+%s' % inc)

        for key,val in def_m.items():
            if val is None or val == "":
                cmd.append("+define+%s" % key)
            else:
                cmd.append("+define+%s=%s" % (key, val))

        if len(src_l) == 0 and len(self._prefile_paths) == 0:
            raise Exception("No source files specified")

        cmd.append("-timescale=1ns/1ps")

        if self.debug:
            cmd.extend(['-kdb', '-debug_access'])

        for vsrc in self._prefile_paths:
            cmd.append(vsrc)

        for vsrc in src_l:
            cmd.append(vsrc)

        with open(logfile, "a") as log:
            log.write("** Compile: %s\n" % str(cmd))
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

        cmd = [ 'vcs' ]

        cmd.append("-timescale=1ns/1ps")

#        if self.hasFlag("sv-uvm"):
        if True:
            cmd.extend(["-ntb_opts", "uvm"])

        if len(self.top) == 0:
            raise Exception("Must specify root module")

        for top in self.top:
            cmd.extend(['-top', top])

#        cmd.extend(['-o', 'top', '-timescale', '1ns/1ps'])
        if self.debug:
            cmd.append('-debug_access')

        with open(logfile, "a") as log:
            log.write("** Elab: %s\n" % str(cmd))
            log.flush()
            res = subprocess.run(
                cmd, 
                cwd=self.builddir,
                stderr=subprocess.STDOUT,
                stdout=log)

            if res.returncode != 0:
                raise Exception("Compilation failed")

    async def run(self, args : HdlSim.RunArgs):
        cmd = [ os.path.join(self.builddir, "simv") ] # '-batch' ]

        if not os.path.isdir(args.rundir):
            os.makedirs(args.rundir)
        cmd.extend(['-ucli', '-i', 'run.tcl'])

        with open(os.path.join(args.rundir, "run.tcl"), "w") as fp:
            # if args.debug:
            #     fp.write("if {[catch {vcd file sim.vcd} errmsg]} {\n")
            #     fp.write("  puts \"Failed to open VCD file: $errmsg\"\n")
            #     fp.write("  exit 1\n")
            #     fp.write("}\n")
            #     spec = ""
            #     for t in self.top:
            #         spec += " /%s/*" % t
            #     fp.write("if {[catch {vcd add -r%s} errmsg]} {\n" % spec)
            #     fp.write("  puts \"Failed to add traces: $errmsg\"\n")
            #     fp.write("  exit 1\n")
            #     fp.write("}\n")

            fp.write("run\n")

            # if args.debug:
            #     fp.write("if {[catch {flush_vcd} errmsg]} {\n")
            #     fp.write("  puts \"Failed to flush VCD: $errmsg\"\n")
            #     fp.write("  exit 1\n")
            #     fp.write("}\n")

            fp.write("quit\n")

        for pa in args.plusargs:
            cmd.append("+%s" % pa)

        logfile = args.run_logfile
        if not os.path.isabs(logfile):
            logfile = os.path.join(args.rundir, logfile)

        if not os.path.isdir(os.path.dirname(logfile)):
            os.makedirs(os.path.dirname(logfile))

        with open(logfile, "w") as log:
            log.write("** Command: %s\n" % str(cmd))
            log.flush()
            res = subprocess.run(
                cmd,
                cwd=args.rundir,
                env=self.env,
                stderr=subprocess.STDOUT,
                stdout=log)
            
            if res.returncode != 0:
                raise Exception("Run failed")

        pass


ToolRgy.register(ToolKind.Sim, "vcs", SimVCS)

