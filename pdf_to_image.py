from pdf2image import convert_from_path
from env import POPPLER_PATH, IMAGES, IMG_EXT, IMG_WIDTH, IMG_HEIGHT

def pdf_to_image(
    pdf_path,
    img_w=IMG_WIDTH,
    img_h=IMG_HEIGHT,
    save_dir=IMAGES,
    save_name="1",
    poppler_path=POPPLER_PATH,
):
    # size=400 will fit the image to a 400x400 box, preserving aspect ratio
    # size=(400, None) will make the image 400 pixels wide, preserving aspect ratio
    # size=(500, 500) will resize the image to 500x500 pixels, not preserving aspect ratio
    images = convert_from_path(pdf_path, poppler_path=poppler_path, size=(img_w, img_h))
    if len(images) == 1:
        images[0].save(f"{save_dir}/{save_name}{IMG_EXT}")
    elif len(images) > 1:
        for i, image in enumerate(images, start=1):
            image.save(f"{save_dir}/{save_name}_{i}{IMG_EXT}")


if __name__ == "__main__":
    pdf_to_image("./pdf_file/1.pdf")
