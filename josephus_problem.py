from collections import deque


class Student:
    def __init__(self, name, id):
        self.name = name
        self.id = id

    def __repr__(self):
        return "{%s:%d}" % (self.name, self.id)


def josephus_circle_solution(container, start_index, interval):
    assert(0 <= start_index < len(container))
    assert(interval and type(interval) == int)
    assert(container.__iter__ and container.__iter__().__next__
           or container.__next__)

    deque_from_container = deque(container)
    if interval < 0:
        deque_from_container.reverse()
        interval = -interval
    passed_index = start_index - 1
    result_list = list()
    deque_len = len(deque_from_container)

    while deque_len > 1:
        passed_index = (passed_index + interval) % deque_len
        result_list.append(deque_from_container[passed_index])
        deque_from_container.remove(deque_from_container[passed_index])
        passed_index -= 1
        deque_len -= 1

    result_list.append(deque_from_container[0])
    return result_list


# josephus_circle_solution函数的递归版本
def josephus_circle_solution_recursive(container, start_index, interval):
    assert(0 <= start_index < len(container))
    assert(interval and type(interval) == int)
    assert(container.__iter__ and container.__iter__().__next__
           or container.__next__)

    deque_from_container = deque(container)
    if interval < 0:
        deque_from_container.reverse()
        interval = -interval
    passed_index = start_index - 1
    result_list = list()
    deque_len = len(deque_from_container)

    return josephus_circle_solution_recursive_helper(
        passed_index, interval, deque_len, result_list, deque_from_container)


def josephus_circle_solution_recursive_helper(
        passed_index, interval, deque_len, result_list, deque_from_container):
    if deque_len == 1:
        result_list.append(deque_from_container[0])
        return result_list

    passed_index = (passed_index + interval) % deque_len
    result_list.append(deque_from_container[passed_index])
    deque_from_container.remove(deque_from_container[passed_index])
    passed_index -= 1
    deque_len -= 1

    return josephus_circle_solution_recursive_helper(
        passed_index, interval, deque_len, result_list, deque_from_container)


if __name__ == "__main__":
    stu_info = (("肖龚柏1", 1), ("肖龚柏2", 2), ("肖龚柏3", 3),
                ("肖龚柏4", 4), ("肖龚柏5", 5), ("肖龚柏6", 6), ("肖龚柏7", 7))
    stu_list = [Student(*x) for x in stu_info]
    print(josephus_circle_solution(stu_list, 0, 3))
