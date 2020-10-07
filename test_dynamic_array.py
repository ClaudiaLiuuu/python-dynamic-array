import unittest
from time import time
from dynamic_array import DynamicArray


class DynamicArrayTestCase(unittest.TestCase):
    @staticmethod
    def time_array_appends(num_elements):
        """Returns average time in seconds of num_elements appends"""
        arr = DynamicArray()
        start_time = time()
        for i in range(num_elements):
            arr.append(i)
        end_time = time()
        return (end_time - start_time) / num_elements

    def setUp(self):
        self.arr = DynamicArray()

    def test_append(self):
        """Test correct placement in array when appending 1,000 numbers"""
        num_elements = 1000
        self.assertEqual(len(self.arr), 0)
        for i in range(num_elements):
            self.arr.append(i)
            self.assertEqual(self.arr[i], i)
        self.assertEqual(len(self.arr), num_elements)

    def test_append_performance(self):
        """Test amortized runtime by comparing 1,000 appends with 1,000,000"""
        avg_small = self.time_array_appends(10)
        avg_medium = self.time_array_appends(1000)
        avg_large = self.time_array_appends(1000000)
        self.assertAlmostEqual(avg_small, avg_medium, delta=0.05)
        self.assertAlmostEqual(avg_small, avg_large, delta=0.05)
        self.assertAlmostEqual(avg_medium, avg_large, delta=0.05)

    def test_extend(self):
        self.assertEqual(True, False)

    def test_insert(self):
        self.assertEqual(True, False)

    def test_remove(self):
        self.assertEqual(True, False)

    def test_pop(self):
        self.assertEqual(True, False)

    def test_clear(self):
        self.assertEqual(True, False)

    def test_index(self):
        self.assertEqual(True, False)

    def test_count(self):
        self.assertEqual(True, False)

    def test_sort(self):
        self.assertEqual(True, False)

    def test_reverse(self):
        self.assertEqual(True, False)

    def test_copy(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
