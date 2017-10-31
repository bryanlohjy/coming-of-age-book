import narrative
from drawing import draw_book
import time
import datetime
import os
from fpdf import FPDF
from PIL import Image

plot = narrative.Story(28)
# Create pages from plot
book = draw_book(plot)

# draw pages into a new directory
timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H%M%S%f')
image_dir = 'temp/outputs/images/{}/'.format(timestamp)
if not os.path.exists(image_dir):
    os.makedirs(image_dir)

# Create images from pages
print('Exporting pages...')
for i in range(len(book)):
    print('Page {:02d} exported'.format(i))
    page = book[i]
    page.draw(output_directory='{}{:02d}.png'.format(image_dir, i))

# Generating PDF
#A Adapted from https://stackoverflow.com/questions/27327513/create-pdf-from-a-list-of-images
def makePdf(pdfFileName, listPages, dir = '', pdfpath=''):
    print('Creating pdf...')
    cover = Image.open(dir + str(listPages[0]))
    width, height = cover.size

    pdf = FPDF(unit = "pt", format = [width, height])

    for page in listPages:
        pdf.add_page()
        pdf.image(dir + str(page), 0, 0)
    pdf.output(pdfpath + ".pdf", "F")
    print('Done!')
    
image_paths = os.listdir(image_dir)
pdf_output_path = 'temp/outputs/pdfs/{}'.format(timestamp)
makePdf(timestamp, image_paths, dir=image_dir, pdfpath=pdf_output_path)