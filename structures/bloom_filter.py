"""
Skeleton for COMP3506/7505 A2, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov
"""
import math
from structures.entry import Entry
from typing import Any
from structures.util import object_to_byte_array
from structures.bit_vector import BitVector

class BloomFilter:
    """
    A BloomFilter uses a BitVector as a container. To insert a given key, we
    hash the key using a series of h unique hash functions to set h bits.
    Looking up a given key follows the same logic, but only checks if all
    bits are set or not.

    Note that a BloomFilter is considered static. It is initialized with the
    number of total keys desired (as a parameter) and will not grow. You
    must decide what this means in terms of allocating your bitvector space
    accordingly.

    You can add functions if you need to.

    *** A NOTE ON KEYS ***
    We will only ever use int or str keys.
    We will not use `None` as a key.
    You might like to look at the `object_to_byte_array` function
    stored in util.py -- This function can be used to convert a string
    or integer key into a byte array, and then you can use the byte array
    to make your own hash function (bytes are just integers in the range
    [0-255] of course).
    """

    FP_RATE = 0.02

    def __init__(self, max_keys: int) -> None:
        # You should use max_keys to decide how many bits your bitvector
        # should have, and allocate it accordingly.
        self._data = BitVector()
        self._data.allocate(self.calculate_bit_array_size(max_keys, self.FP_RATE))         
        # More variables here if you need, of course
        self._hashes = min(8, int((self._data.get_size() / max_keys) * math.log(2)))    

    def __str__(self) -> str:
        """
        A helper that allows you to print a BloomFilter type
        via the str() method.
        This is not marked. <<<<
        """
        pass

    def insert(self, key: Any) -> None:
        """
        Insert a key into the Bloom filter.
        Time complexity for full marks: O(1)
        """
        for i in range(self._hashes):
            index = self.get_hash(key, i)
            self._data.set_at(index)

    def contains(self, key: Any) -> bool:
        """
        Returns True if all bits associated with the h unique hash functions
        over k are set. False otherwise.
        Time complexity for full marks: O(1)
        """
        return all(self._data.get_at(self.get_hash(key, i)) == 1 
                   for i in range(self._hashes))

    def __contains__(self, key: Any) -> bool:
        """
        Same as contains, but lets us do magic like:
        `if key in my_bloom_filter:`
        Time complexity for full marks: O(1)
        """
        return self.contains(key)

    def is_empty(self) -> bool:
        """
        Boolean helper to tell us if the structure is empty or not
        Time complexity for full marks: O(1)
        """
        for i in range(self._data.get_size()):
            if self._data.get_at(i) == 1:
                return False
        return True

    def get_capacity(self) -> int:
        """
        Return the total capacity (the number of bits) that the underlying
        BitVector can currently maintain.
        Time complexity for full marks: O(1)
        """
        return self._data.get_size()

    def hash1(self, key: Any) -> int:
        byte_array = object_to_byte_array(key)
        h = 5381
        for byte in byte_array:
            h = ((h << 5) + h) + byte
        return h & 0xFFFFFFFF

    def hash2(self, key: Any) -> int:
        byte_array = object_to_byte_array(key)
        h = 0
        for byte in byte_array:
            h = (h * 31 + byte) & 0xFFFFFFFF
        return h | 1  # Ensure it's odd for better distribution in double hashing
    
    def get_hash(self, key: Any, index: int) -> int:
        h1 = self.hash1(key)
        h2 = self.hash2(key)
        return (h1 + index * h2) % self._data.get_size()
    
    def calculate_bit_array_size(self, n: int, p: float) -> int:
        m = -(n * math.log(p)) / (math.log(2)**2)
        return int(m)

