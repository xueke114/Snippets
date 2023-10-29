from PyPDF2 import PdfWriter, PdfReader
output_pdf = PdfWriter()

with open(r'2023-03.pdf', 'rb') as readfile:
    input_pdf = PdfReader(readfile)
    total_pages = len(input_pdf.pages)
    for page in range(total_pages - 1, -1, -1):
        output_pdf.add_page(input_pdf.pages[page])
    with open(r'2023-03-output.pdf', "wb") as writefile:
        output_pdf.write(writefile)