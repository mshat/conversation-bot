import sys
import unittest
sys.path.append("..")
from tools.state_index import StateIndex


class CircularListTest(unittest.TestCase):
    def test_current_state(self):
        state_list = ['STEP1', 'STEP2', 'STEP3', 'STEP4']

        state = StateIndex(state_list)

        self.assertEqual(0, state.current)

    def test_current_state_name(self):
        state_list = ['STEP1', 'STEP2', 'STEP3', 'STEP4']

        state = StateIndex(state_list)

        self.assertEqual(state_list[0], state.current_state_name)

    def test_change_current_to_next_item(self):
        state_list = ['STEP1', 'STEP2', 'STEP3', 'STEP4']
        state = StateIndex(state_list)

        state.next()

        self.assertEqual(1, state.current)

    def test_change_current_to_prev_item(self):
        state_list = ['STEP1', 'STEP2', 'STEP3', 'STEP4']
        state = StateIndex(state_list)

        state.prev()

        self.assertEqual(3, state.current)
