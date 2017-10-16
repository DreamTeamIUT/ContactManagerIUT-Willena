from appData.field_types.basic_field import BasicField


class NameField(BasicField):
    DESCRIPTION = "Champ correspondant aux noms propre. Mise en majuscule automatique de la première lettre"
    NAME = "Nom propre"

    def __init__(self, write_name,  name="", value="", canskip=False):
        super().__init__(write_name, name=name, value=value, canskip=canskip)

    def set_value(self, value: str):
        self.value = value.title()

    def is_valid(self, value=""):
        if value == "" and self.can_skip:
            return True

        if len(value) > 0:
            return True
        else:
            print(self.get_error_message())
            return False

    def get_error_message(self, value=""):
        if not self.can_skip and value == "":
            return "Champ obligatoire"

        if not self.is_valid(value):
            return "La chaine entrée est invalide"

instance = {"type": "NameField", "class": NameField}
