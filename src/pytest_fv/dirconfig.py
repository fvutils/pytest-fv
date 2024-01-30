import os
import pytest

class DirConfig(object):

    def __init__(self, request):
        self.request = request

        self._rundir = os.path.join(os.getcwd(), "rundir")
        pass

    def builddir(self, name="build"):
        return os.path.join(self._rundir, name)
    
    def rundir(self, seed=None):
        return os.path.join(self._rundir, 
                            self.request.node.name)


@pytest.fixture
def dirconfig(request):
    return DirConfig(request)
