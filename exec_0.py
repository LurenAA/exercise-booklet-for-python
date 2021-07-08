from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

IMAGE_PATH = "python-logo@2x.png"
TTF_PATH = r"C:\Windows\Fonts\ALGER.TTF"
OUTPUT_PATH = "result.png"


def add_text_to_pic(pic_file, position_tuple, added_text,
                    ttf_path=TTF_PATH, font_size=30, color='red'):

    font_type = ImageFont.truetype(ttf_path, font_size)
    editable_image = ImageDraw.Draw(pic_file)
    editable_image.text(position_tuple, added_text,
                        color, font_type)

    return pic_file


def add_num_to_pic(pic_file, position_tuple, added_num=4,
                   ttf_path=TTF_PATH, font_size=30, color='red'):

    assert(type(position_tuple) == tuple)
    return add_text_to_pic(pic_file, position_tuple, str(added_num),
                           ttf_path, font_size, color)


if __name__ == "__main__":
    image = Image.open(IMAGE_PATH)
    image_width, image_height = image.size
    add_num_to_pic = add_num_to_pic(image, (image_width - 30, 15))
    image.save(OUTPUT_PATH)
