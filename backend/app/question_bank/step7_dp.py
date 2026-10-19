"""Core route step 7: dynamic programming (动态规划 §1–§6)."""

from .question_schema import INCORRECT, OPTIMAL, SUBOPTIMAL, Choice, Question

QUESTIONS = [
    # ---------------------------------------------------------------- §1.1 climbing stairs
    Question(
        slug="climbing-stairs", number=70, title="Climbing Stairs",
        difficulty="Easy", topics=("dp",),
        summary="Climb n steps taking 1 or 2 at a time. Count the distinct ways.",
        example="3  →  3",
        criterion="Which approach is linear with O(1) extra space?",
        hint="What was your last move onto step n?",
        choices=(
            Choice(
                "f(i) = f(i − 1) + f(i − 2) with two variables", OPTIMAL, time="O(n)", space="O(1)", visual="dp-1d",
                detail="Roll the last two counts forward from f(0) = f(1) = 1.",
                why="Every way to reach i ends with a 1-step from i − 1 or a 2-step from i − 2, and only the last two values are ever needed.",
            ),
            Choice(
                "Memoized recursion", SUBOPTIMAL, time="O(n)", space="O(n)", visual="recursion",
                detail="Cache f(i) in a table while recursing from n.",
                why="Correct and linear, but stores every value and uses an O(n) call stack.",
            ),
            Choice(
                "2ⁿ⁻¹", INCORRECT, time="O(1)", space="O(1)", visual="math",
                detail="Count every way to split n into ordered parts.",
                why="That allows steps of any size. For n = 3, is a single 3-step allowed?",
            ),
            Choice(
                "n", INCORRECT, time="O(1)", space="O(1)", visual="math",
                detail="One way per possible number of 2-steps.",
                why="Where you place the 2-steps also matters: 1+2 and 2+1 differ.",
            ),
        ),
    ),
    Question(
        slug="min-cost-climbing-stairs", number=746, title="Min Cost Climbing Stairs",
        difficulty="Easy", topics=("dp",),
        summary="Stepping on step i costs cost[i]; you climb 1 or 2 steps and may start at step 0 or 1. Return the cheapest way past the top.",
        example="[10,15,20]  →  15",
        criterion="Which approach is linear with O(1) extra space?",
        hint="To stand at the top, which step did you leave from?",
        choices=(
            Choice(
                "dp[i] = min(dp[i − 1] + cost[i − 1], dp[i − 2] + cost[i − 2])", OPTIMAL, time="O(n)", space="O(1)", visual="dp-1d",
                detail="dp[0] = dp[1] = 0; roll two values up to dp[n].",
                why="Reaching i costs the cheaper of arriving from one or two below, plus that step's cost.",
            ),
            Choice(
                "Plain recursion", SUBOPTIMAL, time="O(2ⁿ)", space="O(n)", visual="recursion",
                detail="Recurse on both choices without caching.",
                why="Correct, but the same steps are solved again and again.",
            ),
            Choice(
                "Always step to the cheaper of the next two", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Greedy one step at a time.",
                why="A cheap next step can force you onto an expensive one after it.",
            ),
            Choice(
                "Sum of the cheaper of each pair", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="Add min(cost[i], cost[i + 1]) for every other i.",
                why="Moves can't be planned pair by pair; a 2-step changes the pairing.",
            ),
        ),
    ),
    Question(
        slug="climbing-stairs-ii", number=3693, title="Climbing Stairs II",
        difficulty="Medium", topics=("dp",),
        summary="From step i you may jump to i + 1, i + 2 or i + 3; landing on j costs costs[j] + (j − i)². Return the cheapest way from step 0 to step n.",
        example="n = 4, costs = [1,2,3,4]  →  13",
        criterion="Which approach is linear?",
        hint="Which steps can jump to step j?",
        choices=(
            Choice(
                "dp[j] = costs[j] + min over d ∈ {1,2,3} of dp[j − d] + d²", OPTIMAL, time="O(n)", space="O(n)", visual="dp-1d",
                detail="Fill dp from 1 to n with dp[0] = 0.",
                why="Each step has only three possible predecessors, so each state costs O(1).",
            ),
            Choice(
                "Dijkstra over steps", SUBOPTIMAL, time="O(n log n)", space="O(n)", visual="dijkstra",
                detail="Treat jumps as weighted edges and run Dijkstra.",
                why="Correct, but edges only go forward, so plain DP order already works.",
            ),
            Choice(
                "Ignore the jump penalty", INCORRECT, time="O(n)", space="O(n)", visual="dp-1d",
                detail="Pay only costs[j].",
                why="A 3-step adds 9. Would 0 → 3 still look free?",
            ),
            Choice(
                "Always jump 1", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="The penalty is smallest for 1-steps.",
                why="Skipping an expensive step can be worth the penalty, as in example 2.",
            ),
        ),
    ),
    Question(
        slug="combination-sum-iv", number=377, title="Combination Sum IV",
        difficulty="Medium", topics=("dp",),
        summary="Count the ordered sequences of distinct positive nums (reuse allowed) that sum to target.",
        example="[1,2,3], 4  →  7",
        criterion="Which approach is O(target · n)?",
        hint="Order matters, so this is climbing stairs with steps from nums.",
        choices=(
            Choice(
                "dp[t] = Σ dp[t − x], target in the outer loop", OPTIMAL, time="O(target·n)", space="O(target)", visual="dp-1d",
                detail="dp[0] = 1; for t from 1 to target, add dp[t − x] for every x ≤ t.",
                why="The last number of a sequence can be any x, so sequences summing to t split by their last element.",
            ),
            Choice(
                "Backtracking over sequences", SUBOPTIMAL, time="Exponential", space="O(target)", visual="backtrack",
                detail="Enumerate every sequence.",
                why="Correct, but the count can be huge.",
            ),
            Choice(
                "nums in the outer loop", INCORRECT, time="O(target·n)", space="O(target)", visual="dp-1d",
                detail="Coin-change order: for x in nums, for t from x to target.",
                why="That counts combinations, so 1+3 and 3+1 merge. The answer would be 4.",
            ),
            Choice(
                "Combinations times orderings", INCORRECT, time="Exponential", space="O(target)", visual="math",
                detail="Multiply each combination by k!.",
                why="Repeated numbers like 1+1+2 have fewer than 3! orders.",
            ),
        ),
    ),
    Question(
        slug="count-ways-to-build-good-strings", number=2466, title="Count Ways To Build Good Strings",
        difficulty="Medium", topics=("dp",),
        summary="Build strings by repeatedly appending zero '0's or one '1's. Count strings with length in [low, high], mod 10⁹ + 7.",
        example="low = 3, high = 3, zero = 1, one = 1  →  8",
        criterion="Which approach is O(high)?",
        hint="A string of length i ends with which block?",
        choices=(
            Choice(
                "dp[i] = dp[i − zero] + dp[i − one], sum over [low, high]", OPTIMAL, time="O(high)", space="O(high)", visual="dp-1d",
                detail="dp[0] = 1; add dp[i] to the answer when i is in range.",
                why="It's climbing stairs with step sizes zero and one. Different block orders give different strings.",
            ),
            Choice(
                "Recursion without memo", SUBOPTIMAL, time="Exponential", space="O(high)", visual="recursion",
                detail="Branch on the next block until past high.",
                why="Correct, but recomputes shared lengths.",
            ),
            Choice(
                "Only length high", INCORRECT, time="O(high)", space="O(high)", visual="dp-1d",
                detail="Return dp[high].",
                why="All lengths from low to high count.",
            ),
            Choice(
                "Count strings by zeros and ones used", INCORRECT, time="O(high²)", space="O(high²)", visual="dp-2d",
                detail="C(blocks, zero blocks) without order.",
                why="That counts block counts, not arrangements.",
            ),
        ),
    ),
    Question(
        slug="number-of-good-binary-strings", number=2533, title="Number of Good Binary Strings",
        difficulty="Medium", topics=("dp",),
        summary="A binary string is good if its length is in [minLength, maxLength], every block of 1s has a length divisible by oneGroup, and every block of 0s by zeroGroup. Count good strings mod 10⁹ + 7.",
        example="minLength = 2, maxLength = 3, oneGroup = 1, zeroGroup = 2  →  5",
        criterion="Which approach is O(maxLength)?",
        hint="Cut every block into pieces of exactly oneGroup or zeroGroup characters.",
        choices=(
            Choice(
                "dp[i] = dp[i − oneGroup] + dp[i − zeroGroup]", OPTIMAL, time="O(maxLength)", space="O(maxLength)", visual="dp-1d",
                detail="dp[0] = 1; sum dp[i] for i in range.",
                why="Each good string splits uniquely into pieces of length oneGroup (1s) and zeroGroup (0s), so it's the build-good-strings recurrence.",
            ),
            Choice(
                "Track the current block length", SUBOPTIMAL, time="O(maxLength²)", space="O(maxLength²)", visual="dp-2d",
                detail="dp over (length, last char, run length).",
                why="Correct, but the run length isn't needed once blocks are cut into fixed pieces.",
            ),
            Choice(
                "Blocks of exactly one group size", INCORRECT, time="O(maxLength)", space="O(maxLength)", visual="dp-1d",
                detail="Require alternating blocks of exactly oneGroup and zeroGroup.",
                why="Blocks can be any multiple, and two equal pieces in a row form a longer block.",
            ),
            Choice(
                "Only maxLength", INCORRECT, time="O(maxLength)", space="O(maxLength)", visual="dp-1d",
                detail="Return dp[maxLength].",
                why="Shorter good strings count too.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §1.2 house robber
    Question(
        slug="house-robber", number=198, title="House Robber",
        difficulty="Medium", topics=("dp",),
        summary="Rob houses in a row without robbing two adjacent ones. Return the most money.",
        example="[2,7,9,3,1]  →  12",
        criterion="Which approach is linear with O(1) extra space?",
        hint="For the last house: rob it or skip it. What does each choice leave?",
        choices=(
            Choice(
                "f(i) = max(f(i − 1), f(i − 2) + nums[i])", OPTIMAL, time="O(n)", space="O(1)", visual="dp-1d",
                detail="Roll two values across the array.",
                why="Skipping house i leaves f(i − 1); robbing it forbids i − 1 and leaves f(i − 2).",
            ),
            Choice(
                "Recursion without memo", SUBOPTIMAL, time="O(2ⁿ)", space="O(n)", visual="recursion",
                detail="Try both choices at every house.",
                why="Correct, but exponential.",
            ),
            Choice(
                "Better of even and odd indices", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="Sum alternate houses two ways.",
                why="For [2,1,1,2], both give 3, but robbing the two 2s gives 4.",
            ),
            Choice(
                "Rob the largest available greedily", INCORRECT, time="O(n log n)", space="O(n)", visual="greedy",
                detail="Take the richest house, block its neighbours, repeat.",
                why="For [3,4,3], greed takes 4; the two 3s give 6.",
            ),
        ),
    ),
    Question(
        slug="house-robber-ii", number=213, title="House Robber II",
        difficulty="Medium", topics=("dp",),
        summary="Houses form a circle, so the first and last are adjacent. Rob without taking two adjacent houses.",
        example="[2,3,2]  →  3",
        criterion="Which approach is linear with O(1) extra space?",
        hint="The first and last can't both be robbed. Split into two linear cases.",
        choices=(
            Choice(
                "Linear robber on [0..n−2] and on [1..n−1]", OPTIMAL, time="O(n)", space="O(1)", visual="dp-1d",
                detail="Return the better of the two runs (or nums[0] if n = 1).",
                why="Any valid plan excludes the first or the last house, so one of the two linear problems contains it.",
            ),
            Choice(
                "DP with a 'robbed first' flag", SUBOPTIMAL, time="O(n)", space="O(n)", visual="dp-2d",
                detail="Track whether house 0 was robbed in each state.",
                why="Correct, but stores more state than two runs need.",
            ),
            Choice(
                "Linear robber on the whole array", INCORRECT, time="O(n)", space="O(1)", visual="dp-1d",
                detail="Ignore the circle.",
                why="For [2,3,2], that robs both 2s, which are adjacent around the circle.",
            ),
            Choice(
                "Drop the smaller end", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Remove whichever of the first and last is smaller, then go linear.",
                why="The best plan may skip the larger end because of its neighbours.",
            ),
        ),
    ),
    Question(
        slug="count-number-of-ways-to-place-houses", number=2320, title="Count Number of Ways to Place Houses",
        difficulty="Medium", topics=("dp",),
        summary="A street has n plots on each side. Place houses so no two are adjacent on the same side. Count placements mod 10⁹ + 7.",
        example="2  →  9",
        criterion="Which approach is linear?",
        hint="Do the two sides interact at all?",
        choices=(
            Choice(
                "Count one side, then square", OPTIMAL, time="O(n)", space="O(1)", visual="dp-1d",
                detail="f(i) = f(i − 1) + f(i − 2) counts one side; return f(n)².",
                why="The sides are independent, so the total is the product of each side's count.",
            ),
            Choice(
                "DP over both sides at once", SUBOPTIMAL, time="O(n)", space="O(n)", visual="dp-2d",
                detail="Track four states per plot pair.",
                why="Correct, but needlessly combines independent sides.",
            ),
            Choice(
                "Count 2n plots in a row", INCORRECT, time="O(n)", space="O(1)", visual="dp-1d",
                detail="Treat both sides as one long street.",
                why="Plot n on one side and plot 1 on the other aren't neighbours.",
            ),
            Choice(
                "Double one side's count", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="Return 2·f(n).",
                why="Every choice on one side pairs with every choice on the other.",
            ),
        ),
    ),
    Question(
        slug="house-robber-v", number=3840, title="House Robber V",
        difficulty="Medium", topics=("dp",),
        summary="Houses have money and a color; you can't rob two adjacent houses of the same color. Return the most money.",
        example="nums = [3,1,2,4], colors = [2,3,2,2]  →  8",
        criterion="Which approach is linear?",
        hint="Whether you can rob i after i − 1 depends on their colors. What state do you need?",
        choices=(
            Choice(
                "DP with 'robbed i − 1' state", OPTIMAL, time="O(n)", space="O(1)", visual="dp-1d",
                detail="rob[i] = nums[i] + max(skip[i − 1], rob[i − 1] if colors differ); skip[i] = max(rob[i − 1], skip[i − 1]).",
                why="Only the previous house's choice and color matter, so two rolling values suffice.",
            ),
            Choice(
                "Try all subsets", SUBOPTIMAL, time="O(2ⁿ·n)", space="O(n)", visual="brute",
                detail="Check each set of houses.",
                why="Correct, but exponential.",
            ),
            Choice(
                "Classic house robber", INCORRECT, time="O(n)", space="O(1)", visual="dp-1d",
                detail="Never rob adjacent houses.",
                why="Different-colored neighbours are allowed: 3 and 1 above.",
            ),
            Choice(
                "Rob everything", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Ignore colors.",
                why="Two adjacent houses of the same color can't both be robbed.",
            ),
        ),
    ),
    Question(
        slug="delete-and-earn", number=740, title="Delete and Earn",
        difficulty="Medium", topics=("dp",),
        summary="Taking a value x earns x and deletes every x − 1 and x + 1. Return the most points.",
        example="[2,2,3,3,3,4]  →  9",
        criterion="Which approach is O(n + V)?",
        hint="If you take one 3, take all of them. What does that turn the problem into?",
        choices=(
            Choice(
                "Bucket by value, then house robber", OPTIMAL, time="O(n + V)", space="O(V)", visual="dp-1d",
                detail="points[x] = x · count(x); rob over x = 0..V.",
                why="Taking x forbids x − 1 and x + 1, exactly the adjacency rule of house robber over values.",
            ),
            Choice(
                "Sort, robber over distinct values", SUBOPTIMAL, time="O(n log n)", space="O(n)", visual="sort",
                detail="Group sorted values and handle gaps.",
                why="Correct, but sorting is unnecessary when values are small.",
            ),
            Choice(
                "Take the largest value first", INCORRECT, time="O(n log n)", space="O(n)", visual="greedy",
                detail="Greedily take the biggest value and its copies.",
                why="Taking 4 deletes the 3s worth 9.",
            ),
            Choice(
                "Robber over the original order", INCORRECT, time="O(n)", space="O(1)", visual="dp-1d",
                detail="Treat array neighbours as conflicts.",
                why="Conflicts are by value, not position.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §1.3 maximum subarray
    Question(
        slug="find-the-substring-with-maximum-cost", number=2606, title="Find the Substring With Maximum Cost",
        difficulty="Medium", topics=("dp",),
        summary="Letters in chars have custom values vals; others are worth their alphabet position. Return the maximum cost of a substring (the empty substring costs 0).",
        example="s = \"adaa\", chars = \"d\", vals = [-1000]  →  2",
        criterion="Which approach is linear?",
        hint="Map each letter to its value. What classic problem is left?",
        choices=(
            Choice(
                "Kadane with a floor of 0", OPTIMAL, time="O(n + 26)", space="O(26)", visual="dp-1d",
                detail="cur = max(cur, 0) + value; track the best, starting at 0.",
                why="It's maximum subarray sum, and the empty substring makes 0 the minimum answer.",
            ),
            Choice(
                "Every substring", SUBOPTIMAL, time="O(n²)", space="O(26)", visual="brute",
                detail="Sum from each start.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Non-empty Kadane", INCORRECT, time="O(n)", space="O(26)", visual="dp-1d",
                detail="Require at least one letter.",
                why="If every value is negative, the empty substring's 0 is best.",
            ),
            Choice(
                "Sum of positive letters", INCORRECT, time="O(n)", space="O(26)", visual="greedy",
                detail="Add every positive value.",
                why="The letters must be contiguous.",
            ),
        ),
    ),
    Question(
        slug="maximum-product-subarray", number=152, title="Maximum Product Subarray",
        difficulty="Medium", topics=("dp",),
        summary="Return the largest product of a non-empty contiguous subarray.",
        example="[-2,3,-4]  →  24",
        criterion="Which approach is linear with O(1) extra space?",
        hint="A negative number turns the smallest product into the largest.",
        choices=(
            Choice(
                "Track both max and min ending here", OPTIMAL, time="O(n)", space="O(1)", visual="dp-1d",
                detail="For x, candidates are x, x·max, x·min; update both and the answer.",
                why="The best product ending at i comes from the largest or the most negative product before it.",
            ),
            Choice(
                "Every subarray", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="Multiply from each start.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Kadane with products", INCORRECT, time="O(n)", space="O(1)", visual="dp-1d",
                detail="cur = max(x, cur·x).",
                why="For [-2,3,-4], it drops the −6 that later becomes 24.",
            ),
            Choice(
                "Product of all nonzero elements", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="Multiply everything except zeros.",
                why="An odd number of negatives makes it negative; zeros split the array.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §2.1 grid DP
    Question(
        slug="minimum-path-sum", number=64, title="Minimum Path Sum",
        difficulty="Medium", topics=("dp",),
        summary="Moving only right or down, find the path from top-left to bottom-right with the smallest sum.",
        example="[[1,3,1],[1,5,1],[4,2,1]]  →  7",
        criterion="Which approach is O(m·n) with O(n) extra space?",
        hint="To reach a cell, you came from above or from the left.",
        choices=(
            Choice(
                "Row-by-row DP in one array", OPTIMAL, time="O(m·n)", space="O(n)", visual="dp-2d",
                detail="dp[j] = grid[i][j] + min(dp[j] (above), dp[j − 1] (left)).",
                why="Each cell's best depends only on the cell above and to the left, so one row of state is enough.",
            ),
            Choice(
                "Recursion without memo", SUBOPTIMAL, time="O(2^(m+n))", space="O(m + n)", visual="recursion",
                detail="Try both moves from every cell.",
                why="Correct, but exponential.",
            ),
            Choice(
                "Greedy smaller neighbour", INCORRECT, time="O(m + n)", space="O(1)", visual="greedy",
                detail="Step right or down, whichever is smaller.",
                why="From 1, both 3 and 1 lead on; the cheap step down leads to 4 and 2.",
            ),
            Choice(
                "Sum of each row's minimum", INCORRECT, time="O(m·n)", space="O(1)", visual="matrix",
                detail="Pick the smallest cell in every row.",
                why="Those cells need not form a connected path.",
            ),
        ),
    ),
    Question(
        slug="unique-paths", number=62, title="Unique Paths",
        difficulty="Medium", topics=("dp",),
        summary="Count paths from the top-left to the bottom-right of an m×n grid moving only right or down.",
        example="m = 3, n = 7  →  28",
        criterion="Which approach is O(min(m, n))?",
        hint="Every path is a sequence of exactly m − 1 downs and n − 1 rights.",
        choices=(
            Choice(
                "Binomial C(m + n − 2, m − 1)", OPTIMAL, time="O(min(m, n))", space="O(1)", visual="math",
                detail="Compute the product of (n − 1 + i)/i for i = 1..m − 1 step by step.",
                why="A path is just a choice of which moves are downs, so the count is a binomial coefficient.",
            ),
            Choice(
                "Grid DP", SUBOPTIMAL, time="O(m·n)", space="O(n)", visual="dp-2d",
                detail="dp[j] += dp[j − 1] row by row.",
                why="Correct and general, but the closed form is faster.",
            ),
            Choice(
                "m · n", INCORRECT, time="O(1)", space="O(1)", visual="math",
                detail="One path per cell.",
                why="For 2×2 there are 2 paths, not 4.",
            ),
            Choice(
                "2^(m + n − 2)", INCORRECT, time="O(1)", space="O(1)", visual="math",
                detail="Two choices per move.",
                why="The number of downs is fixed, so not every sequence stays in the grid.",
            ),
        ),
    ),
    Question(
        slug="unique-paths-ii", number=63, title="Unique Paths II",
        difficulty="Medium", topics=("dp",),
        summary="Count right/down paths from top-left to bottom-right that avoid obstacle cells.",
        example="[[0,0,0],[0,1,0],[0,0,0]]  →  2",
        criterion="Which approach is O(m·n) with O(n) extra space?",
        hint="An obstacle has zero ways to be reached.",
        choices=(
            Choice(
                "Grid DP, zero at obstacles", OPTIMAL, time="O(m·n)", space="O(n)", visual="dp-2d",
                detail="dp[j] = 0 at obstacles, else dp[j] + dp[j − 1].",
                why="Paths through an obstacle vanish because its count is 0, and one row of state suffices.",
            ),
            Choice(
                "Enumerate paths by DFS", SUBOPTIMAL, time="O(2^(m+n))", space="O(m + n)", visual="recursion",
                detail="Count every path that avoids obstacles.",
                why="Correct, but exponential.",
            ),
            Choice(
                "Binomial minus paths through each obstacle", INCORRECT, time="O(k·(m + n))", space="O(1)", visual="math",
                detail="Subtract paths through each obstacle separately.",
                why="Paths through two obstacles are subtracted twice.",
            ),
            Choice(
                "Treat obstacles as 1-way cells", INCORRECT, time="O(m·n)", space="O(n)", visual="dp-2d",
                detail="Set dp to 1 at obstacles.",
                why="Paths must not pass through obstacles at all.",
            ),
        ),
    ),
    Question(
        slug="triangle", number=120, title="Triangle",
        difficulty="Medium", topics=("dp",),
        summary="From the top of a triangle, move to an adjacent number on the row below. Return the smallest path sum to the bottom.",
        example="[[2],[3,4],[6,5,7],[4,1,8,3]]  →  11",
        criterion="Which approach is O(n²) with O(n) extra space?",
        hint="Work from the bottom up: what's the best path starting at each cell?",
        choices=(
            Choice(
                "Bottom-up DP in one row", OPTIMAL, time="O(n²)", space="O(n)", visual="dp-1d",
                detail="Start from the last row; dp[j] = tri[i][j] + min(dp[j], dp[j + 1]).",
                why="Each cell's best continuation depends on two cells below, and the answer ends up in dp[0].",
            ),
            Choice(
                "Recursion without memo", SUBOPTIMAL, time="O(2ⁿ)", space="O(n)", visual="recursion",
                detail="Try both children from every cell.",
                why="Correct, but exponential.",
            ),
            Choice(
                "Greedy smaller child", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="From the top, always step to the smaller number.",
                why="A small number now can lead to large ones later.",
            ),
            Choice(
                "Sum of row minimums", INCORRECT, time="O(n²)", space="O(1)", visual="math",
                detail="Add the smallest of each row.",
                why="Row minimums may not be adjacent.",
            ),
        ),
    ),
    Question(
        slug="count-paths-with-the-given-xor-value", number=3393, title="Count Paths With the Given XOR Value",
        difficulty="Medium", topics=("dp",),
        summary="Count right/down paths from top-left to bottom-right whose cells XOR to k (values and k below 16), mod 10⁹ + 7.",
        example="[[2,1,5],[7,10,0],[12,6,4]], k = 11  →  3",
        criterion="Which approach is O(m·n·16)?",
        hint="Values are below 16, so the XOR so far has only 16 possibilities.",
        choices=(
            Choice(
                "dp[i][j][x] over the running XOR", OPTIMAL, time="O(m·n·16)", space="O(n·16)", visual="dp-2d",
                detail="dp[i][j][x ^ grid[i][j]] += dp from above and left with XOR x.",
                why="The future only needs the XOR so far, and 16 values make it a tiny extra dimension.",
            ),
            Choice(
                "Enumerate every path", SUBOPTIMAL, time="O(2^(m+n))", space="O(m + n)", visual="recursion",
                detail="DFS, checking the XOR at the end.",
                why="Correct, but exponential.",
            ),
            Choice(
                "Count paths, check one XOR", INCORRECT, time="O(m·n)", space="O(n)", visual="dp-2d",
                detail="Track the XOR of one representative path per cell.",
                why="Different paths to a cell have different XORs.",
            ),
            Choice(
                "XOR of the whole grid", INCORRECT, time="O(m·n)", space="O(1)", visual="bits",
                detail="Compare the XOR of every cell with k.",
                why="A path visits only some cells.",
            ),
        ),
    ),
    Question(
        slug="minimum-falling-path-sum", number=931, title="Minimum Falling Path Sum",
        difficulty="Medium", topics=("dp",),
        summary="Choose one cell per row, each row's column within 1 of the previous. Return the smallest sum.",
        example="[[2,1,3],[6,5,4],[7,8,9]]  →  13",
        criterion="Which approach is O(n²)?",
        hint="A cell's best path comes from one of three cells above.",
        choices=(
            Choice(
                "Row-by-row DP over three parents", OPTIMAL, time="O(n²)", space="O(n)", visual="dp-2d",
                detail="dp[j] = cell + min of the previous row's j − 1, j, j + 1.",
                why="Each cell has at most three predecessors, so each state is O(1).",
            ),
            Choice(
                "Recursion without memo", SUBOPTIMAL, time="O(3ⁿ)", space="O(n)", visual="recursion",
                detail="Try three moves from each cell.",
                why="Correct, but exponential.",
            ),
            Choice(
                "Row minimums", INCORRECT, time="O(n²)", space="O(1)", visual="matrix",
                detail="Add the smallest cell of each row.",
                why="The row minimums may be more than one column apart.",
            ),
            Choice(
                "Greedy from the top", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Start at the smallest top cell and step to the smallest neighbour.",
                why="A cheap first move can lead to expensive rows.",
            ),
        ),
    ),
    Question(
        slug="minimum-cost-path-with-alternating-directions-ii", number=3603, title="Minimum Cost Path with Alternating Directions II",
        difficulty="Medium", topics=("dp",),
        summary="Entering cell (i, j) costs (i + 1)(j + 1). Starting by entering (0, 0), you alternate: move right or down, then wait one second paying waitCost of your cell. Return the cheapest cost to reach (m − 1, n − 1).",
        example="m = 2, n = 2, waitCost = [[3,5],[2,4]]  →  9",
        criterion="Which approach is O(m·n)?",
        hint="Which cells on a path pay their wait cost?",
        choices=(
            Choice(
                "Grid DP, waiting at every cell but the start and the end", OPTIMAL, time="O(m·n)", space="O(n)", visual="dp-2d",
                detail="dp = entry cost + min(above, left), plus waitCost for intermediate cells.",
                why="After each move except the last you wait once, so each intermediate cell adds its wait cost; the rest is a min path sum.",
            ),
            Choice(
                "Dijkstra over cells", SUBOPTIMAL, time="O(m·n log(m·n))", space="O(m·n)", visual="dijkstra",
                detail="Treat entries and waits as edge weights.",
                why="Correct, but moves only go right or down, so DP order suffices.",
            ),
            Choice(
                "Wait at the start too", INCORRECT, time="O(m·n)", space="O(n)", visual="dp-2d",
                detail="Add waitCost[0][0].",
                why="The first move happens at second 1, before any waiting.",
            ),
            Choice(
                "Entry costs only", INCORRECT, time="O(m·n)", space="O(n)", visual="dp-2d",
                detail="Ignore waiting.",
                why="Example 2 pays 2 for waiting at (1, 0).",
            ),
        ),
    ),
    Question(
        slug="minimum-path-cost-in-a-grid", number=2304, title="Minimum Path Cost in a Grid",
        difficulty="Medium", topics=("dp",),
        summary="Move from any cell in row i to any cell in row i + 1; moving from value v to column c costs moveCost[v][c]. A path's cost is its values plus move costs. Return the cheapest path from the first row to the last.",
        example="grid = [[5,3],[4,0],[2,1]], moveCost = [[9,8],[1,5],[10,12],[18,6],[2,4],[14,3]]  →  17",
        criterion="Which approach is O(m·n²)?",
        hint="A cell in row i + 1 can be reached from every cell of row i.",
        choices=(
            Choice(
                "Row-by-row DP over all previous cells", OPTIMAL, time="O(m·n²)", space="O(n)", visual="dp-2d",
                detail="dp[j] = grid[i][j] + min over k of prev[k] + moveCost[grid[i−1][k]][j].",
                why="Each cell's best depends only on the previous row, considered in full.",
            ),
            Choice(
                "Try every path", SUBOPTIMAL, time="O(nᵐ)", space="O(m)", visual="recursion",
                detail="DFS over all column choices.",
                why="Correct, but exponential in the number of rows.",
            ),
            Choice(
                "Greedy cheapest next step", INCORRECT, time="O(m·n)", space="O(1)", visual="greedy",
                detail="From each cell, take the cheapest move into the next row.",
                why="A cheap move now can lead to an expensive cell and moves later.",
            ),
            Choice(
                "Ignore move costs", INCORRECT, time="O(m·n)", space="O(1)", visual="matrix",
                detail="Add the smallest value of each row.",
                why="Moves have costs that depend on value and column.",
            ),
        ),
    ),
    Question(
        slug="minimum-falling-path-sum-ii", number=1289, title="Minimum Falling Path Sum II",
        difficulty="Hard", topics=("dp",),
        summary="Choose one cell per row of an n×n grid so no two consecutive rows use the same column. Return the smallest sum.",
        example="[[1,2,3],[4,5,6],[7,8,9]]  →  13",
        criterion="Which approach is O(n²)?",
        hint="For each cell, the best previous choice is the previous row's minimum, unless it's in the same column.",
        choices=(
            Choice(
                "Track the previous row's smallest and second smallest", OPTIMAL, time="O(n²)", space="O(1)", visual="dp-2d",
                detail="For column j, add the previous minimum, or the second minimum if the minimum was in column j.",
                why="Excluding one column only ever changes the best predecessor to the runner-up, so two values summarize the row.",
            ),
            Choice(
                "Check every previous column", SUBOPTIMAL, time="O(n³)", space="O(n)", visual="dp-2d",
                detail="dp[j] = cell + min over k ≠ j of prev[k].",
                why="Correct, but rescans the row per cell.",
            ),
            Choice(
                "Row minimums", INCORRECT, time="O(n²)", space="O(1)", visual="matrix",
                detail="Add each row's smallest value.",
                why="Two consecutive minimums can share a column.",
            ),
            Choice(
                "Only the previous minimum", INCORRECT, time="O(n²)", space="O(1)", visual="dp-2d",
                detail="Always add the previous row's minimum.",
                why="If it's in the same column, it's not allowed.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §2.2 grid DP, further practice
    Question(
        slug="dungeon-game", number=174, title="Dungeon Game",
        difficulty="Hard", topics=("dp",),
        summary="A knight walks right/down from the top-left to the princess at the bottom-right; cells add or remove health, which must stay ≥ 1. Return the minimum starting health.",
        example="[[-2,-3,3],[-5,-10,1],[10,30,-5]]  →  7",
        criterion="Which approach is O(m·n)?",
        hint="Going forward, you don't know what's ahead. What if you start from the princess?",
        choices=(
            Choice(
                "Backward DP on needed health", OPTIMAL, time="O(m·n)", space="O(n)", visual="dp-2d",
                detail="need[i][j] = max(1, min(need right, need below) − dungeon[i][j]), filled from the bottom-right.",
                why="The health needed at a cell depends only on what's needed afterwards, so working backward makes each cell O(1).",
            ),
            Choice(
                "Binary search the start health with a check", SUBOPTIMAL, time="O(m·n log V)", space="O(n)", visual="binary-search",
                detail="For a guess, run a forward DP of the best remaining health.",
                why="Correct, but needs log V passes.",
            ),
            Choice(
                "Forward max-sum path", INCORRECT, time="O(m·n)", space="O(n)", visual="dp-2d",
                detail="Find the path with the largest total and its minimum prefix.",
                why="A path with a big total can dip very low early.",
            ),
            Choice(
                "Forward DP of the lowest point", INCORRECT, time="O(m·n)", space="O(n)", visual="dp-2d",
                detail="Track the best minimum prefix sum per cell going forward.",
                why="Two states compete: the lowest point so far and the current sum. One number can't rank them.",
            ),
        ),
    ),
    Question(
        slug="longest-increasing-path-in-a-matrix", number=329, title="Longest Increasing Path in a Matrix",
        difficulty="Hard", topics=("dp",),
        summary="Moving up, down, left or right, return the length of the longest strictly increasing path.",
        example="[[9,9,4],[6,6,8],[2,1,1]]  →  4",
        criterion="Which approach is O(m·n)?",
        hint="Strictly increasing paths can't loop, so the answer from each cell never changes.",
        choices=(
            Choice(
                "DFS with memo", OPTIMAL, time="O(m·n)", space="O(m·n)", visual="graph-dfs",
                detail="best(c) = 1 + max best(neighbour) over larger neighbours; cache it.",
                why="The 'larger neighbour' edges form a DAG, so each cell's answer is computed once.",
            ),
            Choice(
                "DFS without memo", SUBOPTIMAL, time="Exponential", space="O(m·n)", visual="recursion",
                detail="Explore from every cell from scratch.",
                why="Correct, but shared tails are re-explored.",
            ),
            Choice(
                "Right and down only", INCORRECT, time="O(m·n)", space="O(m·n)", visual="dp-2d",
                detail="Grid DP in reading order.",
                why="The best path in the example goes up: 1 → 2 → 6 → 9.",
            ),
            Choice(
                "Count distinct values", INCORRECT, time="O(m·n)", space="O(m·n)", visual="set",
                detail="Any increasing sequence of values works.",
                why="The cells must be adjacent.",
            ),
        ),
    ),
    Question(
        slug="cherry-pickup", number=741, title="Cherry Pickup",
        difficulty="Hard", topics=("dp",),
        summary="Walk right/down from top-left to bottom-right, then left/up back, collecting cherries (each once) and avoiding thorns (−1). Return the most cherries, or 0.",
        example="[[0,1,-1],[1,0,-1],[1,1,1]]  →  5",
        criterion="Which approach is O(n³)?",
        hint="Make two people walk forward together, step by step.",
        choices=(
            Choice(
                "Two walkers in lockstep", OPTIMAL, time="O(n³)", space="O(n²)", visual="dp-2d",
                detail="dp[k][r1][r2] after k steps; columns follow from k; count a shared cell once.",
                why="The return trip is a second forward path. Walking both at the same step makes overlaps detectable.",
            ),
            Choice(
                "Try all pairs of paths", SUBOPTIMAL, time="Exponential", space="O(n)", visual="brute",
                detail="Enumerate both paths.",
                why="Correct, but exponential.",
            ),
            Choice(
                "Best path, then best path on what's left", INCORRECT, time="O(n²)", space="O(n²)", visual="greedy",
                detail="Greedy two passes.",
                why="The best single path can block a better pair.",
            ),
            Choice(
                "Two walkers without lockstep", INCORRECT, time="O(n⁴)", space="O(n⁴)", visual="dp-2d",
                detail="Track both positions independently.",
                why="Without equal steps you can't tell whether they visit the same cell at different times.",
            ),
        ),
    ),
    Question(
        slug="check-if-there-is-a-path-with-equal-number-of-0s-and-1s", number=2510, title="Check if There is a Path With Equal Number of 0's And 1's",
        difficulty="Medium", topics=("dp",),
        summary="Return whether some right/down path from the top-left to the bottom-right of a binary grid visits equally many 0s and 1s.",
        example="[[0,1,0,0],[0,1,0,0],[1,0,1,0]]  →  true",
        criterion="Which approach is O(m·n)?",
        hint="Paths to a cell have counts of 1s forming a range with no gaps. Why?",
        choices=(
            Choice(
                "DP of min and max 1s per cell", OPTIMAL, time="O(m·n)", space="O(n)", visual="dp-2d",
                detail="Fail if m + n − 1 is odd; else check that half of it lies between the bottom-right's min and max.",
                why="Swapping one move changes the count by at most 1, so every count between min and max is achievable.",
            ),
            Choice(
                "Set of reachable counts per cell", SUBOPTIMAL, time="O(m·n·(m + n))", space="O(n·(m + n))", visual="dp-2d",
                detail="Track every possible count of 1s.",
                why="Correct, but stores what the min and max already describe.",
            ),
            Choice(
                "Equal totals in the grid", INCORRECT, time="O(m·n)", space="O(1)", visual="counting",
                detail="Check the whole grid's counts.",
                why="A path visits only m + n − 1 cells.",
            ),
            Choice(
                "Greedy balance", INCORRECT, time="O(m + n)", space="O(1)", visual="greedy",
                detail="Step toward whichever value is behind.",
                why="Local choices can lead into a region with no balance.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §3.1 0-1 knapsack
    Question(
        slug="partition-equal-subset-sum", number=416, title="Partition Equal Subset Sum",
        difficulty="Medium", topics=("dp",),
        summary="Return whether nums can be split into two subsets with equal sums.",
        example="[1,5,11,5]  →  true",
        criterion="Which approach is O(n · S)?",
        hint="One subset must sum to exactly half.",
        choices=(
            Choice(
                "0/1 knapsack on reachable sums", OPTIMAL, time="O(n·S)", space="O(S)", visual="dp-1d",
                detail="Fail if S is odd; for each x, for s from S/2 down to x, can[s] |= can[s − x].",
                why="It's subset sum for S/2. Iterating s downward uses each number at most once.",
            ),
            Choice(
                "Backtracking", SUBOPTIMAL, time="O(2ⁿ)", space="O(n)", visual="backtrack",
                detail="Try including or excluding each number.",
                why="Correct, but exponential.",
            ),
            Choice(
                "Greedy into the smaller side", INCORRECT, time="O(n log n)", space="O(1)", visual="greedy",
                detail="Sort descending and add to the lighter subset.",
                why="[3,3,2,2,2] totals 12, and 3+3 vs 2+2+2 works, but greedy splits the 3s.",
            ),
            Choice(
                "Iterate s upward", INCORRECT, time="O(n·S)", space="O(S)", visual="dp-1d",
                detail="Same DP but s from x to S/2.",
                why="Then one number can be reused, as in [2] reaching 4.",
            ),
        ),
    ),
    Question(
        slug="length-of-the-longest-subsequence-that-sums-to-target", number=2915, title="Length of the Longest Subsequence That Sums to Target",
        difficulty="Medium", topics=("dp",),
        summary="Return the length of the longest subsequence that sums to target, or −1.",
        example="[1,2,3,4,5], 9  →  3",
        criterion="Which approach is O(n · target)?",
        hint="Subset sum, but maximize how many items you use.",
        choices=(
            Choice(
                "0/1 knapsack maximizing count", OPTIMAL, time="O(n·target)", space="O(target)", visual="dp-1d",
                detail="dp[s] = max(dp[s], dp[s − x] + 1), with s descending; unreachable sums are −∞.",
                why="Each item is used once and contributes 1 to the length, so it's a knapsack with value 1.",
            ),
            Choice(
                "Every subset", SUBOPTIMAL, time="O(2ⁿ)", space="O(n)", visual="backtrack",
                detail="Enumerate subsets summing to target.",
                why="Correct, but exponential.",
            ),
            Choice(
                "Take smallest numbers first", INCORRECT, time="O(n log n)", space="O(1)", visual="greedy",
                detail="Add from the smallest until the sum is reached.",
                why="1+2+3 = 6, then 4 overshoots. Is 9 reachable this way?",
            ),
            Choice(
                "Count subsets", INCORRECT, time="O(n·target)", space="O(target)", visual="dp-1d",
                detail="dp[s] += dp[s − x].",
                why="That counts subsets, not their lengths.",
            ),
        ),
    ),
    Question(
        slug="ones-and-zeroes", number=474, title="Ones and Zeroes",
        difficulty="Medium", topics=("dp",),
        summary="Choose the most binary strings with at most m zeros and n ones in total.",
        example="[\"10\",\"0001\",\"111001\",\"1\",\"0\"], m = 5, n = 3  →  4",
        criterion="Which approach is O(L · m · n)?",
        hint="Each string has a cost in two resources.",
        choices=(
            Choice(
                "Two-dimensional 0/1 knapsack", OPTIMAL, time="O(L·m·n)", space="O(m·n)", visual="dp-2d",
                detail="For each string, for i from m down, for j from n down: dp[i][j] = max(dp[i][j], dp[i − z][j − o] + 1).",
                why="Each string is an item with two weights and value 1; descending loops use it once.",
            ),
            Choice(
                "Every subset of strings", SUBOPTIMAL, time="O(2ᴸ)", space="O(L)", visual="backtrack",
                detail="Try all selections.",
                why="Correct, but exponential.",
            ),
            Choice(
                "Shortest strings first", INCORRECT, time="O(L log L)", space="O(1)", visual="greedy",
                detail="Pick strings with fewest characters.",
                why="Two resources: a short string can use the scarce one.",
            ),
            Choice(
                "Two separate knapsacks", INCORRECT, time="O(L·(m + n))", space="O(m + n)", visual="dp-1d",
                detail="Solve for zeros and ones separately and take the smaller.",
                why="The same strings must satisfy both limits.",
            ),
        ),
    ),
    Question(
        slug="lcp-47-security-check", number=None, title="Security Check",
        difficulty="Hard", topics=("dp",),
        ref="LCP 47", url="https://leetcode.cn/problems/oPs9Bm/",
        summary="Security rooms in a chain have capacities; each is first-in-first-out or last-in-first-out. M + 1 people pass through in order. Count the type settings (mod 10⁹ + 7) where person k is the first to leave the last room.",
        example="capacities = [2,2,3], k = 2  →  2",
        criterion="Which approach is O(N · k)?",
        hint="A FIFO room doesn't change who comes out first. How many people does a LIFO room of capacity c hold back?",
        choices=(
            Choice(
                "Count subsets of LIFO rooms with Σ(c − 1) = k", OPTIMAL, time="O(N·k)", space="O(k)", visual="dp-1d",
                detail="0/1 knapsack counting: for each room, ways[s] += ways[s − (c − 1)], s descending.",
                why="A LIFO room fills up and releases its last entrant first, delaying by c − 1 people. FIFO rooms delay nothing, so the delays must add to k.",
            ),
            Choice(
                "Simulate every type setting", SUBOPTIMAL, time="O(2ᴺ·M)", space="O(M)", visual="brute",
                detail="Try all 2ᴺ assignments and simulate.",
                why="Correct, but exponential.",
            ),
            Choice(
                "Count subsets with Σc = k", INCORRECT, time="O(N·k)", space="O(k)", visual="dp-1d",
                detail="Use full capacities as delays.",
                why="The person entering a full LIFO room is the one who comes out; the delay is c − 1.",
            ),
            Choice(
                "Choose rooms freely", INCORRECT, time="O(1)", space="O(1)", visual="math",
                detail="2ᴺ settings.",
                why="Only settings with the right total delay work.",
            ),
        ),
    ),
    Question(
        slug="maximum-profit-from-trading-stocks", number=2291, title="Maximum Profit From Trading Stocks",
        difficulty="Medium", topics=("dp",),
        summary="Buy each stock at most once at present[i] within budget, and sell next year at future[i]. Return the maximum profit.",
        example="present = [5,4,6,2,3], future = [8,5,4,3,5], budget = 10  →  6",
        criterion="Which approach is O(n · budget)?",
        hint="Each stock has a cost and a profit.",
        choices=(
            Choice(
                "0/1 knapsack, budget descending", OPTIMAL, time="O(n·budget)", space="O(budget)", visual="dp-1d",
                detail="For profitable stocks, dp[b] = max(dp[b], dp[b − cost] + gain).",
                why="Classic knapsack: weight present[i], value future[i] − present[i], each used once.",
            ),
            Choice(
                "Every subset", SUBOPTIMAL, time="O(2ⁿ)", space="O(n)", visual="backtrack",
                detail="Try all purchase sets.",
                why="Correct, but exponential.",
            ),
            Choice(
                "Best profit ratio first", INCORRECT, time="O(n log n)", space="O(1)", visual="greedy",
                detail="Buy by gain/cost.",
                why="Items can't be split, so ratio greed can leave budget unused.",
            ),
            Choice(
                "Budget ascending", INCORRECT, time="O(n·budget)", space="O(budget)", visual="dp-1d",
                detail="Same DP with b increasing.",
                why="That buys the same stock more than once.",
            ),
        ),
    ),
    Question(
        slug="maximize-total-tastiness-of-purchased-fruits", number=2431, title="Maximize Total Tastiness of Purchased Fruits",
        difficulty="Medium", topics=("dp",),
        summary="Buy fruits within maxAmount to maximize tastiness; up to maxCoupons fruits can be bought at half price (rounded down).",
        example="price = [10,20,20], tastiness = [5,8,8], maxAmount = 20, maxCoupons = 1  →  13",
        criterion="Which approach is O(n · amount · coupons)?",
        hint="Add the number of coupons used as a knapsack dimension.",
        choices=(
            Choice(
                "Knapsack over (money, coupons)", OPTIMAL, time="O(n·A·C)", space="O(A·C)", visual="dp-2d",
                detail="Each fruit: skip, buy at full price, or buy with a coupon at half price.",
                why="A coupon is a second limited resource, so it becomes a second dimension of the 0/1 knapsack.",
            ),
            Choice(
                "Try every coupon assignment", SUBOPTIMAL, time="O(3ⁿ)", space="O(n)", visual="backtrack",
                detail="Each fruit has three options; enumerate.",
                why="Correct, but exponential.",
            ),
            Choice(
                "Coupons on the most expensive", INCORRECT, time="O(n·A)", space="O(A)", visual="greedy",
                detail="Use coupons on the priciest fruits, then knapsack.",
                why="The best coupon targets depend on which fruits are bought.",
            ),
            Choice(
                "Ignore coupons", INCORRECT, time="O(n·A)", space="O(A)", visual="dp-1d",
                detail="Plain knapsack at full price.",
                why="Example 2 needs coupons to afford both fruits.",
            ),
        ),
    ),
    Question(
        slug="maximum-weight-in-two-bags", number=3647, title="Maximum Weight in Two Bags",
        difficulty="Medium", topics=("dp",),
        summary="Put each item in bag 1 (capacity w1), bag 2 (capacity w2) or neither. Return the most total weight packed.",
        example="weights = [1,4,3,2], w1 = 5, w2 = 4  →  9",
        criterion="Which approach is O(n · w1 · w2)?",
        hint="Track how full both bags are at once.",
        choices=(
            Choice(
                "2-D reachability knapsack", OPTIMAL, time="O(n·w1·w2)", space="O(w1·w2)", visual="dp-2d",
                detail="can[a][b] |= can[a − x][b] or can[a][b − x], iterating a and b downward; answer the best reachable a + b.",
                why="Both bags share the items, so their fills must be decided together.",
            ),
            Choice(
                "Try every assignment", SUBOPTIMAL, time="O(3ⁿ)", space="O(n)", visual="backtrack",
                detail="Each item goes to bag 1, bag 2 or neither.",
                why="Correct, but exponential.",
            ),
            Choice(
                "Fill bag 1 best, then bag 2", INCORRECT, time="O(n·(w1 + w2))", space="O(w1 + w2)", visual="dp-1d",
                detail="Two knapsacks in sequence.",
                why="Bag 1's best fill can take items bag 2 needed.",
            ),
            Choice(
                "One bag of size w1 + w2", INCORRECT, time="O(n·(w1 + w2))", space="O(w1 + w2)", visual="dp-1d",
                detail="Merge the bags.",
                why="An item can't straddle two bags.",
            ),
        ),
    ),
    Question(
        slug="number-of-ways-to-build-house-of-cards", number=2189, title="Number of Ways to Build House of Cards",
        difficulty="Medium", topics=("dp",),
        summary="A row of t triangles uses 3t − 1 cards; each higher row sits on horizontal cards, so it has fewer triangles. Count distinct houses using exactly n cards.",
        example="16  →  2",
        criterion="Which approach is O(n²)?",
        hint="A house is a set of distinct row sizes.",
        choices=(
            Choice(
                "0/1 knapsack over row sizes", OPTIMAL, time="O(n²)", space="O(n)", visual="dp-1d",
                detail="For t = 1, 2, …, ways[c] += ways[c − (3t − 1)] with c descending.",
                why="Rows strictly shrink upward, so a house is a set of distinct t's. Counting subsets by total cards is a 0/1 knapsack.",
            ),
            Choice(
                "Recursion on the bottom row", SUBOPTIMAL, time="Exponential", space="O(n)", visual="recursion",
                detail="Pick the bottom row, recurse on smaller rows without memo.",
                why="Correct, but recomputes subproblems.",
            ),
            Choice(
                "Complete knapsack", INCORRECT, time="O(n²)", space="O(n)", visual="dp-1d",
                detail="Allow a row size to repeat.",
                why="Two rows with the same number of triangles can't stack.",
            ),
            Choice(
                "Count row sizes that divide n", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="One house per t with 3t − 1 dividing n.",
                why="Houses mix different row sizes.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §3.2 unbounded knapsack
    Question(
        slug="coin-change", number=322, title="Coin Change",
        difficulty="Medium", topics=("dp",),
        summary="Return the fewest coins (unlimited of each kind) that make amount, or −1.",
        example="[1,2,5], 11  →  3",
        criterion="Which approach is O(n · amount)?",
        hint="The last coin used can be any denomination.",
        choices=(
            Choice(
                "Unbounded knapsack for the minimum", OPTIMAL, time="O(n·amount)", space="O(amount)", visual="dp-1d",
                detail="dp[a] = min over coins of dp[a − c] + 1, with a ascending.",
                why="Ascending a lets a coin be reused, and each amount's best splits on its last coin.",
            ),
            Choice(
                "BFS over amounts", SUBOPTIMAL, time="O(n·amount)", space="O(amount)", visual="graph-bfs",
                detail="Each level adds one coin; stop at amount.",
                why="Correct and the same bound, but with queue overhead.",
            ),
            Choice(
                "Largest coin first", INCORRECT, time="O(n log n)", space="O(1)", visual="greedy",
                detail="Take as many of the biggest coin as fit, then the next.",
                why="For [1,3,4] and 6, greed takes 4+1+1; 3+3 uses two.",
            ),
            Choice(
                "0/1 knapsack", INCORRECT, time="O(n·amount)", space="O(amount)", visual="dp-1d",
                detail="Iterate a descending.",
                why="Each coin could then be used only once.",
            ),
        ),
    ),
    Question(
        slug="coin-change-ii", number=518, title="Coin Change II",
        difficulty="Medium", topics=("dp",),
        summary="Count the combinations (order doesn't matter) of coins that make amount.",
        example="amount = 5, coins = [1,2,5]  →  4",
        criterion="Which approach counts each combination once in O(n · amount)?",
        hint="Which loop goes outside: coins or amounts?",
        choices=(
            Choice(
                "Coins outer, amount inner ascending", OPTIMAL, time="O(n·amount)", space="O(amount)", visual="dp-1d",
                detail="ways[0] = 1; for each coin c, for a from c to amount: ways[a] += ways[a − c].",
                why="Processing coins in a fixed order builds each multiset in one canonical order, so it's counted once.",
            ),
            Choice(
                "Backtracking with a start index", SUBOPTIMAL, time="Exponential", space="O(amount)", visual="backtrack",
                detail="Enumerate non-decreasing coin choices.",
                why="Correct, but exponential in the count.",
            ),
            Choice(
                "Amount outer, coins inner", INCORRECT, time="O(n·amount)", space="O(amount)", visual="dp-1d",
                detail="Combination Sum IV's order.",
                why="That counts 1+2+2 and 2+1+2 separately.",
            ),
            Choice(
                "Amount descending", INCORRECT, time="O(n·amount)", space="O(amount)", visual="dp-1d",
                detail="0/1 order.",
                why="Each coin could be used only once.",
            ),
        ),
    ),
    Question(
        slug="perfect-squares", number=279, title="Perfect Squares",
        difficulty="Medium", topics=("dp",),
        summary="Return the fewest perfect squares that sum to n.",
        example="12  →  3",
        criterion="Which approach is O(√n)?",
        hint="Every positive integer is a sum of at most four squares. When exactly do you need four?",
        choices=(
            Choice(
                "Number theory: check 1, 2, 4, else 3", OPTIMAL, time="O(√n)", space="O(1)", visual="math",
                detail="1 if n is a square; 4 if n = 4ᵃ(8b + 7); 2 if n − i² is a square for some i; else 3.",
                why="Lagrange's four-square theorem bounds the answer by 4, and Legendre's three-square theorem tells exactly when 4 is needed.",
            ),
            Choice(
                "Unbounded knapsack DP", SUBOPTIMAL, time="O(n√n)", space="O(n)", visual="dp-1d",
                detail="dp[i] = 1 + min over squares s ≤ i of dp[i − s].",
                why="Correct and the expected DP, but slower than the closed test.",
            ),
            Choice(
                "Largest square first", INCORRECT, time="O(√n)", space="O(1)", visual="greedy",
                detail="Subtract the biggest square repeatedly.",
                why="12 → 9 + 1 + 1 + 1 is four; 4 + 4 + 4 is three.",
            ),
            Choice(
                "Digit sum", INCORRECT, time="O(log n)", space="O(1)", visual="math",
                detail="Unrelated shortcut.",
                why="Squares don't relate to decimal digits.",
            ),
        ),
    ),
    Question(
        slug="minimum-number-of-primes-to-sum-to-target", number=3610, title="Minimum Number of Primes to Sum to Target",
        difficulty="Medium", topics=("dp",),
        summary="Using the first m primes (each any number of times), return the fewest primes summing to n, or −1.",
        example="n = 10, m = 2  →  4",
        criterion="Which approach is O(n · m)?",
        hint="Coin change with primes as coins.",
        choices=(
            Choice(
                "Sieve, then unbounded knapsack", OPTIMAL, time="O(n·m)", space="O(n)", visual="dp-1d",
                detail="Get the first m primes; dp[a] = min dp[a − p] + 1.",
                why="It's coin change for the minimum, with the primes as denominations.",
            ),
            Choice(
                "BFS over sums", SUBOPTIMAL, time="O(n·m)", space="O(n)", visual="graph-bfs",
                detail="Each level adds a prime.",
                why="Correct, with queue overhead.",
            ),
            Choice(
                "Largest prime first", INCORRECT, time="O(m)", space="O(1)", visual="greedy",
                detail="Take the biggest prime that fits, repeatedly.",
                why="For n = 10 with [2,3], greed takes 3,3,3 and gets stuck at 1.",
            ),
            Choice(
                "Goldbach: at most 3", INCORRECT, time="O(1)", space="O(1)", visual="math",
                detail="Answer 1, 2 or 3 by parity.",
                why="Only the first m primes are allowed.",
            ),
        ),
    ),
    Question(
        slug="the-number-of-ways-to-make-the-sum", number=3183, title="The Number of Ways to Make the Sum",
        difficulty="Medium", topics=("dp",),
        summary="Coins 1, 2 and 6 are unlimited; there are only two coins of 4. Count the combinations that make n, mod 10⁹ + 7.",
        example="12  →  22",
        criterion="Which approach is O(n)?",
        hint="Handle the limited coin separately: you use zero, one or two 4s.",
        choices=(
            Choice(
                "Complete knapsack on 1, 2, 6, then add 0–2 fours", OPTIMAL, time="O(n)", space="O(n)", visual="dp-1d",
                detail="f = combinations of {1, 2, 6}; answer f[n] + f[n − 4] + f[n − 8].",
                why="The 4s are independent of the rest, so the answer splits by how many 4s are used.",
            ),
            Choice(
                "Knapsack with a 4-count dimension", SUBOPTIMAL, time="O(3n)", space="O(3n)", visual="dp-2d",
                detail="dp[a][j] with j fours used.",
                why="Correct, but carries a dimension the split removes.",
            ),
            Choice(
                "Treat 4 as unlimited", INCORRECT, time="O(n)", space="O(n)", visual="dp-1d",
                detail="Complete knapsack on all four coins.",
                why="That counts [4, 4, 4] for 12.",
            ),
            Choice(
                "Count ordered sequences", INCORRECT, time="O(n)", space="O(n)", visual="dp-1d",
                detail="Amount in the outer loop.",
                why="Order doesn't matter here.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §3.4 grouped knapsack
    Question(
        slug="number-of-dice-rolls-with-target-sum", number=1155, title="Number of Dice Rolls With Target Sum",
        difficulty="Medium", topics=("dp",),
        summary="Roll n dice with k faces each. Count the ways the faces sum to target, mod 10⁹ + 7.",
        example="n = 2, k = 6, target = 7  →  6",
        criterion="Which approach is O(n · target)?",
        hint="Each die picks one face from a group. The new count is a window sum of the old counts.",
        choices=(
            Choice(
                "Grouped knapsack with prefix sums", OPTIMAL, time="O(n·target)", space="O(target)", visual="prefix",
                detail="new[s] = Σ old[s − f] for f in 1..k, computed as a prefix-sum difference.",
                why="Each die contributes a sliding window of k previous counts; prefix sums give each window in O(1).",
            ),
            Choice(
                "Grouped knapsack, loop over faces", SUBOPTIMAL, time="O(n·k·target)", space="O(target)", visual="dp-1d",
                detail="For each die, sum the k previous counts directly.",
                why="Correct and the standard version, but redoes overlapping windows.",
            ),
            Choice(
                "Complete knapsack on faces", INCORRECT, time="O(k·target)", space="O(target)", visual="dp-1d",
                detail="Any number of each face.",
                why="Exactly n dice must be used.",
            ),
            Choice(
                "Combinations of faces", INCORRECT, time="O(n·k·target)", space="O(target)", visual="dp-2d",
                detail="Count multisets of faces.",
                why="Dice are distinct: (1,6) and (6,1) differ.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §4.1 longest common subsequence
    Question(
        slug="longest-common-subsequence", number=1143, title="Longest Common Subsequence",
        difficulty="Medium", topics=("dp",),
        summary="Return the length of the longest subsequence common to text1 and text2.",
        example="\"abcde\", \"ace\"  →  3",
        criterion="Which approach is O(m·n)?",
        hint="Compare the last characters. If they match, what's left? If not?",
        choices=(
            Choice(
                "dp[i][j] on prefixes", OPTIMAL, time="O(m·n)", space="O(min(m, n))", visual="dp-2d",
                detail="Match: dp[i−1][j−1] + 1; else max(dp[i−1][j], dp[i][j−1]).",
                why="Each pair of prefixes depends on three smaller ones, so the table fills in O(1) per cell (one row of state suffices).",
            ),
            Choice(
                "Recursion without memo", SUBOPTIMAL, time="O(2^(m+n))", space="O(m + n)", visual="recursion",
                detail="Branch on dropping a character from either string.",
                why="Correct, but the same prefix pairs are solved again and again.",
            ),
            Choice(
                "Count shared characters", INCORRECT, time="O(m + n)", space="O(Σ)", visual="counting",
                detail="Sum min(count1[c], count2[c]).",
                why="\"ab\" and \"ba\" share both letters but their LCS is 1.",
            ),
            Choice(
                "Longest common substring", INCORRECT, time="O(m·n)", space="O(n)", visual="dp-2d",
                detail="Reset to 0 on a mismatch.",
                why="A subsequence can skip characters: \"ace\" in \"abcde\".",
            ),
        ),
    ),
    Question(
        slug="delete-operation-for-two-strings", number=583, title="Delete Operation for Two Strings",
        difficulty="Medium", topics=("dp",),
        summary="One step deletes one character from either string. Return the fewest steps to make them equal.",
        example="\"sea\", \"eat\"  →  2",
        criterion="Which approach is O(m·n)?",
        hint="What's left when both strings become equal?",
        choices=(
            Choice(
                "m + n − 2·LCS", OPTIMAL, time="O(m·n)", space="O(n)", visual="dp-2d",
                detail="Compute the LCS length by DP.",
                why="The final common string is a common subsequence; keeping the longest one deletes the fewest characters.",
            ),
            Choice(
                "BFS over deletions", SUBOPTIMAL, time="Exponential", space="Exponential", visual="queue",
                detail="Delete one character per level until equal.",
                why="Correct, but the state space explodes.",
            ),
            Choice(
                "|m − n|", INCORRECT, time="O(1)", space="O(1)", visual="math",
                detail="Delete from the longer one only.",
                why="\"sea\" and \"eat\" have equal length but differ.",
            ),
            Choice(
                "Mismatched positions", INCORRECT, time="O(min(m, n))", space="O(1)", visual="two-pointers",
                detail="Count indices where the characters differ.",
                why="Deleting shifts later characters; position-by-position comparison doesn't model that.",
            ),
        ),
    ),
    Question(
        slug="minimum-ascii-delete-sum-for-two-strings", number=712, title="Minimum ASCII Delete Sum for Two Strings",
        difficulty="Medium", topics=("dp",),
        summary="Delete characters from both strings to make them equal, minimizing the total ASCII value deleted.",
        example="\"sea\", \"eat\"  →  231",
        criterion="Which approach is O(m·n)?",
        hint="It's the deletion problem with weights.",
        choices=(
            Choice(
                "Weighted LCS DP", OPTIMAL, time="O(m·n)", space="O(n)", visual="dp-2d",
                detail="dp[i][j] = cheapest cost for the prefixes; match: dp[i−1][j−1]; else min(dp[i−1][j] + s1[i], dp[i][j−1] + s2[j]).",
                why="Same structure as LCS, but each deletion pays its character's ASCII value.",
            ),
            Choice(
                "Recursion without memo", SUBOPTIMAL, time="O(2^(m+n))", space="O(m + n)", visual="recursion",
                detail="Branch on deleting from either string.",
                why="Correct, but exponential.",
            ),
            Choice(
                "Use the longest LCS", INCORRECT, time="O(m·n)", space="O(n)", visual="dp-2d",
                detail="Keep a longest common subsequence and delete the rest.",
                why="The longest kept string isn't always the most valuable; keeping fewer but larger characters can cost less.",
            ),
            Choice(
                "Delete all differing characters", INCORRECT, time="O(m + n)", space="O(Σ)", visual="counting",
                detail="Remove letters not in both strings.",
                why="Shared letters in a different order still need deletions.",
            ),
        ),
    ),
    Question(
        slug="edit-distance", number=72, title="Edit Distance",
        difficulty="Medium", topics=("dp",),
        summary="Return the fewest inserts, deletes and replacements to turn word1 into word2.",
        example="\"horse\", \"ros\"  →  3",
        criterion="Which approach is O(m·n)?",
        hint="Look at the last characters: equal, or one of three operations.",
        choices=(
            Choice(
                "dp[i][j] with three operations", OPTIMAL, time="O(m·n)", space="O(n)", visual="dp-2d",
                detail="Equal: dp[i−1][j−1]; else 1 + min(insert dp[i][j−1], delete dp[i−1][j], replace dp[i−1][j−1]).",
                why="The last characters must end up aligned somehow, and each case reduces to smaller prefixes.",
            ),
            Choice(
                "BFS over edited strings", SUBOPTIMAL, time="Exponential", space="Exponential", visual="queue",
                detail="Apply every edit at every level.",
                why="Correct, but the number of strings explodes.",
            ),
            Choice(
                "m + n − 2·LCS", INCORRECT, time="O(m·n)", space="O(n)", visual="dp-2d",
                detail="Count insertions and deletions only.",
                why="A replacement does in one step what delete + insert does in two.",
            ),
            Choice(
                "Mismatches plus the length difference", INCORRECT, time="O(m + n)", space="O(1)", visual="two-pointers",
                detail="Compare position by position.",
                why="\"horse\" → \"ros\" aligns h-r-s with r-o-s only after deleting.",
            ),
        ),
    ),
    Question(
        slug="maximum-length-of-repeated-subarray", number=718, title="Maximum Length of Repeated Subarray",
        difficulty="Medium", topics=("dp",),
        summary="Return the length of the longest subarray that appears in both arrays.",
        example="[1,2,3,2,1], [3,2,1,4,7]  →  3",
        criterion="Which approach is O(m·n)?",
        hint="Unlike LCS, a mismatch breaks the run.",
        choices=(
            Choice(
                "dp[i][j] = common suffix length", OPTIMAL, time="O(m·n)", space="O(n)", visual="dp-2d",
                detail="Equal: dp[i−1][j−1] + 1; else 0; track the max.",
                why="A common subarray ending at i and j extends the one ending at i − 1 and j − 1, or doesn't exist.",
            ),
            Choice(
                "Compare every pair of starts", SUBOPTIMAL, time="O(m·n·min(m, n))", space="O(1)", visual="brute",
                detail="Extend from each (i, j) while equal.",
                why="Correct, but overlapping runs are re-walked.",
            ),
            Choice(
                "LCS", INCORRECT, time="O(m·n)", space="O(n)", visual="dp-2d",
                detail="Longest common subsequence.",
                why="A subarray must be contiguous.",
            ),
            Choice(
                "Common elements", INCORRECT, time="O(m + n)", space="O(m)", visual="set",
                detail="Count values present in both.",
                why="Shared values needn't be adjacent.",
            ),
        ),
    ),
    Question(
        slug="maximum-multiplication-score", number=3290, title="Maximum Multiplication Score",
        difficulty="Medium", topics=("dp",),
        summary="a has 4 numbers. Choose indices i0 < i1 < i2 < i3 in b to maximize a[0]·b[i0] + a[1]·b[i1] + a[2]·b[i2] + a[3]·b[i3].",
        example="a = [3,2,5,6], b = [2,-6,4,-5,-3,2,-7]  →  26",
        criterion="Which approach is O(n)?",
        hint="Walk through b once. For each j, what's the best score having matched the first j numbers of a?",
        choices=(
            Choice(
                "Four running best values", OPTIMAL, time="O(4·n)", space="O(1)", visual="dp-1d",
                detail="For each b[i], update f[j] = max(f[j], f[j − 1] + a[j]·b[i]) for j from 3 down to 0.",
                why="It's LCS-style matching of a into b; updating j downward uses each b[i] at most once.",
            ),
            Choice(
                "All index quadruples", SUBOPTIMAL, time="O(n⁴)", space="O(1)", visual="brute",
                detail="Try every i0 < i1 < i2 < i3.",
                why="Correct, but quartic.",
            ),
            Choice(
                "Best product for each a[k] separately", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Pick the best b for each a[k] independently.",
                why="The indices must be increasing.",
            ),
            Choice(
                "Sort b", INCORRECT, time="O(n log n)", space="O(n)", visual="sort",
                detail="Match sorted a with sorted b.",
                why="Order in b matters.",
            ),
        ),
    ),
    Question(
        slug="distinct-subsequences", number=115, title="Distinct Subsequences",
        difficulty="Hard", topics=("dp",),
        summary="Count the distinct ways t appears as a subsequence of s.",
        example="\"rabbbit\", \"rabbit\"  →  3",
        criterion="Which approach is O(m·n)?",
        hint="For s[i] = t[j], you may use it for t[j] or not.",
        choices=(
            Choice(
                "dp[i][j] = ways to form t[..j] from s[..i]", OPTIMAL, time="O(m·n)", space="O(n)", visual="dp-2d",
                detail="dp[i][j] = dp[i−1][j] + (s[i] == t[j] ? dp[i−1][j−1] : 0).",
                why="Each occurrence either skips s[i] or uses it to match t[j]; these cases don't overlap.",
            ),
            Choice(
                "Enumerate matches recursively", SUBOPTIMAL, time="Exponential", space="O(n)", visual="recursion",
                detail="Count matches without memo.",
                why="Correct, but exponential.",
            ),
            Choice(
                "Whether t is a subsequence", INCORRECT, time="O(m)", space="O(1)", visual="two-pointers",
                detail="Greedy two-pointer check.",
                why="That's a yes/no, not a count.",
            ),
            Choice(
                "Product of letter counts", INCORRECT, time="O(m)", space="O(Σ)", visual="math",
                detail="Multiply how often each needed letter appears.",
                why="Order matters: matched letters must be in sequence.",
            ),
        ),
    ),
    Question(
        slug="interleaving-string", number=97, title="Interleaving String",
        difficulty="Medium", topics=("dp",),
        summary="Return whether s3 is formed by interleaving s1 and s2 (keeping each one's order).",
        example="\"aabcc\", \"dbbca\", \"aadbbcbcac\"  →  true",
        criterion="Which approach is O(m·n)?",
        hint="After using i letters of s1 and j of s2, the next letter of s3 is fixed.",
        choices=(
            Choice(
                "dp[i][j] = s3 prefix reachable", OPTIMAL, time="O(m·n)", space="O(n)", visual="dp-2d",
                detail="dp[i][j] = (dp[i−1][j] and s1[i−1] == s3[i+j−1]) or (dp[i][j−1] and s2[j−1] == s3[i+j−1]).",
                why="The position in s3 is i + j, so (i, j) fully describes progress.",
            ),
            Choice(
                "Backtracking", SUBOPTIMAL, time="O(2^(m+n))", space="O(m + n)", visual="backtrack",
                detail="Try taking from s1 or s2 when both match.",
                why="Correct, but re-explores the same (i, j).",
            ),
            Choice(
                "Prefer s1 when both match", INCORRECT, time="O(m + n)", space="O(1)", visual="greedy",
                detail="Greedy two pointers.",
                why="Taking the wrong 'a' early can make s3 impossible later.",
            ),
            Choice(
                "Letter counts match", INCORRECT, time="O(m + n)", space="O(Σ)", visual="counting",
                detail="Check s1 + s2 is an anagram of s3.",
                why="Order within s1 and s2 must be kept.",
            ),
        ),
    ),
    Question(
        slug="wildcard-matching", number=44, title="Wildcard Matching",
        difficulty="Hard", topics=("dp",),
        summary="'?' matches any single character and '*' any sequence (including empty). Return whether the pattern matches the whole string.",
        example="\"adceb\", \"*a*b\"  →  true",
        criterion="Which approach is O(m·n)?",
        hint="A '*' either matches nothing or eats one more character.",
        choices=(
            Choice(
                "dp[i][j] on prefixes", OPTIMAL, time="O(m·n)", space="O(n)", visual="dp-2d",
                detail="'*': dp[i][j−1] (empty) or dp[i−1][j] (one more char); '?' or equal: dp[i−1][j−1].",
                why="Letting '*' consume one character at a time turns its many choices into two transitions.",
            ),
            Choice(
                "Recursion without memo", SUBOPTIMAL, time="Exponential", space="O(m + n)", visual="recursion",
                detail="Try every length for each '*'.",
                why="Correct, but consecutive stars explode.",
            ),
            Choice(
                "'*' matches exactly one character", INCORRECT, time="O(m·n)", space="O(n)", visual="dp-2d",
                detail="Treat '*' like '?'.",
                why="\"aa\" with \"*\" should match.",
            ),
            Choice(
                "Regex '*' rules", INCORRECT, time="O(m·n)", space="O(n)", visual="dp-2d",
                detail="Make '*' repeat the previous character.",
                why="Here '*' stands alone and matches any sequence.",
            ),
        ),
    ),
    Question(
        slug="regular-expression-matching", number=10, title="Regular Expression Matching",
        difficulty="Hard", topics=("dp",),
        summary="'.' matches any character and 'x*' matches zero or more x. Return whether the pattern matches the whole string.",
        example="\"aab\", \"c*a*b\"  →  true",
        criterion="Which approach is O(m·n)?",
        hint="'x*' either disappears or matches one more x.",
        choices=(
            Choice(
                "dp[i][j] on prefixes", OPTIMAL, time="O(m·n)", space="O(n)", visual="dp-2d",
                detail="If p[j−1] is '*': dp[i][j−2] (zero copies) or (match s[i−1] with p[j−2] and dp[i−1][j]); else character match and dp[i−1][j−1].",
                why="Each 'x*' has two moves: vanish or consume one character while staying, so each cell is O(1).",
            ),
            Choice(
                "Backtracking", SUBOPTIMAL, time="Exponential", space="O(m + n)", visual="backtrack",
                detail="Try each repeat count for every 'x*'.",
                why="Correct, but exponential on patterns like a*a*a*.",
            ),
            Choice(
                "'*' as a glob wildcard", INCORRECT, time="O(m·n)", space="O(n)", visual="dp-2d",
                detail="'*' matches any sequence.",
                why="'c*' means some c's, not anything.",
            ),
            Choice(
                "'x*' needs at least one x", INCORRECT, time="O(m·n)", space="O(n)", visual="dp-2d",
                detail="Treat 'x*' like 'x+'.",
                why="\"c*\" must match the empty prefix in the example.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §4.2 longest increasing subsequence
    Question(
        slug="longest-increasing-subsequence", number=300, title="Longest Increasing Subsequence",
        difficulty="Medium", topics=("dp",),
        summary="Return the length of the longest strictly increasing subsequence.",
        example="[10,9,2,5,3,7,101,18]  →  4",
        criterion="Which approach is O(n log n)?",
        hint="For each length, keep the smallest possible tail.",
        choices=(
            Choice(
                "Tails array with binary search", OPTIMAL, time="O(n log n)", space="O(n)", visual="binary-search",
                detail="For x, replace the first tail ≥ x, or append if none.",
                why="Tails stay sorted, and a smaller tail can only help future extensions, so one search per element suffices.",
            ),
            Choice(
                "dp[i] over all j < i", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="dp-1d",
                detail="dp[i] = 1 + max dp[j] with nums[j] < nums[i].",
                why="Correct and classic, but quadratic.",
            ),
            Choice(
                "Longest increasing run", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Longest contiguous increasing stretch.",
                why="A subsequence can skip elements: 2, 3, 7, 18.",
            ),
            Choice(
                "Tails with lower bound on '>'", INCORRECT, time="O(n log n)", space="O(n)", visual="binary-search",
                detail="Replace the first tail > x.",
                why="Equal values would then extend the sequence, but it must be strictly increasing.",
            ),
        ),
    ),
    Question(
        slug="increasing-triplet-subsequence", number=334, title="Increasing Triplet Subsequence",
        difficulty="Medium", topics=("dp",),
        summary="Return whether there are i < j < k with nums[i] < nums[j] < nums[k].",
        example="[2,1,5,0,4,6]  →  true",
        criterion="Which approach is linear with O(1) extra space?",
        hint="It's the LIS tails array, capped at length 2.",
        choices=(
            Choice(
                "Two tails: first and second", OPTIMAL, time="O(n)", space="O(1)", visual="greedy",
                detail="x ≤ first → first = x; else x ≤ second → second = x; else true.",
                why="first and second are the smallest tails of increasing runs of length 1 and 2; anything above second completes a triple.",
            ),
            Choice(
                "Prefix min and suffix max", SUBOPTIMAL, time="O(n)", space="O(n)", visual="prefix",
                detail="Check prefMin[j] < nums[j] < sufMax[j].",
                why="Correct and linear, but uses two arrays.",
            ),
            Choice(
                "Adjacent triples", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Look for three increasing neighbours.",
                why="[5,1,6,2,7] has no three increasing neighbours, yet 5 < 6 < 7.",
            ),
            Choice(
                "Reset second when first drops", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="When x < first, set first = x and clear second.",
                why="In [2,4,1,5], clearing forgets that 2 < 4 already exists, so 5 isn't seen as a third.",
            ),
        ),
    ),
    Question(
        slug="russian-doll-envelopes", number=354, title="Russian Doll Envelopes",
        difficulty="Hard", topics=("dp",),
        summary="An envelope fits in another if both width and height are strictly smaller. Return the most envelopes you can nest.",
        example="[[5,4],[6,4],[6,7],[2,3]]  →  3",
        criterion="Which approach is O(n log n)?",
        hint="Sort by width. How should equal widths be ordered so LIS on heights can't chain them?",
        choices=(
            Choice(
                "Sort width ↑, height ↓ on ties, then LIS on heights", OPTIMAL, time="O(n log n)", space="O(n)", visual="sort",
                detail="Run the tails-array LIS on the heights.",
                why="Descending heights within a width make same-width envelopes unable to form an increasing pair.",
            ),
            Choice(
                "Sort, then O(n²) DP", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="dp-1d",
                detail="dp[i] = 1 + max dp[j] for envelopes that fit.",
                why="Correct, but quadratic for 10⁵ envelopes.",
            ),
            Choice(
                "Sort both ascending", INCORRECT, time="O(n log n)", space="O(n)", visual="sort",
                detail="Ties by height ascending, then LIS on heights.",
                why="[6,4] then [6,7] would chain, but equal widths can't nest.",
            ),
            Choice(
                "Sort by area", INCORRECT, time="O(n log n)", space="O(n)", visual="sort",
                detail="Nest by increasing area.",
                why="A wide flat envelope has a big area but can't hold a narrow tall one.",
            ),
        ),
    ),
    Question(
        slug="number-of-longest-increasing-subsequence", number=673, title="Number of Longest Increasing Subsequence",
        difficulty="Medium", topics=("dp",),
        summary="Return how many longest strictly increasing subsequences there are.",
        example="[1,3,5,4,7]  →  2",
        criterion="Which approach is O(n²) and counts every LIS?",
        hint="For each end, track both the best length and how many ways reach it.",
        choices=(
            Choice(
                "Length and count per index", OPTIMAL, time="O(n²)", space="O(n)", visual="dp-1d",
                detail="For j < i with nums[j] < nums[i]: a longer length resets cnt[i] = cnt[j]; an equal one adds cnt[j].",
                why="Every LIS ending at i extends some best sequence ending at a smaller value, so counts add along equal-length links.",
            ),
            Choice(
                "Enumerate increasing subsequences", SUBOPTIMAL, time="Exponential", space="O(n)", visual="backtrack",
                detail="List all and count the longest.",
                why="Correct, but exponential.",
            ),
            Choice(
                "Count indices with the max length", INCORRECT, time="O(n²)", space="O(n)", visual="dp-1d",
                detail="Number of i with len[i] = max.",
                why="One end can be reached in several ways.",
            ),
            Choice(
                "LIS length", INCORRECT, time="O(n log n)", space="O(n)", visual="binary-search",
                detail="Return the length.",
                why="The task asks how many.",
            ),
        ),
    ),
    Question(
        slug="largest-divisible-subset", number=368, title="Largest Divisible Subset",
        difficulty="Medium", topics=("dp",),
        summary="Return a largest subset of distinct positive integers where every pair divides one way or the other.",
        example="[1,2,4,8]  →  [1,2,4,8]",
        criterion="Which approach is O(n²)?",
        hint="After sorting, a divisible subset is a chain where each element divides the next.",
        choices=(
            Choice(
                "Sort, LIS-style DP on divisibility with parents", OPTIMAL, time="O(n²)", space="O(n)", visual="dp-1d",
                detail="dp[i] = 1 + max dp[j] with nums[i] % nums[j] == 0; rebuild via parent links.",
                why="Divisibility is transitive, so checking each new element against the chain's last element is enough.",
            ),
            Choice(
                "Every subset", SUBOPTIMAL, time="O(2ⁿ·n²)", space="O(n)", visual="backtrack",
                detail="Check all pairs in all subsets.",
                why="Correct, but exponential.",
            ),
            Choice(
                "Multiples of the smallest", INCORRECT, time="O(n)", space="O(n)", visual="greedy",
                detail="Take everything divisible by the smallest value.",
                why="For [1,2,3], 2 and 3 are both multiples of 1 but don't divide each other.",
            ),
            Choice(
                "Unsorted DP", INCORRECT, time="O(n²)", space="O(n)", visual="dp-1d",
                detail="Same DP without sorting.",
                why="A divisor appearing later would never be chained before its multiple.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §5 partition DP
    Question(
        slug="word-break", number=139, title="Word Break",
        difficulty="Medium", topics=("dp",),
        summary="Return whether s can be split into words from wordDict (words reusable).",
        example="\"leetcode\", [\"leet\",\"code\"]  →  true",
        criterion="Which approach is O(n · L) set lookups (L = longest word)?",
        hint="Can the prefix ending at i be split? Look at the last word.",
        choices=(
            Choice(
                "dp[i] over the last word", OPTIMAL, time="O(n·L)", space="O(n)", visual="dp-1d",
                detail="dp[i] = some j in [i − L, i) with dp[j] and s[j..i) in the set.",
                why="A valid split's last word starts at some j with a valid prefix, and words longer than L can't exist.",
            ),
            Choice(
                "Backtracking", SUBOPTIMAL, time="Exponential", space="O(n)", visual="backtrack",
                detail="Try every word at every position without memo.",
                why="Correct, but re-explores failed suffixes.",
            ),
            Choice(
                "Greedy longest word", INCORRECT, time="O(n·L)", space="O(1)", visual="greedy",
                detail="Take the longest matching word each time.",
                why="\"cars\" with [\"car\",\"ca\",\"rs\"]: greedy takes \"car\" and fails.",
            ),
            Choice(
                "Every word appears in s", INCORRECT, time="O(n·W)", space="O(1)", visual="brute",
                detail="Check each dictionary word is a substring.",
                why="The pieces must cover s exactly.",
            ),
        ),
    ),
    Question(
        slug="palindrome-partitioning-ii", number=132, title="Palindrome Partitioning II",
        difficulty="Hard", topics=("dp",),
        summary="Return the fewest cuts that split s into palindromes.",
        example="\"aab\"  →  1",
        criterion="Which approach is O(n²)?",
        hint="Precompute which substrings are palindromes.",
        choices=(
            Choice(
                "isPal table, then dp over the last piece", OPTIMAL, time="O(n²)", space="O(n²)", visual="dp-2d",
                detail="dp[i] = 0 if s[0..i] is a palindrome, else min dp[j − 1] + 1 over palindromic s[j..i].",
                why="The table answers palindrome checks in O(1), so each end tries n starts.",
            ),
            Choice(
                "DP checking palindromes on the fly", SUBOPTIMAL, time="O(n³)", space="O(n)", visual="dp-1d",
                detail="Test s[j..i] with two pointers inside the DP.",
                why="Correct, but rechecks substrings.",
            ),
            Choice(
                "Greedy longest palindrome prefix", INCORRECT, time="O(n²)", space="O(n)", visual="greedy",
                detail="Cut off the longest palindrome each time.",
                why="\"aaba\" can be cut as \"a\" + \"aba\" with 1 cut; greedy takes \"aa\" then needs \"b\", \"a\".",
            ),
            Choice(
                "Number of distinct letters minus 1", INCORRECT, time="O(n)", space="O(Σ)", visual="counting",
                detail="One piece per letter.",
                why="\"aba\" needs 0 cuts.",
            ),
        ),
    ),
    Question(
        slug="decode-ways", number=91, title="Decode Ways",
        difficulty="Medium", topics=("dp",),
        summary="Digits map 1–26 to letters. Count the ways to decode s.",
        example="\"226\"  →  3",
        criterion="Which approach is linear with O(1) extra space?",
        hint="The last letter used one digit or two.",
        choices=(
            Choice(
                "f(i) from one- and two-digit endings", OPTIMAL, time="O(n)", space="O(1)", visual="dp-1d",
                detail="Add f(i − 1) if s[i − 1] ≠ '0'; add f(i − 2) if s[i−2..i−1] is 10–26.",
                why="Each decoding ends with a valid one- or two-digit code, like climbing stairs with conditions.",
            ),
            Choice(
                "Recursion without memo", SUBOPTIMAL, time="O(2ⁿ)", space="O(n)", visual="recursion",
                detail="Branch on one or two digits.",
                why="Correct, but exponential.",
            ),
            Choice(
                "Ignore zeros", INCORRECT, time="O(n)", space="O(1)", visual="dp-1d",
                detail="Treat '0' as a letter.",
                why="\"06\" has no decoding.",
            ),
            Choice(
                "Fibonacci of the length", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="Every pair of digits is a code.",
                why="\"27\" can't be read as one letter.",
            ),
        ),
    ),
    Question(
        slug="decode-ways-ii", number=639, title="Decode Ways II",
        difficulty="Hard", topics=("dp",),
        summary="Like Decode Ways, but '*' stands for any digit 1–9. Count decodings mod 10⁹ + 7.",
        example="\"1*\"  →  18",
        criterion="Which approach is linear with O(1) extra space?",
        hint="How many one-digit and two-digit codes can each character or pair stand for?",
        choices=(
            Choice(
                "Decode Ways with multiplicities", OPTIMAL, time="O(n)", space="O(1)", visual="dp-1d",
                detail="f(i) = one(c)·f(i − 1) + two(p, c)·f(i − 2), where one/two count the valid codes for '*' cases (e.g. '*' alone = 9, '**' = 15).",
                why="The recurrence is the same; each step just weights the two endings by how many codes they can be.",
            ),
            Choice(
                "Expand every '*'", SUBOPTIMAL, time="O(9ᵏ·n)", space="O(n)", visual="brute",
                detail="Try all digits for each star and run Decode Ways.",
                why="Correct, but exponential in the number of stars.",
            ),
            Choice(
                "'*' as 0–9", INCORRECT, time="O(n)", space="O(1)", visual="dp-1d",
                detail="Ten choices per star.",
                why="'*' never stands for 0.",
            ),
            Choice(
                "Count '**' as 9 × 9 two-digit codes", INCORRECT, time="O(n)", space="O(1)", visual="dp-1d",
                detail="Every star pair forms a valid two-digit code.",
                why="Only 11–19 and 21–26 work: 15 codes.",
            ),
        ),
    ),
    Question(
        slug="lcr-165-decrypt-number", number=None, title="Decrypt Number",
        difficulty="Medium", topics=("dp",),
        ref="LCR 165", url="https://leetcode.cn/problems/ba-shu-zi-fan-yi-cheng-zi-fu-chuan-lcof/",
        summary="Digits 0–25 map to letters a–z. Count the ways to decode a non-negative integer.",
        example="216612  →  6",
        criterion="Which approach is linear in the number of digits?",
        hint="Which two-digit numbers are valid here?",
        choices=(
            Choice(
                "f(i) = f(i − 1) + (10 ≤ last two ≤ 25 ? f(i − 2) : 0)", OPTIMAL, time="O(d)", space="O(1)", visual="dp-1d",
                detail="Walk the digits with two rolling values.",
                why="Every single digit is a letter here; a pair counts only from 10 to 25 (no leading zero).",
            ),
            Choice(
                "Recursion without memo", SUBOPTIMAL, time="O(2ᵈ)", space="O(d)", visual="recursion",
                detail="Branch on one or two digits.",
                why="Correct, but exponential.",
            ),
            Choice(
                "Allow 00–09 as pairs", INCORRECT, time="O(d)", space="O(1)", visual="dp-1d",
                detail="Any two digits ≤ 25.",
                why="\"06\" isn't a two-digit code; it's 0 then 6.",
            ),
            Choice(
                "Decode Ways rules", INCORRECT, time="O(d)", space="O(1)", visual="dp-1d",
                detail="1–26, zero can't stand alone.",
                why="Here 0 is 'a' and 26 isn't a letter.",
            ),
        ),
    ),
    Question(
        slug="minimum-cost-to-separate-sentence-into-rows", number=2052, title="Minimum Cost to Separate Sentence Into Rows",
        difficulty="Medium", topics=("dp",),
        summary="Break a sentence into rows of at most k characters (words stay whole, single spaces between). A row of length n costs (k − n)²; the last row is free. Return the minimum total.",
        example="\"i love leetcode\", k = 12  →  36",
        criterion="Which approach is O(w · k) for w words?",
        hint="Choose where the current row ends; the rest is the same problem.",
        choices=(
            Choice(
                "DP over the first word of each row", OPTIMAL, time="O(w·k)", space="O(w)", visual="dp-1d",
                detail="dp[i] = 0 if words i.. fit in one row; else min over row ends j of (k − len(i..j))² + dp[j + 1].",
                why="Each row is a contiguous block, and only blocks of at most k characters (so at most k/2 words) are tried.",
            ),
            Choice(
                "Try every set of line breaks", SUBOPTIMAL, time="O(2ʷ)", space="O(w)", visual="backtrack",
                detail="Enumerate break positions.",
                why="Correct, but exponential.",
            ),
            Choice(
                "Greedy: fill each row", INCORRECT, time="O(w)", space="O(1)", visual="greedy",
                detail="Put as many words as fit, then break.",
                why="Squared costs reward balanced rows; a full row can leave a nearly empty one before the last.",
            ),
            Choice(
                "Charge the last row", INCORRECT, time="O(w·k)", space="O(w)", visual="dp-1d",
                detail="Include the final row's cost.",
                why="The last row is free.",
            ),
        ),
    ),
    Question(
        slug="minimum-subarrays-in-a-valid-split", number=2464, title="Minimum Subarrays in a Valid Split",
        difficulty="Medium", topics=("dp",),
        summary="Split nums into subarrays whose first and last elements have gcd > 1. Return the fewest subarrays, or −1.",
        example="[2,6,3,4,3]  →  2",
        criterion="Which approach is O(n² log V)?",
        hint="Decide where the last subarray starts.",
        choices=(
            Choice(
                "dp[i] over the last subarray's start", OPTIMAL, time="O(n² log V)", space="O(n)", visual="dp-1d",
                detail="dp[i] = min over j ≤ i with gcd(nums[j], nums[i]) > 1 of dp[j − 1] + 1.",
                why="Any valid split ends with some valid last piece, and the prefix before it is a smaller subproblem.",
            ),
            Choice(
                "Try every split", SUBOPTIMAL, time="O(2ⁿ)", space="O(n)", visual="backtrack",
                detail="Enumerate cut positions.",
                why="Correct, but exponential.",
            ),
            Choice(
                "Greedy longest first piece", INCORRECT, time="O(n² log V)", space="O(1)", visual="greedy",
                detail="Extend the first piece as far as a valid end exists.",
                why="A long first piece can leave a suffix that can't be split.",
            ),
            Choice(
                "Check adjacent gcds", INCORRECT, time="O(n log V)", space="O(1)", visual="two-pointers",
                detail="Cut wherever neighbours are coprime.",
                why="Only each piece's first and last elements matter.",
            ),
        ),
    ),
    Question(
        slug="split-array-largest-sum", number=410, title="Split Array Largest Sum",
        difficulty="Hard", topics=("dp",),
        summary="Split nums (non-negative) into k non-empty contiguous parts to minimize the largest part's sum.",
        example="[7,2,5,10,8], k = 2  →  18",
        criterion="Which approach is O(n log S)?",
        hint="Given a cap X, how few parts can you make greedily?",
        choices=(
            Choice(
                "Binary search on the answer with a greedy count", OPTIMAL, time="O(n log S)", space="O(1)", visual="binary-search",
                detail="Find the smallest X such that filling parts greedily up to X needs ≤ k parts.",
                why="Feasibility is monotone in X, and the greedy count is exact for a fixed cap.",
            ),
            Choice(
                "Partition DP", SUBOPTIMAL, time="O(k·n²)", space="O(k·n)", visual="dp-2d",
                detail="dp[j][i] = min over the last cut of max(dp[j−1][c], sum(c..i)).",
                why="Correct and the classic DP, but slower.",
            ),
            Choice(
                "Equal-length parts", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="Cut every n/k elements.",
                why="Values differ in size.",
            ),
            Choice(
                "Total / k, rounded up", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="The average part.",
                why="Elements can't be split; [1,10] with k = 2 gives 10, not 6.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §6.1 stock trading
    Question(
        slug="best-time-to-buy-and-sell-stock-ii", number=122, title="Best Time to Buy and Sell Stock II",
        difficulty="Medium", topics=("dp",),
        summary="Buy and sell any number of times, holding at most one share. Return the maximum profit.",
        example="[7,1,5,3,6,4]  →  7",
        criterion="Which approach is linear with O(1) extra space?",
        hint="A long rise is the sum of its daily rises.",
        choices=(
            Choice(
                "Sum of positive daily differences", OPTIMAL, time="O(n)", space="O(1)", visual="greedy",
                detail="Add max(0, p[i] − p[i − 1]).",
                why="Any profitable trade equals the sum of its daily rises, and capturing every rise is allowed.",
            ),
            Choice(
                "DP over every buy-sell pair", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="dp-1d",
                detail="best[i] = max over j < i of best[j] + p[i] − p[j].",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Max minus min", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="One trade at the extremes.",
                why="Several trades can beat one: 4 + 3 = 7 here.",
            ),
            Choice(
                "Sum of all differences", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="Add p[i] − p[i − 1] including drops.",
                why="That's just last − first.",
            ),
        ),
    ),
    Question(
        slug="best-time-to-buy-and-sell-stock-iii", number=123, title="Best Time to Buy and Sell Stock III",
        difficulty="Hard", topics=("dp",),
        summary="At most two transactions (one share at a time). Return the maximum profit.",
        example="[3,3,5,0,0,3,1,4]  →  6",
        criterion="Which approach is linear with O(1) extra space?",
        hint="Track four states: after buy 1, sell 1, buy 2, sell 2.",
        choices=(
            Choice(
                "Four-state machine", OPTIMAL, time="O(n)", space="O(1)", visual="dp-1d",
                detail="b1 = max(b1, −p); s1 = max(s1, b1 + p); b2 = max(b2, s1 − p); s2 = max(s2, b2 + p).",
                why="Each state is the best balance after that many actions, and each day can move one step along the chain.",
            ),
            Choice(
                "Best single trade on each side of a split", SUBOPTIMAL, time="O(n)", space="O(n)", visual="prefix",
                detail="Prefix best and suffix best arrays, combined at each split.",
                why="Correct and linear, but stores two arrays.",
            ),
            Choice(
                "Two largest rises", INCORRECT, time="O(n log n)", space="O(n)", visual="sort",
                detail="Sum the two biggest daily rises.",
                why="A trade can span several days; the rise 0 → 3 → 1 → 4 merges into 4.",
            ),
            Choice(
                "Unlimited trades", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Sum every rise.",
                why="That may use more than two trades.",
            ),
        ),
    ),
    Question(
        slug="best-time-to-buy-and-sell-stock-iv", number=188, title="Best Time to Buy and Sell Stock IV",
        difficulty="Hard", topics=("dp",),
        summary="At most k transactions. Return the maximum profit.",
        example="k = 2, [3,2,6,5,0,3]  →  7",
        criterion="Which approach is O(n·k)?",
        hint="Generalize the four states to 2k states.",
        choices=(
            Choice(
                "2k-state machine", OPTIMAL, time="O(n·k)", space="O(k)", visual="dp-2d",
                detail="buy[j] = max(buy[j], sell[j − 1] − p); sell[j] = max(sell[j], buy[j] + p); if k ≥ n/2, sum all rises.",
                why="Each pair of states is one transaction, and the large-k shortcut avoids useless work.",
            ),
            Choice(
                "DP over the last sell and its buy", SUBOPTIMAL, time="O(k·n²)", space="O(k·n)", visual="dp-2d",
                detail="dp[j][i] = max(dp[j][i − 1], max over m of p[i] − p[m] + dp[j − 1][m]).",
                why="Correct, but the inner max can be carried as a running value.",
            ),
            Choice(
                "Sum of the k largest rises", INCORRECT, time="O(n log n)", space="O(n)", visual="sort",
                detail="Pick the biggest k daily rises.",
                why="Adjacent rises may belong to one transaction.",
            ),
            Choice(
                "k times the best single trade", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="Repeat the best trade.",
                why="Trades can't overlap or reuse days.",
            ),
        ),
    ),
    Question(
        slug="best-time-to-buy-and-sell-stock-with-cooldown", number=309, title="Best Time to Buy and Sell Stock with Cooldown",
        difficulty="Medium", topics=("dp",),
        summary="Unlimited transactions, but after selling you must wait one day before buying again.",
        example="[1,2,3,0,2]  →  3",
        criterion="Which approach is linear with O(1) extra space?",
        hint="Which states do you need: holding, just sold, resting?",
        choices=(
            Choice(
                "Three-state machine", OPTIMAL, time="O(n)", space="O(1)", visual="dp-1d",
                detail="hold = max(hold, rest − p); sold = hold + p; rest = max(rest, previous sold).",
                why="The cooldown is enforced by buying only from 'rest', which can't follow a sale on the same day.",
            ),
            Choice(
                "DP over every buy and sell", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="dp-1d",
                detail="Try every previous buy for each sell.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Sum of rises", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Ignore the cooldown.",
                why="Selling at 3 and buying at 0 the next day isn't allowed.",
            ),
            Choice(
                "Buy from the sold state", INCORRECT, time="O(n)", space="O(1)", visual="dp-1d",
                detail="hold = max(hold, sold − p).",
                why="That buys on the day right after selling.",
            ),
        ),
    ),
    Question(
        slug="best-time-to-buy-and-sell-stock-with-transaction-fee", number=714, title="Best Time to Buy and Sell Stock with Transaction Fee",
        difficulty="Medium", topics=("dp",),
        summary="Unlimited transactions; each sale costs fee. Return the maximum profit.",
        example="[1,3,2,8,4,9], fee = 2  →  8",
        criterion="Which approach is linear with O(1) extra space?",
        hint="Two states: holding or not.",
        choices=(
            Choice(
                "Two-state machine with the fee on sale", OPTIMAL, time="O(n)", space="O(1)", visual="dp-1d",
                detail="cash = max(cash, hold + p − fee); hold = max(hold, cash − p).",
                why="The fee is paid once per transaction, and the states merge small dips into one longer trade when that's cheaper.",
            ),
            Choice(
                "DP over every buy-sell pair", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="dp-1d",
                detail="Try every buy for each sell.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Sum of rises minus fee each", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Trade every rise and pay the fee.",
                why="Small rises lose money after the fee, and merging trades saves fees.",
            ),
            Choice(
                "Ignore the fee", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Sum all rises.",
                why="Each sale costs fee.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §6.2 state machine basics
    Question(
        slug="maximum-energy-boost-from-two-drinks", number=3259, title="Maximum Energy Boost From Two Drinks",
        difficulty="Medium", topics=("dp",),
        summary="Each hour drink A or B for energyA[i] or energyB[i]; switching drinks costs one hour of nothing. Return the most energy over n hours.",
        example="A = [1,3,1], B = [3,1,1]  →  5",
        criterion="Which approach is linear with O(1) extra space?",
        hint="Ending on A at hour i: you were on A at i − 1, or on B at i − 2 (then switched).",
        choices=(
            Choice(
                "Two states, switching from two hours back", OPTIMAL, time="O(n)", space="O(1)", visual="dp-1d",
                detail="fA[i] = max(fA[i − 1], fB[i − 2]) + A[i]; same for B.",
                why="A switch wastes exactly one hour, so the other drink's state from two hours ago is the only other source.",
            ),
            Choice(
                "Try every switching pattern", SUBOPTIMAL, time="O(2ⁿ)", space="O(n)", visual="brute",
                detail="Enumerate choices per hour.",
                why="Correct, but exponential.",
            ),
            Choice(
                "Best drink each hour", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Take max(A[i], B[i]).",
                why="Switching costs an hour.",
            ),
            Choice(
                "Better of all-A and all-B", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="Never switch.",
                why="One switch can pay off when drinks alternate in value over long stretches.",
            ),
        ),
    ),
    Question(
        slug="number-of-ways-to-select-buildings", number=2222, title="Number of Ways to Select Buildings",
        difficulty="Medium", topics=("dp",),
        summary="Choose 3 buildings (in order) from a 0/1 string so no two consecutive chosen ones have the same type. Count the ways.",
        example="\"001101\"  →  6",
        criterion="Which approach is linear?",
        hint="Valid picks are \"010\" or \"101\" subsequences. Fix the middle.",
        choices=(
            Choice(
                "Enumerate the middle with left/right counts", OPTIMAL, time="O(n)", space="O(1)", visual="counting",
                detail="For a middle '1', add (0s on the left)·(0s on the right); symmetric for '0'.",
                why="Once the middle is fixed, the two outer picks are independent choices of the opposite type.",
            ),
            Choice(
                "All triples", SUBOPTIMAL, time="O(n³)", space="O(1)", visual="brute",
                detail="Check every i < j < k.",
                why="Correct, but cubic.",
            ),
            Choice(
                "Contiguous \"010\"/\"101\" only", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Count matching windows of length 3.",
                why="The buildings don't have to be adjacent.",
            ),
            Choice(
                "zeros · ones · (n − 2)", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="A formula ignoring order.",
                why="Positions matter: a 0 must sit on each side of a middle 1.",
            ),
        ),
    ),
    Question(
        slug="maximum-strength-of-a-group", number=2708, title="Maximum Strength of a Group",
        difficulty="Medium", topics=("dp",),
        summary="Return the largest product of a non-empty subset of nums.",
        example="[3,-1,-5,2,5,-9]  →  1350",
        criterion="Which approach is linear?",
        hint="Track both the largest and smallest product of the elements seen so far.",
        choices=(
            Choice(
                "Running max and min products", OPTIMAL, time="O(n)", space="O(1)", visual="dp-1d",
                detail="For x, new max = max(max, x, max·x, min·x); new min likewise.",
                why="A negative turns the smallest product into the largest, so both extremes must be kept, as in maximum product subarray but without contiguity.",
            ),
            Choice(
                "Every subset", SUBOPTIMAL, time="O(2ⁿ·n)", space="O(n)", visual="brute",
                detail="Multiply all subsets.",
                why="Correct for n ≤ 13, but exponential.",
            ),
            Choice(
                "Product of positives", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Skip all negatives.",
                why="−5 and −9 multiply to 45.",
            ),
            Choice(
                "Product of all non-zeros", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="Multiply everything except zeros.",
                why="An odd number of negatives makes it negative; dropping the closest-to-zero one is better.",
            ),
        ),
    ),
    Question(
        slug="wiggle-subsequence", number=376, title="Wiggle Subsequence",
        difficulty="Medium", topics=("dp",),
        summary="Return the length of the longest subsequence whose successive differences strictly alternate in sign.",
        example="[1,17,5,10,13,15,10,5,16,8]  →  7",
        criterion="Which approach is linear with O(1) extra space?",
        hint="Track the best wiggle ending with an up move and with a down move.",
        choices=(
            Choice(
                "Up and down counters", OPTIMAL, time="O(n)", space="O(1)", visual="dp-1d",
                detail="If nums[i] > nums[i − 1], up = down + 1; if smaller, down = up + 1.",
                why="Each new rise can extend the best sequence ending in a fall, and vice versa; plateaus change nothing.",
            ),
            Choice(
                "O(n²) DP", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="dp-1d",
                detail="For each i, check every j < i in both directions.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Count sign changes", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Count where consecutive differences change sign, zeros included.",
                why="A zero difference isn't up or down, and counting it breaks runs.",
            ),
            Choice(
                "Number of local extremes", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Count peaks and valleys only.",
                why="The two endpoints also count.",
            ),
        ),
    ),
    Question(
        slug="maximum-coin-collection", number=3466, title="Maximum Coin Collection",
        difficulty="Medium", topics=("dp",),
        summary="Two lanes have coin values per mile (negative = toll). Mario enters at any mile in lane 1, drives at least one mile, and may switch lanes at most twice (even right after entering). Return the most coins.",
        example="lane1 = [1,-2,-10,3], lane2 = [-5,10,0,1]  →  14",
        criterion="Which approach is linear?",
        hint="States: switches used so far (0, 1, 2), which also tells the current lane.",
        choices=(
            Choice(
                "Kadane over (switches used) states", OPTIMAL, time="O(n)", space="O(1)", visual="dp-1d",
                detail="f0 = max(f0, 0) + lane1[i]; f1 = max(f1, f0_prev, 0) + lane2[i]; f2 = max(f2, f1_prev) + lane1[i]; track the best.",
                why="Entering anywhere is the 'restart at 0' of Kadane, and each switch moves to the next state.",
            ),
            Choice(
                "Try all entry, exit and switch points", SUBOPTIMAL, time="O(n⁴)", space="O(1)", visual="brute",
                detail="Enumerate segments.",
                why="Correct, but polynomially huge.",
            ),
            Choice(
                "Must start at mile 0", INCORRECT, time="O(n)", space="O(1)", visual="dp-1d",
                detail="No fresh starts.",
                why="Example 3 enters at mile 1.",
            ),
            Choice(
                "Unlimited switches", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Take the better lane every mile.",
                why="At most two switches are allowed.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §6.3 state machine, further practice
    Question(
        slug="knight-dialer", number=935, title="Knight Dialer",
        difficulty="Medium", topics=("dp",),
        summary="A knight hops between digits on a phone pad. Count the distinct numbers of length n it can dial, mod 10⁹ + 7.",
        example="2  →  20",
        criterion="Which approach is O(n)?",
        hint="The count ending on a digit depends only on the counts of the digits that jump to it.",
        choices=(
            Choice(
                "DP over the 10 digits", OPTIMAL, time="O(10·n)", space="O(10)", visual="dp-1d",
                detail="new[d] = Σ old[s] for each digit s that a knight move takes to d.",
                why="Ten states per length and fixed transitions make each step constant time.",
            ),
            Choice(
                "DFS over all numbers", SUBOPTIMAL, time="O(3ⁿ)", space="O(n)", visual="recursion",
                detail="Enumerate every dialed sequence.",
                why="Correct, but exponential.",
            ),
            Choice(
                "10 · 2ⁿ⁻¹", INCORRECT, time="O(1)", space="O(1)", visual="math",
                detail="Assume every digit has two moves.",
                why="4 and 6 have three moves; 5 has none.",
            ),
            Choice(
                "Exclude 5 only", INCORRECT, time="O(1)", space="O(1)", visual="math",
                detail="9 · 2ⁿ⁻¹.",
                why="5 is still a valid one-digit number, and move counts differ.",
            ),
        ),
    ),
    Question(
        slug="lcp-19-autumn-leaves", number=None, title="Autumn Leaves",
        difficulty="Medium", topics=("dp",),
        ref="LCP 19", url="https://leetcode.cn/problems/UlBDOe/",
        summary="A string of 'r' and 'y' leaves must become red, yellow, red sections, each non-empty. One operation swaps one leaf's color. Return the fewest operations.",
        example="\"rrryyyrryyyrr\"  →  2",
        criterion="Which approach is linear?",
        hint="Each leaf is in section 1, 2 or 3, and sections only move forward.",
        choices=(
            Choice(
                "Three-state DP", OPTIMAL, time="O(n)", space="O(1)", visual="dp-1d",
                detail="f0 from f0; f1 from f0 or f1; f2 from f1 or f2; add 1 when the leaf's color doesn't fit its section; start each section only after the previous one is non-empty.",
                why="The cost only depends on which section the current leaf is in, so three running minima cover all splits.",
            ),
            Choice(
                "Try every pair of cut points", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="prefix",
                detail="Prefix counts for each (i, j).",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Allow empty sections", INCORRECT, time="O(n)", space="O(1)", visual="dp-1d",
                detail="Skip the non-empty rule.",
                why="\"rr\" would cost 0, but it needs a yellow middle.",
            ),
            Choice(
                "Recolor the middle third", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="Fix sections of equal size.",
                why="Sections can be any size.",
            ),
        ),
    ),
    Question(
        slug="paint-fence", number=276, title="Paint Fence",
        difficulty="Medium", topics=("dp",),
        summary="Paint n posts with k colors so no three consecutive posts share a color. Count the ways.",
        example="n = 3, k = 2  →  6",
        criterion="Which approach is linear with O(1) extra space?",
        hint="Split by whether the last two posts match.",
        choices=(
            Choice(
                "same/diff states", OPTIMAL, time="O(n)", space="O(1)", visual="dp-1d",
                detail="same_i = diff_{i−1}; diff_i = (same_{i−1} + diff_{i−1})·(k − 1).",
                why="A post can match the previous one only if those two didn't already match.",
            ),
            Choice(
                "Recursion over colors", SUBOPTIMAL, time="O(kⁿ)", space="O(n)", visual="recursion",
                detail="Try each color for each post.",
                why="Correct, but exponential.",
            ),
            Choice(
                "k · (k − 1)ⁿ⁻¹", INCORRECT, time="O(1)", space="O(1)", visual="math",
                detail="Forbid any two equal neighbours.",
                why="Two equal neighbours are allowed; only three are not.",
            ),
            Choice(
                "kⁿ", INCORRECT, time="O(1)", space="O(1)", visual="math",
                detail="No restriction.",
                why="Three equal posts in a row are forbidden.",
            ),
        ),
    ),
    Question(
        slug="maximum-subarray-sum-after-one-operation", number=1746, title="Maximum Subarray Sum After One Operation",
        difficulty="Medium", topics=("dp",),
        summary="You must square exactly one element. Return the largest non-empty subarray sum afterwards.",
        example="[2,-1,-4,-3]  →  17",
        criterion="Which approach is linear with O(1) extra space?",
        hint="Kadane with one extra state: whether the square has been used.",
        choices=(
            Choice(
                "Kadane with used/unused states", OPTIMAL, time="O(n)", space="O(1)", visual="dp-1d",
                detail="g = max(f + x², g + x, x²); f = max(f + x, x); track the best g.",
                why="The square is applied at most once inside the subarray, so two running states cover every placement.",
            ),
            Choice(
                "Try squaring each element with Kadane", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="Run Kadane n times.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Square the largest |x|", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Square the biggest magnitude, then Kadane.",
                why="It may lie outside the best subarray.",
            ),
            Choice(
                "Kadane, then square the max element", INCORRECT, time="O(n)", space="O(1)", visual="dp-1d",
                detail="Find the best subarray first.",
                why="Squaring can create a better subarray elsewhere, as with −4 above.",
            ),
        ),
    ),
    Question(
        slug="maximum-alternating-subarray-sum", number=2036, title="Maximum Alternating Subarray Sum",
        difficulty="Medium", topics=("dp",),
        summary="A subarray's alternating sum is nums[i] − nums[i + 1] + nums[i + 2] − …. Return the maximum over all subarrays.",
        example="[3,-1,1,2]  →  5",
        criterion="Which approach is linear with O(1) extra space?",
        hint="Track the best sum ending at i where nums[i] is added, and where it's subtracted.",
        choices=(
            Choice(
                "Two-state Kadane", OPTIMAL, time="O(n)", space="O(1)", visual="dp-1d",
                detail="plus = max(minus + x, x); minus = plus_prev − x; track max(plus, minus).",
                why="Signs alternate along the subarray, so an added element follows a subtracted one, and a subarray may start at any added element.",
            ),
            Choice(
                "Every subarray", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="Compute from each start.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Fixed signs by index", INCORRECT, time="O(n)", space="O(1)", visual="dp-1d",
                detail="Multiply nums[i] by (−1)ⁱ and run Kadane.",
                why="A subarray starting at an odd index must start with +.",
            ),
            Choice(
                "Kadane on raw values", INCORRECT, time="O(n)", space="O(1)", visual="dp-1d",
                detail="Ignore the alternation.",
                why="Signs alternate within the subarray.",
            ),
        ),
    ),
    Question(
        slug="minimum-costs-using-the-train-line", number=2361, title="Minimum Costs Using the Train Line",
        difficulty="Hard", topics=("dp",),
        summary="Stops 0..n lie on a regular and an express route; moving i − 1 → i costs regular[i] or express[i]; switching to express costs expressCost (switching back is free). Return the cheapest cost to reach each stop.",
        example="regular = [1,6,9,5], express = [5,2,3,10], expressCost = 8  →  [1,7,14,19]",
        criterion="Which approach is linear?",
        hint="At each stop you're either on the regular or the express route.",
        choices=(
            Choice(
                "Two-state DP", OPTIMAL, time="O(n)", space="O(1)", visual="dp-1d",
                detail="reg = min(reg, exp) + regular[i]; exp = min(exp, reg_prev + expressCost) + express[i]; answer min(reg, exp).",
                why="Only the current route matters for the future, so two running costs capture every switching pattern.",
            ),
            Choice(
                "Dijkstra on a two-layer graph", SUBOPTIMAL, time="O(n log n)", space="O(n)", visual="dijkstra",
                detail="Nodes are (stop, route).",
                why="Correct, but edges only go forward, so DP order suffices.",
            ),
            Choice(
                "Cheaper segment each step", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Pick min(regular, express) per segment.",
                why="Switching to express costs expressCost each time.",
            ),
            Choice(
                "Free switching both ways", INCORRECT, time="O(n)", space="O(1)", visual="dp-1d",
                detail="Ignore expressCost.",
                why="Getting onto the express line isn't free.",
            ),
        ),
    ),
    Question(
        slug="constructing-two-increasing-arrays", number=3269, title="Constructing Two Increasing Arrays",
        difficulty="Hard", topics=("dp",),
        summary="Replace each 0 with an even and each 1 with an odd positive integer so both arrays are strictly increasing and no integer is used twice. Return the smallest possible largest number.",
        example="nums1 = [], nums2 = [1,0,1,1]  →  5",
        criterion="Which approach is O(m·n)?",
        hint="Numbers are handed out in increasing order across both arrays. What's the state after using i of nums1 and j of nums2?",
        choices=(
            Choice(
                "dp[i][j] = smallest largest number used so far", OPTIMAL, time="O(m·n)", space="O(n)", visual="dp-2d",
                detail="Extend with nums1[i] or nums2[j], taking the next number above dp of the right parity.",
                why="Assigning values in increasing order keeps both arrays increasing and distinct, so only the current maximum matters.",
            ),
            Choice(
                "Backtrack over the merge order", SUBOPTIMAL, time="O(C(m + n, m))", space="O(m + n)", visual="backtrack",
                detail="Try every interleaving of the two arrays and assign numbers greedily.",
                why="Correct, but the same (i, j) prefixes are reached by many interleavings.",
            ),
            Choice(
                "Fill each array separately", INCORRECT, time="O(m + n)", space="O(1)", visual="greedy",
                detail="Use the smallest valid numbers for each array on its own.",
                why="Both arrays would reuse the same integers.",
            ),
            Choice(
                "Interleave by index", INCORRECT, time="O(m + n)", space="O(1)", visual="two-pointers",
                detail="Alternate nums1[i], nums2[i], nums1[i + 1], ….",
                why="The best order depends on the parities needed.",
            ),
        ),
    ),
]
