from abc import ABC, abstractmethod


class BidirectionalCircularIterator:
    def __init__(self, collection_length):
        assert collection_length > 0
        self._collection_length = collection_length
        self._index = 0

    @property
    def current_index(self):
        return self._index

    @property
    def next_index(self):
        return (self._index + 1) % self._collection_length

    @property
    def prev_index(self):
        return (self._index - 1) % self._collection_length

    def next(self):
        self._index = self.next_index

    def prev(self):
        self._index = self.prev_index

    def reset(self):
        self._index = 0


class CircularStruct(ABC):
    def __init__(self, collection):
        self._collection = collection
        self._iterator = BidirectionalCircularIterator(len(self._collection))

    @property
    @abstractmethod
    def current(self):
        pass

    @property
    def _current_index(self):
        return self._iterator.current_index

    @property
    def _next_index(self):
        return self._iterator.next_index

    @property
    def _prev_index(self):
        return self._iterator.prev_index

    def next(self):
        self._iterator.next()
        return self.current

    def prev(self):
        self._iterator.prev()
        return self.current


class CircularList(CircularStruct):
    def __init__(self, collection: list):
        super().__init__(collection)

    @property
    def collection(self):
        return self._collection

    @property
    def current(self):
        return self.collection[self._current_index]

    @property
    def next_item(self):
        return self._collection[self._next_index]

    @property
    def prev_item(self):
        return self._collection[self._prev_index]

