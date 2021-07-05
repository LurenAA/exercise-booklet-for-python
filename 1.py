import random


def gen_code():
    code = ""
    num = 0
    for i in range(6):
        num = random.randint(33, 126)
        code += chr(num)
    return code


if __name__ == "__main__":
    my_set = set()
    code = ""
    flag = False
    for i in range(200):
        while not flag:
            code = gen_code()
            if code not in my_set:
                flag = True
                my_set.add(code)
        flag = False
    print(my_set)
