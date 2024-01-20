#****************************************************************************
#* test_util.py
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

class Util(object):

    def __init__(self, request):
        cwd = os.getcwd()
        rundir = os.path.join(cwd, "rundir")

        self.test_rundir = os.path.join(rundir, request.node.name)

        if os.path.isdir(self.test_rundir):
            shutil.rmtree(self.test_rundir)
        os.makedirs(self.test_rundir)

        pass

    def mkFile(self, path, content):
        fullpath = os.path.join(self.test_rundir, path)
        fulldir = os.path.dirname(fullpath)

        if not os.path.isdir(fulldir):
            os.makedirs(fulldir)
        
        with open(fullpath, "w") as fp:
            fp.write(content)

    def mkCore(self, vlnv, paths):
        name = vlnv.replace(':','_')

        with open(os.path.join(self.test_rundir, "%s.core" % name), "w") as fp:
            fp.write("CAPI=2:\n")
            fp.write("name: %s\n" % vlnv)
            fp.write("\n")
            fp.write("filesets:\n")
            fp.write("  hvl:\n")
            fp.write("    files:\n")
            for path in paths:
                fp.write("    - \"%s\"\n" % path)
                fp.write("    file_type: systemVerilogSource\n")
            fp.write("\n")
            fp.write("targets:\n")
            fp.write("  default:\n")
            fp.write("    filesets:\n")
            fp.write("      - hvl\n")

    def assertLineExists(self, file, line):
        assert os.path.isfile(file)

        found = False
        with open(file, "r") as fp:
            for l in fp.readlines():
                l = l.strip()
                if l == line:
                    found = True
                    break
        assert found



