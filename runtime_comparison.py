from dynamic_array import DynamicArray
from time import time


def test_method_runtime(method, size, value=None):
    """Return average runtime of method on size elements for native list and DynamicArray"""
    arr_dyn = DynamicArray()
    arr_list = list()

    # Get alias for respective method in class
    method_dyn = arr_dyn.__getattribute__(method)
    method_list = arr_list.__getattribute__(method)

    def time_method(func):
        """Return average runtime in microseconds of function over size elements"""
        start_time = time()  # Begin timing
        for i in range(size):  # Run size operations
            func(value)
        end_time = time()  # End timing
        return ((end_time - start_time) / size) * 10 ** 6  # Return average

    return time_method(method_dyn), time_method(method_list)


def format_method(method_name, value=None):
    dyn_sml, nat_sml = test_method_runtime(method_name, 100, value)
    dyn_med, nat_med = test_method_runtime(method_name, 10000, value)
    dyn_lrg, nat_lrg = test_method_runtime(method_name, 1000000, value)

    results[method_name] = {
        'dynamic': [dyn_sml, dyn_med, dyn_lrg],
        'native': [nat_sml, nat_med, nat_lrg],
    }


results = {}
format_method('append', 5)
print(results)