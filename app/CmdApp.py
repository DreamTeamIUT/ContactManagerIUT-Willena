import os
import shutil

from app.CliApp import CliApp
from app.WebApp import WebApp
from appData.DataManipulation import DataManipulation
from appData.Contact import Contact

class CmdApp:
    NOT_SUPPORTED_EXIT_CODE = 11
    DEFAULT_FILE_PATH = "data/base.csv"
    DEFAULT_DB_FORMAT = "csv"
    NOT_FOUND_EXIT_CODE = 10

    @staticmethod
    def loadFile(file=DEFAULT_FILE_PATH):
        from appData import io_formats
        format = io_formats.get_format_from_ext(os.path.splitext(file)[1])
        if format is None:
            print("Format non supporté !")
            exit(CmdApp.NOT_SUPPORTED_EXIT_CODE)
        contacts = format.import_data(file)
        return contacts

    @staticmethod
    def save(content, file=DEFAULT_FILE_PATH, zip=False, db=False):
        tmp_folder = "./tmp/" + os.path.splitext(os.path.basename(file))[0]
        if os.path.exists(tmp_folder):
            shutil.rmtree(tmp_folder)

        os.makedirs(tmp_folder)

        from appData import io_formats
        format = io_formats.get_format_from_ext(os.path.splitext(file)[1])
        export = format.export_data(content, file if not zip else tmp_folder+os.path.basename(file))

        if zip:
            export = io_formats.get_format("zip").export_data(export, file)

        return export

    @staticmethod
    def parse(args):
        if args.formats:
            CmdApp.print_formats()
            return True
        elif args.fields:
            CmdApp.print_fields()
            return True
        elif "which" in vars(args).keys():
            if args.which == "cli":
                CliApp(args.base)
                return True
            elif args.which == "web":
                WebApp(base=args.base, port=args.port, ip=args.ip_address)
                return True
            elif args.which == "search":
                CmdApp.search(base=args.base, keyword=args.keyword)
                return True
            elif args.which == "import":
                CmdApp.import_data(base=args.base, _from=args.fileimport)
                return True
            elif args.which == "export":
                choice = CmdApp.parse_user_selection(args.select_contact)
                CmdApp.export(choice, args.to, base=args.base, zip=args.zip)
                return True
            elif args.which == "list":
                choice = None
                if args.select_contact is not None:
                    choice = CmdApp.parse_user_selection(args.select_contact)
                CmdApp.display(base=args.base, choice=choice)
                return True
            elif args.which == "convert":
                v = vars(args)
                if v['from'] != '' and v['to'] != '':
                    CmdApp.convert(_from=v['from'], _to=v['to'], zip=args.zip)
                    return True
            elif args.which == "contact":
                if args.add:
                    CmdApp.add(args.base)
                    return True
                elif args.edit is not None:
                    choice = CmdApp.parse_user_selection(args.edit)
                    CmdApp.edit(base=args.base, choice=choice)
                    return True
                elif args.delete is not None:
                    choice = CmdApp.parse_user_selection(args.delete)
                    CmdApp.delete(base=args.base, choice=choice)
                    return True
            elif args.which == "clear":
                CmdApp.clear_db(args.base)
                return True
        return False

    @staticmethod
    def print_formats():
        print("Available formats")
        from appData import io_formats
        for f in io_formats.get_formats():
            print(" - {}".format(f))
        exit(0)

    @staticmethod
    def print_fields():
        print("Available fields")
        from appData import field_types
        for f in field_types.get_fields():
            print(" - {}".format(f))
        exit(0)

    @staticmethod
    def search(base=DEFAULT_FILE_PATH, keyword=""):
        contacts = DataManipulation.find_coresponding_contacts(CmdApp.loadFile(base), keyword)
        if len(contacts) == 0:
            exit(CmdApp.NOT_FOUND_EXIT_CODE)

        for c in contacts:
            contact, cid = c
            print(str(cid) + " - ", end="")
            print(contact)

    @staticmethod
    def import_data(_from, base=DEFAULT_FILE_PATH):
        contacts = CmdApp.loadFile(base)
        contacts_to_add = CmdApp.loadFile(_from)
        CmdApp.save(contacts + contacts_to_add, base)

    @staticmethod
    def add(base=DEFAULT_FILE_PATH):
        contacts = CmdApp.loadFile(base)
        c = [Contact().wizard()]
        CmdApp.save(contacts + c, base)

    @staticmethod
    def parse_user_selection(select_contact):
        tmp = []
        try:
            for l in select_contact:
                index = int(l)
                tmp.append(index)
            return tmp
        except ValueError:
            return None

    @staticmethod
    def export(choice, to, base=DEFAULT_FILE_PATH, zip=False):
        contacts = CmdApp.loadFile(base)
        if choice is None:
            return CmdApp.save(contacts, to, zip)
        else:
            return CmdApp.save(DataManipulation.get_selected_from_index(contacts, choice), to, zip)

    @staticmethod
    def display(base, choice):
        contacts = CmdApp.loadFile(base)
        if choice is not None:
            contacts = DataManipulation.get_selected_from_index(contacts, choice)

        for c in contacts:
            print(c)
            print("-------------")

    @staticmethod
    def convert(_from, _to, zip=False):
        contacts = CmdApp.loadFile(_from)
        CmdApp.save(contacts, _to, zip)

    @staticmethod
    def delete(base, choice):
        contacts = CmdApp.loadFile(base)
        contacts_to_remove = DataManipulation.get_selected_from_index(contacts, choice)
        for c in contacts_to_remove:
            contacts.remove(c)
        CmdApp.save(contacts, base)

    @staticmethod
    def edit(base, choice):
        contacts = CmdApp.loadFile(base)
        print(choice)
        if 0 <= min(choice) <= max(choice) < len(contacts):
            for c in DataManipulation.get_selected_from_index(contacts, choice):
                c.wizard()
        CmdApp.save(contacts, base)

    @staticmethod
    def clear_db(base):
        f = open(base, "w+")
        f.write(';'.join(Contact().get_dic().keys()))
        f.close()
