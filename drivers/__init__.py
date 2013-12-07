# import os
# import glob
# __all__ = [ os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__)+"/drivers/*.py")] + [ os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__)+"/postprocessors/*.py")]

__all__ = []

import pkgutil
import inspect

for loader, name, is_pkg in pkgutil.walk_packages(__path__):
    module = loader.find_module(name).load_module(name)

    for name, value in inspect.getmembers(module):
        if name.startswith('__'):
            continue

        globals()[name] = value
        __all__.append(name)