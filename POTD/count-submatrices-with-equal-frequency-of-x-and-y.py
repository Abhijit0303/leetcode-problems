"""3212. Count Submatrices With Equal Frequency of X and Y
Solved
Medium
Topics
premium lock icon
Companies
Hint
Given a 2D character matrix grid, where grid[i][j] is either 'X', 'Y', or '.', return the number of submatrices that contain:

grid[0][0]
an equal frequency of 'X' and 'Y'.
at least one 'X'.


Example 1:

Input: grid = [["X","Y","."],["Y",".","."]]

Output: 3

Explanation:



Example 2:

Input: grid = [["X","X"],["X","Y"]]

Output: 0

Explanation:

No submatrix has an equal frequency of 'X' and 'Y'.

Example 3:

Input: grid = [[".","."],[".","."]]

Output: 0

Explanation:

No submatrix has at least one 'X'.



Constraints:

1 <= grid.length, grid[i].length <= 1000
grid[i][j] is either 'X', 'Y', or '.'."""
class Solution:
    def numberOfSubmatrices(self, grid: List[List[str]]) -> int:
        m, n = len(grid), len(grid[0])

    # prefix sum for values
        prefix = [[0] * n for _ in range(m)]
    # prefix count of X
        countX = [[0] * n for _ in range(m)]

        def val(c):
            if c == 'X': return 1
            if c == 'Y': return -1
            return 0

        res = 0

        for i in range(m):
            for j in range(n):
            # value prefix
                prefix[i][j] = val(grid[i][j])
                countX[i][j] = 1 if grid[i][j] == 'X' else 0

                if i > 0:
                    prefix[i][j] += prefix[i-1][j]
                    countX[i][j] += countX[i-1][j]
                if j > 0:
                    prefix[i][j] += prefix[i][j-1]
                    countX[i][j] += countX[i][j-1]
                if i > 0 and j > 0:
                    prefix[i][j] -= prefix[i-1][j-1]
                    countX[i][j] -= countX[i-1][j-1]

            # check conditions
                if prefix[i][j] == 0 and countX[i][j] > 0:
                    res += 1

        return res
