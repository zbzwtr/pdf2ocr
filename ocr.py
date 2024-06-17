import pytesseract
import os
from PIL import Image
import pandas as pd
from env import OCR_OUT, TESS_PATH, TESSDATA_PATH

# TODO: OCR Evaluation Metrics (character error rate, word error rate)
# TODO: Label text for a single pdf (ground truth)
# TODO: traineddata files vs finetuning?

os.environ["TESSDATA_PREFIX"] = (
    TESS_PATH
)
TESS_PATH = TESSDATA_PATH
pytesseract.pytesseract.tesseract_cmd = TESS_PATH


def ocr(img_path, save_dir=OCR_OUT, save_name="1"):
    """
      --psm NUM             Specify page segmentation mode.
      --oem NUM             Specify OCR Engine mode.
    NOTE: These options must occur before any configfile.

    Page segmentation modes:
      0    Orientation and script detection (OSD) only.
      1    Automatic page segmentation with OSD.
      2    Automatic page segmentation, but no OSD, or OCR. (not implemented)
      3    Fully automatic page segmentation, but no OSD. (Default)
      4    Assume a single column of text of variable sizes.
      5    Assume a single uniform block of vertically aligned text.
      6    Assume a single uniform block of text.
      7    Treat the image as a single text line.
      8    Treat the image as a single word.
      9    Treat the image as a single word in a circle.
    10    Treat the image as a single character.
    11    Sparse text. Find as much text as possible in no particular order.
    12    Sparse text with OSD.
    13    Raw line. Treat the image as a single text line,
          bypassing hacks that are Tesseract-specific.

    OCR Engine modes:
      0    Legacy engine only.
      1    Neural nets LSTM engine only.
      2    Legacy + LSTM engines.
      3    Default, based on what is available.
    """
    img = Image.open(img_path)

    # psm 11 may be useful
    custom_oem_psm_config = r"--oem 1 --psm 3 -l eng"
    data = pytesseract.image_to_data(img, config=custom_oem_psm_config)
    with open(f"{save_dir}/{save_name}.tsv", "w") as f:
        f.write(data)

    # we prefer csv
    df = pd.read_csv(
        f"{save_dir}/{save_name}.tsv", sep="\t", header=0, encoding="unicode_escape"
    )
    df.to_csv(f"{save_dir}/{save_name}.csv")

if __name__ == "__main__":
    ocr("./data/1.jpg")