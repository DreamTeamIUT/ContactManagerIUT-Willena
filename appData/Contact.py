import copy

from appData.EasyMenu import EasyMenu

from appData import field_types
from appData.field_types.image_field import ImageField


class Contact:
    def __init__(self):
        self.available_headers = []

        self.available_headers.append(field_types.get_field("NameField")('N', "Nom"))
        self.available_headers.append(field_types.get_field("NameField")('P', "Prenom"))
        self.available_headers.append(field_types.get_field("PhoneField")('Tel1', "Telephone 1", canskip=True))
        self.available_headers.append(field_types.get_field("PhoneField")("Tel2", "Telephone 2", canskip=True))
        self.available_headers.append(field_types.get_field("EmailField")('E', "Email", canskip=True))
        self.available_headers.append(field_types.get_field("DateField")("DN", "Date de naissance", canskip=True))
        self.available_headers.append(field_types.get_field("BasicField")("A1", "Adresse 1", canskip=True))
        self.available_headers.append(field_types.get_field("BasicField")("A2", "Adresse 2", canskip=True))
        self.available_headers.append(field_types.get_field("BasicField")('L1', "Code postal", canskip=True))
        self.available_headers.append(field_types.get_field("NameField")("V1", "Ville", canskip=True))
        self.available_headers.append(field_types.get_field("NameField")("C1", "Pays", canskip=True))
        self.available_headers.append(field_types.get_field("ImageField")("Im", "Photo", canskip=True))

    def wizard(self):
        for h in self.available_headers:
            h.ask_value()
        #self.add_field()
        return self

    def get_string(self):
        string_to_return = ""
        for h in self.available_headers:
            string_to_return += "\n\t[%s]: %s" % (h.get_name(), h.get_value())
        return string_to_return

    def get_dic(self):
        dictio = {}
        for h in self.available_headers:
            dictio[h.get_name()] = h.value
        return dictio

    def add_field(self):
        c = input("Voulez vous ajouter de nouveaux champs ? (Ces champs peuvent ne pas être présent dans" +
                  " certain format  d'exportation)(O/N) : ")
        if c.lower().startswith("o"):
            menu = EasyMenu("Voici les types de champs")
            menu.set_prompt("Votre choix : ")
            menu.set_multiple(True)

            for types in field_types.get_fields():
                menu.add_entry(
                        "{} - {}".format(field_types.get_field(types).NAME, field_types.get_field(types).DESCRIPTION),
                        None)
            menu.show_menu()
            ch = menu.wait_for_choise()
            value = input("Entrez le nom du champs")
            header = field_types.get_field_by_index(ch[0])(value)
            header.ask_value()
            self.available_headers.append(header)
            return self.add_field()
        return

    @staticmethod
    def from_dic(dic):
        c = Contact()
        for f in c.available_headers:
            f.set_value(dic[f.name])
        return c

    def is_in(self, patern: str):
        for h in self.available_headers:
            if type(h) is not ImageField:
                if patern.lower() in h.get_value().lower():
                    return True

    @staticmethod
    def update_all(contacts):
        tmp_names = {}
        for c in contacts:
            for h in c.available_headers:
                if h.get_WName() not in tmp_names.keys():
                    tmp_names[h.get_WName()] = h

        for c in contacts:
            for ids in tmp_names.keys():
                if c.get_header_by_id(ids) is None:
                    print("In ! ")
                    nwh = copy.deepcopy(tmp_names[ids])
                    nwh.value = ""
                    c.available_headers.append(nwh)
        print(contacts)
        return contacts

    @staticmethod
    def get_header_names(contact):
        tmp_names = []
        for h in contact.available_headers:
            if h.get_name() not in tmp_names:
                tmp_names.append(h.get_name())
        return tmp_names

    @staticmethod
    def get_header_ids(contact):
        tmp_names = []
        for h in contact.available_headers:
            if h.get_WName() not in tmp_names:
                tmp_names.append(h.get_WName())
        return tmp_names

    @staticmethod
    def diff(first, second):
        second = set(second)
        return [item for item in first if item not in second]

    def get_header_by_id(self, id):
        for h in self.available_headers:
            if h.get_WName() == id:
                return h
        return None

    def important_headers(self, *args):
        headers = []

        for h in self.available_headers:
            if not h.can_skip:
                headers.append(h)

        for a in args:
            headers.append(self.get_header_by_id(a))

        return headers

    def __repr__(self):
        return self.get_string()
