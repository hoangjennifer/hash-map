# Implements a hash map using separate chaining.


from include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        capacity when the current load factor of table is greater than or equal to 1.0.
        """
        # Statement, check if the load factor is greater than or equal to 1.0, if so, resize to double its current capacity.
        if self.table_load() >= 1.0:
            self.resize_table(2 * self._capacity)

        # Initialize index, bucket and hash key.
        index = self._hash_function(key) % self._buckets.length()
        bucket = self._buckets.get_at_index(index)
        cur = bucket.contains(key)

        # Statement, check if key exists.  If so, replace its associated value.  If not, insert value and increment size.
        if cur != None:
            cur.value = value
        else:
            bucket.insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        Method returns number of empty buckets in hash table.
        """
        # Initialize counter.  Loop hash map, check if buckets are empty, if so, increment counter.  Return counter.
        counter = 0
        for i in range(self._capacity):
            if self._buckets.get_at_index(i).length() == 0:
                counter += 1
        return counter

    def table_load(self) -> float:
        """
        Method returns current hash table load factor.
        """
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Method clears contents of hash map.  It doesn't change underlying hash table capacity.
        """
        # Loop array, clear hash map and update size.
        for i in range(self._capacity):
            self._buckets.set_at_index(i, LinkedList())
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Method changes capacity of internal hash table.  All existing key/value pairs remain in new hash map and all hash table
        links are rehashed.  First, check that new_capacity is not less than 1, if so, method does nothing.  If new_capacity
        is 1 or more, check that it's a prime number.  If not, change it to next highest prime number.
        """
        # Statement, check if capacity is less than 1, if so, do nothing.
        if new_capacity < 1:
            return

        # Statement, check if capacity is a prime number, if not, change it to next highest prime number.
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Initialize current buckets, length of buckets, size as zero, capacity as new capacity and new array.
        curBuckets = self._buckets
        curBucketsLen = self._capacity
        self._size = 0
        self._capacity = new_capacity
        self._buckets = DynamicArray()

        # Loop array, add values to linked list.
        for i in range(new_capacity):
            self._buckets.append(LinkedList())

        # Move current data to new buckets with bigger capacity.
        for i in range(curBucketsLen):
            cur = curBuckets.get_at_index(i)
            if cur != None:
                for node in cur:
                    self.put(node.key, node.value)

    def get(self, key: str):
        """
        Method returns value associated with given key.  If key isn't in hash map, method returns None.
        """
        # Initialize index.  Statement, check if hash map contains key.  If so, return value.  Otherwise, return None.
        index = self._hash_function(key) % self._capacity
        if self._buckets.get_at_index(index).contains(key):
            return self._buckets.get_at_index(index).contains(key).value
        else:
            return None

    def contains_key(self, key: str) -> bool:
        """
        Method returns True if given key is in hash map, otherwise returns False.  An empty hash doesn't contain any keys.
        """
        # Initialize index.  Statement, check if hash map contains key.  If so, return True.  Otherwise, return False.
        index = self._hash_function(key) % self._capacity
        if self._buckets.get_at_index(index).contains(key):
            return True
        return False

    def remove(self, key: str) -> None:
        """
        Method removes given key and its associated value from hash map.  If key isn't in hash map, method does nothing.
        """
        # Initialize index.  Statement, check if hash map contains key.  If so, remove key and decrement size.
        index = self._hash_function(key) % self._capacity
        if self._buckets.get_at_index(index).contains(key):
            self._buckets.get_at_index(index).remove(key)
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Method returns a dynamic array where each index contains a tuple of a key/value pair stored in hash map.  Order of keys in
        array do not matter.
        """
        # Initialize new array.  Loop array, check if a key exists, if so, then add to new array as tuple.  Return new array.
        NewArray = DynamicArray()
        for i in range(self._capacity):
            cur = self._buckets.get_at_index(i)
            if cur != None:
                for node in cur:
                    NewArray.append((node.key, node.value))
        return NewArray


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Standalone function outside of HashMap class that receives a dynamic array, not guaranteed to be sorted.  Function returns a
    tuple containing, in this order, a dynamic array comprising the mode (most occurring) value/s of array and an integer that
    represents highest frequency (how many times they appear).  If there is more than one value with highest frequency, all values
    at that frequency are included in array being returned, order doesn't matter.  It there is only one mode, dynamic array will
    only contain that value.  Assume that input array contains at least one element and that all values stored in array will be
    strings.  No checks needed.  It's implemented with O(N) time complexity.
    """
    # Initialize array and frequency counter.  Statement, check if array has the key.  If so, update value in map.  If not, insert.
    map = HashMap()
    frequency = 0
    for i in range(da.length()):
        key = da.get_at_index(i)
        if map.contains_key(key):
            map.put(key, map.get(key) + 1)
        else:
            map.put(key, 1)

    # Initialize keys and values.  Statement, check each key/value pair.  If valuee is greater than frequency, then update frequency.
    keysValues = map.get_keys_and_values()
    for i in range(keysValues.length()):
        key, value = keysValues.get_at_index(i)
        if value > frequency:
            frequency = value

    # Initialize mode.  Statement, check if value is equal to frequency.  If so, append and return mode and frequency.
    mode = DynamicArray()
    for i in range(keysValues.length()):
        key, value = keysValues.get_at_index(i)
        if value == frequency:
            mode.append(key)
    return mode, frequency

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
    m = HashMap(53, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
