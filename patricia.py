class PatriciaNode:
    def __init__(self, key: str, bit: int):
        self.key   = key    
        self.bit   = bit    
        self.left  = None   
        self.right = None   


class PatriciaTrie:
    def __init__(self):
        self.root = None

    def _get_bit(self, key: str, b: int) -> int:
        if b < 0:
            return 0
        byte_index = b // 8              
        bit_index  = 7 - (b % 8)        
        if byte_index >= len(key):
            return 0                     
        return (ord(key[byte_index]) >> bit_index) & 1  

    def _first_differing_bit(self, a: str, b: str) -> int:
        max_bits = max(len(a), len(b)) * 8
        for i in range(max_bits):
            if self._get_bit(a, i) != self._get_bit(b, i):
                return i  
        return -1  

    def _search_node(self, key: str):
        if not self.root:
            return None
        curr = self.root
        prev = None

        while prev is None or curr.bit > prev.bit:
            prev = curr
            if self._get_bit(key, curr.bit) == 0:
                curr = curr.left  
            else:
                curr = curr.right  
        return curr  

    def search(self, key: str) -> bool:
        node = self._search_node(key)
        return node is not None and node.key == key  

    def insert(self, key: str):
        if not self.root:
            self.root = PatriciaNode(key, 0)
            self.root.left  = self.root
            self.root.right = self.root
            print(f"Inserted (root): {key}")
            return

        candidate = self._search_node(key)
        if candidate.key == key:
            print(f"Key already exists: {key}")
            return

        diff_bit = self._first_differing_bit(key, candidate.key)

        curr = self.root
        prev = None
        while (prev is None or curr.bit > prev.bit) and curr.bit < diff_bit:
            prev = curr
            if self._get_bit(key, curr.bit) == 0:
                curr = curr.left
            else:
                curr = curr.right

        new_node = PatriciaNode(key, diff_bit)
        if self._get_bit(key, diff_bit) == 0:
            new_node.left  = new_node  
            new_node.right = curr      
        else:
            new_node.left  = curr
            new_node.right = new_node  

        if prev is None:
            self.root = new_node
        else:
            if prev.left is curr:
                prev.left = new_node
            else:
                prev.right = new_node

        print(f"Inserted: {key} (diff_bit={diff_bit})")

    def _collect_keys(self, node, prev_bit: int, keys: list):
        if node is None or node.bit <= prev_bit:
            return  
        keys.append(node.key)
        self._collect_keys(node.left,  node.bit, keys)
        self._collect_keys(node.right, node.bit, keys)

    def delete(self, key: str):
        if not self.search(key):
            print(f"Key not found: {key}")
            return

        all_keys = []
        self._collect_keys(self.root, -1, all_keys)
        self.root = None  

        for k in all_keys:
            if k != key:
                self.insert(k)

        print(f"Deleted: {key}")

# main
if __name__ == "__main__":
    pt = PatriciaTrie()

    print("PATRICIA TRIE OPERATIONS \n")

    for word in ["apple", "app", "application", "bat", "ball"]:
        pt.insert(word)

    print("\n Search")
    for word in ["apple", "app", "ap", "bat", "cat"]:
        print(f"Search '{word}': {'Found' if pt.search(word) else 'Not Found'}")

    print("\n Delete")
    pt.delete("app")
    print(f"Search 'app' after delete: {'Found' if pt.search('app') else 'Not Found'}")
    print(f"Search 'apple' still exists: {'Found' if pt.search('apple') else 'Not Found'}")
    pt.delete("xyz")