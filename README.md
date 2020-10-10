## Dynamic Array
This project is an implementation of a dynamic array class in python using a compact array as the underlying data structure. The goal is to mimic python's native list class to learn about implementing special method's for sequence types and modifying the size of the array to keep a constant amortized runtime for insertion and deletion operations.

The compact array that supports this class is doubled in size once the capacity of the dynamic array fills, and it shrinks to half size once the current number of elements in the list is a quarter of capacity.

#### Supported Methods

This dynamic arrays supports all of the public methods of python's list class as well as operators such as `+` for concatenation of arrays and `*` for repeating elements in the array. It also supports slice notation.

#### Usage
To use this dynamic array, simply import it and create an instance of the class. It can then be used similarly to the native list. It has been tested to work with python 3.8.

```
from dynamic_array import DynamicArray
arr = DynamicArray()
for i in range(5):
    arr.append(i)
print(arr) # [0, 1, 2, 3, 4]
arr.pop() # 4
arr.pop(0) # 0
print(arr) # [1, 2, 3]
```

#### Testing
Tests are included in the `test_dynamic_array.py` file and can be run with the `unittest` module.
```
python3 -m unittest test_dynamic_array
...........................
----------------------------------------------------------------------
Ran 27 tests in 4.285s

OK

```

#### Runtime Analysis
This section will be updated with average runtime comparisons between the methods of python's native list with this dynamic array.