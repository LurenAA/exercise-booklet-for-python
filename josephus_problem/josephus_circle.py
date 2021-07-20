from collections import deque


class JcSolution:
    def __init__(
        self, container: "iterable", start_index: int, interval: "nonzeno int"
    ):
        assert interval and type(interval) == int
        assert (
            hasattr(container, "__iter__")
            and hasattr(container.__iter__(), "__next__")
            or hasattr(container, "__next__")
            or hasattr(container, "__getitem__")
        )
        assert 0 <= start_index < len(container)

        self._container = container
        self._start_index = start_index
        self._interval = interval

    def __iter__(self):
        return self._solve_josephus_circle(
            self._container, self._start_index, self._interval
        )

    def _solve_josephus_circle(
        self, container, start_index, interval
    ):
        deque_copy = deque(container)
        if interval < 0:
            deque_copy.reverse()
            interval = -interval
        passed_index = start_index - 1
        # result_list = list()
        deque_len = len(deque_copy)

        while deque_len > 1:
            passed_index = (passed_index + interval) % deque_len
            # result_list.append(deque_copy[passed_index])
            yield deque_copy[passed_index]
            del deque_copy[passed_index]
            passed_index -= 1
            deque_len -= 1

        # result_list.append(deque_copy[0])
        yield deque_copy[0]
        # return result_list
