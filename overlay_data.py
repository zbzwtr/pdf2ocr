import cv2
import pandas as pd
import os
from pathlib import Path
from PIL import ImageFont, ImageDraw, Image
import numpy as np
from env import OCR_FONT, OCR_COLOR


def _create_blank_BGR_image(h: int, w: int):
    # output shape: (h, w, c)
    return np.full(shape=(h, w, 3), fill_value=255, dtype=np.uint8)


def _show_window(img: np.ndarray):
    # original img
    winname = "img"
    cv2.namedWindow(winname)
    cv2.moveWindow(winname, 40, 40)
    cv2.imshow(winname, img)
    # ocr'd image
    cv2.waitKey(0)


# by passing data struc
def _overlay_data(img, d, w_scale=1, h_scale=1, show_boxes=True):
    """
    img: cv2 img
    d: pytess dict output
    """
    img = cv2.resize(img, (0, 0), fx=w_scale, fy=h_scale)
    n_boxes = len(d["level"])
    # draw text.
    # opencv only uses a small subset of ascii encoding, which can lead to large amount of question marks
    # overcome problem by using PIL to draw the text.
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(img)
    draw = ImageDraw.Draw(pil_image)
    font = ImageFont.truetype(OCR_FONT, 12)

    for i in range(n_boxes):
        (x, y) = (d["left"][i], d["top"][i])
        x = int(x * w_scale)
        y = int(y * h_scale)
        if int(d["word_num"][i]) > 0:
            text = str(d["text"][i])
            font_scale = min(w_scale, h_scale)
            font_scale = int(font_scale) if font_scale >= 1 else 1
            draw.text((x, y - 16), text, font=font, font_size=8, fill=OCR_COLOR)

    img = np.asarray(pil_image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    if show_boxes:
        for i in range(n_boxes):
            (x, y, w, h) = (d["left"][i], d["top"][i], d["width"][i], d["height"][i])
            x, w = int(x * w_scale), int(w * w_scale)
            y, h = int(y * h_scale), int(h * h_scale)
            linewidth = int(2 * min(w_scale, h_scale))
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), linewidth)

    winname = "img"
    cv2.namedWindow(winname)
    cv2.moveWindow(winname, 40, 40)
    cv2.imshow(winname, img)
    cv2.waitKey(0)


def _side_by_side(orig_img, d, w_scale=1, h_scale=1, show_boxes=True):
    """
    img: cv2 img
    d: pytess dict output
    """
    # TODO: safety check for shapes on ocr_img and orig_img
    org_h, org_w, channels = orig_img.shape
    h, w = int(org_h * h_scale), int(org_w * w_scale)
    ocr_img = _create_blank_BGR_image(h, w)
    orig_img = cv2.resize(orig_img, (0, 0), fx=w_scale, fy=h_scale)
    print(ocr_img.shape)
    print(orig_img.shape)
    n_boxes = len(d["level"])
    # draw text.
    # opencv only uses a small subset of ascii encoding, which can lead to large amount of question marks
    # overcome problem by using PIL to draw the text.
    ocr_img = cv2.cvtColor(ocr_img, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(ocr_img)
    draw = ImageDraw.Draw(pil_image)
    font = ImageFont.truetype(OCR_FONT, 12)

    for i in range(n_boxes):
        (x, y) = (d["left"][i], d["top"][i])
        x = int(x * w_scale)
        y = int(y * h_scale)
        if int(d["word_num"][i]) > 0:
            text = str(d["text"][i])
            font_scale = min(w_scale, h_scale)
            font_scale = int(font_scale) if font_scale >= 1 else 1
            draw.text((x, y - 16), text, font=font, font_size=7, fill=OCR_COLOR)

    ocr_img = np.asarray(pil_image)
    ocr_img = cv2.cvtColor(ocr_img, cv2.COLOR_RGB2BGR)

    if show_boxes:
        for i in range(n_boxes):
            (x, y, w, h) = (d["left"][i], d["top"][i], d["width"][i], d["height"][i])
            x, w = int(x * w_scale), int(w * w_scale)
            y, h = int(y * h_scale), int(h * h_scale)
            linewidth = int(2 * min(w_scale, h_scale))
            cv2.rectangle(ocr_img, (x, y), (x + w, y + h), (0, 255, 0), linewidth)

    img = np.concatenate((orig_img, ocr_img), axis=1)
    _show_window(img)


def show_ocr(
    img_path, bboxes_path, w_scale=1, h_scale=1, show_boxes=True, side_by_side=False
):
    # original img
    img = cv2.imread(img_path)

    # read tess output
    df = pd.read_csv(bboxes_path, header=0, encoding="utf-8", sep="\t")
    print(df.iloc[138])
    # return
    d = df.to_dict()
    if side_by_side:
        _side_by_side(img, d, w_scale, h_scale, show_boxes)
    else:
        _overlay_data(img, d, w_scale, h_scale, show_boxes)


if __name__ == "__main__":
    files = [Path(f).stem for f in os.listdir("./images")]
    for file in files:
        # ocr
        show_ocr(
            f"./images/{file}.jpg",
            f"./ocr/{file}.tsv",
            w_scale=0.4,
            h_scale=0.4,
            show_boxes=False,
            side_by_side=True,
        )
        # break
        # # ocr ground truth
        # overlay_data(f"./images/{file}.jpg", f"./ocr_truth/{file}.csv", w_scale=0.4, h_scale=0.4, show_boxes=False)
