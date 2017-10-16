import os

from appData.EasyMenu import EasyMenu
from appData.DataManipulation import DataManipulation
from appData import io_formats, Contact

#Classe gérant l'application en ligne de commande interactive


class CliApp:
    DEFAULT_FILE_PATH = "data/base.csv"
    DEFAULT_DB_FORMAT = "csv"

    def __init__(self, base=None):
        self.contacts = []
        self.loaded = False
        self.file_path = ""

        if base is not None:
            self.contacts = io_formats.get_format_from_ext(os.path.splitext(base)[1]).import_data(base)
            if len(self.contacts) > 0:
                self.loaded = True
                self.file_path = base

        self.make_menu()

    def make_menu(self, empty=False):
        menu = EasyMenu("-" * 10 + "Contact Manager" + "-" * 10)
        menu.set_prompt("Entrez votre choix : ")
        if not self.loaded and not empty:
            menu.add_entry("Charger une base", self.load_base)
            menu.add_entry("Nouvelle base", self.create_base)
        else:
            self.loaded = True
            menu.add_entry("Visualiser la base", self.visualise)
            menu.add_entry("Exporter un/des contacts", self.select_format)
            menu.add_entry("Importer un/des contacts", self.import_menu)
            menu.add_entry("Ajouter un contact", self.add_contact)
            menu.add_entry("Editer un contact", self.edit_contact)
            menu.add_entry("Suprimer un contact", self.delete_contact)
        menu.add_entry("Convertir des données", self.convert)
        menu.add_entry("Quitter", self.quit)
        menu.show_menu()
        self.execute(menu.wait_for_choise())

    def display_base(self):
        for element in self.contacts:
            print(element)

    def import_menu(self, *args):
        file_path = input("Entrez un chemin pour le fichier: ")

        menu = EasyMenu("Importation de fichiers")
        menu.set_prompt("Votre choix (a,b,c): ")
        menu.set_multiple(True)

        files_to_process = []

        if os.path.exists(file_path):
            if os.path.isdir(file_path):
                filtered_files = DataManipulation.filter_file(DataManipulation.get_files(file_path),
                                                              tuple(io_formats.get_ext()))
                for filtered in filtered_files:
                    files_to_process.append(os.path.join(file_path, filtered))
                    menu.add_entry(filtered, None)
                menu.show_menu()
                chx = menu.wait_for_choise()
                sel = DataManipulation.get_selected_from_index(files_to_process, chx)
                for file in sel:
                    ext = os.path.splitext(file)[1]
                    print(ext)
                    l = io_formats.get_format_from_ext(ext).import_data(file_path + '/' + file)
                    self.contacts = self.contacts + l
                self.make_menu()
                return
            else:
                if file_path.endswith(tuple(io_formats.get_ext())):
                    ext = os.path.splitext(file_path)[1]
                    l = io_formats.get_format_from_ext(ext).import_data(file_path)
                    self.contacts = self.contacts + l
            self.make_menu()
            return

        print("Le chemin/fichier n'est pas valide/dans un format reconu")
        self.import_menu()

    def export_all(self, args):
        file_format = args[0]
        file_path = input("Entrez un chemin pour le fichier: ")
        io_formats.get_format(file_format).export_data(self.contacts, file_path)
        self.make_menu()

    def export_single(self, file_format):
        file_format = file_format[0]
        menu = EasyMenu("Veuillez choisir le/les contacts")
        menu.set_prompt("Votre choix (a,b,c,d): ")
        menu.set_multiple(True)

        for contact in self.contacts:
            menu.add_entry(contact.get_string(), None)

        menu.show_menu()
        chx = menu.wait_for_choise()
        contact_to_write = DataManipulation.get_selected_from_index(self.contacts, chx)
        file_path = input("Entrez un chemin pour le fichier: ")
        io_formats.get_format(file_format).export_data(contact_to_write, file_path)

        self.make_menu()

    def export(self, args):
        file_format = args[0]
        menu = EasyMenu("Que voulez vous exporter en " + file_format + " ?")
        menu.set_prompt("Votre choix : ")

        print(file_format)

        menu.add_entry("Tous les contacts", self.export_all, file_format)
        menu.add_entry("Un/plusieurs contact(s)", self.export_single, file_format)

        menu.show_menu()
        self.execute(menu.wait_for_choise())

    def select_format(self, *args):
        if len(self.contacts) == 0:
            print("Aucun contact...")
            self.make_menu()
            return
        temp_menu = EasyMenu("Selection du format d'exportation")
        temp_menu.set_prompt("Votre choix: ")
        for file_format in io_formats.get_formats():
            temp_menu.add_entry(file_format, self.export, file_format)

        temp_menu.show_menu()
        self.execute(temp_menu.wait_for_choise())

    def delete_contact(self, *args):
        menu = EasyMenu("Veuillez choisir le/les contacts")
        menu.set_prompt("Votre choix (a,b,c,d): ")
        menu.set_multiple(True)

        for contact in self.contacts:
            menu.add_entry(contact.get_string(), None)

        menu.show_menu()
        chx = menu.wait_for_choise()
        contact_to_delete = DataManipulation.get_selected_from_index(self.contacts, chx)
        for i in contact_to_delete:
            self.contacts.remove(i)
        # io_formats.get_format(self.DEFAULT_DB_FORMAT).export_data(self.contacts, self.file_path)

        self.make_menu()

    def load_base(self, *args):
        self.file_path = input("Entrez le chemin du fichier de base donnée[" + self.DEFAULT_FILE_PATH + "] :")
        if self.file_path == "":
            self.file_path = self.DEFAULT_FILE_PATH
            self.contacts = io_formats.get_format(self.DEFAULT_DB_FORMAT).import_data(self.file_path)
            self.loaded = True
        self.make_menu()

    def create_base(self, *args):
        self.file_path = input("Entrez le chemin du fichier de base donnee[" + self.DEFAULT_FILE_PATH + "] :")
        if self.file_path == '':
            self.file_path = self.DEFAULT_FILE_PATH
        try:
            f = open(self.file_path, "w+")
            f.close()
            self.make_menu(True)
        except FileNotFoundError:
            print("Impossible de creer le fichier, verifiez le chemin.")
            self.create_base()

    def edit_contact(self, *args):
        corresponding_contacts = DataManipulation.find_coresponding_contacts(self.contacts, input(
                "Entrez un mot cle pour la recherche : "))
        if len(corresponding_contacts) == 0:
            m = EasyMenu("La recherche ne donne pas de resultat (" + str(
                    len(corresponding_contacts)) + "), voulez-vous recommencer ?")
            m.set_prompt("Votre choix : ")
            m.add_entry("Oui", self.edit_contact)
            m.add_entry("Non", self.make_menu)

            m.show_menu()
            self.execute(m.wait_for_choise())
        else:
            def start_edit(*args):
                index = args[0][0]
                self.contacts[index].wizard()
                self.contacts = Contact.Contact.update_all(self.contacts)
                io_formats.get_format(self.DEFAULT_DB_FORMAT).export_data(self.contacts, self.file_path)

                self.make_menu()

            menu = EasyMenu("Veuillez choisir le contact a modifier")
            menu.set_prompt("Votre choix: ")

            for contact, i in corresponding_contacts:
                menu.add_entry(contact.get_string(), start_edit, i)

            menu.show_menu()
            self.execute(menu.wait_for_choise())

    def add_contact(self, *args):
        self.contacts.append(Contact.Contact().wizard())
        self.contacts = Contact.Contact.update_all(self.contacts)
        io_formats.get_format(self.DEFAULT_DB_FORMAT).export_data(self.contacts, self.file_path)
        self.make_menu()

    def visualise(self, *args):
        print("Liste des contacts")
        for c in self.contacts:
            print("-" * 15 + " Contact " + "-" * 15)
            print(c)
            print("-" * 15 + "-" * 9 + "-" * 15)
        self.make_menu()

    def quit(self, *args):
        print("Save and quit")
        if self.loaded:
            io_formats.get_format(self.DEFAULT_DB_FORMAT).export_data(self.contacts, self.file_path)
        exit(0)

    def execute(self, tuple):
        tuple[0](tuple[1])

    @staticmethod
    def convert_file(info):
        # print(info)
        source_format, choosed_format, chosed_path = info
        temp_import = io_formats.get_format_from_ext(source_format).import_data(chosed_path)
        # print(temp_import)
        io_formats.get_format(choosed_format).export_data(temp_import, chosed_path.replace(source_format,
                                                                                           io_formats.get_format(
                                                                                                   choosed_format).EXT))
        print("Le nouveau fichier sera écrit a côté du précédant sous le nom :" + chosed_path.replace(source_format,
                                                                                                      io_formats.get_format(
                                                                                                          choosed_format).EXT))

    def convert(self, *args):

        input_file = input("Entrez le fichier de départ : ")
        if os.path.exists(input_file):
            temp_menu = EasyMenu("Selection du format d'exportation")
            temp_menu.set_prompt("Votre choix: ")
            for file_format in io_formats.get_formats():
                if not input_file.endswith("." + file_format):
                    temp_menu.add_entry(file_format, CliApp.convert_file, os.path.splitext(input_file)[1], file_format,
                                        input_file)

            temp_menu.show_menu()
            self.execute(temp_menu.wait_for_choise())
        self.make_menu()
