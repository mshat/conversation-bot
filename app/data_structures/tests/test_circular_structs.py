import unittest
from ..circular_structs import CircularList


class CircularListTest(unittest.TestCase):
    def test_current(self):
        nums_list = [1, 2, 3, 4]

        circular_nums = CircularList(nums_list)

        self.assertEqual(1, circular_nums.current)

    def test_collection_property(self):
        nums_list = [1, 2, 3, 4]

        circular_nums = CircularList(nums_list)

        self.assertEqual(nums_list, circular_nums.collection)

    def test_next_item_property(self):
        nums_list = [1, 2, 3, 4]

        circular_nums = CircularList(nums_list)

        self.assertEqual(2, circular_nums.next_item)

    def test_prev_item_property(self):
        nums_list = [1, 2, 3, 4]

        circular_nums = CircularList(nums_list)

        self.assertEqual(4, circular_nums.prev_item)

    def test_get_next_item_index_without_changing_current(self):
        nums_list = [1, 2, 3, 4]

        circular_nums = CircularList(nums_list)

        self.assertEqual(2, circular_nums.next_item)
        self.assertEqual(1, circular_nums.current)

    def test_get_prev_item_index_without_changing_current(self):
        nums_list = [1, 2, 3, 4]

        circular_nums = CircularList(nums_list)

        self.assertEqual(4, circular_nums.prev_item)
        self.assertEqual(1, circular_nums.current)

    def test_change_current_to_next_item(self):
        nums_list = [1, 2, 3, 4]
        circular_nums = CircularList(nums_list)

        circular_nums.next()

        self.assertEqual(2, circular_nums.current)

    def test_change_current_to_prev_item(self):
        nums_list = [1, 2, 3, 4]
        circular_nums = CircularList(nums_list)

        circular_nums.prev()

        self.assertEqual(4, circular_nums.current)

    def test_change_current_to_full_circle_item_use_next(self):
        nums_list = [1, 2, 3, 4]
        circular_nums = CircularList(nums_list)

        for i in range(len(nums_list)):
            circular_nums.next()

        self.assertEqual(1, circular_nums.current)

    def test_change_current_to_full_circle_item_use_prev(self):
        nums_list = [1, 2, 3, 4]
        circular_nums = CircularList(nums_list)

        for i in range(len(nums_list)):
            circular_nums.prev()

        self.assertEqual(1, circular_nums.current)

    def test_change_current_to_full_circle_plus_one_item(self):
        nums_list = [1, 2, 3, 4]
        circular_nums = CircularList(nums_list)

        for i in range(len(nums_list) + 1):
            circular_nums.next()

        self.assertEqual(2, circular_nums.current)

