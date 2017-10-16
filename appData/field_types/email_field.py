import re

from appData.field_types.basic_field import BasicField


class EmailField(BasicField):
    DESCRIPTION = "Champs adapté aux email. Verifie que l'adresse respecte un bon format"
    NAME = "Email"

    def __init__(self, write_name, name="", value="", canskip=False):
        super().__init__(write_name, name=name, value=value, canskip=canskip)

    def is_valid(self, value=""):
        if value == "" and self.can_skip:
            return True

        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", value):
            return True
        else:
            print(self.get_error_message())
            return False

    def get_error_message(self, value=""):
        if not self.can_skip and value == "":
            return "Champ obligatoire"

        return "L'email n'est pas au bon format"


instance = {"type": "EmailField", "class": EmailField}
