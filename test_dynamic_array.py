import unittest
from time import time
from dynamic_array import DynamicArray


class DynamicArrayTestCase(unittest.TestCase):
    """Tests for all public methods and operations of the DynamicArray class using
    _INITIAL_SIZE as the size of the test array which is filled with the values
    range(self._INITIAL_SIZE) and _GROWTH_FACTOR as the multiplier for shrinking
    and expanding the dynamic array.
    """
    _INITIAL_SIZE = 5  # Do not set below 5
    _GROWTH_FACTOR = 2

    def setUp(self):
        """Create a new DynamicArray instance"""
        self.arr = DynamicArray(self._GROWTH_FACTOR)
        for i in range(self._INITIAL_SIZE):
            self.arr.append(i)

    def test_append(self):
        """Test correct placement in array when appending 1,000 numbers"""
        arr = DynamicArray(self._GROWTH_FACTOR)
        num_elements = 1000
        self.assertEqual(len(arr), 0)
        for i in range(num_elements):
            arr.append(i)
            self.assertEqual(arr[i], i)
        self.assertEqual(len(arr), num_elements)

    def test_extend(self):
        """Test extending array maintains original values and adds new values"""
        self.arr.extend([i for i in range(self._INITIAL_SIZE, self._INITIAL_SIZE + 20)])
        for i in range(self._INITIAL_SIZE + 20):
            self.assertEqual(self.arr[i], i)

    def test_insert(self):
        """Test array insertion correctly inserts value at desired index"""
        # [0, 1, 2, 3, 4] --> [40, 0, 1, 50, 2, 3, 4, 60]
        arr = DynamicArray(self._GROWTH_FACTOR)
        for i in range(5):
            arr.append(i)
        arr.insert(0, 'apple')
        arr.insert(3, (5, -1))
        arr.insert(len(arr), self.arr)
        self.assertEqual(arr, ['apple', 0, 1, (5, -1), 2, 3, 4,
                               [i for i in range(self._INITIAL_SIZE)]])

    def test_insert_out_of_bounds(self):
        """Test inserting with indices that are out of bounds"""
        # [0, 1, 2, 3, 4] --> [-1, 0, 1, 2, 3, 5, 4, 6]
        arr = DynamicArray(self._GROWTH_FACTOR)
        for i in range(5):
            arr.append(i)
        arr.insert(-1, 5)
        arr.insert(100, 6)
        arr.insert(-10, -1)
        self.assertEqual(arr, [-1, 0, 1, 2, 3, 5, 4, 6])

    def test_remove_valid_item(self):
        """Test that element in array is removed"""
        self.arr.remove(2)
        self.assertNotIn(2, self.arr)
        self.assertEqual(self.arr[2], 3)

    def test_remove_invalid_item(self):
        """Test that ValueError is raised when element not found"""
        self.assertRaises(ValueError, self.arr.remove, self._INITIAL_SIZE)

    def test_pop_from_end(self):
        """Test that value popped from end is removed and returned"""
        self.assertEqual(self.arr.pop(), self._INITIAL_SIZE - 1)
        self.assertNotIn(self._INITIAL_SIZE - 1, self.arr)
        self.assertEqual(len(self.arr), self._INITIAL_SIZE - 1)

    def test_pop_from_middle(self):
        """Test that value popped from middle is removed and returned"""
        self.assertEqual(self.arr.pop(2), 2)
        self.assertNotIn(2, self.arr)
        self.assertEqual(len(self.arr), self._INITIAL_SIZE - 1)

    def test_pop_from_beginning(self):
        """Test that value popped from beginning is removed and returned"""
        self.assertEqual(self.arr.pop(0), 0)
        self.assertNotIn(0, self.arr)
        self.assertEqual(len(self.arr), self._INITIAL_SIZE - 1)

    def test_clear(self):
        """Test that all values are removed from the array"""
        self.arr.clear()
        self.assertEqual(len(self.arr), 0)
        self.assertEqual(self.arr, [])

    def test_index_single(self):
        """Test that index of item is returned when item is in array"""
        # Since the range function is used for setting up the initial values in the
        # dynamic array, the value at any index is equal to that index value. This makes
        # it ambiguous whether or not index() is returning the index or the value, so
        # that is why a new value without this property is appended and tested against.
        unique_value = self._INITIAL_SIZE + 2
        self.arr.append(unique_value)
        self.assertEqual(self.arr.index(unique_value), self._INITIAL_SIZE)

    def test_index_slice(self):
        """Test that index of item is returned from slice of array"""
        # See test_index_single method for explanation of unique_value
        unique_value = self._INITIAL_SIZE + 2
        self.arr.append(unique_value)
        s = self._INITIAL_SIZE  # Alias for less verbose statement
        self.assertEqual(self.arr.index(unique_value, s - (s // 2)), s)

    def test_index_invalid(self):
        """Test that ValueError is raised when item is not present in array"""
        self.assertRaises(ValueError, self.arr.index, self._INITIAL_SIZE + 2)

    def test_count(self):
        """Test correct number of occurrences is returned"""
        self.arr.append(self._INITIAL_SIZE - 1)
        self.assertEqual(self.arr.count(self._INITIAL_SIZE - 1), 2)
        self.assertEqual(self.arr.count(0), 1)
        self.assertEqual(self.arr.count(self._INITIAL_SIZE), 0)

    def test_sort(self):
        """Test that elements are correctly sorted in ascending order"""
        sorted_list = sorted([i for i in range(self._INITIAL_SIZE)])
        self.arr.sort()
        self.assertEqual(sorted_list, self.arr)

    def test_reverse(self):
        """Test that elements are reversed in array"""
        reversed_list = list(reversed([i for i in range(self._INITIAL_SIZE)]))
        self.arr.reverse()
        self.assertEqual(reversed_list, self.arr)

    def test_copy(self):
        """Test that a shallow copy of the list is returned"""
        copied_list = self.arr.copy()
        for i in range(len(self.arr)):
            self.assertIs(copied_list[i], self.arr[i])

    def test_print(self):
        """Test that array prints values similar to print(list)"""
        self.assertEqual(str(self.arr), str([i for i in range(self._INITIAL_SIZE)]))

    def test_comparison_operators(self):
        """Test array support for comparison operators (==, !=, <, <=, >, >=)"""
        self.assertEqual(self.arr, [i for i in range(5)])
        self.assertNotEqual(self.arr, [i for i in range(1, 6)])  # Different values
        self.assertNotEqual(self.arr, [i for i in range(0, 4)])  # Different lengths
        self.assertLess(self.arr, [i for i in range(1, 6)])  # One higher
        self.assertLessEqual(self.arr, [i for i in range(1, 6)])
        self.assertLessEqual(self.arr, [i for i in range(5)])
        self.assertGreater(self.arr, [i for i in range(-1, 4)])
        self.assertGreaterEqual(self.arr, [i for i in range(-1, 4)])
        self.assertGreaterEqual(self.arr, [i for i in range(5)])

    def time_array_appends(self, num_elements):
        """Returns average time in seconds of num_elements appends"""
        arr = DynamicArray(self._GROWTH_FACTOR)
        start_time = time()
        for i in range(num_elements):
            arr.append(i)
        end_time = time()
        # Return arr as well so it can be used for other tests
        return arr, (end_time - start_time) / num_elements

    @staticmethod
    def time_array_deletions(arr):
        """Returns average time in seconds of deleting all elements in arr"""
        start_time = time()
        length = len(arr)
        for i in range(length):
            arr.pop()
        end_time = time()
        return (end_time - start_time) / length

    def test_insert_and_delete_performance(self):
        """Test amortized runtime by comparing 10, 1000, and 1000000 operations"""
        # Test insertion runtime
        small_arr, avg_small_ins = self.time_array_appends(10)
        medium_arr, avg_medium_ins = self.time_array_appends(1000)
        large_arr, avg_large_ins = self.time_array_appends(1000000)
        self.assertAlmostEqual(avg_small_ins, avg_medium_ins, delta=0.05)
        self.assertAlmostEqual(avg_small_ins, avg_large_ins, delta=0.05)
        self.assertAlmostEqual(avg_medium_ins, avg_large_ins, delta=0.05)

        # Test deletion runtime
        avg_small_del = self.time_array_deletions(small_arr)
        avg_medium_del = self.time_array_deletions(medium_arr)
        avg_large_del = self.time_array_deletions(large_arr)
        self.assertAlmostEqual(avg_small_del, avg_medium_del, delta=0.05)
        self.assertAlmostEqual(avg_small_del, avg_large_del, delta=0.05)
        self.assertAlmostEqual(avg_medium_del, avg_large_del, delta=0.05)

        # Test that the size of the array actually changes
        # It seems to be bad practice to rely on protected data for testing, but
        # it needs to be specifically tested whether or not the true size of the
        # underlying array is actually shrinking when these deletion operations
        # are executed.
        self.assertEqual(len(small_arr._arr), self._GROWTH_FACTOR)
        self.assertEqual(len(medium_arr._arr), self._GROWTH_FACTOR)
        self.assertEqual(len(large_arr._arr), self._GROWTH_FACTOR)

# todo Add additional tests for operators like +
# todo Move tests into separate folder
# todo Use more values than just numbers in the tests


if __name__ == '__main__':
    unittest.main()
