#****************************************************************************
#* sim_mti.py
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

class SimMti(SimVlogBase):

    def __init__(self, builddir):
        super().__init__(builddir, FSConfig({
            "systemVerilogSource", "verilogSource"}, {
            "sv-uvm" : True}))
        pass

    async def build(self):
        src_l, cpp_l, inc_s, def_m = self._getSrcIncDef()

        cmd = [
            'vlog', "-sv"
        ]

#        if self.hasFlag("sv-uvm"):
        cmd.extend(["-L", "uvm"])

        for inc in inc_s:
            cmd.append('+incdir+%s' % inc)

        for key,val in def_m.items():
            if val is None or val == "":
                cmd.append("+define+%s" % key)
            else:
                cmd.append("+define+%s=%s" % (key, val))

        if len(src_l) == 0 and len(self._prefile_paths) == 0:
            raise Exception("No source files specified")
        
        for vsrc in self._prefile_paths:
            cmd.append(vsrc)

        for vsrc in src_l:
            cmd.append(vsrc)

        logfile = self.build_logfile
        if not os.path.isabs(logfile):
            logfile = os.path.join(self.builddir, logfile)

        if not os.path.isdir(self.builddir):
            os.makedirs(self.builddir)

        print("cmd: %s" % str(cmd))
        with open(logfile, "w") as log:
            log.write("** Compile\n")
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

        cmd = [ 'vopt' ]
#        '--relax',  '--snapshot', 'snap' ]

        if len(self.top) == 0:
            raise Exception("Must specify root module")

        for top in self.top:
            cmd.append(top)

        cmd.extend(['-o', '__simv', '-timescale', '1ns/1ps'])
        if self.debug:
            cmd.append('-debug')

        print("cmd: %s" % str(cmd))
        with open(logfile, "a") as log:
            log.write("** Elab\n")
            log.flush()
            res = subprocess.run(
                cmd, 
                cwd=self.builddir,
                stderr=subprocess.STDOUT,
                stdout=log)

            if res.returncode != 0:
                raise Exception("Compilation failed")

    async def run(self, args : HdlSim.RunArgs):

        if not os.path.isdir(args.rundir):
            os.makedirs(args.rundir)

        logfile = args.run_logfile
        if not os.path.isabs(logfile):
            logfile = os.path.join(args.rundir, logfile)

        m = "w"

        if self.builddir != args.rundir:
            # Need to map 
            cmd = [ 'vmap', 'work', os.path.join(self.builddir, 'work') ]

            with open(logfile, m) as log:
                m = "a"
                res = subprocess.run(
                    cmd,
                    cwd=args.rundir,
                    stdout=log,
                    stderr=subprocess.STDOUT)
            
            if res.returncode != 0:
                raise Exception("Failed to map library")

        cmd = [ 'vsim', '-batch' ]

#        cmd.extend(['-valgrind', '--tool=memcheck'])

        cmd.extend(['-do', 'run.tcl'])

        with open(os.path.join(args.rundir, "run.tcl"), "w") as fp:
#            fp.write("puts $env(LD_LIBRARY_PATH)\n")
#            fp.write("puts $env(PYTHONPATH)\n")
            if args.debug:
                # fp.write("if {[catch {vcd file sim.vcd} errmsg]} {\n")
                # fp.write("  puts \"Failed to open VCD file: $errmsg\"\n")
                # fp.write("  exit 1\n")
                # fp.write("}\n")
                # spec = ""
                # for t in self.top:
                #     spec += " /%s/*" % t
                # fp.write("if {[catch {vcd add -r%s} errmsg]} {\n" % spec)
                # fp.write("  puts \"Failed to add traces: $errmsg\"\n")
                # fp.write("  exit 1\n")
                # fp.write("}\n")
                pass

            fp.write("run -all\n")

            # if args.debug:
            #     fp.write("if {[catch {flush_vcd} errmsg]} {\n")
            #     fp.write("  puts \"Failed to flush VCD: $errmsg\"\n")
            #     fp.write("  exit 1\n")
            #     fp.write("}\n")

            fp.write("quit -f\n")

        cmd.append('__simv')

        for dpi in args.dpi_libs:
            if dpi.endswith(".so"):
                dpi = dpi[:-3]
            cmd.extend(["-sv_lib", dpi])

        for pli in args.pli_libs:
            cmd.extend(["-pli", pli])

        for pa in args.plusargs:
            cmd.append("+%s" % pa)

        with open(logfile, m) as log:
            m = "a"
            res = subprocess.run(
                cmd,
                cwd=args.rundir,
                env=args.env,
                stderr=subprocess.STDOUT,
                stdout=log)
            
            if res.returncode != 0:
                raise Exception("Run failed")

        pass


ToolRgy.register(ToolKind.Sim, "mti", SimMti)

