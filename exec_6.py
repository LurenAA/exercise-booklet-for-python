import os

TEST_DIR_PATH = "test_diaries"
TEST_WORDS = "python"


def count_text_words(file_path, words):

    assert(type(words) == str
           and type(file_path) == str)
    total_words_num = 0
    words_len = len(words)

    with open(file_path, "r") as file:
        for line in file:
            begin = 0
            while begin < len(line):
                str_low_index = line.find(words, begin)
                if str_low_index == -1:
                    break
                begin = words_len + str_low_index
                total_words_num += 1

    return total_words_num


if __name__ == "__main__":
    diaries = os.listdir(TEST_DIR_PATH)
    for diary in diaries:
        total_words_num = count_text_words(TEST_DIR_PATH +
                                           "/" + diary, TEST_WORDS)
        print(diary + ": " + str(total_words_num))
