from data_structures.circular_structs import CircularStruct


class StateIndexException(Exception): pass


class StateIndex(CircularStruct):
    def __init__(self, states: list):
        super().__init__(states)
        self._indexed_states = {i: state for i, state in enumerate(self._collection)}
        self._states_indexes = {state: index for index, state in self._indexed_states.items()}

    @property
    def collection(self):
        return self._collection

    @property
    def states(self):
        return self._states_indexes

    @property
    def current_state_name(self):
        return self._indexed_states[self._iterator.current_index]

    @property
    def current(self):
        return self._iterator.current_index

    @property
    def next_state(self):
        return self._indexed_states[self._iterator.next_index]

    @property
    def prev_state(self):
        return self._indexed_states[self._iterator.prev_index]

    def get_state(self, name):
        if name in self._states_indexes.keys():
            index = self._states_indexes[name]
        else:
            raise StateIndexException('There is no such state in the list of state!')
        return index

    def reset_state(self):
        self._iterator.reset()
