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
        self._size = self.calculate_bit_array_size(max_keys, self.FP_RATE)
        self._data = BitVector()
        self._data.allocate(self._size)
        # More variables here if you need, of course
        calculated_hashes = int((self._size / max_keys) * math.log(2))
        if calculated_hashes > 8:
            self._hashes = 8
        else:
            self._hashes = calculated_hashes
        self._size_mask = self._size - 1  
 
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
        h1, h2 = self._get_hash_pair(key)
        for i in range(self._hashes):
            index = (h1 + i * h2) & self._size_mask
            self._data.set_at(index)

    def contains(self, key: Any) -> bool:
        """
        Returns True if all bits associated with the h unique hash functions
        over k are set. False otherwise.
        Time complexity for full marks: O(1)
        """
        h1, h2 = self._get_hash_pair(key)
        return all(self._data.get_at((h1 + i * h2) & self._size_mask) == 1 
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
        for i in range(self._size):
            if self._data.get_at(i) == 1:
                return False
        return True

    def get_capacity(self) -> int:
        """
        Return the total capacity (the number of bits) that the underlying
        BitVector can currently maintain.
        Time complexity for full marks: O(1)
        """
        return self._size

    def _hash1(self, byte_array: bytes) -> int:
        h = 5381
        for byte in byte_array:
            h = ((h << 5) + h + byte) & self._size_mask
        return h

    def _hash2(self, byte_array: bytes) -> int:
        h = 0
        for byte in byte_array:
            h = (h * 31 + byte) & self._size_mask
        return (h | 1) & self._size_mask
    
    @staticmethod
    def calculate_bit_array_size(n: int, p: float) -> int:
        m = -(n * math.log(p)) / (math.log(2)**2)
        calculated_size = 1 << math.ceil(math.log2(m))
        if calculated_size < 256:
            return 256
        return calculated_size
    
    def _get_hash_pair(self, key: Any) -> tuple[int, int]:
        byte_array = object_to_byte_array(key)
        h1 = self._hash1(byte_array)
        h2 = self._hash2(byte_array)
        return h1, h2

