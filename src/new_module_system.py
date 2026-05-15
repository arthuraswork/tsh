from stdlib.objects import tsh_objects
from stdlib.define import Module
from stdlib.math_tsh import tsh_math
from stdlib.tools import tools
from stdlib.sounds import sounds 
from stdlib.comparison import comparison
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