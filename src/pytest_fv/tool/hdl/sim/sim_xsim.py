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
import os
import shutil
import subprocess
from pytest_fv import HdlSim, ToolRgy, ToolKind, Env, FSConfig
from .sim_vlog_base import SimVlogBase

class SimXsim(SimVlogBase):

    def __init__(self, builddir):
        super().__init__(builddir, FSConfig([
            "verilogSource", "systemVerilogSource"], 
            {"sv-uvm": True}))
        pass

    async def build(self):
        src_l, cpp_l, inc_s, def_m = self._getSrcIncDef()

        cmd = ['xvlog', "-sv" ] 

        if "sv-uvm" in self.fs_cfg.flags.keys():
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

        cmd = [ 'xelab' ]
#        cmd.extend(['-mt', 'off'])
#        '--relax',  '--snapshot', 'snap' ]

        if len(self.top) == 0:
            raise Exception("Must specify root module")

        for top in self.top:
            cmd.append(top)

        cmd.extend(['-relax', '-s', 'top', '-timescale', '1ns/1ps'])
        if self.debug:
            cmd.extend(['-debug', 'all'])

        if len(self.dpi_libs):
            cmd.append("--dpi_absolute")
        for dpi in self.dpi_libs:
            dpi_file = os.path.basename(dpi)
            dpi_dir = os.path.dirname(dpi)
#            if dpi_file.endswith(".so"):
#                dpi_file = dpi_file[:-3]
            cmd.extend(["-sv_root", dpi_dir, "-sv_lib", dpi_file])
#            cmd.extend(["-sv_lib", dpi])

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

        # Manage clean-up and initialization of run directory
        if args.rundir != self.builddir:
            if os.path.isdir(args.rundir):
                shutil.rmtree(args.rundir)
            os.makedirs(args.rundir)

            os.symlink(
                os.path.join(self.builddir, "xsim.dir"),
                os.path.join(args.rundir, "xsim.dir")
            )

        which_xsim = shutil.which('xsim')
        print("which_xsim: %s" % which_xsim)

        vivado_bindir = os.path.dirname(which_xsim)
        vivado_dir = os.path.dirname(vivado_bindir)
        python_dir = os.path.join(vivado_dir, "tps/lnx64/python-3.8.3")
        python_libdir = os.path.join(python_dir, "lib")

        env = Env(self.env)
        env.append_path("LD_LIBRARY_PATH", python_libdir)

        cmd = [ 'xsim' ]
        cmd.extend(['--onerror', 'quit'])
        cmd.extend(['-t', 'run.tcl'])

        with open(os.path.join(args.rundir, "run.tcl"), "w") as fp:
            if args.debug:
                fp.write("if {[catch {open_vcd sim.vcd} errmsg]} {\n")
                fp.write("  puts \"Failed to open VCD file: $errmsg\"\n")
                fp.write("  exit 1\n")
                fp.write("}\n")
                spec = ""
                for t in self.top:
                    spec += " /%s/*" % t
                fp.write("if {[catch {log_vcd %s} errmsg]} {\n" % spec)
                fp.write("  puts \"Failed to add traces: $errmsg\"\n")
                fp.write("  exit 1\n")
                fp.write("}\n")

            fp.write("run -all\n")

            if args.debug:
                fp.write("if {[catch {flush_vcd} errmsg]} {\n")
                fp.write("  puts \"Failed to flush VCD: $errmsg\"\n")
                fp.write("  exit 1\n")
                fp.write("}\n")

            fp.write("exit\n")

        cmd.append('top')


        for pa in args.plusargs:
            cmd.extend(['--testplusarg', pa])

        logfile = args.run_logfile
        if not os.path.isabs(logfile):
            logfile = os.path.join(args.rundir, logfile)

        with open(logfile, "w") as log:
            res = subprocess.run(
                cmd,
                cwd=args.rundir,
                env=env.env,
                stderr=subprocess.STDOUT,
                stdout=log)
            
            if res.returncode != 0:
                raise Exception("Run failed")

        pass


ToolRgy.register(ToolKind.Sim, "xsm", SimXsim)

