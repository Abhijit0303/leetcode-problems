"""190. Reverse Bits
Solved
Easy
Topics
premium lock icon
Companies
Reverse bits of a given 32 bits signed integer.



Example 1:

Input: n = 43261596

Output: 964176192

Explanation:

Integer	Binary
43261596	00000010100101000001111010011100
964176192	00111001011110000010100101000000
Example 2:

Input: n = 2147483644

Output: 1073741822

Explanation:

Integer	Binary
2147483644	01111111111111111111111111111100
1073741822	00111111111111111111111111111110


Constraints:

0 <= n <= 231 - 2
n is even.


Follow up: If this function is called many times, how would you optimize it?"""

"""class Solution:
    def reverseBits(self, n: int) -> int:
        ans = 0
        for _ in range(32):
            ans = (ans << 1) | (n & 1)
            n >>= 1
        return ans
        """

class Solution:
    table = [0] * 256
    for i in range(256):
        x = i
        res = 0
        for _ in range(8):
            res = (res << 1) | (x & 1)
            x >>= 1
        table[i] = res

    def reverseBits(self, n: int) -> int:
        return (
            (self.table[n & 0xff] << 24) |
            (self.table[(n >> 8) & 0xff] << 16) |
            (self.table[(n >> 16) & 0xff] << 8) |
            (self.table[(n >> 24) & 0xff])
        )
