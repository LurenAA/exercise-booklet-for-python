def josephus_problem_solution(total_person_num, kill_person_num):
    person_list = list(range(total_person_num))
    kill_index = -1

    while len(person_list) > 1:
        kill_index = (kill_index + kill_person_num % total_person_num
                      + total_person_num) % total_person_num
        person_list.pop(kill_index)
        kill_index -= 1
        total_person_num -= 1

    return person_list[0]


def josephus_problem_solution_recursive(total_person_num, kill_person_num):
    person_list = list(range(total_person_num))
    kill_index = -1
    return josephus_problem_solution_recursive_helper(
        total_person_num, kill_person_num, person_list, kill_index)


def josephus_problem_solution_recursive_helper(
        total_person_num, kill_person_num, person_list, kill_index):
    if len(person_list) == 1:
        return person_list[0]

    kill_index = (kill_index + kill_person_num % total_person_num
                  + total_person_num) % total_person_num
    person_list.pop(kill_index)
    kill_index -= 1
    total_person_num -= 1

    return josephus_problem_solution_recursive_helper(
            total_person_num, kill_person_num, person_list, kill_index)


if __name__ == "__main__":
    print(josephus_problem_solution_recursive(5, 3))
