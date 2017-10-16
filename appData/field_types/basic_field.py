class BasicField:
    DESCRIPTION = "Champ simple sans validation particulière"
    NAME = "Texte"

    def __init__(self, write_name, name="", value="", canskip=False):
        self.name = name if name != "" else write_name
        self.value = value
        self.writabe_name = write_name
        self.can_skip = canskip

    def set_name(self, name: str):
        self.name = name.replace(' ', '_')

    def set_value(self, value: str):
        self.value = value

    def get_name(self):
        return self.name

    def get_WName(self):
        return self.writabe_name

    def get_value(self):
        return self.value

    def is_valid(self, value=""):
        return True

    def get_error_message(self):
        return ''

    def ask_value(self):
        str_to_write = "(%s)%s" % (self.name, "*" if not self.can_skip else "") + (
            "[%s]" % self.value if len(self.value) > 0 else "") + " : "
        v = input(str_to_write)

        if v == "" and self.value != "":
            return

        if v == "" and self.can_skip:
            self.set_value("")
            return

        if not self.is_valid(v):
            return self.ask_value()
        else:
            self.set_value(v)
            return


instance = {"type": "BasicField", "class": BasicField}
