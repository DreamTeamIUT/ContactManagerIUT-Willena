import os


class DataManipulation:
    @staticmethod
    def find_coresponding_contacts(contacts: list, patern):
        list_corresponding = []
        for contact in contacts:
            if contact.is_in(patern):
                list_corresponding.append((contact, contacts.index(contact)))
                break
        return list_corresponding

    @staticmethod
    def get_selected_from_index(contacts, selection):
        return [contacts[i] for i in selection]

    @staticmethod
    def string_list_to_int(data):
        return [int(i) for i in data]

    @staticmethod
    def filter_file(files, filter):
        temp = []
        for f in files:
            if f.endswith(filter):
                temp.append(f)
        return temp

    @staticmethod
    def get_files(path):
        return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
