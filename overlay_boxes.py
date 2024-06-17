import cv2
import pandas as pd


# by passing data struc
def _overlay_data(img, d, w_scale=1, h_scale=1):
    """
    img: cv2 img
    d: pytess dict output
    """
    img = cv2.resize(img, (0, 0), fx=w_scale, fy=h_scale)
    n_boxes = len(d["level"])
    for i in range(n_boxes):
        (x, y, w, h) = (d["left"][i], d["top"][i], d["width"][i], d["height"][i])
        x, w = int(x * w_scale), int(w * w_scale)
        y, h = int(y * h_scale), int(h * h_scale)
        linewidth = int(2 * min(w_scale, h_scale))
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), linewidth)
        if int(d["word_num"][i]) > 0:
            text = str(d["text"][i])
            font_scale = min(w_scale, h_scale)
            cv2.putText(
                img,
                text,
                (x, y),
                cv2.FONT_HERSHEY_DUPLEX,
                font_scale,
                (0, 0, 255),
                1,
                2,
            )

    cv2.imshow("img", img)
    cv2.waitKey(0)


# by passing file paths
def overlay_data(img_path, bboxes_path, w_scale=1, h_scale=1):
    # original img
    img = cv2.imread(img_path)

    # read tess output
    df = pd.read_csv(bboxes_path, header=0, encoding="unicode_escape")
    print(df.head())
    d = df.to_dict()

    _overlay_data(img, d, w_scale, h_scale)


if __name__ == "__main__":
    overlay_data("./images/2.jpg", "./ocr/2.csv", w_scale=0.4, h_scale=0.4)
