import random

import pymysql

USER_NAME = "root"
PASS_WORD = "x99228899"
HOST = "127.0.0.1"
DB = "test"
CHARSET = "utf8"


def gen_code():
    code = ""
    num = 0
    for i in range(6):
        num = random.randint(33, 126)
        code += chr(num)
    return code


if __name__ == "__main__":
    db = pymysql.connect(host=HOST, port=3306,
                         user=USER_NAME, passwd=PASS_WORD,
                         db=DB, charset=CHARSET)
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
