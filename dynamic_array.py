import ctypes
from collections.abc import MutableSequence


class DynamicArray(MutableSequence):
    """An implementation of a dynamic array which supports the same methods as python's
    included list class. The list class is certainly more robust, but this implementation
    is done for practice.

    This class supports adding objects of any type to the array, and there is no need to
    declare an explicit length or type of object stored in the array. The runtimes should
    be asymptotically the same as python's native list implementation, but the actual
    runtimes will likely be slower than lists. Eventually, there will be support for
    operators such as +, but for now only the public list methods have been implemented.
    """

    def __init__(self, growth_factor=2):
        """Initializes DynamicArray with 0 elements, capacity of 1, an empty compact
        array of length 1 for storing pointers, and a growth factor of 2 such that the
        capacity will double each time that the array becomes full and shrink in half
        when less than 1/4 of the capacity is full.
        """
        self._length = 0  # Number of elements in array
        self._capacity = 1  # Capacity of array before expanding
        self._arr = self._create_array(self._capacity)  # Compact array of pointers
        self._growth_factor = max(2, growth_factor)  # Factor to grow array when capacity reached

    def __getitem__(self, idx):
        """Return the element at the specified index or return sliced array"""
        if isinstance(idx, slice):
            # Insert extreme values if none are specified
            start = 0 if idx.start is None else idx.start
            stop = self._length if idx.stop is None else idx.stop
            step = 1 if idx.step is None or idx.step == 0 else idx.step
            if start < 0:  # For negative indexing, convert to positive counterpart
                start = self._convert_negative_index(start)
            if stop < 0:
                stop = self._convert_negative_index(stop)
            if step < 1:  # Need to flip the start and stop values
                start, stop = stop - 1, start - 1
            # Return a new array with the values specified by the slice
            slice_arr = DynamicArray(self._growth_factor)
            for i in range(start, stop, step):
                slice_arr.append(self._arr[i])
            return slice_arr
        else:  # Integer index
            if idx < 0:  # For negative indexing, convert to positive counterpart
                idx = self._convert_negative_index(idx)
            if 0 <= idx < self._length:  # Check if index is within bounds
                return self._arr[idx]
            raise IndexError("Index out of bounds")

    def __setitem__(self, idx, element):
        """Set array value at index to element from syntax arr[idx] = element"""
        if idx < 0:  # For negative indexing, convert to positive counterpart
            idx = self._convert_negative_index(idx)
        if not 0 <= idx < self._length:  # Ignore indices outside of bounds
            raise IndexError(f'index {idx} out of bounds')
        self._arr[idx] = element

    def __delitem__(self, idx):
        """Delete the item at index from syntax del arr[idx]"""
        self.pop(idx)

    def __len__(self):
        """Return the number of elements in the array"""
        return self._length

    def __str__(self):
        """Return a string representation of the array"""
        return f'[{"".join(str(val) + ", " for val in self)[:-2]}]'

    def __repr__(self):
        """Return a string representation of the array for testing"""
        return self.__str__()

    def __eq__(self, seq):
        """Check if array is lexicographically equal to seq"""
        # If seq is different length or not a list, then it is not equal
        if self._length != len(seq) or not isinstance(seq, list):
            return False
        # seq is equal if every element at the same index has equivalent value
        return all(self._arr[i] == seq[i] for i in range(self._length))

    def __ne__(self, seq):
        """Check if array is not lexicographically equal to seq"""
        return not self.__eq__(seq)  # Reverse of equality check

    def __lt__(self, seq):
        """Check if array is lexicographically less than seq"""
        if any(self._arr[i] < seq[i] for i in range(min(self._length, len(seq)))):
            return True
        return self._length < len(seq)

    def __le__(self, seq):
        """Check if array is lexicographically less than or equal to seq"""
        if any(self._arr[i] > seq[i] for i in range(min(self._length, len(seq)))):
            return False
        return self._length <= len(seq)

    def __gt__(self, seq):
        """Check if array is lexicographically greater than seq"""
        return not self.__le__(seq)

    def __ge__(self, seq):
        """Check if array is lexicographically greater than or equal to seq"""
        return not self.__lt__(seq)

    def __add__(self, right_arr):
        """Concatenate array with the right operand"""
        concat_arr = self.copy()
        concat_arr.extend(right_arr)
        return concat_arr

    def __radd__(self, left_arr):
        """Concatenate array to the left operand"""
        concat_arr = left_arr.copy()
        concat_arr.extend(self)
        return concat_arr

    def __mul__(self, num):
        """Repeat values in arr num times if num is the right operand"""
        if num <= 0:  # Return an empty array
            return DynamicArray(self._growth_factor)
        # Append values to a new array num - 1 times
        mult_arr = self.copy()
        length = len(mult_arr)
        for _ in range(num - 1):
            for i in range(length):
                mult_arr.append(mult_arr[i])
        return mult_arr

    def __rmul__(self, num):
        """Repeat values in arr num times if num is the left operand"""
        return self.__mul__(num)

    def append(self, element):
        """Add a new element to the end of the array"""
        if self._length == self._capacity:  # Need to increase size
            self._grow_arr()  # Increase capacity by growth factor
        self._arr[self._length] = element
        self._length += 1

    def extend(self, seq):
        """Add all elements from seq to end of array"""
        for element in seq:
            self.append(element)

    def insert(self, idx, element):
        """Insert element in array at index"""
        if self._length == self._capacity:  # Need to increase size
            self._grow_arr()
        if idx < 0:  # For negative indexing, convert to positive counterpart
            idx = self._convert_negative_index(idx)
        idx = min(self._length, idx)  # Any index over the length is converted
        # Move values after idx one right to make room for new element
        for i in range(self._length, idx, -1):
            self._arr[i] = self._arr[i - 1]
        self._arr[idx] = element  # Insert element at new blank space
        self._length += 1

    def remove(self, element):
        """Remove first instance of element from array"""
        for i in range(self._length):  # Find index of element in array
            if self._arr[i] == element:
                # Move all elements after index j one forward to "delete" element
                for j in range(i, self._length - 1):
                    self._arr[j] = self._arr[j + 1]
                self._length -= 1
                self._check_shrink()  # Shrink array if length is too small
                return
        raise ValueError(f'{element} not in list')  # Raise if element not found

    def pop(self, idx=-1):
        """Remove element from end of array and return"""
        if idx < 0:  # For negative indexing, convert to positive counterpart
            idx = self._convert_negative_index(idx)
        if not 0 <= idx < self._length:  # Ignore indices outside of bounds
            raise IndexError(f'index {idx} out of bounds')
        element = self._arr[idx]  # Save element so it can be returned
        # Move all elements after index i one forward to "delete" element
        for i in range(idx, self._length - 1):
            self._arr[i] = self._arr[i + 1]
        self._length -= 1
        self._check_shrink()  # Shrink array if length is too small
        return element

    def clear(self):
        """Remove all values from the array"""
        self._length = 0  # "Erase" values by ignoring them
        self._resize_arr(1)  # Shrink array to original size

    def index(self, element, start=0, end=None):
        """Return index of first item matching element with support for slicing"""
        if end is None:  # Only bound end if value has been provided
            end = self._length
        if end < 0:  # For negative indexing, convert to positive counterpart
            end = self._convert_negative_index(end)
        start = min(self._length, max(0, start))  # Place start in bounds if extreme
        end = min(self._length, max(0, end))  # Place end in bounds if extreme
        for i in range(start, end):  # Search for element within bounds
            if self._arr[i] == element:
                return i
        raise ValueError(f'{element} not found in array')  # Raise if element not found

    def count(self, element):
        """Return number of occurrences of element in array"""
        count = 0
        for i in range(self._length):  # Increment count when equal value is found
            if self._arr[i] == element:
                count += 1
        return count

    def sort(self):
        """Sort elements in ascending order in place"""
        self._quick_sort(0, self._length - 1)

    def reverse(self):
        """Reverse all elements of the array in place"""
        left = 0  # Start at beginning of array
        right = self._length - 1  # Start at end of array
        while left <= right:  # Swap values until pointers collide
            self._arr[left], self._arr[right] = self._arr[right], self._arr[left]
            left, right = left + 1, right - 1

    def copy(self):
        """Return a shallow copy of the array"""
        copy_arr = DynamicArray(self._growth_factor)  # Create new array to store values
        for i in range(self._length):  # Append all values from original
            copy_arr.append(self._arr[i])
        return copy_arr

    def _quick_sort(self, start, end):
        """Recursively sort elements using the quick sort algorithm end inclusive"""
        if start >= end:  # Length of 1 or less
            return
        pivot = self._arr[end]  # Select pivot as last value in array
        left = start
        right = end - 1  # Begin one before the pivot
        while left <= right:  # Continue until all values are ordered
            while left <= right and self._arr[left] < pivot:  # Find first value greater than pivot
                left += 1
            while left <= right and pivot < self._arr[right]:  # Find first value less than pivot
                right -= 1
            if left <= right:  # If unordered, then swap two found values
                self._arr[left], self._arr[right] = self._arr[right], self._arr[left]
                left, right = left + 1, right - 1  # Increment for next iteration
        self._arr[left], self._arr[end] = self._arr[end], self._arr[left]  # Move pivot to middle
        self._quick_sort(start, left - 1)  # Sort left portion
        self._quick_sort(left + 1, end)  # Sort right portion

    def _convert_negative_index(self, idx):
        """Convert negative index to its positive counterpart"""
        return max(0, self._length + idx)

    def _check_shrink(self):
        """Checks if array should shrink and executes _shrink_arr if True"""
        # As an example, if length is 1/4 of capacity and growth factor is 2,
        # then the capacity should shrink in half to keep length proportional
        # to capacity
        if self._length < int(self._capacity / (self._growth_factor ** 2)):
            self._shrink_arr()

    def _shrink_arr(self):
        """Increase the capacity of the array by current capacity * growth factor"""
        self._resize_arr(self._capacity // self._growth_factor)

    def _grow_arr(self):
        """Decrease the capacity of the array by current capacity / growth factor"""
        self._resize_arr(self._capacity * self._growth_factor)

    def _resize_arr(self, new_capacity):
        """Resize the array to the specified capacity"""
        if new_capacity < self._length:
            raise RuntimeError('New capacity is lower than length')
        longer_arr = self._create_array(new_capacity)
        for i in range(self._length):
            longer_arr[i] = self._arr[i]
        self._arr = longer_arr
        self._capacity = new_capacity

    @staticmethod
    def _create_array(capacity):
        """Return a compact array for storing pointers"""
        return (ctypes.py_object * capacity)()


# todo complete README
# todo test operators versus native list to test runtime
# todo determine order for methods if necessary


if __name__ == '__main__':
    arr = DynamicArray()
    for i in range(5):
        arr.append(i)
    print(arr[:5:-3])
