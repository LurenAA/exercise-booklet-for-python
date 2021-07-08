import random

DEFAULT_NUM = 200


def gen_code():
    code = ""
    num = 0

    for i in range(6):
        num = random.randint(33, 126)
        code += chr(num)

    return code


def gen_code_set(num=DEFAULT_NUM):
    assert(type(num) == int and num > 0)

    num = int(num)
    code_set = set()
    code = ""
    flag = False

    for i in range(num):
        while not flag:
            code = gen_code()
            if code not in code_set:
                flag = True
                code_set.add(code)
        flag = False

    return code_set


if __name__ == "__main__":
    print(gen_code_set())
