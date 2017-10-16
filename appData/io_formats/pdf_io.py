import base64
from io import BytesIO

import io
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas as can
from reportlab.lib import utils


class PdfInputOutput:
    EXT = ".pdf"

    class PdfWritter:
        STEP = 20

        def __init__(self, out_file):
            self.canvas = can.Canvas(out_file, pagesize=letter)
            self.canvas.setLineWidth(.3)
            self.posY = 750
            self.start = 750

        def add_string(self, x=30, value=""):
            self.posY -= self.STEP
            self.canvas.drawString(x, self.posY, value)

        def add_line(self, x1=10, x2=600):
            self.posY -= (2 * self.STEP)
            self.canvas.line(x1, self.posY, x2, self.posY)

        def add_image(self, x, base64data=None, url=None):
            img_file = None

            if base64data is not None:
                img_file = ImageReader(io.BytesIO(base64.b64decode(base64data)))
            elif url is not None:
                img_file = ImageReader(url)
            if img_file is not None:
                self.canvas.drawImage(img_file, x, self.start - self.STEP * 5, width=100, height=100, mask='auto')

        def add_break(self):
            self.start = self.posY - self.STEP * 2

        def save(self):
            self.canvas.save()

    @staticmethod
    def export_data(contacts, file_path):
        if not file_path.endswith(PdfInputOutput.EXT):
            file_path += PdfInputOutput.EXT

        pdf = PdfInputOutput.PdfWritter(file_path)

        for c in contacts:
            dic = c.get_dic()
            pdf.add_string(
                    value="Nom : {}          prenom: {}           Date de naissance: {}".format(dic['Nom'],
                                                                                                dic['Prenom'],
                                                                                                dic[
                                                                                                    'Date de naissance']))
            pdf.add_string(value="Addresse 1 : {}".format(dic["Adresse 1"]))
            pdf.add_string(value="Addresse 2 : {}".format(dic["Adresse 2"]))
            pdf.add_string(value="Code postal: {}         Ville: {}".format(dic['Code postal'], dic['Ville']))
            pdf.add_string(value="Pays: {}".format(dic['Pays']))
            pdf.add_string(
                    value="Telephone 1: {}          Telephone 2: {}".format(dic['Telephone 1'], dic['Telephone 2']))
            pdf.add_string(value="Email: {}".format(dic['Email']))
            if dic['Photo'] != "":
                pdf.add_image(500, base64data=dic['Photo'])

            pdf.add_line()

        pdf.save()
        return file_path

    @staticmethod
    def import_data(file_path):
        print("Il n'est pas possible d'importer un pdf !")
        return


instance = {"format": "pdf", "class": PdfInputOutput}
