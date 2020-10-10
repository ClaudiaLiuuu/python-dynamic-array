## Dynamic Array
This project is an implementation of a dynamic array class in python using a compact array as the underlying data structure. The goal is to mimic python's native list class to learn about implementing special method's for sequence types and modifying the size of the array to keep a constant amortized runtime for insertion and deletion operations.

The compact array that supports this class is doubled in size once the capacity of the dynamic array fills, and it shrinks to half size once the current number of elements in the list is a quarter of capacity.

#### Files
* `dynamic_array.py` contains the `DynamicArray` class
* `test_dynamic_array.py` contains tests for public methods and operations of the `DynamicArray` class
* `runtime_comparison.py` compares the runtimes of `DynamicArray` methods versus python's native `list`

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

#### Runtime Analysis
The file `runtime_comparison.py` compares the runtimes of the public methods of `DynamicArray` with the runtimes of python's `list` using the `time` module. This is an imperfect comparison because other processes running on the machine will make this process take longer, but it provides some insight into the efficiency of a python `list`. A sample output is included below, and it is clear that python's native implementation of a dynamic array vastly outperforms this one. The output for each method can be interpreted as:
```
All times are in microseconds.

append - average time per append for n appends
extend - average time per extend for n extends
insert - average time per insertion to front for n inserts
remove - average time per remove for n removes of element in front
pop - average time per pop for n pops from back
clear - time to clear an array of n elements
index - time to find element near back of array of n elements
count - time to count element occurrence in array of n elements
sort - time to sort array of n elements
reverse - time to reverse array of n elements
copy - time to return a shallow copy of array of n elements
```

**Sample Table:**
```
                              n = 10         n = 100        n = 1000       
append    | DynamicArray      10.70          4.28           6.49           
          | Native List       0.31           0.20           0.19           
---------------------------------------------------------------------------
extend    | DynamicArray      10.70          5.79           8.59           
          | Native List       0.41           0.37           0.11           
---------------------------------------------------------------------------
insert    | DynamicArray      5.20           31.65          404.59         
          | Native List       0.31           0.30           0.37           
---------------------------------------------------------------------------
remove    | DynamicArray      4.98           22.12          292.49         
          | Native List       0.21           0.14           0.18           
---------------------------------------------------------------------------
pop       | DynamicArray      3.91           2.27           2.21           
          | Native List       0.19           0.06           0.06           
---------------------------------------------------------------------------
clear     | DynamicArray      4.05           2.86           14.07          
          | Native List       0.95           0.95           2.62           
---------------------------------------------------------------------------
index     | DynamicArray      6.20           11.92          114.20         
          | Native List       0.00           2.15           12.87          
---------------------------------------------------------------------------
count     | DynamicArray      5.01           13.83          152.83         
          | Native List       0.95           0.95           4.05           
---------------------------------------------------------------------------
sort      | DynamicArray      24.80          1226.90        89034.08       
          | Native List       2.15           4.77           19.79          
---------------------------------------------------------------------------
reverse   | DynamicArray      9.06           46.97          468.02         
          | Native List       0.95           0.95           1.19           
---------------------------------------------------------------------------
copy      | DynamicArray      3.10           3.10           3.10           
          | Native List       0.72           0.95           0.00           
---------------------------------------------------------------------------
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