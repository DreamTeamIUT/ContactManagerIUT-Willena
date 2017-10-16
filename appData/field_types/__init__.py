import pkgutil

__all__ = {}

for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    module = loader.find_module(module_name).load_module(module_name)
    __all__[module.instance["type"]] = module.instance["class"]
    exec('%s = module' % module_name)

#print("modules ", __all__)


def get_field(field_type):
    try:
        return __all__[field_type]
    except:
        print("Erreur champ inexistant!")


def get_fields():
    return __all__


def get_field_by_index(index):
    i = 0
    for field in __all__:
        if i == index:
            return __all__[field]
        i += 1
    raise NotImplementedError("Champ inexistant")
