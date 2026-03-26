"""3548. Equal Sum Grid Partition II
Attempted
Hard
Topics
premium lock icon
Companies
Hint
You are given an m x n matrix grid of positive integers. Your task is to determine if it is possible to make either one horizontal or one vertical cut on the grid such that:

Each of the two resulting sections formed by the cut is non-empty.
The sum of elements in both sections is equal, or can be made equal by discounting at most one single cell in total (from either section).
If a cell is discounted, the rest of the section must remain connected.
Return true if such a partition exists; otherwise, return false.

Note: A section is connected if every cell in it can be reached from any other cell by moving up, down, left, or right through other cells in the section.



Example 1:

Input: grid = [[1,4],[2,3]]

Output: true

Explanation:



A horizontal cut after the first row gives sums 1 + 4 = 5 and 2 + 3 = 5, which are equal. Thus, the answer is true.
Example 2:

Input: grid = [[1,2],[3,4]]

Output: true

Explanation:



A vertical cut after the first column gives sums 1 + 3 = 4 and 2 + 4 = 6.
By discounting 2 from the right section (6 - 2 = 4), both sections have equal sums and remain connected. Thus, the answer is true.
Example 3:

Input: grid = [[1,2,4],[2,3,5]]

Output: false

Explanation:



A horizontal cut after the first row gives 1 + 2 + 4 = 7 and 2 + 3 + 5 = 10.
By discounting 3 from the bottom section (10 - 3 = 7), both sections have equal sums, but they do not remain connected as it splits the bottom section into two parts ([2] and [5]). Thus, the answer is false.
Example 4:

Input: grid = [[4,1,8],[3,2,6]]

Output: false

Explanation:

No valid cut exists, so the answer is false.



Constraints:

1 <= m == grid.length <= 105
1 <= n == grid[i].length <= 105
2 <= m * n <= 105
1 <= grid[i][j] <= 105"""


"""Still Atempting"""

class Solution(object):
    def canPartitionGrid(self, g):
        """
        :type grid: List[List[int]]
        :rtype: bool
        """
        m,n=len(g),len(g[0])
        tot=sum(map(sum,g))

    # horizontal
        s=0
        freq={}
        for i in range(m-1):
            for v in g[i]:
                s+=v
                freq[v]=freq.get(v,0)+1

            if s*2==tot:return True
            d=abs(s-(tot-s))

            if s>tot-s:
                if d in freq and ((i+1>1 and n>1) or d in (g[i][0],g[i][-1])):
                    return True
            else:
                found=any(d in row for row in g[i+1:])
                if found and ((m-i-1>1 and n>1) or d in (g[i+1][0],g[i+1][-1])):
                    return True

    # vertical
        s=0
        freq={}
        for j in range(n-1):
            for i in range(m):
                v=g[i][j]
                s+=v
                freq[v]=freq.get(v,0)+1

            if s*2==tot:return True
            d=abs(s-(tot-s))

            if s>tot-s:
                if d in freq and ((m>1 and j+1>1) or d in (g[0][j],g[-1][j])):
                    return True
            else:
                found=any(g[i][k]==d for i in range(m) for k in range(j+1,n))
                if found and ((m>1 and n-j-1>1) or d in (g[0][j+1],g[-1][j+1])):
                    return True

        return False