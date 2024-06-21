from pdf_to_image import pdf_to_image
from pdf_to_image2 import pdf_to_image2
from ocr import ocr
import os
from pathlib import Path
from env import PDFS, IMAGES, IMG_EXT
from overlay_data import show_ocr

pdfs = [os.path.join(PDFS, fp) for fp in os.listdir(PDFS)]

# pdf to raster images
for pdf in pdfs:
    print(pdf)
    fn = Path(pdf).stem
    # pdf_to_image -> poppler
    # pdf_to_image2 -> pymupdf
    pdf_to_image2(pdf_path=pdf, save_name=fn)

imgs = [
    os.path.join(IMAGES, img)
    for img in os.listdir(IMAGES)
    if Path(img).suffix == IMG_EXT
]

# img to ocr
for img in imgs:
    print(img)
    fn = Path(img).stem
    ocr(img_path=img, save_name=fn)

show_ocr(
    f"./images/1.jpg",
    f"./ocr/1.tsv",
    w_scale=0.4,
    h_scale=0.4,
    show_boxes=False,
    side_by_side=True,
)
