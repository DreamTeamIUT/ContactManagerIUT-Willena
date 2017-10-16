import json
import os

from appData import Contact


class JsonInputOutput:
    EXT = ".json"

    @staticmethod
    def export_data(contacts, file_path):

        if not file_path.endswith(JsonInputOutput.EXT):
            file_path += JsonInputOutput.EXT

        folder = os.path.dirname(file_path)
        if not os.path.exists(folder):
            os.makedirs(folder)
        with open(file_path, "w") as file:
            file.write(json.dumps([i.get_dic() for i in contacts], indent=4))

        return file_path

    @staticmethod
    def import_data(file_path):
        temp = []
        with open(file_path, 'r') as file:
            data = json.loads(file.read())
            for i in data:
                temp.append(Contact.Contact.from_dic(i))
        return temp


instance = {"format": "json", "class": JsonInputOutput}
