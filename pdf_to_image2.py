import fitz
from env import IMG_WIDTH, IMG_HEIGHT, IMAGES, IMG_EXT


def _get_pdf_dims(doc: fitz.Document) -> list[tuple]:
    # page sizes in pts
    # when converting to image, a point can be looked at as synonymous as a pixel in a resolution
    # so zoom=2 in fitz.Matrix would double the res
    page_dims = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        rect = page.rect
        dims = (rect.width, rect.height)
        page_dims.append(dims)
    return page_dims


def __res_to_zoom(pdf_w, pdf_h, img_w=IMG_WIDTH, img_h=IMG_HEIGHT):
    zoom_x = img_w / pdf_w
    zoom_y = img_h / pdf_h
    return (zoom_x, zoom_y)


def _res_to_zoom(page_dims: list[tuple]) -> list[tuple]:
    zooms = []
    for dims in page_dims:
        w, h = dims[0], dims[1]
        zoom_x, zoom_y = __res_to_zoom(w, h, img_w=IMG_WIDTH, img_h=IMG_HEIGHT)
        zooms.append((zoom_x, zoom_y))
    return zooms


def pdf_to_image2(pdf_path, save_dir=IMAGES, save_name="1"):
    doc = fitz.open(pdf_path)
    pdf_dims = _get_pdf_dims(doc)
    pdf_zooms = _res_to_zoom(pdf_dims)

    if len(doc) == 1:
        zoom_x, zoom_y = pdf_zooms[0][0], pdf_zooms[0][1]
        mat = fitz.Matrix(zoom_x, zoom_y)
        pix = doc[0].get_pixmap(matrix=mat)
        pix.save(f"{save_dir}/{save_name}{IMG_EXT}")
    else:
        for i, pdf_zoom in enumerate(pdf_zooms, start=0):
            zoom_x, zoom_y = pdf_zoom[0], pdf_zoom[1]
            mat = fitz.Matrix(zoom_x, zoom_y)
            pix = doc[i].get_pixmap(matrix=mat)
            pix.save(f"{save_dir}/{save_name}_{i + 1}{IMG_EXT}")


if __name__ == "__main__":
    pdf_to_image2("./pdf_file/1.pdf")
