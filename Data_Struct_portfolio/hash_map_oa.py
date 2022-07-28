# Name: Derek Gilmartin
# OSU Email: gilmartd@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6 HashMaps
# Due Date: 6/3/2022
# Description: Hash map creation, and methods to manipulate it. Two part assignment, Open Assignment and Chaining for
# collision resolution


from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(None)

        self._capacity = capacity
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

    # ----------CODE ABOVE THIS LINE PROVIDED BY INSTRUCTOR-------------------------------------------------------- #

    def put(self, key: str, value: object) -> None:
        """
        Adds a value to the hash-map or replaces a value if the key already exists
        """
        # remember, if the load factor is greater than or equal to 0.5,
        # resize the table before putting the new key/value pair
        if self.table_load() >= .5:
            self.resize_table(2*self._capacity)
        pair = HashEntry(key, value)
        bucket = self._hash_function(key) % self._capacity
        i = 1
        while self._buckets[bucket] is not None:
            if self._buckets[bucket].is_tombstone is True:
                break
            elif self._buckets[bucket].key == key:
                if self._buckets[bucket].is_tombstone is False:
                    self._size -=1
                    break
            else:
                bucket = (self._hash_function(key) + i*i) % self._capacity
                i += 1
        self._buckets[bucket] = pair
        self._size += 1

    def table_load(self) -> float:
        """
        Returns the hash table load factor (load = number of elements/number of buckets)
        """
        return self._size/self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hashmap
        """
        empty = 0
        for bucket in range(self._buckets.length()):
            if self._buckets[bucket] is None:
                empty += 1
        return empty

    def resize_table(self, new_capacity: int) -> None:
        """
        Creates a larger hash map, copies keys and updates their "position" in the new hash map, then points the original
        labels to the new map
        """
        # remember to rehash non-deleted entries into new table
        if new_capacity < 1:
            return
        if new_capacity < self._size:
            return
        new_map = HashMap(new_capacity, self._hash_function)
        new_map._buckets = DynamicArray()
        for _ in range(new_capacity):
            new_map._buckets.append(None)
        for i in range (self._buckets.length()):
            if self._buckets[i] is not None:
                if self._buckets[i].is_tombstone is False:
                    new_map.put(self._buckets[i].key, self._buckets[i].value)
        self._buckets = new_map._buckets
        self._size = new_map._size
        self._capacity = new_map._capacity


    def get(self, key: str) -> object:
        """
        returns a value associated with a given key if it exists in the map
        """
        bucket = self._hash_function(key) % self._capacity
        for i in range(self._buckets.length()):
            if self._buckets[bucket] is None:
                return None
            elif self._buckets[bucket].key == key:
                if self._buckets[bucket].is_tombstone is False:
                    return self._buckets[bucket].value
            else:
                bucket = (self._hash_function(key) + i*i) % self._capacity

    def contains_key(self, key: str) -> bool:
        """
        Returns True if a key exists in the map
        """
        if self._size == 0:
            return False
        bucket = self._hash_function(key) % self._capacity
        for i in range(self._buckets.length()):
            if self._buckets[bucket] is None:
                return False
            elif self._buckets[bucket].key == key:
                if self._buckets[bucket].is_tombstone is False:
                    return True
            else:
                bucket = (self._hash_function(key) + i*i) % self._capacity

    def remove(self, key: str) -> None:
        """
        Removes a key-value pair from the buckets array and replaces it with the value '_TS_'
        """
        bucket = self._hash_function(key) % self._capacity
        for i in range(self._buckets.length()):
            if self._buckets[bucket] is None:
                return
            elif self._buckets[bucket].key == key:
                if self._buckets[bucket].is_tombstone is False:
                    self._buckets[bucket].is_tombstone = True
                    self._size -=1
            else:
                bucket = (self._hash_function(key) + i*i) % self._capacity

    def clear(self) -> None:
        """
        Clears the hashmap but preserves the capacity of the original array
        """
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(None)
        self._size = 0

    def get_keys(self) -> DynamicArray:
        """
        Returns a dynamic array of all the keys in the hashmap
        """
        keys_array = DynamicArray()
        for i in range(self._buckets.length()):
            if self._buckets[i] is not None:
                if self._buckets[i].is_tombstone is False:
                    keys_array.append(self._buckets[i].key)
        return keys_array

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
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
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() >= 0.5:
            print("Check that capacity gets updated during resize(); "
                  "don't wait until the next put()")

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
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
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
    m = HashMap(75, hash_function_2)
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
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
