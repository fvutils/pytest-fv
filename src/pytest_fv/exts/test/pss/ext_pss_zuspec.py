#****************************************************************************
#* ext_pss_zuspec.py
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
import sys
from pytest_fv import Flow, TaskDelegator
from .ext_pss import ExtPSS

class ExtPSSZuspec(ExtPSS):

    def __init__(self):
        super().__init__("zuspec")

    async def genApi(self, flow, builddir):
        print("genApi")
        if not os.path.isdir(builddir):
            os.makedirs(builddir)

        deps = flow.fs.getFiles(self.pss_vlnv)

        files = []
        file_type = {'pssSource'}
        file_flags = {'is_toplevel': True}
        for dep in deps:
            d_files = dep.get_files(file_flags)

            for f in d_files:
                if f['file_type'] in file_type:
                    files.append(os.path.join(dep.core_root, f['name']))

        with open(os.path.join(builddir, "pss_files.f"), "w") as fp:
            for f in files:
                fp.write("%s\n" % f)

        with open(os.path.join(builddir, "pss_files.pss"), "w") as fp:
            for f in files:
                with open(f, "r") as fp_pss:
                    fp.write(fp_pss.read())

        python_bindir = os.path.dirname(sys.executable)
        env = os.environ.copy()
        env["PATH"] = python_bindir + ":" + env["PATH"]

        cmd = ['zuspec', 'gen-sv-import-api']
        cmd.extend(files)

        res = subprocess.run(
            cmd,
            cwd=builddir,
            env=env)
        
        if res.returncode != 0:
            raise Exception("Failed to generate PSS API")
        

#        with open(os.path.join(builddir, "pss_api_pkg.sv"), "w") as fp:
#            fp.write("package pss_api_pkg;\n")
#            fp.write("endpackage\n")

        pass

    def apply(self, flow):

        builddir = flow.getBuildDir()
        pss_builddir = os.path.join(builddir, "zuspec")

        flow.addTaskToPhase("build.pre", TaskDelegator(
            "zuspec.gen.api_pkg",
            self.genApi(flow, pss_builddir)))

        # Add the DPI library path for the simulator
        try:
            import zsp_sv
        except Exception as e:
            print("Error: Failed to import package zsp_sv")
            raise e

        libpath = os.path.join(
            zsp_sv.get_libdirs()[0],
            "lib" + zsp_sv.get_libs()[0])

        zuspec_sv = None
        for inc in zsp_sv.get_incdirs():
            if os.path.exists(os.path.join(inc, "zsp/sv/zuspec.sv")):
                zuspec_sv = os.path.join(inc, "zsp/sv/zuspec.sv")

        if zuspec_sv is None:
            raise Exception("Failed to find zuspec.sv")

        sim = flow.getTool("sim")
        # Register Zuspec core package and the generated API as 
        # pre-files to compile

        sim.addPreFilePath(zuspec_sv)
        sim.addPreFilePath(os.path.join(pss_builddir, "pss_api_pkg.sv"))

        sim.plusargs.append("zuspec.pssfiles=%s" % os.path.join(pss_builddir, "pss_files.pss"))

        sim.dpi_libs.append(libpath)

        pass

