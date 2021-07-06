import redis

from exec_1 import gen_code_set

if __name__ == "__main__":
    redi = redis.Redis(host='localhost', port=6379, decode_responses=True)

    code_set = gen_code_set()

    for (index, code) in enumerate(code_set):
        redi.set('code' + str(index), code)
