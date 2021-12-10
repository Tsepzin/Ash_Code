import PyPDF2, os

month = input('Enter the month number:')
year = input('Enter the year number:')

# Get all the PDF filenames.
pdfFiles = []
for filename in os.listdir(os.path.join(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Fund Reports\Fund Management FI\Governance',year + '-' + month)):
	if filename.endswith('.pdf'):
		pdfFiles.append(filename)
pdfFiles.sort(key=str.lower)
pdfWriter = PyPDF2.PdfFileWriter()

for filename in pdfFiles:
	pdfFileObj = open(os.path.join(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Fund Reports\Fund Management FI\Governance',year + '-' + month,filename), 'rb')
	pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

	for pageNum in range(pdfReader.numPages):
		pageObj = pdfReader.getPage(pageNum)
		pdfWriter.addPage(pageObj)
		
# Save the resulting PDF to a file.
pdfOutput = open(os.path.join(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Fund Reports\Fund Management FI\Governance',year + '-' + month,'FI Governance Pack.pdf_' + year + '-' + month + '.pdf'), 'wb')
pdfWriter.write(pdfOutput)
pdfOutput.close()


# # Add page number
# from PyPDF2 import PdfFileWriter, PdfFileReader
# import io
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import A4

# pdf = PdfFileReader(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Fund Reports\Fund Management FI\Governance',year + '-' + month,'FI Governance Pack_prelim.pdf_' + year + '-' + month + '.pdf')
# pdf_writer = PdfFileWriter()

# for page in range(pdf.getNumPages()):
    
    # packet = io.BytesIO()

    # can = canvas.Canvas(packet, pagesize=A4)


    # can.drawString(10, 200, "Page " + str(page) )
    # can.save()
    # packet.seek(0)
    # watermark = PdfFileReader(packet)
    # watermark_page = watermark.getPage(0)



    # pdf_page = pdf.getPage(page)
    # pdf_page.mergePage(watermark_page)
    # pdf_writer.addPage(pdf_page)

# with open(r'\\rmb-vpr-file02\Ashburton\Support Services\Risk Management\Investment Analytics\Fund Reports\Fund Management FI\Governance',year + '-' + month,'FI Governance Pack_3.pdf_' + year + '-' + month + '.pdf', 'wb') as fh:
    # pdf_writer.write(fh)