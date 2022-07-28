# Name: Derek Gilmartin
# OSU Email: gilmartd@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6 HashMaps
# Due Date: 6/3/2022
# Description: Hash map creation, and methods to manipulate it. Two part assignment, Open Assignment and Chaining for
# collision resolution


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(LinkedList())

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

    # --------------CODE ABOVE THIS LINE WAS PROVIDED BY THE ISNTRUCTOR---------------------------------------------------- #

    def put(self, key: str, value: object) -> None:
        """
        Adds a value to the hash-map or replaces a value if the key already exists
        """
        bucket = self._hash_function(key) % self._capacity  # finds index of the dynamic array
        node = self._buckets[bucket].contains(key)          # .contains returns the node if it exists, or None if not
        if node is not None:
            node.value = value
        else:
            self._buckets[bucket].insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table
        """
        empty = 0
        for bucket in range(self._buckets.length()):
            if self._buckets[bucket].length() == 0:
                empty += 1
        return empty

    def table_load(self) -> float:
        """
        Returns the hash table load factor (load = number of elements/number of buckets)
        """
        return self._size/self._capacity

    def clear(self) -> None:
        """
        Empties the HashMap but does not change capacity
        """
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Creates a larger hash map, copies keys and updates their "position" in the new hash map, then points the original
        labels to the new map
        """
        if new_capacity <1:
            return
        new_map = HashMap(new_capacity, self._hash_function)
        new_map._buckets = DynamicArray()
        for i in range(new_capacity):
            new_map._buckets.append(LinkedList())
        # There is now an empty da of correct capacity but no key/value pairs inserted yet
        for i in range(self._buckets.length()):
            for i in self._buckets[i]:          #uses iterator to iterate through the links in the SLL of each index
                key = i.key
                value = i.value
                new_map.put(key,value)
        self._buckets = new_map._buckets        #copies the new dynamic array attributes into self
        self._size= new_map._size
        self._capacity = new_map._capacity


    def get(self, key: str) -> object:
        """
        returns a value associated with a given key if it exists in the map
        """
        bucket = self._hash_function(key) % self._capacity
        node = self._buckets[bucket].contains(key)
        if node is not None:
            return node.value
        else:
            return

    def contains_key(self, key: str) -> bool:
        """
        Returns True if a key exists in the map
        """
        if key is None:
            return
        bucket = self._hash_function(key) % self._capacity
        node = self._buckets[bucket].contains(key)
        if node is not None:
            return True
        else:
            return False

    def remove(self, key: str) -> None:
        """
        Removes a key-value pair form the hash map
        """
        bucket = self._hash_function(key) % self._capacity
        node = self._buckets[bucket].contains(key)
        if node is not None:
            self._buckets[bucket].remove(key)
            self._size-=1


    def get_keys(self) -> DynamicArray:
        """
        returns an array of all the key values in the hashmap
        """
        keys = DynamicArray()
        for i in range(self._buckets.length()):
            for i in self._buckets[i]:
                keys.append(i.key)
        return keys

    def get_node(self, key: str) -> object:
        """
        returns a node associated with a given key if it exists in the map
        """
        bucket = self._hash_function(key) % self._capacity
        node = self._buckets[bucket].contains(key)
        if node is not None:
            return node
        else:
            return



def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Finds the mode of the array by creating a node for a given value, the node's value is the number of times that value
    is repeated in the array. Has O(n) complexity
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap(da.length() // 3, hash_function_1)
    mode_array = DynamicArray()
    mode_count = 1
    for i in range(da.length()):
        if map.contains_key(da[i]) is True:
            value = map.get_node(da[i])           #this is the node associated with the value from the DA
            value.value +=1                  #adds one to the value associated with the value from the DA (value from da != key/value pair, int his case the key is the value from the da and the value is the occurance value)
            if value.value > mode_count:    #if the occurance supersedes the current "high score", create a new da and populate it with the new winner
                mode_count = value.value
                mode_array = DynamicArray()
                mode_array.append(da[i])
            elif value.value == mode_count:
                mode_array.append(da[i])
        else:
            map.put(da[i], 1)
            if mode_count == 1:
                mode_array.append(da[i])
    return (mode_array, mode_count)


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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    map = HashMap(da.length() // 3, hash_function_1)
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        map = HashMap(da.length() // 3, hash_function_2)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}\n")
