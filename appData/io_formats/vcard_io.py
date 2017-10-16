import base64
import os
from datetime import datetime

import vobject

from appData import Contact


class VcardInputOutput:
    EXT = ".vcf"

    @staticmethod
    def export_data(contacts, file_path):

        if not file_path.endswith(VcardInputOutput.EXT):
            file_path += VcardInputOutput.EXT

        folder = os.path.dirname(file_path)
        if not os.path.exists(folder):
            os.makedirs(folder)

        if len(contacts) == 1:
            dic = contacts[0].get_dic()
            with open(file_path, 'w') as f:
                f.write(VcardInputOutput.replace_elems(dic))
            return file_path


        print("\n En vcard il n'est pas possible de mettre plusieur contact dans un fichier.")
        print("Plusieurs fichiers seront ajouté dans le dossier : " + os.path.abspath(folder))
        print("Chaque fichier de contact sera identifié par son Nom/Prenom")
        files = []

        for c in contacts:
            dic = c.get_dic()
            file_name = '/' + dic['Nom'] + "_" + dic['Prenom'] + '.vcf'
            files.append(folder+file_name)
            with open(folder + file_name, 'w') as f:
                f.write(VcardInputOutput.replace_elems(dic))

        return files

    @staticmethod
    def import_data(file_path):
        temp_dic = {}
        with open(file_path, 'r') as file:
            o = vobject.readOne(str(file.read()))
            #print(o.contents)
            for c in o.contents:
                for element in o.contents[c]:
                    if element.name == "N":
                        temp_dic['Nom'] = element.value.family
                        temp_dic['Prenom'] = element.value.given
                    if element.name == "BDAY":
                        temp_dic['Date de naissance'] = element.value
                    if element.name == 'ADR':
                        temp_dic['Adresse 1'] = element.value.street
                        temp_dic['Adresse 2'] = element.value.extended
                        temp_dic['Ville'] = element.value.city
                        temp_dic['Code postal'] = element.value.code
                        temp_dic['Pays'] = element.value.country
                    if element.name == 'EMAIL':
                        temp_dic['Email'] = element.value
                    if element.name == 'TEL':
                        if 'Telephone 1' in temp_dic.keys():
                            temp_dic['Telephone 2'] = element.value
                        else:
                            temp_dic['Telephone 1'] = element.value
                    if element.name == "PHOTO":
                        temp_dic['Photo'] = base64.b64encode(element.value).decode('UTF-8')
            return [Contact.Contact.from_dic(temp_dic)]

    @staticmethod
    def replace_elems(dic):
        vcard = vobject.vCard()

        o = vcard.add('N')
        o.value = vobject.vcard.Name(family=dic['Nom'], given=dic['Prenom'])

        o = vcard.add('FN')
        o.value = dic['Prenom'] + " " + dic['Nom']

        o = vcard.add('email')
        o.value = dic['Email']
        o.type_param = "INTERNET"

        o = vcard.add("adr")
        o.value = vobject.vcard.Address(street=dic['Adresse 1'], extended=dic['Adresse 2'], city=dic['Ville'], code=dic['Code postal'],
                                        country=dic['Pays'])

        o = vcard.add('tel')
        o.type_param = "HOME"
        o.value = dic['Telephone 1']

        o = vcard.add('tel')
        o.type_param = "WORK"
        o.value = dic['Telephone 2']

        o = vcard.add('photo')
        o.type_param = "JPEG"
        o.encoding_param = "BASE64"
        o.value = dic['Photo']

        o = vcard.add('BDAY')
        o.value = dic['Date de naissance']

        o = vcard.add('rev')
        o.value = datetime.now().isoformat()

        return vcard.serialize()


instance = {"format": "vcard", "class": VcardInputOutput}
