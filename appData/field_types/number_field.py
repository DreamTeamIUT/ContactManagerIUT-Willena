from appData.field_types.basic_field import BasicField


class NumberField(BasicField):
    DESCRIPTION = "Champ destiné a contenir des nombre flottant. Tout autre valeur est refusé"
    NAME = "Nombre "

    def __init__(self, write_name, name="", value="", canskip=False):
        super().__init__(write_name, name=name, value=value, canskip=canskip)

    def is_valid(self, value=""):
        if value == "" and self.can_skip:
            return True

        try:
            float(value)
            return True
        except:
            print(self.get_error_message())
            return False

    def get_error_message(self, value=""):
        if not self.can_skip and value == "":
            return "Champ obligatoire"

        return "La valeur n'est pas un nombre valide !"

instance = {"type": "NumberField", "class": NumberField}
