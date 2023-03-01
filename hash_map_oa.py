# Implements a hash map using open addressing.

from include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Method updates key/value pair in hash map.  If given key already exists in hash map, associated value is replaced with new
        value.  If given key is not in hash map, new key/value pair is added.  The table is also resized to double its current
        capacity when the current load factor of table is greater than or equal to 0.5.
        """
        # Statement, check if the load factor is greater than or equal to 1.0, if so, resize to double its current capacity.
        if self.table_load() >= 0.5:
            self.resize_table(2 * self._capacity)

        # Initialize index and i^2'th slot in the i'th iteration for quadratic probing.
        index = self._hash_function(key) % self._capacity
        i = 0

        # Loop while boolean is True.  Initialize element in bucket.  Statement, check for bucket in index.  Statement, check if key
        # exists.  If so, replace value in key.  If it's a hash entry, update to False, increment size and return.  If key not
        # found, update i^2'th slot by adding one and index.  If index not found, add value, increment size and return.
        while True:
            bucketElement = self._buckets.get_at_index(index)
            if bucketElement:
                if bucketElement.key == key:
                    self._buckets.set_at_index(index, HashEntry(key, value))
                    if bucketElement.is_tombstone:
                        self._buckets.get_at_index(index).is_tombstone = False
                        self._size += 1
                    return
                i = i + 1
                index = (self._hash_function(key) + i * i) % self._capacity
            else:
                self._buckets.set_at_index(index, HashEntry(key, value))
                self._size += 1
                return

    def table_load(self) -> float:
        """
        Method returns current hash table load factor.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Method returns number of empty buckets in hash table.
        """
        # Initialize difference and return difference.
        difference = self._capacity - self._size
        return difference

    def resize_table(self, new_capacity: int) -> None:
        """
        Method changes capacity of internal hash table.  All existing key/value pairs remain in new hash map and all hash table
        links are rehashed.  First, check that new_capacity is not less than size, if so, method does nothing.  If new_capacity
        is valid, check that it's a prime number.  If not, change it to next highest prime number.
        """
        # Statement, check if capacity is less than size, if so, do nothing.
        if new_capacity < self._size:
            return

        # Statement, check if capacity is a prime number, if not, change it to next highest prime number.
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Initialize current buckets, length of buckets, size as zero, capacity as new capacity and new array.  Loop capacity as
        # placeholder.
        curBuckets = self._buckets
        curBucketsLen = self._capacity
        self._size = 0
        self._capacity = new_capacity
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(None)

        # Loop hash map.  Statement, check if current index value and boolean is false, then move current data to new array with
        # bigger capacity.
        for i in range(curBucketsLen):
            if curBuckets.get_at_index(i) and (curBuckets.get_at_index(i).is_tombstone is False):
                self.put(curBuckets.get_at_index(i).key, curBuckets.get_at_index(i).value)

    def get(self, key: str) -> object:
        """
        Method returns value associated with given key.  If key isn't in hash map, method returns None.
        """
        # Initialize index and i^2'th slot in the i'th iteration.
        index = self._hash_function(key) % self._capacity
        i = 0

        # Loop while boolean is True.  Initialize element in bucket.  Statement, check for bucket in index.  Statement, check if key
        # exists.  If it's a hash entry, return None.  Otherwise, return value.  If key not found, update i^2'th slot by adding one
        # and index.  If index not found, return None.
        while True:
            bucketElement = self._buckets.get_at_index(index)
            if bucketElement:
                if bucketElement.key == key:
                    if bucketElement.is_tombstone:
                        return None
                    return bucketElement.value
                else:
                    i = i + 1
                    index = (self._hash_function(key) + i * i) % self._capacity
            else:
                return None

    def contains_key(self, key: str) -> bool:
        """
        Method returns True if given key is in hash map, otherwise returns False.  An empty hash doesn't contain any keys.
        """
        # Initialize index and i^2'th slot in the i'th iteration.
        index = self._hash_function(key) % self._capacity
        i = 0

        # Loop while boolean is True.  Initialize element in bucket.  Statement, check for bucket in index.  Statement, check if key
        # exists, then return true.  If key not found, update i^2'th slot by adding one and index.  If index not found, return false.
        while True:
            bucketElement = self._buckets.get_at_index(index)
            if bucketElement:
                if bucketElement.key == key:
                    return True
                else:
                    i = i + 1
                    index = (self._hash_function(key) + i * i) % self._capacity
            else:
                return False

    def remove(self, key: str) -> None:
        """
        Method removes given key and its associated value from hash map.  If key isn't in hash map, method does nothing.
        """
        # Initialize index and i^2'th slot in the i'th iteration.
        index = self._hash_function(key) % self._capacity
        i = 0

        # Loop while boolean is True.  Initialize element in bucket.  Statement, check for bucket in index.  Statement, check if key
        # exists.  If it's a hash entry, return.  Otherwise, update to true, decrement size and return.  If key not found, update
        # i^2'th slot by adding one and index.  If index not found, return.
        while True:
            bucketElement = self._buckets.get_at_index(index)
            if bucketElement:
                if bucketElement.key == key:
                    if self._buckets.get_at_index(index).is_tombstone:
                        return
                    self._buckets.get_at_index(index).is_tombstone = True
                    self._size -= 1
                    return
                else:
                    i = i + 1
                    index = (self._hash_function(key) + i * i) % self._capacity
            else:
                return

    def clear(self) -> None:
        """
        Method clears contents of hash map.  It doesn't change underlying hash table capacity.
        """
        # Loop capacity, clear hash map and update size.
        for i in range(self._capacity):
            self._buckets.set_at_index(i, None)
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Method returns a dynamic array where each index contains a tuple of a key/value pair stored in hash map.  Order of keys in
        array do not matter.
        """
        # Initialize new array.  Loop capacity, initialize current value.  Statement, check if a key exists, if so, then add to new
        # array as tuple.  Return new array.
        NewArray = DynamicArray()
        for i in range(self._capacity):
            cur = self._buckets.get_at_index(i)
            if cur != None and cur.is_tombstone is False:
                NewArray.append((cur.key, cur.value))
        return NewArray

    def __iter__(self):
        """
        Method enables hash map to iterate across itself.
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Method returns next item in hash map based on current location of iterator.  It only iterates over active items.
        """
        # Loop while index is less than length.  Statement, check that value exists in current index.  If so, increment index and
        # return value in index.  Otherwise, increment index.  Raise StopIteration to signal iteration is done.
        while self._index < self._buckets.length():
            if self._buckets[self._index] is not None:
                self._index += 1
                return self._buckets[self._index - 1]
            self._index += 1
        raise StopIteration

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
