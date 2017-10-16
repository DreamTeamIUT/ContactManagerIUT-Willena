import datetime

from appData.field_types.basic_field import BasicField


class DateField(BasicField):
    DESCRIPTION = "Champ destiné aux dates. Une verification est appliqué afin que la date soit au bon format"
    NAME = "Date"

    def __init__(self, write_name, name="", value="", canskip=False):
        super().__init__(write_name, name=name, value=value, canskip=canskip)

    def is_valid(self, value=""):
        if value == "" and self.can_skip:
            return True

        try:
            datetime.datetime.strptime(value, '%d/%m/%Y')
            return True
        except ValueError:
            print(self.get_error_message())
            return False

    def get_error_message(self, value=""):
        if not self.can_skip and value == "":
            return "Champ obligatoire"

        return 'La date doit avoir le format JJ-MM-AAAA'


instance = {"type": "DateField", "class": DateField}
