import pymysql

from exec_1 import gen_code_set

USER_NAME = "root"
PASS_WORD = "x99228899"
HOST = "127.0.0.1"
DB = "test"
CHARSET = "utf8"

if __name__ == "__main__":
    db = pymysql.connect(host=HOST, port=3306,
                         user=USER_NAME, passwd=PASS_WORD,
                         db=DB, charset=CHARSET)
    cursor = db.cursor()

    code_set = gen_code_set()

    for code in code_set:
        cursor.execute("insert into actcode values (%s)" % (
                       db.escape(code)))
        db.commit()

    db.close()
