class TrieNode:
    def __init__(self):
        self.children = {}   
        self.is_end = False  


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str):
        curr = self.root
        for ch in word:
            if ch not in curr.children:
                curr.children[ch] = TrieNode()  
            curr = curr.children[ch]            
        curr.is_end = True  
        print(f"Inserted: {word}")

    def search(self, word: str) -> bool:
        curr = self.root
        for ch in word:
            if ch not in curr.children:
                return False  
            curr = curr.children[ch]
        return curr.is_end 

    def starts_with(self, prefix: str) -> bool:
        curr = self.root
        for ch in prefix:
            if ch not in curr.children:
                return False
            curr = curr.children[ch]
        return True  

    def _delete_helper(self, node: TrieNode, word: str, depth: int) -> bool:
        if node is None:
            return False

        if depth == len(word):
            if not node.is_end:
                return False        
            node.is_end = False     
            return len(node.children) == 0  

        ch = word[depth]
        if ch not in node.children:
            return False  

        should_delete = self._delete_helper(node.children[ch], word, depth + 1)

        if should_delete:
            del node.children[ch] 
            return len(node.children) == 0 and not node.is_end

        return False

    def delete(self, word: str):
        if self.search(word):
            self._delete_helper(self.root, word, 0)
            print(f"Deleted: {word}")
        else:
            print(f"Word not found: {word}")


# Main
if __name__ == "__main__":
    trie = Trie()

    print(" TRIE OPERATIONS \n")

    for word in ["apple", "app", "application", "bat", "ball"]:
        trie.insert(word)

    print("\n Search")
    for word in ["apple", "app", "ap", "bat", "cat"]:
        result = "Found" if trie.search(word) else "Not Found"
        print(f"Search '{word}': {result}")

    print("\n Prefix Check")
    print(f"starts_with 'app': {trie.starts_with('app')}")
    print(f"starts_with 'cat': {trie.starts_with('cat')}")

    print("\n Delete")
    trie.delete("app")
    print(f"Search 'app' after delete: {'Found' if trie.search('app') else 'Not Found'}")
    print(f"Search 'apple' still exists: {'Found' if trie.search('apple') else 'Not Found'}")
    trie.delete("xyz")  