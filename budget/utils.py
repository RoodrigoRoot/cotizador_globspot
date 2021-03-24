from .models import Prices
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
import PyPDF2 
from django.conf import settings


def get_quantity(quantity):
    price = 0
    total = 0
    
    if quantity <= 5:
        price = Prices.objects.get(value=1).price
        total = quantity * price

    elif quantity > 5 and quantity <= 10:
        price = Prices.objects.get(value=2).price
        total = quantity * price

    elif quantity > 11 and quantity <= 30:
        price = Prices.objects.get(value=3).price
        total = quantity * price

    elif quantity > 30:
        price = Prices.objects.get(value=4).price
        total = quantity * price

    return price, total


class PDFHelper:

    @classmethod
    def create_pdf_budget(cls, budget):
        

        def first_page(budget):
            packet = io.BytesIO()
            # create a new PDF with Reportlab
            can = canvas.Canvas(packet, pagesize=letter)
            can.setFillColor(HexColor("#000"))
            can.setFont('Helvetica-Bold', 16)
            len_company = len(str(budget.company).split())
            if len_company >= 2:
                can.drawString(555, 140, "{}".format(budget.company))
            else:
                can.drawString(590, 140, "{}".format(budget.company))

            can.setFont('Helvetica-Bold', 12)
            can.drawString(585, 110, "{}".format(budget.company_contact))
            can.setFont('Helvetica-Bold', 12)
            can.drawString(600, 80, "Asesor:")
            can.drawString(580, 60, "{} {}".format(budget.creator.user.first_name, 
            budget.creator.user.last_name
            ))
            can.setFont('Helvetica-Bold', 10)
            months = {1:"Enero", 2: "Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo"
            , 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre",
            11:"Noviembre", 12:"Diciembre"
            }
            
            can.drawString(590, 30, "{} {}".format(months[budget.created_at.month], 
            budget.created_at.year
            ))
            can.save()

                #move to the beginning of the StringIO buffer
            packet.seek(0)
            new_pdf = PdfFileReader(packet)
            # read your existing PDF
            existing_pdf = PdfFileReader(open(str(settings.BASE_DIR)+"/budget/portada.pdf", "rb"))
            output = PdfFileWriter()
            # add the "watermark" (which is the new pdf) on the existing page
            page = existing_pdf.getPage(0)
            page.mergePage(new_pdf.getPage(0))
            output.addPage(page)
            # finally, write "output" to a real file
            outputStream = open(str(settings.BASE_DIR)+"/budget/portada_.pdf", "wb")
            output.write(outputStream)
            outputStream.close()

        
        def merge_first_pdf(budget):            
        
            # Open the files that have to be merged one by one
            pdf2File = open(str(settings.BASE_DIR)+"/budget/template.pdf", 'rb')
            pdf1File = open(str(settings.BASE_DIR)+"/budget/portada_.pdf", 'rb')
            
            # Read the files that you have opened
            pdf1Reader = PyPDF2.PdfFileReader(pdf1File)
            pdf2Reader = PyPDF2.PdfFileReader(pdf2File)
            
            # Create a new PdfFileWriter object which represents a blank PDF document
            pdfWriter = PyPDF2.PdfFileWriter()
            
            # Loop through all the pagenumbers for the first document
            for pageNum in range(pdf1Reader.numPages):
                pageObj = pdf1Reader.getPage(pageNum)
                pdfWriter.addPage(pageObj)
            
            # Loop through all the pagenumbers for the second document
            for pageNum in range(pdf2Reader.numPages):
                pageObj = pdf2Reader.getPage(pageNum)
                pdfWriter.addPage(pageObj)
            
            # Now that you have copied all the pages in both the documents, write them into the a new document
            pdfOutputFile = open(str(settings.BASE_DIR)+"/budget/template_.pdf", 'wb')
            pdfWriter.write(pdfOutputFile)
            
            # Close all the files - Created as well as opened
            pdfOutputFile.close()
            pdf1File.close()
            pdf2File.close()
        

        def costs(budget):

            packet = io.BytesIO()
            # create a new PDF with Reportlab
            can = canvas.Canvas(packet, pagesize=letter)
            can.setFont('Helvetica-Bold', 10)
            can.setFillColor(colors.white)
            can.drawString(400, 130, "Cantidad de dispositvos: {}".format(budget.quantity))
            can.drawString(400, 120, "Precio unitario: ${:,}".format(budget.unit_cost))
            can.setFont('Helvetica-Bold', 12)
            can.setFillColor(colors.black)
            total = round(budget.total * 1.16, 2)
            can.drawString(395, 88, "Total: ${:,} MXN (IVA Incluido)".format(total))

            can.save()

            #move to the beginning of the StringIO buffer
            packet.seek(0)
            new_pdf = PdfFileReader(packet)
            # read your existing PDF
            existing_pdf = ""
            existing_pdf = PdfFileReader(open(str(settings.BASE_DIR)+"/budget/costo.pdf", "rb"))

            if budget.foreing:
                existing_pdf = PdfFileReader(open(str(settings.BASE_DIR)+"/budget/costo_foraneo.pdf", "rb"))
                
            output = PdfFileWriter()
            # add the "watermark" (which is the new pdf) on the existing page
            page = existing_pdf.getPage(0)
            page.mergePage(new_pdf.getPage(0))
            output.addPage(page)
            # finally, write "output" to a real file
            outputStream = open(str(settings.BASE_DIR)+"/budget/costo_.pdf", "wb")
            output.write(outputStream)
            outputStream.close()


        def sincerely(budget):
            packet = io.BytesIO()
            # create a new PDF with Reportlab
            can = canvas.Canvas(packet, pagesize=letter)
            can.setFillColor(HexColor("#40ABE6"))
            can.setFont('Helvetica-Bold', 18)
            can.drawString(290, 250, "{} {}".format(budget.creator.user.first_name, 
            budget.creator.user.last_name
            ))
            can.drawString(278, 215, budget.creator.charge)
            can.save()

                #move to the beginning of the StringIO buffer
            packet.seek(0)
            new_pdf = PdfFileReader(packet)
            # read your existing PDF
            existing_pdf = PdfFileReader(open(str(settings.BASE_DIR)+"/budget/atte.pdf", "rb"))
            output = PdfFileWriter()
            # add the "watermark" (which is the new pdf) on the existing page
            page = existing_pdf.getPage(0)
            page.mergePage(new_pdf.getPage(0))
            output.addPage(page)
            # finally, write "output" to a real file
            outputStream = open(str(settings.BASE_DIR)+"/budget/atte_.pdf", "wb")
            output.write(outputStream)
            outputStream.close()

        def add_credit_card():
            # Open the files that have to be merged one by one
            pdf2File = open(str(settings.BASE_DIR)+"/budget/tarjeta.pdf", 'rb')
            pdf1File = open(str(settings.BASE_DIR)+"/budget/template_1.pdf", 'rb')
            
            # Read the files that you have opened
            pdf1Reader = PyPDF2.PdfFileReader(pdf1File)
            pdf2Reader = PyPDF2.PdfFileReader(pdf2File)
            
            # Create a new PdfFileWriter object which represents a blank PDF document
            pdfWriter = PyPDF2.PdfFileWriter()
            
            # Loop through all the pagenumbers for the first document
            for pageNum in range(pdf1Reader.numPages):
                pageObj = pdf1Reader.getPage(pageNum)
                pdfWriter.addPage(pageObj)
            
            # Loop through all the pagenumbers for the second document
            for pageNum in range(pdf2Reader.numPages):
                pageObj = pdf2Reader.getPage(pageNum)
                pdfWriter.addPage(pageObj)
            
            # Now that you have copied all the pages in both the documents, write them into the a new document
            pdfOutputFile = open(str(settings.BASE_DIR)+"/budget/template_1_1.pdf", 'wb')
            pdfWriter.write(pdfOutputFile)
            

            # Close all the files - Created as well as opened
            pdfOutputFile.close()
            pdf1File.close()
            pdf2File.close()



        def merge_template(budget):
            
        
            # Open the files that have to be merged one by one
            pdf2File = open(str(settings.BASE_DIR)+"/budget/costo_.pdf", 'rb')
            pdf1File = open(str(settings.BASE_DIR)+"/budget/template_.pdf", 'rb')
            
            # Read the files that you have opened
            pdf1Reader = PyPDF2.PdfFileReader(pdf1File)
            pdf2Reader = PyPDF2.PdfFileReader(pdf2File)
            
            # Create a new PdfFileWriter object which represents a blank PDF document
            pdfWriter = PyPDF2.PdfFileWriter()
            
            # Loop through all the pagenumbers for the first document
            for pageNum in range(pdf1Reader.numPages):
                pageObj = pdf1Reader.getPage(pageNum)
                pdfWriter.addPage(pageObj)
            
            # Loop through all the pagenumbers for the second document
            for pageNum in range(pdf2Reader.numPages):
                pageObj = pdf2Reader.getPage(pageNum)
                pdfWriter.addPage(pageObj)
            
            # Now that you have copied all the pages in both the documents, write them into the a new document
            pdfOutputFile = open(str(settings.BASE_DIR)+"/budget/template_1.pdf", 'wb')
            pdfWriter.write(pdfOutputFile)
            
            # Close all the files - Created as well as opened
            pdfOutputFile.close()
            pdf1File.close()
            pdf2File.close()



        def merge_penultimate_pdf(budget):
        
            # Open the files that have to be merged one by one
            pdf2File = open(str(settings.BASE_DIR)+"/budget/condiciones.pdf", 'rb')
            pdf1File = open(str(settings.BASE_DIR)+"/budget/template_1_1.pdf", 'rb')
            
            # Read the files that you have opened
            pdf1Reader = PyPDF2.PdfFileReader(pdf1File)
            pdf2Reader = PyPDF2.PdfFileReader(pdf2File)
            
            # Create a new PdfFileWriter object which represents a blank PDF document
            pdfWriter = PyPDF2.PdfFileWriter()
            
            # Loop through all the pagenumbers for the first document
            for pageNum in range(pdf1Reader.numPages):
                pageObj = pdf1Reader.getPage(pageNum)
                pdfWriter.addPage(pageObj)
            
            # Loop through all the pagenumbers for the second document
            for pageNum in range(pdf2Reader.numPages):
                pageObj = pdf2Reader.getPage(pageNum)
                pdfWriter.addPage(pageObj)
            
            # Now that you have copied all the pages in both the documents, write them into the a new document
            pdfOutputFile = open(str(settings.BASE_DIR)+"/budget/Cotizacion.pdf", 'wb')
            pdfWriter.write(pdfOutputFile)
            
            # Close all the files - Created as well as opened
            pdfOutputFile.close()
            pdf1File.close()
            pdf2File.close()


        def merge_last_pdf(budget):
            
            # Open the files that have to be merged one by one
            pdf2File = open(str(settings.BASE_DIR)+"/budget/atte_.pdf", 'rb')
            pdf1File = open(str(settings.BASE_DIR)+"/budget/Cotizacion.pdf", 'rb')
            
            # Read the files that you have opened
            pdf1Reader = PyPDF2.PdfFileReader(pdf1File)
            pdf2Reader = PyPDF2.PdfFileReader(pdf2File)
            
            # Create a new PdfFileWriter object which represents a blank PDF document
            pdfWriter = PyPDF2.PdfFileWriter()
            
            # Loop through all the pagenumbers for the first document
            for pageNum in range(pdf1Reader.numPages):
                pageObj = pdf1Reader.getPage(pageNum)
                pdfWriter.addPage(pageObj)
            
            # Loop through all the pagenumbers for the second document
            for pageNum in range(pdf2Reader.numPages):
                pageObj = pdf2Reader.getPage(pageNum)
                pdfWriter.addPage(pageObj)
            
            # Now that you have copied all the pages in both the documents, write them into the a new document
            pdfOutputFile = open(str(settings.BASE_DIR)+"/budget/Cotizacion_.pdf", 'wb')
            pdfWriter.write(pdfOutputFile)
            
            # Close all the files - Created as well as opened
            pdfOutputFile.close()
            pdf1File.close()
            pdf2File.close()

      
        first_page(budget)
        merge_first_pdf(budget)
        costs(budget)
        merge_template(budget)
        sincerely(budget)
        add_credit_card()
        merge_penultimate_pdf(budget)
        merge_last_pdf(budget)

def delete_files(budget):
    import os
    os.remove(str(settings.BASE_DIR)+"/budget/template_1.pdf")
    os.remove(str(settings.BASE_DIR)+"/budget/template_.pdf")
    os.remove(str(settings.BASE_DIR)+"/budget/costo_.pdf")
    os.remove(str(settings.BASE_DIR)+"/budget/portada_.pdf")
    os.remove(str(settings.BASE_DIR)+"/budget/atte_.pdf")
    os.remove(str(settings.BASE_DIR)+"/budget/Cotizacion.pdf")
    os.remove(str(settings.BASE_DIR)+"/budget/template_1_1.pdf")
    os.remove(str(settings.BASE_DIR)+"/budget/Cotizacion_.pdf")
        


