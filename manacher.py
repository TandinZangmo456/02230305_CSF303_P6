def manacher(s: str) -> str:
    t = '#' + '#'.join(s) + '#'
    n = len(t)
    p = [0] * n

    center = 0
    right  = 0

    for i in range(n):
        mirror = 2 * center - i

        if i < right:
            p[i] = min(right - i, p[mirror])
        a = i + p[i] + 1  
        b = i - p[i] - 1 
        while a < n and b >= 0 and t[a] == t[b]:
            p[i] += 1  
            a += 1
            b -= 1

        if i + p[i] > right:
            center = i           
            right  = i + p[i]   

    max_len    = max(p)        
    center_idx = p.index(max_len)  
    start = (center_idx - max_len) // 2
    return s[start : start + max_len]

def manacher_verbose(s: str):
    t = '#' + '#'.join(s) + '#'
    n = len(t)
    p = [0] * n
    center = right = 0

    for i in range(n):
        mirror = 2 * center - i
        if i < right:
            p[i] = min(right - i, p[mirror])
        a, b = i + p[i] + 1, i - p[i] - 1
        while a < n and b >= 0 and t[a] == t[b]:
            p[i] += 1
            a += 1
            b -= 1
        if i + p[i] > right:
            center, right = i, i + p[i]

    print(f"\nTransformed: {t}")
    print(f"Radii p[]:   {p}")
    print(f"Palindromes found:")
    for i, r in enumerate(p):
        if r > 0:  
            start = (i - r) // 2
            sub = s[start: start + r]
            print(f"  Center t[{i}]='{t[i]}', radius={r} → '{sub}'")


# Main

if __name__ == "__main__":
    print(" MANACHER'S ALGORITHM \n")

    test_cases = [
        "babad",     
        "cbbd",       
        "racecar",   
        "abacaba",   
        "abcde",      
        "aabbaa",     
        "a",         
    ]

    for s in test_cases:
        result = manacher(s)
        print(f"Input: {s!r:15}  →  Longest Palindrome: {result!r}")

    print("\n VERBOSE TRACE for 'racecar")
    manacher_verbose("racecar")