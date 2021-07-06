TEST_TEXT_PATH = "exec_0.py"


def count_program_line(file_path):
    tripple_quote_flag = False
    total_line_num = 0
    annonation_line_num = 0
    blank_line = 0

    with open(TEST_TEXT_PATH) as file:
        for line in file:
            total_line_num += 1
            if tripple_quote_flag:
                annonation_line_num += 1
                if line[:3] == "'''" or line[:3] == '"""':
                    tripple_quote_flag = False
            else:
                if line == "\n":
                    blank_line += 1
                elif line[0] == "#":
                    annonation_line_num += 1
                elif line[:3] == "'''" or line[:3] == '"""':
                    annonation_line_num += 1
                    tripple_quote_flag = True

    return (total_line_num, annonation_line_num, blank_line)


if __name__ == "__main__":
    print(count_program_line(TEST_TEXT_PATH))
