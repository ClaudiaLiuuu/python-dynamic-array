import sys
from dynamic_array import DynamicArray
from time import time

# Defines the number of times to run a method in a row. For example, with SMALL of 100,
# the append method will be run 100 times in a row for the test of small arrays.
SMALL = 10
MEDIUM = 100
LARGE = 1000

DEF_VAL = 6  # Default value to pass to methods that need a number (Example: arr.append(6))

sys.setrecursionlimit(1500)  # Allow for greater recursion depth for sort test


def comp_method_runtime(method, times, arr_dyn, arr_list, value=None):
    """Return average runtime of method run times number of times for native list and DynamicArray"""
    # Get alias for respective method in class
    method_dyn = arr_dyn.__getattribute__(method)
    method_list = arr_list.__getattribute__(method)

    def time_method(func):
        """Return average runtime in microseconds of function over size elements"""
        start_time = time()  # Begin timing
        if value is None:  # When no value is passed, simply run the method
            for i in range(times):  # Run method specified number of times
                func()
        else:  # Pass the values by unpacking when arguments are needed
            for i in range(times):
                func(*value)
        end_time = time()  # End timing
        return ((end_time - start_time) / times) * 10 ** 6  # Return average

    return time_method(method_dyn), time_method(method_list)


def comp_public_methods():
    """Iterate through public methods and return a dictionary containing the average runtimes"""
    # Define each method as a tuple containing the name, any values to pass to the method embedded
    # in a list to allow for unpacking, and a third value specifying how many times the method
    # should be run or None to use the default settings of 100, 1000, and 10000
    methods = [('append', [DEF_VAL], None),
               ('extend', [[DEF_VAL, DEF_VAL]], None),
               ('insert', [0, DEF_VAL], None),  # Always insert in the front
               ('remove', [DEF_VAL], None),  # Remove every element from the array
               ('pop', None, None),
               ('clear', None, 1),
               ('index', [DEF_VAL], 1),
               ('count', [DEF_VAL], 1),
               ('sort', None, 1),
               ('reverse', None, 1),
               ('copy', None, 1)]

    results = {}  # Stores the runtimes

    for method_name, value, num_times in methods:
        # Create the starting arrays for the comparisons
        dyn_sml, dyn_med, dyn_lrg = DynamicArray(), DynamicArray(), DynamicArray()
        nat_sml, nat_med, nat_lrg = list(), list(), list()

        # Certain comparisons need to have arrays already created for running the methods such
        # as pop(), so these arrays are created in advance. This code could certainly be cleaned
        # up a bit by putting some of this repetitive structure into a function, but it is
        # currently not too long and clearly displays what it is doing.
        if method_name in {'remove', 'pop', 'clear', 'count'}:
            dyn_sml.extend([DEF_VAL for i in range(SMALL)])
            nat_sml.extend([DEF_VAL for i in range(SMALL)])
            dyn_med.extend([DEF_VAL for i in range(MEDIUM)])
            nat_med.extend([DEF_VAL for i in range(MEDIUM)])
            dyn_lrg.extend([DEF_VAL for i in range(LARGE)])
            nat_lrg.extend([DEF_VAL for i in range(LARGE)])
        elif method_name in {'index', 'sort', 'reverse'}:
            dyn_sml.extend([i for i in range(SMALL, 0, -1)])
            nat_sml.extend([i for i in range(SMALL, 0, -1)])
            dyn_med.extend([i for i in range(MEDIUM, 0, -1)])
            nat_med.extend([i for i in range(MEDIUM, 0, -1)])
            dyn_lrg.extend([i for i in range(LARGE, 0, -1)])
            nat_lrg.extend([i for i in range(LARGE, 0, -1)])

        # For some operations such as sort and reverse, they should only be run once
        sml_times = SMALL if num_times is None else 1
        med_times = MEDIUM if num_times is None else 1
        lrg_times = LARGE if num_times is None else 1

        # Compute the runtimes and store the average
        dyn_sml, nat_sml = comp_method_runtime(method_name, sml_times, dyn_sml, nat_sml, value)
        dyn_med, nat_med = comp_method_runtime(method_name, med_times, dyn_med, nat_med, value)
        dyn_lrg, nat_lrg = comp_method_runtime(method_name, lrg_times, dyn_lrg, nat_lrg, value)

        # Store the averages for each method in the results dictionary
        results[method_name] = {
            'dynamic': [dyn_sml, dyn_med, dyn_lrg],
            'native': [nat_sml, nat_med, nat_lrg],
        }

    return results


result = comp_public_methods()  # Calculate runtimes

# Print results separated by method
print(f'{"":<30}n = {SMALL:<11}n = {MEDIUM:<11}n = {LARGE:<11}')
for method, times in result.items():
    print(f'{method:<10}', end='')
    for implementation, time in times.items():
        if implementation == 'dynamic':
            print(f'{"| DynamicArray":<20}{time[0]:<15.2f}{time[1]:<15.2f}{time[2]:<15.2f}')
        else:
            print(f'{"":<10}{"| Native List":<20}{time[0]:<15.2f}{time[1]:<15.2f}{time[2]:<15.2f}')
    print(f'{"":-<75}')

