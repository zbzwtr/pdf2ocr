# pdf2ocr

### Purpose

* Simple pdf document to ocr pipeline.


### How to Use

* Just set the constant variables in env.py run the main script.

**env.py**
```python
# paths
PDFS = "./pdf_file" # folder for original pdfs that want text extraction
IMAGES = "./images" # folder for raster images
OCR_OUT = "./ocr" # ocr output from image
OCR_TRUTH = "./ocr_truth" # ground truth labels for ocr (opt)
# windows binaries: https://github.com/oschwartz10612/poppler-windows
# unix: https://poppler.freedesktop.org/
POPPLER_PATH = ""
# https://github.com/tesseract-ocr/tesseract
TESS_PATH = ""
TESSDATA_PATH = ""
# settings
IMG_EXT = ".jpg"
OCR_FONT = "" # path to font
OCR_COLOR = (255, 0, 0, 255) # RGBA
IMG_WIDTH = 1700
IMG_HEIGHT = int(1700 * 1.414)
```