#****************************************************************************
#* console.py
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
import asyncio
import subprocess
import sys
import ivpm

class Console(object):

    _inst = None

    def __init__(self):
        pass

    def println(self, line):
        sys.stdout.write(line)
        sys.stdout.write("\n")

    def write(self, log_fp, line):
        if log_fp is not None:
            log_fp.write(line)
        sys.stdout.write(line)

    def run(self, log_fp, cmd, **kwargs):
        loop = asyncio.get_running_loop()

        class Protocol(asyncio.SubprocessProtocol):
            def __init__(self, console, exit_future):
                print("Protocol", flush=True)
                self.exit_future = exit_future

            def __call__(self):
                return self
            
            def process_exited(self) -> None:
                print("process_exited")
                pass

        proc = ivpm.ivpm_popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            **kwargs)

        line = ""
        while True:
            c = proc.stdout.read(16)
#            print("c: %s" % str(c), flush=True)
            if len(c) == 0:
                break
            else:
                line += c.decode()
            while True:
                next = line.find("\n")
                if next != -1:
                    self.write(log_fp, line[:next+1])
                    line = line[next+1:]
                else:
                    break

        while proc.poll() is None:
            proc.wait()

        return proc



    @classmethod
    def inst(cls):
        if cls._inst is None:
            cls._inst = Console()
        return cls._inst


