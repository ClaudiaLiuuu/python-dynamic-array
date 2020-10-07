import ctypes


class DynamicArray:
    def __init__(self):
        self._length = 0
        self._capacity = 1
        self._arr = self._create_array(self._capacity)
        self._growth_factor = 2

    def __getitem__(self, idx):
        """Return the element at the specified index"""
        if 0 <= idx < self._length:
            return self._arr[idx]
        raise IndexError("Index out of bounds")

    def __len__(self):
        """Return the number of elements in the array"""
        return self._length

    def __eq__(self, seq):
        """Check if array is lexicographically equal to seq"""
        if self._length != len(seq) or not isinstance(seq, list):
            return False
        return all(self._arr[i] == seq[i] for i in range(self._length))

    def __ne__(self, seq):
        """Check if array is not lexicographically equal to seq"""
        return not self.__eq__(seq)

    def append(self, element):
        """Add a new element to the end of the array"""
        if self._length == self._capacity:  # Need to increase size
            self._grow_arr()
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
                return
        raise ValueError(f'{element} not in list')  # Raise if element not found

    def pop(self, idx=-1):
        """Remove element from end of array and return"""
        if idx < 0:  # For negative indexing, convert to positive counterpart
            idx = self._convert_negative_index(idx)
        if not 0 <= idx < self._length:  # Ignore indices outside of bounds
            raise IndexError(f'pop index {idx} out of bounds')
        element = self._arr[idx]  # Save element so it can be returned
        # Move all elements after index i one forward to "delete" element
        for i in range(idx, self._length - 1):
            self._arr[i] = self._arr[i + 1]
        self._length -= 1
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
        return (ctypes.py_object * capacity)()


if __name__ == '__main__':
    arr = DynamicArray()
    for i in range(5):
        arr.append(i)
