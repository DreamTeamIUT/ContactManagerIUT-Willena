import phonenumbers

from appData.field_types.basic_field import BasicField


class PhoneField(BasicField):
    DESCRIPTION = "Champ destiné à prendre en charge les numéros de téléphones et les mettre sous format international"
    NAME = "Téléphone"

    def __init__(self, write_name, name="", value="", canskip=False):
        super().__init__(write_name, name=name, value=value, canskip=canskip)

    def set_value(self, value: str):
        self.value = str(phonenumbers.format_number(phonenumbers.parse(value, None),
                                                    phonenumbers.PhoneNumberFormat.INTERNATIONAL)) if value != "" else ""

    def is_valid(self, value=""):
        if value == "" and self.can_skip:
            return True

        if value.startswith("+"):
            try:
                phonenumbers.parse(value, None)
                return True
            except:
                print(self.get_error_message())
                return False

        print(self.get_error_message())
        return False

    def get_error_message(self, value=""):
        if not self.can_skip and value == "":
            return "Champ obligatoire"

        return "Entrez un telephone valide (+xxx xxxxxxxxx) "


instance = {"type": "PhoneField", "class": PhoneField}
