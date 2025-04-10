import pkgutil
from importlib.util import spec_from_file_location, module_from_spec
from os import path
from sys import modules

from aiogram import Dispatcher

__all__ = []

for _loader, module_name, _is_pkg in pkgutil.walk_packages(__path__):
    __all__.append(module_name)

    _spec = spec_from_file_location(module_name, location=path.join(__path__[0], module_name + '.py'))
    _module = module_from_spec(_spec)
    _spec.loader.exec_module(_module)
    modules[module_name] = _module


def register_handlers(dp: Dispatcher):
    for module in __all__:
        modules[module].register_handlers(dp)
