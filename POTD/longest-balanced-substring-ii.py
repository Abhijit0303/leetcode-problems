"""3714. Longest Balanced Substring II
Medium
Topics
premium lock icon
Companies
Hint
You are given a string s consisting only of the characters 'a', 'b', and 'c'.

A substring of s is called balanced if all distinct characters in the substring appear the same number of times.

Return the length of the longest balanced substring of s.



Example 1:

Input: s = "abbac"

Output: 4

Explanation:

The longest balanced substring is "abba" because both distinct characters 'a' and 'b' each appear exactly 2 times.

Example 2:

Input: s = "aabcc"

Output: 3

Explanation:

The longest balanced substring is "abc" because all distinct characters 'a', 'b' and 'c' each appear exactly 1 time.

Example 3:

Input: s = "aba"

Output: 2

Explanation:

One of the longest balanced substrings is "ab" because both distinct characters 'a' and 'b' each appear exactly 1 time. Another longest balanced substring is "ba".



Constraints:

1 <= s.length <= 105
s contains only the characters 'a', 'b', and 'c'."""

class Solution:
    def longestBalanced(self, s: str) -> int:
        n = len(s)
        ans = 0

        # Case 1: single char
        i = 0
        while i < n:
            j = i
            while j < n and s[j] == s[i]:
                j += 1
            ans = max(ans, j - i)
            i = j

        # helper for 2-char case
        def solve_pair(x, y):
            nonlocal ans
            diff = 0
            seen = {0: -1}
            for i, ch in enumerate(s):
                if ch != x and ch != y:
                    diff = 0
                    seen = {0: i}
                    continue

                if ch == x:
                    diff += 1
                else:
                    diff -= 1

                if diff in seen:
                    ans = max(ans, i - seen[diff])
                else:
                    seen[diff] = i

        # Case 2: pairs
        solve_pair('a', 'b')
        solve_pair('a', 'c')
        solve_pair('b', 'c')

        # Case 3: a, b, c
        a = b = c = 0
        seen = {(0, 0): -1}

        for i, ch in enumerate(s):
            if ch == 'a':
                a += 1
            elif ch == 'b':
                b += 1
            else:
                c += 1

            key = (a - b, a - c)
            if key in seen:
                ans = max(ans, i - seen[key])
            else:
                seen[key] = i

        return ans
