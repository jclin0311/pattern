"""Core route step 2: binary search (二分算法 §1)."""

from .question_schema import INCORRECT, OPTIMAL, SUBOPTIMAL, Choice, Question

QUESTIONS = [
    # ---------------------------------------------------------------- §1.1 basics
    Question(
        slug="find-first-and-last-position-of-element-in-sorted-array", number=34, title="Find First and Last Position of Element in Sorted Array",
        difficulty="Medium", topics=("binary-search",),
        summary="In a sorted array, return the first and last index of target, or [−1, −1].",
        example="[5,7,7,8,8,10], 8  →  [3, 4]",
        criterion="Which approach is O(log n) even when target repeats many times?",
        hint="The first index of target is the first position with a value ≥ target. What's the last index in those terms?",
        choices=(
            Choice(
                "Two lower-bound searches", OPTIMAL, time="O(log n)", space="O(1)", visual="binary-search",
                detail="start = lower_bound(target); end = lower_bound(target + 1) − 1; check nums[start] == target.",
                why="Both answers are boundaries in a sorted array, and each boundary is one binary search, however many copies there are.",
            ),
            Choice(
                "Find one copy, then expand", SUBOPTIMAL, time="O(log n + k)", space="O(1)", visual="two-pointers",
                detail="Binary search any copy, then walk left and right while values equal target.",
                why="Correct, but an array of a million 8s walks a million steps.",
            ),
            Choice(
                "Report the hit twice", INCORRECT, time="O(log n)", space="O(1)", visual="binary-search",
                detail="Return [i, i] for whichever copy the search lands on.",
                why="The search might land on index 3 or 4. Is [3, 3] the answer?",
            ),
            Choice(
                "End at lower_bound(target + 1)", INCORRECT, time="O(log n)", space="O(1)", visual="binary-search",
                detail="Use the first position ≥ target + 1 as the last index.",
                why="That's index 5, the 10. Which index holds the last 8?",
            ),
        ),
    ),
    Question(
        slug="search-insert-position", number=35, title="Search Insert Position",
        difficulty="Easy", topics=("binary-search",),
        summary="In a sorted array of distinct integers, return target's index, or the index where it would be inserted.",
        example="[1,3,5,6], 2  →  1",
        criterion="Which approach is O(log n)?",
        hint="Both cases are the same question: where is the first value ≥ target?",
        choices=(
            Choice(
                "Lower bound", OPTIMAL, time="O(log n)", space="O(1)", visual="binary-search",
                detail="Binary search the first index whose value ≥ target; return it (n if none).",
                why="If target is present, that's its index; otherwise it's where target would go. One boundary covers both.",
            ),
            Choice(
                "Scan from the left", SUBOPTIMAL, time="O(n)", space="O(1)", visual="brute",
                detail="Return the first index with value ≥ target.",
                why="Correct, but ignores that the array is sorted.",
            ),
            Choice(
                "Upper bound", INCORRECT, time="O(log n)", space="O(1)", visual="binary-search",
                detail="Return the first index with value > target.",
                why="For target 5 that returns 3. Where is 5?",
            ),
            Choice(
                "Return mid when the loop ends", INCORRECT, time="O(log n)", space="O(1)", visual="binary-search",
                detail="Run a standard search and return the last mid checked.",
                why="For target 7, the last mid is 3 (the 6). Should 7 go before 6?",
            ),
        ),
    ),
    Question(
        slug="binary-search", number=704, title="Binary Search",
        difficulty="Easy", topics=("binary-search",),
        summary="Return the index of target in a sorted array of distinct integers, or −1.",
        example="[-1,0,3,5,9,12], 9  →  4",
        criterion="Which approach is O(log n) and terminates on every input?",
        hint="With a closed interval [left, right], when should the loop stop, and how must each side move?",
        choices=(
            Choice(
                "Closed interval, move past mid", OPTIMAL, time="O(log n)", space="O(1)", visual="binary-search",
                detail="While left ≤ right: compare nums[mid]; set left = mid + 1 or right = mid − 1.",
                why="Each step discards mid and one side, so the interval shrinks every time and a one-element interval is still checked.",
            ),
            Choice(
                "Linear scan", SUBOPTIMAL, time="O(n)", space="O(1)", visual="brute",
                detail="Check each element.",
                why="Correct, but ignores the sorted order.",
            ),
            Choice(
                "Loop while left < right", INCORRECT, time="O(log n)", space="O(1)", visual="binary-search",
                detail="Same updates, but stop when left equals right.",
                why="For [5] and target 5, does the loop run at all?",
            ),
            Choice(
                "Set left = mid", INCORRECT, time="O(log n)", space="O(1)", visual="binary-search",
                detail="When nums[mid] < target, move left to mid.",
                why="With left = 0, right = 1, mid stays 0. Does the interval shrink?",
            ),
        ),
    ),
    Question(
        slug="find-smallest-letter-greater-than-target", number=744, title="Find Smallest Letter Greater Than Target",
        difficulty="Easy", topics=("binary-search",),
        summary="Letters are sorted. Return the smallest letter strictly greater than target, wrapping to letters[0] if none.",
        example="[\"c\",\"f\",\"j\"], \"c\"  →  \"f\"",
        criterion="Which approach is O(log n)?",
        hint="'Strictly greater' is which bound?",
        choices=(
            Choice(
                "Upper bound with wrap", OPTIMAL, time="O(log n)", space="O(1)", visual="binary-search",
                detail="Find the first index with letter > target; return letters[i % n].",
                why="The first strictly greater letter is a boundary. If it's past the end, the wrap rule gives letters[0].",
            ),
            Choice(
                "Scan from the left", SUBOPTIMAL, time="O(n)", space="O(1)", visual="brute",
                detail="Return the first letter > target, else letters[0].",
                why="Correct, but linear in a sorted array.",
            ),
            Choice(
                "Lower bound", INCORRECT, time="O(log n)", space="O(1)", visual="binary-search",
                detail="Find the first letter ≥ target.",
                why="For target \"c\", that's \"c\" itself. Is it strictly greater?",
            ),
            Choice(
                "Upper bound, no wrap", INCORRECT, time="O(log n)", space="O(1)", visual="binary-search",
                detail="Return letters[i] directly.",
                why="For target \"z\", i = n. What's at letters[n]?",
            ),
        ),
    ),
    Question(
        slug="maximum-count-of-positive-integer-and-negative-integer", number=2529, title="Maximum Count of Positive Integer and Negative Integer",
        difficulty="Easy", topics=("binary-search",),
        summary="In a sorted array, return max(number of negatives, number of positives). Zero is neither.",
        example="[-3,-2,-1,0,0,1,2]  →  3",
        criterion="Which approach is O(log n)?",
        hint="Negatives end where values reach 0; positives start where values pass 0.",
        choices=(
            Choice(
                "Two boundaries around 0", OPTIMAL, time="O(log n)", space="O(1)", visual="binary-search",
                detail="neg = lower_bound(0); pos = n − upper_bound(0); return the max.",
                why="Sorted order puts negatives, zeros and positives in three blocks. Two searches find the block edges.",
            ),
            Choice(
                "Count in one pass", SUBOPTIMAL, time="O(n)", space="O(1)", visual="counting",
                detail="Tally signs element by element.",
                why="Correct, but doesn't use the sorted order.",
            ),
            Choice(
                "Count zeros as positive", INCORRECT, time="O(log n)", space="O(1)", visual="binary-search",
                detail="pos = n − lower_bound(0).",
                why="In the example, that counts 4 positives. How many are there?",
            ),
            Choice(
                "Split at one search for 0", INCORRECT, time="O(log n)", space="O(1)", visual="binary-search",
                detail="Find any 0 at index i; negatives = i, positives = n − i − 1.",
                why="With two zeros, which index do you land on, and where does the other zero go?",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §1.2 further practice
    Question(
        slug="find-the-distance-value-between-two-arrays", number=1385, title="Find the Distance Value Between Two Arrays",
        difficulty="Easy", topics=("binary-search",),
        summary="Count elements x of arr1 such that no element of arr2 lies within d of x.",
        example="arr1 = [4,5,8], arr2 = [10,9,1,8], d = 2  →  2",
        criterion="Which approach is O((n + m) log m)?",
        hint="After sorting arr2, which single element decides whether anything lies in [x − d, x + d]?",
        choices=(
            Choice(
                "Sort arr2, lower bound of x − d", OPTIMAL, time="O((n + m) log m)", space="O(1)", visual="binary-search",
                detail="For each x, find the first arr2 value ≥ x − d and check that it's > x + d (or absent).",
                why="If any value lies in the range, the smallest value ≥ x − d does. One search per x.",
            ),
            Choice(
                "Compare every pair", SUBOPTIMAL, time="O(n·m)", space="O(1)", visual="brute",
                detail="For each x, check every element of arr2.",
                why="Correct, but rechecks all of arr2 for every x.",
            ),
            Choice(
                "Compare with arr2's min and max", INCORRECT, time="O(n + m)", space="O(1)", visual="math",
                detail="Count x farther than d from both min(arr2) and max(arr2).",
                why="8 is far from 1 and 10 but equals an 8 in arr2. Is it counted?",
            ),
            Choice(
                "Compare index by index", INCORRECT, time="O(n)", space="O(1)", visual="two-pointers",
                detail="Check |arr1[i] − arr2[i]| > d.",
                why="Every element of arr2 matters, not just the one at the same index.",
            ),
        ),
    ),
    Question(
        slug="compare-strings-by-frequency-of-the-smallest-character", number=1170, title="Compare Strings by Frequency of the Smallest Character",
        difficulty="Medium", topics=("binary-search",),
        summary="f(s) is how often s's smallest letter appears. For each query q, count words w with f(q) < f(w). Words have at most 10 letters.",
        example="queries = [\"cbd\"], words = [\"zaaaz\"]  →  [1]",
        criterion="Which approach is O(n + q) after computing f?",
        hint="f(w) is between 1 and 10. Do you even need to sort?",
        choices=(
            Choice(
                "Suffix counts over f values", OPTIMAL, time="O(n + q)", space="O(1)", visual="prefix",
                detail="Count words by f (1–10), build suffix sums, and answer each query as suffix[f(q) + 1].",
                why="With only 10 possible values, a counting table replaces the sort and answers each query in O(1).",
            ),
            Choice(
                "Sort f(words), binary search", SUBOPTIMAL, time="O((n + q) log n)", space="O(n)", visual="binary-search",
                detail="Sort the f values and upper-bound f(q) for each query.",
                why="Correct and the classic approach, but the small value range makes the log factor unnecessary.",
            ),
            Choice(
                "Use the most frequent letter", INCORRECT, time="O(n + q)", space="O(1)", visual="counting",
                detail="f = count of the most common letter.",
                why="\"zaaaz\" has smallest letter a, appearing 3 times. Is that what's defined?",
            ),
            Choice(
                "Count f(w) ≥ f(q)", INCORRECT, time="O(n + q)", space="O(1)", visual="prefix",
                detail="Include ties.",
                why="The condition is strict. Should a word with equal f count?",
            ),
        ),
    ),
    Question(
        slug="successful-pairs-of-spells-and-potions", number=2300, title="Successful Pairs of Spells and Potions",
        difficulty="Medium", topics=("binary-search",),
        summary="A spell and potion pair succeeds if their product is at least success. For each spell, count successful potions.",
        example="spells = [5,1,3], potions = [1,2,3,4,5], success = 7  →  [4,0,3]",
        criterion="Which approach is O((n + m) log m)?",
        hint="For a fixed spell s, what's the weakest potion that works?",
        choices=(
            Choice(
                "Sort potions, lower bound of ⌈success / s⌉", OPTIMAL, time="O((n + m) log m)", space="O(1)", visual="binary-search",
                detail="For each spell, find the first potion ≥ ⌈success / s⌉; count the rest.",
                why="Products grow with the potion, so successful potions form a suffix of the sorted list. Its start is one binary search.",
            ),
            Choice(
                "Try every pair", SUBOPTIMAL, time="O(n·m)", space="O(1)", visual="brute",
                detail="Multiply each spell by each potion.",
                why="Correct, but 10⁵ × 10⁵ products.",
            ),
            Choice(
                "Floor division threshold", INCORRECT, time="O((n + m) log m)", space="O(1)", visual="binary-search",
                detail="Search for success // s.",
                why="Spell 5 needs 7: 7 // 5 = 1, but 5 × 1 = 5 < 7. Does potion 1 succeed?",
            ),
            Choice(
                "Two pointers over unsorted potions", INCORRECT, time="O(n + m)", space="O(1)", visual="two-pointers",
                detail="Walk spells and potions together in input order.",
                why="Without sorting, successful potions aren't contiguous. What would the pointer mean?",
            ),
        ),
    ),
    Question(
        slug="longest-subsequence-with-limited-sum", number=2389, title="Longest Subsequence With Limited Sum",
        difficulty="Easy", topics=("binary-search",),
        summary="For each query, return the size of the largest subsequence of nums whose sum is ≤ the query.",
        example="nums = [4,5,2,1], queries = [3,10,21]  →  [2,3,4]",
        criterion="Which approach is O((n + q) log n)?",
        hint="To fit the most elements under a budget, which elements should you take?",
        choices=(
            Choice(
                "Sort, prefix sums, upper bound", OPTIMAL, time="O((n + q) log n)", space="O(n)", visual="binary-search",
                detail="Sort nums, build prefix sums, and for each query count prefixes ≤ query.",
                why="The smallest elements give the longest subsequence. Prefix sums of the sorted array are increasing, so each query is one search.",
            ),
            Choice(
                "Greedy per query", SUBOPTIMAL, time="O(n log n + n·q)", space="O(1)", visual="greedy",
                detail="Sort once, then add smallest elements for each query until over budget.",
                why="Correct, but every query re-adds the same prefix.",
            ),
            Choice(
                "Prefix sums in original order", INCORRECT, time="O(n + q log n)", space="O(n)", visual="prefix",
                detail="Search the unsorted prefix sums.",
                why="A subsequence can skip elements. For query 3, can you take 2 and 1 without the 4?",
            ),
            Choice(
                "Largest elements first", INCORRECT, time="O((n + q) log n)", space="O(n)", visual="sort",
                detail="Sort descending and take while the sum fits.",
                why="Big elements use the budget fastest. Is that how you get the most elements?",
            ),
        ),
    ),
    Question(
        slug="closest-equal-element-queries", number=3488, title="Closest Equal Element Queries",
        difficulty="Medium", topics=("binary-search",),
        summary="In a circular array, for each queried index i, return the smallest circular distance to another index with the same value, or −1.",
        example="nums = [1,3,1,4,1,3,2], queries = [0,3,5]  →  [2,-1,3]",
        criterion="Which approach is O(n + q)?",
        hint="Group indices by value. In a circle, which members of i's group can be closest?",
        choices=(
            Choice(
                "Precompute from each index's neighbours in its group", OPTIMAL, time="O(n + q)", space="O(n)", visual="hashmap",
                detail="List indices per value (already sorted); for each index, compare its previous and next in the list, wrapping around; answer queries by lookup.",
                why="Within a sorted group, the closest index is an adjacent one on the circle. That's O(1) per index, so all answers cost O(n).",
            ),
            Choice(
                "Group lists, binary search per query", SUBOPTIMAL, time="O(n + q log n)", space="O(n)", visual="binary-search",
                detail="Find i's position in its value's list and check the neighbours with wrap.",
                why="Correct, but the position could be stored when the lists are built.",
            ),
            Choice(
                "Ignore the wrap", INCORRECT, time="O(n + q)", space="O(n)", visual="hashmap",
                detail="Use only the linear distance to the previous and next copy.",
                why="Index 5 and index 1 are 3 apart around the circle but 4 apart in a line.",
            ),
            Choice(
                "Only the next copy", INCORRECT, time="O(n + q)", space="O(n)", visual="hashmap",
                detail="Measure to the next index with the same value.",
                why="The closest copy might be behind you. What about index 4's 1?",
            ),
        ),
    ),
    Question(
        slug="time-based-key-value-store", number=981, title="Time Based Key-Value Store",
        difficulty="Medium", topics=("binary-search",),
        summary="set(key, value, timestamp) stores a value (timestamps per key strictly increase). get(key, timestamp) returns the value with the largest timestamp ≤ the given one, or \"\".",
        example="set(foo, bar, 1); get(foo, 3) → \"bar\"; set(foo, bar2, 4); get(foo, 4) → \"bar2\"",
        criterion="Which approach answers get in O(log n)?",
        hint="Since timestamps arrive in increasing order, what does each key's history look like?",
        choices=(
            Choice(
                "Append per key, binary search on get", OPTIMAL, time="O(1) set, O(log n) get", space="O(n)", visual="binary-search",
                detail="Map key → list of (timestamp, value); get finds the last timestamp ≤ t.",
                why="Appends keep each list sorted for free, so get is a boundary search.",
            ),
            Choice(
                "Scan the history backwards", SUBOPTIMAL, time="O(1) set, O(n) get", space="O(n)", visual="brute",
                detail="Walk the key's list from newest until a timestamp ≤ t.",
                why="Correct, but an old timestamp means walking the whole history.",
            ),
            Choice(
                "Exact timestamp lookup", INCORRECT, time="O(1)", space="O(n)", visual="hashmap",
                detail="Store (key, timestamp) → value and look up the exact pair.",
                why="get(foo, 3) has no entry at 3. What should it return?",
            ),
            Choice(
                "Latest value only", INCORRECT, time="O(1)", space="O(k)", visual="hashmap",
                detail="Keep just the newest value per key.",
                why="After set at 4, what does get(foo, 3) need?",
            ),
        ),
    ),
    Question(
        slug="find-k-closest-elements", number=658, title="Find K Closest Elements",
        difficulty="Medium", topics=("binary-search",),
        summary="In a sorted array, return the k elements closest to x (ties prefer smaller values), in sorted order.",
        example="[1,2,3,4,5], k = 4, x = 3  →  [1,2,3,4]",
        criterion="Which approach is O(log(n − k) + k)?",
        hint="The answer is a window of length k. Binary search where it starts.",
        choices=(
            Choice(
                "Binary search the window's left edge", OPTIMAL, time="O(log(n − k) + k)", space="O(1)", visual="binary-search",
                detail="Search l in [0, n − k]: if x − arr[mid] > arr[mid + k] − x, move right; else left.",
                why="Comparing the window's two candidate ends tells which way the best window lies, so the start is found in log(n − k) steps.",
            ),
            Choice(
                "Shrink from both ends", SUBOPTIMAL, time="O(n)", space="O(1)", visual="two-pointers",
                detail="Start with the whole array and drop the farther end until k remain.",
                why="Correct, but drops up to n − k elements one at a time.",
            ),
            Choice(
                "k elements from lower_bound(x)", INCORRECT, time="O(log n + k)", space="O(1)", visual="binary-search",
                detail="Take the k elements starting at the first value ≥ x.",
                why="From 3 there are only [3,4,5], and 2 is as close as 4. What about elements left of x?",
            ),
            Choice(
                "Sort by distance, take k", INCORRECT, time="O(n log n)", space="O(n)", visual="sort",
                detail="Sort by |a − x| and return the first k.",
                why="The output must be in sorted order, and ties must favour the smaller value. Does a distance sort guarantee either?",
            ),
        ),
    ),
    Question(
        slug="lcp-08-plot-trigger-time", number=None, title="Plot Trigger Time",
        difficulty="Medium", topics=("binary-search",),
        ref="LCP 08", url="https://leetcode.cn/problems/ju-qing-hong-fa-shi-jian/",
        summary="Three stats start at 0 and each day grow by increase[d]. A plot triggers once all three reach its requirement. Return each plot's trigger day, or −1.",
        example="increase = [[2,8,4],[2,5,0],[10,9,8]], requirements = [[2,11,3],[15,10,7],[9,17,12],[8,1,14]]  →  [2,-1,3,-1]",
        criterion="Which approach is O(d + q log d)?",
        hint="Each stat's running total never decreases. When does each stat alone meet its requirement?",
        choices=(
            Choice(
                "Prefix sums, three searches, take the max", OPTIMAL, time="O(d + q log d)", space="O(d)", visual="binary-search",
                detail="Build running totals per stat (day 0 included); for each requirement, binary search the first day each stat suffices; answer the latest of the three.",
                why="Each stat is monotone, so its first sufficient day is a boundary. The plot fires when the slowest stat gets there.",
            ),
            Choice(
                "Scan days for each requirement", SUBOPTIMAL, time="O(q·d)", space="O(d)", visual="brute",
                detail="Walk the running totals until all three are met.",
                why="Correct, but 10⁵ requirements × 10⁴ days.",
            ),
            Choice(
                "Search on the sum of stats", INCORRECT, time="O(d + q log d)", space="O(d)", visual="binary-search",
                detail="Find the first day C + R + H ≥ c + r + h.",
                why="A large R can't make up for a small C. Does the sum respect each requirement?",
            ),
            Choice(
                "Start at day 1", INCORRECT, time="O(d + q log d)", space="O(d)", visual="binary-search",
                detail="Search only days 1..d.",
                why="Requirement [0,0,0] is met before any day passes. What should it return?",
            ),
        ),
    ),
    Question(
        slug="shortest-distance-to-target-color", number=1182, title="Shortest Distance to Target Color",
        difficulty="Medium", topics=("binary-search",),
        summary="colors holds values 1–3. For each query (i, c), return the distance from i to the nearest index with color c, or −1.",
        example="colors = [1,1,2,1,3,2,2,3,3], queries = [[1,3],[2,2],[6,1]]  →  [3,0,3]",
        criterion="Which approach is O(n + q)?",
        hint="With only three colors, could you precompute the nearest one of each in both directions?",
        choices=(
            Choice(
                "Nearest-left and nearest-right tables", OPTIMAL, time="O(n + q)", space="O(n)", visual="dp-1d",
                detail="Sweep left to right and right to left, recording the last index of each color; answer each query in O(1).",
                why="Three colors means 3n entries per direction. Each query reads two of them.",
            ),
            Choice(
                "Index lists per color, binary search", SUBOPTIMAL, time="O(n + q log n)", space="O(n)", visual="binary-search",
                detail="Store sorted positions per color and search around i.",
                why="Correct, but the small color count allows precomputing every answer.",
            ),
            Choice(
                "Search only to the right", INCORRECT, time="O(n + q)", space="O(n)", visual="dp-1d",
                detail="Use the next index with color c.",
                why="For query (6, 1), the nearest 1 is at index 3, to the left.",
            ),
            Choice(
                "Distance to c's first occurrence", INCORRECT, time="O(n + q)", space="O(1)", visual="hashmap",
                detail="Record where each color first appears and return |i − first[c]|.",
                why="For (6, 1), the first 1 is at index 0, but index 3 is closer.",
            ),
        ),
    ),
    Question(
        slug="maximum-team-size-with-overlapping-intervals", number=3893, title="Maximum Team Size with Overlapping Intervals",
        difficulty="Medium", topics=("binary-search",),
        summary="Each employee works an interval [start, end]. A team is valid if one member's interval overlaps every other member's. Return the largest valid team.",
        example="[[1,5],[2,3],[4,6]]  →  3",
        criterion="Which approach is O(n log n)?",
        hint="Fix the member who overlaps everyone. Which intervals don't overlap theirs?",
        choices=(
            Choice(
                "Count overlaps per interval with sorted ends", OPTIMAL, time="O(n log n)", space="O(n)", visual="binary-search",
                detail="Sort starts and ends; for interval i, overlaps = n − (ends < start_i) − (starts > end_i).",
                why="An interval misses i only if it ends before i starts or starts after i ends, and those two sets don't intersect. Each count is a binary search.",
            ),
            Choice(
                "Check every pair", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="For each interval, count all intervals overlapping it.",
                why="Correct, but 10⁵ intervals means 10¹⁰ checks.",
            ),
            Choice(
                "Most intervals at one point", INCORRECT, time="O(n log n)", space="O(n)", visual="sort",
                detail="Sweep start and end events and return the peak.",
                why="Members only need to overlap the centre person, not each other. [2,3] and [4,6] never meet, yet both join [1,5].",
            ),
            Choice(
                "Overlaps of the longest interval", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Pick the longest interval as the centre and count.",
                why="A short interval in a crowded spot can overlap more. Is length what matters?",
            ),
        ),
    ),
    Question(
        slug="minimum-relative-loss-after-buying-chocolates", number=2819, title="Minimum Relative Loss After Buying Chocolates",
        difficulty="Hard", topics=("binary-search",),
        summary="For a chocolate costing p, Bob pays min(p, k) and Alice pays the rest; Bob's relative loss is his share minus Alice's. For each query (k, m), Bob picks m chocolates to minimize his total relative loss.",
        example="prices = [1,9,22,10,19], queries = [[18,4],[5,2]]  →  [34, -21]",
        criterion="Which approach is O((n + q) log n)?",
        hint="Loss is p for p ≤ k and 2k − p above it: rising, then falling. Which chocolates have the smallest losses?",
        choices=(
            Choice(
                "Sort, prefix sums, binary search the split", OPTIMAL, time="O((n + q) log n)", space="O(n)", visual="binary-search",
                detail="Bob takes some l cheapest and m − l most expensive; binary search l by comparing the next cheap loss with the next expensive one; sum with prefix sums.",
                why="Small losses sit at both ends of the sorted prices, so the best m form a prefix plus a suffix. The comparison is monotone in l, so l is a boundary search.",
            ),
            Choice(
                "Per query, compute losses and pick m smallest", SUBOPTIMAL, time="O(q·n log n)", space="O(n)", visual="sort",
                detail="For each query, compute every loss and sort.",
                why="Correct, but each query redoes n work the prefix sums already summarize.",
            ),
            Choice(
                "Always the m cheapest", INCORRECT, time="O(n log n + q)", space="O(n)", visual="greedy",
                detail="Take the m lowest prices.",
                why="For k = 5, the 22 gives loss 2·5 − 22 = −12. Is a cheap chocolate better?",
            ),
            Choice(
                "Always the m most expensive", INCORRECT, time="O(n log n + q)", space="O(n)", visual="greedy",
                detail="Take the m highest prices.",
                why="For k = 18, the 19 gives 17 but the 1 gives 1. Which is smaller?",
            ),
        ),
    ),
    Question(
        slug="search-a-2d-matrix", number=74, title="Search a 2D Matrix",
        difficulty="Medium", topics=("binary-search",),
        summary="Each row is sorted, and each row's first value exceeds the previous row's last. Return whether target is in the matrix.",
        example="[[1,3,5,7],[10,11,16,20],[23,30,34,60]], 3  →  true",
        criterion="Which approach is O(log(m·n))?",
        hint="Read the rows one after another. What do you get?",
        choices=(
            Choice(
                "Binary search as one flat array", OPTIMAL, time="O(log(m·n))", space="O(1)", visual="binary-search",
                detail="Search indices 0..m·n − 1, reading matrix[i / n][i % n].",
                why="The row rule makes the whole matrix one sorted sequence, so one search covers it.",
            ),
            Choice(
                "Staircase from the top-right", SUBOPTIMAL, time="O(m + n)", space="O(1)", visual="matrix",
                detail="Move left if the value is too big, down if too small.",
                why="Correct, and it works for weaker orderings too, but this matrix allows a logarithmic search.",
            ),
            Choice(
                "Row whose first value exceeds target", INCORRECT, time="O(log m + log n)", space="O(1)", visual="binary-search",
                detail="Pick the first row with first value > target and search it.",
                why="For target 3, that picks row 1 (starting at 10). Is 3 there?",
            ),
            Choice(
                "Search the middle column", INCORRECT, time="O(log m)", space="O(1)", visual="binary-search",
                detail="Binary search the column at n / 2.",
                why="Most values aren't in that column.",
            ),
        ),
    ),
    Question(
        slug="element-appearing-more-than-25-in-sorted-array", number=1287, title="Element Appearing More Than 25% In Sorted Array",
        difficulty="Easy", topics=("binary-search",),
        summary="A sorted array has exactly one value that appears more than 25% of the time. Return it.",
        example="[1,2,2,6,6,6,6,7,10]  →  6",
        criterion="Which approach is O(log n)?",
        hint="A run longer than n/4 must cover one of a few fixed positions. Which ones?",
        choices=(
            Choice(
                "Check the values at n/4, n/2, 3n/4", OPTIMAL, time="O(log n)", space="O(1)", visual="binary-search",
                detail="For each candidate, find its first and last index by binary search; return the one whose run exceeds n/4.",
                why="A run longer than n/4 can't fit between those positions without covering one. So there are 3 candidates, each checked with two searches.",
            ),
            Choice(
                "Scan runs", SUBOPTIMAL, time="O(n)", space="O(1)", visual="counting",
                detail="Walk the array measuring each run.",
                why="Correct, but reads every element.",
            ),
            Choice(
                "Return the median", INCORRECT, time="O(1)", space="O(1)", visual="math",
                detail="arr[n / 2].",
                why="A run of just over 25% can sit at the start. Does it reach the middle?",
            ),
            Choice(
                "Return arr[n / 4]", INCORRECT, time="O(1)", space="O(1)", visual="math",
                detail="The run must pass index n/4.",
                why="It must cover one of the quarter points, not necessarily the first.",
            ),
        ),
    ),
    Question(
        slug="closest-nodes-queries-in-a-binary-search-tree", number=2476, title="Closest Nodes Queries in a Binary Search Tree",
        difficulty="Medium", topics=("binary-search",),
        summary="For each query q, return [largest value ≤ q, smallest value ≥ q] in a BST (−1 where none). The tree may be unbalanced.",
        example="root = [6,2,13,1,4,9,15,null,null,null,null,null,null,14], queries = [2,5,16]  →  [[2,2],[4,6],[15,-1]]",
        criterion="Which approach is O(n + q log n) even for a skewed tree?",
        hint="A BST search costs its height. What sorted structure doesn't depend on the shape?",
        choices=(
            Choice(
                "In-order to an array, then binary search", OPTIMAL, time="O(n + q log n)", space="O(n)", visual="binary-search",
                detail="Collect values in order; for each query, a lower bound gives both answers.",
                why="In-order traversal yields a sorted array regardless of shape, so each query costs log n.",
            ),
            Choice(
                "Search the BST per query", SUBOPTIMAL, time="O(q·h)", space="O(h)", visual="tree-dfs",
                detail="Walk down from the root, tracking floor and ceiling.",
                why="Correct, but a chain-shaped tree has h = n.",
            ),
            Choice(
                "Only the node where the search stops", INCORRECT, time="O(q·h)", space="O(h)", visual="tree-dfs",
                detail="Return that node's value for both.",
                why="For q = 5 the search ends at 4. Where's the ceiling 6?",
            ),
            Choice(
                "Neighbours in level order", INCORRECT, time="O(n + q log n)", space="O(n)", visual="tree-bfs",
                detail="Binary search the BFS order.",
                why="Is level order sorted?",
            ),
        ),
    ),
    Question(
        slug="check-if-a-number-is-majority-element-in-a-sorted-array", number=1150, title="Check If a Number Is Majority Element in a Sorted Array",
        difficulty="Easy", topics=("binary-search",),
        summary="Return whether target appears more than n/2 times in a sorted array.",
        example="[2,4,5,5,5,5,5,6,6], 5  →  true",
        criterion="Which approach is O(log n)?",
        hint="If target's first copy is at i, where must another copy be for it to be a majority?",
        choices=(
            Choice(
                "Lower bound, then check i + n/2", OPTIMAL, time="O(log n)", space="O(1)", visual="binary-search",
                detail="i = lower_bound(target); return i + n/2 < n and nums[i + n/2] == target.",
                why="Copies are contiguous from i, so more than n/2 of them reach index i + n/2. One search and one check.",
            ),
            Choice(
                "Count in one pass", SUBOPTIMAL, time="O(n)", space="O(1)", visual="counting",
                detail="Count occurrences of target.",
                why="Correct, but ignores the sorted order.",
            ),
            Choice(
                "Middle element equals target", INCORRECT, time="O(1)", space="O(1)", visual="math",
                detail="Return nums[n / 2] == target.",
                why="A majority must cover the middle, but covering the middle isn't enough. [1,2,2,3]?",
            ),
            Choice(
                "Exactly n/2 counts", INCORRECT, time="O(log n)", space="O(1)", visual="binary-search",
                detail="Check nums[i + n/2 − 1] == target.",
                why="That accepts exactly half. Is half a majority?",
            ),
        ),
    ),
]
