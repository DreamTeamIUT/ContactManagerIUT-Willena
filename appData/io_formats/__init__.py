import pkgutil

__all__ = {}

for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    module = loader.find_module(module_name).load_module(module_name)
    __all__[module.instance["format"]] = module.instance["class"]
    exec('%s = module' % module_name)

#print("modules ", __all__)


def get_format(string):
    return __all__[string]


def get_formats():
    return __all__


def get_ext():
    return [__all__[f].EXT for f in __all__.keys()]


def get_format_from_ext(ext):
    for f in __all__.keys():
        if ext == __all__[f].EXT:
            return __all__[f]
    return None
