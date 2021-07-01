from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

if __name__ == "__main__":
    my_image = Image.open("python-logo@2x.png")
    image_width, image_height = my_image.size
    add_num = "4"
    number_font = ImageFont.truetype('Roboto-Black.ttf', 30)
    editable_image = ImageDraw.Draw(my_image)
    editable_image.text((image_width - 30, 15), add_num,
                        (0, 0, 0), number_font)
    my_image.save("result.png")
