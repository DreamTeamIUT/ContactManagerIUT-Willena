import os
import shutil
from random import randint
from zipfile import ZipFile

from appData.Contact import Contact
from appData.DataManipulation import DataManipulation
from appData.io_formats.vcard_io import VcardInputOutput


class ZipInputOutput:
    EXT = ".zip"

    @staticmethod
    def export_data(contacts, file_path: str):
        if not file_path.endswith(ZipInputOutput.EXT):
            file_path += ZipInputOutput.EXT

        folder = os.path.dirname(file_path)
        if not os.path.exists(folder):
            os.makedirs(folder)

        if len(contacts) > 0:
            if type(contacts[0]) is Contact:
                contacts = VcardInputOutput.export_data(contacts, "./tmp/" + str(randint(0, 50)) + '.vcf')
            if type(contacts) is list:
                with ZipFile(file_path, 'w') as file:
                    for f in contacts:
                        file.write(os.path.abspath(f), os.path.basename(f))
            else:
                with ZipFile(file_path, 'w') as file:
                    file.write(os.path.abspath(contacts), os.path.basename(contacts))
        return file_path

    @staticmethod
    def import_data(file_path):
        from appData import io_formats
        tmp_folder = "./tmp/" + os.path.splitext(os.path.basename(file_path))[0]
        if os.path.exists(tmp_folder):
            shutil.rmtree(tmp_folder)

        os.makedirs(tmp_folder)

        with ZipFile(file_path, 'r') as file:
            file.extractall(tmp_folder)

        files = DataManipulation.filter_file(DataManipulation.get_files(tmp_folder+'/tmp/'), tuple(io_formats.get_ext()))
        print(files)
        contacts = []
        for f in files:
            contacts += io_formats.get_format_from_ext(os.path.splitext(f)[1]).import_data(tmp_folder+'/tmp/'+f)
        return contacts


instance = {"format": "zip", "class": ZipInputOutput}
