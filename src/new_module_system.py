from newlib.objects import tsh_objects
from newlib.define import Module
from newlib.math_tsh import tsh_math
from newlib.tools import tools
from newlib.sounds import sounds 
from newlib.comparison import comparison
class Modules:
    modules = dict()

    def add(self, module: Module):
        self.modules[module.name] = module.content

modules = Modules()
modules.add(tsh_objects)
modules.add(tsh_math)
modules.add(tools)
modules.add(comparison)
modules.add(sounds)