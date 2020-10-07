import ctypes


class DynamicArray:
    def __init__(self):
        self._length = 0
        self._capacity = 1
        self._arr = self._create_array(self._capacity)

    def __getitem__(self, idx):
        """Return the element at the specified index"""
        if 0 <= idx < self._length:
            return self._arr[idx]
        raise IndexError("Index out of bounds")

    def __len__(self):
        """Return the number of elements in the array"""
        return self._length

    def append(self, element):
        """Add a new element to the end of the array"""
        if self._length == self._capacity:  # Need to increase size
            self._capacity *= 2
            longer_arr = self._create_array(self._capacity)
            for i in range(self._length):
                longer_arr[i] = self._arr[i]
            self._arr = longer_arr

        self._arr[self._length] = element
        self._length += 1

    @staticmethod
    def _create_array(capacity):
        return (ctypes.py_object * capacity)()


if __name__ == '__main__':
    arr = DynamicArray()
    print(len(arr))
    for i in range(100):
        arr.append(i)
    print(len(arr))
