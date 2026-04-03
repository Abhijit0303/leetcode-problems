"""3661. Maximum Walls Destroyed by Robots
Solved
Hard
Topics
premium lock icon
Companies
Hint
There is an endless straight line populated with some robots and walls. You are given integer arrays robots, distance, and walls:
robots[i] is the position of the ith robot.
distance[i] is the maximum distance the ith robot's bullet can travel.
walls[j] is the position of the jth wall.
Every robot has one bullet that can either fire to the left or the right at most distance[i] meters.

A bullet destroys every wall in its path that lies within its range. Robots are fixed obstacles: if a bullet hits another robot before reaching a wall, it immediately stops at that robot and cannot continue.

Return the maximum number of unique walls that can be destroyed by the robots.

Notes:

A wall and a robot may share the same position; the wall can be destroyed by the robot at that position.
Robots are not destroyed by bullets.


Example 1:

Input: robots = [4], distance = [3], walls = [1,10]

Output: 1

Explanation:

robots[0] = 4 fires left with distance[0] = 3, covering [1, 4] and destroys walls[0] = 1.
Thus, the answer is 1.
Example 2:

Input: robots = [10,2], distance = [5,1], walls = [5,2,7]

Output: 3

Explanation:

robots[0] = 10 fires left with distance[0] = 5, covering [5, 10] and destroys walls[0] = 5 and walls[2] = 7.
robots[1] = 2 fires left with distance[1] = 1, covering [1, 2] and destroys walls[1] = 2.
Thus, the answer is 3.
Example 3:
Input: robots = [1,2], distance = [100,1], walls = [10]

Output: 0

Explanation:

In this example, only robots[0] can reach the wall, but its shot to the right is blocked by robots[1]; thus the answer is 0.



Constraints:

1 <= robots.length == distance.length <= 105
1 <= walls.length <= 105
1 <= robots[i], walls[j] <= 109
1 <= distance[i] <= 105
All values in robots are unique
All values in walls are unique"""

class Solution(object):
    def maxWalls(self, robots, distance, walls):
        """
        :type robots: List[int]
        :type distance: List[int]
        :type walls: List[int]
        :rtype: int
        """
        n = len(robots)
        indexed_robots = sorted(range(n), key=lambda i: robots[i])
        sorted_robot_pos = [robots[i] for i in indexed_robots]
        sorted_robot_dist = [distance[i] for i in indexed_robots]
        sorted_walls = sorted(walls)
        walls_set = set(walls)

        def bisect_left(a, x):
            lo, hi = 0, len(a)
            while lo < hi:
                mid = (lo + hi) // 2
                if a[mid] < x: lo = mid + 1
                else: hi = mid
            return lo

        def bisect_right(a, x):
            lo, hi = 0, len(a)
            while lo < hi:
                mid = (lo + hi) // 2
                if a[mid] <= x: lo = mid + 1
                else: hi = mid
            return lo

        def count_walls(l, r):
            if l > r: return 0
            return bisect_right(sorted_walls, r) - bisect_left(sorted_walls, l)

        def union_count(a1, b1, a2, b2):
            if a1 > b1 and a2 > b2: return 0
            if a1 > b1: return count_walls(a2, b2)
            if a2 > b2: return count_walls(a1, b1)
            if a2 > b1 + 1 or b2 < a1 - 1:
                return count_walls(a1, b1) + count_walls(a2, b2)
            return count_walls(min(a1, a2), max(b1, b2))

        at_wall = [1 if sorted_robot_pos[i] in walls_set else 0 for i in range(n)]

        if n == 1:
            left_walls = count_walls(max(1, sorted_robot_pos[0] - sorted_robot_dist[0]), sorted_robot_pos[0])
            right_walls = count_walls(sorted_robot_pos[0], sorted_robot_pos[0] + sorted_robot_dist[0])
            return max(left_walls, right_walls)

        def get_ranges(i):
            pos, dist = sorted_robot_pos[i], sorted_robot_dist[i]
            left_cap = sorted_robot_pos[i-1] + 1 if i > 0 else 1
            right_cap = sorted_robot_pos[i+1] - 1 if i < n-1 else pos + dist
            left_range = (max(pos - dist, left_cap), pos)
            right_range = (pos, min(pos + dist, right_cap))
            return left_range, right_range

        # For each robot, firing left or right gives a fixed interval (capped by neighbors)
        # We need to pick one direction per robot to maximize unique walls hit
        # Intervals of different robots can overlap -> use DP tracking covered regions is too expensive
        # Instead: note walls between robot[i] and robot[i+1] can only be hit by robot[i] (right) or robot[i+1] (left)
        # So the problem decomposes per-gap independently... EXCEPT a robot's choice affects both adjacent gaps.

        # DP: process robots left to right
        # dp[0] = max walls if current robot fires LEFT
        # dp[1] = max walls if current robot fires RIGHT
        # When transitioning i-1 -> i, we resolve the gap between them.

        def gap_contribution(i, prev_fires_right, curr_fires_left):
            L = sorted_robot_pos[i-1] + 1
            R = sorted_robot_pos[i] - 1
            if L > R: return 0
            a1, b1 = (sorted_robot_pos[i-1], min(sorted_robot_pos[i-1] + sorted_robot_dist[i-1], R)) if prev_fires_right else (1, 0)
            a2, b2 = (max(sorted_robot_pos[i] - sorted_robot_dist[i], L), sorted_robot_pos[i]) if curr_fires_left else (1, 0)
            # Clamp to gap [L, R]
            if prev_fires_right: a1, b1 = max(a1, L), min(b1, R)
            if curr_fires_left:  a2, b2 = max(a2, L), min(b2, R)
            return union_count(a1, b1, a2, b2)

        # left boundary walls: only robot 0 firing left can reach
        left_boundary = count_walls(max(1, sorted_robot_pos[0] - sorted_robot_dist[0]), sorted_robot_pos[0] - 1)
        # right boundary walls: only last robot firing right can reach
        right_boundary = count_walls(sorted_robot_pos[n-1] + 1, sorted_robot_pos[n-1] + sorted_robot_dist[n-1])

        # Base: robot 0
        dp = [
            left_boundary + at_wall[0],  # fires left
            at_wall[0]                    # fires right (right gap resolved later)
        ]

        for i in range(1, n):
            g00 = gap_contribution(i, False, False)  # prev left, curr left  -> 0 (neither covers gap)
            g01 = gap_contribution(i, False, True)   # prev left, curr left  -> curr covers gap left side
            g10 = gap_contribution(i, True,  False)  # prev right, curr right-> prev covers gap right side
            g11 = gap_contribution(i, True,  True)   # both cover gap

            new_dp = [0, 0]
            # curr fires LEFT (d=0)
            new_dp[0] = max(
                dp[0] + g01 + at_wall[i],   # prev fired left
                dp[1] + g11 + at_wall[i]    # prev fired right
            )
            # curr fires RIGHT (d=1)
            new_dp[1] = max(
                dp[0] + g00 + at_wall[i],   # prev fired left, gap uncovered
                dp[1] + g10 + at_wall[i]    # prev fired right
            )
            dp = new_dp

        return max(dp[0], dp[1] + right_boundary)
