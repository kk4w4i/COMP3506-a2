"""
Skeleton for COMP3506/7505 A2, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov

Please read the following carefully. This file is used to implement a Map
class which supports efficient insertions, accesses, and deletions of
elements.

There is an Entry type defined in entry.py which *must* be used in your
map interface. The Entry is a very simple class that stores keys and values.
The special reason we make you use Entry types is because Entry extends the
Hashable class in util.py - by extending Hashable, you must implement
and use the `get_hash()` method inside Entry if you wish to use hashing to
implement your map. We *will* be assuming Entry types are used in your Map
implementation.
Note that if you opt to not use hashing, then you can simply override the
get_hash function to return -1 for example.
"""

from typing import Any
from structures.entry import Entry
from structures.dynamic_array import DynamicArray

class Map:
    """
    An implementation of the Map ADT.
    The provided methods consume keys and values via the Entry type.
    """

    def __init__(self) -> None:
        """
        Construct the map.
        You are free to make any changes you find suitable in this function
        to initialise your map.
        """
        self.table = [None] * 128
        self.size = 0
        self.capacity = 128

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [[None] * self.capacity]
        self.size = 0
        for bucket in old_table:
            if bucket:
                for i in range(bucket.get_size()):
                    entry = bucket[i]
                    self.insert(entry)
        

    def insert(self, entry: Entry) -> Any | None:
        """
        Associate value v with key k for efficient lookups. If k already exists
        in your map, you must return the old value associated with k. Return
        None otherwise. (We will not use None as a key or a value in our tests).
        Time complexity for full marks: O(1*)
        """
        if self.size / self.capacity > 0.75:
            self._resize()

        index = self._hash(entry.get_key())
        if self.table[index] is None:
            self.table[index] = DynamicArray()
        else:
            bucket = self.table[index]
            for i in range(bucket.get_size()):
                exist_entry = bucket[i]
                if exist_entry == entry:
                    old_value = exist_entry.get_value()
                    exist_entry.update_value(entry.get_value())
                    return old_value
        self.table[index].append(entry)
        self.size += 1
        return None

    def insert_kv(self, key: Any, value: Any) -> Any | None:
        """
        A version of insert which takes a key and value explicitly.
        Handy if you wish to provide keys and values directly to the insert
        function. It will return the value returned by insert, so keep this
        in mind. You can modify this if you want, as long as it behaves.
        Time complexity for full marks: O(1*)
        """
        #hint: entry = Entry(key, value)
        return self.insert(Entry(key, value))

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        For convenience, you may wish to use this as an alternative
        for insert as well. However, this version does _not_ return
        anything. Can be used like: my_map[some_key] = some_value
        Time complexity for full marks: O(1*)
        """
        self.insert_kv(key, value)

    def remove(self, key: Any) -> None:
        """
        Remove the key/value pair corresponding to key k from the
        data structure. Don't return anything.
        Time complexity for full marks: O(1*)
        """
        index = self._hash(key)
        if self.table[index]:
            bucket = self.table[index]
            for i in range(bucket.get_size()):
                entry = bucket[i]
                if entry.get_key() == key:
                    self.table[index].remove_at(i)
                    self.size -= 1
                    return

    def find(self, key: Any) -> Any | None:
        """
        Find and return the value v corresponding to key k if it
        exists; return None otherwise.
        Time complexity for full marks: O(1*)
        """
        index = self._hash(key)
        if self.table[index] != None:
            bucket = self.table[index]
            for i in range(bucket.get_size()):
                    entry = bucket[i]
                    if entry.get_key() == key:
                        return entry.get_value()
        return None

    def __getitem__(self, key: Any) -> Any | None:
        """
        For convenience, you may wish to use this as an alternative
        for find()
        Time complexity for full marks: O(1*)
        """
        return self.find(key)

    def get_size(self) -> int:
        """
        Time complexity for full marks: O(1)
        """
        return self.size

    def is_empty(self) -> bool:
        """
        Time complexity for full marks: O(1)
        """
        return self.size == 0

    def _hash(self, key: Any) -> int:
        temp_entry = Entry(key, None)
        return temp_entry.get_hash() % self.capacity
    
    def __str__(self):
        result = []
        for bucket in self.table:
            if bucket:
                for i in range(bucket.get_size()):
                    entry = bucket[i]
                    result.append(f"'{entry.get_key()}': {entry.get_value()}")
        return "{" + ", ".join(result) + "}"

