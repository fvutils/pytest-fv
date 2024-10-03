import os
import pytest

class DirConfig(object):

    def __init__(self, 
                 request : pytest.FixtureRequest,
                 pytestconfig : pytest.Config):
        from .fv_config import FvConfig
        self._cfg = FvConfig.inst(request, pytestconfig)
        self.request = request
        self._rundir = os.path.join(self._cfg.rootdir, "rundir")

    @property
    def config(self) -> 'pytest_fv.FvConfig':
        return self._cfg

    def builddir(self, name="build"):
        return os.path.join(self._rundir, name)
    
    def rundir(self, seed=None):
        print("module: %s" % str(self.request.module.__name__))
        return os.path.join(self._rundir, 
                            self.request.module.__name__ + "_" + self.request.node.name)
    
    def test_srcdir(self):
        return os.path.dirname(self.request.path)
    
    def mkBuildDirFile(self, path, content):
        fullpath = os.path.join(self.builddir(), path)
        if not os.path.isdir(os.path.dirname(fullpath)):
            os.makedirs(os.path.dirname(fullpath))
        with open(fullpath, "w") as fp:
            fp.write(content)
        return fullpath


@pytest.fixture
def dirconfig(request, pytestconfig):
    return DirConfig(request, pytestconfig)
