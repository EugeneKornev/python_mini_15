import sys
from collections import deque
from threading import Thread, Lock
from time import perf_counter

stack = deque()
lock = Lock()
global_res = 0


def producer(k: int):
    global stack
    for i in range(k):
        with lock:
            stack.append((i, 5, 3))


def matrix_multi(p: [[int]], q: [[int]]) -> [[int]]:
    r = [[0 for _ in range(len(q[0]))] for __ in range(len(p))]
    for i in range(len(p)):
        for j in range(len(q[0])):
            for k in range(len(q)):
                r[i][j] += p[i][k] * q[k][j]
    return r


def eye(n: int) -> [[int]]:
    return [[int(i == j) for j in range(n)] for i in range(n)]


def matrix_expo(p: [[int]], n: int) -> [[int]]:
    match n:
        case 0:
            return eye(len(p))
        case 1:
            return p
        case _:
            return matrix_multi(p, matrix_expo(p, n - 1))


def matrix_create(value: int, size: int) -> [[int]]:
    result = [[0 for _ in range(size)] for __ in range(size)]
    for i in range(size):
        for j in range(size):
            result[i][j] = value ** (i + j)
    return result


def matrix_sum(p: [[int]]) -> int:
    return sum(sum(i) for i in p)


def consumer():
    global stack
    res = 0
    while True:
        with lock:
            if len(stack) == 0:
                break
            size, value, times = stack.pop()
        matr = matrix_create(value, size)
        matr = matrix_expo(matr, times)
        res += matrix_sum(matr)
    with lock:
        global global_res
        global_res += res


def test(n, k):
    global global_res
    threads = [Thread(target=consumer) for _ in range(n)]
    prod = Thread(target=producer, args=[k])
    start = perf_counter()
    prod.start()
    for e in threads:
        e.start()
    for e in threads:
        e.join()
    prod.join()
    end = perf_counter()
    tmp_res = global_res
    global_res = 0
    return tmp_res, end - start


def main():
    if hasattr(sys, "_is_gil_enabled") and not sys._is_gil_enabled():
        print("GIL is disabled")
    else:
        print("GIL is enabled")
    count_of_tasks = 75
    for i in [1, 2, 3, 4] + [j for j in range(5, 51, 5)]:
        sum_of_matr, time_of_exe = test(i, count_of_tasks)
        # print(f"{i} {time_of_exe} {sum_of_matr}")
        print(f"{i} {time_of_exe}")


if __name__ == "__main__":
    main()

