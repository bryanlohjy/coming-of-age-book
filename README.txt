Photo Album Generator =======
I wanted to explore a sequence-based visual narrative through the pages of a book - the generated output is a photo album of a person's lifetime, from birth to death. The photos are stock photos which have been curated by hand, organised by stage of life and notable life events. A fairly rigid plot of life events is then generated and matched to the curated photos.

Steps to generate content ======
1. Run the setup script. This will create the necessary directories and start downloading images.
2. Once that is completed, run the gen_pdf.py python script. This will draw the data, export them into images and output it into a single pdf. 
3. The pdf will be available in temp/outputs/pdfs

Printing parameters ======
Size: A5, landscape
Binding: Saddlestich booklet