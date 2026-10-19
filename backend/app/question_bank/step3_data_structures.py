"""Core route step 3: common data structures (数据结构 §0 enumeration, §1 prefix sums, §3 stack, §4 queue, §5 heap)."""

from .question_schema import INCORRECT, OPTIMAL, SUBOPTIMAL, Choice, Question

QUESTIONS = [
    # ---------------------------------------------------------------- §0.1 enumerate the right, maintain the left
    Question(
        slug="two-sum", number=1, title="Two Sum",
        difficulty="Easy", topics=("data-structures",),
        summary="Return the indices of the two numbers that add up to target. Exactly one answer exists; an element can't be used twice.",
        example="[2,7,11,15], 9  →  [0, 1]",
        criterion="Which approach is linear?",
        hint="Standing at index j, what value would you need to have seen already?",
        choices=(
            Choice(
                "One pass with a value → index map", OPTIMAL, time="O(n)", space="O(n)", visual="hashmap",
                detail="For each j, look up target − nums[j] in the map, then store nums[j] → j.",
                why="Enumerate the right element and remember everything to its left. Looking up before storing keeps an element from pairing with itself.",
            ),
            Choice(
                "Sort with indices, two pointers", SUBOPTIMAL, time="O(n log n)", space="O(n)", visual="two-pointers",
                detail="Sort (value, index) pairs and move pointers inward.",
                why="Correct, but sorting costs more than one hashed pass.",
            ),
            Choice(
                "Two pointers on the unsorted array", INCORRECT, time="O(n)", space="O(1)", visual="two-pointers",
                detail="Move the left pointer up if the sum is small, the right down if large.",
                why="That logic needs sorted order. Does moving left up make the sum bigger here?",
            ),
            Choice(
                "Store before looking up", INCORRECT, time="O(n)", space="O(n)", visual="hashmap",
                detail="Put nums[j] in the map first, then look for target − nums[j].",
                why="For [3,2,4] and target 6, the 3 finds itself. Is [0, 0] allowed?",
            ),
        ),
    ),
    Question(
        slug="number-of-good-pairs", number=1512, title="Number of Good Pairs",
        difficulty="Easy", topics=("data-structures",),
        summary="Count pairs i < j with nums[i] == nums[j].",
        example="[1,2,3,1,1,3]  →  4",
        criterion="Which approach is linear?",
        hint="When you reach a value, how many good pairs does it close?",
        choices=(
            Choice(
                "Add the count seen so far", OPTIMAL, time="O(n)", space="O(n)", visual="hashmap",
                detail="For each x, add count[x], then increment count[x].",
                why="Each earlier copy of x forms one pair with the current one, so the running count is exactly the new pairs.",
            ),
            Choice(
                "Check every pair", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="Compare all i < j.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Count repeated values", INCORRECT, time="O(n)", space="O(n)", visual="counting",
                detail="Count values that appear at least twice.",
                why="Three 1s make 3 pairs, not 1.",
            ),
            Choice(
                "Sum of counts", INCORRECT, time="O(n)", space="O(n)", visual="counting",
                detail="Add up how often each value appears.",
                why="That's just n. Should a value seen once contribute?",
            ),
        ),
    ),
    Question(
        slug="largest-positive-integer-that-exists-with-its-negative", number=2441, title="Largest Positive Integer That Exists With Its Negative",
        difficulty="Easy", topics=("data-structures",),
        summary="Return the largest positive k such that −k is also in nums, or −1.",
        example="[-1,10,6,7,-7,1]  →  7",
        criterion="Which approach is linear?",
        hint="As you scan, what do you need to know about values seen before?",
        choices=(
            Choice(
                "Hash set, check the opposite", OPTIMAL, time="O(n)", space="O(n)", visual="set",
                detail="For each x, if −x is in the set, update the answer with |x|; add x.",
                why="Whichever of k and −k comes second finds the other in O(1).",
            ),
            Choice(
                "Sort, two pointers", SUBOPTIMAL, time="O(n log n)", space="O(1)", visual="two-pointers",
                detail="Move inward from the most negative and most positive values.",
                why="Correct, but sorting is unnecessary.",
            ),
            Choice(
                "Check only the maximum", INCORRECT, time="O(n)", space="O(n)", visual="set",
                detail="Return max if −max is present, else −1.",
                why="10 has no −10, but 7 works. Should you give up?",
            ),
            Choice(
                "Largest |x| that appears", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="Return the largest absolute value.",
                why="That's 10, which has no partner.",
            ),
        ),
    ),
    Question(
        slug="best-time-to-buy-and-sell-stock", number=121, title="Best Time to Buy and Sell Stock",
        difficulty="Easy", topics=("data-structures",),
        summary="Buy on one day and sell on a later day. Return the maximum profit, or 0.",
        example="[7,1,5,3,6,4]  →  5",
        criterion="Which approach is linear with O(1) extra space?",
        hint="If you sell today, which buying day is best?",
        choices=(
            Choice(
                "Track the minimum so far", OPTIMAL, time="O(n)", space="O(1)", visual="greedy",
                detail="For each day, profit = price − lowest earlier price; keep the best; update the minimum.",
                why="Selling on day j, the best buy is the cheapest day before it. One running minimum covers every j.",
            ),
            Choice(
                "Try every pair of days", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="Check all buy < sell.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Global max minus global min", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="Subtract the lowest price from the highest.",
                why="In [7,1,5,3,6,4] that works, but in [7,6,1] the max comes before the min. Can you sell before buying?",
            ),
            Choice(
                "Sum of all rises", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Add every day-to-day increase.",
                why="That allows many trades. How many are allowed here?",
            ),
        ),
    ),
    Question(
        slug="maximum-difference-between-increasing-elements", number=2016, title="Maximum Difference Between Increasing Elements",
        difficulty="Easy", topics=("data-structures",),
        summary="Return the largest nums[j] − nums[i] with i < j and nums[i] < nums[j], or −1.",
        example="[7,1,5,4]  →  4",
        criterion="Which approach is linear with O(1) extra space?",
        hint="This is the stock problem with a twist. What's the twist?",
        choices=(
            Choice(
                "Running minimum, strict comparison", OPTIMAL, time="O(n)", space="O(1)", visual="greedy",
                detail="Answer −1; for each j, if nums[j] > min so far, update with the difference; update the min.",
                why="The best partner for j is the smallest earlier value. Requiring > keeps equal values from counting.",
            ),
            Choice(
                "Every pair", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="Check all i < j.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Allow equal values", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Start the answer at 0 and use ≥.",
                why="For [9,4,3,2], what should be returned when nothing increases?",
            ),
            Choice(
                "Max minus min", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="Return the overall spread if positive.",
                why="The max must come after the min.",
            ),
        ),
    ),
    Question(
        slug="maximum-distance-in-arrays", number=624, title="Maximum Distance in Arrays",
        difficulty="Medium", topics=("data-structures",),
        summary="Given m sorted arrays, pick two numbers from two different arrays. Return the largest |a − b|.",
        example="[[1,2,3],[4,5],[1,2,3]]  →  4",
        criterion="Which approach is O(m)?",
        hint="Each array only matters through its first and last elements. What do you need from earlier arrays?",
        choices=(
            Choice(
                "Running min and max of earlier arrays", OPTIMAL, time="O(m)", space="O(1)", visual="greedy",
                detail="For each array, compare its last with the earlier min and its first with the earlier max; then update both.",
                why="Comparing only with earlier arrays guarantees the two numbers come from different arrays.",
            ),
            Choice(
                "Every pair of arrays", SUBOPTIMAL, time="O(m²)", space="O(1)", visual="brute",
                detail="Compare ends of every two arrays.",
                why="Correct, but quadratic in m.",
            ),
            Choice(
                "Global max minus global min", INCORRECT, time="O(m)", space="O(1)", visual="math",
                detail="Take the largest last and the smallest first.",
                why="For [[1,100],[50,60]], both come from the first array. Is that allowed?",
            ),
            Choice(
                "Adjacent arrays only", INCORRECT, time="O(m)", space="O(1)", visual="two-pointers",
                detail="Compare each array with the next one.",
                why="The best pair can be far apart in the list.",
            ),
        ),
    ),
    Question(
        slug="minimum-absolute-difference-between-two-values", number=3880, title="Minimum Absolute Difference Between Two Values",
        difficulty="Easy", topics=("data-structures",),
        summary="nums holds 0, 1 and 2. Return the smallest |i − j| with nums[i] = 1 and nums[j] = 2, or −1.",
        example="[1,0,0,2,0,1]  →  2",
        criterion="Which approach is linear?",
        hint="At a 2, which 1 is the closest one on its left?",
        choices=(
            Choice(
                "Track the last 1 and the last 2", OPTIMAL, time="O(n)", space="O(1)", visual="two-pointers",
                detail="At a 1, compare with the last 2; at a 2, compare with the last 1.",
                why="The nearest partner on the left is the most recent one, and checking at both kinds of cells covers both directions.",
            ),
            Choice(
                "Every pair", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="Compare all (1, 2) index pairs.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Only 2s after 1s", INCORRECT, time="O(n)", space="O(1)", visual="two-pointers",
                detail="At a 2, compare with the last 1; ignore 1s after 2s.",
                why="The example's best pair is the 2 at 3 with the 1 at 5.",
            ),
            Choice(
                "First 1 and first 2", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Return |first 1 − first 2|.",
                why="That's 3 here. Is there a closer pair?",
            ),
        ),
    ),
    Question(
        slug="max-sum-of-a-pair-with-equal-sum-of-digits", number=2342, title="Max Sum of a Pair With Equal Sum of Digits",
        difficulty="Medium", topics=("data-structures",),
        summary="Return the largest nums[i] + nums[j] (i ≠ j) whose digit sums are equal, or −1.",
        example="[18,43,36,13,7]  →  54",
        criterion="Which approach is linear (times the digit count)?",
        hint="For each digit sum, which earlier number is worth remembering?",
        choices=(
            Choice(
                "Map digit sum → largest seen", OPTIMAL, time="O(n·d)", space="O(n)", visual="hashmap",
                detail="For each x, if its digit sum has a best y, try x + y; then keep the larger of x and y.",
                why="The best partner for x is the largest earlier number with the same digit sum, and one value per key keeps that.",
            ),
            Choice(
                "Group, sort each group", SUBOPTIMAL, time="O(n log n)", space="O(n)", visual="sort",
                detail="Bucket by digit sum and add the top two of each bucket.",
                why="Correct, but only the top two of each group matter.",
            ),
            Choice(
                "Two largest numbers", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Add the two biggest values.",
                why="43 and 36 have digit sums 7 and 9. Are they a pair?",
            ),
            Choice(
                "Equal last digits", INCORRECT, time="O(n)", space="O(1)", visual="hashmap",
                detail="Group by last digit instead.",
                why="18 and 36 both have digit sum 9 but different last digits.",
            ),
        ),
    ),
    Question(
        slug="maximum-valid-pair-sum", number=3979, title="Maximum Valid Pair Sum",
        difficulty="Medium", topics=("data-structures",),
        summary="Return the largest nums[i] + nums[j] over pairs with j − i ≥ k.",
        example="[1,3,5,2,8], k = 2  →  13",
        criterion="Which approach is linear with O(1) extra space?",
        hint="For index j, which earlier indices are allowed, and which of them is best?",
        choices=(
            Choice(
                "Prefix max lagging by k", OPTIMAL, time="O(n)", space="O(1)", visual="greedy",
                detail="For j from k, update best = max(best, nums[j − k]) and try best + nums[j].",
                why="Allowed partners for j are exactly indices ≤ j − k, and the best is their maximum, which grows by one element per step.",
            ),
            Choice(
                "Every valid pair", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="Check all i, j with j − i ≥ k.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Two largest values", INCORRECT, time="O(n)", space="O(1)", visual="sort",
                detail="Add the two biggest numbers.",
                why="For [9,8,1] with k = 2, 9 and 8 are adjacent. What's the real answer?",
            ),
            Choice(
                "Pairs exactly k apart", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Only compare nums[j − k] with nums[j].",
                why="Farther pairs are allowed too. For k = 1 in [5,1,9], is 5 + 9 considered?",
            ),
        ),
    ),
    Question(
        slug="number-of-equivalent-domino-pairs", number=1128, title="Number of Equivalent Domino Pairs",
        difficulty="Easy", topics=("data-structures",),
        summary="Dominoes [a, b] and [c, d] are equivalent if one can be rotated to equal the other. Count equivalent pairs.",
        example="[[1,2],[2,1],[3,4],[5,6]]  →  1",
        criterion="Which approach is linear?",
        hint="What canonical form makes [1,2] and [2,1] the same key?",
        choices=(
            Choice(
                "Count by (min, max) key", OPTIMAL, time="O(n)", space="O(1)", visual="counting",
                detail="Normalize each domino to (min, max); add the count seen so far.",
                why="Rotation only swaps the two halves, so sorting them gives one key per class. With values 1–9, there are 45 keys.",
            ),
            Choice(
                "Compare every pair", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="Check each pair both ways.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Count by (a, b) as given", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Use the domino exactly as written as the key.",
                why="Would [1,2] and [2,1] share a key?",
            ),
            Choice(
                "Count by a + b", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Group dominoes by the sum of their halves.",
                why="[1,4] and [2,3] both sum to 5. Are they equivalent?",
            ),
        ),
    ),
    Question(
        slug="max-number-of-k-sum-pairs", number=1679, title="Max Number of K-Sum Pairs",
        difficulty="Medium", topics=("data-structures",),
        summary="Repeatedly remove two numbers summing to k. Return the most removals possible.",
        example="[1,2,3,4], k = 5  →  2",
        criterion="Which approach is linear?",
        hint="When x arrives, is there an unmatched k − x waiting?",
        choices=(
            Choice(
                "Match against unpaired counts", OPTIMAL, time="O(n)", space="O(n)", visual="hashmap",
                detail="If count[k − x] > 0, pair and decrement it; else increment count[x].",
                why="Any unmatched partner works equally well, so matching greedily on arrival never loses a pair.",
            ),
            Choice(
                "Sort, two pointers", SUBOPTIMAL, time="O(n log n)", space="O(1)", visual="two-pointers",
                detail="Pair the ends when they sum to k, else move one pointer.",
                why="Correct, but sorting costs more than a hashed pass.",
            ),
            Choice(
                "Count pairs without removing", INCORRECT, time="O(n)", space="O(n)", visual="hashmap",
                detail="Add count[k − x] for each x.",
                why="For [3,3,3] and k = 6, that counts 3 pairs. How many removals can happen?",
            ),
            Choice(
                "Count distinct pair values", INCORRECT, time="O(n)", space="O(n)", visual="set",
                detail="Count values x ≤ k − x that both appear.",
                why="[1,4,1,4] has two removals of the same pair kind.",
            ),
        ),
    ),
    Question(
        slug="pairs-with-sum-lcci", number=None, title="Pairs With Sum",
        difficulty="Medium", topics=("data-structures",),
        ref="面试题 16.24", url="https://leetcode.cn/problems/pairs-with-sum-lcci/",
        summary="Return all pairs of elements summing to target, each element used in at most one pair.",
        example="[5,6,5,6], 11  →  [[5,6], [5,6]]",
        criterion="Which approach is linear?",
        hint="This is K-Sum Pairs, but you report the pairs.",
        choices=(
            Choice(
                "Match against unpaired counts", OPTIMAL, time="O(n)", space="O(n)", visual="hashmap",
                detail="If an unpaired target − x exists, emit the pair and decrement; else count x.",
                why="Each element is matched at most once, and any waiting partner is as good as another.",
            ),
            Choice(
                "Sort, two pointers", SUBOPTIMAL, time="O(n log n)", space="O(1)", visual="two-pointers",
                detail="Emit and move both pointers when the ends sum to target.",
                why="Correct, but sorts first.",
            ),
            Choice(
                "Hash set of values", INCORRECT, time="O(n)", space="O(n)", visual="set",
                detail="Emit (x, target − x) whenever the partner is in a set.",
                why="A set forgets how many 5s there are, and can reuse one 5 twice.",
            ),
            Choice(
                "Count pairs, don't consume", INCORRECT, time="O(n)", space="O(n)", visual="hashmap",
                detail="Emit one pair for every earlier partner.",
                why="With [5,6,5,6], how many pairs would that emit, and are elements reused?",
            ),
        ),
    ),
    Question(
        slug="contains-duplicate-ii", number=219, title="Contains Duplicate II",
        difficulty="Easy", topics=("data-structures",),
        summary="Return whether two equal values sit at most k indices apart.",
        example="[1,2,3,1], k = 3  →  true",
        criterion="Which approach is linear with O(min(n, k)) extra space?",
        hint="Only the last k values can pair with the current one.",
        choices=(
            Choice(
                "Set of the last k values", OPTIMAL, time="O(n)", space="O(min(n, k))", visual="sliding-window",
                detail="Check nums[i] in the set, add it, and remove nums[i − k] once the window is full.",
                why="The set holds exactly the allowed partners, so a hit means a close duplicate, and it never grows past k.",
            ),
            Choice(
                "Map value → last index", SUBOPTIMAL, time="O(n)", space="O(n)", visual="hashmap",
                detail="Check i − last[x] ≤ k, then update last[x].",
                why="Correct and linear, but it remembers every distinct value ever seen.",
            ),
            Choice(
                "Adjacent duplicates only", INCORRECT, time="O(n)", space="O(1)", visual="two-pointers",
                detail="Check nums[i] == nums[i − 1].",
                why="The example's 1s are 3 apart.",
            ),
            Choice(
                "Any duplicate at all", INCORRECT, time="O(n)", space="O(n)", visual="set",
                detail="Return true if any value repeats.",
                why="For [1,2,3,1] with k = 2, the 1s are too far apart.",
            ),
        ),
    ),
    Question(
        slug="minimum-consecutive-cards-to-pick-up", number=2260, title="Minimum Consecutive Cards to Pick Up",
        difficulty="Medium", topics=("data-structures",),
        summary="Return the fewest consecutive cards to pick up so that two of them match, or −1.",
        example="[3,4,2,3,4,7]  →  4",
        criterion="Which approach is linear?",
        hint="For each card, which earlier copy gives the shortest span?",
        choices=(
            Choice(
                "Map value → last index", OPTIMAL, time="O(n)", space="O(n)", visual="hashmap",
                detail="At index i, try i − last[x] + 1, then set last[x] = i.",
                why="The nearest earlier copy always gives the shortest span ending at i.",
            ),
            Choice(
                "Every pair", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="Check all equal pairs.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "First duplicate found", INCORRECT, time="O(n)", space="O(n)", visual="set",
                detail="Return the span of the first repeat you reach.",
                why="A later pair can be closer. Is the first repeat the shortest?",
            ),
            Choice(
                "Distinct values plus one", INCORRECT, time="O(n)", space="O(n)", visual="counting",
                detail="By pigeonhole, pick distinct + 1 cards.",
                why="That bounds the answer but ignores where the copies are.",
            ),
        ),
    ),
    Question(
        slug="number-of-pairs-of-interchangeable-rectangles", number=2001, title="Number of Pairs of Interchangeable Rectangles",
        difficulty="Medium", topics=("data-structures",),
        summary="Rectangles are interchangeable if their width/height ratios are equal. Count interchangeable pairs.",
        example="[[4,8],[3,6],[10,20],[15,30]]  →  6",
        criterion="Which approach is linear (times a gcd)?",
        hint="Which exact key represents a ratio?",
        choices=(
            Choice(
                "Count by reduced (w, h)", OPTIMAL, time="O(n log V)", space="O(n)", visual="hashmap",
                detail="Divide w and h by their gcd; add the count seen so far for that key.",
                why="Equal ratios reduce to the same pair, an exact key with no floating-point concerns.",
            ),
            Choice(
                "Every pair by cross-multiplying", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="Check w₁·h₂ == w₂·h₁ for all pairs.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Count by area", INCORRECT, time="O(n)", space="O(n)", visual="hashmap",
                detail="Group rectangles by w·h.",
                why="[4,8] and [3,6] have different areas but the same ratio.",
            ),
            Choice(
                "Count by w − h", INCORRECT, time="O(n)", space="O(n)", visual="hashmap",
                detail="Group by the difference of sides.",
                why="[4,8] differs by 4 and [10,20] by 10. Same ratio?",
            ),
        ),
    ),
    Question(
        slug="max-pair-sum-in-an-array", number=2815, title="Max Pair Sum in an Array",
        difficulty="Easy", topics=("data-structures",),
        summary="Return the largest sum of two numbers whose largest digits are equal, or −1.",
        example="[51,71,17,24,42]  →  88",
        criterion="Which approach is linear (times the digit count)?",
        hint="Only 10 possible largest digits. What's worth remembering for each?",
        choices=(
            Choice(
                "Best value per largest digit", OPTIMAL, time="O(n·d)", space="O(1)", visual="hashmap",
                detail="For x with largest digit m, try x + best[m]; then best[m] = max(best[m], x).",
                why="The best partner for x is the largest earlier number with the same max digit. Ten slots hold all of them.",
            ),
            Choice(
                "Every pair", SUBOPTIMAL, time="O(n²·d)", space="O(1)", visual="brute",
                detail="Compare max digits for all pairs.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Two largest numbers", INCORRECT, time="O(n)", space="O(1)", visual="sort",
                detail="Add the two biggest values.",
                why="71 and 51 have max digits 7 and 5.",
            ),
            Choice(
                "Equal first digits", INCORRECT, time="O(n)", space="O(1)", visual="hashmap",
                detail="Group by leading digit instead.",
                why="17's largest digit is 7, not 1.",
            ),
        ),
    ),
    Question(
        slug="count-number-of-trapezoids-i", number=3623, title="Count Number of Trapezoids I",
        difficulty="Medium", topics=("data-structures",),
        summary="Given distinct points, count horizontal trapezoids: four points forming two horizontal sides on different y values. Return the count mod 10⁹ + 7.",
        example="[[1,0],[2,0],[3,0],[2,2],[3,2]]  →  3",
        criterion="Which approach is linear?",
        hint="A trapezoid picks a pair of points on one horizontal line and a pair on another.",
        choices=(
            Choice(
                "Pairs per line, combined with a running sum", OPTIMAL, time="O(n)", space="O(n)", visual="prefix",
                detail="For each y, p = C(count, 2); add p × (sum of p over earlier lines); then add p to the sum.",
                why="Each trapezoid is one pair from line a and one from line b ≠ a. The running sum counts all earlier lines at once.",
            ),
            Choice(
                "Every pair of lines", SUBOPTIMAL, time="O(Y²)", space="O(Y)", visual="brute",
                detail="Multiply the pair counts for every two y values.",
                why="Correct, but with many lines that's quadratic.",
            ),
            Choice(
                "Square of the total pairs", INCORRECT, time="O(n)", space="O(n)", visual="math",
                detail="(Σ p)².",
                why="That includes both pairs on the same line, and counts each trapezoid twice.",
            ),
            Choice(
                "Choose 4 points", INCORRECT, time="O(1)", space="O(1)", visual="math",
                detail="C(n, 4).",
                why="Four random points rarely form two horizontal sides.",
            ),
        ),
    ),
    Question(
        slug="count-number-of-bad-pairs", number=2364, title="Count Number of Bad Pairs",
        difficulty="Medium", topics=("data-structures",),
        summary="A pair i < j is bad if j − i ≠ nums[j] − nums[i]. Count bad pairs.",
        example="[4,1,3,3]  →  5",
        criterion="Which approach is linear?",
        hint="Rearrange j − i = nums[j] − nums[i]. What's equal on both sides?",
        choices=(
            Choice(
                "All pairs minus pairs with equal nums[i] − i", OPTIMAL, time="O(n)", space="O(n)", visual="hashmap",
                detail="Count good pairs by key nums[i] − i; return n(n − 1)/2 − good.",
                why="A pair is good exactly when nums[i] − i = nums[j] − j, so good pairs are equal keys, counted in one pass.",
            ),
            Choice(
                "Check every pair", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="Test the condition for all i < j.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Count good pairs", INCORRECT, time="O(n)", space="O(n)", visual="hashmap",
                detail="Return the number of pairs with equal nums[i] − i.",
                why="That's the complement. The task asks for bad pairs.",
            ),
            Choice(
                "Key nums[i] + i", INCORRECT, time="O(n)", space="O(n)", visual="hashmap",
                detail="Group by nums[i] + i.",
                why="Check the algebra: does j − i = nums[j] − nums[i] give equal sums?",
            ),
        ),
    ),
    Question(
        slug="count-caesar-cipher-pairs", number=3805, title="Count Caesar Cipher Pairs",
        difficulty="Medium", topics=("data-structures",),
        summary="Two equal-length words are similar if shifting every letter of one forward by the same amount (wrapping z → a) gives the other. Count similar pairs i < j.",
        example="[\"ab\",\"aa\",\"za\",\"aa\"]  →  2",
        criterion="Which approach is linear in the total length?",
        hint="Shift every word so it starts with 'a'. What do similar words become?",
        choices=(
            Choice(
                "Normalize to start with 'a', count keys", OPTIMAL, time="O(n·m)", space="O(n·m)", visual="hashmap",
                detail="Shift each word back by its first letter (mod 26); add the count seen so far for that key.",
                why="Shifting preserves the gaps between letters, so similar words share one normal form.",
            ),
            Choice(
                "Compare every pair", SUBOPTIMAL, time="O(n²·m)", space="O(1)", visual="brute",
                detail="For each pair, check that all letter gaps match mod 26.",
                why="Correct, but quadratic in the number of words.",
            ),
            Choice(
                "Normalize without wrapping", INCORRECT, time="O(n·m)", space="O(n·m)", visual="hashmap",
                detail="Use the raw differences from the first letter.",
                why="\"ab\" gives +1 but \"za\" gives −25. Aren't they similar?",
            ),
            Choice(
                "Sorted letters as key", INCORRECT, time="O(n·m log m)", space="O(n·m)", visual="sort",
                detail="Group anagrams together.",
                why="\"ab\" and \"ba\" are anagrams. Is one a shift of the other?",
            ),
        ),
    ),
    Question(
        slug="identify-the-largest-outlier-in-an-array", number=3371, title="Identify the Largest Outlier in an Array",
        difficulty="Medium", topics=("data-structures",),
        summary="Of n numbers, n − 2 are special, one equals the sum of the special numbers, and one is an outlier. Return the largest possible outlier.",
        example="[2,3,5,10]  →  10",
        criterion="Which approach is linear?",
        hint="If x is the outlier and y the sum element, what's the total of the array?",
        choices=(
            Choice(
                "Try each outlier, look up the sum element", OPTIMAL, time="O(n)", space="O(n)", visual="hashmap",
                detail="With total S, for x: if S − x is even and y = (S − x)/2 occurs at another index, x is valid.",
                why="S = 2y + x, so each candidate x determines y. A count map checks y's presence, including when y = x needs two copies.",
            ),
            Choice(
                "Try each (outlier, sum) pair", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="For every i ≠ j, check S − x − y = y.",
                why="Correct, but y is already forced by x.",
            ),
            Choice(
                "The maximum element", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Return max(nums).",
                why="In [1,2,3,6,4], 6 is the sum of 1, 2 and 3, so the outlier is 4.",
            ),
            Choice(
                "Ignore the index check", INCORRECT, time="O(n)", space="O(n)", visual="set",
                detail="Accept y if the value appears at all.",
                why="If y equals x, both roles need two different elements.",
            ),
        ),
    ),
    Question(
        slug="minimum-absolute-distance-between-mirror-pairs", number=3761, title="Minimum Absolute Distance Between Mirror Pairs",
        difficulty="Medium", topics=("data-structures",),
        summary="A mirror pair is i < j with reverse(nums[i]) = nums[j] (leading zeros dropped). Return the smallest j − i, or −1.",
        example="[12,21,45,33,54]  →  1",
        criterion="Which approach is linear (times the digit count)?",
        hint="At j, which earlier value would you need, and which earlier index is closest?",
        choices=(
            Choice(
                "Map reverse(nums[i]) → latest i", OPTIMAL, time="O(n·d)", space="O(n)", visual="hashmap",
                detail="At j, if nums[j] is a key, try j − index; then store reverse(nums[j]) → j.",
                why="The closest valid i for j is the latest one whose reverse equals nums[j]. Storing the reverse keeps the direction right.",
            ),
            Choice(
                "Every pair", SUBOPTIMAL, time="O(n²·d)", space="O(1)", visual="brute",
                detail="Check reverse(nums[i]) == nums[j] for all i < j.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Check both directions", INCORRECT, time="O(n·d)", space="O(n)", visual="hashmap",
                detail="Accept reverse(nums[i]) = nums[j] or reverse(nums[j]) = nums[i].",
                why="For [21,120], reverse(120) = 21 but reverse(21) = 12. Is that a mirror pair?",
            ),
            Choice(
                "Keep the first index", INCORRECT, time="O(n·d)", space="O(n)", visual="hashmap",
                detail="Store each reversed value only the first time it appears.",
                why="A later copy of nums[i] would be closer to j.",
            ),
        ),
    ),
    Question(
        slug="delayed-count-of-equal-elements", number=3837, title="Delayed Count of Equal Elements",
        difficulty="Medium", topics=("data-structures",),
        summary="For each index i, count indices j > i + k with nums[j] = nums[i].",
        example="[1,2,1,1], k = 1  →  [2,0,0,0]",
        criterion="Which approach is linear?",
        hint="Walk i from the right. Which element becomes eligible when i moves left by one?",
        choices=(
            Choice(
                "Right-to-left with a lagging count map", OPTIMAL, time="O(n)", space="O(n)", visual="hashmap",
                detail="Before answering i, add nums[i + k + 1] (if it exists) to the counts; answer count[nums[i]].",
                why="The eligible set for i is everything from i + k + 1 onward, and it grows by exactly one element per step.",
            ),
            Choice(
                "Scan right of i + k for each i", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="Count matches from i + k + 1 to the end.",
                why="Correct, but rescans the same suffix.",
            ),
            Choice(
                "Ignore the delay", INCORRECT, time="O(n)", space="O(n)", visual="hashmap",
                detail="Count equal values anywhere after i.",
                why="For i = 2, the 1 at index 3 is only one step away. With k = 1, does it count?",
            ),
            Choice(
                "Count from the left", INCORRECT, time="O(n)", space="O(n)", visual="hashmap",
                detail="Count equal values before i − k.",
                why="The task looks forward, not back.",
            ),
        ),
    ),
    Question(
        slug="count-smaller-elements-with-opposite-parity", number=3907, title="Count Smaller Elements With Opposite Parity",
        difficulty="Medium", topics=("data-structures",),
        summary="For each index i, count later indices j with nums[j] < nums[i] and opposite parity.",
        example="[5,2,4,1,3]  →  [2,1,2,0,0]",
        criterion="Which approach is O(n log V)?",
        hint="Walking right to left, you need 'how many smaller values of the other parity have I seen'.",
        choices=(
            Choice(
                "Right-to-left with one Fenwick tree per parity", OPTIMAL, time="O(n log V)", space="O(V)", visual="prefix",
                detail="Answer i by a prefix query on the tree of the opposite parity, then insert nums[i] into its own tree.",
                why="Each tree counts later values of one parity, and a prefix sum below nums[i] gives the smaller ones in O(log V).",
            ),
            Choice(
                "Scan the suffix for each i", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="Check every later element.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Ignore the value condition", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Count later elements of opposite parity.",
                why="For 2 at index 1, is the 3 later on smaller?",
            ),
            Choice(
                "One tree for both parities", INCORRECT, time="O(n log V)", space="O(V)", visual="prefix",
                detail="Count all later smaller values.",
                why="For 5 at index 0, the 1 and 3 are smaller but odd. Should they count?",
            ),
        ),
    ),
    Question(
        slug="pairs-of-songs-with-total-durations-divisible-by-60", number=1010, title="Pairs of Songs With Total Durations Divisible by 60",
        difficulty="Medium", topics=("data-structures",),
        summary="Count pairs i < j with (time[i] + time[j]) % 60 == 0.",
        example="[30,20,150,100,40]  →  3",
        criterion="Which approach is linear?",
        hint="Only remainders mod 60 matter. Which remainder completes r?",
        choices=(
            Choice(
                "Count remainders, add the complement's count", OPTIMAL, time="O(n)", space="O(1)", visual="counting",
                detail="For each t, add cnt[(60 − t % 60) % 60], then increment cnt[t % 60].",
                why="Pairs are fixed by remainders. The outer % 60 sends remainder 0 to partner 0 instead of 60.",
            ),
            Choice(
                "Every pair", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="Test all pairs.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Partner 60 − r without the final mod", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Look up cnt[60 − t % 60].",
                why="For t = 60, that reads cnt[60]. Where are songs with remainder 0 counted?",
            ),
            Choice(
                "Count songs divisible by 60", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Count t with t % 60 == 0 and choose pairs among them.",
                why="30 and 150 aren't divisible by 60, but their sum is.",
            ),
        ),
    ),
    Question(
        slug="count-pairs-that-form-a-complete-day-ii", number=3185, title="Count Pairs That Form a Complete Day II",
        difficulty="Medium", topics=("data-structures",),
        summary="Count pairs i < j whose hours add up to a multiple of 24.",
        example="[12,12,30,24,24]  →  2",
        criterion="Which approach is linear?",
        hint="Same idea as songs divisible by 60.",
        choices=(
            Choice(
                "Remainder counts", OPTIMAL, time="O(n)", space="O(1)", visual="counting",
                detail="Add cnt[(24 − h % 24) % 24], then increment cnt[h % 24].",
                why="Only remainders mod 24 matter, so 24 counters and one pass suffice.",
            ),
            Choice(
                "Sort by remainder, two pointers", SUBOPTIMAL, time="O(n log n)", space="O(n)", visual="two-pointers",
                detail="Sort remainders and pair from both ends, handling 0 and 12 specially.",
                why="Correct with care, but sorting is unnecessary for 24 buckets.",
            ),
            Choice(
                "Every pair of exact multiples", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Count pairs among hours divisible by 24.",
                why="12 + 12 = 24. Are those counted?",
            ),
            Choice(
                "Partner 24 − r without the final mod", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Look up cnt[24 − h % 24].",
                why="Hours 24 and 24 have remainder 0. Which bucket would they look in?",
            ),
        ),
    ),
    Question(
        slug="number-of-beautiful-pairs", number=2748, title="Number of Beautiful Pairs",
        difficulty="Easy", topics=("data-structures",),
        summary="A pair i < j is beautiful if the first digit of nums[i] and the last digit of nums[j] are coprime. Count beautiful pairs.",
        example="[2,5,1,4]  →  5",
        criterion="Which approach is O(9·n)?",
        hint="For j, only the first digits of earlier numbers matter. How many kinds are there?",
        choices=(
            Choice(
                "Count earlier first digits", OPTIMAL, time="O(9·n)", space="O(1)", visual="counting",
                detail="For j, add cnt[d] for each digit d coprime with nums[j] % 10; then count nums[j]'s first digit.",
                why="Nine counters summarize every earlier number, so each j costs at most 9 checks.",
            ),
            Choice(
                "Every pair", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="Check gcd for all i < j.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Ignore order", INCORRECT, time="O(9·n)", space="O(1)", visual="counting",
                detail="Count pairs in both directions.",
                why="(i, j) uses i's first digit and j's last digit. Is (j, i) the same test?",
            ),
            Choice(
                "Compare last digits", INCORRECT, time="O(9·n)", space="O(1)", visual="counting",
                detail="Use the last digit of both numbers.",
                why="The rule uses nums[i]'s first digit.",
            ),
        ),
    ),
    Question(
        slug="count-pairs-of-similar-strings", number=2506, title="Count Pairs Of Similar Strings",
        difficulty="Easy", topics=("data-structures",),
        summary="Two strings are similar if they use the same set of letters. Count similar pairs.",
        example="[\"aba\",\"aabb\",\"abcd\",\"bac\",\"aabc\"]  →  2",
        criterion="Which approach is linear in the total length?",
        hint="What compact key captures a set of letters?",
        choices=(
            Choice(
                "26-bit mask key", OPTIMAL, time="O(total length)", space="O(n)", visual="bits",
                detail="OR in each letter's bit; add the count seen so far for that mask.",
                why="A bitmask is exactly the set of letters, built in one pass per word.",
            ),
            Choice(
                "Sorted unique letters as key", SUBOPTIMAL, time="O(total length · log)", space="O(total length)", visual="sort",
                detail="Key by the sorted set of characters.",
                why="Correct, but builds and sorts strings where an int would do.",
            ),
            Choice(
                "Sorted word as key", INCORRECT, time="O(total length · log)", space="O(total length)", visual="sort",
                detail="Group anagrams.",
                why="\"aba\" and \"aabb\" use the same letters with different counts. Are they similar?",
            ),
            Choice(
                "Equal lengths", INCORRECT, time="O(n)", space="O(n)", visual="counting",
                detail="Group words by length.",
                why="\"aba\" and \"bac\" are both length 3.",
            ),
        ),
    ),
    Question(
        slug="maximum-value-of-an-ordered-triplet-ii", number=2874, title="Maximum Value of an Ordered Triplet II",
        difficulty="Medium", topics=("data-structures",),
        summary="Return the largest (nums[i] − nums[j]) · nums[k] with i < j < k, or 0 if all are negative.",
        example="[12,6,1,2,7]  →  77",
        criterion="Which approach is linear with O(1) extra space?",
        hint="Enumerate k. What's the best (nums[i] − nums[j]) to its left, and how do you maintain it?",
        choices=(
            Choice(
                "Running max and max difference", OPTIMAL, time="O(n)", space="O(1)", visual="greedy",
                detail="For each x: answer = max(answer, maxDiff · x); maxDiff = max(maxDiff, maxPre − x); maxPre = max(maxPre, x).",
                why="Values are positive, so the best k wants the largest earlier difference, which in turn wants the largest earlier i. Two running maxima carry both.",
            ),
            Choice(
                "Prefix and suffix maximum arrays", SUBOPTIMAL, time="O(n)", space="O(n)", visual="prefix",
                detail="For each j, (prefixMax[j − 1] − nums[j]) · suffixMax[j + 1].",
                why="Correct and linear, but stores two arrays.",
            ),
            Choice(
                "(max − min) · max", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="Use the global extremes.",
                why="The indices must be in order i < j < k.",
            ),
            Choice(
                "Consecutive triples only", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Check (a − b) · c for adjacent a, b, c.",
                why="In the example, i = 0, j = 2, k = 4 isn't contiguous.",
            ),
        ),
    ),
    Question(
        slug="maximum-sum-of-two-non-overlapping-subarrays", number=1031, title="Maximum Sum of Two Non-Overlapping Subarrays",
        difficulty="Medium", topics=("data-structures",),
        summary="Return the largest total of two non-overlapping subarrays of lengths firstLen and secondLen (either order).",
        example="[0,6,5,2,2,5,1,9,4], firstLen = 1, secondLen = 2  →  20",
        criterion="Which approach is linear?",
        hint="Enumerate where the right subarray ends. What's the best left subarray before it?",
        choices=(
            Choice(
                "Prefix sums with a running best left block", OPTIMAL, time="O(n)", space="O(n)", visual="prefix",
                detail="For each end, add the right block's sum to the best block of the other length ending before it; do both orders.",
                why="Enumerating the right block and remembering the best left block is 'enumerate right, maintain left' with prefix sums for O(1) block sums.",
            ),
            Choice(
                "Every pair of positions", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="brute",
                detail="Try all non-overlapping placements.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Best first block, then best second", INCORRECT, time="O(n)", space="O(n)", visual="greedy",
                detail="Pick the best firstLen block, then the best secondLen block outside it.",
                why="The single best block can sit where it blocks a better combination.",
            ),
            Choice(
                "One order only", INCORRECT, time="O(n)", space="O(n)", visual="prefix",
                detail="Assume the firstLen block is on the left.",
                why="The answer may put the secondLen block first.",
            ),
        ),
    ),
    Question(
        slug="count-special-quadruplets", number=1995, title="Count Special Quadruplets",
        difficulty="Easy", topics=("data-structures",),
        summary="Count index quadruplets a < b < c < d with nums[a] + nums[b] + nums[c] = nums[d]. n ≤ 50.",
        example="[1,1,1,3,5]  →  4",
        criterion="Which approach is O(n²)?",
        hint="Rewrite as nums[a] + nums[b] = nums[d] − nums[c]. Which index splits the two sides?",
        choices=(
            Choice(
                "Enumerate b, count right-side differences", OPTIMAL, time="O(n²)", space="O(V)", visual="hashmap",
                detail="Walk b from right to left; add pairs (c = b + 1, d > c) to a count of nums[d] − nums[c]; then for each a < b add count[nums[a] + nums[b]].",
                why="Splitting at b turns four nested loops into two pair loops that meet in a hash map.",
            ),
            Choice(
                "Three loops plus a count of d", SUBOPTIMAL, time="O(n³)", space="O(V)", visual="brute",
                detail="Enumerate a, b, c and look up how many d > c have the sum.",
                why="Correct, but one loop more than needed.",
            ),
            Choice(
                "Ignore index order", INCORRECT, time="O(n²)", space="O(V)", visual="hashmap",
                detail="Count value combinations without requiring a < b < c < d.",
                why="In [3,1,1,1], 1 + 1 + 1 = 3, but the 3 comes first. Should it count?",
            ),
            Choice(
                "Distinct values only", INCORRECT, time="O(n²)", space="O(V)", visual="set",
                detail="Work on the set of values.",
                why="The three 1s give several quadruplets.",
            ),
        ),
    ),
    Question(
        slug="two-sum-bsts", number=1214, title="Two Sum BSTs",
        difficulty="Medium", topics=("data-structures",),
        summary="Return whether some node in the first BST and some node in the second sum to target.",
        example="root1 = [2,1,4], root2 = [1,0,3], target = 5  →  true",
        criterion="Which approach is O(m + n)?",
        hint="In-order traversal gives sorted values. What can you do with two sorted lists?",
        choices=(
            Choice(
                "In-order lists, two pointers", OPTIMAL, time="O(m + n)", space="O(m + n)", visual="two-pointers",
                detail="Walk the first list up and the second down, moving whichever side the sum calls for.",
                why="Sorted lists let one pointer sweep each, so every candidate pair is ruled in or out in linear time.",
            ),
            Choice(
                "Search tree 2 for each node of tree 1", SUBOPTIMAL, time="O(m·h)", space="O(h)", visual="tree-dfs",
                detail="For each x in tree 1, BST-search tree 2 for target − x.",
                why="Correct, but a skewed tree 2 makes each search O(n).",
            ),
            Choice(
                "Compare the roots", INCORRECT, time="O(1)", space="O(1)", visual="brute",
                detail="Return root1 + root2 == target.",
                why="4 + 1 = 5 uses non-root nodes.",
            ),
            Choice(
                "Two Sum inside one tree", INCORRECT, time="O(m)", space="O(m)", visual="hashmap",
                detail="Look for two nodes of tree 1 that sum to target.",
                why="One node must come from each tree.",
            ),
        ),
    ),
    Question(
        slug="number-of-divisible-triplet-sums", number=2964, title="Number of Divisible Triplet Sums",
        difficulty="Medium", topics=("data-structures",),
        summary="Count triplets i < j < k with (nums[i] + nums[j] + nums[k]) divisible by d.",
        example="[3,3,4,7,8], d = 5  →  3",
        criterion="Which approach is O(n²)?",
        hint="Fix j and k. Which remainder must nums[i] have, and where do you keep that count?",
        choices=(
            Choice(
                "Enumerate (j, k), count i's remainder", OPTIMAL, time="O(n²)", space="O(n)", visual="hashmap",
                detail="For each j, loop k > j and add cnt[(−nums[j] − nums[k]) mod d]; then add nums[j] % d to cnt.",
                why="cnt holds remainders of indices before j, so every i < j < k is counted once.",
            ),
            Choice(
                "All triples", SUBOPTIMAL, time="O(n³)", space="O(1)", visual="brute",
                detail="Test every i < j < k.",
                why="Correct, but cubic.",
            ),
            Choice(
                "Count remainder triples without order", INCORRECT, time="O(n + d²)", space="O(d)", visual="counting",
                detail="Multiply remainder counts for every remainder triple summing to 0 mod d.",
                why="Without care, equal remainders and orderings are counted several times.",
            ),
            Choice(
                "Two-element version", INCORRECT, time="O(n)", space="O(d)", visual="counting",
                detail="Count pairs whose sum is divisible by d.",
                why="The task needs three elements.",
            ),
        ),
    ),
    Question(
        slug="count-indices-with-opposite-parity", number=3917, title="Count Indices With Opposite Parity",
        difficulty="Easy", topics=("data-structures",),
        summary="For each index i, count later indices j whose value has the opposite parity.",
        example="[1,2,3,4]  →  [2,1,1,0]",
        criterion="Which approach is linear?",
        hint="Walking from the right, what two numbers summarize everything after i?",
        choices=(
            Choice(
                "Right-to-left odd and even counts", OPTIMAL, time="O(n)", space="O(1)", visual="counting",
                detail="Answer i with the count of the other parity, then add nums[i] to its own count.",
                why="Two counters fully describe the suffix for this question.",
            ),
            Choice(
                "Scan the suffix for each i", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="Count opposite-parity elements after i.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Count all opposite-parity elements", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Use totals over the whole array.",
                why="Only later indices count. Should index 3 see the 1 at index 0?",
            ),
            Choice(
                "Count same parity", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Use the count of the same parity.",
                why="The rule asks for different parity.",
            ),
        ),
    ),
    Question(
        slug="two-furthest-houses-with-different-colors", number=2078, title="Two Furthest Houses With Different Colors",
        difficulty="Easy", topics=("data-structures",),
        summary="Return the largest |i − j| between two houses of different colors.",
        example="[1,1,1,6,1,1,1]  →  3",
        criterion="Which approach is linear with O(1) extra space?",
        hint="Must one of the two houses be at an end of the street?",
        choices=(
            Choice(
                "Pair with the first or the last house", OPTIMAL, time="O(n)", space="O(1)", visual="two-pointers",
                detail="Take the farthest house differing from house 0, and the farthest differing from house n − 1; return the larger distance.",
                why="If neither end were used, one end differs from one of the chosen houses and gives a longer pair. So an end is always involved.",
            ),
            Choice(
                "Every pair", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="Check all pairs.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "n − 1 if the ends differ, else 0", INCORRECT, time="O(1)", space="O(1)", visual="math",
                detail="Only compare the two ends.",
                why="In the example the ends match, yet the answer is 3.",
            ),
            Choice(
                "Distance between the first two colors", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Find the first change of color.",
                why="That's the closest change, not the farthest.",
            ),
        ),
    ),
    Question(
        slug="4sum-ii", number=454, title="4Sum II",
        difficulty="Medium", topics=("data-structures",),
        summary="Given four arrays of length n, count tuples (i, j, k, l) with A[i] + B[j] + C[k] + D[l] = 0.",
        example="A = [1,2], B = [-2,-1], C = [-1,2], D = [0,2]  →  2",
        criterion="Which approach is O(n²)?",
        hint="Split the four arrays into two halves.",
        choices=(
            Choice(
                "Count A + B sums, look up −(C + D)", OPTIMAL, time="O(n²)", space="O(n²)", visual="hashmap",
                detail="Map every A[i] + B[j] to its count; for every C[k] + D[l], add count[−(C[k] + D[l])].",
                why="Meeting in the middle turns n⁴ tuples into two n² loops joined by a hash map.",
            ),
            Choice(
                "Three loops plus a count of D", SUBOPTIMAL, time="O(n³)", space="O(n)", visual="brute",
                detail="Enumerate A, B, C and look up the needed D.",
                why="Correct, but one loop more than needed.",
            ),
            Choice(
                "Sort all four, move pointers", INCORRECT, time="O(n log n)", space="O(1)", visual="two-pointers",
                detail="Treat it like a four-pointer sweep.",
                why="Two pointers count one pair per step. How would they count many tuples with equal sums?",
            ),
            Choice(
                "Distinct value tuples", INCORRECT, time="O(n²)", space="O(n²)", visual="set",
                detail="Count distinct (a, b, c, d) values instead of index tuples.",
                why="Equal values at different indices are different tuples.",
            ),
        ),
    ),
    Question(
        slug="contains-duplicate-iii", number=220, title="Contains Duplicate III",
        difficulty="Hard", topics=("data-structures",),
        summary="Return whether there are i ≠ j with |i − j| ≤ indexDiff and |nums[i] − nums[j]| ≤ valueDiff.",
        example="[1,2,3,1], indexDiff = 3, valueDiff = 0  →  true",
        criterion="Which approach is linear?",
        hint="Put values into buckets of width valueDiff + 1. What can you say about two values in one bucket?",
        choices=(
            Choice(
                "Buckets over a sliding window", OPTIMAL, time="O(n)", space="O(min(n, k))", visual="hashmap",
                detail="Bucket = value // (valueDiff + 1); check the same and adjacent buckets; evict the element leaving the window.",
                why="Two values in one bucket are close enough, so each bucket holds at most one value. Only neighbours need a real comparison.",
            ),
            Choice(
                "Sorted set over the window", SUBOPTIMAL, time="O(n log k)", space="O(k)", visual="sort",
                detail="Find the smallest value ≥ x − valueDiff in the window.",
                why="Correct, but each lookup costs log k.",
            ),
            Choice(
                "Adjacent elements only", INCORRECT, time="O(n)", space="O(1)", visual="two-pointers",
                detail="Compare nums[i] with nums[i + 1].",
                why="The example's 1s are three apart.",
            ),
            Choice(
                "Hash set of exact values", INCORRECT, time="O(n)", space="O(k)", visual="set",
                detail="Look for an equal value in the window.",
                why="With valueDiff = 2, 1 and 3 are close. Would exact lookup find them?",
            ),
        ),
    ),
    Question(
        slug="longest-balanced-substring-i", number=3713, title="Longest Balanced Substring I",
        difficulty="Medium", topics=("data-structures",),
        summary="A substring is balanced if all its distinct letters appear equally often. Return the longest balanced substring's length. n ≤ 1000.",
        example="\"abbac\"  →  4",
        criterion="Which approach is O(n²)?",
        hint="While extending from a start, which two numbers decide balance in O(1)?",
        choices=(
            Choice(
                "Extend each start, track distinct and max count", OPTIMAL, time="O(n²)", space="O(26)", visual="counting",
                detail="Balanced exactly when maxCount × distinct == length.",
                why="If every letter has the same count, that count is the max and length = max × distinct. Both update in O(1) per extension.",
            ),
            Choice(
                "Extend each start, compare all 26 counts", SUBOPTIMAL, time="O(26·n²)", space="O(26)", visual="brute",
                detail="Check every nonzero count after each extension.",
                why="Correct, but scans the alphabet every step.",
            ),
            Choice(
                "Two most common letters", INCORRECT, time="O(n)", space="O(26)", visual="counting",
                detail="Look only at the top two letters.",
                why="\"zabc\" is balanced with four letters.",
            ),
            Choice(
                "Distinct-letter windows", INCORRECT, time="O(n)", space="O(26)", visual="sliding-window",
                detail="Longest substring without repeats.",
                why="\"abba\" repeats letters and is still balanced.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §0.2 enumerate the middle
    Question(
        slug="count-special-triplets", number=3583, title="Count Special Triplets",
        difficulty="Medium", topics=("data-structures",),
        summary="Count i < j < k with nums[i] = nums[k] = 2·nums[j], mod 10⁹ + 7.",
        example="[6,3,6]  →  1",
        criterion="Which approach is linear?",
        hint="Fix the middle. What do you need from each side?",
        choices=(
            Choice(
                "Enumerate j with left and right counts", OPTIMAL, time="O(n)", space="O(n)", visual="hashmap",
                detail="Keep counts of values left and right of j; add left[2x] · right[2x].",
                why="Once j is fixed, i and k are independent choices on each side, so their counts multiply.",
            ),
            Choice(
                "Enumerate j, scan both sides", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="Count matches left and right of each j directly.",
                why="Correct, but rescans the array per j.",
            ),
            Choice(
                "Count of 2x squared", INCORRECT, time="O(n)", space="O(n)", visual="counting",
                detail="For each x, add total[2x]².",
                why="That ignores which side each 2x is on, and counts i = k.",
            ),
            Choice(
                "Enumerate i and k only", INCORRECT, time="O(n²)", space="O(1)", visual="brute",
                detail="For equal pairs i < k, add 1 if nums[i]/2 appears anywhere.",
                why="j must lie strictly between i and k, and several j can work.",
            ),
        ),
    ),
    Question(
        slug="unique-length-3-palindromic-subsequences", number=1930, title="Unique Length-3 Palindromic Subsequences",
        difficulty="Medium", topics=("data-structures",),
        summary="Count the distinct palindromes of length 3 that appear as subsequences of s.",
        example="\"aabca\"  →  3",
        criterion="Which approach is O(26·n)?",
        hint="A length-3 palindrome is x?x. For a fixed x, which occurrences give the most choices for '?'",
        choices=(
            Choice(
                "First and last occurrence of each letter", OPTIMAL, time="O(26·n)", space="O(26)", visual="two-pointers",
                detail="For each letter x, count distinct letters strictly between its first and last occurrence.",
                why="The outermost pair of x's contains every possible middle letter, and each distinct middle gives one palindrome.",
            ),
            Choice(
                "Every triple into a set", SUBOPTIMAL, time="O(n³)", space="O(26²)", visual="brute",
                detail="Enumerate all i < j < k with s[i] = s[k].",
                why="Correct, but cubic.",
            ),
            Choice(
                "Count occurrences, not distinct", INCORRECT, time="O(n²)", space="O(1)", visual="counting",
                detail="Count all subsequence occurrences of x?x.",
                why="\"aaaa\" contains \"aaa\" several ways. How many distinct palindromes?",
            ),
            Choice(
                "Adjacent triples only", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Check s[i] == s[i + 2].",
                why="\"aabca\" has a?a with the a's four apart.",
            ),
        ),
    ),
    Question(
        slug="right-triangles", number=3128, title="Right Triangles",
        difficulty="Medium", topics=("data-structures",),
        summary="In a 0/1 grid, count triples of 1s where one cell shares a row with a second and a column with the third.",
        example="[[0,1,0],[0,1,1],[0,1,0]]  →  2",
        criterion="Which approach is O(m·n)?",
        hint="Fix the right-angle cell. How many choices are there for the other two?",
        choices=(
            Choice(
                "Row and column counts per corner", OPTIMAL, time="O(m·n)", space="O(m + n)", visual="matrix",
                detail="Count 1s per row and column; for each 1, add (row − 1) · (col − 1).",
                why="The corner's row partner and column partner are chosen independently from the other 1s in its row and column.",
            ),
            Choice(
                "For each corner, scan its row and column", SUBOPTIMAL, time="O(m·n·(m + n))", space="O(1)", visual="brute",
                detail="Count partners by walking the row and column.",
                why="Correct, but rescans lines that never change.",
            ),
            Choice(
                "row · col per corner", INCORRECT, time="O(m·n)", space="O(m + n)", visual="matrix",
                detail="Multiply the full counts.",
                why="Those counts include the corner itself.",
            ),
            Choice(
                "Choose three 1s", INCORRECT, time="O(m·n)", space="O(1)", visual="math",
                detail="C(ones, 3).",
                why="Most triples don't form a right angle.",
            ),
        ),
    ),
    Question(
        slug="minimum-sum-of-mountain-triplets-ii", number=2909, title="Minimum Sum of Mountain Triplets II",
        difficulty="Medium", topics=("data-structures",),
        summary="A mountain is i < j < k with nums[i] < nums[j] > nums[k]. Return the smallest nums[i] + nums[j] + nums[k], or −1.",
        example="[8,6,1,5,3]  →  9",
        criterion="Which approach is linear?",
        hint="Fix the peak j. What's the best choice on each side?",
        choices=(
            Choice(
                "Prefix and suffix minima", OPTIMAL, time="O(n)", space="O(n)", visual="prefix",
                detail="For each j, if pre[j] < nums[j] > suf[j], try pre[j] + nums[j] + suf[j].",
                why="With j fixed, the smallest side values minimize the sum and are also the easiest to stay below nums[j].",
            ),
            Choice(
                "Scan both sides per peak", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="Find the smallest smaller element on each side of every j.",
                why="Correct, but rescans per j.",
            ),
            Choice(
                "Global minimum on each side", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Use the overall min of the array for both sides.",
                why="The two sides must be on opposite sides of j.",
            ),
            Choice(
                "Smallest three values", INCORRECT, time="O(n)", space="O(1)", visual="sort",
                detail="Add the three smallest numbers.",
                why="They must form a peak in index order.",
            ),
        ),
    ),
    Question(
        slug="132-pattern", number=456, title="132 Pattern",
        difficulty="Medium", topics=("data-structures",),
        summary="Return whether there are i < j < k with nums[i] < nums[k] < nums[j].",
        example="[3,1,4,2]  →  true",
        criterion="Which approach is linear?",
        hint="Scan from the right. Keep candidates for the '3', and remember the best '2' they've produced.",
        choices=(
            Choice(
                "Right-to-left monotonic stack", OPTIMAL, time="O(n)", space="O(n)", visual="monotonic-stack",
                detail="Pop smaller values into k (the '2') while the current value beats them; if any value is below k, the pattern exists.",
                why="Each pop records the largest '2' under some '3' to its left. Any later smaller value completes the pattern. Every element is pushed and popped once.",
            ),
            Choice(
                "Prefix min, then scan right of each j", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="prefix",
                detail="For each j, look for k > j with prefMin[j] < nums[k] < nums[j].",
                why="Correct, but scans the suffix per j.",
            ),
            Choice(
                "Consecutive triples", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Check adjacent a < c < b.",
                why="The indices don't have to be adjacent.",
            ),
            Choice(
                "Any rise then fall", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="True if the array goes up and later down.",
                why="[1,3,0] rises then falls, but 0 isn't above 1.",
            ),
        ),
    ),
    Question(
        slug="count-good-triplets", number=1534, title="Count Good Triplets",
        difficulty="Easy", topics=("data-structures",),
        summary="Count i < j < k with |arr[i] − arr[j]| ≤ a, |arr[j] − arr[k]| ≤ b and |arr[i] − arr[k]| ≤ c. n ≤ 100, values ≤ 1000.",
        example="[3,0,1,1,9,7], a = 7, b = 2, c = 3  →  4",
        criterion="Which approach is O(n² + n·V)?",
        hint="Fix j and k. The valid arr[i] values form one range. How do you count values in a range quickly?",
        choices=(
            Choice(
                "Enumerate (j, k), prefix counts of earlier values", OPTIMAL, time="O(n² + n·V)", space="O(V)", visual="prefix",
                detail="For each pair with |arr[j] − arr[k]| ≤ b, count i < j with value in the intersection of both ranges using prefix counts.",
                why="The two constraints on arr[i] are intervals, and their intersection is one interval. Prefix counts over values answer it in O(1).",
            ),
            Choice(
                "Three nested loops", SUBOPTIMAL, time="O(n³)", space="O(1)", visual="brute",
                detail="Check every triple.",
                why="Correct and fine for n = 100, but cubic.",
            ),
            Choice(
                "Check only adjacent triples", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Test arr[i], arr[i + 1], arr[i + 2].",
                why="The indices needn't be adjacent.",
            ),
            Choice(
                "Ignore index order", INCORRECT, time="O(n³)", space="O(1)", visual="brute",
                detail="Count every triple of values meeting the bounds in any order.",
                why="Swapping i and j changes which bound applies to which pair.",
            ),
        ),
    ),
    Question(
        slug="maximum-increasing-triplet-value", number=3073, title="Maximum Increasing Triplet Value",
        difficulty="Medium", topics=("data-structures",),
        summary="Return the largest nums[i] − nums[j] + nums[k] over i < j < k with nums[i] < nums[j] < nums[k].",
        example="[5,6,9]  →  8",
        criterion="Which approach is O(n log n)?",
        hint="Fix j. You want the largest value below nums[j] on the left and the largest value on the right.",
        choices=(
            Choice(
                "Sorted set on the left, suffix max on the right", OPTIMAL, time="O(n log n)", space="O(n)", visual="sort",
                detail="For each j, find the largest left value < nums[j]; if the suffix max after j exceeds nums[j], try the triplet.",
                why="With j fixed, the best i is the largest smaller value before it and the best k is the largest value after it. A sorted set gives the first, a suffix array the second.",
            ),
            Choice(
                "Scan the left side per j", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="brute",
                detail="Search all i < j for the largest smaller value.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Prefix maximum on the left", INCORRECT, time="O(n)", space="O(n)", visual="prefix",
                detail="Use the largest earlier value for i.",
                why="The largest earlier value may be ≥ nums[j]. Is it still increasing?",
            ),
            Choice(
                "Adjacent triples", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Only consider i, i + 1, i + 2.",
                why="The indices can be far apart.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §0.3 walking diagonals
    Question(
        slug="sort-matrix-by-diagonals", number=3446, title="Sort Matrix by Diagonals",
        difficulty="Medium", topics=("data-structures",),
        summary="In an n×n matrix, sort the diagonals in the bottom-left triangle (main diagonal included) in non-increasing order and those in the top-right triangle in non-decreasing order.",
        example="[[1,7,3],[9,8,2],[4,5,6]]  →  [[8,2,3],[9,6,7],[4,5,1]]",
        criterion="Which approach is O(n² log n)?",
        hint="Every cell on one diagonal has the same i − j.",
        choices=(
            Choice(
                "Collect, sort and write back each diagonal", OPTIMAL, time="O(n² log n)", space="O(n)", visual="matrix",
                detail="For each value of i − j, gather the diagonal, sort it in the required direction and put it back.",
                why="Diagonals are independent, so each sort only touches its own cells, and i − j picks the direction.",
            ),
            Choice(
                "Bubble sort along each diagonal", SUBOPTIMAL, time="O(n³)", space="O(1)", visual="brute",
                detail="Swap neighbours along a diagonal until sorted.",
                why="Correct, but quadratic per diagonal.",
            ),
            Choice(
                "Same direction everywhere", INCORRECT, time="O(n² log n)", space="O(n)", visual="sort",
                detail="Sort every diagonal ascending.",
                why="The two triangles are sorted in opposite directions.",
            ),
            Choice(
                "Sort rows instead", INCORRECT, time="O(n² log n)", space="O(1)", visual="sort",
                detail="Sort each row.",
                why="Values must stay on their own diagonal.",
            ),
        ),
    ),
    Question(
        slug="difference-of-number-of-distinct-values-on-diagonals", number=2711, title="Difference of Number of Distinct Values on Diagonals",
        difficulty="Medium", topics=("data-structures",),
        summary="For each cell, return |distinct values strictly above-left on its diagonal − distinct values strictly below-right|.",
        example="[[1,2,3],[3,1,5],[3,2,1]]  →  [[1,1,0],[1,0,1],[0,1,1]]",
        criterion="Which approach is O(m·n)?",
        hint="Walk each diagonal once forward and once backward.",
        choices=(
            Choice(
                "Two sweeps per diagonal with a set", OPTIMAL, time="O(m·n)", space="O(min(m, n))", visual="set",
                detail="Forward: record the set size before adding each cell. Backward: same for the other side. Combine.",
                why="Each cell is visited twice per diagonal, and a growing set gives 'distinct so far' in O(1).",
            ),
            Choice(
                "Walk both directions from each cell", SUBOPTIMAL, time="O(m·n·min(m, n))", space="O(min(m, n))", visual="brute",
                detail="Build two fresh sets for every cell.",
                why="Correct, but repeats each diagonal's work per cell.",
            ),
            Choice(
                "Count cells, not distinct values", INCORRECT, time="O(m·n)", space="O(1)", visual="counting",
                detail="Use how many cells lie on each side.",
                why="Repeated values on a diagonal count once.",
            ),
            Choice(
                "Use the cell's row and column", INCORRECT, time="O(m·n)", space="O(m + n)", visual="matrix",
                detail="Count distinct values above and to the left.",
                why="The task is about the diagonal only.",
            ),
        ),
    ),
    Question(
        slug="sort-the-matrix-diagonally", number=1329, title="Sort the Matrix Diagonally",
        difficulty="Medium", topics=("data-structures",),
        summary="Sort each top-left-to-bottom-right diagonal of a matrix in ascending order.",
        example="[[3,3,1,1],[2,2,1,2],[1,1,1,2]]  →  [[1,1,1,1],[1,2,2,2],[1,2,3,3]]",
        criterion="Which approach is O(m·n log min(m, n))?",
        hint="What key do all cells on one diagonal share?",
        choices=(
            Choice(
                "Group by i − j, sort, write back", OPTIMAL, time="O(m·n log min(m, n))", space="O(m·n)", visual="matrix",
                detail="Collect each diagonal, sort it, and refill its cells in order.",
                why="i − j identifies a diagonal, and sorting each one independently is exactly what's asked.",
            ),
            Choice(
                "Bubble sort each diagonal in place", SUBOPTIMAL, time="O(m·n·min(m, n))", space="O(1)", visual="brute",
                detail="Swap out-of-order neighbours along the diagonal.",
                why="Correct, but quadratic per diagonal.",
            ),
            Choice(
                "Sort the anti-diagonals", INCORRECT, time="O(m·n log)", space="O(m·n)", visual="sort",
                detail="Group by i + j instead.",
                why="i + j is the other direction.",
            ),
            Choice(
                "Sort the whole matrix", INCORRECT, time="O(m·n log(m·n))", space="O(m·n)", visual="sort",
                detail="Sort all values and fill row by row.",
                why="Values must stay on their diagonal.",
            ),
        ),
    ),
    Question(
        slug="diagonal-traverse", number=498, title="Diagonal Traverse",
        difficulty="Medium", topics=("data-structures",),
        summary="Return the matrix's elements in zigzag diagonal order: up-right along one anti-diagonal, down-left along the next, and so on.",
        example="[[1,2,3],[4,5,6],[7,8,9]]  →  [1,2,4,7,5,3,6,8,9]",
        criterion="Which approach uses O(1) extra space besides the output?",
        hint="Cells on one anti-diagonal share i + j. Which end of it should you start from?",
        choices=(
            Choice(
                "Walk each anti-diagonal in the right direction", OPTIMAL, time="O(m·n)", space="O(1)", visual="matrix",
                detail="For d = i + j from 0 to m + n − 2, start at the correct end (by parity of d) and step diagonally.",
                why="Choosing the start by d's parity emits each anti-diagonal in the right order directly, with no buffer.",
            ),
            Choice(
                "Collect anti-diagonals, reverse every other", SUBOPTIMAL, time="O(m·n)", space="O(m·n)", visual="array-copy",
                detail="Group cells by i + j, then reverse alternate groups.",
                why="Correct and linear, but stores every diagonal first.",
            ),
            Choice(
                "Same direction every time", INCORRECT, time="O(m·n)", space="O(1)", visual="matrix",
                detail="Always go up-right.",
                why="The second diagonal should be 2 then 4, not 4 then 2.",
            ),
            Choice(
                "Row-major order", INCORRECT, time="O(m·n)", space="O(1)", visual="matrix",
                detail="Read rows left to right.",
                why="That's [1,2,3,…], not a diagonal walk.",
            ),
        ),
    ),
    Question(
        slug="max-black-square-lcci", number=None, title="Max Black Square",
        difficulty="Medium", topics=("data-structures",),
        ref="面试题 17.23", url="https://leetcode.cn/problems/max-black-square-lcci/",
        summary="In an n×n grid of 0 (black) and 1 (white), find the largest square whose four borders are all black. Return [row, col, size] (top-left, smallest row then column on ties), or [].",
        example="[[1,0,1],[0,0,1],[0,0,1]]  →  [1, 0, 2]",
        criterion="Which approach checks each candidate square in O(1)?",
        hint="If you knew how far black extends right and down from every cell, how would you test a square's borders?",
        choices=(
            Choice(
                "Right and down black runs, then try sizes", OPTIMAL, time="O(n³)", space="O(n²)", visual="dp-2d",
                detail="Precompute right[r][c] and down[r][c]; for each top-left, try sizes from large to small, checking the four runs.",
                why="A border is black exactly when the run from its start is long enough. Four lookups test a square.",
            ),
            Choice(
                "Walk the borders of every square", SUBOPTIMAL, time="O(n⁴)", space="O(1)", visual="brute",
                detail="For each top-left and size, check all border cells.",
                why="Correct, but each check costs O(size).",
            ),
            Choice(
                "Largest all-black square", INCORRECT, time="O(n²)", space="O(n²)", visual="dp-2d",
                detail="Classic maximal square DP.",
                why="Only the borders must be black. The inside can be white.",
            ),
            Choice(
                "Largest black row run", INCORRECT, time="O(n²)", space="O(1)", visual="matrix",
                detail="Use the longest horizontal black segment as the size.",
                why="The other three sides must be black too.",
            ),
        ),
    ),
    Question(
        slug="longest-line-of-consecutive-one-in-matrix", number=562, title="Longest Line of Consecutive One in Matrix",
        difficulty="Medium", topics=("data-structures",),
        summary="Return the longest line of consecutive 1s in a binary matrix: horizontal, vertical, diagonal or anti-diagonal.",
        example="[[0,1,1,0],[0,1,1,0],[0,0,0,1]]  →  3",
        criterion="Which approach is O(m·n)?",
        hint="For each cell and each direction, the run ending here extends the run ending at one neighbour.",
        choices=(
            Choice(
                "Four run counters per cell", OPTIMAL, time="O(m·n)", space="O(n)", visual="dp-2d",
                detail="For each 1, set h, v, d, a from the left, up, up-left and up-right neighbours plus one; track the max.",
                why="Each run ending at a cell continues exactly one neighbour's run in that direction, so one pass covers all four.",
            ),
            Choice(
                "Walk four directions from every cell", SUBOPTIMAL, time="O(m·n·max(m, n))", space="O(1)", visual="brute",
                detail="Extend from each 1 in each direction.",
                why="Correct, but re-walks the same lines.",
            ),
            Choice(
                "Rows and columns only", INCORRECT, time="O(m·n)", space="O(n)", visual="matrix",
                detail="Track horizontal and vertical runs.",
                why="The example's longest line is diagonal: (0,1), (1,2), (2,3).",
            ),
            Choice(
                "Count ones per row", INCORRECT, time="O(m·n)", space="O(1)", visual="counting",
                detail="Use the row with the most 1s.",
                why="Ones in a row needn't be consecutive.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §1.1 prefix sums
    Question(
        slug="range-sum-query-immutable", number=303, title="Range Sum Query - Immutable",
        difficulty="Easy", topics=("data-structures",),
        summary="Answer many queries sumRange(left, right) on a fixed array.",
        example="[-2,0,3,-5,2,-1]: sumRange(0, 2) → 1, sumRange(2, 5) → -1",
        criterion="Which approach answers each query in O(1)?",
        hint="If you knew the sum of every prefix, how would you get the sum of a middle part?",
        choices=(
            Choice(
                "Prefix sums, s[r + 1] − s[l]", OPTIMAL, time="O(n) build, O(1) query", space="O(n)", visual="prefix",
                detail="s[0] = 0 and s[i + 1] = s[i] + nums[i]; sumRange(l, r) = s[r + 1] − s[l].",
                why="A range is a long prefix minus a short one. With s defined on half-open ranges, no ±1 fixes are needed.",
            ),
            Choice(
                "Add up each range", SUBOPTIMAL, time="O(n) per query", space="O(1)", visual="brute",
                detail="Loop from left to right on every call.",
                why="Correct, but repeated queries redo the same additions.",
            ),
            Choice(
                "s[r] − s[l]", INCORRECT, time="O(1) query", space="O(n)", visual="prefix",
                detail="Use prefix sums without the shift.",
                why="With s[i] = sum of the first i elements, s[2] − s[0] leaves out nums[2].",
            ),
            Choice(
                "Precompute all ranges", INCORRECT, time="O(n²) build", space="O(n²)", visual="dp-2d",
                detail="Store every (l, r) sum in a table.",
                why="It answers in O(1), but with n = 10⁴ that's 10⁸ entries. Does it fit?",
            ),
        ),
    ),
    Question(
        slug="sum-of-variable-length-subarrays", number=3427, title="Sum of Variable Length Subarrays",
        difficulty="Easy", topics=("data-structures",),
        summary="For each i, take the subarray nums[max(0, i − nums[i])..i]. Return the total of all these subarray sums.",
        example="[2,3,1]  →  11",
        criterion="Which approach is linear?",
        hint="Each subarray ends at i. How do prefix sums give its sum in O(1)?",
        choices=(
            Choice(
                "Prefix sums per subarray", OPTIMAL, time="O(n)", space="O(n)", visual="prefix",
                detail="Add s[i + 1] − s[max(0, i − nums[i])] for each i.",
                why="Each subarray is one prefix difference, so n subarrays cost O(n).",
            ),
            Choice(
                "Add each subarray directly", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="Loop over each subarray's elements.",
                why="Correct, but long subarrays overlap heavily.",
            ),
            Choice(
                "Start at i − nums[i] + 1", INCORRECT, time="O(n)", space="O(n)", visual="prefix",
                detail="Use one fewer element.",
                why="For i = 2 with nums[2] = 1, the subarray is nums[1..2]. Does this start include nums[1]?",
            ),
            Choice(
                "Sum of nums[i] · (nums[i] + 1)", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="Assume each subarray repeats nums[i].",
                why="The subarray holds different values, not copies of nums[i].",
            ),
        ),
    ),
    Question(
        slug="count-vowel-strings-in-ranges", number=2559, title="Count Vowel Strings in Ranges",
        difficulty="Medium", topics=("data-structures",),
        summary="For each query [l, r], count words in words[l..r] that start and end with a vowel.",
        example="[\"aba\",\"bcb\",\"ece\",\"aa\",\"e\"], [[0,2],[1,4],[1,1]]  →  [2,3,0]",
        criterion="Which approach is O(n + q)?",
        hint="Turn each word into 0 or 1. What answers range counts quickly?",
        choices=(
            Choice(
                "Prefix count of vowel words", OPTIMAL, time="O(n + q)", space="O(n)", visual="prefix",
                detail="s[i + 1] = s[i] + (word i qualifies); answer s[r + 1] − s[l].",
                why="Counting in a range is summing 0/1 flags, which prefix sums answer in O(1).",
            ),
            Choice(
                "Scan each range", SUBOPTIMAL, time="O(n·q)", space="O(1)", visual="brute",
                detail="Check every word in [l, r] per query.",
                why="Correct, but rechecks words for every query.",
            ),
            Choice(
                "Words containing a vowel", INCORRECT, time="O(n + q)", space="O(n)", visual="prefix",
                detail="Flag words with any vowel.",
                why="\"bcb\" has no vowel ends. Would \"bab\" count?",
            ),
            Choice(
                "Words starting with a vowel", INCORRECT, time="O(n + q)", space="O(n)", visual="prefix",
                detail="Check only the first letter.",
                why="Both ends must be vowels.",
            ),
        ),
    ),
    Question(
        slug="xor-queries-of-a-subarray", number=1310, title="XOR Queries of a Subarray",
        difficulty="Medium", topics=("data-structures",),
        summary="For each query [l, r], return arr[l] XOR … XOR arr[r].",
        example="[1,3,4,8], [[0,1],[1,2],[0,3],[3,3]]  →  [2,7,14,8]",
        criterion="Which approach is O(n + q)?",
        hint="XOR undoes itself. What's the XOR analogue of a prefix difference?",
        choices=(
            Choice(
                "Prefix XOR", OPTIMAL, time="O(n + q)", space="O(n)", visual="prefix",
                detail="p[i + 1] = p[i] ^ arr[i]; answer p[r + 1] ^ p[l].",
                why="x ^ x = 0, so XORing two prefixes cancels the shared part and leaves the range.",
            ),
            Choice(
                "XOR each range directly", SUBOPTIMAL, time="O(n·q)", space="O(1)", visual="brute",
                detail="Loop over the range per query.",
                why="Correct, but repeats work across queries.",
            ),
            Choice(
                "Prefix sums, then subtract", INCORRECT, time="O(n + q)", space="O(n)", visual="prefix",
                detail="Use sums instead of XOR.",
                why="1 + 3 = 4 but 1 XOR 3 = 2.",
            ),
            Choice(
                "p[r] ^ p[l]", INCORRECT, time="O(n + q)", space="O(n)", visual="prefix",
                detail="Use the unshifted prefixes.",
                why="With p[i] covering the first i elements, that misses arr[r] and includes arr[l] wrongly.",
            ),
        ),
    ),
    Question(
        slug="special-array-ii", number=3152, title="Special Array II",
        difficulty="Medium", topics=("data-structures",),
        summary="A subarray is special if every pair of adjacent elements has different parity. Answer whether nums[l..r] is special for each query.",
        example="[4,3,1,6], [[0,2],[2,3]]  →  [false, true]",
        criterion="Which approach is O(n + q)?",
        hint="Mark each adjacent pair that breaks the rule. When is a range special?",
        choices=(
            Choice(
                "Prefix count of bad adjacent pairs", OPTIMAL, time="O(n + q)", space="O(n)", visual="prefix",
                detail="bad[i] = 1 if nums[i − 1] and nums[i] share parity; query is special iff the count over (l, r] is 0.",
                why="A range fails exactly when it contains a bad pair, and prefix counts tell that in O(1).",
            ),
            Choice(
                "Check each range", SUBOPTIMAL, time="O(n·q)", space="O(1)", visual="brute",
                detail="Walk adjacent pairs inside [l, r].",
                why="Correct, but rescans per query.",
            ),
            Choice(
                "Count bad pairs over [l, r]", INCORRECT, time="O(n + q)", space="O(n)", visual="prefix",
                detail="Include the pair (l − 1, l).",
                why="That pair has one element outside the range. Should it matter?",
            ),
            Choice(
                "Compare the endpoints' parity", INCORRECT, time="O(1) query", space="O(1)", visual="math",
                detail="Special if nums[l] and nums[r] fit an alternating pattern.",
                why="A break in the middle wouldn't be seen.",
            ),
        ),
    ),
    Question(
        slug="maximum-absolute-sum-of-any-subarray", number=1749, title="Maximum Absolute Sum of Any Subarray",
        difficulty="Medium", topics=("data-structures",),
        summary="Return the largest |sum| over all subarrays (the empty subarray counts as 0).",
        example="[1,-3,2,3,-4]  →  5",
        criterion="Which approach is linear with O(1) extra space?",
        hint="A subarray sum is a difference of two prefix sums. Which two give the largest absolute difference?",
        choices=(
            Choice(
                "Max prefix minus min prefix", OPTIMAL, time="O(n)", space="O(1)", visual="prefix",
                detail="Track the running sum's max and min (starting at 0); return max − min.",
                why="|s[j] − s[i]| is largest when the two prefixes are the extremes, and their order doesn't matter for absolute value.",
            ),
            Choice(
                "Check every subarray", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="Extend from each start, tracking |sum|.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Kadane only", INCORRECT, time="O(n)", space="O(1)", visual="dp-1d",
                detail="Return the maximum subarray sum.",
                why="For [-5,1], the best is |−5| = 5, a negative subarray.",
            ),
            Choice(
                "Sum of absolute values", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="Add |x| for every element.",
                why="Signs inside one subarray cancel.",
            ),
        ),
    ),
    Question(
        slug="maximum-subarray", number=53, title="Maximum Subarray",
        difficulty="Medium", topics=("data-structures",),
        summary="Return the largest sum of a non-empty contiguous subarray.",
        example="[-2,1,-3,4,-1,2,1,-5,4]  →  6",
        criterion="Which approach is linear with O(1) extra space?",
        hint="Ending at j, the best start is where the prefix sum before it was smallest.",
        choices=(
            Choice(
                "Running prefix minus running min prefix", OPTIMAL, time="O(n)", space="O(1)", visual="prefix",
                detail="For each j, try s − minPrefix, then update minPrefix with s (Kadane is the same idea).",
                why="Enumerate the right end and keep the best left prefix: the smallest one seen so far.",
            ),
            Choice(
                "Prefix sums, every pair", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="brute",
                detail="Try s[j + 1] − s[i] for all i ≤ j.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Sum of positives", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Add every positive element.",
                why="The subarray must be contiguous. In the example, 4 and the last 4 are separated by −5.",
            ),
            Choice(
                "Reset at any negative", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Start a new sum whenever a negative number appears.",
                why="4, −1, 2, 1 sums to 6 across a negative. Should −1 break it?",
            ),
        ),
    ),
    Question(
        slug="shift-distance-between-two-strings", number=3361, title="Shift Distance Between Two Strings",
        difficulty="Medium", topics=("data-structures",),
        summary="Shifting letter j forward costs nextCost[j]; backward costs previousCost[j] (both wrap). Return the cheapest total cost to turn s into t.",
        example="\"leet\" → \"code\", all costs 1  →  31",
        criterion="Which approach is O(n + 26)?",
        hint="Moving from letter a to letter b forward costs a sum of consecutive nextCost entries. How do you get such sums in O(1), with wrap-around?",
        choices=(
            Choice(
                "Prefix sums over doubled cost arrays", OPTIMAL, time="O(n + 26)", space="O(1)", visual="prefix",
                detail="Build prefix sums of nextCost and previousCost repeated twice (length 52); each position costs min(forward range, backward range).",
                why="Doubling the 26 costs turns every wrapping range into a plain range, so each character's two options are O(1) differences.",
            ),
            Choice(
                "Walk letter by letter", SUBOPTIMAL, time="O(26·n)", space="O(1)", visual="brute",
                detail="Sum the costs step by step in both directions.",
                why="Correct, but up to 25 steps per character.",
            ),
            Choice(
                "Always shift forward", INCORRECT, time="O(n + 26)", space="O(1)", visual="prefix",
                detail="Use only nextCost.",
                why="In example 1, a → b backward costs 1 while forward costs 100.",
            ),
            Choice(
                "Fewest steps, then pay", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Go whichever way is shorter, then add up its costs.",
                why="Shorter isn't cheaper when costs differ per letter.",
            ),
        ),
    ),
    Question(
        slug="make-a-positive-array", number=3511, title="Make a Positive Array",
        difficulty="Medium", topics=("data-structures",),
        summary="An array is positive if every subarray with more than two elements has a positive sum. One operation replaces any element with any value. Return the fewest operations.",
        example="[-10,15,-12]  →  1",
        criterion="Which approach is linear?",
        hint="Scan left to right. When a long-enough subarray ending at i fails, which element is best to replace?",
        choices=(
            Choice(
                "Greedy scan with prefix sums", OPTIMAL, time="O(n)", space="O(1)", visual="prefix",
                detail="Track the largest prefix sum ending at least two positions back; if the current prefix isn't above it, replace nums[i] with a huge value, count it, and restart after i.",
                why="A failing subarray ending at i must be fixed by some element in it; replacing the rightmost one with a huge value also fixes every later subarray that contains it.",
            ),
            Choice(
                "Recheck all subarrays after each step", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="Same greedy, but test every subarray ending at i directly.",
                why="Correct, but each step rescans its left side.",
            ),
            Choice(
                "Replace every negative", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Count the negative numbers.",
                why="The example has two negatives, but one replacement fixes it.",
            ),
            Choice(
                "Check length-3 windows only", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Fix triples with non-positive sums.",
                why="Longer subarrays can fail even when every triple is positive.",
            ),
        ),
    ),
    Question(
        slug="minimum-time-to-visit-all-houses", number=3540, title="Minimum Time to Visit All Houses",
        difficulty="Medium", topics=("data-structures",),
        summary="Houses 0..n−1 sit on a circle. forward[i] is the road length from i to i + 1, backward[i] from i to i − 1. Starting at house 0, visit the houses in queries in order. Return the shortest total distance.",
        example="forward = [1,4,4], backward = [4,1,2], queries = [1,2,0,2]  →  12",
        criterion="Which approach is O(n + q)?",
        hint="Each leg goes either clockwise or counter-clockwise. How do you get either length in O(1)?",
        choices=(
            Choice(
                "Prefix sums in both directions", OPTIMAL, time="O(n + q)", space="O(n)", visual="prefix",
                detail="Build prefix sums of forward and backward; each leg costs the smaller of the two arc sums (wrapping via the total).",
                why="Each direction is a contiguous arc, so its length is one prefix difference, possibly wrapping around the total.",
            ),
            Choice(
                "Walk each leg", SUBOPTIMAL, time="O(n·q)", space="O(1)", visual="brute",
                detail="Add road lengths step by step both ways.",
                why="Correct, but a leg can be n roads long.",
            ),
            Choice(
                "Always go forward", INCORRECT, time="O(n + q)", space="O(n)", visual="prefix",
                detail="Use only forward roads.",
                why="Going back one house may be much shorter than going around.",
            ),
            Choice(
                "Use forward lengths both ways", INCORRECT, time="O(n + q)", space="O(n)", visual="prefix",
                detail="Assume a road is equally long in both directions.",
                why="forward and backward lengths differ.",
            ),
        ),
    ),
    Question(
        slug="count-odd-numbers-in-an-interval-range", number=1523, title="Count Odd Numbers in an Interval Range",
        difficulty="Easy", topics=("data-structures",),
        summary="Count the odd numbers between low and high inclusive.",
        example="low = 3, high = 7  →  3",
        criterion="Which approach is O(1)?",
        hint="How many odd numbers are in [0, x]? Then subtract.",
        choices=(
            Choice(
                "Prefix count formula", OPTIMAL, time="O(1)", space="O(1)", visual="prefix",
                detail="odds(x) = (x + 1) / 2 counts odds in [0, x]; answer odds(high) − odds(low − 1).",
                why="It's a prefix difference on the implicit array 'is odd', with a closed form for each prefix.",
            ),
            Choice(
                "Loop and count", SUBOPTIMAL, time="O(high − low)", space="O(1)", visual="brute",
                detail="Check each number's parity.",
                why="Correct, but the range can be 10⁹ long.",
            ),
            Choice(
                "(high − low) / 2", INCORRECT, time="O(1)", space="O(1)", visual="math",
                detail="Half the gap.",
                why="For 3..7 that gives 2, but 3, 5, 7 are odd.",
            ),
            Choice(
                "(high − low) / 2 + 1", INCORRECT, time="O(1)", space="O(1)", visual="math",
                detail="Half the gap plus one.",
                why="For 2..4 that gives 2, but only 3 is odd.",
            ),
        ),
    ),
    Question(
        slug="shifting-letters", number=848, title="Shifting Letters",
        difficulty="Medium", topics=("data-structures",),
        summary="shifts[i] means shift the first i + 1 letters forward by shifts[i] (wrapping). Return the final string.",
        example="\"abc\", [3,5,9]  →  \"rpl\"",
        criterion="Which approach is linear?",
        hint="How much does letter i move in total?",
        choices=(
            Choice(
                "Suffix sums of shifts", OPTIMAL, time="O(n)", space="O(1)", visual="prefix",
                detail="Walk from the right, accumulating shifts mod 26, and shift each letter by the running total.",
                why="Letter i is moved by every shift at index ≥ i, which is a suffix sum.",
            ),
            Choice(
                "Apply each shift to its prefix", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="brute",
                detail="For each i, move letters 0..i.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Prefix sums of shifts", INCORRECT, time="O(n)", space="O(1)", visual="prefix",
                detail="Shift letter i by shifts[0] + … + shifts[i].",
                why="shifts[0] only touches letter 0. Should letter 2 move by it?",
            ),
            Choice(
                "No mod until the end", INCORRECT, time="O(n)", space="O(1)", visual="prefix",
                detail="Add raw totals and take % 26 when building the letter.",
                why="Totals can reach 10⁵ × 10⁹. Does that fit in 32 bits?",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §1.2 prefix sums with a hash map
    Question(
        slug="subarray-sum-equals-k", number=560, title="Subarray Sum Equals K",
        difficulty="Medium", topics=("data-structures",),
        summary="Count subarrays whose sum equals k. Values may be negative.",
        example="[1,1,1], k = 2  →  2",
        criterion="Which approach is linear?",
        hint="A subarray ending at j sums to k when an earlier prefix equals what?",
        choices=(
            Choice(
                "Count earlier prefixes equal to s − k", OPTIMAL, time="O(n)", space="O(n)", visual="prefix",
                detail="Start with count[0] = 1; for each prefix s, add count[s − k], then count[s] += 1.",
                why="Each earlier prefix equal to s − k marks one start. A map counts them in O(1).",
            ),
            Choice(
                "Every subarray", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="Extend from each start with a running sum.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Sliding window", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Shrink while the sum exceeds k.",
                why="With negatives, adding can lower the sum, so the window's logic breaks.",
            ),
            Choice(
                "Forget count[0] = 1", INCORRECT, time="O(n)", space="O(n)", visual="prefix",
                detail="Start with an empty map.",
                why="A subarray starting at index 0 needs the empty prefix. Is [1,1] counted?",
            ),
        ),
    ),
    Question(
        slug="number-of-sub-arrays-with-odd-sum", number=1524, title="Number of Sub-arrays With Odd Sum",
        difficulty="Medium", topics=("data-structures",),
        summary="Count subarrays with an odd sum, mod 10⁹ + 7.",
        example="[1,3,5]  →  4",
        criterion="Which approach is linear with O(1) extra space?",
        hint="A subarray's sum is odd when its two prefixes have what parities?",
        choices=(
            Choice(
                "Count prefix parities", OPTIMAL, time="O(n)", space="O(1)", visual="prefix",
                detail="Keep counts of even and odd prefixes (even starts at 1); add the count of the opposite parity.",
                why="Odd minus even is odd. Two counters stand in for the whole map.",
            ),
            Choice(
                "Every subarray", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="Extend from each start, tracking parity.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Count odd elements", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Each odd element is one odd subarray.",
                why="[1,3,5] as a whole sums to 9, odd. Is it counted?",
            ),
            Choice(
                "Pair with same parity", INCORRECT, time="O(n)", space="O(1)", visual="prefix",
                detail="Add the count of prefixes with the same parity.",
                why="Same parity gives an even difference.",
            ),
        ),
    ),
    Question(
        slug="subarray-sums-divisible-by-k", number=974, title="Subarray Sums Divisible by K",
        difficulty="Medium", topics=("data-structures",),
        summary="Count subarrays whose sum is divisible by k. Values may be negative.",
        example="[4,5,0,-2,-3,1], k = 5  →  7",
        criterion="Which approach is O(n + k)?",
        hint="Two prefixes with the same remainder bracket what kind of subarray?",
        choices=(
            Choice(
                "Count prefix remainders", OPTIMAL, time="O(n + k)", space="O(k)", visual="prefix",
                detail="Normalize r = ((s % k) + k) % k; add count[r], then count[r] += 1 (count[0] starts at 1).",
                why="Equal remainders differ by a multiple of k. Normalizing keeps negative sums in the same bucket as their positive equivalents.",
            ),
            Choice(
                "Every subarray", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="Check each running sum.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Raw remainder in C++/Java", INCORRECT, time="O(n + k)", space="O(k)", visual="prefix",
                detail="Use s % k directly as the key.",
                why="−1 % 5 is −1 there, not 4. Will −1 and 4 meet?",
            ),
            Choice(
                "Count elements divisible by k", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Count x with x % k == 0.",
                why="[5,0] works, and so does [−2,−3].",
            ),
        ),
    ),
    Question(
        slug="continuous-subarray-sum", number=523, title="Continuous Subarray Sum",
        difficulty="Medium", topics=("data-structures",),
        summary="Return whether some subarray of length at least 2 has a sum that's a multiple of k.",
        example="[23,2,4,6,7], k = 6  →  true",
        criterion="Which approach is linear?",
        hint="Equal prefix remainders mean a multiple of k. Which occurrence of a remainder should you keep to satisfy 'length ≥ 2'?",
        choices=(
            Choice(
                "Earliest index per remainder", OPTIMAL, time="O(n)", space="O(min(n, k))", visual="prefix",
                detail="Store remainder → first prefix index (0 → −1); if seen at j with i − j ≥ 2, return true.",
                why="Keeping the earliest index maximizes length, so if any valid pair exists for this remainder, the earliest one works.",
            ),
            Choice(
                "Every subarray", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="Check all lengths ≥ 2.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Latest index per remainder", INCORRECT, time="O(n)", space="O(min(n, k))", visual="prefix",
                detail="Overwrite the index each time.",
                why="For [5,0,0] and k = 3, the latest index can be too close. Would [0,0] still be found?",
            ),
            Choice(
                "Allow length 1", INCORRECT, time="O(n)", space="O(k)", visual="prefix",
                detail="Accept any repeated remainder.",
                why="[6] alone is a multiple of 6, but too short.",
            ),
        ),
    ),
    Question(
        slug="count-the-number-of-beautiful-subarrays", number=2588, title="Count the Number of Beautiful Subarrays",
        difficulty="Medium", topics=("data-structures",),
        summary="An operation picks two elements sharing a set bit k and subtracts 2ᵏ from both. A subarray is beautiful if it can be made all zero. Count beautiful subarrays.",
        example="[4,3,1,2,4]  →  2",
        criterion="Which approach is linear?",
        hint="Each operation removes a bit from two elements. What must be true of every bit position's count?",
        choices=(
            Choice(
                "Count equal prefix XORs", OPTIMAL, time="O(n)", space="O(n)", visual="prefix",
                detail="A subarray is beautiful iff its XOR is 0; add count[prefixXor], then increment it (count[0] = 1).",
                why="Every bit must appear an even number of times, which is XOR = 0. Equal prefix XORs bracket exactly those subarrays.",
            ),
            Choice(
                "Every subarray's XOR", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="Extend from each start, tracking XOR.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Sum is even", INCORRECT, time="O(n)", space="O(1)", visual="prefix",
                detail="Count subarrays with even sum.",
                why="[1,2,1] sums to 4, but bit 1 appears once.",
            ),
            Choice(
                "Equal adjacent elements", INCORRECT, time="O(n)", space="O(1)", visual="two-pointers",
                detail="Count pairs of equal neighbours.",
                why="[3,1,2] has XOR 0 with no equal neighbours.",
            ),
        ),
    ),
    Question(
        slug="contiguous-array", number=525, title="Contiguous Array",
        difficulty="Medium", topics=("data-structures",),
        summary="Return the length of the longest subarray of a binary array with equal 0s and 1s.",
        example="[0,1,0]  →  2",
        criterion="Which approach is linear?",
        hint="Count 1 as +1 and 0 as −1. What does a balanced subarray look like in prefix sums?",
        choices=(
            Choice(
                "First index of each balance", OPTIMAL, time="O(n)", space="O(n)", visual="prefix",
                detail="Store balance → earliest index (0 → −1); at each i, try i − first[balance].",
                why="Equal balances bracket a subarray with sum 0. The earliest occurrence gives the longest one ending at i.",
            ),
            Choice(
                "Every subarray", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="Extend from each start, tracking the balance.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "2 · min(zeros, ones)", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Balance the totals.",
                why="For [1,0,0,0,0,1] that gives 4, but the 1s are far apart. The answer is 2.",
            ),
            Choice(
                "Latest index of each balance", INCORRECT, time="O(n)", space="O(n)", visual="prefix",
                detail="Overwrite the index each time.",
                why="That finds the shortest balanced subarray ending at i, not the longest.",
            ),
        ),
    ),
    Question(
        slug="find-longest-subarray-lcci", number=None, title="Find Longest Subarray",
        difficulty="Medium", topics=("data-structures",),
        ref="面试题 17.05", url="https://leetcode.cn/problems/find-longest-subarray-lcci/",
        summary="An array holds letters and digits. Return the longest subarray with equally many letters and digits (the leftmost on ties), or [].",
        example="[\"A\",\"1\",\"B\",\"C\",\"D\",\"2\",\"3\",\"4\",\"E\",\"5\",\"F\",\"G\",\"6\",\"7\",\"H\",\"I\",\"J\",\"K\",\"L\",\"M\"]  →  the first 14 items",
        criterion="Which approach is linear?",
        hint="It's Contiguous Array with letters as +1 and digits as −1.",
        choices=(
            Choice(
                "First index of each balance, strict improvement", OPTIMAL, time="O(n)", space="O(n)", visual="prefix",
                detail="Store balance → earliest index; update the answer only when a strictly longer subarray appears.",
                why="Earliest indices give the longest subarray per end, and strict improvement keeps the leftmost on ties.",
            ),
            Choice(
                "Every subarray", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="Track letters minus digits from each start.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Update on equal length", INCORRECT, time="O(n)", space="O(n)", visual="prefix",
                detail="Replace the answer when the length ties.",
                why="That keeps the rightmost of equal-length answers.",
            ),
            Choice(
                "Latest index per balance", INCORRECT, time="O(n)", space="O(n)", visual="prefix",
                detail="Overwrite the stored index.",
                why="That shortens every candidate.",
            ),
        ),
    ),
    Question(
        slug="find-maximum-balanced-xor-subarray-length", number=3755, title="Find Maximum Balanced XOR Subarray Length",
        difficulty="Medium", topics=("data-structures",),
        summary="Return the longest subarray whose XOR is 0 and which has equally many even and odd numbers, or 0.",
        example="[3,1,3,2,0]  →  4",
        criterion="Which approach is linear?",
        hint="Each condition is 'two prefixes are equal' for some prefix quantity. Combine them.",
        choices=(
            Choice(
                "First index of each (XOR, balance) pair", OPTIMAL, time="O(n)", space="O(n)", visual="prefix",
                detail="Key = (prefix XOR, evens − odds); store the earliest index and measure from it.",
                why="Both conditions hold exactly when both prefix quantities match, so a pair key captures them together.",
            ),
            Choice(
                "Every subarray", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="Track XOR and balance from each start.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Two separate maps", INCORRECT, time="O(n)", space="O(n)", visual="hashmap",
                detail="Find the longest XOR-zero and the longest balanced subarray separately and take the shorter.",
                why="Those two subarrays needn't be the same subarray.",
            ),
            Choice(
                "XOR only", INCORRECT, time="O(n)", space="O(n)", visual="prefix",
                detail="Longest subarray with XOR 0.",
                why="[3,1,3,2,0] also has XOR 0 but 3 odds and 2 evens.",
            ),
        ),
    ),
    Question(
        slug="count-triplets-that-can-form-two-arrays-of-equal-xor", number=1442, title="Count Triplets That Can Form Two Arrays of Equal XOR",
        difficulty="Medium", topics=("data-structures",),
        summary="Count (i, j, k) with i < j ≤ k and XOR(arr[i..j−1]) = XOR(arr[j..k]).",
        example="[2,3,1,6,7]  →  4",
        criterion="Which approach is linear?",
        hint="a = b means XOR(arr[i..k]) = 0. Then how many j work?",
        choices=(
            Choice(
                "Equal prefix XORs, summing index gaps", OPTIMAL, time="O(n)", space="O(n)", visual="prefix",
                detail="For each prefix, keep the count and the index sum of earlier equal prefixes; each match at (i, k) adds k − i choices of j.",
                why="Any split j inside a zero-XOR range works. Keeping count and index sum per key adds all those gaps in O(1).",
            ),
            Choice(
                "Pairs of equal prefixes", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="prefix",
                detail="For every i < k with equal prefixes, add k − i.",
                why="Correct, but enumerates pairs one by one.",
            ),
            Choice(
                "One j per zero-XOR range", INCORRECT, time="O(n)", space="O(n)", visual="prefix",
                detail="Count zero-XOR ranges.",
                why="Every j inside such a range is a different triplet.",
            ),
            Choice(
                "Every triple", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="C(n, 3).",
                why="Most splits don't give equal XORs.",
            ),
        ),
    ),
    Question(
        slug="valid-subarrays-with-matching-sum-digits-i", number=3969, title="Valid Subarrays With Matching Sum Digits I",
        difficulty="Medium", topics=("data-structures",),
        summary="A subarray is valid if its sum's first and last digits both equal x. Count valid subarrays. n ≤ 1500.",
        example="[1,100,1], x = 1  →  4",
        criterion="Which approach is O(n²)?",
        hint="With n ≤ 1500, every subarray can be checked, if each sum costs O(1).",
        choices=(
            Choice(
                "Every subarray with a running sum", OPTIMAL, time="O(n²·d)", space="O(1)", visual="prefix",
                detail="Extend from each start, updating the sum, and check its first and last digits.",
                why="The running sum gives each subarray's total in O(1); checking digits costs O(d).",
            ),
            Choice(
                "Recompute each sum", SUBOPTIMAL, time="O(n³)", space="O(1)", visual="brute",
                detail="Add the elements of every subarray from scratch.",
                why="Correct, but redoes the additions.",
            ),
            Choice(
                "Last digit only", INCORRECT, time="O(n)", space="O(1)", visual="prefix",
                detail="Count subarrays whose sum ends in x via remainders mod 10.",
                why="11 ends in 1 and starts with 1, but 21 ends in 1 and starts with 2.",
            ),
            Choice(
                "First digit of each element", INCORRECT, time="O(n²)", space="O(1)", visual="brute",
                detail="Check that both ends of the subarray start with x.",
                why="The rule is about the sum's digits, not the elements'.",
            ),
        ),
    ),
    Question(
        slug="maximum-size-subarray-sum-equals-k", number=325, title="Maximum Size Subarray Sum Equals k",
        difficulty="Medium", topics=("data-structures",),
        summary="Return the length of the longest subarray summing to k. Values may be negative.",
        example="[1,-1,5,-2,3], k = 3  →  4",
        criterion="Which approach is linear?",
        hint="Ending at j, which earlier prefix gives the longest subarray?",
        choices=(
            Choice(
                "Earliest index per prefix sum", OPTIMAL, time="O(n)", space="O(n)", visual="prefix",
                detail="Store prefix → first index (0 → −1); try j − first[s − k].",
                why="Among matching starts, the earliest is longest, so only the first occurrence of each prefix matters.",
            ),
            Choice(
                "Every subarray", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="Track running sums from each start.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Latest index per prefix", INCORRECT, time="O(n)", space="O(n)", visual="prefix",
                detail="Overwrite the index.",
                why="That gives the shortest match ending at j.",
            ),
            Choice(
                "Sliding window", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Shrink while the sum exceeds k.",
                why="Negatives break the window's monotonicity.",
            ),
        ),
    ),
    Question(
        slug="split-array-with-equal-sum", number=548, title="Split Array with Equal Sum",
        difficulty="Hard", topics=("data-structures",),
        summary="Find 0 < i, i + 1 < j, j + 1 < k < n − 1 so that the four parts between the cuts (excluding nums[i], nums[j], nums[k]) all have equal sums.",
        example="[1,2,1,2,1,2,1]  →  true",
        criterion="Which approach is O(n²)?",
        hint="Fix the middle cut j. What can the left side offer, and what must the right side match?",
        choices=(
            Choice(
                "Fix j, set of left sums, scan right", OPTIMAL, time="O(n²)", space="O(n)", visual="prefix",
                detail="For each j, collect sums where the two left parts match (over i); then check k on the right for a match in that set.",
                why="Splitting at j makes the left and right choices independent, joined by a set lookup.",
            ),
            Choice(
                "All three cuts", SUBOPTIMAL, time="O(n³)", space="O(n)", visual="brute",
                detail="Try every (i, j, k) with prefix sums.",
                why="Correct, but cubic.",
            ),
            Choice(
                "Total divisible by 4", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="True if (total − three cut values) can split evenly.",
                why="The cut values aren't known in advance.",
            ),
            Choice(
                "Equal quarters by length", INCORRECT, time="O(n)", space="O(n)", visual="prefix",
                detail="Cut at n/4, n/2, 3n/4.",
                why="Equal sums needn't mean equal lengths.",
            ),
        ),
    ),
    Question(
        slug="widest-pair-of-indices-with-equal-range-sum", number=1983, title="Widest Pair of Indices With Equal Range Sum",
        difficulty="Medium", topics=("data-structures",),
        summary="Given binary arrays nums1 and nums2, return the widest j − i + 1 with sum(nums1[i..j]) = sum(nums2[i..j]).",
        example="nums1 = [1,1,0,1], nums2 = [0,1,1,0]  →  3",
        criterion="Which approach is linear?",
        hint="Look at the difference nums1[x] − nums2[x].",
        choices=(
            Choice(
                "Earliest index per prefix difference", OPTIMAL, time="O(n)", space="O(n)", visual="prefix",
                detail="Prefix of nums1 − nums2; store the first index per value and measure from it.",
                why="Equal range sums mean the difference sums to 0, i.e. two equal prefixes. The earliest gives the widest.",
            ),
            Choice(
                "Every pair", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="Compare running sums from each start.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Positions where both match", INCORRECT, time="O(n)", space="O(1)", visual="two-pointers",
                detail="Longest run with nums1[x] == nums2[x].",
                why="Ranges can balance with mismatches, like [1,0] vs [0,1].",
            ),
            Choice(
                "Equal totals", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Return n if the totals match, else 0.",
                why="A smaller range can balance when the whole doesn't.",
            ),
        ),
    ),
    Question(
        slug="number-of-substrings-with-fixed-ratio", number=2489, title="Number of Substrings With Fixed Ratio",
        difficulty="Medium", topics=("data-structures",),
        summary="Count substrings of a binary string where zeros : ones = num1 : num2 exactly (num1, num2 coprime).",
        example="\"0110011\", num1 = 1, num2 = 2  →  4",
        criterion="Which approach is linear?",
        hint="zeros · num2 = ones · num1. Write that as a difference of two prefix values.",
        choices=(
            Choice(
                "Count prefix values zeros·num2 − ones·num1", OPTIMAL, time="O(n)", space="O(n)", visual="prefix",
                detail="Add count[key] for each prefix, then increment it (count[0] = 1).",
                why="The ratio holds exactly when the key is equal at both ends, so it's the 'equal prefixes' count.",
            ),
            Choice(
                "Every substring", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="Track zeros and ones from each start.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Compare as a float ratio", INCORRECT, time="O(n)", space="O(n)", visual="hashmap",
                detail="Key prefixes by zeros / ones.",
                why="A substring's ratio isn't a ratio of prefix ratios.",
            ),
            Choice(
                "Only length num1 + num2", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Count windows of that length with the right counts.",
                why="Longer multiples like 2:4 also match.",
            ),
        ),
    ),
    Question(
        slug="count-subarrays-with-more-ones-than-zeros", number=2031, title="Count Subarrays With More Ones Than Zeros",
        difficulty="Medium", topics=("data-structures",),
        summary="Count subarrays of a binary array with more 1s than 0s, mod 10⁹ + 7.",
        example="[0,1,1,0,1]  →  9",
        criterion="Which approach is linear?",
        hint="With ±1 prefix balances, you need the number of earlier prefixes smaller than the current one. The balance moves by 1 each step.",
        choices=(
            Choice(
                "Running count of smaller prefixes", OPTIMAL, time="O(n)", space="O(n)", visual="prefix",
                detail="Keep counts per balance and 'number of earlier prefixes < current'; adjust it by count[balance] when stepping up or down.",
                why="Since the balance changes by exactly 1, the smaller-prefix count changes by one bucket's size, so no tree is needed.",
            ),
            Choice(
                "Fenwick tree over balances", SUBOPTIMAL, time="O(n log n)", space="O(n)", visual="prefix",
                detail="Query how many earlier prefixes are below the current one.",
                why="Correct, but the ±1 steps make the log factor unnecessary.",
            ),
            Choice(
                "Equal prefixes", INCORRECT, time="O(n)", space="O(n)", visual="prefix",
                detail="Count earlier prefixes equal to the current one.",
                why="That counts balanced subarrays, not ones with more 1s.",
            ),
            Choice(
                "Count windows with majority ones", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Shrink while zeros ≥ ones.",
                why="Majority isn't monotone in the window, so shrinking can skip valid subarrays.",
            ),
        ),
    ),
    Question(
        slug="number-of-divisible-substrings", number=2950, title="Number of Divisible Substrings",
        difficulty="Medium", topics=("data-structures",),
        summary="Letters map to digits 1–9 as on a phone pad (ab → 1, cde → 2, …). A substring is divisible if its digit sum is divisible by its length. Count them.",
        example="\"abcd\"  →  6",
        criterion="Which approach is O(9·n)?",
        hint="Divisible means the average is an integer, and the average is between 1 and 9.",
        choices=(
            Choice(
                "One prefix count per average", OPTIMAL, time="O(9·n)", space="O(n)", visual="prefix",
                detail="For a = 1..9, count substrings where Σ(digit − a) = 0 using equal prefixes.",
                why="sum = a · length means the shifted values sum to 0. Each a is a 'count equal prefixes' pass.",
            ),
            Choice(
                "Every substring", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="Track sum and length from each start.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Single letters only", INCORRECT, time="O(1)", space="O(1)", visual="math",
                detail="Return n.",
                why="\"ab\" maps to 1, 1 and averages 1. It counts too.",
            ),
            Choice(
                "Sum divisible by 9", INCORRECT, time="O(n)", space="O(9)", visual="prefix",
                detail="Count substrings with sum % 9 == 0.",
                why="The divisor is the length, not 9.",
            ),
        ),
    ),
    Question(
        slug="minimum-positive-sum-subarray", number=3364, title="Minimum Positive Sum Subarray",
        difficulty="Easy", topics=("data-structures",),
        summary="Among subarrays with length between l and r and a positive sum, return the smallest sum, or −1.",
        example="[3,-2,1,4], l = 2, r = 3  →  1",
        criterion="Which approach is O(n log n)?",
        hint="For a right end j, you want the largest earlier prefix that's still below s[j], within the allowed start range.",
        choices=(
            Choice(
                "Prefix sums with a sorted window of starts", OPTIMAL, time="O(n log n)", space="O(n)", visual="prefix",
                detail="Keep prefixes s[j − r..j − l] in a sorted set; find the largest one below s[j].",
                why="sum = s[j] − s[i] is smallest-positive when s[i] is the largest value below s[j]. A sorted set finds it in log time.",
            ),
            Choice(
                "Every allowed subarray", SUBOPTIMAL, time="O(n·(r − l))", space="O(n)", visual="brute",
                detail="Check each length from l to r at every end.",
                why="Correct and fine for small n, but scans the whole length range per end.",
            ),
            Choice(
                "Smallest positive element", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Return the smallest positive number.",
                why="Lengths below l aren't allowed.",
            ),
            Choice(
                "Minimum subarray sum", INCORRECT, time="O(n)", space="O(1)", visual="dp-1d",
                detail="Kadane for the minimum.",
                why="The minimum can be negative. The sum must be positive.",
            ),
        ),
    ),
    Question(
        slug="max-sum-of-rectangle-no-larger-than-k", number=363, title="Max Sum of Rectangle No Larger Than K",
        difficulty="Hard", topics=("data-structures",),
        summary="Return the largest sum of a sub-rectangle of a matrix that is at most k.",
        example="[[1,0,1],[0,-2,3]], k = 2  →  2",
        criterion="Which approach is O(m²·n log n)?",
        hint="Fix the top and bottom rows. The columns then collapse into a 1-D problem.",
        choices=(
            Choice(
                "Row pair, then sorted prefix sums", OPTIMAL, time="O(m²·n log n)", space="O(n)", visual="prefix",
                detail="For each pair of rows, sum columns, then for each prefix s find the smallest earlier prefix ≥ s − k in a sorted set.",
                why="Fixing rows reduces the problem to 'best subarray ≤ k', which a sorted set solves in n log n.",
            ),
            Choice(
                "Every rectangle with 2-D prefix sums", SUBOPTIMAL, time="O(m²·n²)", space="O(m·n)", visual="dp-2d",
                detail="Try all corners and compute each sum in O(1).",
                why="Correct, but enumerates every column pair too.",
            ),
            Choice(
                "Kadane per row pair", INCORRECT, time="O(m²·n)", space="O(n)", visual="dp-1d",
                detail="Take the max subarray and accept it if ≤ k.",
                why="The best sum ≤ k may not be the overall max.",
            ),
            Choice(
                "Largest single cell ≤ k", INCORRECT, time="O(m·n)", space="O(1)", visual="matrix",
                detail="Look at 1×1 rectangles only.",
                why="Bigger rectangles can add up closer to k.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §1.3 sums of distances
    Question(
        slug="sum-of-absolute-differences-in-a-sorted-array", number=1685, title="Sum of Absolute Differences in a Sorted Array",
        difficulty="Medium", topics=("data-structures",),
        summary="For each i in a sorted array, return Σ |nums[i] − nums[j]| over all j.",
        example="[2,3,5]  →  [4,3,5]",
        criterion="Which approach is linear?",
        hint="Left of i, every term is nums[i] − nums[j]; right of i, nums[j] − nums[i].",
        choices=(
            Choice(
                "Prefix sums on both sides", OPTIMAL, time="O(n)", space="O(n)", visual="prefix",
                detail="ans[i] = nums[i]·i − s[i] + (s[n] − s[i + 1]) − nums[i]·(n − 1 − i).",
                why="Sorted order removes the absolute values, leaving a count times nums[i] minus a prefix sum on each side.",
            ),
            Choice(
                "Sum each i directly", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="Loop over all j for each i.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Total minus n · nums[i]", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="|Σ (nums[j] − nums[i])|.",
                why="Absolute value of a sum isn't a sum of absolute values.",
            ),
            Choice(
                "Only the neighbours", INCORRECT, time="O(n)", space="O(1)", visual="two-pointers",
                detail="Add the gaps to the adjacent elements.",
                why="Every j contributes, not just neighbours.",
            ),
        ),
    ),
    Question(
        slug="minimum-operations-to-make-array-modulo-alternating-i", number=3937, title="Minimum Operations to Make Array Modulo Alternating I",
        difficulty="Medium", topics=("data-structures",),
        summary="One operation adds or subtracts 1. Make all even-indexed values ≡ x and all odd-indexed values ≡ y (mod k), for some x ≠ y. Return the fewest operations. n, k ≤ 100.",
        example="[1,4,2,8], k = 3  →  2",
        criterion="Which approach is O(n·k)?",
        hint="Compute the cost for every target residue on each side. How do you combine them under x ≠ y?",
        choices=(
            Choice(
                "Cost per residue per side, best and second-best", OPTIMAL, time="O(n·k)", space="O(k)", visual="counting",
                detail="For each residue r, cost = Σ min distance to r over that side's elements; combine the two sides' best, falling back to a second-best when they pick the same residue.",
                why="Sides are independent except for x ≠ y, so the best pair uses each side's best, or one side's runner-up.",
            ),
            Choice(
                "Try every (x, y) pair", SUBOPTIMAL, time="O(n·k²)", space="O(1)", visual="brute",
                detail="Compute both costs for every pair of distinct residues.",
                why="Correct, but recomputes costs for each pair.",
            ),
            Choice(
                "Allow x = y", INCORRECT, time="O(n·k)", space="O(k)", visual="counting",
                detail="Take each side's best independently.",
                why="Example 2's [1,1,1] would cost 0. Is that allowed?",
            ),
            Choice(
                "Only move upward", INCORRECT, time="O(n·k)", space="O(k)", visual="counting",
                detail="Cost = (r − x mod k) going up only.",
                why="Moving down can be cheaper, as with 2 → 1 in example 1.",
            ),
        ),
    ),
    Question(
        slug="minimum-operations-to-make-subarray-elements-equal", number=3422, title="Minimum Operations to Make Subarray Elements Equal",
        difficulty="Medium", topics=("data-structures",),
        summary="One operation adds or subtracts 1. Return the fewest operations to make some subarray of length k all equal.",
        example="[4,-3,2,1,-4,6], k = 3  →  5",
        criterion="Which approach is O(n log k)?",
        hint="For a fixed window, the best common value is its median. How do you keep the median and the distance sums while sliding?",
        choices=(
            Choice(
                "Sliding median with two heaps and sums", OPTIMAL, time="O(n log k)", space="O(k)", visual="heap",
                detail="Maintain the lower and upper halves (with lazy deletion) and their sums; cost = median·|low| − sumLow + sumHigh − median·|high|.",
                why="Distances to the median split into two sums, which the heaps keep up to date as the window slides.",
            ),
            Choice(
                "Sort each window", SUBOPTIMAL, time="O(n·k log k)", space="O(k)", visual="sort",
                detail="Sort, take the median, sum the distances.",
                why="Correct, but redoes the sort each slide.",
            ),
            Choice(
                "Use the mean", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Move everything to the rounded average.",
                why="For [0,0,9] the mean 3 costs 12, the median 0 costs 9.",
            ),
            Choice(
                "Max minus min", INCORRECT, time="O(n)", space="O(k)", visual="sliding-window",
                detail="Cost = window max − window min.",
                why="Every element moves, not just the extremes.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §1.5 further practice
    Question(
        slug="design-exam-scores-tracker", number=3709, title="Design Exam Scores Tracker",
        difficulty="Medium", topics=("data-structures",),
        summary="record(time, score) arrives with strictly increasing times; totalScore(start, end) returns the total of scores recorded in [start, end].",
        example="record(1,98); totalScore(1,1) → 98; record(5,99); totalScore(1,5) → 197; totalScore(3,4) → 0",
        criterion="Which approach answers queries in O(log n)?",
        hint="Times arrive sorted. What can you append to make range totals cheap?",
        choices=(
            Choice(
                "Append times and prefix sums, binary search", OPTIMAL, time="O(1) record, O(log n) query", space="O(n)", visual="binary-search",
                detail="Find the first time ≥ start and the last time ≤ end; subtract their prefix sums.",
                why="Appends keep both lists sorted, so a time range maps to an index range by two searches.",
            ),
            Choice(
                "Scan all records per query", SUBOPTIMAL, time="O(n) query", space="O(n)", visual="brute",
                detail="Add scores whose times fall in range.",
                why="Correct, but linear per query.",
            ),
            Choice(
                "Array indexed by time", INCORRECT, time="O(1)", space="O(T)", visual="prefix",
                detail="Prefix sums over every possible time.",
                why="Times go up to 10⁹.",
            ),
            Choice(
                "Running total only", INCORRECT, time="O(1)", space="O(1)", visual="counting",
                detail="Return the total so far.",
                why="totalScore(3, 4) should be 0, not 98.",
            ),
        ),
    ),
    Question(
        slug="number-of-same-end-substrings", number=2955, title="Number of Same-End Substrings",
        difficulty="Medium", topics=("data-structures",),
        summary="For each query [l, r], count substrings of s[l..r] whose first and last characters are equal.",
        example="\"abcaab\", [[0,0],[1,4],[2,5],[0,5]]  →  [1,5,5,10]",
        criterion="Which approach is O(26·(n + q))?",
        hint="If a letter occurs m times in the range, how many same-end substrings does it produce?",
        choices=(
            Choice(
                "Prefix counts per letter", OPTIMAL, time="O(26·(n + q))", space="O(26·n)", visual="prefix",
                detail="Get each letter's count m in [l, r] from prefix counts and add m(m + 1)/2.",
                why="Any two occurrences (or one with itself) form one substring, and prefix counts give m in O(1).",
            ),
            Choice(
                "Count per query by scanning", SUBOPTIMAL, time="O(n·q)", space="O(26)", visual="brute",
                detail="Tally letters in [l, r] for each query.",
                why="Correct, but rescans per query.",
            ),
            Choice(
                "m(m − 1)/2", INCORRECT, time="O(26·(n + q))", space="O(26·n)", visual="prefix",
                detail="Count pairs of distinct occurrences.",
                why="Single characters are same-end substrings too.",
            ),
            Choice(
                "Length of the range", INCORRECT, time="O(1)", space="O(1)", visual="math",
                detail="Count single characters only.",
                why="\"aa\" and \"abca\" count as well.",
            ),
        ),
    ),
    Question(
        slug="maximize-the-beauty-of-the-garden", number=1788, title="Maximize the Beauty of the Garden",
        difficulty="Hard", topics=("data-structures",),
        summary="Remove any flowers so at least two remain and the first and last remaining have the same value. Return the largest possible sum of the remaining values (values may be negative).",
        example="[1,2,3,1,2]  →  8",
        criterion="Which approach is linear?",
        hint="Fix the value v of the ends. Which two occurrences, and which flowers in between, should you keep?",
        choices=(
            Choice(
                "Prefix sums of positives, first occurrence per value", OPTIMAL, time="O(n)", space="O(n)", visual="prefix",
                detail="For each j, if nums[j] appeared first at i, try 2·nums[j] + (positive sum strictly between i and j).",
                why="Keep the outermost pair of v and every positive flower between; prefix sums of max(x, 0) give that in O(1).",
            ),
            Choice(
                "Every pair of equal values", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="brute",
                detail="Try each equal pair with the positive sum between.",
                why="Correct, but the first occurrence is always the best left end.",
            ),
            Choice(
                "Sum of positives", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Keep every positive flower.",
                why="The ends must match.",
            ),
            Choice(
                "Plain prefix sums between", INCORRECT, time="O(n)", space="O(n)", visual="prefix",
                detail="Keep everything between the two ends.",
                why="Negative flowers in between can be removed.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §1.6 2-D prefix sums
    Question(
        slug="range-sum-query-2d-immutable", number=304, title="Range Sum Query 2D - Immutable",
        difficulty="Medium", topics=("data-structures",),
        summary="Answer many sumRegion(r1, c1, r2, c2) queries on a fixed matrix.",
        example="sumRegion(2,1,4,3) on the sample  →  8",
        criterion="Which approach answers each query in O(1)?",
        hint="If you knew the sum of every top-left rectangle, how would you get any rectangle?",
        choices=(
            Choice(
                "2-D prefix sums, inclusion–exclusion", OPTIMAL, time="O(m·n) build, O(1) query", space="O(m·n)", visual="dp-2d",
                detail="P[i + 1][j + 1] = P[i][j + 1] + P[i + 1][j] − P[i][j] + a[i][j]; a region is four lookups.",
                why="Any rectangle is the big top-left block minus two strips plus the doubly removed corner.",
            ),
            Choice(
                "Row prefix sums", SUBOPTIMAL, time="O(m) query", space="O(m·n)", visual="prefix",
                detail="Sum each row's range with its own prefix sums.",
                why="Correct, but costs one lookup per row.",
            ),
            Choice(
                "Forget to add the corner back", INCORRECT, time="O(1) query", space="O(m·n)", visual="dp-2d",
                detail="Subtract both strips without re-adding P[r1][c1].",
                why="The top-left corner gets subtracted twice.",
            ),
            Choice(
                "Sum each region directly", INCORRECT, time="O(m·n) query", space="O(1)", visual="brute",
                detail="Loop over the cells.",
                why="With 10⁴ queries on a 200×200 matrix, that's 4·10⁸ additions. Is that O(1)?",
            ),
        ),
    ),
    Question(
        slug="matrix-block-sum", number=1314, title="Matrix Block Sum",
        difficulty="Medium", topics=("data-structures",),
        summary="For each cell, return the sum of all cells within k rows and k columns of it (clipped to the matrix).",
        example="[[1,2,3],[4,5,6],[7,8,9]], k = 1  →  [[12,21,16],[27,45,33],[24,39,28]]",
        criterion="Which approach is O(m·n)?",
        hint="Each answer is a rectangle sum.",
        choices=(
            Choice(
                "2-D prefix sums with clamped bounds", OPTIMAL, time="O(m·n)", space="O(m·n)", visual="dp-2d",
                detail="Clamp the block to the matrix and read it with four prefix lookups.",
                why="Every block is a rectangle, so each cell is O(1) after one O(m·n) build.",
            ),
            Choice(
                "Sum each block directly", SUBOPTIMAL, time="O(m·n·k²)", space="O(1)", visual="brute",
                detail="Loop over the (2k + 1)² neighbourhood.",
                why="Correct, but neighbouring blocks overlap almost entirely.",
            ),
            Choice(
                "No clamping", INCORRECT, time="O(m·n)", space="O(m·n)", visual="dp-2d",
                detail="Use i − k and i + k directly as bounds.",
                why="At the corner, i − k is −1. What does that index read?",
            ),
            Choice(
                "Row sums only", INCORRECT, time="O(m·n)", space="O(m·n)", visual="prefix",
                detail="Sum the cell's row within k columns.",
                why="The block spans k rows above and below too.",
            ),
        ),
    ),
    Question(
        slug="count-submatrices-with-top-left-element-and-sum-less-than-k", number=3070, title="Count Submatrices with Top-Left Element and Sum Less Than k",
        difficulty="Medium", topics=("data-structures",),
        summary="Count submatrices that contain grid[0][0] and have sum ≤ k. Values are non-negative.",
        example="[[7,6,3],[6,6,1]], k = 18  →  4",
        criterion="Which approach is O(m·n)?",
        hint="A submatrix containing the top-left corner is fixed by its bottom-right cell.",
        choices=(
            Choice(
                "2-D prefix sums, count cells ≤ k", OPTIMAL, time="O(m·n)", space="O(n)", visual="dp-2d",
                detail="Build P on the fly (one row of storage is enough) and count P[i][j] ≤ k.",
                why="Each candidate is exactly one top-left prefix, so the count is the number of prefix values ≤ k.",
            ),
            Choice(
                "Sum each candidate directly", SUBOPTIMAL, time="O(m²·n²)", space="O(1)", visual="brute",
                detail="Add up each top-left rectangle.",
                why="Correct, but overlapping rectangles are re-added.",
            ),
            Choice(
                "Count cells ≤ k", INCORRECT, time="O(m·n)", space="O(1)", visual="counting",
                detail="Count individual values.",
                why="The submatrix sum includes all cells above and left.",
            ),
            Choice(
                "Every submatrix", INCORRECT, time="O(m²·n²)", space="O(m·n)", visual="dp-2d",
                detail="Count all submatrices with sum ≤ k.",
                why="They must contain grid[0][0].",
            ),
        ),
    ),
    Question(
        slug="find-kth-largest-xor-coordinate-value", number=1738, title="Find Kth Largest XOR Coordinate Value",
        difficulty="Medium", topics=("data-structures",),
        summary="The value of (a, b) is the XOR of matrix[i][j] over all i ≤ a, j ≤ b. Return the k-th largest value.",
        example="[[5,2],[1,6]], k = 1  →  7",
        criterion="Which approach is O(m·n) on average?",
        hint="Build every value with a 2-D prefix XOR. Then you need a selection, not a full sort.",
        choices=(
            Choice(
                "2-D prefix XOR, then quickselect", OPTIMAL, time="O(m·n) average", space="O(m·n)", visual="dp-2d",
                detail="P[i + 1][j + 1] = P[i][j + 1] ^ P[i + 1][j] ^ P[i][j] ^ a[i][j]; select the k-th largest.",
                why="XOR's inclusion–exclusion uses XOR for both add and subtract. Quickselect finds one order statistic in linear average time.",
            ),
            Choice(
                "2-D prefix XOR, then sort", SUBOPTIMAL, time="O(m·n log(m·n))", space="O(m·n)", visual="sort",
                detail="Sort all values and index k − 1 from the top.",
                why="Correct, but sorts everything for one value.",
            ),
            Choice(
                "Prefix sums instead of XOR", INCORRECT, time="O(m·n)", space="O(m·n)", visual="dp-2d",
                detail="Use + and − in the recurrence.",
                why="5 ⊕ 2 is 7, but 5 + 2 is 7 by luck; 5 ⊕ 1 is 4, not 6.",
            ),
            Choice(
                "k-th largest matrix entry", INCORRECT, time="O(m·n)", space="O(1)", visual="matrix",
                detail="Ignore the prefix and pick from the raw values.",
                why="Values are prefix XORs, not single cells.",
            ),
        ),
    ),
    Question(
        slug="count-submatrices-with-equal-frequency-of-x-and-y", number=3212, title="Count Submatrices With Equal Frequency of X and Y",
        difficulty="Medium", topics=("data-structures",),
        summary="Cells are 'X', 'Y' or '.'. Count submatrices that contain grid[0][0], have equally many X and Y, and at least one X.",
        example="[[\"X\",\"Y\",\".\"],[\"Y\",\".\",\".\"]]  →  3",
        criterion="Which approach is O(m·n)?",
        hint="Again each candidate is a top-left prefix. Which two prefix quantities decide it?",
        choices=(
            Choice(
                "2-D prefixes of X − Y and of X", OPTIMAL, time="O(m·n)", space="O(n)", visual="dp-2d",
                detail="Count cells where the X − Y prefix is 0 and the X prefix is positive.",
                why="Equal counts means the difference is 0, and 'at least one X' needs the X count. Both are prefix sums.",
            ),
            Choice(
                "Count each candidate directly", SUBOPTIMAL, time="O(m²·n²)", space="O(1)", visual="brute",
                detail="Tally X and Y in each top-left rectangle.",
                why="Correct, but re-scans overlapping rectangles.",
            ),
            Choice(
                "Skip the 'at least one X' check", INCORRECT, time="O(m·n)", space="O(n)", visual="dp-2d",
                detail="Count cells where X − Y = 0.",
                why="An all-dot prefix has zero of each. Does it count?",
            ),
            Choice(
                "Equal counts per cell", INCORRECT, time="O(m·n)", space="O(1)", visual="matrix",
                detail="Count cells that are neither X nor Y.",
                why="The condition is on the whole submatrix.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §3.1 stack basics
    Question(
        slug="build-an-array-with-stack-operations", number=1441, title="Build an Array With Stack Operations",
        difficulty="Medium", topics=("data-structures",),
        summary="Read numbers 1, 2, … in order. Using Push and Pop, make the stack equal target (strictly increasing). Return the operations.",
        example="target = [1,3], n = 3  →  [\"Push\",\"Push\",\"Pop\",\"Push\"]",
        criterion="Which approach is O(target's last value)?",
        hint="A number you don't want still has to be read. How do you get rid of it?",
        choices=(
            Choice(
                "Push each number, pop the unwanted ones", OPTIMAL, time="O(max)", space="O(1)", visual="stack",
                detail="For 1..target[-1], emit Push, plus Pop if it isn't the next target value; stop at the last target.",
                why="Every number must pass through the stack in order, and an unwanted one leaves immediately, so the stack always matches target's prefix.",
            ),
            Choice(
                "Check membership by scanning target", SUBOPTIMAL, time="O(max·len)", space="O(1)", visual="brute",
                detail="For each number, search target to decide whether to pop.",
                why="Correct, but target is sorted. A pointer is enough.",
            ),
            Choice(
                "Push only target values", INCORRECT, time="O(len)", space="O(1)", visual="stack",
                detail="Emit Push once per target value.",
                why="2 is read before 3. Where does it go?",
            ),
            Choice(
                "Continue to n", INCORRECT, time="O(n)", space="O(1)", visual="stack",
                detail="Keep reading until n, popping what's not in target.",
                why="Extra Push/Pop pairs after the last target value aren't needed.",
            ),
        ),
    ),
    Question(
        slug="backspace-string-compare", number=844, title="Backspace String Compare",
        difficulty="Easy", topics=("data-structures",),
        summary="'#' is a backspace. Return whether s and t are equal after typing them into empty editors.",
        example="\"ab#c\", \"ad#c\"  →  true",
        criterion="Which approach is linear with O(1) extra space?",
        hint="Read from the end. When you see '#', what does it tell you about the characters before it?",
        choices=(
            Choice(
                "Two pointers from the end, counting skips", OPTIMAL, time="O(n + m)", space="O(1)", visual="two-pointers",
                detail="Walk each string backward, skipping characters erased by pending '#'s; compare the next surviving characters.",
                why="A backspace only affects characters before it, so reading backward knows each character's fate immediately.",
            ),
            Choice(
                "Build both results with a stack", SUBOPTIMAL, time="O(n + m)", space="O(n + m)", visual="stack",
                detail="Push characters, pop on '#', then compare.",
                why="Correct and simple, but stores both strings.",
            ),
            Choice(
                "Remove '#' and the char right before, once", INCORRECT, time="O(n + m)", space="O(n + m)", visual="brute",
                detail="Delete each '#' with the character immediately before it in the original string.",
                why="In \"ab##\", the second '#' erases a, which isn't immediately before it in the original.",
            ),
            Choice(
                "Compare without '#'", INCORRECT, time="O(n + m)", space="O(1)", visual="two-pointers",
                detail="Strip all '#' and compare.",
                why="\"ab#c\" becomes \"abc\". Should b still be there?",
            ),
        ),
    ),
    Question(
        slug="baseball-game", number=682, title="Baseball Game",
        difficulty="Easy", topics=("data-structures",),
        summary="Process operations: an integer records a score, '+' records the sum of the last two, 'D' doubles the last, 'C' removes the last. Return the total.",
        example="[\"5\",\"2\",\"C\",\"D\",\"+\"]  →  30",
        criterion="Which approach is linear?",
        hint="Every operation looks at the most recent scores.",
        choices=(
            Choice(
                "Stack of scores", OPTIMAL, time="O(n)", space="O(n)", visual="stack",
                detail="Push, pop or peek per operation; sum the stack at the end.",
                why="'C' undoes the latest score and '+' reads the latest two, exactly a stack's operations.",
            ),
            Choice(
                "List with deletion by shifting", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="array-copy",
                detail="Keep scores in an array and shift elements to remove.",
                why="Correct, but removals from the end don't need shifting.",
            ),
            Choice(
                "Running total only", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Keep just the sum.",
                why="'C' needs to know the last score, and '+' the last two.",
            ),
            Choice(
                "'D' doubles the total", INCORRECT, time="O(n)", space="O(n)", visual="stack",
                detail="Double the running total instead of the last score.",
                why="'D' records 2 × the previous score, not 2 × everything.",
            ),
        ),
    ),
    Question(
        slug="removing-stars-from-a-string", number=2390, title="Removing Stars From a String",
        difficulty="Medium", topics=("data-structures",),
        summary="Each '*' removes itself and the closest non-star character to its left. Return the final string.",
        example="\"leet**cod*e\"  →  \"lecoe\"",
        criterion="Which approach is linear?",
        hint="Which character does a star remove: the oldest or the newest surviving one?",
        choices=(
            Choice(
                "Stack of characters", OPTIMAL, time="O(n)", space="O(n)", visual="stack",
                detail="Push letters; pop on '*'.",
                why="The closest surviving letter to the left is the top of the stack.",
            ),
            Choice(
                "Find and delete repeatedly", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="brute",
                detail="Locate a star, delete it and its left neighbour, repeat.",
                why="Correct, but each deletion shifts the string.",
            ),
            Choice(
                "Remove the star and the next char", INCORRECT, time="O(n)", space="O(n)", visual="brute",
                detail="Delete the character after each star.",
                why="The rule removes the character to the left.",
            ),
            Choice(
                "Drop all stars", INCORRECT, time="O(n)", space="O(n)", visual="brute",
                detail="Delete just the '*' characters.",
                why="Each star also removes a letter.",
            ),
        ),
    ),
    Question(
        slug="design-browser-history", number=1472, title="Design Browser History",
        difficulty="Medium", topics=("data-structures",),
        summary="Support visit(url) (which clears forward history), back(steps) and forward(steps), returning the current page.",
        example="visit a, visit b, back(1) → a, visit c, forward(1) → c",
        criterion="Which approach makes every operation O(1)?",
        hint="Keep all pages in one array. What two indices do you need?",
        choices=(
            Choice(
                "Array with current and last indices", OPTIMAL, time="O(1) per call", space="O(n)", visual="array-copy",
                detail="visit writes at cur + 1 and sets last = cur; back/forward clamp cur to [0, last].",
                why="Moving is just changing an index, and a visit discards forward pages by moving 'last', without deleting anything.",
            ),
            Choice(
                "Two stacks", SUBOPTIMAL, time="O(steps)", space="O(n)", visual="stack",
                detail="Move pages between back and forward stacks one at a time.",
                why="Correct, but back(100) moves 100 pages.",
            ),
            Choice(
                "Keep forward history after visit", INCORRECT, time="O(1)", space="O(n)", visual="array-copy",
                detail="Write the new page but don't reset the last index.",
                why="After visiting c, should forward go to the old b?",
            ),
            Choice(
                "Single stack of visited pages", INCORRECT, time="O(steps)", space="O(n)", visual="stack",
                detail="Pop on back.",
                why="Popped pages are lost, so forward has nothing to return to.",
            ),
        ),
    ),
    Question(
        slug="validate-stack-sequences", number=946, title="Validate Stack Sequences",
        difficulty="Medium", topics=("data-structures",),
        summary="pushed and popped are permutations of distinct values. Return whether this push/pop order is possible on one stack.",
        example="pushed = [1,2,3,4,5], popped = [4,5,3,2,1]  →  true",
        criterion="Which approach is linear?",
        hint="Simulate. When should you pop?",
        choices=(
            Choice(
                "Simulate, popping greedily", OPTIMAL, time="O(n)", space="O(n)", visual="stack",
                detail="Push each value; while the top equals popped[j], pop and advance j; succeed if the stack ends empty.",
                why="Values are distinct, so if the top is the next to pop, popping now is the only way it can ever be popped in order.",
            ),
            Choice(
                "Search pushed for each popped value", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="brute",
                detail="Locate each value's push position and check stack order by scanning.",
                why="Correct with care, but quadratic.",
            ),
            Choice(
                "popped is pushed reversed", INCORRECT, time="O(n)", space="O(1)", visual="two-pointers",
                detail="Valid only if every value is popped after all pushes.",
                why="The example pops 4 before pushing 5.",
            ),
            Choice(
                "Same set of values", INCORRECT, time="O(n)", space="O(n)", visual="set",
                detail="Valid if both contain the same values.",
                why="[1,2,3] pushed and [3,1,2] popped: can 1 come out before 2?",
            ),
        ),
    ),
    Question(
        slug="find-mirror-score-of-a-string", number=3412, title="Find Mirror Score of a String",
        difficulty="Medium", topics=("data-structures",),
        summary="Letters mirror across the alphabet (a ↔ z, b ↔ y). For each i left to right, pair it with the closest unmarked j < i holding its mirror, mark both, and add i − j. Return the score.",
        example="\"aczzx\"  →  5",
        criterion="Which approach is linear?",
        hint="'Closest unmarked index of a letter' is the most recent one. One structure per letter.",
        choices=(
            Choice(
                "26 stacks of unmarked indices", OPTIMAL, time="O(n)", space="O(n)", visual="stack",
                detail="If the mirror letter's stack is non-empty, pop j and add i − j; else push i onto its own letter's stack.",
                why="The closest unmarked earlier index of a letter is its most recent push, which a stack gives in O(1).",
            ),
            Choice(
                "Scan left for each i", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="brute",
                detail="Walk back from i to the first unmarked mirror.",
                why="Correct, but rescans long stretches.",
            ),
            Choice(
                "Queues instead of stacks", INCORRECT, time="O(n)", space="O(n)", visual="queue",
                detail="Pair with the oldest unmarked mirror.",
                why="The rule asks for the closest one, which is the newest.",
            ),
            Choice(
                "Pair every mirror occurrence", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Don't mark indices.",
                why="Marked indices can't be used again.",
            ),
        ),
    ),
    Question(
        slug="simplify-path", number=71, title="Simplify Path",
        difficulty="Medium", topics=("data-structures",),
        summary="Simplify an absolute Unix path: '.' is the current directory, '..' goes up, repeated slashes are one, and other names (including '...') are directories.",
        example="\"/home//foo/\"  →  \"/home/foo\"",
        criterion="Which approach is linear?",
        hint="What does '..' undo?",
        choices=(
            Choice(
                "Split on '/', stack of names", OPTIMAL, time="O(n)", space="O(n)", visual="stack",
                detail="Skip empty parts and '.', pop on '..' (if possible), push anything else; join with '/'.",
                why="'..' cancels the most recent directory, which is the stack's top.",
            ),
            Choice(
                "Rewrite the string until stable", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="brute",
                detail="Repeatedly replace '//', '/./' and 'dir/../' patterns.",
                why="Correct with care, but each pass rescans the string.",
            ),
            Choice(
                "Treat '...' as going up", INCORRECT, time="O(n)", space="O(n)", visual="stack",
                detail="Pop on any name made of dots.",
                why="'...' is a valid directory name.",
            ),
            Choice(
                "Pop on '..' even at root", INCORRECT, time="O(n)", space="O(n)", visual="stack",
                detail="Always pop on '..'.",
                why="'/..' should stay at '/'. What happens with an empty stack?",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §3.2 stack design
    Question(
        slug="min-stack", number=155, title="Min Stack",
        difficulty="Medium", topics=("data-structures",),
        summary="Design a stack with push, pop, top and getMin, all in O(1).",
        example="push -2, push 0, push -3, getMin → -3, pop, getMin → -2",
        criterion="Which approach makes getMin O(1)?",
        hint="When the top is popped, what was the minimum before it was pushed?",
        choices=(
            Choice(
                "Store the min alongside each element", OPTIMAL, time="O(1)", space="O(n)", visual="stack",
                detail="Push (x, min(x, current min)); getMin reads the top's second value.",
                why="Each entry remembers the minimum of everything at or below it, so popping restores the previous minimum automatically.",
            ),
            Choice(
                "Scan for the min", SUBOPTIMAL, time="O(n) getMin", space="O(n)", visual="brute",
                detail="Search the stack on each getMin.",
                why="Correct, but getMin is linear.",
            ),
            Choice(
                "One min variable", INCORRECT, time="O(1)", space="O(n)", visual="stack",
                detail="Update a single min on push.",
                why="After popping −3, what's the min, and how would you know?",
            ),
            Choice(
                "Min-heap of values", INCORRECT, time="O(log n)", space="O(n)", visual="heap",
                detail="Push values into a heap too and peek for getMin.",
                why="Popping the stack doesn't remove that value from the heap.",
            ),
        ),
    ),
    Question(
        slug="design-a-stack-with-increment-operation", number=1381, title="Design a Stack With Increment Operation",
        difficulty="Medium", topics=("data-structures",),
        summary="A bounded stack supports push, pop and increment(k, val), which adds val to the bottom k elements.",
        example="push 1, push 2, increment(5, 100), pop → 102",
        criterion="Which approach makes every operation O(1)?",
        hint="Record the increment lazily at one position. When does it need to move?",
        choices=(
            Choice(
                "Lazy increments passed down on pop", OPTIMAL, time="O(1)", space="O(n)", visual="stack",
                detail="inc[min(k, size) − 1] += val; on pop, return x + inc[top] and add inc[top] to inc[top − 1].",
                why="An increment at position i applies to everything at or below i. Passing it down on pop keeps that true without touching all k elements.",
            ),
            Choice(
                "Add to each of the bottom k", SUBOPTIMAL, time="O(k) increment", space="O(n)", visual="brute",
                detail="Loop over the elements directly.",
                why="Correct, but increment is linear.",
            ),
            Choice(
                "Global offset", INCORRECT, time="O(1)", space="O(1)", visual="counting",
                detail="Add val to one counter applied to every pop.",
                why="Only the bottom k get it, and later pushes shouldn't.",
            ),
            Choice(
                "Lazy value, not passed down", INCORRECT, time="O(1)", space="O(n)", visual="stack",
                detail="Store inc at position k − 1 and add it only when that element pops.",
                why="Elements below k − 1 also need the increment.",
            ),
        ),
    ),
    Question(
        slug="exclusive-time-of-functions", number=636, title="Exclusive Time of Functions",
        difficulty="Medium", topics=("data-structures",),
        summary="On one thread, logs \"id:start:t\" and \"id:end:t\" (inclusive end) describe nested calls. Return each function's exclusive time.",
        example="n = 2, [\"0:start:0\",\"1:start:2\",\"1:end:5\",\"0:end:6\"]  →  [3, 4]",
        criterion="Which approach is linear?",
        hint="Time between two consecutive log entries belongs to whichever function is running. Which one is that?",
        choices=(
            Choice(
                "Stack of running ids and the previous timestamp", OPTIMAL, time="O(n)", space="O(n)", visual="stack",
                detail="On start, credit t − prev to the top, push; on end, credit t − prev + 1 to the top, pop, set prev = t + 1.",
                why="The running function is always the stack's top, so each gap goes to exactly one function.",
            ),
            Choice(
                "Subtract children afterwards", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="brute",
                detail="Compute each call's total span, then subtract the spans of calls nested in it.",
                why="Correct, but finding nested calls rescans the logs.",
            ),
            Choice(
                "end − start per call", INCORRECT, time="O(n)", space="O(n)", visual="stack",
                detail="Credit each function its full span.",
                why="Function 0's span includes function 1's time.",
            ),
            Choice(
                "Exclusive end", INCORRECT, time="O(n)", space="O(n)", visual="stack",
                detail="Credit t − prev on end, without the +1.",
                why="End times are inclusive: 1 runs from 2 through 5, which is 4 units.",
            ),
        ),
    ),
    Question(
        slug="max-stack", number=716, title="Max Stack",
        difficulty="Hard", topics=("data-structures",),
        summary="Design a stack with push, pop, top, peekMax and popMax (removes the topmost maximum).",
        example="push 5, push 1, push 5, top → 5, popMax → 5, top → 1",
        criterion="Which approach makes popMax O(log n)?",
        hint="popMax removes from the middle. What lets you delete from the middle quickly, and find the max quickly?",
        choices=(
            Choice(
                "Doubly linked list plus a sorted map", OPTIMAL, time="O(log n)", space="O(n)", visual="linked-list",
                detail="The list holds stack order; a sorted map value → list of nodes finds the max; unlink nodes in O(1).",
                why="The map gives the max in log time, and the linked list removes any node without shifting.",
            ),
            Choice(
                "Two stacks, buffer on popMax", SUBOPTIMAL, time="O(n) popMax", space="O(n)", visual="stack",
                detail="Keep a max-so-far stack; popMax pops into a buffer until the max, then pushes back.",
                why="Correct, but popMax may move the whole stack.",
            ),
            Choice(
                "Heap only", INCORRECT, time="O(log n)", space="O(n)", visual="heap",
                detail="Keep values in a max-heap.",
                why="pop needs the most recent value, which a heap can't give.",
            ),
            Choice(
                "Max-so-far stack without rebuilding", INCORRECT, time="O(1)", space="O(n)", visual="stack",
                detail="popMax pops the max stack only.",
                why="The value stays in the main stack.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §3.3 adjacent cancellation
    Question(
        slug="minimum-string-length-after-removing-substrings", number=2696, title="Minimum String Length After Removing Substrings",
        difficulty="Easy", topics=("data-structures",),
        summary="Repeatedly remove any \"AB\" or \"CD\". Return the shortest possible final length.",
        example="\"ABFCACDB\"  →  2",
        criterion="Which approach is linear?",
        hint="After removing a pair, its neighbours touch. Which character does a new character pair with?",
        choices=(
            Choice(
                "Stack, cancel with the top", OPTIMAL, time="O(n)", space="O(n)", visual="stack",
                detail="If the top and the new character form AB or CD, pop; else push.",
                why="Removals expose the character below, which is the stack's new top, so cascades are handled for free.",
            ),
            Choice(
                "Replace until nothing changes", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="brute",
                detail="Repeatedly delete occurrences of AB and CD.",
                why="Correct, but each pass rebuilds the string.",
            ),
            Choice(
                "One replacement pass", INCORRECT, time="O(n)", space="O(n)", visual="brute",
                detail="Delete AB and CD once.",
                why="In \"ACDB\", removing CD creates AB.",
            ),
            Choice(
                "Count A, B, C, D", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="n − 2·min(A, B) − 2·min(C, D).",
                why="\"BA\" has one A and one B but can't be removed.",
            ),
        ),
    ),
    Question(
        slug="remove-all-adjacent-duplicates-in-string", number=1047, title="Remove All Adjacent Duplicates In String",
        difficulty="Easy", topics=("data-structures",),
        summary="Repeatedly remove two adjacent equal letters. Return the final string.",
        example="\"abbaca\"  →  \"ca\"",
        criterion="Which approach is linear?",
        hint="After \"bb\" disappears, which letters become neighbours?",
        choices=(
            Choice(
                "Stack, pop on equal top", OPTIMAL, time="O(n)", space="O(n)", visual="stack",
                detail="If the new letter equals the top, pop; else push.",
                why="The stack holds the current reduced prefix, so cascading removals happen naturally.",
            ),
            Choice(
                "Rescan until stable", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="brute",
                detail="Remove one pair at a time and rescan.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "One pass, no cascading", INCORRECT, time="O(n)", space="O(n)", visual="brute",
                detail="Remove pairs found in the original string.",
                why="\"abba\" loses bb, then aa meet. Are they removed?",
            ),
            Choice(
                "Remove letters with even counts", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Keep letters that appear an odd number of times.",
                why="\"abab\" has no adjacent pairs at all.",
            ),
        ),
    ),
    Question(
        slug="make-the-string-great", number=1544, title="Make The String Great",
        difficulty="Easy", topics=("data-structures",),
        summary="Repeatedly remove two adjacent characters that are the same letter in different cases. Return the result.",
        example="\"leEeetcode\"  →  \"leetcode\"",
        criterion="Which approach is linear?",
        hint="Same pattern as removing adjacent duplicates. What's the match test?",
        choices=(
            Choice(
                "Stack, pop on case-flipped match", OPTIMAL, time="O(n)", space="O(n)", visual="stack",
                detail="Pop when top and current differ only in case (e.g. |a − b| = 32 in ASCII).",
                why="Each removal exposes the previous character, which the stack keeps on top.",
            ),
            Choice(
                "Rescan until stable", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="brute",
                detail="Remove one bad pair per scan.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Remove equal letters ignoring case", INCORRECT, time="O(n)", space="O(n)", visual="stack",
                detail="Pop when the lowercase forms match.",
                why="\"ee\" is the same case. Is it bad?",
            ),
            Choice(
                "Lowercase everything", INCORRECT, time="O(n)", space="O(n)", visual="brute",
                detail="Return s.lower().",
                why="That changes letters instead of removing pairs.",
            ),
        ),
    ),
    Question(
        slug="resulting-string-after-adjacent-removals", number=3561, title="Resulting String After Adjacent Removals",
        difficulty="Medium", topics=("data-structures",),
        summary="Repeatedly remove the leftmost adjacent pair of letters that are consecutive in the circular alphabet (a–b, b–a, z–a, …). Return the result.",
        example="\"adcb\"  →  \"\"",
        criterion="Which approach is linear?",
        hint="Does removing pairs left to right with a stack produce the same result as the leftmost-first rule?",
        choices=(
            Choice(
                "Stack, pop on consecutive letters", OPTIMAL, time="O(n)", space="O(n)", visual="stack",
                detail="Pop when (top − c) mod 26 is 1 or 25; else push.",
                why="The stack is always fully reduced, so the first removable pair involves the new letter and the top, matching the leftmost rule.",
            ),
            Choice(
                "Simulate the leftmost removal", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="brute",
                detail="Scan for the leftmost pair, remove it, repeat.",
                why="Correct, but rescans after each removal.",
            ),
            Choice(
                "Ignore the wrap", INCORRECT, time="O(n)", space="O(n)", visual="stack",
                detail="Only |top − c| = 1.",
                why="\"zadb\" should lose \"za\".",
            ),
            Choice(
                "Only a → b order", INCORRECT, time="O(n)", space="O(n)", visual="stack",
                detail="Pop only when c = top + 1.",
                why="\"dc\" is removable too.",
            ),
        ),
    ),
    Question(
        slug="check-if-word-is-valid-after-substitutions", number=1003, title="Check If Word Is Valid After Substitutions",
        difficulty="Medium", topics=("data-structures",),
        summary="Starting from \"\", you may insert \"abc\" anywhere, repeatedly. Return whether s can be built this way.",
        example="\"aabcbc\"  →  true",
        criterion="Which approach is linear?",
        hint="Reverse the process: remove \"abc\" wherever it appears. Where can the last-inserted \"abc\" be found?",
        choices=(
            Choice(
                "Stack, pop when the top reads abc", OPTIMAL, time="O(n)", space="O(n)", visual="stack",
                detail="Push letters; when the top three are a, b, c, pop them; valid if the stack ends empty.",
                why="Removing an \"abc\" can only expose another one ending at the next letter, which is what the stack checks.",
            ),
            Choice(
                "Remove \"abc\" until none remain", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="brute",
                detail="Repeatedly delete occurrences of \"abc\".",
                why="Correct, but each pass copies the string.",
            ),
            Choice(
                "Equal counts of a, b, c", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Valid if the three counts match.",
                why="\"abccba\" has equal counts but isn't valid.",
            ),
            Choice(
                "Prefix counts a ≥ b ≥ c", INCORRECT, time="O(n)", space="O(1)", visual="prefix",
                detail="Check the order of counts in every prefix.",
                why="\"abacbc\" passes that test. Can it be built?",
            ),
        ),
    ),
    Question(
        slug="merge-adjacent-equal-elements", number=3834, title="Merge Adjacent Equal Elements",
        difficulty="Medium", topics=("data-structures",),
        summary="Repeatedly replace the leftmost pair of adjacent equal elements with their sum. Return the final array.",
        example="[2,2,4]  →  [8]",
        criterion="Which approach is linear (amortized)?",
        hint="After a merge, the new value may equal its left neighbour.",
        choices=(
            Choice(
                "Stack with cascading merges", OPTIMAL, time="O(n)", space="O(n)", visual="stack",
                detail="Push x; while the top two are equal, pop both and push their sum.",
                why="The stack is always merged as far as possible, so the leftmost pair always involves the newest value. Each merge removes an element, so the work is linear.",
            ),
            Choice(
                "Simulate from the start each time", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="brute",
                detail="Scan for the leftmost equal pair, merge, repeat.",
                why="Correct, but rescans after each merge.",
            ),
            Choice(
                "One pass, no cascade", INCORRECT, time="O(n)", space="O(n)", visual="brute",
                detail="Merge equal neighbours once.",
                why="[2,2,4] becomes [4,4]. Should those merge?",
            ),
            Choice(
                "Group equal runs", INCORRECT, time="O(n)", space="O(n)", visual="counting",
                detail="Replace each run of equal values with its sum.",
                why="[2,2,2] merges the first two into 4, leaving [4,2], not [6].",
            ),
        ),
    ),
    Question(
        slug="merge-close-characters", number=3853, title="Merge Close Characters",
        difficulty="Medium", topics=("data-structures",),
        summary="Two equal characters are close if their indices differ by at most k; the right one merges into (disappears into) the left. Merge pairs (smallest left index first) until none remain. Return the string.",
        example="\"yybyzybz\", k = 2  →  \"ybzybz\"",
        criterion="Which approach is linear?",
        hint="Build the result left to right. When a character arrives, which earlier character could absorb it?",
        choices=(
            Choice(
                "Output with last position per character", OPTIMAL, time="O(n)", space="O(n)", visual="hashmap",
                detail="Skip c if its last position in the output is within k of the next output index; else append it and record the position.",
                why="Indices are measured in the current string, which is the output built so far. The latest copy of c is the closest one that could absorb it.",
            ),
            Choice(
                "Simulate merges on the whole string", SUBOPTIMAL, time="O(n³)", space="O(n)", visual="brute",
                detail="Find the smallest-left close pair, delete the right one, repeat.",
                why="Correct, but rescans the string after every merge.",
            ),
            Choice(
                "Use original indices", INCORRECT, time="O(n)", space="O(n)", visual="hashmap",
                detail="Measure distances in the input string.",
                why="After the first y merges, the third y is 2 away in the new string but 3 in the original.",
            ),
            Choice(
                "Remove all later copies", INCORRECT, time="O(n)", space="O(1)", visual="set",
                detail="Keep only the first occurrence of each character.",
                why="Far-apart copies stay.",
            ),
        ),
    ),
    Question(
        slug="minimum-deletions-to-make-array-beautiful", number=2216, title="Minimum Deletions to Make Array Beautiful",
        difficulty="Medium", topics=("data-structures",),
        summary="An array is beautiful if its length is even and nums[i] ≠ nums[i + 1] for every even i. Return the fewest deletions.",
        example="[1,1,2,3,5]  →  1",
        criterion="Which approach is linear with O(1) extra space?",
        hint="Build the result pair by pair. When does the current element have to go?",
        choices=(
            Choice(
                "Greedy pairing", OPTIMAL, time="O(n)", space="O(1)", visual="greedy",
                detail="Track the kept length; delete nums[i] when it would start a pair equal to the next element; delete one more if the kept length ends odd.",
                why="Deleting the first element of a bad pair is never worse than deleting later, since it keeps the following elements' positions flexible.",
            ),
            Choice(
                "Simulate deletions on the array", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="array-copy",
                detail="Delete elements in place and shift.",
                why="Correct, but each deletion shifts the rest.",
            ),
            Choice(
                "Count equal adjacent pairs", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Count i with nums[i] = nums[i + 1] in the original.",
                why="Deletions shift positions, so which pairs matter changes.",
            ),
            Choice(
                "Skip the final odd check", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Fix pairs but ignore the length.",
                why="The length must be even.",
            ),
        ),
    ),
    Question(
        slug="remove-all-adjacent-duplicates-in-string-ii", number=1209, title="Remove All Adjacent Duplicates in String II",
        difficulty="Medium", topics=("data-structures",),
        summary="Repeatedly remove k adjacent equal letters. Return the final string.",
        example="\"deeedbbcccbdaa\", k = 3  →  \"aa\"",
        criterion="Which approach is linear?",
        hint="Keep runs, not single letters, on the stack.",
        choices=(
            Choice(
                "Stack of (letter, run length)", OPTIMAL, time="O(n)", space="O(n)", visual="stack",
                detail="Extend the top run or push a new one; pop it when it reaches k.",
                why="Runs let you see k equal letters in O(1), and a pop exposes the run before it for cascades.",
            ),
            Choice(
                "Rescan until stable", SUBOPTIMAL, time="O(n²/k)", space="O(n)", visual="brute",
                detail="Remove one block per scan.",
                why="Correct, but rescans after each removal.",
            ),
            Choice(
                "New run after every pop", INCORRECT, time="O(n)", space="O(n)", visual="stack",
                detail="After popping a run, always start a fresh run for the next letter.",
                why="After eee goes, the two d's touch. If the second d starts its own run, can ddd ever reach k?",
            ),
            Choice(
                "Remove runs of length ≥ k once", INCORRECT, time="O(n)", space="O(n)", visual="brute",
                detail="Delete long runs in one pass.",
                why="Removals create new runs, like \"bbcccb\" → \"bbb\".",
            ),
        ),
    ),
    Question(
        slug="asteroid-collision", number=735, title="Asteroid Collision",
        difficulty="Medium", topics=("data-structures",),
        summary="Positive asteroids move right, negative move left, at the same speed. On collision the smaller explodes (both if equal). Return the survivors.",
        example="[5,10,-5]  →  [5,10]",
        criterion="Which approach is linear?",
        hint="A left-mover can only hit right-movers to its left. Which one does it meet first?",
        choices=(
            Choice(
                "Stack of survivors", OPTIMAL, time="O(n)", space="O(n)", visual="stack",
                detail="For a negative asteroid, pop smaller positive tops; stop at a larger one, cancel an equal one, or push if none remain.",
                why="The nearest right-mover is the top of the stack. Each asteroid is pushed and popped at most once.",
            ),
            Choice(
                "Simulate pairwise until stable", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="brute",
                detail="Resolve one adjacent collision per pass.",
                why="Correct, but repeated passes are quadratic.",
            ),
            Choice(
                "Collide any opposite signs", INCORRECT, time="O(n)", space="O(n)", visual="stack",
                detail="Treat [−2, 2] as a collision too.",
                why="Those move apart.",
            ),
            Choice(
                "Keep the largest per direction", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Return the biggest right-mover and biggest left-mover.",
                why="Many asteroids can survive.",
            ),
        ),
    ),
    Question(
        slug="car-fleet", number=853, title="Car Fleet",
        difficulty="Medium", topics=("data-structures",),
        summary="Cars drive toward target and can't pass; a car that catches up joins the car ahead as one fleet. Return how many fleets arrive.",
        example="target = 12, position = [10,8,0,5,3], speed = [2,4,1,1,3]  →  3",
        criterion="Which approach is O(n log n)?",
        hint="Process cars from closest to the target. When does a car join the fleet ahead?",
        choices=(
            Choice(
                "Sort by position, compare arrival times", OPTIMAL, time="O(n log n)", space="O(n)", visual="sort",
                detail="From nearest to farthest, compute (target − pos)/speed; a new fleet starts when the time exceeds the current fleet's time.",
                why="A car arriving no later than the fleet ahead would catch it and be held back, so only strictly slower arrivals start new fleets.",
            ),
            Choice(
                "Simulate in small time steps", SUBOPTIMAL, time="O(n·T)", space="O(n)", visual="brute",
                detail="Move cars step by step and merge on contact.",
                why="Correct with fine enough steps, but slow and fiddly.",
            ),
            Choice(
                "Count distinct speeds", INCORRECT, time="O(n)", space="O(n)", visual="set",
                detail="Each speed is one fleet.",
                why="Two equally fast cars far apart arrive separately.",
            ),
            Choice(
                "Process from the back", INCORRECT, time="O(n log n)", space="O(n)", visual="sort",
                detail="Start from the farthest car.",
                why="A car's fate depends on the car ahead, so start at the front.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §3.4 valid parentheses
    Question(
        slug="valid-parentheses", number=20, title="Valid Parentheses",
        difficulty="Easy", topics=("data-structures",),
        summary="Return whether a string of ()[]{} brackets is properly matched and nested.",
        example="\"([]{})\"  →  true",
        criterion="Which approach is linear?",
        hint="A closing bracket must match which opening bracket?",
        choices=(
            Choice(
                "Stack of open brackets", OPTIMAL, time="O(n)", space="O(n)", visual="stack",
                detail="Push openers; on a closer, the top must be its partner; end empty.",
                why="The most recent unclosed opener is the one a closer must match, which is the top.",
            ),
            Choice(
                "Remove matched pairs until stable", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="brute",
                detail="Repeatedly delete \"()\", \"[]\", \"{}\".",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Balance counter per type", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Track three counters that never go negative.",
                why="\"([)]\" keeps all counters fine but crosses.",
            ),
            Choice(
                "Total balance only", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="One counter for all bracket types.",
                why="\"(]\" balances to 0.",
            ),
        ),
    ),
    Question(
        slug="minimum-add-to-make-parentheses-valid", number=921, title="Minimum Add to Make Parentheses Valid",
        difficulty="Medium", topics=("data-structures",),
        summary="Return the fewest parentheses to insert to make s valid.",
        example="\"())\"  →  1",
        criterion="Which approach is linear with O(1) extra space?",
        hint="Track open parentheses. What happens when a ')' arrives with none open?",
        choices=(
            Choice(
                "Balance plus unmatched-close counter", OPTIMAL, time="O(n)", space="O(1)", visual="counting",
                detail="On ')', use an open one if any, else count a needed '('; answer = needed + leftover opens.",
                why="An unmatched ')' needs a '(' before it, and each leftover '(' needs a ')'. Two counters capture both.",
            ),
            Choice(
                "Stack of unmatched characters", SUBOPTIMAL, time="O(n)", space="O(n)", visual="stack",
                detail="Push and cancel matches; the stack's size is the answer.",
                why="Correct, but the stack only ever holds ')'s then '('s, so counts suffice.",
            ),
            Choice(
                "|opens − closes|", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Fix the total imbalance.",
                why="\"))((\" balances to 0 but needs 4.",
            ),
            Choice(
                "Count ')' with no '(' before", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Only fix unmatched closers.",
                why="\"(((\" needs 3 closers.",
            ),
        ),
    ),
    Question(
        slug="remove-outermost-parentheses", number=1021, title="Remove Outermost Parentheses",
        difficulty="Easy", topics=("data-structures",),
        summary="s is valid. Split it into primitive parts and remove the outermost pair of each.",
        example="\"(()())(())\"  →  \"()()()\"",
        criterion="Which approach is linear with O(1) extra space besides the output?",
        hint="A character is outermost exactly when what is true of the depth?",
        choices=(
            Choice(
                "Depth counter", OPTIMAL, time="O(n)", space="O(1)", visual="counting",
                detail="Emit '(' if depth > 0 before incrementing; emit ')' if depth > 0 after decrementing.",
                why="Outermost parentheses are exactly those at depth 0, so a counter decides each character.",
            ),
            Choice(
                "Split into parts, then strip", SUBOPTIMAL, time="O(n)", space="O(n)", visual="array-copy",
                detail="Collect each primitive part, then drop its ends.",
                why="Correct, but builds the parts first.",
            ),
            Choice(
                "Drop the first and last characters", INCORRECT, time="O(n)", space="O(1)", visual="brute",
                detail="Strip s once.",
                why="Each primitive part has its own outer pair.",
            ),
            Choice(
                "Drop every '(' followed by '('", INCORRECT, time="O(n)", space="O(1)", visual="brute",
                detail="Use a local pattern.",
                why="Depth isn't visible from neighbours alone.",
            ),
        ),
    ),
    Question(
        slug="maximum-nesting-depth-of-the-parentheses", number=1614, title="Maximum Nesting Depth of the Parentheses",
        difficulty="Easy", topics=("data-structures",),
        summary="Return the maximum nesting depth of parentheses in a valid expression.",
        example="\"(1+(2*3)+((8)/4))+1\"  →  3",
        criterion="Which approach is linear with O(1) extra space?",
        hint="You don't need to know which parenthesis is open, only how many.",
        choices=(
            Choice(
                "Depth counter with a running max", OPTIMAL, time="O(n)", space="O(1)", visual="counting",
                detail="+1 on '(', −1 on ')', track the max.",
                why="The depth at any point is the number of unclosed '(', which a counter tracks.",
            ),
            Choice(
                "Stack of '('", SUBOPTIMAL, time="O(n)", space="O(n)", visual="stack",
                detail="Push and pop, tracking the stack's size.",
                why="Correct, but the contents are never used.",
            ),
            Choice(
                "Count '('", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Return the number of '('.",
                why="\"()()\" has two but depth 1.",
            ),
            Choice(
                "Longest run of '('", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Count consecutive '('.",
                why="\"(a(b))\" nests twice without adjacent '('.",
            ),
        ),
    ),
    Question(
        slug="score-of-parentheses", number=856, title="Score of Parentheses",
        difficulty="Medium", topics=("data-structures",),
        summary="\"()\" scores 1, AB scores A + B, and (A) scores 2·A. Return the score of a balanced string.",
        example="\"(()(()))\"  →  6",
        criterion="Which approach is linear with O(1) extra space?",
        hint="Each innermost \"()\" is doubled once per enclosing pair.",
        choices=(
            Choice(
                "Add 2^depth at each \"()\"", OPTIMAL, time="O(n)", space="O(1)", visual="counting",
                detail="Track depth; when ')' immediately follows '(', add 1 << (depth after closing).",
                why="Distributing the doubling, the total is a sum over innermost pairs of 2 to their depth.",
            ),
            Choice(
                "Stack of partial scores", SUBOPTIMAL, time="O(n)", space="O(n)", visual="stack",
                detail="Push 0 on '('; on ')', pop v and add max(2v, 1) to the new top.",
                why="Correct and direct, but needs O(n) space.",
            ),
            Choice(
                "Count pairs", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Each pair scores 1.",
                why="((())) scores 4 but has 3 pairs.",
            ),
            Choice(
                "2^(max depth)", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="Use only the deepest level.",
                why="\"()()\" scores 2.",
            ),
        ),
    ),
    Question(
        slug="minimum-remove-to-make-valid-parentheses", number=1249, title="Minimum Remove to Make Valid Parentheses",
        difficulty="Medium", topics=("data-structures",),
        summary="s has letters and parentheses. Remove the fewest parentheses to make it valid; return any valid result.",
        example="\"lee(t(c)o)de)\"  →  \"lee(t(c)o)de\"",
        criterion="Which approach is linear?",
        hint="Which ')' can't be matched, and which '(' are left over at the end?",
        choices=(
            Choice(
                "Stack of '(' indices, mark the unmatched", OPTIMAL, time="O(n)", space="O(n)", visual="stack",
                detail="Mark ')' when the stack is empty; after the scan, mark the indices left in the stack; drop marked characters.",
                why="Every unmatched parenthesis must go, and removing exactly those is enough.",
            ),
            Choice(
                "Try removals by BFS", SUBOPTIMAL, time="O(n·2ⁿ)", space="O(2ⁿ)", visual="queue",
                detail="Remove one character per level until valid.",
                why="Correct, but exponential, and this problem needs only one answer.",
            ),
            Choice(
                "Remove unmatched ')' only", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Skip ')' when nothing is open.",
                why="\"a((b\" keeps two unmatched '('.",
            ),
            Choice(
                "Remove all parentheses", INCORRECT, time="O(n)", space="O(n)", visual="brute",
                detail="Valid, but…",
                why="It isn't the fewest removals.",
            ),
        ),
    ),
    Question(
        slug="minimum-number-of-swaps-to-make-the-string-balanced", number=1963, title="Minimum Number of Swaps to Make the String Balanced",
        difficulty="Medium", topics=("data-structures",),
        summary="s has equally many '[' and ']'. Return the fewest swaps of any two characters to make it balanced.",
        example="\"]]][[[\"  →  2",
        criterion="Which approach is linear with O(1) extra space?",
        hint="After cancelling matched pairs, the rest looks like \"]]]…[[[\". How many does one swap fix?",
        choices=(
            Choice(
                "⌈unmatched ']' / 2⌉", OPTIMAL, time="O(n)", space="O(1)", visual="counting",
                detail="Count ']' that arrive with no '[' open; return (count + 1) / 2.",
                why="Swapping the first unmatched ']' with the last unmatched '[' fixes two unmatched pairs at once.",
            ),
            Choice(
                "Stack to find unmatched ones", SUBOPTIMAL, time="O(n)", space="O(n)", visual="stack",
                detail="Cancel pairs with a stack, then count.",
                why="Correct, but a counter does the same job.",
            ),
            Choice(
                "Number of unmatched ']'", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="One swap per unmatched closer.",
                why="\"]]][[[\" has 3 but needs 2.",
            ),
            Choice(
                "Swap adjacent pairs", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Count adjacent \"][\".",
                why="Swaps can be between any positions.",
            ),
        ),
    ),
    Question(
        slug="reverse-substrings-between-each-pair-of-parentheses", number=1190, title="Reverse Substrings Between Each Pair of Parentheses",
        difficulty="Medium", topics=("data-structures",),
        summary="Reverse the text inside each matched pair of parentheses, innermost first, and remove the parentheses.",
        example="\"(u(love)i)\"  →  \"iloveu\"",
        criterion="Which approach is linear?",
        hint="Pair up parentheses first. When reading, what happens if you jump to a parenthesis's partner and turn around?",
        choices=(
            Choice(
                "Pair indices, then walk with jumps", OPTIMAL, time="O(n)", space="O(n)", visual="stack",
                detail="Match parentheses with a stack; walk the string, and at a parenthesis jump to its partner and reverse direction.",
                why="Each reversal flips the reading direction inside it, so jumping and turning around reads characters in final order without copying.",
            ),
            Choice(
                "Stack of strings, reverse on ')'", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="stack",
                detail="Build the current string; on ')', reverse it and append to the outer one.",
                why="Correct, but deep nesting reverses the same characters many times.",
            ),
            Choice(
                "Reverse once, drop parentheses", INCORRECT, time="O(n)", space="O(n)", visual="brute",
                detail="Reverse the whole string's letters.",
                why="\"love\" is reversed twice in the example, so it ends up forwards.",
            ),
            Choice(
                "Reverse outermost first", INCORRECT, time="O(n²)", space="O(n)", visual="brute",
                detail="Process from the outside in, reversing raw text including inner parentheses.",
                why="Reversing turns inner '(' into ')' order. Are the pairs still matched?",
            ),
        ),
    ),
    Question(
        slug="valid-parenthesis-string", number=678, title="Valid Parenthesis String",
        difficulty="Medium", topics=("data-structures",),
        summary="'*' can be '(', ')' or empty. Return whether s can be valid.",
        example="\"(*))\"  →  true",
        criterion="Which approach is linear with O(1) extra space?",
        hint="Instead of one open count, track the range of possible open counts.",
        choices=(
            Choice(
                "Track min and max open counts", OPTIMAL, time="O(n)", space="O(1)", visual="greedy",
                detail="'(' raises both, ')' lowers both, '*' lowers min and raises max; fail if max < 0; clamp min at 0; valid if min is 0 at the end.",
                why="Every count in [min, max] is reachable, so the string works iff 0 is in the final range and max never went negative.",
            ),
            Choice(
                "Two stacks of indices", SUBOPTIMAL, time="O(n)", space="O(n)", visual="stack",
                detail="Match ')' with '(' first, then '*'; finally match leftover '(' with later '*'.",
                why="Correct, but stores indices.",
            ),
            Choice(
                "Treat '*' as '('", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Count stars as openers.",
                why="\"(*\" would then be two unclosed.",
            ),
            Choice(
                "Ignore '*'", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Check the brackets alone.",
                why="\"(*))\" needs the star as '('.",
            ),
        ),
    ),
    Question(
        slug="longest-valid-parentheses", number=32, title="Longest Valid Parentheses",
        difficulty="Hard", topics=("data-structures",),
        summary="Return the length of the longest valid (well-formed) parentheses substring.",
        example="\")()())\"  →  4",
        criterion="Which approach is linear with O(1) extra space?",
        hint="Scan with open and close counters. When do you reset? Why scan twice?",
        choices=(
            Choice(
                "Two counter passes", OPTIMAL, time="O(n)", space="O(1)", visual="counting",
                detail="Left to right: record 2·close when equal, reset when close > open; then right to left with roles swapped.",
                why="The forward pass misses runs with extra '(' at the end, like \"(()\"; the backward pass catches them.",
            ),
            Choice(
                "Stack of indices with a sentinel", SUBOPTIMAL, time="O(n)", space="O(n)", visual="stack",
                detail="Push −1; push '(' indices; on ')', pop and measure from the new top, or push i if empty.",
                why="Correct and linear, but uses O(n) space.",
            ),
            Choice(
                "Count matched pairs", INCORRECT, time="O(n)", space="O(n)", visual="stack",
                detail="Return 2 × total matched pairs.",
                why="\"()(()\" has two matched pairs, not contiguous.",
            ),
            Choice(
                "One forward pass", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Only the left-to-right counter pass.",
                why="\"(()\" never has equal counts, so it reports 0.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §3.5 expression parsing
    Question(
        slug="clumsy-factorial", number=1006, title="Clumsy Factorial",
        difficulty="Medium", topics=("data-structures",),
        summary="clumsy(n) = n * (n−1) / (n−2) + (n−3) − (n−4) * … cycling *, /, +, − with normal precedence and integer division.",
        example="10  →  12",
        criterion="Which approach is O(1)?",
        hint="Work out clumsy for small n. Does a pattern appear by n mod 4?",
        choices=(
            Choice(
                "Closed form by n mod 4", OPTIMAL, time="O(1)", space="O(1)", visual="math",
                detail="For n > 4, the answer is n + 1, n + 2, n + 2 or n − 1 depending on n mod 4; small n are special cases.",
                why="Each block k·(k−1)/(k−2) is about k + 1, and the following + and − blocks cancel in a fixed pattern.",
            ),
            Choice(
                "Stack evaluation", SUBOPTIMAL, time="O(n)", space="O(n)", visual="stack",
                detail="Apply * and / to the top, push + terms and − terms, sum the stack.",
                why="Correct and the standard method, but the expression has a closed form.",
            ),
            Choice(
                "Left to right", INCORRECT, time="O(n)", space="O(1)", visual="brute",
                detail="Apply operators in order without precedence.",
                why="10·9/8+7−6·5… multiplies 6·5 before subtracting.",
            ),
            Choice(
                "Exact division", INCORRECT, time="O(n)", space="O(n)", visual="stack",
                detail="Use real division.",
                why="10·9/8 floors to 11.",
            ),
        ),
    ),
    Question(
        slug="evaluate-reverse-polish-notation", number=150, title="Evaluate Reverse Polish Notation",
        difficulty="Medium", topics=("data-structures",),
        summary="Evaluate an expression in postfix notation (+, −, *, / truncating toward zero).",
        example="[\"2\",\"1\",\"+\",\"3\",\"*\"]  →  9",
        criterion="Which approach is linear?",
        hint="An operator applies to which two values?",
        choices=(
            Choice(
                "Operand stack", OPTIMAL, time="O(n)", space="O(n)", visual="stack",
                detail="Push numbers; on an operator, pop b then a, push a op b.",
                why="In postfix, an operator's operands are the two most recent values, exactly the stack's top two.",
            ),
            Choice(
                "Rebuild and rescan", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="brute",
                detail="Find the first operator, replace it and its operands with the result, repeat.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Pop a then b", INCORRECT, time="O(n)", space="O(n)", visual="stack",
                detail="Use the first popped value as the left operand.",
                why="[\"4\",\"2\",\"-\"] would give −2.",
            ),
            Choice(
                "Floor division", INCORRECT, time="O(n)", space="O(n)", visual="stack",
                detail="Use Python's // for '/'.",
                why="−7 / 2 truncates to −3, but // gives −4.",
            ),
        ),
    ),
    Question(
        slug="decode-string", number=394, title="Decode String",
        difficulty="Medium", topics=("data-structures",),
        summary="k[encoded] means encoded repeated k times; patterns nest. Return the decoded string.",
        example="\"3[a2[c]]\"  →  \"accaccacc\"",
        criterion="Which approach is linear in the output size?",
        hint="When you hit '[', what do you need to remember to finish the outer string later?",
        choices=(
            Choice(
                "Stack of (count, prefix)", OPTIMAL, time="O(output)", space="O(output)", visual="stack",
                detail="On '[', push the current count and string and start fresh; on ']', pop and set string = prefix + count × string.",
                why="Each nesting level waits for its inner result. The stack holds exactly those pending levels.",
            ),
            Choice(
                "Expand innermost brackets repeatedly", SUBOPTIMAL, time="O(output·depth)", space="O(output)", visual="brute",
                detail="Find an innermost k[…], replace it with its expansion, repeat.",
                why="Correct, but rewrites the whole string each time.",
            ),
            Choice(
                "Single-digit counts", INCORRECT, time="O(output)", space="O(output)", visual="stack",
                detail="Read one digit before '['.",
                why="\"12[a]\" means 12, not 2.",
            ),
            Choice(
                "Ignore nesting", INCORRECT, time="O(n)", space="O(n)", visual="brute",
                detail="Expand each k[…] by its literal contents.",
                why="Inner patterns must be expanded first.",
            ),
        ),
    ),
    Question(
        slug="string-to-integer-atoi", number=8, title="String to Integer (atoi)",
        difficulty="Medium", topics=("data-structures",),
        summary="Parse leading spaces, an optional sign and digits into a 32-bit integer, clamping on overflow and ignoring the rest.",
        example="\"   -42abc\"  →  -42",
        criterion="Which approach is correct without exceeding 32-bit arithmetic?",
        hint="How do you detect overflow before it happens?",
        choices=(
            Choice(
                "One pass, check before multiplying", OPTIMAL, time="O(n)", space="O(1)", visual="greedy",
                detail="Skip spaces, read a sign, then for each digit clamp if result > (INT_MAX − d) / 10.",
                why="Checking the bound before result·10 + d keeps every intermediate value in range.",
            ),
            Choice(
                "Parse into 64-bit, then clamp", SUBOPTIMAL, time="O(n)", space="O(1)", visual="greedy",
                detail="Accumulate in a long and clamp at the end (stopping early when far past the limit).",
                why="Correct if you stop early, but relies on a wider type.",
            ),
            Choice(
                "Accumulate, clamp at the end", INCORRECT, time="O(n)", space="O(1)", visual="brute",
                detail="Read all digits into an int, then clamp.",
                why="\"99999999999\" overflows before you clamp.",
            ),
            Choice(
                "Skip all non-digits", INCORRECT, time="O(n)", space="O(1)", visual="brute",
                detail="Collect digits anywhere in the string.",
                why="\"4193 with words\" stops at the space; \"words 987\" is 0.",
            ),
        ),
    ),
    Question(
        slug="basic-calculator", number=224, title="Basic Calculator",
        difficulty="Hard", topics=("data-structures",),
        summary="Evaluate an expression with +, −, parentheses and unary minus.",
        example="\"(1+(4+5+2)-3)+(6+8)\"  →  23",
        criterion="Which approach is linear?",
        hint="Without * and /, every number is added with a sign. What decides that sign?",
        choices=(
            Choice(
                "Stack of enclosing signs", OPTIMAL, time="O(n)", space="O(n)", visual="stack",
                detail="Keep the current sign as the product of the enclosing parentheses' signs; on '(' push it, on ')' pop.",
                why="Each number's final sign is its own operator times the signs of the parentheses around it.",
            ),
            Choice(
                "Recursive evaluation of substrings", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="recursion",
                detail="Find each matching ')' and evaluate the inside by copying it.",
                why="Correct, but copying substrings at each level is quadratic.",
            ),
            Choice(
                "Ignore parentheses", INCORRECT, time="O(n)", space="O(1)", visual="brute",
                detail="Apply signs left to right, skipping brackets.",
                why="\"1−(2+3)\" would give 2 instead of −4.",
            ),
            Choice(
                "Flip sign only for the next number", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Treat \"−(\" as negating just the first number inside.",
                why="The minus applies to everything inside.",
            ),
        ),
    ),
    Question(
        slug="basic-calculator-ii", number=227, title="Basic Calculator II",
        difficulty="Medium", topics=("data-structures",),
        summary="Evaluate an expression with +, −, *, / (truncating) and no parentheses.",
        example="\"3+2*2\"  →  7",
        criterion="Which approach is linear with O(1) extra space?",
        hint="* and / only affect the most recent term.",
        choices=(
            Choice(
                "Running total plus last term", OPTIMAL, time="O(n)", space="O(1)", visual="greedy",
                detail="On + or −, add the last term to the total and start a new one; on * or /, update the last term.",
                why="High-precedence operators only modify the current term, so one term is the only state that's still open.",
            ),
            Choice(
                "Stack of terms", SUBOPTIMAL, time="O(n)", space="O(n)", visual="stack",
                detail="Push signed terms; pop and replace on * and /; sum at the end.",
                why="Correct and common, but only the top is ever modified.",
            ),
            Choice(
                "Left to right", INCORRECT, time="O(n)", space="O(1)", visual="brute",
                detail="Apply operators as they appear.",
                why="3 + 2 then × 2 gives 10.",
            ),
            Choice(
                "* and / right to left", INCORRECT, time="O(n)", space="O(n)", visual="stack",
                detail="Apply a run of * and / from the right end.",
                why="8/2*2 is (8/2)*2 = 8. Right to left gives 2.",
            ),
        ),
    ),
    Question(
        slug="number-of-atoms", number=726, title="Number of Atoms",
        difficulty="Hard", topics=("data-structures",),
        summary="Count atoms in a chemical formula with nested parentheses and multipliers. Return element counts sorted by name.",
        example="\"K4(ON(SO3)2)2\"  →  \"K4N2O14S4\"",
        criterion="Which approach is linear before sorting?",
        hint="A multiplier after ')' applies to everything inside. Reading backwards, you see it first.",
        choices=(
            Choice(
                "Right-to-left with a multiplier stack", OPTIMAL, time="O(n + k log k)", space="O(n)", visual="stack",
                detail="Read numbers from the right; on ')', push current multiplier × number; on '(', pop; add each atom × multiplier.",
                why="Reading backwards meets every multiplier before its contents, so each atom is counted once with its full multiplier.",
            ),
            Choice(
                "Stack of count maps", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="stack",
                detail="On ')', pop a map, multiply its counts and merge into the outer map.",
                why="Correct, but deep nesting re-multiplies and re-merges the same atoms.",
            ),
            Choice(
                "Ignore parentheses", INCORRECT, time="O(n)", space="O(n)", visual="hashmap",
                detail="Count atoms with their own subscripts only.",
                why="(SO3)2 doubles S and O.",
            ),
            Choice(
                "Single-letter elements", INCORRECT, time="O(n)", space="O(n)", visual="hashmap",
                detail="Treat each capital letter alone as an element.",
                why="\"Mg\" is one element, not M and g.",
            ),
        ),
    ),
    Question(
        slug="tag-validator", number=591, title="Tag Validator",
        difficulty="Hard", topics=("data-structures",),
        summary="Validate a code snippet of nested tags <TAG>…</TAG> (names 1–9 uppercase letters) with CDATA sections, all wrapped in one closed tag.",
        example="\"<DIV>This is the first line <![CDATA[<div>]]></DIV>\"  →  true",
        criterion="Which approach is linear?",
        hint="Tags nest like brackets. What should CDATA content be treated as?",
        choices=(
            Choice(
                "Scan with a stack of tag names", OPTIMAL, time="O(n)", space="O(n)", visual="stack",
                detail="Push opening tags, match closing tags with the top, skip CDATA to its terminator, and require the stack to empty exactly at the end.",
                why="Tags nest like parentheses with names, and CDATA is opaque text, so one scan with a stack checks everything.",
            ),
            Choice(
                "Strip innermost tags repeatedly", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="brute",
                detail="Remove CDATA, then delete innermost matched tag pairs until stable.",
                why="Correct with care, but each pass rescans the code.",
            ),
            Choice(
                "Parse tags inside CDATA", INCORRECT, time="O(n)", space="O(n)", visual="stack",
                detail="Treat <div> inside CDATA as a tag.",
                why="CDATA content is plain text.",
            ),
            Choice(
                "Allow several top-level tags", INCORRECT, time="O(n)", space="O(n)", visual="stack",
                detail="Accept when the stack empties anywhere.",
                why="The whole code must be wrapped in one tag.",
            ),
        ),
    ),
    Question(
        slug="parse-lisp-expression", number=736, title="Parse Lisp Expression",
        difficulty="Hard", topics=("data-structures",),
        summary="Evaluate a Lisp-like expression with integers, variables, (add a b), (mult a b) and (let v1 e1 … expr) with lexical scoping.",
        example="\"(let x 2 (mult x (let x 3 y 4 (add x y))))\"  →  14",
        criterion="Which approach is linear in the input (with scoped lookups)?",
        hint="An inner let shadows outer variables only inside it. What structure models nested scopes?",
        choices=(
            Choice(
                "Recursive descent with a scope stack", OPTIMAL, time="O(n)", space="O(n)", visual="recursion",
                detail="Parse with one cursor; each let pushes a scope, assignments go into it, lookups search from the innermost; pop on return.",
                why="One cursor reads every character once, and the scope stack gives each let its own bindings that vanish when it ends.",
            ),
            Choice(
                "Re-tokenize substrings recursively", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="recursion",
                detail="Split each parenthesized expression into parts by copying substrings.",
                why="Correct, but copying at every level is quadratic.",
            ),
            Choice(
                "One global variable map", INCORRECT, time="O(n)", space="O(n)", visual="hashmap",
                detail="Assign variables globally.",
                why="After the inner let ends, x should be 2 again.",
            ),
            Choice(
                "Evaluate all assignments first", INCORRECT, time="O(n)", space="O(n)", visual="hashmap",
                detail="Bind every let variable before evaluating.",
                why="Later assignments can use earlier ones in order, and scope matters.",
            ),
        ),
    ),
    Question(
        slug="valid-number", number=65, title="Valid Number",
        difficulty="Hard", topics=("data-structures",),
        summary="Return whether s is a valid number: optional sign, digits with an optional decimal point, and an optional exponent e/E followed by an integer.",
        example="\"-123.456e789\"  →  true;  \"1e\"  →  false",
        criterion="Which approach is linear and checks the grammar exactly?",
        hint="Which facts do you need to remember while scanning: seen a digit? a dot? an exponent?",
        choices=(
            Choice(
                "One scan with state flags", OPTIMAL, time="O(n)", space="O(1)", visual="greedy",
                detail="Track seenDigit, seenDot, seenExp; a sign only at the start or after e; a dot only before e; reset seenDigit after e; end with seenDigit.",
                why="Each rule is local to a position plus a few facts about the past, so flags decide validity in one pass.",
            ),
            Choice(
                "Hand-written regular expression", SUBOPTIMAL, time="O(n)", space="O(1)", visual="brute",
                detail="Match ^[+-]?(\\d+\\.?\\d*|\\.\\d+)([eE][+-]?\\d+)?$.",
                why="Correct when written carefully, but hard to get exactly right and to read.",
            ),
            Choice(
                "Language float parser", INCORRECT, time="O(n)", space="O(1)", visual="brute",
                detail="Return whether float(s) succeeds.",
                why="float(\"inf\") and float(\"nan\") succeed. Are they valid here?",
            ),
            Choice(
                "Allow a dot in the exponent", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Treat the exponent like the mantissa.",
                why="\"1e2.5\" is invalid.",
            ),
        ),
    ),
    Question(
        slug="ternary-expression-parser", number=439, title="Ternary Expression Parser",
        difficulty="Medium", topics=("data-structures",),
        summary="Evaluate a nested ternary expression of single-digit values and T/F conditions, grouping right to left.",
        example="\"F?1:T?4:5\"  →  \"4\"",
        criterion="Which approach is linear?",
        hint="The rightmost '?' has both its branches already as plain values.",
        choices=(
            Choice(
                "Scan right to left with a stack", OPTIMAL, time="O(n)", space="O(n)", visual="stack",
                detail="Push values; at a '?', pop the true and false branches and push the one chosen by the condition before it.",
                why="Right-to-left grouping means each '?' sees fully evaluated branches on the stack.",
            ),
            Choice(
                "Recursive split at the matching ':'", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="recursion",
                detail="Find each '?''s matching ':' by counting, then recurse on substrings.",
                why="Correct, but scanning for matches at every level is quadratic.",
            ),
            Choice(
                "Group left to right", INCORRECT, time="O(n)", space="O(1)", visual="brute",
                detail="Evaluate the first ternary first.",
                why="\"T?T?1:2:3\" nests in the true branch.",
            ),
            Choice(
                "Take the first value", INCORRECT, time="O(1)", space="O(1)", visual="brute",
                detail="Return the first value after the first '?'.",
                why="The first condition here is F.",
            ),
        ),
    ),
    Question(
        slug="evaluate-valid-expressions", number=3749, title="Evaluate Valid Expressions",
        difficulty="Hard", topics=("data-structures",),
        summary="An expression is an integer (possibly negative) or op(a,b) with op among add, sub, mul and div (every division is exact). Evaluate it.",
        example="\"div(mul(4,sub(9,5)),add(1,1))\"  →  8",
        criterion="Which approach is linear?",
        hint="Every op(…) has its arguments complete when its ')' arrives.",
        choices=(
            Choice(
                "Recursive descent with one cursor", OPTIMAL, time="O(n)", space="O(depth)", visual="recursion",
                detail="parse(): if a letter, read the op, '(', parse(), ',', parse(), ')'; else read an integer.",
                why="The grammar is prefix notation, so one forward pass decides every token, and recursion depth matches nesting.",
            ),
            Choice(
                "Rewrite the innermost op repeatedly", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="brute",
                detail="Find an op with numeric arguments, replace it by its value, repeat.",
                why="Correct, but rescans the string each time.",
            ),
            Choice(
                "Evaluate operators left to right", INCORRECT, time="O(n)", space="O(n)", visual="brute",
                detail="Apply each op as soon as you see it to the numbers that follow.",
                why="mul's arguments must be finished before div uses the result.",
            ),
            Choice(
                "Read '-' as an operator", INCORRECT, time="O(n)", space="O(depth)", visual="recursion",
                detail="Treat every '-' as subtraction.",
                why="\"-42\" is a negative literal. What's on the left of that minus?",
            ),
        ),
    ),
    Question(
        slug="basic-calculator-iii", number=772, title="Basic Calculator III",
        difficulty="Hard", topics=("data-structures",),
        summary="Evaluate an expression with +, −, *, / (truncating) and parentheses.",
        example="\"2*(5+5*2)/3+(6/2+8)\"  →  21",
        criterion="Which approach is linear?",
        hint="Treat a parenthesized group as one number. How do you get its value without copying it?",
        choices=(
            Choice(
                "Recursive descent with a shared cursor", OPTIMAL, time="O(n)", space="O(depth)", visual="recursion",
                detail="Calculator II's total-and-last-term loop; on '(', recurse and use the result as a number; return on ')'.",
                why="A shared cursor means each character is read once, and recursion handles parentheses as single values.",
            ),
            Choice(
                "Recurse on copied substrings", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="recursion",
                detail="Find each matching ')' and evaluate a copy of the inside.",
                why="Correct, but copying at each level is quadratic.",
            ),
            Choice(
                "Left to right", INCORRECT, time="O(n)", space="O(1)", visual="brute",
                detail="Ignore precedence.",
                why="5 + 5 × 2 would become 20.",
            ),
            Choice(
                "Ignore parentheses", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Drop them and use precedence.",
                why="2 × (5 + …) groups the sum first.",
            ),
        ),
    ),
    Question(
        slug="brace-expansion", number=1087, title="Brace Expansion",
        difficulty="Medium", topics=("data-structures",),
        summary="s like \"{a,b}c{d,e}f\" has single letters or {option lists} (no nesting). Return every word it describes, sorted.",
        example="\"{a,b}c{d,e}f\"  →  [\"acdf\",\"acef\",\"bcdf\",\"bcef\"]",
        criterion="Which approach produces the sorted output directly?",
        hint="If each option list is sorted, in what order does a left-to-right product come out?",
        choices=(
            Choice(
                "Parse groups, sort each, then take the product", OPTIMAL, time="O(output·n)", space="O(n)", visual="backtrack",
                detail="Turn s into a list of sorted option lists and backtrack over them left to right.",
                why="With every group sorted, the product is generated in lexicographic order, so no final sort is needed.",
            ),
            Choice(
                "Generate in any order, then sort", SUBOPTIMAL, time="O(output·n·log)", space="O(output·n)", visual="sort",
                detail="Expand without sorting groups and sort the words.",
                why="Correct, but sorts the whole output.",
            ),
            Choice(
                "No sorting at all", INCORRECT, time="O(output·n)", space="O(n)", visual="backtrack",
                detail="Expand groups in the given order.",
                why="\"{b,a}\" would list b first.",
            ),
            Choice(
                "Concatenate the groups", INCORRECT, time="O(n)", space="O(n)", visual="brute",
                detail="Join all options into one word.",
                why="Each word picks one option per group.",
            ),
        ),
    ),
    Question(
        slug="build-binary-expression-tree-from-infix-expression", number=1597, title="Build Binary Expression Tree From Infix Expression",
        difficulty="Hard", topics=("data-structures",),
        summary="Build a binary expression tree from an infix expression with single-digit operands, +, −, *, / and parentheses. Its in-order traversal (without parentheses) must match the input's order.",
        example="\"3*4-2*5\"  →  tree rooted at '-' with children 3*4 and 2*5",
        criterion="Which approach is linear?",
        hint="Use the classic two-stack (shunting-yard) method, building nodes instead of numbers.",
        choices=(
            Choice(
                "Operator stack and node stack", OPTIMAL, time="O(n)", space="O(n)", visual="stack",
                detail="Before pushing an operator, reduce while the top has ≥ precedence; '(' waits, ')' reduces to '('; a reduction pops two nodes and makes a new one.",
                why="Reducing higher-or-equal precedence first gives left associativity and precedence, and each token is pushed and popped once.",
            ),
            Choice(
                "Split at the lowest-precedence operator recursively", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="recursion",
                detail="Find the last top-level + or − (else * or /) and recurse on both sides.",
                why="Correct, but each level rescans its substring.",
            ),
            Choice(
                "Build left to right", INCORRECT, time="O(n)", space="O(n)", visual="tree-dfs",
                detail="Each operator takes the tree so far as its left child.",
                why="3*4−2*5 would group (3*4−2)*5.",
            ),
            Choice(
                "Reduce only on strictly higher precedence", INCORRECT, time="O(n)", space="O(n)", visual="stack",
                detail="Leave equal-precedence operators on the stack.",
                why="8−3−2 would become 8−(3−2).",
            ),
        ),
    ),
    Question(
        slug="design-an-expression-tree-with-evaluate-function", number=1628, title="Design an Expression Tree With Evaluate Function",
        difficulty="Medium", topics=("data-structures",),
        summary="Build an expression tree from postfix tokens and give each node an evaluate() method.",
        example="[\"3\",\"4\",\"+\",\"2\",\"*\",\"7\",\"/\"]  →  evaluate() = 2",
        criterion="Which approach builds the tree in linear time?",
        hint="Postfix again: an operator's operands are the two most recent subtrees.",
        choices=(
            Choice(
                "Stack of subtrees", OPTIMAL, time="O(n)", space="O(n)", visual="stack",
                detail="Push leaves; on an operator, pop right then left and push a new node.",
                why="Each operator combines the two latest subtrees, exactly as in RPN evaluation.",
            ),
            Choice(
                "Re-scan for the next operator", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="brute",
                detail="Find the first operator, combine its two preceding items, splice, repeat.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Pop left then right", INCORRECT, time="O(n)", space="O(n)", visual="stack",
                detail="The first popped subtree becomes the left child.",
                why="\"4\",\"2\",\"-\" would evaluate to −2.",
            ),
            Choice(
                "Evaluate without a tree", INCORRECT, time="O(n)", space="O(n)", visual="stack",
                detail="Return only the number.",
                why="The task is to design the tree with an evaluate method.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §4.1 queue basics
    Question(
        slug="number-of-recent-calls", number=933, title="Number of Recent Calls",
        difficulty="Easy", topics=("data-structures",),
        summary="ping(t) records a request at time t (strictly increasing) and returns how many requests fall in [t − 3000, t].",
        example="ping 1 → 1, ping 100 → 2, ping 3001 → 3, ping 3002 → 3",
        criterion="Which approach is O(1) amortized per ping?",
        hint="Once a request is too old for one ping, can it matter for a later one?",
        choices=(
            Choice(
                "Queue, drop expired from the front", OPTIMAL, time="O(1) amortized", space="O(W)", visual="queue",
                detail="Append t; pop the front while it's below t − 3000; return the size.",
                why="Times increase, so expired requests are always at the front and never come back. Each one is popped once.",
            ),
            Choice(
                "Keep all times, count by scanning", SUBOPTIMAL, time="O(n) per ping", space="O(n)", visual="brute",
                detail="Store every time and count those in range.",
                why="Correct, but rescans old requests forever.",
            ),
            Choice(
                "Count all pings", INCORRECT, time="O(1)", space="O(1)", visual="counting",
                detail="Return the total so far.",
                why="ping 3002 should not count the request at 1.",
            ),
            Choice(
                "Exclusive lower bound", INCORRECT, time="O(1) amortized", space="O(W)", visual="queue",
                detail="Drop times ≤ t − 3000.",
                why="At t = 3001, the ping at 1 is exactly 3000 earlier and still counts.",
            ),
        ),
    ),
    Question(
        slug="design-ride-sharing-system", number=3829, title="Design Ride Sharing System",
        difficulty="Medium", topics=("data-structures",),
        summary="Riders and drivers join over time. match() pairs the earliest waiting driver with the earliest waiting rider, or returns [−1, −1]. cancelRider(id) removes a waiting rider (no effect if matched).",
        example="addRider 3, addDriver 2, addRider 1, match → [2,3], addDriver 5, cancelRider 3, match → [5,1]",
        criterion="Which approach makes every operation O(1) amortized?",
        hint="Removing a rider from the middle of a queue is expensive. What if you just remember they cancelled?",
        choices=(
            Choice(
                "Two queues with lazy cancellation", OPTIMAL, time="O(1) amortized", space="O(n)", visual="queue",
                detail="Mark cancelled riders in a set; when matching, skip marked riders at the front.",
                why="Each rider is skipped or matched once, so lazy deletion keeps every call cheap while preserving arrival order.",
            ),
            Choice(
                "Remove cancelled riders from a list", SUBOPTIMAL, time="O(n) cancel", space="O(n)", visual="array-copy",
                detail="Search and delete the rider on cancel.",
                why="Correct, but each cancel scans and shifts.",
            ),
            Choice(
                "Match the newest rider", INCORRECT, time="O(1)", space="O(n)", visual="stack",
                detail="Use stacks instead of queues.",
                why="Riders must be served in arrival order.",
            ),
            Choice(
                "Cancel matched riders too", INCORRECT, time="O(1)", space="O(n)", visual="queue",
                detail="Mark any rider id on cancel.",
                why="A matched rider is gone; cancelling must not affect a later rider with the same id.",
            ),
        ),
    ),
    Question(
        slug="reveal-cards-in-increasing-order", number=950, title="Reveal Cards In Increasing Order",
        difficulty="Medium", topics=("data-structures",),
        summary="Repeatedly reveal the top card, then move the next top card to the bottom. Order the deck so cards are revealed in increasing order.",
        example="[17,13,11,2,3,5,7]  →  [2,13,3,11,5,17,7]",
        criterion="Which approach is O(n log n)?",
        hint="Simulate the process on positions instead of cards.",
        choices=(
            Choice(
                "Simulate on a queue of positions", OPTIMAL, time="O(n log n)", space="O(n)", visual="queue",
                detail="Sort the cards; queue indices 0..n−1; repeatedly pop a position for the next smallest card and rotate one index to the back.",
                why="The reveal order depends only on positions, so simulating it on indices tells where each sorted card must go.",
            ),
            Choice(
                "Simulate with array shifting", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="array-copy",
                detail="Same simulation, but remove and append by shifting a list.",
                why="Correct, but each step shifts the list.",
            ),
            Choice(
                "Sorted order", INCORRECT, time="O(n log n)", space="O(1)", visual="sort",
                detail="Return the deck sorted ascending.",
                why="The second card is moved to the bottom, not revealed second.",
            ),
            Choice(
                "Interleave halves", INCORRECT, time="O(n log n)", space="O(n)", visual="two-pointers",
                detail="Put the smaller half at even positions and the rest at odd positions in order.",
                why="Cards moved to the bottom get revealed in a rotating pattern, not a simple interleave.",
            ),
        ),
    ),
    Question(
        slug="dota2-senate", number=649, title="Dota2 Senate",
        difficulty="Medium", topics=("data-structures",),
        summary="Senators from Radiant (R) and Dire (D) act in order, round after round; each bans one opposing senator. Return the party that wins.",
        example="\"DDRRR\"  →  \"Dire\"",
        criterion="Which approach is linear?",
        hint="Whose turn comes first decides who bans whom. How do you keep turns in order across rounds?",
        choices=(
            Choice(
                "Two queues of indices", OPTIMAL, time="O(n)", space="O(n)", visual="queue",
                detail="Compare the fronts; the smaller index bans the other and rejoins with index + n.",
                why="The earliest senator acts next and should ban the next opponent. Re-queuing with + n places them in the next round.",
            ),
            Choice(
                "Simulate rounds with a ban array", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="brute",
                detail="Each active senator scans ahead for the next opponent to ban.",
                why="Correct, but scanning for the next opponent is linear each time.",
            ),
            Choice(
                "Majority wins", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Return the party with more senators.",
                why="In \"DDRRR\", the two D's act first and win despite fewer seats.",
            ),
            Choice(
                "Ban the earliest opponent", INCORRECT, time="O(n)", space="O(n)", visual="queue",
                detail="Each senator bans the first opponent in the string.",
                why="An opponent who has already acted this round is less dangerous than one about to act.",
            ),
        ),
    ),
    Question(
        slug="moving-average-from-data-stream", number=346, title="Moving Average from Data Stream",
        difficulty="Easy", topics=("data-structures",),
        summary="next(val) returns the average of the last size values seen.",
        example="size 3: next 1 → 1.0, next 10 → 5.5, next 3 → 4.67, next 5 → 6.0",
        criterion="Which approach is O(1) per call?",
        hint="What changes in the sum when a new value arrives?",
        choices=(
            Choice(
                "Queue with a running sum", OPTIMAL, time="O(1)", space="O(size)", visual="queue",
                detail="Add the new value; if over size, subtract and pop the oldest.",
                why="Only one value enters and at most one leaves per call.",
            ),
            Choice(
                "Sum the last size values each time", SUBOPTIMAL, time="O(size)", space="O(n)", visual="brute",
                detail="Keep a list and add up its tail.",
                why="Correct, but re-adds the window every call.",
            ),
            Choice(
                "Average of everything", INCORRECT, time="O(1)", space="O(1)", visual="counting",
                detail="Divide the total by the count.",
                why="Old values must drop out.",
            ),
            Choice(
                "Divide by size always", INCORRECT, time="O(1)", space="O(size)", visual="queue",
                detail="Use size as the denominator from the start.",
                why="With one value, next 1 should be 1.0, not 0.33.",
            ),
        ),
    ),
    Question(
        slug="design-hit-counter", number=362, title="Design Hit Counter",
        difficulty="Medium", topics=("data-structures",),
        summary="hit(t) records a hit; getHits(t) returns hits in the past 300 seconds. Timestamps don't decrease; many hits can share a second.",
        example="hit 1, hit 2, hit 3, getHits 4 → 3, hit 300, getHits 300 → 4, getHits 301 → 3",
        criterion="Which approach uses O(300) memory however many hits arrive?",
        hint="Within one second, do you need each hit separately?",
        choices=(
            Choice(
                "300 circular buckets of (time, count)", OPTIMAL, time="O(1) hit, O(300) get", space="O(300)", visual="queue",
                detail="Bucket t % 300 stores its timestamp and count, reset when the timestamp is stale; getHits sums fresh buckets.",
                why="Only 300 seconds matter, so per-second counts in a fixed ring replace an unbounded list of hits.",
            ),
            Choice(
                "Queue of every hit", SUBOPTIMAL, time="O(1) amortized", space="O(hits)", visual="queue",
                detail="Append each hit and drop expired ones on getHits.",
                why="Correct, but a burst of a million hits in one second stores a million entries.",
            ),
            Choice(
                "Total counter", INCORRECT, time="O(1)", space="O(1)", visual="counting",
                detail="Count all hits ever.",
                why="Hits older than 300 seconds must not count.",
            ),
            Choice(
                "Buckets without timestamps", INCORRECT, time="O(1)", space="O(300)", visual="counting",
                detail="Index by t % 300 but never check the stored time.",
                why="After 300 seconds a bucket is reused; its old count would be added to new hits.",
            ),
        ),
    ),
    Question(
        slug="maximum-requests-without-violating-the-limit", number=3851, title="Maximum Requests Without Violating the Limit",
        difficulty="Medium", topics=("data-structures",),
        summary="requests[i] = [user, time]. A user violates the limit if some interval [t, t + window] holds more than k of their requests. Drop as few requests as possible; return how many remain.",
        example="[[1,2],[1,5],[1,2],[1,6]], k = 2, window = 5  →  2",
        criterion="Which approach is O(n log n)?",
        hint="Users are independent. For one user's sorted times, keep each request if you can. What do you need to check?",
        choices=(
            Choice(
                "Per user, sorted times, greedy with a queue of kept times", OPTIMAL, time="O(n log n)", space="O(n)", visual="queue",
                detail="Drop kept times older than t − window from the front; keep t if fewer than k remain, else drop it.",
                why="Keeping the earliest possible requests leaves the most room for later ones, and the queue holds exactly the kept requests that conflict with t.",
            ),
            Choice(
                "Greedy, recount kept requests each time", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="brute",
                detail="Scan all kept times of the user for each new request.",
                why="Correct, but rescans the history.",
            ),
            Choice(
                "Count dropped requests in the window", INCORRECT, time="O(n log n)", space="O(n)", visual="sliding-window",
                detail="Limit by all requests in the window, kept or not.",
                why="Dropped requests don't count toward the limit.",
            ),
            Choice(
                "At most k per user overall", INCORRECT, time="O(n)", space="O(n)", visual="counting",
                detail="Keep the first k requests of each user.",
                why="The limit is per window; far-apart requests can all stay.",
            ),
        ),
    ),
    Question(
        slug="design-phone-directory", number=379, title="Design Phone Directory",
        difficulty="Medium", topics=("data-structures",),
        summary="Manage numbers 0..maxNumbers − 1: get() hands out any free number (−1 if none), check(n) says whether n is free, release(n) frees it.",
        example="maxNumbers 3: get → 0, get → 1, check 2 → true, get → 2, check 2 → false, release 2, check 2 → true",
        criterion="Which approach makes every call O(1)?",
        hint="Keep the free numbers somewhere you can take from in O(1), and a quick way to test membership.",
        choices=(
            Choice(
                "Queue of free numbers plus a used flag array", OPTIMAL, time="O(1)", space="O(n)", visual="queue",
                detail="get pops a free number and marks it; release marks it free and enqueues it (if it was used).",
                why="The queue yields a free number instantly, and the flag array answers check and blocks double releases.",
            ),
            Choice(
                "Scan for a free slot", SUBOPTIMAL, time="O(n) get", space="O(n)", visual="brute",
                detail="Search the flag array for the first free number.",
                why="Correct, but get is linear.",
            ),
            Choice(
                "Counter only", INCORRECT, time="O(1)", space="O(1)", visual="counting",
                detail="Hand out 0, 1, 2, … and ignore releases.",
                why="Released numbers must be reusable.",
            ),
            Choice(
                "Enqueue on every release", INCORRECT, time="O(1)", space="O(n)", visual="queue",
                detail="Push the number back even if it was already free.",
                why="Releasing a free number twice would hand it out twice.",
            ),
        ),
    ),
    Question(
        slug="first-unique-number", number=1429, title="First Unique Number",
        difficulty="Medium", topics=("data-structures",),
        summary="Keep a queue of integers; showFirstUnique() returns the first value that appears exactly once (or −1); add(x) appends x.",
        example="[2,3,5]: showFirstUnique → 2, add 5, add 2 → showFirstUnique → 3",
        criterion="Which approach is O(1) amortized per call?",
        hint="Once a value stops being unique, can it ever become unique again?",
        choices=(
            Choice(
                "Queue plus counts, pop non-unique fronts", OPTIMAL, time="O(1) amortized", space="O(n)", visual="queue",
                detail="Count every value; showFirstUnique pops from the front while the front's count is > 1.",
                why="A value that became non-unique stays that way, so it can be discarded for good. Each value is popped once.",
            ),
            Choice(
                "Scan for the first unique each time", SUBOPTIMAL, time="O(n) show", space="O(n)", visual="brute",
                detail="Walk the queue checking counts.",
                why="Correct, but rescans dead values every call.",
            ),
            Choice(
                "Remember one 'first unique' variable", INCORRECT, time="O(1)", space="O(n)", visual="counting",
                detail="Update it only when the current one gets a duplicate, setting it to the newly added value.",
                why="After 2 is duplicated, the next unique is 3, which was added earlier, not the newest value.",
            ),
            Choice(
                "Set of seen values", INCORRECT, time="O(1)", space="O(n)", visual="set",
                detail="Return the first value in insertion order.",
                why="A set can't tell a value seen twice from one seen once.",
            ),
        ),
    ),
    Question(
        slug="time-taken-to-cross-the-door", number=2534, title="Time Taken to Cross the Door",
        difficulty="Hard", topics=("data-structures",),
        summary="People arrive at a door (sorted times) to enter (0) or exit (1); one person crosses per second. If the door was idle last second, exit goes first; otherwise the previous direction goes first; ties by index. Return each crossing time.",
        example="arrival = [0,1,1,2,4], state = [0,1,0,0,1]  →  [0,3,1,2,4]",
        criterion="Which approach is O(n + T)?",
        hint="Keep the waiting people for each direction in arrival order.",
        choices=(
            Choice(
                "Two queues and the last direction", OPTIMAL, time="O(n + T)", space="O(n)", visual="queue",
                detail="Each second, enqueue new arrivals; pick a queue by the rules (idle → exit); pop one; if both empty, mark idle.",
                why="Within a direction, order is by index, which a queue keeps. The rules only need the previous second's use.",
            ),
            Choice(
                "Rescan all waiting people each second", SUBOPTIMAL, time="O(n·T)", space="O(n)", visual="brute",
                detail="Search the waiting list for the next person.",
                why="Correct, but each second scans everyone.",
            ),
            Choice(
                "Strict arrival order", INCORRECT, time="O(n)", space="O(1)", visual="queue",
                detail="Let people cross in index order.",
                why="At t = 1, person 2 enters before person 1 exits.",
            ),
            Choice(
                "Exit always first", INCORRECT, time="O(n + T)", space="O(n)", visual="queue",
                detail="Prefer exits every second.",
                why="After an entry, the next waiting enterer goes first.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §4.2 queue design
    Question(
        slug="design-front-middle-back-queue", number=1670, title="Design Front Middle Back Queue",
        difficulty="Medium", topics=("data-structures",),
        summary="Support push and pop at the front, middle and back (the middle is the frontmost of two middles).",
        example="pushFront 1, pushBack 2, pushMiddle 3, pushMiddle 4 → [1,4,3,2]; popMiddle → 4",
        criterion="Which approach makes every operation O(1)?",
        hint="Split the queue into two halves. Where is the middle then?",
        choices=(
            Choice(
                "Two deques kept balanced", OPTIMAL, time="O(1)", space="O(n)", visual="queue",
                detail="Keep the left half with as many or one fewer elements than the right; the middle is at their seam; rebalance by moving one element.",
                why="With the halves balanced, the middle is always at an end of one deque, and each operation moves at most one element.",
            ),
            Choice(
                "Array with insertion", SUBOPTIMAL, time="O(n) middle", space="O(n)", visual="array-copy",
                detail="Insert and delete at index n/2 in a list.",
                why="Correct, but middle operations shift half the list.",
            ),
            Choice(
                "Single deque", INCORRECT, time="O(1)", space="O(n)", visual="queue",
                detail="Treat the middle like the front.",
                why="pushMiddle must go in the middle.",
            ),
            Choice(
                "Unbalanced halves", INCORRECT, time="O(1)", space="O(n)", visual="queue",
                detail="Never move elements between the deques.",
                why="After many pushFronts, the seam is far from the middle.",
            ),
        ),
    ),
    Question(
        slug="implement-stack-using-queues", number=225, title="Implement Stack using Queues",
        difficulty="Easy", topics=("data-structures",),
        summary="Implement a stack (push, pop, top, empty) using only queue operations.",
        example="push 1, push 2, top → 2, pop → 2, empty → false",
        criterion="Which approach uses a single queue?",
        hint="After pushing x to the back, how do you bring it to the front?",
        choices=(
            Choice(
                "One queue, rotate after push", OPTIMAL, time="O(n) push, O(1) pop", space="O(n)", visual="queue",
                detail="Enqueue x, then dequeue and re-enqueue the previous n − 1 elements.",
                why="Rotating puts the newest element at the front, so the queue's front is always the stack's top.",
            ),
            Choice(
                "Two queues, move on push", SUBOPTIMAL, time="O(n) push, O(1) pop", space="O(n)", visual="queue",
                detail="Enqueue x into an empty queue, move everything from the other queue behind it, swap names.",
                why="Correct with the same costs, but it needs a second queue.",
            ),
            Choice(
                "Pop from the front directly", INCORRECT, time="O(1)", space="O(n)", visual="queue",
                detail="Use the queue as is.",
                why="That's first-in, first-out. A stack pops the newest.",
            ),
            Choice(
                "Rotate on pop without restoring", INCORRECT, time="O(n)", space="O(n)", visual="queue",
                detail="Move n − 1 elements back, then pop, but don't fix top().",
                why="top() would then see the oldest element.",
            ),
        ),
    ),
    Question(
        slug="implement-queue-using-stacks", number=232, title="Implement Queue using Stacks",
        difficulty="Easy", topics=("data-structures",),
        summary="Implement a FIFO queue (push, pop, peek, empty) using only stack operations.",
        example="push 1, push 2, peek → 1, pop → 1, empty → false",
        criterion="Which approach is O(1) amortized per operation?",
        hint="Pouring one stack into another reverses it.",
        choices=(
            Choice(
                "In-stack and out-stack, refill lazily", OPTIMAL, time="O(1) amortized", space="O(n)", visual="stack",
                detail="Push to in; pop/peek from out, pouring in → out only when out is empty.",
                why="Each element is moved from in to out once, so the total work is linear over all operations.",
            ),
            Choice(
                "Pour back and forth on every pop", SUBOPTIMAL, time="O(n) per pop", space="O(n)", visual="stack",
                detail="Move all to the other stack, pop, move all back.",
                why="Correct, but moves everything twice per pop.",
            ),
            Choice(
                "One stack", INCORRECT, time="O(1)", space="O(n)", visual="stack",
                detail="Pop from the top.",
                why="That returns 2 first, not 1.",
            ),
            Choice(
                "Pour even when out isn't empty", INCORRECT, time="O(n)", space="O(n)", visual="stack",
                detail="Move in → out before every pop.",
                why="New elements would land on top of older ones in out and come out first.",
            ),
        ),
    ),
    Question(
        slug="design-circular-queue", number=622, title="Design Circular Queue",
        difficulty="Medium", topics=("data-structures",),
        summary="Implement a fixed-capacity circular queue: enQueue, deQueue, Front, Rear, isEmpty, isFull.",
        example="k = 3: enQueue 1, 2, 3 → true; enQueue 4 → false; Rear → 3; deQueue; enQueue 4 → true; Rear → 4",
        criterion="Which approach makes every operation O(1)?",
        hint="With a head index and a size, where does the next element go?",
        choices=(
            Choice(
                "Array with head and size", OPTIMAL, time="O(1)", space="O(k)", visual="queue",
                detail="Insert at (head + size) % k; deQueue advances head; size tells empty and full apart.",
                why="Indices wrap around the array, so no element ever moves, and size removes the empty/full ambiguity.",
            ),
            Choice(
                "Shift on deQueue", SUBOPTIMAL, time="O(k) deQueue", space="O(k)", visual="array-copy",
                detail="Remove index 0 and shift the rest left.",
                why="Correct, but shifts every time.",
            ),
            Choice(
                "Head and tail, no size", INCORRECT, time="O(1)", space="O(k)", visual="queue",
                detail="Full and empty both mean head == tail.",
                why="How do you tell an empty queue from a full one?",
            ),
            Choice(
                "Grow the array", INCORRECT, time="O(1) amortized", space="O(n)", visual="array-copy",
                detail="Append past capacity.",
                why="enQueue must fail when the queue holds k items.",
            ),
        ),
    ),
    Question(
        slug="design-circular-deque", number=641, title="Design Circular Deque",
        difficulty="Medium", topics=("data-structures",),
        summary="Implement a fixed-capacity double-ended queue with insert, delete and peek at both ends.",
        example="k = 3: insertLast 1, insertLast 2, insertFront 3, insertFront 4 → false; getRear → 2",
        criterion="Which approach makes every operation O(1)?",
        hint="Moving the head backward is just (head − 1 + k) % k.",
        choices=(
            Choice(
                "Array with head and size, wrapping both ways", OPTIMAL, time="O(1)", space="O(k)", visual="queue",
                detail="insertFront moves head back one; insertLast writes at (head + size) % k.",
                why="Both ends are index arithmetic on a fixed ring, so nothing shifts.",
            ),
            Choice(
                "List with insert at 0", SUBOPTIMAL, time="O(k) front ops", space="O(k)", visual="array-copy",
                detail="Insert and delete at index 0 by shifting.",
                why="Correct, but front operations are linear.",
            ),
            Choice(
                "Negative index without wrap", INCORRECT, time="O(1)", space="O(k)", visual="queue",
                detail="head − 1 without adding k.",
                why="From head 0, that's −1. Which slot is that in your language?",
            ),
            Choice(
                "Ignore capacity", INCORRECT, time="O(1)", space="O(n)", visual="queue",
                detail="Always accept inserts.",
                why="The fourth insert should fail.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §4.3 deque
    Question(
        slug="faulty-keyboard", number=2810, title="Faulty Keyboard",
        difficulty="Easy", topics=("data-structures",),
        summary="Typing 'i' reverses everything typed so far (the 'i' isn't typed). Return the final text.",
        example="\"string\"  →  \"rtsng\"",
        criterion="Which approach is linear?",
        hint="Instead of reversing, change which end you add to.",
        choices=(
            Choice(
                "Deque with a direction flag", OPTIMAL, time="O(n)", space="O(n)", visual="queue",
                detail="Flip a flag on 'i'; append to the back or front depending on it; reverse once at the end if flipped.",
                why="Reversing then appending is the same as prepending, so a flag replaces every reversal.",
            ),
            Choice(
                "Reverse on every 'i'", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="array-copy",
                detail="Actually reverse the text each time.",
                why="Correct, but many i's mean many full reversals.",
            ),
            Choice(
                "Drop the i's only", INCORRECT, time="O(n)", space="O(n)", visual="brute",
                detail="Remove 'i' characters.",
                why="That gives \"strng\", not \"rtsng\".",
            ),
            Choice(
                "Reverse once if any 'i'", INCORRECT, time="O(n)", space="O(n)", visual="brute",
                detail="Reverse the whole result if the count of i's is odd.",
                why="Characters typed after an 'i' aren't reversed by it.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §5.1 heap basics
    Question(
        slug="last-stone-weight", number=1046, title="Last Stone Weight",
        difficulty="Easy", topics=("data-structures",),
        summary="Repeatedly smash the two heaviest stones: equal ones vanish, otherwise the difference remains. Return the last stone's weight, or 0.",
        example="[2,7,4,1,8,1]  →  1",
        criterion="Which approach is O(n log n)?",
        hint="You need the two largest, again and again, with new values arriving.",
        choices=(
            Choice(
                "Max-heap", OPTIMAL, time="O(n log n)", space="O(n)", visual="heap",
                detail="Pop two, push the difference if non-zero, repeat.",
                why="A heap gives the current maximum in O(log n) even as differences are inserted.",
            ),
            Choice(
                "Re-sort every round", SUBOPTIMAL, time="O(n² log n)", space="O(1)", visual="sort",
                detail="Sort, smash the top two, repeat.",
                why="Correct, but sorts n times.",
            ),
            Choice(
                "Sort once, smash adjacent pairs", INCORRECT, time="O(n log n)", space="O(1)", visual="sort",
                detail="Pair stones in sorted order from the top.",
                why="A difference can become one of the heaviest stones next round.",
            ),
            Choice(
                "Alternating sum of sorted stones", INCORRECT, time="O(n log n)", space="O(1)", visual="math",
                detail="8 − 7 + 4 − 2 + 1 − 1.",
                why="The process doesn't follow a fixed sign pattern.",
            ),
        ),
    ),
    Question(
        slug="final-array-state-after-k-multiplication-operations-i", number=3264, title="Final Array State After K Multiplication Operations I",
        difficulty="Easy", topics=("data-structures",),
        summary="k times, multiply the smallest value (the first one on ties) by multiplier. Return the array.",
        example="nums = [2,1,3,5,6], k = 5, multiplier = 2  →  [8,4,6,5,6]",
        criterion="Which approach is O((n + k) log n)?",
        hint="Ties go to the smaller index. What should the heap compare?",
        choices=(
            Choice(
                "Min-heap of (value, index)", OPTIMAL, time="O((n + k) log n)", space="O(n)", visual="heap",
                detail="Pop the smallest pair, multiply, push it back; write values at the end.",
                why="Comparing (value, index) gives the smallest value with the first index on ties.",
            ),
            Choice(
                "Scan for the minimum each time", SUBOPTIMAL, time="O(n·k)", space="O(1)", visual="brute",
                detail="Find the first smallest by scanning.",
                why="Correct, but linear per step.",
            ),
            Choice(
                "Heap of values only", INCORRECT, time="O((n + k) log n)", space="O(n)", visual="heap",
                detail="Ignore which index a value came from.",
                why="You must update a specific position, the first among equals.",
            ),
            Choice(
                "Multiply the k smallest once", INCORRECT, time="O(n log n)", space="O(n)", visual="sort",
                detail="Sort and multiply the first k.",
                why="A multiplied value can still be the smallest and be picked again.",
            ),
        ),
    ),
    Question(
        slug="take-gifts-from-the-richest-pile", number=2558, title="Take Gifts From the Richest Pile",
        difficulty="Easy", topics=("data-structures",),
        summary="k times, replace the largest pile with the floor of its square root. Return the total left.",
        example="[25,64,9,4,100], k = 4  →  29",
        criterion="Which approach is O(n + k log n)?",
        hint="The largest pile changes every step.",
        choices=(
            Choice(
                "Max-heap", OPTIMAL, time="O(n + k log n)", space="O(n)", visual="heap",
                detail="Heapify, then pop the max and push its root k times.",
                why="The heap always exposes the current richest pile in O(log n).",
            ),
            Choice(
                "Scan for the max", SUBOPTIMAL, time="O(n·k)", space="O(1)", visual="brute",
                detail="Find the largest by scanning each time.",
                why="Correct, but linear per step.",
            ),
            Choice(
                "Square-root the k largest once", INCORRECT, time="O(n log n)", space="O(1)", visual="sort",
                detail="Sort and shrink the top k.",
                why="100 becomes 10, but 10 may still be the largest later.",
            ),
            Choice(
                "Halve instead", INCORRECT, time="O(n + k log n)", space="O(n)", visual="heap",
                detail="Replace the pile with half of it.",
                why="The rule is the square root.",
            ),
        ),
    ),
    Question(
        slug="smallest-number-in-infinite-set", number=2336, title="Smallest Number in Infinite Set",
        difficulty="Medium", topics=("data-structures",),
        summary="Start with all positive integers. popSmallest removes and returns the smallest; addBack(n) puts n back if it was removed.",
        example="addBack 2, popSmallest → 1, popSmallest → 2, popSmallest → 3, addBack 1, popSmallest → 1",
        criterion="Which approach is O(log n) per call?",
        hint="Numbers above some point have never been touched. What about smaller numbers added back?",
        choices=(
            Choice(
                "Counter plus a min-heap of added-back numbers", OPTIMAL, time="O(log n)", space="O(n)", visual="heap",
                detail="cur is the smallest never-popped number; addBack(n) pushes n if n < cur and not already queued (track with a set).",
                why="Everything ≥ cur is present, so only re-added numbers below cur need a heap; the set prevents duplicates.",
            ),
            Choice(
                "Boolean array, scan for the smallest", SUBOPTIMAL, time="O(n) pop", space="O(n)", visual="brute",
                detail="Mark removed numbers and search upward.",
                why="Correct, but popSmallest scans.",
            ),
            Choice(
                "Heap without a dedupe set", INCORRECT, time="O(log n)", space="O(n)", visual="heap",
                detail="Push on every addBack below cur.",
                why="addBack(1) twice would let 1 be popped twice.",
            ),
            Choice(
                "Counter only", INCORRECT, time="O(1)", space="O(1)", visual="counting",
                detail="Return cur++ and ignore addBack.",
                why="addBack 1 must make 1 available again.",
            ),
        ),
    ),
    Question(
        slug="maximal-score-after-applying-k-operations", number=2530, title="Maximal Score After Applying K Operations",
        difficulty="Medium", topics=("data-structures",),
        summary="k times, pick any element, add it to your score, and replace it with ⌈x / 3⌉. Return the maximum score.",
        example="[1,10,3,3,3], k = 3  →  17",
        criterion="Which approach is O(n + k log n)?",
        hint="Taking the largest now never hurts later picks. Why?",
        choices=(
            Choice(
                "Max-heap, take the largest each time", OPTIMAL, time="O(n + k log n)", space="O(n)", visual="heap",
                detail="Pop x, add it, push ⌈x / 3⌉.",
                why="Shrinking the largest leaves the others untouched, and the largest is always the best single gain.",
            ),
            Choice(
                "Scan for the largest", SUBOPTIMAL, time="O(n·k)", space="O(1)", visual="brute",
                detail="Find the max by scanning each time.",
                why="Correct, but linear per step.",
            ),
            Choice(
                "Sum the k largest", INCORRECT, time="O(n log n)", space="O(1)", visual="sort",
                detail="Take each of the top k once.",
                why="10 then becomes 4, which beats a 3. Can it be picked again?",
            ),
            Choice(
                "Floor instead of ceiling", INCORRECT, time="O(n + k log n)", space="O(n)", visual="heap",
                detail="Replace x with x // 3.",
                why="The rule is the ceiling: 10 becomes 4, not 3.",
            ),
        ),
    ),
    Question(
        slug="minimum-operations-to-exceed-threshold-value-ii", number=3066, title="Minimum Operations to Exceed Threshold Value II",
        difficulty="Medium", topics=("data-structures",),
        summary="While some value is below k, remove the two smallest x ≤ y and insert 2x + y. Return the number of operations.",
        example="[2,11,10,1,3], k = 10  →  2",
        criterion="Which approach is O(n log n)?",
        hint="You always need the two smallest of a changing collection.",
        choices=(
            Choice(
                "Min-heap", OPTIMAL, time="O(n log n)", space="O(n)", visual="heap",
                detail="While the top is below k, pop two, push 2x + y (use 64-bit), count.",
                why="Each operation removes one element, and the heap finds the two smallest in O(log n).",
            ),
            Choice(
                "Sort after every operation", SUBOPTIMAL, time="O(n² log n)", space="O(1)", visual="sort",
                detail="Re-sort to find the two smallest.",
                why="Correct, but sorts repeatedly.",
            ),
            Choice(
                "Count values below k", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="One operation per small value.",
                why="One operation removes two values and may create another small one.",
            ),
            Choice(
                "x + 2y", INCORRECT, time="O(n log n)", space="O(n)", visual="heap",
                detail="Insert x + 2y.",
                why="The rule doubles the smaller one.",
            ),
        ),
    ),
    Question(
        slug="remove-stones-to-minimize-the-total", number=1962, title="Remove Stones to Minimize the Total",
        difficulty="Medium", topics=("data-structures",),
        summary="k times, pick a pile and remove ⌊x / 2⌋ stones from it. Return the smallest possible total.",
        example="[5,4,9], k = 2  →  12",
        criterion="Which approach is O(n + k log n)?",
        hint="Which pile loses the most stones?",
        choices=(
            Choice(
                "Max-heap, halve the largest", OPTIMAL, time="O(n + k log n)", space="O(n)", visual="heap",
                detail="Pop x, push x − ⌊x / 2⌋, k times.",
                why="The largest pile gives the biggest single removal, and a heap tracks it as piles shrink.",
            ),
            Choice(
                "Scan for the largest", SUBOPTIMAL, time="O(n·k)", space="O(1)", visual="brute",
                detail="Find the max by scanning each time.",
                why="Correct, but linear per step.",
            ),
            Choice(
                "Halve the k largest once each", INCORRECT, time="O(n log n)", space="O(1)", visual="sort",
                detail="Sort and halve the top k.",
                why="9 becomes 5, which can still be the largest.",
            ),
            Choice(
                "Halve the smallest", INCORRECT, time="O(n + k log n)", space="O(n)", visual="heap",
                detail="Use a min-heap.",
                why="Small piles lose few stones.",
            ),
        ),
    ),
    Question(
        slug="kth-largest-element-in-a-stream", number=703, title="Kth Largest Element in a Stream",
        difficulty="Easy", topics=("data-structures",),
        summary="After each add(val), return the k-th largest value seen so far.",
        example="k = 3, [4,5,8,2]: add 3 → 4, add 5 → 5, add 10 → 5",
        criterion="Which approach is O(log k) per add?",
        hint="Only the k largest values ever matter. Which of them is the answer?",
        choices=(
            Choice(
                "Min-heap of size k", OPTIMAL, time="O(log k)", space="O(k)", visual="heap",
                detail="Push val; if the heap exceeds k, pop the smallest; return the top.",
                why="The heap holds the k largest values, and its minimum is the k-th largest.",
            ),
            Choice(
                "Sorted list with insertion", SUBOPTIMAL, time="O(n) per add", space="O(n)", visual="sort",
                detail="Insert in order and index the k-th from the end.",
                why="Correct, but insertion shifts elements.",
            ),
            Choice(
                "Max-heap of everything", INCORRECT, time="O(log n)", space="O(n)", visual="heap",
                detail="Return the top.",
                why="That's the largest, not the k-th largest.",
            ),
            Choice(
                "Track one variable", INCORRECT, time="O(1)", space="O(1)", visual="greedy",
                detail="Keep the current answer and update it if val is bigger.",
                why="When a bigger value arrives, the new k-th largest is a different stored value.",
            ),
        ),
    ),
    Question(
        slug="k-th-nearest-obstacle-queries", number=3275, title="K-th Nearest Obstacle Queries",
        difficulty="Medium", topics=("data-structures",),
        summary="Obstacles are added at points (x, y) one by one. After each, return the k-th smallest Manhattan distance |x| + |y| to the origin, or −1.",
        example="[[1,2],[3,4],[2,3],[-3,0]], k = 2  →  [-1,7,5,3]",
        criterion="Which approach is O(n log k)?",
        hint="Same as the k-th largest in a stream, but for the k-th smallest.",
        choices=(
            Choice(
                "Max-heap of size k", OPTIMAL, time="O(n log k)", space="O(k)", visual="heap",
                detail="Push each distance; pop the largest when over k; answer the top once k are held.",
                why="The heap holds the k nearest; its maximum is the k-th nearest.",
            ),
            Choice(
                "Sort all distances each time", SUBOPTIMAL, time="O(n² log n)", space="O(n)", visual="sort",
                detail="Re-sort after each insertion.",
                why="Correct, but sorts n times.",
            ),
            Choice(
                "Min-heap of all distances", INCORRECT, time="O(n log n)", space="O(n)", visual="heap",
                detail="Return the top.",
                why="That's the nearest, not the k-th nearest.",
            ),
            Choice(
                "Euclidean distance", INCORRECT, time="O(n log k)", space="O(k)", visual="heap",
                detail="Use √(x² + y²).",
                why="The task uses |x| + |y|.",
            ),
        ),
    ),
    Question(
        slug="seat-reservation-manager", number=1845, title="Seat Reservation Manager",
        difficulty="Medium", topics=("data-structures",),
        summary="Seats 1..n start free. reserve() takes the smallest free seat; unreserve(s) frees seat s.",
        example="n = 5: reserve → 1, reserve → 2, unreserve 2, reserve → 2, reserve → 3",
        criterion="Which approach is O(log n) per call?",
        hint="Which seats need to be in the heap?",
        choices=(
            Choice(
                "Counter plus a min-heap of returned seats", OPTIMAL, time="O(log n)", space="O(n)", visual="heap",
                detail="reserve pops the heap if non-empty, else returns the next never-used seat; unreserve pushes s.",
                why="Seats above the counter are all free, so only returned seats need ordering.",
            ),
            Choice(
                "Scan a boolean array", SUBOPTIMAL, time="O(n) reserve", space="O(n)", visual="brute",
                detail="Find the first free seat by scanning.",
                why="Correct, but reserve is linear.",
            ),
            Choice(
                "Stack of returned seats", INCORRECT, time="O(1)", space="O(n)", visual="stack",
                detail="Hand out the most recently returned seat.",
                why="After unreserving 4 then 2, reserve must give 2, the smallest.",
            ),
            Choice(
                "Counter only", INCORRECT, time="O(1)", space="O(1)", visual="counting",
                detail="Always give the next new seat.",
                why="Unreserved seats must be reused.",
            ),
        ),
    ),
    Question(
        slug="minimum-operations-to-halve-array-sum", number=2208, title="Minimum Operations to Halve Array Sum",
        difficulty="Medium", topics=("data-structures",),
        summary="One operation halves any element (exactly, as a real number). Return the fewest operations to cut the total by at least half.",
        example="[5,19,8,1]  →  3",
        criterion="Which approach is O(n log n)?",
        hint="Halving which element removes the most?",
        choices=(
            Choice(
                "Max-heap, halve the largest", OPTIMAL, time="O(n log n)", space="O(n)", visual="heap",
                detail="Pop x, add x / 2 to the reduction, push x / 2, until the reduction reaches half the sum.",
                why="Halving the largest removes the most each step, and that greedy choice never hurts later ones.",
            ),
            Choice(
                "Scan for the largest", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="Find the max by scanning each step.",
                why="Correct, but linear per step.",
            ),
            Choice(
                "Halve each element once, largest first", INCORRECT, time="O(n log n)", space="O(1)", visual="sort",
                detail="Sort and halve in order without reconsidering.",
                why="19 becomes 9.5, still larger than 8. Should it be halved again?",
            ),
            Choice(
                "Integer halving", INCORRECT, time="O(n log n)", space="O(n)", visual="heap",
                detail="Use x // 2.",
                why="The task uses exact halves; flooring changes the count.",
            ),
        ),
    ),
    Question(
        slug="maximum-product-after-k-increments", number=2233, title="Maximum Product After K Increments",
        difficulty="Medium", topics=("data-structures",),
        summary="k times, increment any element by 1. Return the largest possible product mod 10⁹ + 7.",
        example="[0,4], k = 5  →  20",
        criterion="Which approach is O((n + k) log n)?",
        hint="Adding 1 to which element multiplies the product by the most?",
        choices=(
            Choice(
                "Min-heap, increment the smallest", OPTIMAL, time="O((n + k) log n)", space="O(n)", visual="heap",
                detail="Pop the smallest, add 1, push it back; multiply everything mod p at the end.",
                why="Raising x by 1 multiplies the product by (x + 1)/x, which is largest for the smallest x.",
            ),
            Choice(
                "Scan for the smallest", SUBOPTIMAL, time="O(n·k)", space="O(1)", visual="brute",
                detail="Find the minimum by scanning each step.",
                why="Correct, but linear per step.",
            ),
            Choice(
                "Increment the largest", INCORRECT, time="O((n + k) log n)", space="O(n)", visual="heap",
                detail="Grow the biggest element.",
                why="For [0,4], that leaves a 0 and a product of 0.",
            ),
            Choice(
                "Spread k evenly", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="Add k / n to every element.",
                why="For [0,4] and k = 5, adding 3 and 2 gives 3·6 = 18. Can you do better?",
            ),
        ),
    ),
    Question(
        slug="minimum-number-of-seconds-to-make-mountain-height-zero", number=3296, title="Minimum Number of Seconds to Make Mountain Height Zero",
        difficulty="Medium", topics=("data-structures",),
        summary="Worker i lowers the mountain by x units in t·(1 + 2 + … + x) seconds, where t = workerTimes[i]. Workers work at once. Return the fewest seconds to lower it by mountainHeight.",
        example="mountainHeight = 4, workerTimes = [2,1,1]  →  3",
        criterion="Which approach is O(H log n)?",
        hint="Hand out units one at a time. Which worker should take the next unit?",
        choices=(
            Choice(
                "Min-heap of each worker's finish time after one more unit", OPTIMAL, time="O(H log n)", space="O(n)", visual="heap",
                detail="Pop the worker whose total would be smallest with one more unit, give it the unit, push its next total; the answer is the last total taken.",
                why="Giving each unit to whoever would finish it earliest keeps the slowest worker's total as small as possible.",
            ),
            Choice(
                "Scan all workers per unit", SUBOPTIMAL, time="O(H·n)", space="O(n)", visual="brute",
                detail="For each unit, find the best worker by scanning.",
                why="Correct, but linear per unit.",
            ),
            Choice(
                "Split the height evenly", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="Each worker takes H / n units.",
                why="Faster workers should take more units.",
            ),
            Choice(
                "Give everything to the fastest", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="One worker does all units.",
                why="Costs grow with each unit, so sharing is faster.",
            ),
        ),
    ),
    Question(
        slug="the-number-of-the-smallest-unoccupied-chair", number=1942, title="The Number of the Smallest Unoccupied Chair",
        difficulty="Medium", topics=("data-structures",),
        summary="Friends arrive and leave at distinct times; each sits on the smallest free chair. Return the chair targetFriend sits on.",
        example="times = [[1,4],[2,3],[4,6]], targetFriend = 1  →  1",
        criterion="Which approach is O(n log n)?",
        hint="At each arrival, you need the smallest free chair and to free chairs whose owners have left.",
        choices=(
            Choice(
                "Sort arrivals; heaps of free chairs and of (leave, chair)", OPTIMAL, time="O(n log n)", space="O(n)", visual="heap",
                detail="Before each arrival, release everyone who left by then into the free-chair heap; seat the arrival on the smallest free chair.",
                why="Both 'next to leave' and 'smallest free chair' are minimums of changing sets, which heaps maintain in log time.",
            ),
            Choice(
                "Scan chairs at each arrival", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="brute",
                detail="Mark chairs occupied and search for the first free one.",
                why="Correct, but linear per arrival.",
            ),
            Choice(
                "Chair = arrival rank", INCORRECT, time="O(n log n)", space="O(1)", visual="sort",
                detail="The k-th arriving friend gets chair k − 1.",
                why="Chairs are freed and reused.",
            ),
            Choice(
                "Free chairs after seating", INCORRECT, time="O(n log n)", space="O(n)", visual="heap",
                detail="Seat first, then release those who left at that time.",
                why="Someone leaving at time 4 frees a chair for someone arriving at time 4.",
            ),
        ),
    ),
    Question(
        slug="minimum-cost-to-connect-sticks", number=1167, title="Minimum Cost to Connect Sticks",
        difficulty="Medium", topics=("data-structures",),
        summary="Joining sticks of lengths x and y costs x + y and yields one stick of x + y. Return the cheapest way to join all sticks into one.",
        example="[2,4,3]  →  14",
        criterion="Which approach is O(n log n)?",
        hint="A stick joined early is paid for again in every later join.",
        choices=(
            Choice(
                "Min-heap, join the two shortest", OPTIMAL, time="O(n log n)", space="O(n)", visual="heap",
                detail="Pop the two smallest, add their sum to the cost, push it back.",
                why="This is Huffman's rule: the sticks joined first are counted most often, so they should be the shortest.",
            ),
            Choice(
                "Re-sort after every join", SUBOPTIMAL, time="O(n² log n)", space="O(n)", visual="sort",
                detail="Sort to find the two shortest each time.",
                why="Correct, but sorts repeatedly.",
            ),
            Choice(
                "Join in sorted order left to right", INCORRECT, time="O(n log n)", space="O(1)", visual="sort",
                detail="Add sticks one by one to a growing stick.",
                why="For [1,1,1,1], that costs 2 + 3 + 4 = 9, but pairing first costs 8.",
            ),
            Choice(
                "Sum of lengths", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="Each stick paid once.",
                why="Sticks are paid again every time their bundle is joined.",
            ),
        ),
    ),
    Question(
        slug="meeting-rooms-ii", number=253, title="Meeting Rooms II",
        difficulty="Medium", topics=("data-structures",),
        summary="Return the fewest conference rooms needed for a list of meeting intervals.",
        example="[[0,30],[5,10],[15,20]]  →  2",
        criterion="Which approach is O(n log n)?",
        hint="When a meeting starts, which room is the best one to reuse?",
        choices=(
            Choice(
                "Sort by start, min-heap of end times", OPTIMAL, time="O(n log n)", space="O(n)", visual="heap",
                detail="For each meeting, pop the earliest end if it's ≤ the start; push this meeting's end; answer = heap size.",
                why="The room that frees up earliest is the only one worth checking. The heap's size is the number of rooms in use.",
            ),
            Choice(
                "Check every room per meeting", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="brute",
                detail="Scan existing rooms for one that's free.",
                why="Correct, but linear per meeting.",
            ),
            Choice(
                "Overlaps with the first meeting", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Count meetings overlapping the earliest.",
                why="Overlaps elsewhere can need more rooms.",
            ),
            Choice(
                "Count all overlapping pairs", INCORRECT, time="O(n²)", space="O(1)", visual="brute",
                detail="Rooms = overlapping pairs + 1.",
                why="[5,10] and [15,20] both overlap [0,30] but not each other; 2 rooms suffice.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §5.2 heap, further practice
    Question(
        slug="merge-k-sorted-lists", number=23, title="Merge k Sorted Lists",
        difficulty="Hard", topics=("data-structures",),
        summary="Merge k sorted linked lists into one sorted list.",
        example="[[1,4,5],[1,3,4],[2,6]]  →  [1,1,2,3,4,4,5,6]",
        criterion="Which approach is O(N log k) for N nodes in total?",
        hint="The next output is the smallest of the k current heads.",
        choices=(
            Choice(
                "Min-heap of list heads", OPTIMAL, time="O(N log k)", space="O(k)", visual="heap",
                detail="Pop the smallest head, append it, push its next.",
                why="The heap holds at most k nodes, so each of the N outputs costs log k.",
            ),
            Choice(
                "Merge lists one at a time", SUBOPTIMAL, time="O(N·k)", space="O(1)", visual="linked-list",
                detail="Merge list 1 with list 2, then the result with list 3, and so on.",
                why="Correct, but early nodes are re-walked in every merge.",
            ),
            Choice(
                "Concatenate", INCORRECT, time="O(N)", space="O(1)", visual="linked-list",
                detail="Link the lists end to end.",
                why="The result must be sorted.",
            ),
            Choice(
                "Interleave heads in turn", INCORRECT, time="O(N)", space="O(1)", visual="two-pointers",
                detail="Take one node from each list in rotation.",
                why="Rotation ignores values.",
            ),
        ),
    ),
    Question(
        slug="ipo", number=502, title="IPO",
        difficulty="Hard", topics=("data-structures",),
        summary="Start with capital w and do at most k projects; a project needs capital[i] to start and adds profits[i]. Return the final capital.",
        example="k = 2, w = 0, profits = [1,2,3], capital = [0,1,1]  →  4",
        criterion="Which approach is O(n log n)?",
        hint="Among projects you can afford now, which should you take?",
        choices=(
            Choice(
                "Sort by capital, max-heap of affordable profits", OPTIMAL, time="O(n log n)", space="O(n)", visual="heap",
                detail="Push every newly affordable project's profit; take the largest; repeat k times.",
                why="Profits only increase capital, so taking the best affordable project now unlocks at least as much later.",
            ),
            Choice(
                "Scan for the best affordable project", SUBOPTIMAL, time="O(n·k)", space="O(n)", visual="brute",
                detail="Each round, search all unused projects.",
                why="Correct, but rescans everything each round.",
            ),
            Choice(
                "Highest profits regardless of capital", INCORRECT, time="O(n log n)", space="O(1)", visual="sort",
                detail="Take the k largest profits.",
                why="With w = 0, the profit-3 project costs 1 and can't start first.",
            ),
            Choice(
                "Cheapest projects first", INCORRECT, time="O(n log n)", space="O(1)", visual="sort",
                detail="Take the k lowest capital requirements.",
                why="A cheap project may have tiny profit.",
            ),
        ),
    ),
    Question(
        slug="trapping-rain-water-ii", number=407, title="Trapping Rain Water II",
        difficulty="Hard", topics=("data-structures",),
        summary="Return how much rain water a 2-D elevation map traps.",
        example="[[1,4,3,1,3,2],[3,2,1,3,2,4],[2,3,3,2,3,1]]  →  4",
        criterion="Which approach is O(m·n log(m·n))?",
        hint="Water can only escape over the boundary. Which boundary cell limits its neighbours?",
        choices=(
            Choice(
                "Min-heap from the border inward", OPTIMAL, time="O(m·n log(m·n))", space="O(m·n)", visual="heap",
                detail="Push all border cells; pop the lowest, fill each unvisited neighbour up to that height, push it with max(height, its own).",
                why="The lowest point of the current wall decides the water level just inside it, like Dijkstra on 'lowest escape height'.",
            ),
            Choice(
                "Repeated relaxation until stable", SUBOPTIMAL, time="O((m·n)²)", space="O(m·n)", visual="brute",
                detail="Set each cell's level to max(height, min neighbour level) and repeat.",
                why="Correct when it converges, but may need many sweeps.",
            ),
            Choice(
                "1-D trapping per row and column, take the min", INCORRECT, time="O(m·n)", space="O(m·n)", visual="two-pointers",
                detail="Min of row-wise and column-wise water.",
                why="Water can escape diagonally around obstacles, through paths a row or column can't see.",
            ),
            Choice(
                "Fill to the lowest border height", INCORRECT, time="O(m·n)", space="O(1)", visual="matrix",
                detail="Every cell holds water up to the border's minimum.",
                why="Inner walls can hold water higher than the lowest border.",
            ),
        ),
    ),
    Question(
        slug="lcp-33-water-storage", number=None, title="Water Storage",
        difficulty="Easy", topics=("data-structures",),
        ref="LCP 33", url="https://leetcode.cn/problems/o8SXZn/",
        summary="Each vat i has a bucket of capacity bucket[i] and needs at least vat[i] water. One operation either upgrades one bucket by 1 or fills every vat once with its bucket. Return the fewest operations.",
        example="bucket = [1,3], vat = [6,8]  →  4",
        criterion="Which approach is O(n·V) for vats up to V?",
        hint="Fix the number of fills p. How many upgrades does each bucket then need?",
        choices=(
            Choice(
                "Try every number of fills", OPTIMAL, time="O(n·V)", space="O(1)", visual="brute",
                detail="For p from 1 to max(vat), cost = p + Σ max(0, ⌈vat[i]/p⌉ − bucket[i]); answer the minimum (0 if all vats need 0).",
                why="Once p is fixed, each bucket's needed size is forced, so the total is easy to compute, and p never needs to exceed the largest vat.",
            ),
            Choice(
                "Heap: upgrade the bucket that needs the most fills", SUBOPTIMAL, time="O(V·n log n)", space="O(n)", visual="heap",
                detail="Repeatedly upgrade the bottleneck bucket and track the best total.",
                why="Correct when run long enough, but harder to bound and to get right.",
            ),
            Choice(
                "Never upgrade", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="Fill until every vat is full.",
                why="With bucket 0, you'd never finish.",
            ),
            Choice(
                "Upgrade all buckets to the vat size", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="Make every bucket big enough for one fill.",
                why="Upgrades cost one each. Is one fill really cheapest?",
            ),
        ),
    ),
    Question(
        slug="design-a-file-sharing-system", number=1500, title="Design a File Sharing System",
        difficulty="Medium", topics=("data-structures",),
        summary="Users join with some chunks and get the smallest unused positive id (ids are reused after leave). request(user, chunk) returns the sorted ids of users owning the chunk and gives the chunk to the requester if any owner exists.",
        example="join [1,2] → 1, join [2,3] → 2, join [4] → 3, request(1,3) → [2], request(2,2) → [1,2], leave 1, request(2,1) → []",
        criterion="Which approach gives the smallest free id in O(log n)?",
        hint="Same pattern as Smallest Number in Infinite Set.",
        choices=(
            Choice(
                "Counter plus a min-heap of freed ids; chunk → sorted owner set", OPTIMAL, time="O(log n) join/leave", space="O(n + m)", visual="heap",
                detail="join takes the smallest freed id or the next new one; leave pushes the id back and removes it from its chunks.",
                why="Freed ids are the only ones below the counter, so a heap gives the smallest in log time.",
            ),
            Choice(
                "Scan for the smallest unused id", SUBOPTIMAL, time="O(n) join", space="O(n)", visual="brute",
                detail="Search a used-id set from 1 upward.",
                why="Correct, but join is linear.",
            ),
            Choice(
                "Never reuse ids", INCORRECT, time="O(1)", space="O(1)", visual="counting",
                detail="Hand out increasing ids.",
                why="The last join in the example must get id 1 again.",
            ),
            Choice(
                "Don't transfer requested chunks", INCORRECT, time="O(log n)", space="O(n + m)", visual="hashmap",
                detail="request returns owners but doesn't record the new owner.",
                why="After request(1, 3), user 1 owns chunk 3.",
            ),
        ),
    ),
    Question(
        slug="find-time-required-to-eliminate-bacterial-strains", number=3506, title="Find Time Required to Eliminate Bacterial Strains",
        difficulty="Hard", topics=("data-structures",),
        summary="One white blood cell can split into two in splitTime, and each cell can eliminate one strain taking timeReq[i]. Return the minimum time to eliminate all strains.",
        example="timeReq = [10,4,5], splitTime = 2  →  12",
        criterion="Which approach is O(n log n)?",
        hint="Think of the splits as a binary tree with strains at the leaves. Which two strains should share the deepest split?",
        choices=(
            Choice(
                "Min-heap, merge the two quickest", OPTIMAL, time="O(n log n)", space="O(n)", visual="heap",
                detail="Pop the two smallest a ≤ b, push splitTime + b, until one value remains.",
                why="Like Huffman coding, the fastest strains go deepest; merging them into one 'subtree time' keeps the slowest path minimal.",
            ),
            Choice(
                "Try every split tree", SUBOPTIMAL, time="Exponential", space="O(n)", visual="backtrack",
                detail="Enumerate all binary trees over the strains.",
                why="Correct, but exponential.",
            ),
            Choice(
                "Sum of times", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="One cell does everything.",
                why="Splitting lets cells work in parallel.",
            ),
            Choice(
                "Merge the two slowest first", INCORRECT, time="O(n log n)", space="O(n)", visual="heap",
                detail="Use a max-heap.",
                why="The slowest strain should split off early, not wait behind more splits.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §5.3 k-th smallest
    Question(
        slug="ugly-number-ii", number=264, title="Ugly Number II",
        difficulty="Medium", topics=("data-structures",),
        summary="Ugly numbers have only 2, 3 and 5 as prime factors (1 is ugly). Return the n-th ugly number.",
        example="10  →  12",
        criterion="Which approach is O(n)?",
        hint="Every ugly number is 2, 3 or 5 times a smaller ugly number.",
        choices=(
            Choice(
                "Three pointers merging ×2, ×3, ×5", OPTIMAL, time="O(n)", space="O(n)", visual="dp-1d",
                detail="next = min(u[i2]·2, u[i3]·3, u[i5]·5); advance every pointer that produced it.",
                why="It merges three sorted streams of ugly numbers; advancing all matching pointers removes duplicates like 6.",
            ),
            Choice(
                "Min-heap with a seen set", SUBOPTIMAL, time="O(n log n)", space="O(n)", visual="heap",
                detail="Pop the smallest, push it ×2, ×3, ×5 if new.",
                why="Correct, but each step pays log n.",
            ),
            Choice(
                "Powers of 2, 3 and 5 only", INCORRECT, time="O(n log n)", space="O(n)", visual="math",
                detail="Merge the sequences 2ⁱ, 3ʲ and 5ᵏ.",
                why="6 = 2·3 is ugly. Is it a power of a single prime?",
            ),
            Choice(
                "Advance only one pointer on ties", INCORRECT, time="O(n)", space="O(n)", visual="dp-1d",
                detail="Move just the first pointer that matches.",
                why="6 = 2·3 = 3·2 would be produced twice.",
            ),
        ),
    ),
    Question(
        slug="kth-smallest-element-in-a-sorted-matrix", number=378, title="Kth Smallest Element in a Sorted Matrix",
        difficulty="Medium", topics=("data-structures",),
        summary="Rows and columns of an n×n matrix are sorted. Return the k-th smallest element.",
        example="[[1,5,9],[10,11,13],[12,13,15]], k = 8  →  13",
        criterion="Which approach is O(n log(max − min))?",
        hint="Can you count how many elements are ≤ x in O(n)?",
        choices=(
            Choice(
                "Binary search on value with a staircase count", OPTIMAL, time="O(n log(max − min))", space="O(1)", visual="binary-search",
                detail="Count elements ≤ mid by walking from the bottom-left; find the smallest mid with count ≥ k.",
                why="The count is monotone in x and costs O(n) by the staircase walk, so the value is found in log(range) counts.",
            ),
            Choice(
                "Min-heap over row heads", SUBOPTIMAL, time="O(k log n)", space="O(n)", visual="heap",
                detail="Pop the smallest and push the next in its row, k times.",
                why="Correct, but k can be n², making it O(n² log n).",
            ),
            Choice(
                "Row-major index", INCORRECT, time="O(1)", space="O(1)", visual="matrix",
                detail="Return matrix[(k − 1) / n][(k − 1) % n].",
                why="Rows overlap: 12 in row 2 is smaller than 13 in row 1.",
            ),
            Choice(
                "Diagonal element", INCORRECT, time="O(1)", space="O(1)", visual="matrix",
                detail="Return the element on the anti-diagonal of size k.",
                why="Sorted rows and columns don't fix the order along diagonals.",
            ),
        ),
    ),
    Question(
        slug="find-k-pairs-with-smallest-sums", number=373, title="Find K Pairs with Smallest Sums",
        difficulty="Medium", topics=("data-structures",),
        summary="Given two sorted arrays, return the k pairs (one element from each) with the smallest sums.",
        example="[1,7,11], [2,4,6], k = 3  →  [[1,2],[1,4],[1,6]]",
        criterion="Which approach is O(k log k)?",
        hint="After taking pair (i, j), which pairs become candidates?",
        choices=(
            Choice(
                "Min-heap seeded with (i, 0)", OPTIMAL, time="O(k log k)", space="O(k)", visual="heap",
                detail="Push (i, 0) for the first k values of i; pop the smallest, then push (i, j + 1).",
                why="Each row's pairs are sorted, so only the next pair in the popped row can become the new minimum.",
            ),
            Choice(
                "All pairs, then sort", SUBOPTIMAL, time="O(m·n log(m·n))", space="O(m·n)", visual="sort",
                detail="Build every pair and sort by sum.",
                why="Correct, but builds far more pairs than k.",
            ),
            Choice(
                "Pair nums1[0] with everything", INCORRECT, time="O(k)", space="O(1)", visual="greedy",
                detail="Return (nums1[0], nums2[j]) for j < k.",
                why="For [1,1,2], [1,2,3], k = 2, the second-best pair uses nums1[1].",
            ),
            Choice(
                "Two pointers", INCORRECT, time="O(k)", space="O(1)", visual="two-pointers",
                detail="Advance whichever array's next element is smaller.",
                why="That walks one path through the grid of pairs and misses others with small sums.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §5.4 rearranging
    Question(
        slug="string-without-aaa-or-bbb", number=984, title="String Without AAA or BBB",
        difficulty="Medium", topics=("data-structures",),
        summary="Return any string with a letters 'a' and b letters 'b' and no \"aaa\" or \"bbb\" (one always exists).",
        example="a = 4, b = 1  →  \"aabaa\"",
        criterion="Which approach is linear?",
        hint="Which letter should you write next, and when are you forced to switch?",
        choices=(
            Choice(
                "Write the more plentiful letter unless it would make three", OPTIMAL, time="O(a + b)", space="O(1)", visual="greedy",
                detail="Prefer the letter with more remaining; switch if the last two characters are already that letter.",
                why="Spending the majority letter early keeps the counts balanced enough that a valid string never gets stuck.",
            ),
            Choice(
                "Backtracking", SUBOPTIMAL, time="Exponential worst", space="O(a + b)", visual="backtrack",
                detail="Try letters and undo on violations.",
                why="Correct, but unnecessary: greedy never needs to undo.",
            ),
            Choice(
                "Alternate until one runs out", INCORRECT, time="O(a + b)", space="O(1)", visual="two-pointers",
                detail="Write \"abab…\" then the leftovers.",
                why="For a = 4, b = 1, that ends in \"aaa\".",
            ),
            Choice(
                "All a's then all b's", INCORRECT, time="O(a + b)", space="O(1)", visual="brute",
                detail="Write each letter in one run.",
                why="Runs of three or more appear.",
            ),
        ),
    ),
    Question(
        slug="reorganize-string", number=767, title="Reorganize String",
        difficulty="Medium", topics=("data-structures",),
        summary="Rearrange s so no two adjacent characters are equal, or return \"\" if impossible.",
        example="\"aab\"  →  \"aba\"",
        criterion="Which approach is linear?",
        hint="If the most frequent letter fits at every other position, can the rest always be placed?",
        choices=(
            Choice(
                "Fill even indices with the most frequent letter first", OPTIMAL, time="O(n)", space="O(Σ)", visual="counting",
                detail="Fail if the top count exceeds ⌈n/2⌉; place the top letter at 0, 2, 4, …, then continue with the others, wrapping to odd indices.",
                why="Same letters land two apart, and wrapping from even to odd never puts a letter next to itself when no count exceeds ⌈n/2⌉.",
            ),
            Choice(
                "Max-heap, place the two most frequent each round", SUBOPTIMAL, time="O(n log Σ)", space="O(Σ)", visual="heap",
                detail="Pop two letters, append both, push them back with reduced counts.",
                why="Correct, but pays a heap operation per character.",
            ),
            Choice(
                "Sort and interleave halves", INCORRECT, time="O(n log n)", space="O(n)", visual="sort",
                detail="Merge the first and second half of the sorted string alternately.",
                why="For \"aabbbc\", halves \"aab\" and \"bbc\" give \"ababbc\". Is that valid?",
            ),
            Choice(
                "Swap equal neighbours", INCORRECT, time="O(n²)", space="O(1)", visual="brute",
                detail="Repeatedly swap a repeated character with the next different one.",
                why="It can fail or loop when one letter dominates.",
            ),
        ),
    ),
    Question(
        slug="task-scheduler", number=621, title="Task Scheduler",
        difficulty="Medium", topics=("data-structures",),
        summary="Tasks take one interval each; two equal tasks must be at least n intervals apart (idle allowed). Return the fewest intervals.",
        example="[\"A\",\"A\",\"A\",\"B\",\"B\",\"B\"], n = 2  →  8",
        criterion="Which approach is linear?",
        hint="The most frequent task forces a frame. How big is it, and what fills the gaps?",
        choices=(
            Choice(
                "Frame formula", OPTIMAL, time="O(n_tasks)", space="O(26)", visual="math",
                detail="max(len(tasks), (maxCount − 1)·(n + 1) + number of tasks with maxCount).",
                why="The most frequent task needs maxCount − 1 full gaps of n + 1 slots plus a final row; other tasks fill gaps, and if they overflow there's no idling at all.",
            ),
            Choice(
                "Simulate with a heap and cooldown queue", SUBOPTIMAL, time="O(T·log 26)", space="O(26)", visual="heap",
                detail="Each interval run the most frequent available task.",
                why="Correct, but simulates every interval.",
            ),
            Choice(
                "Tasks plus n idles per repeat", INCORRECT, time="O(n_tasks)", space="O(26)", visual="counting",
                detail="Add n idle slots between each pair of equal tasks.",
                why="Other tasks can fill those slots.",
            ),
            Choice(
                "(maxCount − 1)·(n + 1) + 1", INCORRECT, time="O(n_tasks)", space="O(26)", visual="math",
                detail="Ignore ties and the task total.",
                why="With A and B both 3 times, the last row needs 2 slots, giving 8, not 7.",
            ),
        ),
    ),
    Question(
        slug="rearrange-string-k-distance-apart", number=358, title="Rearrange String k Distance Apart",
        difficulty="Hard", topics=("data-structures",),
        summary="Rearrange s so equal characters are at least k apart, or return \"\".",
        example="\"aabbcc\", k = 3  →  \"abcabc\"",
        criterion="Which approach is O(n log Σ)?",
        hint="At each position, place the most frequent letter that isn't cooling down.",
        choices=(
            Choice(
                "Max-heap plus a cooldown queue", OPTIMAL, time="O(n log Σ)", space="O(Σ)", visual="heap",
                detail="Pop the most frequent letter, append it, park it in a queue; once the queue holds k letters, return the front to the heap.",
                why="Using the most frequent available letter keeps future choices open, and the queue enforces the distance.",
            ),
            Choice(
                "Scan all letters at each position", SUBOPTIMAL, time="O(n·Σ)", space="O(Σ)", visual="brute",
                detail="Pick the most frequent letter whose last use is ≥ k ago.",
                why="Correct, but scans the alphabet per position.",
            ),
            Choice(
                "Round-robin by frequency", INCORRECT, time="O(n log Σ)", space="O(Σ)", visual="sort",
                detail="Cycle through letters sorted by count, without checking distance.",
                why="When fewer than k letters remain, the cycle repeats a letter too soon.",
            ),
            Choice(
                "Reorganize for k = 2", INCORRECT, time="O(n)", space="O(Σ)", visual="counting",
                detail="Only prevent adjacent repeats.",
                why="\"abab\" has no adjacent repeats but a's are 2 apart, not 3.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §5.5 regret heap
    Question(
        slug="lcp-30-magic-tower", number=None, title="Magic Tower",
        difficulty="Medium", topics=("data-structures",),
        ref="LCP 30", url="https://leetcode.cn/problems/p0NxJO/",
        summary="Visit rooms in order starting with 1 HP; nums[i] adds or removes HP, which must stay positive. One adjustment moves a monster room to the end. Return the fewest adjustments, or −1.",
        example="[100,100,100,-250,-60,-140,-50,-50,100,150]  →  1",
        criterion="Which approach is O(n log n)?",
        hint="When HP is about to drop to zero, which monster seen so far is best to postpone?",
        choices=(
            Choice(
                "Min-heap of monsters, postpone the worst", OPTIMAL, time="O(n log n)", space="O(n)", visual="heap",
                detail="Return −1 if 1 + total ≤ 0; walk rooms, push each negative; when HP ≤ 0, pop the most negative, add it back to HP and count it.",
                why="Postponing the strongest monster restores the most HP for one move. Moved rooms still count at the end, which the total check covers.",
            ),
            Choice(
                "Try postponing each monster", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="brute",
                detail="When stuck, test each earlier monster as the one to move.",
                why="Correct, but rescans per failure.",
            ),
            Choice(
                "Postpone the monster that kills you", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Move the current room when HP drops.",
                why="An earlier, stronger monster gives back more HP.",
            ),
            Choice(
                "Skip the final total check", INCORRECT, time="O(n log n)", space="O(n)", visual="heap",
                detail="Assume postponing always works.",
                why="Postponed monsters still have to be fought at the end.",
            ),
        ),
    ),
    Question(
        slug="course-schedule-iii", number=630, title="Course Schedule III",
        difficulty="Hard", topics=("data-structures",),
        summary="Course i takes duration[i] days and must finish by lastDay[i]; courses run one at a time from day 1. Return the most courses you can take.",
        example="[[100,200],[200,1300],[1000,1250],[2000,3200]]  →  3",
        criterion="Which approach is O(n log n)?",
        hint="Take courses by deadline. If one doesn't fit, could swapping out a longer one help?",
        choices=(
            Choice(
                "Sort by deadline, max-heap of durations", OPTIMAL, time="O(n log n)", space="O(n)", visual="heap",
                detail="Add each course; if time exceeds its deadline, drop the longest course taken so far.",
                why="Dropping the longest keeps the count and frees the most time, which only helps later courses.",
            ),
            Choice(
                "DP over courses and time", SUBOPTIMAL, time="O(n·D)", space="O(D)", visual="dp-1d",
                detail="Knapsack on total days used.",
                why="Correct, but deadlines up to 10⁴ times n courses is much slower.",
            ),
            Choice(
                "Shortest courses first", INCORRECT, time="O(n log n)", space="O(1)", visual="sort",
                detail="Take courses by duration.",
                why="A short course with an early deadline might not wait.",
            ),
            Choice(
                "By deadline, skip what doesn't fit", INCORRECT, time="O(n log n)", space="O(1)", visual="greedy",
                detail="Never swap out a course.",
                why="A long early course can block two shorter later ones.",
            ),
        ),
    ),
    Question(
        slug="maximum-transactions-without-negative-balance", number=3711, title="Maximum Transactions Without Negative Balance",
        difficulty="Medium", topics=("data-structures",),
        summary="Process transactions in order from balance 0, skipping any you like; the balance must never go negative. Return the most transactions you can perform.",
        example="[2,-5,3,-1,-2]  →  4",
        criterion="Which approach is O(n log n)?",
        hint="Take everything; when the balance dips below 0, which taken transaction is best to undo?",
        choices=(
            Choice(
                "Min-heap of taken withdrawals, drop the largest", OPTIMAL, time="O(n log n)", space="O(n)", visual="heap",
                detail="Take each transaction; push negatives; if the balance goes negative, pop the most negative and add it back.",
                why="Undoing one transaction is unavoidable then, and undoing the biggest withdrawal restores the most balance for future steps.",
            ),
            Choice(
                "DP over index and count", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="dp-2d",
                detail="Best balance for each number of transactions taken.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Skip the transaction that goes negative", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Only skip the current one.",
                why="An earlier, larger withdrawal may be the better one to skip.",
            ),
            Choice(
                "Skip all withdrawals", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Count positives only.",
                why="Small withdrawals are affordable.",
            ),
        ),
    ),
    Question(
        slug="make-the-prefix-sum-non-negative", number=2599, title="Make the Prefix Sum Non-negative",
        difficulty="Medium", topics=("data-structures",),
        summary="One operation moves any element to the end. Return the fewest operations so that no prefix sum is negative (always possible).",
        example="[3,-5,-2,6]  →  1",
        criterion="Which approach is O(n log n)?",
        hint="It's Magic Tower again with a starting value of 0.",
        choices=(
            Choice(
                "Min-heap, move the most negative when stuck", OPTIMAL, time="O(n log n)", space="O(n)", visual="heap",
                detail="Walk the array; push negatives; when the prefix goes below 0, pop the most negative, add it back, count one move.",
                why="Each move is forced at that point, and moving the largest negative fixes the prefix the most.",
            ),
            Choice(
                "Try every element to move", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="When stuck, test each earlier negative.",
                why="Correct, but quadratic.",
            ),
            Choice(
                "Move the current element", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Postpone whichever element made the prefix negative.",
                why="An earlier larger negative may fix more.",
            ),
            Choice(
                "Count negatives", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Move every negative element.",
                why="In example 1, −5 is fine where it is.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §5.7 two heaps
    Question(
        slug="find-median-from-data-stream", number=295, title="Find Median from Data Stream",
        difficulty="Hard", topics=("data-structures",),
        summary="Support addNum and findMedian over a stream of integers.",
        example="add 1, add 2 → median 1.5; add 3 → median 2",
        criterion="Which approach is O(log n) add and O(1) median?",
        hint="Split the numbers into a lower and an upper half.",
        choices=(
            Choice(
                "Max-heap of the low half, min-heap of the high half", OPTIMAL, time="O(log n) add, O(1) median", space="O(n)", visual="heap",
                detail="Insert into one heap, move its top to the other, rebalance sizes; the median comes from the tops.",
                why="The two tops are the middle elements, and each add moves at most one element between heaps.",
            ),
            Choice(
                "Sorted list with insertion", SUBOPTIMAL, time="O(n) add", space="O(n)", visual="sort",
                detail="Insert in order; read the middle.",
                why="Correct, but insertion shifts elements.",
            ),
            Choice(
                "Running mean", INCORRECT, time="O(1)", space="O(1)", visual="counting",
                detail="Return sum / count.",
                why="For [1,2,10], the mean is 4.33 but the median is 2.",
            ),
            Choice(
                "Heaps without rebalancing", INCORRECT, time="O(log n)", space="O(n)", visual="heap",
                detail="Send each number to a heap by comparison only.",
                why="If the heaps' sizes drift apart, their tops aren't the middle.",
            ),
        ),
    ),
    Question(
        slug="sliding-window-median", number=480, title="Sliding Window Median",
        difficulty="Hard", topics=("data-structures",),
        summary="Return the median of each window of size k as it slides across nums.",
        example="[1,3,-1,-3,5,3,6,7], k = 3  →  [1,-1,-1,3,5,6]",
        criterion="Which approach is O(n log k)?",
        hint="Two heaps work for adding. How do you remove the element that leaves?",
        choices=(
            Choice(
                "Two heaps with lazy deletion", OPTIMAL, time="O(n log k)", space="O(k)", visual="heap",
                detail="Mark leaving elements in a map; rebalance by valid sizes; discard marked tops when they surface.",
                why="Lazy deletion avoids removing from a heap's middle; marked elements are dropped when they reach the top.",
            ),
            Choice(
                "Sort each window", SUBOPTIMAL, time="O(n·k log k)", space="O(k)", visual="sort",
                detail="Copy and sort, then read the middle.",
                why="Correct, but re-sorts k elements per slide.",
            ),
            Choice(
                "Median of medians of neighbours", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Use the middle element of the window in index order.",
                why="The window isn't sorted.",
            ),
            Choice(
                "Running mean", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Average the window.",
                why="The median isn't the mean.",
            ),
        ),
    ),
    Question(
        slug="lcp-24-number-game", number=None, title="Number Game",
        difficulty="Hard", topics=("data-structures",),
        ref="LCP 24", url="https://leetcode.cn/problems/5TxKeK/",
        summary="For each prefix nums[0..i], return (mod 10⁹ + 7) the fewest ±1 operations to make it an increasing run with step 1 (a, a + 1, …, a + i).",
        example="[3,4,5,1,6,7]  →  [0,0,0,5,6,7]",
        criterion="Which approach is O(n log n)?",
        hint="Subtract each index: nums[j] − j must all become equal. What's the best common value?",
        choices=(
            Choice(
                "Two heaps tracking the median and sums of b[j] = nums[j] − j", OPTIMAL, time="O(n log n)", space="O(n)", visual="heap",
                detail="Insert each b[j]; cost = median·|low| − sumLow + sumHigh − median·|high|.",
                why="Making all b[j] equal costs least at their median, and two heaps keep the median and half-sums as the prefix grows.",
            ),
            Choice(
                "Sort each prefix", SUBOPTIMAL, time="O(n² log n)", space="O(n)", visual="sort",
                detail="Recompute the median and distance sum per prefix.",
                why="Correct, but re-sorts every prefix.",
            ),
            Choice(
                "Use nums[j] directly", INCORRECT, time="O(n log n)", space="O(n)", visual="heap",
                detail="Make all prefix values equal to their median.",
                why="The target is a step-1 run, not a constant.",
            ),
            Choice(
                "Use the mean", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="Move everything to the average of b.",
                why="Sum of distances is minimized by the median, not the mean.",
            ),
        ),
    ),
    Question(
        slug="design-an-array-statistics-tracker", number=3369, title="Design an Array Statistics Tracker",
        difficulty="Hard", topics=("data-structures",),
        summary="Support addNumber, removeFirstAddedNumber, getMean (floored), getMedian (the larger middle on ties) and getMode (the smallest on ties).",
        example="add 4, 4, 2, 3 → mean 3, median 4, mode 4; remove first → mode 2",
        criterion="Which approach makes every call O(log n)?",
        hint="Removal is by arrival order, but median and mode need value order. Which structures cover each?",
        choices=(
            Choice(
                "Queue + sum; two lazy heaps for the median; counts with a sorted (−freq, value) set for the mode", OPTIMAL, time="O(log n)", space="O(n)", visual="heap",
                detail="The queue says what to remove; the running sum gives the mean; heaps with lazy deletion give the median; re-keying one count updates the mode.",
                why="Each statistic gets a structure that updates in log time when one value enters or leaves.",
            ),
            Choice(
                "Sort the contents on each query", SUBOPTIMAL, time="O(n log n) per query", space="O(n)", visual="sort",
                detail="Compute median and mode from a sorted copy.",
                why="Correct, but every query re-sorts.",
            ),
            Choice(
                "Remove the smallest instead of the oldest", INCORRECT, time="O(log n)", space="O(n)", visual="heap",
                detail="Pop the min-heap on removeFirstAddedNumber.",
                why="The first added number isn't necessarily the smallest.",
            ),
            Choice(
                "Lower middle for the median", INCORRECT, time="O(log n)", space="O(n)", visual="heap",
                detail="Return the smaller of two middles.",
                why="For [2,3,4,4] the rule wants 4.",
            ),
        ),
    ),
]
