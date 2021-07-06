from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

IMAGE_PATH = "python-logo@2x.png"
TTF_PATH = r"C:\Windows\Fonts\ALGER.TTF"
OUTPUT_PATH = "result.png"


def add_num_to_pic(pic_file, added_num=4,
                   ttf_path=TTF_PATH, font_size=30, color='red'):
    image_width, image_height = pic_file.size
    added_num = str(added_num)
    number_font = ImageFont.truetype(ttf_path, font_size)

    editable_image = ImageDraw.Draw(pic_file)
    editable_image.text((image_width - 30, 15), added_num,
                        color, number_font)

    return pic_file


if __name__ == "__main__":
    image = Image.open(IMAGE_PATH)
    add_num_to_pic = add_num_to_pic(image)
    image.save(OUTPUT_PATH)
