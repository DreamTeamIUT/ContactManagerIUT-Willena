import base64
import os
import re
import urllib.request

from appData.field_types.basic_field import BasicField


class ImageField(BasicField):
    DESCRIPTION = "Champs destiné a prendre en charge les image jpeg"
    NAME = "Image Jpeg"

    def __init__(self, write_name, name="", value="", canskip=False):
        super().__init__(write_name, name=name, value=value, canskip=canskip)

    def set_value(self, path):

        if re.match("^([A-Za-z0-9+\/]{4})*([A-Za-z0-9+\/]{4}|[A-Za-z0-9+\/]{3}=|[A-Za-z0-9+\/]{2}==)$", path):
            self.value = path
            return

        if re.match("(https?:\/\/)([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?", path):
            print("downloading image...")
            path, message = urllib.request.urlretrieve(path)
        if os.path.exists(path):
            print("reading image...")
            with open(path, "rb") as image_file:
                self.value = base64.b64encode(image_file.read()).decode('UTF-8')
            return

        self.value = ""
        return

    def get_value(self):
        return '*binary data*'

    def is_valid(self, value=""):
        if value == "" and self.can_skip:
            return True

        if re.match("^([A-Za-z0-9+\/]{4})*([A-Za-z0-9+\/]{4}|[A-Za-z0-9+\/]{3}=|[A-Za-z0-9+\/]{2}==)$", value):
            return True

        if re.match("(https?:\/\/)([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?", value):
            print("checking image...")
            with urllib.request.urlopen(value) as response:
                info = response.info()
                if info.get_content_type() == "image/jpeg":
                    return True
            return False
        if os.path.exists(value):
            if value.lower().endswith(".jpg") or value.lower().endswith(".jpeg"):
                print("Path ok")
                return True
            else:
                print("Merci de fournir une image au format jpeg.")
            return False
        print("Merci d'entrer un chemin ou une URL(http) valide")
        return False

    def get_error_message(self, value=""):
        if not self.can_skip and value == "":
            return "Champ obligatoire"

        return "Merci de fournir une image au format jpeg (url http ou fichier)."


instance = {"type": "ImageField", "class": ImageField}
