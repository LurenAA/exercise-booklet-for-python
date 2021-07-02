import random

import pymysql


def gen_code():
    code = ""
    num = 0
    for i in range(6):
        num = random.randint(33, 126)
        code += chr(num)
    return code


if __name__ == "__main__":
    db = pymysql.connect(host="127.0.0.1", port=3306,
                         user="root", passwd="x99228899",
                         db="test", charset="utf8")
    cursor = db.cursor()
    code = ""
    my_set = set()
    flag = False
    for i in range(200):
        while not flag:
            code = gen_code()
            if code not in my_set:
                flag = True
                my_set.add(code)
        cursor.execute("insert into actcode values ({0})".format(
            db.escape(code)))
        db.commit()
        flag = False
    db.close()
