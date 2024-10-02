"""
Skeleton for COMP3506/7505 A2, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov
"""

from typing import Any
from structures.entry import Entry
from structures.dynamic_array import DynamicArray

class PriorityQueue:
    """
    An implementation of the PriorityQueue ADT. We have used the implicit
    tree method: an array stores the data, and we use the heap shape property
    to directly index children/parents.

    The provided methods consume keys and values. Keys are called "priorities"
    and should be comparable numeric values; smaller numbers have higher
    priorities.
    Values are called "data" and store the payload data of interest.
    We use the Entry types to store (k, v) pairs.
    """
    
    def __init__(self):
        """
        Empty construction
        """
        self._arr = DynamicArray()
        self._max_priority = 0
        self._min_cache = None

    def _parent(self, ix: int) -> int:
        """
        Given index ix, return the index of the parent
        """
        return (ix) // 2

    def insert(self, priority: int, data: Any) -> None:
        """
        Insert some data to the queue with a given priority.
        """
        new = Entry(priority, data)
        self._arr.append(new)
        self._sift_up(self._arr.get_size() - 1)
        
        if priority > self._max_priority:
            self._max_priority = priority
        
        if self._min_cache is None or priority < self._min_cache.get_key():
            self._min_cache = new
        
        #update max priority if incoming priority is the maximum
        if priority > self._max_priority:
            self._max_priority = priority

    def insert_fifo(self, data: Any) -> None:
        """
        Insert some data to the queue in FIFO mode. Note that a user
        should never mix `insert` and `insert_fifo` calls, and we assume
        that nobody is silly enough to do this (we do not test this).
        """
        self.insert(self._max_priority, data)
        self._max_priority += 1

    def get_min_priority(self) -> Any:
        """
        Return the priority of the min element
        """
        if self.is_empty():
            return None
        return self._min_cache.get_key()

    def get_min_value(self) -> Any:
        """
        Return the highest priority value from the queue, but do not remove it
        """
        if self.is_empty():
            return None
        return self._min_cache.get_value()

    def remove_min(self) -> Any:
        """
        Extract (remove) the highest priority value from the queue.
        You must then maintain the queue to ensure priority order.
        """
        if self.is_empty():
            return None
        
        result = self._min_cache.get_value()
        last_item = self._arr[self._arr.get_size() - 1]
        self._arr.remove_at(self._arr.get_size() - 1)
        
        if not self.is_empty():
            self._arr[0] = last_item
            self._sift_down(0)
            self._min_cache = self._arr[0]
        else:
            self._min_cache = None
        
        return result

    def get_size(self) -> int:
        """
        Does what it says on the tin
        """
        return self._arr.get_size()

    def is_empty(self) -> bool:
        """
        Ditto above
        """
        return self._arr.is_empty()

    def ip_build(self, input_list: DynamicArray) -> None:
        """
        Take ownership of the list of Entry types, and build a heap
        in-place. That is, turn input_list into a heap, and store it
        inside the self._arr as a DynamicArray. You might like to
        use the DynamicArray build_from_list function. You must use
        only O(1) extra space.
        """
        self._arr = input_list
        size = self._arr.get_size()

        for i in range(size // 2 - 1, -1, -1):
            self._sift_down(i)

        self._min_cache = self._arr[0] if not self.is_empty() else None

        for i in range(self._arr.get_size()):
            if self._arr[i]:
                self._max_priority = max(self._max_priority, self._arr[i].get_key())

    def sort(self) -> DynamicArray:
        """
        Use HEAPSORT to sort the heap being maintained in self._arr, using
        self._arr to store the output (in-place). You must use only O(1)
        extra space. Once sorted, return self._arr (the DynamicArray of
        Entry types).

        Once this sort function is called, the heap can be considered as
        destroyed and will not be used again (hence returning the underlying
        array back to the caller).
        """
        n = self._arr.get_size()

        for i in range(n - 1, 0, -1):
            self._arr[0], self._arr[i] = self._arr[i], self._arr[0]
            self._sift_down_bounded(0, i)

        return self._arr
    
    def get_arrary(self) -> DynamicArray:
        return self._arr
    
    def _sift_down_bounded(self, index: int, size: int) -> None:
        while True:
            smallest = index
            left = 2 * index + 1
            right = 2 * index + 2
            
            if left < size and self._arr[left].get_key() < self._arr[smallest].get_key():
                smallest = left
            if right < size and self._arr[right].get_key() < self._arr[smallest].get_key():
                smallest = right
            
            if smallest == index:
                break
            
            self._arr[index], self._arr[smallest] = self._arr[smallest], self._arr[index]
            index = smallest
    
    def _sift_up(self, index: int) -> None:
        while index > 0:
            parent = self._parent(index)
            if self._arr[index].get_key() < self._arr[parent].get_key():
                self._arr[index], self._arr[parent] = self._arr[parent], self._arr[index]
                index = parent
            else:
                break

    def _sift_down(self, index: int) -> None:
        size = self._arr.get_size()
        while True:
            smallest = index
            left = 2 * index + 1
            right = 2 * index + 2
            
            if left < size and self._arr[left].get_key() < self._arr[smallest].get_key():
                smallest = left
            if right < size and self._arr[right].get_key() < self._arr[smallest].get_key():
                smallest = right
            
            if smallest == index:
                break
            
            self._arr[index], self._arr[smallest] = self._arr[smallest], self._arr[index]
            index = smallest