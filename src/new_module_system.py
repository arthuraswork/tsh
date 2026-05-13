from newlib.objects import objects
from newlib.define import Module

class Modules:
    modules = dict()

    def add(self, module: Module):
        self.modules[module.name] = module.content

modules = Modules()
modules.add(objects)
