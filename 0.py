from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

IMAGE_PATH = "python-logo@2x.png"
TTF_PATH = "Roboto-Black.ttf"
OUTPUT_PATH = "result.png"

if __name__ == "__main__":
    my_image = Image.open(IMAGE_PATH)
    image_width, image_height = my_image.size
    add_num = "4"
    number_font = ImageFont.truetype(TTF_PATH, 30)
    editable_image = ImageDraw.Draw(my_image)
    editable_image.text((image_width - 30, 15), add_num, (255, 0, 0), number_font)
    my_image.save(OUTPUT_PATH)
