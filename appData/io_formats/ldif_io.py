import base64
import os
from datetime import datetime

from ldif3 import LDIFWriter, LDIFParser

from appData import Contact


class LdifInputOutput:
    EXT = ".ldif"

    @staticmethod
    def export_data(contacts, file_path):

        if not file_path.endswith(LdifInputOutput.EXT):
            file_path += LdifInputOutput.EXT

        folder = os.path.dirname(file_path)
        if not os.path.exists(folder):
            os.makedirs(folder)
        f = open(file_path, 'w')
        f.close()
        f = open(file_path, 'ab')

        writer = LDIFWriter(f)
        for c in contacts:
            dn, entry = LdifInputOutput.build_string(c.get_dic())
            writer.unparse(dn, entry)

        return file_path

    @staticmethod
    def import_data(file_path):
        temp_contacts = []
        parser = LDIFParser(open(file_path, 'rb'))
        for dn, entry in parser.parse():
            temp_contacts.append(Contact.Contact.from_dic(LdifInputOutput.build_contact(entry)))
        return temp_contacts

    @staticmethod
    def build_string(dic):
        date = datetime.strptime(dic['Date de naissance'], '%d/%m/%Y')
        dn = 'cn={} {}'.format(dic['Prenom'], dic['Nom'])
        entry = {
            'objectclass': ['top', 'person', 'organizationalPerson', 'inetOrgPerson', 'mozillaAbPersonAlpha'],
            'gn': [dic['Prenom']],
            'sn': [dic['Nom']],
            'mail': [dic['Email']],
            'telephoneNumber': [dic['Telephone 1']],
            'mobile': [dic['Telephone 2']],
            'mozillaHomeStreet': [dic['Adresse 1']],
            'mozillaHomeStreet2': [dic['Adresse 2']],
            'mozillaHomeLocalityName': [dic['Ville']],
            'mozillaHomePostalCode': [dic['Code postal']],
            'mozillaHomeCountryName': [dic['Pays']],
            'birthyear': [str(date.year)],
            'birthmonth': [str(date.month)],
            'birthday': [str(date.day)],
            'jpegPhoto:': [dic['Photo']]
        }

        return dn, entry

    @staticmethod
    def build_contact(entry):
        temp_dico = {
            'Nom': entry['sn'][0],
            'Prenom': entry['gn'][0],
            'Date de naissance': "%s/%s/%s" % (entry['birthday'][0], entry['birthmonth'][0], entry['birthyear'][0]),
            'Email': entry['mail'][0],
            'Telephone 1': entry['mobile'][0],
            'Telephone 2': entry['telephoneNumber'][0],
            'Adresse 1': entry['mozillaHomeStreet'][0],
            'Adresse 2': entry['mozillaHomeStreet2'][0],
            'Code postal': entry['mozillaHomePostalCode'][0],
            'Ville': entry['mozillaHomeLocalityName'][0],
            'Pays': entry['mozillaHomeCountryName'][0],
            'Photo': base64.b64encode(entry['jpegPhoto'][0]).decode('UTF-8')
        }
        return temp_dico


instance = {"format": "ldif", "class": LdifInputOutput}
