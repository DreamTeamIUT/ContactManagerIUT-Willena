import csv
import os

from appData.Contact import Contact


class CsvInputOutput:
    EXT = ".csv"

    @staticmethod
    def export_data(contacts, file_path: str, header=True, pretty=False):

        if not file_path.endswith(CsvInputOutput.EXT):
            file_path += CsvInputOutput.EXT

        folder = os.path.dirname(file_path)
        if not os.path.exists(folder):
            os.makedirs(folder)
        #headers = contacts[0].get_dic().keys()
        headers = Contact().get_dic().keys()
        csvfile = open(file_path, "w")
        writer = csv.DictWriter(csvfile, fieldnames=headers, delimiter=";", lineterminator='\n')
        if header:
            writer.writeheader()

        for row in contacts:
            writer.writerow(row.get_dic())
        csvfile.close()
        return file_path

    @staticmethod
    def import_data(file_path):

        csvfile = open(file_path, "r")
        dialect = csv.Sniffer().sniff(csvfile.read())
        csvfile.seek(0)
        reader = csv.DictReader(csvfile, dialect=dialect)
        temp_contacts = []

        if sorted(reader.fieldnames) == sorted(Contact().get_dic().keys()):
            for row in reader:
                temp_contacts.append(Contact.from_dic(row))
        else:
            csvfile.seek(0)
            reader = csv.reader(csvfile, dialect=dialect)

            header = ['Nom',
                      'Prenom',
                      'Date de naissance',
                      'Email',
                      'Telephone 1',
                      'Telephone 2',
                      'Adresse 1',
                      'Adresse 2',
                      'Code postal',
                      'Ville',
                      'Pays',
                      'Photo']

            temp_dico = {}

            for r in reader:
                for v in r:
                    temp_dico[header.pop(0)] = v

            for h in header:
                temp_dico[h] = ""

            temp_contacts.append(Contact.from_dic(temp_dico))

        csvfile.close()
        return temp_contacts


instance = {"format": "csv", "class": CsvInputOutput}
