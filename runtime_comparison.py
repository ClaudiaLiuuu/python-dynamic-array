from dynamic_array import DynamicArray
from time import time


def test_append(size, value):
    arr_dyn = DynamicArray()
    arr_list = list()
    start_time = time()
    for i in range(size):
        arr_dyn.append(value)
    end_time = time()
    avg_dyn = ((end_time - start_time) / size) * 10**6
    start_time = time()
    for i in range(size):
        arr_list.append(value)
    end_time = time()
    avg_list = ((end_time - start_time) / size) * 10**6
    return avg_dyn, avg_list


avg_dyn_append, avg_list_append = test_append(1000000, 1)
print(avg_dyn_append, avg_list_append)
