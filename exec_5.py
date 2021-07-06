import os

from PIL import Image

TEST_PIC_DIRECTORY = "test_picture_directory"
SAVE_NEW_PIC_DERECTORY = "test_picture_directory_new"
IPHONE_WIDTH = 320
IPHONE_HEIGHT = 568


def resize_pic(pic, width=IPHONE_WIDTH, height=IPHONE_HEIGHT):
    new_pic = pic.resize((width, height))
    return new_pic


if __name__ == "__main__":
    pic_entries = os.listdir(TEST_PIC_DIRECTORY)

    if not os.path.isdir(SAVE_NEW_PIC_DERECTORY):
        os.mkdir(SAVE_NEW_PIC_DERECTORY)

    for pic_file in pic_entries:
        pic = Image.open(TEST_PIC_DIRECTORY + "/" + pic_file)
        new_pic = resize_pic(pic)
        new_pic.save(SAVE_NEW_PIC_DERECTORY + "/" + pic_file)
