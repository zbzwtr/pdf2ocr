from pdf_to_image import pdf_to_image
from ocr import ocr
import os
from pathlib import Path
from env import PDFS, IMAGES, IMG_EXT

pdfs = [os.path.join(PDFS, fp) for fp in os.listdir(PDFS)] 

# pdf to raster images
for pdf in pdfs:
    print(pdf)
    fn = Path(pdf).stem
    pdf_to_image(pdf_path=pdf, save_name=fn)

imgs = [os.path.join(IMAGES, img) for img in os.listdir(IMAGES) if Path(img).suffix == IMG_EXT]

# img to ocr
for img in imgs:
    print(img)
    fn = Path(img).stem
    ocr(img_path=img, save_name=fn)