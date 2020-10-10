from dynamic_array import DynamicArray
from time import time


def test_method_runtime(method, size, arr_dyn, arr_list, value=None):
    """Return average runtime of method on size elements for native list and DynamicArray"""
    # Get alias for respective method in class
    method_dyn = arr_dyn.__getattribute__(method)
    method_list = arr_list.__getattribute__(method)

    def time_method(func):
        """Return average runtime in microseconds of function over size elements"""
        start_time = time()  # Begin timing
        if value is None:
            for i in range(size):
                func()
        else:
            for i in range(size):  # Run size operations
                func(*value)
        end_time = time()  # End timing
        return ((end_time - start_time) / size) * 10 ** 6  # Return average

    return time_method(method_dyn), time_method(method_list)


def compare_public_methods():
    methods = [('append', [6], None),
               ('extend', [[6, 6]], None),
               ('insert', [0, 6], None),
               ('remove', [6], None),
               ('pop', None, None),
               ('clear', None, 1),
               ('index', [6], 1),
               ('count', [6], 1),
               ('sort', None, 1),
               ('reverse', None, 1),
               ('copy', None, 1)]
    results = {}

    for method_name, value, num_times in methods[10:11]:
        print(f'Running method {method_name}')

        dyn_sml, dyn_med, dyn_lrg = DynamicArray(), DynamicArray(), DynamicArray()
        nat_sml, nat_med, nat_lrg = list(), list(), list()

        # Begin tests with initial array already created
        if method_name in {'remove', 'pop', 'clear', 'count'}:
            dyn_sml.extend([6 for i in range(100)])
            nat_sml.extend([6 for i in range(100)])
            dyn_med.extend([6 for i in range(1000)])
            nat_med.extend([6 for i in range(1000)])
            dyn_lrg.extend([6 for i in range(10000)])
            nat_lrg.extend([6 for i in range(10000)])
        elif method_name in {'index', 'sort', 'reverse'}:
            dyn_sml.extend([i for i in range(100, 0, -1)])
            nat_sml.extend([i for i in range(100, 0, -1)])
            dyn_med.extend([i for i in range(1000, 0, -1)])
            nat_med.extend([i for i in range(1000, 0, -1)])
            dyn_lrg.extend([i for i in range(10000, 0, -1)])
            nat_lrg.extend([i for i in range(10000, 0, -1)])

        sml_times = 10 if num_times is None else 1
        med_times = 1000 if num_times is None else 1
        lrg_times = 10000 if num_times is None else 1

        dyn_sml, nat_sml = test_method_runtime(method_name, sml_times, dyn_sml, nat_sml, value)
        dyn_med, nat_med = test_method_runtime(method_name, med_times, dyn_med, nat_med, value)
        dyn_lrg, nat_lrg = test_method_runtime(method_name, lrg_times, dyn_lrg, nat_lrg, value)

        results[method_name] = {
            'dynamic': [dyn_sml, dyn_med, dyn_lrg],
            'native': [nat_sml, nat_med, nat_lrg],
        }

    return results


print(compare_public_methods())
