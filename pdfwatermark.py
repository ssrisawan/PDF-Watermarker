from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import Color
from PyPDF4 import PdfFileReader, PdfFileWriter, PdfFileMerger
from progress.bar import Bar
import os
import sys
import warnings
warnings.filterwarnings("ignore")

def watermark_page(filename, size, text):
    # Creating a canvas with the file name and size (A4 or letter) specified.
    canvas = Canvas(filename, pagesize=size)

    x = size[0]/2
    y = size[1]/4

    for i in range(1,4):
        canvas.saveState()
        canvas.translate(round(x),round(y * i))
        canvas.rotate(20)
        canvas.setFillColor(Color(0,0,0, alpha=0.10))
        canvas.drawCentredString(0,0 , text)
        canvas.restoreState()

    canvas.save()

def watermark(input_filename, output_filename, watermark_filename):
    input_file = open(input_filename, "rb")
    input_pdf = PdfFileReader(input_file)
    input_num_page = input_pdf.getNumPages()
    watermark_file = open(watermark_filename, "rb")
    watermark_pdf = PdfFileReader(watermark_file)
    watermark = watermark_pdf.getPage(0)
    output = PdfFileWriter()

    bar = Bar("Writing " + output_filename + "...", max = input_num_page, suffix="%(percent).1f%%")

    for i in range(input_num_page):
        pdf_page = input_pdf.getPage(i)
        pdf_page.mergePage(watermark)
        pdf_page.compressContentStreams()
        output.addPage(pdf_page)
        bar.next()
    
    output_file = open(output_filename, "wb")
    output.write(output_file)
    input_file.close()
    watermark_file.close()
    output_file.close()

n = len(sys.argv)
tempfile = "temp_watermark.pdf"
if n != 3:
    print("Usage: python " + sys.argv[0] + " 'Source File' 'Name or Email Address to Register'")
else:
    watermark_page(tempfile, A4, "This PDF file is registered to " + sys.argv[2])
    watermark(sys.argv[1], sys.argv[2] + ".pdf", tempfile)
    os.remove(tempfile)