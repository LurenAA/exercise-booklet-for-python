import re

TEST_FILE_PATH = "english_text"


def count_text_words_num(file_path):
    assert(type(file_path) == str)
    total_word_num = 0

    with open(file_path, "r") as file:
        for line in file:
            while len(line):
                match_object = re.search(r"([a-zA-Z]+[-_.][a-zA-Z]+)|"
                                         r"([A-Z]?[a-z]+)|([a-z]+)", line)
                if match_object:
                    # print(match_object.group(0))
                    total_word_num += 1
                    line = line[match_object.end():]
                else:
                    break

    return total_word_num


if __name__ == "__main__":
    total_word_num = count_text_words_num(TEST_FILE_PATH)
    print(total_word_num)
