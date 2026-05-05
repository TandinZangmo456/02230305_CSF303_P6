**Practical 6 - Reflection**

# **Overview**

The practical was implemented in Python for three different data structures and algorithms: a simple Trie, a Patricia Trie and Manacher's Algorithm to detect palindromes. All implementations was tested against a common set of operations and all were confirmed to work correctly per the resulting terminal output.

# **1\. Trie (Standard Prefix Tree)**

## **What I Implemented**

It implemented a normal Trie and each node consists of a dictionary of children with their corresponding character, also each node has an is_end boolean to mark the end of the word. There are 4 operations: insert, search, starts\_with, delete.

## **How It Works**

Insertion traverses through each character in the tree, creating new nodes wherever required and finally marks the node with is\_end \= True. Search goes down that path and will return True if the last node has that flag. The starts_with method has an identical implementation, but does not check whether the end node is a leaf or not (it is a pure prefix query). Deletion employs a recursive post-order helper that unmarks is\_end and prunes child-less nodes on the way back up.

## **Output**

![alt text](<ss/Screenshot from 2026-05-05 16-15-12.png>)
*Figure 1: Terminal output for Trie operations — insert, search, prefix check, and delete.*

All five words were inserted successfully. Searches for apple, app, and bat returned Found, while ap and cat returned Not Found, correctly distinguishing full words from prefixes. After deleting app, the follow-up search confirmed removal, while apple still existed — demonstrating that the deletion preserves shared prefix paths. The attempt to delete xyz printed Word not found: xyz, as expected.

## **What I Learned**

The key insight is the separation of 'prefix exists' from 'word exists' via the is\_end flag. The recursive delete was the most challenging part: it requires deciding whether to prune a node only after confirming the subtree below it is empty. Getting the base case right — checking is\_end at depth \== len(word) — required careful reasoning about the call stack.

# **2\. Patricia Trie**

## **What I Implemented**

The Patricia Trie is a compressed binary trie that stores keys by the index of the first bit where two strings differ, eliminating redundant single-child nodes. Each PatriciaNode stores a key, a bit index, and two child pointers (left for bit=0, right for bit=1). Back-edges — edges pointing to ancestors or self — are used to terminate traversal instead of null pointers.

## **How It Works**

The \_get\_bit method extracts a specific bit from a string using ASCII values. \_first\_differing\_bit scans bits from both strings until it finds a mismatch. Searching follows forward edges as long as curr.bit \> prev.bit; once a back-edge is detected (a decrease in bit index), the current node's key is compared directly to the query. Insertion finds the candidate node, computes the differing bit, walks the tree to the right insertion point, and splices in a new node with a self-referencing edge. Deletion rebuilds the trie from scratch after removing the target, avoiding complex pointer surgery.

## **Output**

![alt text](<ss/Screenshot from 2026-05-05 16-15-28.png>)
*Figure 2: Terminal output for Patricia Trie — showing diff\_bit values on each insertion.*

The output shows root insertion of apple, followed by subsequent insertions with their computed diff\_bit values: app at bit 25, application at bit 36, bat at bit 6, and ball at bit 19\. These positions reflect the exact binary positions where each new string diverges from its closest neighbour in the trie — a direct demonstration of the compressed structure. All searches, deletions, and error cases matched expected results.

## **What I Learned**

The Patricia Trie is considerably more complex to reason about than a standard Trie. The use of back-edges as terminators is elegant but unintuitive. I initially struggled to understand why traversal stops when curr.bit \<= prev.bit. The key realisation is that in a Patricia Trie, bit indices always strictly increase along forward paths, so any decrease signals a back-edge and therefore a leaf. The diff\_bit values in the output made the binary structure tangible and helped verify the logic manually.

# **3\. Manacher's Algorithm**

## **What I Implemented**

Manacher's Algorithm finds the longest palindromic substring in O(n) linear time. The input is transformed by inserting \# separators which unifies odd and even-length palindromes into a single framework. And a radii array p\[\] stores the palindrome radius at each position in the transformed string.

## **How It Works**

The algorithm preserves a middle and right line of the rightmost known palindrome. Each position i, based on the position of the current mirror, is initialised using the radius of the mirror position to prevent unnecessary re-expansion. The algorithm will then seek to expand even more. When right-going palindrome at i, extends past the center, the center and limits are changed. The longest palindrome is obtained by searching the maximum in p and mapping the index of the maximum to the original string.

## **Output**

![alt text](<ss/Screenshot from 2026-05-05 16-15-45.png>)
*Figure 3: Manacher's Algorithm output — test cases and verbose trace for 'racecar'.*

The algorithm accurately found the longest palindrome in all seven test cases: bab in babad, bb in cbbd, the full racecar, abacaba, a in abcde, and the full aabbaa. The verbose trace of racecar revealed the transformed string \#r\#a\#c\#e\#c\#a\#r\#, the full radii array \[0, 1, 0, 1, 0, 1, 0, 7, 0, 1, 0, 1, 0, 1, 0\], and the palindrome centred at position 7 (the character 'e') with radius 7 — spanning the entire word.

#v# **What I Learned**

The \# transformation was the most illuminating part of this implementation. Before studying Manacher's, handling even-length palindromes seemed to require a separate case. The transformation eliminates this entirely. The mirror property — reusing previously computed radii — is what drives the O(n) complexity. The verbose trace made this concrete: positions already covered by the rightmost known palindrome avoid unnecessary re-expansion, keeping the total expansion work linear.

# **Comparative Reflection**

The three different implementations all operate on string data but approach different problems. The standard Trie data structure and its Patricia Trie are both retrieval structures in nature; however, Patricia Trie is a more space-efficient representation than a standard Trie (by eliminating chains of single-child nodes), because it transforms string comparisons into bit-wise comparisons based on the position of the single-child nodes in the tree. On the other hand, Manacher’s algorithm can be described as a purely computational technique – it is an algorithm that does not maintain any type of permanent data structure, but rather uses the fact that palindromes have symmetric structures when simply performing a scan through an input string. 

All three implementations are also unified by their shared theme of how Transformations empower their respective solution sets – the Patricia Trie uses transformations to transform string comparison to bit-level operations; Manacher’s uses transformations to transform the actual input string; and the standard Trie uses transformations to transform character sequences into tree paths for effective prefix-sharing. This reinforces the finding that while some algorithms can be very effective for different types of information, often the most important factors for choosing the best representation for your data is the representation itself, rather than the algorithm that will be used to solve the representation’s data.

In terms of difficult implementation, the Patricia Trie is the clear winner. The Patricia Trie contains both a set of Backedges and uses bit-level addressing, consequently they make using this data structure considered to be much more challenging. Manacher’s algorithm was very algorithmically complex, but became more clear once the transform input string was followed through production. The standard Trie was a fairly simple data structure to use; however the recursive delete process was substantially complicated by the need to manage node-pruning in accordance with base case handling.
