from dynamic_array import DynamicArray
from time import time


def test_method(method, size, value=None):
    arr_dyn = DynamicArray()
    arr_list = list()
    func1 = arr_dyn.__getattribute__(method)
    func2 = arr_list.__getattribute__(method)

    def time_method(func):
        start_time = time()
        for i in range(size):
            func(value)
        end_time = time()
        return ((end_time - start_time) / size) * 10 ** 6

    avg_dyn = time_method(func1)
    avg_list = time_method(func2)

    return avg_dyn, avg_list


avg_dyn_append, avg_list_append = test_method('append', 1000000, 1)
print(avg_dyn_append, avg_list_append)
