#****************************************************************************
#* sim_xcelium.py
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

class SimXcelium(SimVlogBase):

    def __init__(self, builddir):
        super().__init__(builddir, FSConfig({
            "systemVerilogSource", "verilogSource"}, {
            "sv-uvm" : True}))
        self.xcm_home = None
        pass

    async def build(self):
        self.init_xcm_home()

        src_l, cpp_l, inc_s, def_m = self._getSrcIncDef()

        cmd = [
            'xmvlog', "-sv", "-plussv", "-newsv"
        ]

        # Enable support for class type parameters without a default value
        self.setenv("CADENCE_ENABLE_AVSREQ_44905_PHASE_1", "1")
        self.setenv("CADENCE_ENABLE_AVSREQ_63188_PHASE_1", "1")

#        if self.hasFlag("sv-uvm"):
        if True:
            uvm_home = os.path.join(self.xcm_home, "tools/methodology/UVM/CDNS-1.2")
            cmd.extend(["-incdir", os.path.join(uvm_home, "sv/src")])
            cmd.append(os.path.join(uvm_home, "sv/src/uvm_pkg.sv"))

            self.dpi_libs.append(os.path.join(uvm_home, "additions/sv/lib/libuvmdpi.so"))

        for inc in inc_s:
            cmd.append('-incdir')
            cmd.append(inc)

        for key,val in def_m.items():
            cmd.append("-define")
            if val is None or val == "":
                cmd.append(key)
            else:
                cmd.append("%s=%s" % (key, val))

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

        with open(logfile, "w") as log:
            log.write("** Compile: %s\n" % str(cmd))
            log.flush()
            res = subprocess.run(
                cmd, 
                cwd=self.builddir,
                env=self.env,
                stderr=subprocess.STDOUT,
                stdout=log)
            
            if res.returncode != 0:
                raise Exception("Compilation failed")

        if len(cpp_l) > 0:
            print("TODO: need to compile DPI")

        cmd = [ 'xmelab' ]

        if len(self.top) == 0:
            raise Exception("Must specify root module")

        for top in self.top:
            cmd.append(top)

        cmd.extend(['-snapshot', 'top:snap', '-timescale', '1ns/1ps'])
#        if self.debug:
#            cmd.extend(['-debug', 'all'])

        print("cmd: %s" % str(cmd))
        with open(logfile, "a") as log:
            log.write("** Elab %s\n" % str(cmd))
            log.flush()
            res = subprocess.run(
                cmd, 
                cwd=self.builddir,
                stderr=subprocess.STDOUT,
                stdout=log)

            if res.returncode != 0:
                raise Exception("Compilation failed")

    async def run(self, args : HdlSim.RunArgs):
        cmd = [ 'xmsim' ]
#        cmd.extend(['--onerror', 'quit'])
#        cmd.extend(['-t', 'run.tcl'])

        if not os.path.isdir(args.rundir):
            os.makedirs(args.rundir)

        if not os.path.exists(os.path.join(args.rundir, "xcelium.d")):
            os.symlink(
                os.path.join(self.builddir, "xcelium.d"),
                os.path.join(args.rundir, "xcelium.d"))
        
        for dpi in args.dpi_libs:
            cmd.extend(["-sv_lib", dpi])

        # with open(os.path.join(args.rundir, "run.tcl"), "w") as fp:
        #     if args.debug:
        #         fp.write("if {[catch {open_vcd sim.vcd} errmsg]} {\n")
        #         fp.write("  puts \"Failed to open VCD file: $errmsg\"\n")
        #         fp.write("  exit 1\n")
        #         fp.write("}\n")
        #         spec = ""
        #         for t in self.top:
        #             spec += " /%s/*" % t
        #         fp.write("if {[catch {log_vcd %s} errmsg]} {\n" % spec)
        #         fp.write("  puts \"Failed to add traces: $errmsg\"\n")
        #         fp.write("  exit 1\n")
        #         fp.write("}\n")

        #     fp.write("run -all\n")

        #     if args.debug:
        #         fp.write("if {[catch {flush_vcd} errmsg]} {\n")
        #         fp.write("  puts \"Failed to flush VCD: $errmsg\"\n")
        #         fp.write("  exit 1\n")
        #         fp.write("}\n")

        #     fp.write("exit\n")

        cmd.append('top:snap')

        for pa in args.plusargs:
            cmd.append('+%s' % pa)

        logfile = args.run_logfile
        if not os.path.isabs(logfile):
            logfile = os.path.join(args.rundir, logfile)

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

    def init_xcm_home(self):
        if self.xcm_home is not None:
            return

        for elem in os.environ["PATH"].split(":"):
            if os.path.isfile(os.path.join(elem, "xmvlog")):
                self.xcm_home = os.path.abspath(os.path.join(elem, "../.."))
                print("elem: %s ; xcm_home: %s" % (elem, self.xcm_home))
                break
        if self.xcm_home is None:
            raise Exception("Failed to find xmvlog in path")



ToolRgy.register(ToolKind.Sim, "xcm", SimXcelium)

