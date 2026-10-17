"""Test fixture: classic interview problems across every topic, grouped by pattern.

The real bank fills the roadmap step by step; this one keeps flow tests independent of that.
"""

from app.question_bank.question_schema import INCORRECT, OPTIMAL, SUBOPTIMAL, Choice, Question

QUESTIONS = [
    # ---------------------------------------------------------------- Arrays & Hashing
    Question(
        slug="two-sum", number=1, title="Two Sum",
        difficulty="Easy", topics=("data-structures",),
        summary="Given an unsorted integer array and a target, return the indices of the two entries that add up to the target. Exactly one pair works.",
        example="nums = [2, 7, 11, 15], target = 9  →  [0, 1]",
        criterion="Which approach is best when n is up to 10⁴ and you must return original indices?",
        hint="For each number x, what single value would you need to have seen already?",
        choices=(
            Choice(
                "Hash map, one pass", OPTIMAL, time="O(n)", space="O(n)", visual="hashmap",
                detail="Store value → index; for each x, look up target − x before inserting x.",
                why="What do you need to know when you reach x? Only whether target − x appeared earlier. A hash map answers that in O(1), so one pass is enough.",
            ),
            Choice(
                "Sort + two pointers", SUBOPTIMAL, time="O(n log n)", space="O(n)", visual="two-pointers",
                detail="Sort (value, index) pairs, then move pointers inward from both ends.",
                why="This works if you keep the original indices, but why pay for sorting when a lookup table avoids ordering altogether?",
            ),
            Choice(
                "Check every pair", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="Nested loops over i < j, test nums[i] + nums[j].",
                why="Correct, but how many pairs is that at n = 10⁴? About 5·10⁷ — the repeated searching is exactly what a hash map removes.",
            ),
            Choice(
                "Binary search for complement", INCORRECT, time="O(n log n)", space="O(1)", visual="binary-search",
                detail="For each x, binary search the array for target − x.",
                why="Binary search needs sorted input. The array here is unsorted, so what would the search actually return?",
            ),
        ),
    ),
    Question(
        slug="group-anagrams", number=49, title="Group Anagrams",
        difficulty="Medium", topics=("data-structures",),
        summary="Group a list of lowercase strings so that words that are anagrams of each other end up in the same group.",
        example="[\"eat\",\"tea\",\"tan\",\"ate\",\"nat\",\"bat\"]  →  [[\"eat\",\"tea\",\"ate\"],[\"tan\",\"nat\"],[\"bat\"]]",
        criterion="Which approach is the standard interview answer for n words of length ≤ k?",
        hint="What canonical form do all anagrams of a word share?",
        choices=(
            Choice(
                "Hash map keyed by sorted word", OPTIMAL, time="O(n·k log k)", space="O(n·k)", visual="hashmap",
                detail="Sort each word's letters and use the result as the map key.",
                why="What do 'eat', 'tea' and 'ate' have in common? The same sorted letters, 'aet'. Using that as a key groups them in one pass.",
            ),
            Choice(
                "Compare every pair", SUBOPTIMAL, time="O(n²·k log k)", space="O(n·k)", visual="brute",
                detail="For each pair of words, sort both and compare to decide if they belong together.",
                why="It gives correct groups, but why compare pairs when each word can compute its own group key independently?",
            ),
            Choice(
                "Key by length + char-code sum", INCORRECT, time="O(n·k)", space="O(n·k)", visual="math",
                detail="Group words with the same length and the same sum of character codes.",
                why="Is the sum unique to a set of letters? 'ad' and 'bc' have equal length and equal sums, but they are not anagrams.",
            ),
            Choice(
                "Union-find over anagram pairs", SUBOPTIMAL, time="O(n²·k)", space="O(n)", visual="union-find",
                detail="Union every pair of words that are anagrams, then collect components.",
                why="Union-find gives the right components, but it still checks all pairs. A canonical key avoids pairing entirely.",
            ),
        ),
    ),
    Question(
        slug="top-k-frequent-elements", number=347, title="Top K Frequent Elements",
        difficulty="Medium", topics=("data-structures",),
        summary="Return the k values that occur most often in an integer array. The answer is unique.",
        example="nums = [1,1,1,2,2,3], k = 2  →  [1, 2]",
        criterion="Which approach is best when k is much smaller than the number of distinct values?",
        hint="After counting, do you need a full ordering of all values, or only the best k?",
        choices=(
            Choice(
                "Count + min-heap of size k", OPTIMAL, time="O(n log k)", space="O(n)", visual="heap",
                detail="Count with a hash map, keep a min-heap of the k highest counts.",
                why="Do you need to rank every value? No — only the top k. A size-k heap evicts anything that cannot make the cut, so each step costs log k.",
            ),
            Choice(
                "Count + sort by frequency", SUBOPTIMAL, time="O(n log n)", space="O(n)", visual="sort",
                detail="Count with a hash map, sort all distinct values by count.",
                why="Correct, but sorting orders all distinct values. When k is small, how much of that ordering do you actually use?",
            ),
            Choice(
                "Pick the max count k times", SUBOPTIMAL, time="O(k·n)", space="O(n)", visual="brute",
                detail="Count, then scan the map k times, removing the current max each time.",
                why="Works, but each of the k passes rescans everything. What structure keeps the best candidates ready?",
            ),
            Choice(
                "Sort values, take last k distinct", INCORRECT, time="O(n log n)", space="O(n)", visual="sort",
                detail="Sort nums and return the k largest distinct values.",
                why="Are the largest values the most frequent ones? Not necessarily — this ranks by value, not by count.",
            ),
        ),
    ),
    Question(
        slug="product-of-array-except-self", number=238, title="Product of Array Except Self",
        difficulty="Medium", topics=("data-structures",),
        summary="For each position, output the product of every other element. Division is not allowed.",
        example="[1, 2, 3, 4]  →  [24, 12, 8, 6]",
        criterion="Which approach meets O(n) time without division, using only the output array as extra space?",
        hint="The answer at i is (product of everything left of i) × (product of everything right of i).",
        choices=(
            Choice(
                "Prefix × suffix products", OPTIMAL, time="O(n)", space="O(1) extra", visual="prefix",
                detail="Fill output with left products, then sweep right-to-left multiplying a running suffix.",
                why="Can you split 'everything except i' into two parts you can build incrementally? Left products and right products — two sweeps, no division.",
            ),
            Choice(
                "Total product ÷ nums[i]", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="Multiply everything once, divide by each element.",
                why="Division is disallowed, and what happens when the array contains a zero?",
            ),
            Choice(
                "Multiply all others per index", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="For each i, loop over every j ≠ i.",
                why="Correct, but notice how much multiplication is repeated between i and i+1. Could you reuse it?",
            ),
            Choice(
                "Segment tree of products", SUBOPTIMAL, time="O(n log n)", space="O(n)", visual="tree-dfs",
                detail="Build a product segment tree; query [0,i) and (i,n) for each i.",
                why="It works, but the queries are always prefixes and suffixes. Do you need a general range structure for that?",
            ),
        ),
    ),
    Question(
        slug="longest-consecutive-sequence", number=128, title="Longest Consecutive Sequence",
        difficulty="Medium", topics=("data-structures",),
        summary="Find the length of the longest run of consecutive integers that can be formed from the values of an unsorted array.",
        example="[100, 4, 200, 1, 3, 2]  →  4  (1, 2, 3, 4)",
        criterion="The problem requires O(n) time. Which approach meets it?",
        hint="How can you tell that a number is the start of a run?",
        choices=(
            Choice(
                "Hash set, count from run starts", OPTIMAL, time="O(n)", space="O(n)", visual="set",
                detail="Put values in a set; only when x − 1 is absent, count x, x+1, … .",
                why="If x − 1 is in the set, is x ever a run start? No. Counting only from starts means each value is visited a constant number of times.",
            ),
            Choice(
                "Sort, then scan", SUBOPTIMAL, time="O(n log n)", space="O(1)", visual="sort",
                detail="Sort, skip duplicates, and track the current run length.",
                why="Correct and simple, but does it meet the O(n) requirement? Sorting alone costs n log n.",
            ),
            Choice(
                "Count upward from every value", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="brute",
                detail="Use a set, but start counting x, x+1, … from every value.",
                why="Correct, but a run of length L gets recounted from each of its members. What check would avoid that?",
            ),
            Choice(
                "Two pointers on the raw array", INCORRECT, time="O(n)", space="O(1)", visual="two-pointers",
                detail="Move left/right pointers while neighbors differ by 1.",
                why="Consecutive values need not be adjacent in an unsorted array. What would the pointers be comparing?",
            ),
        ),
    ),
    # ---------------------------------------------------------------- Two Pointers
    Question(
        slug="valid-palindrome", number=125, title="Valid Palindrome",
        difficulty="Easy", topics=("sliding-window",),
        summary="Decide whether a string reads the same forward and backward after lowercasing and ignoring non-alphanumeric characters.",
        example="\"A man, a plan, a canal: Panama\"  →  true",
        criterion="Which approach uses O(1) extra space?",
        hint="Compare characters from both ends while skipping the ones that don't count.",
        choices=(
            Choice(
                "Two pointers from both ends", OPTIMAL, time="O(n)", space="O(1)", visual="two-pointers",
                detail="Move i forward and j backward, skipping non-alphanumerics, compare lowercased chars.",
                why="Do you need a cleaned copy to compare the ends? No — skip invalid characters in place and compare as you go.",
            ),
            Choice(
                "Clean copy vs. its reverse", SUBOPTIMAL, time="O(n)", space="O(n)", visual="array-copy",
                detail="Build a filtered lowercase string and compare it to its reverse.",
                why="Correct and readable, but it allocates two extra strings. Can you compare without building them?",
            ),
            Choice(
                "Recursively strip the ends", SUBOPTIMAL, time="O(n²)", space="O(n²)", visual="recursion",
                detail="Check first/last char, recurse on the sliced middle.",
                why="It's correct, but each slice copies the string. How much copying happens over n/2 levels?",
            ),
            Choice(
                "At most one odd letter count", INCORRECT, time="O(n)", space="O(1)", visual="hashmap",
                detail="Count characters; valid if at most one has an odd count.",
                why="That tests whether the letters could be rearranged into a palindrome. 'aab' passes the count test, but it isn't one.",
            ),
        ),
    ),
    Question(
        slug="3sum", number=15, title="3Sum",
        difficulty="Medium", topics=("sliding-window",),
        summary="Return all unique triplets in an array whose values sum to zero.",
        example="[-1, 0, 1, 2, -1, -4]  →  [[-1, -1, 2], [-1, 0, 1]]",
        criterion="Which approach is the standard answer, handling duplicates cleanly with O(1) extra space?",
        hint="Fix one number; the remaining problem is Two Sum on a sorted array.",
        choices=(
            Choice(
                "Sort + fix one + two pointers", OPTIMAL, time="O(n²)", space="O(1) extra", visual="two-pointers",
                detail="Sort; for each i, move l/r inward on the rest, skipping duplicates.",
                why="Once sorted, what does Two Sum become? A two-pointer sweep. Sorting also puts duplicates next to each other so skipping them is trivial.",
            ),
            Choice(
                "Pairs + hash lookup", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="hashmap",
                detail="For each pair, check a hash set for the negated sum; dedupe with a set of triplets.",
                why="Same time bound, but it needs extra memory and fiddly deduplication. What does sorting give you for free?",
            ),
            Choice(
                "Three nested loops", SUBOPTIMAL, time="O(n³)", space="O(n)", visual="brute",
                detail="Try every triplet; store sorted triplets in a set.",
                why="Correct, but at n = 3000 that's billions of triplets. Which inner loop can be replaced by pointers?",
            ),
            Choice(
                "Sliding window of size 3", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Sort, then check each window of three adjacent values.",
                why="Must the three values be adjacent? [-4, …, 1, …, 3] can sum to zero with gaps between them.",
            ),
        ),
    ),
    Question(
        slug="container-with-most-water", number=11, title="Container With Most Water",
        difficulty="Medium", topics=("sliding-window",),
        summary="Given vertical line heights, pick two lines that together with the x-axis hold the most water. Area = width × shorter height.",
        example="[1, 8, 6, 2, 5, 4, 8, 3, 7]  →  49",
        criterion="Which approach is best for n up to 10⁵?",
        hint="If you start as wide as possible, which side can you safely give up?",
        choices=(
            Choice(
                "Two pointers, move the shorter side", OPTIMAL, time="O(n)", space="O(1)", visual="two-pointers",
                detail="Start at both ends; record area; move the pointer at the shorter line inward.",
                why="Can moving the taller line ever help? The width shrinks and the height is still capped by the shorter line — so only moving the shorter one can improve.",
            ),
            Choice(
                "Check every pair", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="Compute the area for every i < j.",
                why="Correct, but at 10⁵ lines that's ~5·10⁹ pairs. Which pairs can you prove are never better?",
            ),
            Choice(
                "Pair the two tallest lines", INCORRECT, time="O(n log n)", space="O(n)", visual="sort",
                detail="Sort heights descending and use the two tallest.",
                why="Area also depends on width. Two tall lines next to each other can hold less than two medium lines far apart.",
            ),
            Choice(
                "Prefix/suffix max water formula", INCORRECT, time="O(n)", space="O(n)", visual="prefix",
                detail="Sum min(leftMax, rightMax) − h over all positions.",
                why="That formula solves Trapping Rain Water. Here you pick only two lines; is the answer a sum over all positions?",
            ),
        ),
    ),
    Question(
        slug="trapping-rain-water", number=42, title="Trapping Rain Water",
        difficulty="Hard", topics=("sliding-window", "monotonic-stack"),
        summary="Given bar heights, compute how much rain water is trapped between the bars after it rains.",
        example="[0,1,0,2,1,0,1,3,2,1,2,1]  →  6",
        criterion="Which approach is best using O(1) extra space?",
        hint="Water above a bar is min(max to its left, max to its right) − its height.",
        choices=(
            Choice(
                "Two pointers with running maxes", OPTIMAL, time="O(n)", space="O(1)", visual="two-pointers",
                detail="Move the side with the smaller max inward, adding max − height.",
                why="If leftMax < rightMax, is the water at the left pointer already decided? Yes — the left side is the bottleneck. That lets you drop the arrays.",
            ),
            Choice(
                "Prefix-max and suffix-max arrays", SUBOPTIMAL, time="O(n)", space="O(n)", visual="prefix",
                detail="Precompute leftMax[] and rightMax[], then sum.",
                why="Correct and a good stepping stone, but can you avoid storing both arrays?",
            ),
            Choice(
                "Scan both sides for every bar", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="For each bar, scan left and right to find the maxima.",
                why="Correct, but it recomputes the same maxima over and over. What could you carry along instead?",
            ),
            Choice(
                "Two pointers, move the taller side", INCORRECT, time="O(n)", space="O(1)", visual="two-pointers",
                detail="Same as above but advance the pointer with the larger max.",
                why="Which side's water level is guaranteed? Only the side with the smaller max. Moving the taller side adds water you can't justify.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- Stack
    Question(
        slug="valid-parentheses", number=20, title="Valid Parentheses",
        difficulty="Easy", topics=("data-structures",),
        summary="Decide whether a string of ()[]{} brackets is properly opened and closed in the right order.",
        example="\"([]{})\" → true,   \"([)]\" → false",
        criterion="Which approach is correct and linear?",
        hint="When you see a closing bracket, which opening bracket must it match?",
        choices=(
            Choice(
                "Stack of open brackets", OPTIMAL, time="O(n)", space="O(n)", visual="stack",
                detail="Push openers; on a closer, pop and check it matches.",
                why="A closer must match the most recent unmatched opener — last in, first out. That is exactly a stack.",
            ),
            Choice(
                "Count each bracket type", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Valid if each type has equal opens and closes.",
                why="What does counting say about '([)]'? The counts balance, but the order is wrong.",
            ),
            Choice(
                "Repeatedly delete (), [], {}", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="brute",
                detail="Remove adjacent matching pairs until none remain.",
                why="It gives the right answer, but each pass rescans the string. A stack does the same cancellation in one pass.",
            ),
            Choice(
                "Split in half and mirror-check", INCORRECT, time="O(n)", space="O(1)", visual="two-pointers",
                detail="Check that the second half mirrors the first.",
                why="Is '()()' a mirror of itself? No, yet it's valid. Nesting isn't the only valid shape.",
            ),
        ),
    ),
    Question(
        slug="daily-temperatures", number=739, title="Daily Temperatures",
        difficulty="Medium", topics=("monotonic-stack",),
        summary="For each day, find how many days you'd wait for a warmer temperature (0 if never).",
        example="[73,74,75,71,69,72,76,73]  →  [1,1,4,2,1,1,0,0]",
        criterion="Which approach is best for n up to 10⁵?",
        hint="Which days are still 'waiting' for a warmer day, and in what order do they get answered?",
        choices=(
            Choice(
                "Monotonic decreasing stack", OPTIMAL, time="O(n)", space="O(n)", visual="monotonic-stack",
                detail="Keep indices of unresolved days; pop while today is warmer and record the gap.",
                why="Waiting days always have non-increasing temperatures, so a warmer day resolves them from the top. Each index is pushed and popped once.",
            ),
            Choice(
                "Scan forward for each day", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="For every day, look ahead until a warmer day appears.",
                why="Correct, but a long cooling streak makes every day scan far ahead. Which work is repeated?",
            ),
            Choice(
                "Min-heap of pending days", SUBOPTIMAL, time="O(n log n)", space="O(n)", visual="heap",
                detail="Push (temp, idx); each day pop all cooler entries and answer them.",
                why="It's correct, but do you need a heap? The pending days are already in sorted order — a stack keeps that for free.",
            ),
            Choice(
                "Next larger value in sorted order", INCORRECT, time="O(n log n)", space="O(n)", visual="sort",
                detail="Sort temperatures; the answer is the index gap to the next larger value.",
                why="The next larger value in sorted order might occur earlier in time. Does sorting keep 'future days only'?",
            ),
        ),
    ),
    Question(
        slug="min-stack", number=155, title="Min Stack",
        difficulty="Medium", topics=("data-structures",),
        summary="Design a stack supporting push, pop, top and getMin, each in constant time.",
        example="push(-2), push(0), push(-3), getMin() → -3, pop(), getMin() → -2",
        criterion="All four operations must be O(1).",
        hint="If you pop the current minimum, how do you know the previous one?",
        choices=(
            Choice(
                "Store (value, min so far) pairs", OPTIMAL, time="O(1) each", space="O(n)", visual="stack",
                detail="Each entry remembers the minimum of the stack at that height.",
                why="What was the minimum before this push? Store it alongside the value, and popping restores it automatically.",
            ),
            Choice(
                "Scan on getMin", SUBOPTIMAL, time="O(n) getMin", space="O(n)", visual="brute",
                detail="Plain stack; getMin looks through all elements.",
                why="Correct, but getMin isn't O(1). What could you precompute at push time?",
            ),
            Choice(
                "Single global min variable", INCORRECT, time="O(1)", space="O(1)", visual="math",
                detail="Update min on push; keep it on pop.",
                why="Push 1, push 0, pop. What is min now? The variable still says 0, but 0 is gone.",
            ),
            Choice(
                "Stack + sorted multiset", SUBOPTIMAL, time="O(log n)", space="O(n)", visual="tree-dfs",
                detail="Mirror values in a balanced BST for min lookups.",
                why="Correct, but log n per operation. Only the minimum matters, and the stack's order already tells you when it changes.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- Binary Search
    Question(
        slug="binary-search", number=704, title="Binary Search",
        difficulty="Easy", topics=("binary-search",),
        summary="Return the index of a target in a sorted array of distinct integers, or −1 if absent.",
        example="nums = [-1,0,3,5,9,12], target = 9  →  4",
        criterion="The solution must run in O(log n).",
        hint="What does comparing with the middle element tell you about half of the array?",
        choices=(
            Choice(
                "Classic binary search", OPTIMAL, time="O(log n)", space="O(1)", visual="binary-search",
                detail="Keep lo/hi; compare with mid and discard half each step.",
                why="Because the array is sorted, one comparison with the middle rules out half the candidates. That halving is what gives log n.",
            ),
            Choice(
                "Linear scan", SUBOPTIMAL, time="O(n)", space="O(1)", visual="brute",
                detail="Check each element in order.",
                why="Correct, but it ignores the sorted order. What information are you throwing away?",
            ),
            Choice(
                "Jump search in √n blocks", SUBOPTIMAL, time="O(√n)", space="O(1)", visual="sliding-window",
                detail="Jump ahead √n at a time, then scan the block.",
                why="Better than linear, but still not logarithmic. Why jump by a fixed step when you can halve?",
            ),
            Choice(
                "Build a value → index map", SUBOPTIMAL, time="O(n)", space="O(n)", visual="hashmap",
                detail="Put every element in a hash map, then look up the target.",
                why="One lookup is O(1), but building the map reads the whole array. Is that under O(log n)?",
            ),
        ),
    ),
    Question(
        slug="search-in-rotated-sorted-array", number=33, title="Search in Rotated Sorted Array",
        difficulty="Medium", topics=("binary-search",),
        summary="A sorted array of distinct values was rotated at an unknown pivot. Find the index of a target, or −1.",
        example="[4,5,6,7,0,1,2], target = 0  →  4",
        criterion="The solution must run in O(log n).",
        hint="At any mid, at least one of the two halves is still properly sorted.",
        choices=(
            Choice(
                "Binary search on the sorted half", OPTIMAL, time="O(log n)", space="O(1)", visual="binary-search",
                detail="At each mid, find which half is sorted and check if the target lies in it.",
                why="Can you always tell which half is sorted? Yes, by comparing nums[lo] with nums[mid]. Then a range check tells you where to go.",
            ),
            Choice(
                "Plain binary search", INCORRECT, time="O(log n)", space="O(1)", visual="binary-search",
                detail="Ignore the rotation and search as if the array were sorted.",
                why="After rotation, is 'target < mid → go left' still true? Not across the pivot — you'd discard the half holding the target.",
            ),
            Choice(
                "Linear scan", SUBOPTIMAL, time="O(n)", space="O(1)", visual="brute",
                detail="Check each element.",
                why="Correct, but it misses the O(log n) requirement. What sortedness is still left to exploit?",
            ),
            Choice(
                "Hash map of value → index", SUBOPTIMAL, time="O(n)", space="O(n)", visual="hashmap",
                detail="Index all values, then look up the target.",
                why="Building the map already reads every element, so the requirement is lost before the lookup.",
            ),
        ),
    ),
    Question(
        slug="koko-eating-bananas", number=875, title="Koko Eating Bananas",
        difficulty="Medium", topics=("binary-search",),
        summary="Koko eats up to k bananas per hour from one pile at a time. Find the minimum k that finishes all piles within h hours.",
        example="piles = [3,6,7,11], h = 8  →  4",
        criterion="Which approach is best when pile sizes go up to 10⁹?",
        hint="If speed k works, does every speed above k also work?",
        choices=(
            Choice(
                "Binary search on speed", OPTIMAL, time="O(n log m)", space="O(1)", visual="binary-search",
                detail="Search k in [1, max(pile)]; check total hours = Σ⌈p/k⌉ ≤ h.",
                why="Feasibility is monotonic in k: faster never hurts. That means you can binary search on the answer instead of the array.",
            ),
            Choice(
                "Try k = 1, 2, 3, …", SUBOPTIMAL, time="O(n·m)", space="O(1)", visual="brute",
                detail="Increase k until the hours fit.",
                why="Correct, but m can be 10⁹. Since feasibility only flips once, do you need to try every k?",
            ),
            Choice(
                "k = ⌈sum / h⌉", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="Divide total bananas evenly across hours.",
                why="Koko can't split an hour between piles. With [3,6,7,11] and h = 8, ⌈27/8⌉ = 4 happens to work — try piles = [5,5], h = 3.",
            ),
            Choice(
                "Greedy on the largest pile", INCORRECT, time="O(n log n)", space="O(n)", visual="heap",
                detail="Use a max-heap and eat the biggest pile first.",
                why="The order Koko eats piles doesn't change the total hours. What quantity are you actually minimizing?",
            ),
        ),
    ),
    # ---------------------------------------------------------------- Sliding Window
    Question(
        slug="best-time-to-buy-and-sell-stock", number=121, title="Best Time to Buy and Sell Stock",
        difficulty="Easy", topics=("data-structures", "dp"),
        summary="Given daily prices, choose one day to buy and a later day to sell for maximum profit (0 if no profit is possible).",
        example="[7, 1, 5, 3, 6, 4]  →  5",
        criterion="Which approach is best for n up to 10⁵?",
        hint="On each day, what's the best price you could have bought at?",
        choices=(
            Choice(
                "Track the minimum so far", OPTIMAL, time="O(n)", space="O(1)", visual="sliding-window",
                detail="One pass: profit = price − min price seen so far.",
                why="If you sell today, the best buy is the cheapest earlier day. Keeping that running minimum answers every day in one pass.",
            ),
            Choice(
                "Check every buy/sell pair", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="Nested loops over i < j.",
                why="Correct, but for each sell day you re-find the cheapest earlier price. Could you remember it instead?",
            ),
            Choice(
                "Global max − global min", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="Subtract the overall lowest price from the overall highest.",
                why="What if the highest price comes before the lowest? You can't sell before you buy.",
            ),
            Choice(
                "Sort prices", INCORRECT, time="O(n log n)", space="O(1)", visual="sort",
                detail="Sort and take last − first.",
                why="Sorting destroys the time order, which is the whole constraint.",
            ),
        ),
    ),
    Question(
        slug="longest-substring-without-repeating-characters", number=3, title="Longest Substring Without Repeating Characters",
        difficulty="Medium", topics=("sliding-window",),
        summary="Find the length of the longest contiguous substring that has no repeated characters.",
        example="\"abcabcbb\"  →  3  (\"abc\")",
        criterion="Which approach is best for strings up to 5·10⁴ characters?",
        hint="When you hit a repeat, where must the new window start?",
        choices=(
            Choice(
                "Sliding window + last-seen map", OPTIMAL, time="O(n)", space="O(Σ)", visual="sliding-window",
                detail="Expand right; on a repeat, jump left past the character's previous index.",
                why="When s[r] repeats, any window containing both copies is invalid — so left can jump straight past the old copy. Each index moves forward only.",
            ),
            Choice(
                "Extend from every start", SUBOPTIMAL, time="O(n²)", space="O(Σ)", visual="brute",
                detail="For each start, grow with a set until a repeat.",
                why="Correct, but after a repeat you restart from the next index and recheck the same characters. Why throw that work away?",
            ),
            Choice(
                "Check every substring", SUBOPTIMAL, time="O(n³)", space="O(Σ)", visual="brute",
                detail="Generate all substrings and test uniqueness.",
                why="Correct but cubic. Which substrings can you rule out without testing them?",
            ),
            Choice(
                "Count distinct characters", INCORRECT, time="O(n)", space="O(Σ)", visual="set",
                detail="Return the number of distinct characters in s.",
                why="'pwwkew' has 4 distinct letters, but the longest repeat-free substring is 'wke' (3). Distinct counts ignore contiguity.",
            ),
        ),
    ),
    Question(
        slug="minimum-window-substring", number=76, title="Minimum Window Substring",
        difficulty="Hard", topics=("sliding-window",),
        summary="Find the shortest substring of s that contains every character of t (with multiplicity).",
        example="s = \"ADOBECODEBANC\", t = \"ABC\"  →  \"BANC\"",
        criterion="Which approach is best for |s|, |t| up to 10⁵?",
        hint="Grow the window until it's valid, then shrink it while it stays valid.",
        choices=(
            Choice(
                "Variable window with need/have counts", OPTIMAL, time="O(|s|+|t|)", space="O(Σ)", visual="sliding-window",
                detail="Expand right until all needed counts are met, then shrink left while valid.",
                why="Once a window is valid, is any longer window with the same left end useful? No — so shrink from the left. Each pointer only moves forward.",
            ),
            Choice(
                "Binary search on window length", SUBOPTIMAL, time="O(|s| log |s|)", space="O(Σ)", visual="binary-search",
                detail="For length L, slide a fixed window and test validity; search the smallest valid L.",
                why="Valid, since a longer window never loses characters. But the variable window finds the answer in a single linear pass.",
            ),
            Choice(
                "Check every substring", SUBOPTIMAL, time="O(n²·Σ)", space="O(Σ)", visual="brute",
                detail="Test all O(n²) substrings.",
                why="Correct, but hopeless at 10⁵. Which windows can you skip once you know one is valid?",
            ),
            Choice(
                "Fixed window of length |t|", INCORRECT, time="O(|s|)", space="O(Σ)", visual="sliding-window",
                detail="Slide a window exactly as long as t.",
                why="Must the answer be exactly |t| long? 'BANC' is longer than 'ABC' — extra characters in between are allowed.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- Linked List
    Question(
        slug="reverse-linked-list", number=206, title="Reverse Linked List",
        difficulty="Easy", topics=("trees",),
        summary="Reverse a singly linked list and return the new head.",
        example="1 → 2 → 3 → 4 → 5  →  5 → 4 → 3 → 2 → 1",
        criterion="Which approach uses O(1) extra space?",
        hint="As you walk, what do you need to remember so you don't lose the rest of the list?",
        choices=(
            Choice(
                "Iterative prev/curr pointers", OPTIMAL, time="O(n)", space="O(1)", visual="linked-list",
                detail="Save next, point curr.next to prev, advance both.",
                why="Each node only needs its arrow flipped. Keeping prev and next lets you do that in place with no extra memory.",
            ),
            Choice(
                "Recursive reversal", SUBOPTIMAL, time="O(n)", space="O(n)", visual="recursion",
                detail="Reverse the rest, then hook head behind the old tail.",
                why="Elegant and correct, but every node adds a stack frame. For long lists, where does that memory go?",
            ),
            Choice(
                "Copy values, write them back", SUBOPTIMAL, time="O(n)", space="O(n)", visual="array-copy",
                detail="Collect values into an array, then overwrite nodes in reverse.",
                why="It produces the right order, but uses an array and rewrites values instead of relinking nodes.",
            ),
            Choice(
                "Swap head and tail", INCORRECT, time="O(n)", space="O(1)", visual="linked-list",
                detail="Exchange the first and last nodes.",
                why="What happens to the middle nodes? For 1→2→3→4, you'd get 4→2→3→1.",
            ),
        ),
    ),
    Question(
        slug="linked-list-cycle", number=141, title="Linked List Cycle",
        difficulty="Easy", topics=("trees", "sliding-window"),
        summary="Decide whether a linked list contains a cycle.",
        example="3 → 2 → 0 → -4 → (back to 2)  →  true",
        criterion="Which approach uses O(1) extra space?",
        hint="If two runners go around a track at different speeds, what eventually happens?",
        choices=(
            Choice(
                "Fast & slow pointers (Floyd)", OPTIMAL, time="O(n)", space="O(1)", visual="fast-slow",
                detail="Move slow by 1, fast by 2; a cycle makes them meet.",
                why="Inside a cycle, the fast pointer gains one step per move on the slow one, so it must catch up. No memory beyond two pointers.",
            ),
            Choice(
                "Hash set of visited nodes", SUBOPTIMAL, time="O(n)", space="O(n)", visual="set",
                detail="Store node references; a repeat means a cycle.",
                why="Correct and easy, but it remembers every node. Can two pointers detect the loop without the set?",
            ),
            Choice(
                "Detect repeated values", INCORRECT, time="O(n)", space="O(n)", visual="hashmap",
                detail="Track node values; a repeated value means a cycle.",
                why="Two different nodes can hold the same value. Is 1 → 1 → null a cycle?",
            ),
            Choice(
                "Count past the expected length", INCORRECT, time="O(n)", space="O(1)", visual="brute",
                detail="Walk; if you take more than n steps, it's a cycle.",
                why="You don't know n — the list has no stored length, and with a cycle you can't count it.",
            ),
        ),
    ),
    Question(
        slug="merge-two-sorted-lists", number=21, title="Merge Two Sorted Lists",
        difficulty="Easy", topics=("trees",),
        summary="Merge two sorted linked lists into one sorted list by splicing their nodes together.",
        example="1→2→4 and 1→3→4  →  1→1→2→3→4→4",
        criterion="Which approach is linear with O(1) extra space?",
        hint="At each step, which node should come next?",
        choices=(
            Choice(
                "Dummy head + splice smaller node", OPTIMAL, time="O(n+m)", space="O(1)", visual="linked-list",
                detail="Compare heads, attach the smaller, advance; append the leftover.",
                why="Both lists are sorted, so the next node is always one of the two heads. A dummy node removes the special case for the first attachment.",
            ),
            Choice(
                "Recursive merge", SUBOPTIMAL, time="O(n+m)", space="O(n+m)", visual="recursion",
                detail="Return the smaller head with next = merge(rest).",
                why="Correct and concise, but it uses one stack frame per node. Is that O(1) space?",
            ),
            Choice(
                "Collect, sort, rebuild", SUBOPTIMAL, time="O((n+m) log(n+m))", space="O(n+m)", visual="sort",
                detail="Put all values in an array, sort, create a new list.",
                why="Correct, but the inputs are already sorted. Why sort again?",
            ),
            Choice(
                "Alternate nodes from each list", INCORRECT, time="O(n+m)", space="O(1)", visual="linked-list",
                detail="Take one node from list 1, then list 2, and repeat.",
                why="With 1→2→3 and 10→20, alternating gives 1,10,2,20,3. Is that sorted?",
            ),
        ),
    ),
    Question(
        slug="lru-cache", number=146, title="LRU Cache",
        difficulty="Medium", topics=("trees", "data-structures"),
        summary="Design a fixed-capacity cache where get and put run in O(1) and the least-recently-used key is evicted when full.",
        example="cap=2: put(1), put(2), get(1), put(3) evicts key 2",
        criterion="get and put must both be O(1) on average.",
        hint="You need fast lookup by key and fast reordering by recency.",
        choices=(
            Choice(
                "Hash map + doubly linked list", OPTIMAL, time="O(1)", space="O(cap)", visual="linked-list",
                detail="Map key → node; move nodes to the front on use; evict from the tail.",
                why="The map finds a node in O(1); the doubly linked list lets you unlink and move it in O(1). Together they cover both needs.",
            ),
            Choice(
                "Hash map + array ordering", SUBOPTIMAL, time="O(cap)", space="O(cap)", visual="array-copy",
                detail="Keep keys in an array ordered by use; move a key on each access.",
                why="Correct eviction, but moving a key inside an array shifts elements. Which structure can move an item in O(1)?",
            ),
            Choice(
                "Hash map + timestamps", SUBOPTIMAL, time="O(cap) evict", space="O(cap)", visual="hashmap",
                detail="Store last-used time; on eviction scan for the oldest.",
                why="Correct, but eviction scans everything. Can you keep items already ordered by recency?",
            ),
            Choice(
                "FIFO queue", INCORRECT, time="O(1)", space="O(cap)", visual="queue",
                detail="Evict the key that was inserted first.",
                why="Insertion order isn't usage order. If key 1 was inserted first but just used, should it be evicted?",
            ),
        ),
    ),
    # ---------------------------------------------------------------- Trees
    Question(
        slug="maximum-depth-of-binary-tree", number=104, title="Maximum Depth of Binary Tree",
        difficulty="Easy", topics=("trees",),
        summary="Return the number of nodes on the longest root-to-leaf path of a binary tree.",
        example="[3, 9, 20, null, null, 15, 7]  →  3",
        criterion="Which approach is the standard linear answer?",
        hint="How does a node's depth relate to its children's depths?",
        choices=(
            Choice(
                "Recursive DFS: 1 + max(children)", OPTIMAL, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="depth(node) = 1 + max(depth(left), depth(right)).",
                why="The answer for a node is built from its children's answers — a natural recursion visiting each node once.",
            ),
            Choice(
                "Follow the leftmost path", INCORRECT, time="O(h)", space="O(1)", visual="tree-dfs",
                detail="Count nodes while going left from the root.",
                why="What if the deepest leaf is on the right? The left spine can be short.",
            ),
            Choice(
                "log₂(number of nodes)", INCORRECT, time="O(n)", space="O(h)", visual="math",
                detail="Count nodes, then take the logarithm.",
                why="That only holds for balanced trees. A tree shaped like a linked list has depth n.",
            ),
            Choice(
                "Search from root for every node", SUBOPTIMAL, time="O(n·h)", space="O(h)", visual="brute",
                detail="For each node, walk from the root to compute its depth; take the max.",
                why="Correct, but each walk repeats work shared by ancestors. What if children just asked their parent's depth?",
            ),
        ),
    ),
    Question(
        slug="lowest-common-ancestor-of-a-binary-search-tree", number=235, title="Lowest Common Ancestor of a BST",
        difficulty="Medium", topics=("trees",),
        summary="In a binary search tree, find the deepest node that has both given nodes p and q as descendants (a node counts as its own descendant).",
        example="root = [6,2,8,0,4,7,9], p = 2, q = 8  →  6",
        criterion="Which approach best uses the BST property?",
        hint="If both p and q are smaller than the current node, where must their ancestor be?",
        choices=(
            Choice(
                "Walk down using BST order", OPTIMAL, time="O(h)", space="O(1)", visual="binary-search",
                detail="Go left if both are smaller, right if both are larger; otherwise stop.",
                why="The first node where p and q split to different sides (or equals one of them) is the LCA. The BST ordering tells you the direction without exploring both subtrees.",
            ),
            Choice(
                "General binary-tree LCA recursion", SUBOPTIMAL, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Recurse into both subtrees; return the node where p and q are found on different sides.",
                why="Correct on any binary tree, but it ignores the ordering. Why search both subtrees when values tell you which one?",
            ),
            Choice(
                "Store root-to-node paths", SUBOPTIMAL, time="O(h)", space="O(h)", visual="array-copy",
                detail="Record the path to p and to q, then find the last common node.",
                why="Correct, but it stores two paths. Can you walk once and stop at the split point?",
            ),
            Choice(
                "Node with value ⌊(p+q)/2⌋", INCORRECT, time="O(h)", space="O(1)", visual="math",
                detail="Search for the midpoint value.",
                why="The LCA's value lies between p and q, but why would it be their exact average? It may not even exist.",
            ),
        ),
    ),
    Question(
        slug="validate-binary-search-tree", number=98, title="Validate Binary Search Tree",
        difficulty="Medium", topics=("trees",),
        summary="Decide whether a binary tree is a valid BST: every node's left subtree is strictly smaller and right subtree strictly larger.",
        example="[5, 1, 4, null, null, 3, 6]  →  false",
        criterion="Which approach is linear with O(h) extra space?",
        hint="A node deep in the right subtree must still be greater than the root.",
        choices=(
            Choice(
                "DFS with (low, high) bounds", OPTIMAL, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Pass allowed range down; left narrows high, right narrows low.",
                why="Each node must respect every ancestor, not just its parent. Carrying the valid range down encodes all those constraints at once.",
            ),
            Choice(
                "Check only parent vs. children", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Valid if left.val < node.val < right.val for every node.",
                why="In [5,1,6,null,null,3,7], each parent–child pair looks fine, but 3 sits in 5's right subtree. Is that allowed?",
            ),
            Choice(
                "In-order into an array", SUBOPTIMAL, time="O(n)", space="O(n)", visual="array-copy",
                detail="Traverse in-order, then check the list is strictly increasing.",
                why="Correct, but you store every value. Could you compare with just the previous value during traversal?",
            ),
            Choice(
                "Scan whole subtrees per node", SUBOPTIMAL, time="O(n²)", space="O(h)", visual="brute",
                detail="For each node, find max of left and min of right subtree.",
                why="Correct, but subtrees are rescanned for every ancestor. Bounds passed downward avoid that.",
            ),
        ),
    ),
    Question(
        slug="binary-tree-level-order-traversal", number=102, title="Binary Tree Level Order Traversal",
        difficulty="Medium", topics=("trees",),
        summary="Return the node values of a binary tree level by level, left to right.",
        example="[3, 9, 20, null, null, 15, 7]  →  [[3], [9, 20], [15, 7]]",
        criterion="Which approach is the standard answer?",
        hint="Which data structure naturally hands you nodes in the order they were discovered?",
        choices=(
            Choice(
                "BFS with a queue, one level at a time", OPTIMAL, time="O(n)", space="O(w)", visual="tree-bfs",
                detail="Process queue.size() nodes per level, enqueueing their children.",
                why="A queue returns nodes in discovery order, which is level order. Snapshotting the queue size separates one level from the next.",
            ),
            Choice(
                "Pre-order DFS output", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Visit root, left, right and output in that order.",
                why="Pre-order dives down the left side first — you'd see 3, 9, 20 only by luck. Try a deeper left subtree.",
            ),
            Choice(
                "One traversal per depth", SUBOPTIMAL, time="O(n·h)", space="O(h)", visual="brute",
                detail="For d = 0..h, walk the tree collecting nodes at depth d.",
                why="Correct, but the tree is walked once per level. One pass with a queue does all levels together.",
            ),
            Choice(
                "Stack-based traversal", INCORRECT, time="O(n)", space="O(h)", visual="stack",
                detail="Replace the queue with a stack.",
                why="A stack returns the most recent node first. Does that give left-to-right levels?",
            ),
        ),
    ),
    # ---------------------------------------------------------------- Tries
    Question(
        slug="implement-trie-prefix-tree", number=208, title="Implement Trie (Prefix Tree)",
        difficulty="Medium", topics=("data-structures",),
        summary="Design a structure supporting insert(word), search(word) and startsWith(prefix).",
        example="insert(\"apple\"), search(\"app\") → false, startsWith(\"app\") → true",
        criterion="Each operation should cost O(L) for a word of length L.",
        hint="Words that share a prefix could share storage for it.",
        choices=(
            Choice(
                "Trie nodes with child maps + end flag", OPTIMAL, time="O(L)", space="O(total chars)", visual="trie",
                detail="Each node maps a character to a child; mark nodes that end a word.",
                why="Shared prefixes share a path, so any prefix query is just walking L edges from the root.",
            ),
            Choice(
                "Hash set; scan for prefixes", SUBOPTIMAL, time="O(N·L) prefix", space="O(total chars)", visual="set",
                detail="search is a set lookup; startsWith checks every stored word.",
                why="search is fast, but startsWith scans all N words. What structure organizes words by prefix?",
            ),
            Choice(
                "Sorted list + binary search", SUBOPTIMAL, time="O(L log N)", space="O(total chars)", visual="binary-search",
                detail="Keep words sorted; binary search for the prefix's position.",
                why="Correct for queries, but inserting into a sorted list shifts elements, and each query still pays log N comparisons.",
            ),
            Choice(
                "One concatenated string + find()", INCORRECT, time="O(total chars)", space="O(total chars)", visual="array-copy",
                detail="Append all words into one string and search it.",
                why="After inserting 'car' and 'pet', would 'rpe' be found? Matches can span word boundaries.",
            ),
        ),
    ),
    Question(
        slug="word-search-ii", number=212, title="Word Search II",
        difficulty="Hard", topics=("data-structures", "trees"),
        summary="Given a letter grid and a list of words, return every word that can be traced through adjacent cells without reusing a cell.",
        example="board 4×4, words = [\"oath\",\"pea\",\"eat\",\"rain\"]  →  [\"eat\",\"oath\"]",
        criterion="Which approach scales to 3·10⁴ words?",
        hint="How can one DFS check many words at once?",
        choices=(
            Choice(
                "Trie of words + one grid DFS", OPTIMAL, time="O(m·n·3^L)", space="O(total chars)", visual="trie",
                detail="Build a trie; DFS from each cell following trie edges, pruning dead prefixes.",
                why="A trie lets a single DFS track all words sharing a prefix, and it stops the moment no word continues. The word count no longer multiplies the search.",
            ),
            Choice(
                "Word Search I for each word", SUBOPTIMAL, time="O(W·m·n·3^L)", space="O(L)", visual="backtrack",
                detail="Run a separate grid DFS for every word.",
                why="Correct, but with 3·10⁴ words you repeat nearly the same DFS thousands of times.",
            ),
            Choice(
                "Sorted words + binary-searched prefixes", SUBOPTIMAL, time="O(m·n·3^L·L log W)", space="O(total chars)", visual="binary-search",
                detail="DFS the grid; at each step binary search the sorted list to check the prefix exists.",
                why="It prunes correctly, but every step pays a binary search with string comparisons. A trie step is O(1).",
            ),
            Choice(
                "BFS allowing cell reuse", INCORRECT, time="O(m·n·W)", space="O(m·n)", visual="graph-bfs",
                detail="BFS from each cell over neighbors, matching letters.",
                why="The rules forbid reusing a cell in one word. Plain BFS can't track per-path visited cells.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- Heap
    Question(
        slug="kth-largest-element-in-an-array", number=215, title="Kth Largest Element in an Array",
        difficulty="Medium", topics=("data-structures",),
        summary="Return the k-th largest value in an unsorted array (by sorted position, duplicates count).",
        example="[3,2,1,5,6,4], k = 2  →  5",
        criterion="Which approach is the standard answer with guaranteed performance when k ≪ n?",
        hint="Do you need all values ordered, or just a running set of the k best?",
        choices=(
            Choice(
                "Min-heap of size k", OPTIMAL, time="O(n log k)", space="O(k)", visual="heap",
                detail="Push each value; pop when size exceeds k; the top is the answer.",
                why="The heap's smallest element is the k-th largest seen so far. Anything smaller can never matter, so the heap stays tiny.",
            ),
            Choice(
                "Sort, take index k−1 from the end", SUBOPTIMAL, time="O(n log n)", space="O(1)", visual="sort",
                detail="Sort the whole array.",
                why="Correct and short, but you order all n elements to read one. How much of that is needed?",
            ),
            Choice(
                "Remove the max k times", SUBOPTIMAL, time="O(n·k)", space="O(1)", visual="brute",
                detail="Scan for the max, remove it, repeat k times.",
                why="Correct, but each round rescans. A heap keeps candidates organized between rounds.",
            ),
            Choice(
                "Put values in a set, then rank", INCORRECT, time="O(n log n)", space="O(n)", visual="set",
                detail="Deduplicate into a sorted set and take the k-th largest.",
                why="Duplicates count here: in [3,3,1], the 2nd largest is 3. A set would say 1.",
            ),
        ),
    ),
    Question(
        slug="merge-k-sorted-lists", number=23, title="Merge k Sorted Lists",
        difficulty="Hard", topics=("data-structures", "trees"),
        summary="Merge k sorted linked lists into one sorted linked list.",
        example="[1→4→5, 1→3→4, 2→6]  →  1→1→2→3→4→4→5→6",
        criterion="Which approach is best for N total nodes across k lists?",
        hint="At every step, the next node is the smallest among k candidates.",
        choices=(
            Choice(
                "Min-heap of list heads", OPTIMAL, time="O(N log k)", space="O(k)", visual="heap",
                detail="Push each head; pop the smallest, append it, push its next.",
                why="Only the k current heads can be next. A heap returns the smallest in log k, and each node passes through it once.",
            ),
            Choice(
                "Merge lists one at a time", SUBOPTIMAL, time="O(N·k)", space="O(1)", visual="linked-list",
                detail="Fold: merge list 1 with 2, the result with 3, and so on.",
                why="Correct, but early nodes get re-walked in every later merge. Could you compare all heads at once?",
            ),
            Choice(
                "Collect all values and sort", SUBOPTIMAL, time="O(N log N)", space="O(N)", visual="sort",
                detail="Dump into an array, sort, rebuild a list.",
                why="Correct, but each list is already sorted — that structure is wasted.",
            ),
            Choice(
                "Concatenate the lists", INCORRECT, time="O(N)", space="O(1)", visual="linked-list",
                detail="Link the tail of each list to the next head.",
                why="1→4→5 followed by 1→3→4 isn't sorted. Concatenation ignores values across lists.",
            ),
        ),
    ),
    Question(
        slug="k-closest-points-to-origin", number=973, title="K Closest Points to Origin",
        difficulty="Medium", topics=("data-structures",),
        summary="Return the k points closest to (0, 0) by Euclidean distance.",
        example="[[1,3], [-2,2]], k = 1  →  [[-2,2]]",
        criterion="Which approach is best when k ≪ n?",
        hint="Keep only the best k seen so far — which one do you throw out?",
        choices=(
            Choice(
                "Max-heap of size k by distance", OPTIMAL, time="O(n log k)", space="O(k)", visual="heap",
                detail="Push each point; pop the farthest when size exceeds k.",
                why="The farthest of your current k is the one to evict. A max-heap exposes exactly that, keeping each step at log k.",
            ),
            Choice(
                "Sort all by distance", SUBOPTIMAL, time="O(n log n)", space="O(n)", visual="sort",
                detail="Sort by x² + y² and take the first k.",
                why="Correct, but it orders every point when only k are needed.",
            ),
            Choice(
                "Pick the closest k times", SUBOPTIMAL, time="O(n·k)", space="O(n)", visual="brute",
                detail="Scan for the nearest remaining point, k rounds.",
                why="Correct, but each round rescans all points.",
            ),
            Choice(
                "Smallest |x| + |y|", INCORRECT, time="O(n log n)", space="O(n)", visual="math",
                detail="Rank points by Manhattan distance.",
                why="(3,0) and (2,2): Manhattan says 3 < 4, Euclidean says 3 > 2.83. Different metric, different answer.",
            ),
        ),
    ),
    Question(
        slug="find-median-from-data-stream", number=295, title="Find Median from Data Stream",
        difficulty="Hard", topics=("data-structures",),
        summary="Design a structure that accepts numbers one at a time and can report the median of everything seen so far.",
        example="add 1, add 2 → median 1.5, add 3 → median 2",
        criterion="Which design has the best addNum / findMedian costs?",
        hint="The median splits the data into a lower half and an upper half.",
        choices=(
            Choice(
                "Two heaps (max-heap low, min-heap high)", OPTIMAL, time="O(log n) add, O(1) median", space="O(n)", visual="heap",
                detail="Keep halves balanced; the median is at the tops.",
                why="You only need the largest of the lower half and the smallest of the upper half. Two heaps expose exactly those two values.",
            ),
            Choice(
                "Sorted array with insertion", SUBOPTIMAL, time="O(n) add", space="O(n)", visual="binary-search",
                detail="Binary search the position, insert, read the middle.",
                why="The search is log n, but inserting into an array shifts elements. What structure avoids the shift?",
            ),
            Choice(
                "Sort on every query", SUBOPTIMAL, time="O(n log n) median", space="O(n)", visual="sort",
                detail="Append on add; sort before reading the middle.",
                why="Correct, but frequent queries re-sort nearly identical data.",
            ),
            Choice(
                "Running average", INCORRECT, time="O(1)", space="O(1)", visual="math",
                detail="Track sum and count; report sum / count.",
                why="Mean and median differ: for [1, 2, 100], the mean is 34.3, the median is 2.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- Backtracking
    Question(
        slug="subsets", number=78, title="Subsets",
        difficulty="Medium", topics=("trees",),
        summary="Return every subset (the power set) of an array of distinct integers.",
        example="[1, 2, 3]  →  [[], [1], [2], [1,2], [3], [1,3], [2,3], [1,2,3]]",
        criterion="Which approach generates each subset exactly once?",
        hint="For each element, there are exactly two choices.",
        choices=(
            Choice(
                "Backtracking: include / exclude", OPTIMAL, time="O(n·2ⁿ)", space="O(n)", visual="backtrack",
                detail="Recurse over indices; branch on taking or skipping each element.",
                why="Each element is either in or out, so the choices form a binary tree with 2ⁿ leaves — one per subset, none repeated.",
            ),
            Choice(
                "All permutations, dedupe as sets", SUBOPTIMAL, time="O(n·n!)", space="O(n·2ⁿ)", visual="brute",
                detail="Generate every ordering of every length, then remove duplicates.",
                why="It finds every subset, but orderings are irrelevant for subsets — n! explodes far past 2ⁿ.",
            ),
            Choice(
                "All contiguous subarrays", INCORRECT, time="O(n³)", space="O(n²)", visual="sliding-window",
                detail="Take every nums[i..j].",
                why="Is [1, 3] a subarray of [1, 2, 3]? No, but it is a subset.",
            ),
            Choice(
                "Empty set, singles and pairs", INCORRECT, time="O(n²)", space="O(n²)", visual="brute",
                detail="Output subsets of size 0, 1 and 2.",
                why="What about [1, 2, 3]? Subsets can be any size up to n.",
            ),
        ),
    ),
    Question(
        slug="combination-sum", number=39, title="Combination Sum",
        difficulty="Medium", topics=("trees",),
        summary="Given distinct positive candidates and a target, list every combination (numbers may repeat) that sums to the target.",
        example="candidates = [2,3,6,7], target = 7  →  [[2,2,3], [7]]",
        criterion="Which approach lists every combination without duplicates?",
        hint="How do you avoid generating [2,3,2] after [2,2,3]?",
        choices=(
            Choice(
                "Backtracking with a start index", OPTIMAL, time="O(n^(T/min))", space="O(T/min)", visual="backtrack",
                detail="Recurse from index i (reuse allowed), stop when the sum exceeds the target.",
                why="Only choosing candidates at or after the current index keeps each combination in non-decreasing order, so duplicates never appear. Overshooting prunes a branch.",
            ),
            Choice(
                "Enumerate all sequences, then dedupe", SUBOPTIMAL, time="O(n^(T/min)·T)", space="O(n^(T/min))", visual="brute",
                detail="Generate every sequence up to length T/min, sort each, keep unique.",
                why="Correct, but orderings multiply the work and you still pay to dedupe. The start index prevents duplicates up front.",
            ),
            Choice(
                "Greedy: largest candidate first", INCORRECT, time="O(T)", space="O(1)", visual="greedy",
                detail="Take the largest candidate that fits until you reach the target.",
                why="Greedy finds at most one combination and may miss the target: candidates [3,5], target 9 → 5 + 3 leaves 1, but 3+3+3 works.",
            ),
            Choice(
                "Coin-change DP table", INCORRECT, time="O(n·T)", space="O(T)", visual="dp-1d",
                detail="dp[s] = number of ways to make s.",
                why="That counts combinations but doesn't list them. The problem asks for the actual lists.",
            ),
        ),
    ),
    Question(
        slug="word-search", number=79, title="Word Search",
        difficulty="Medium", topics=("trees", "grid"),
        summary="Decide whether a word can be traced through horizontally or vertically adjacent cells of a grid, using each cell at most once.",
        example="board 3×4, word = \"ABCCED\"  →  true",
        criterion="Which approach correctly respects the no-reuse rule efficiently?",
        hint="Mark a cell while it's on the current path, and unmark it when you back out.",
        choices=(
            Choice(
                "DFS backtracking with visited marks", OPTIMAL, time="O(m·n·3^L)", space="O(L)", visual="backtrack",
                detail="From each matching cell, DFS to neighbors, marking/unmarking cells on the path.",
                why="Each step has at most three new directions (you can't go back), and you stop as soon as a letter mismatches.",
            ),
            Choice(
                "Enumerate all paths of length L", SUBOPTIMAL, time="O(m·n·4^L)", space="O(L)", visual="brute",
                detail="Generate every path of length L from each cell, then compare to the word.",
                why="Correct, but it explores paths that went wrong at the first letter. Comparing as you go prunes them.",
            ),
            Choice(
                "BFS with a global visited set", INCORRECT, time="O(m·n)", space="O(m·n)", visual="graph-bfs",
                detail="BFS from the start cell, never revisiting any cell.",
                why="A cell used by one failed path might be needed by another. A global visited set blocks it forever.",
            ),
            Choice(
                "Compare letter counts", INCORRECT, time="O(m·n)", space="O(Σ)", visual="counting",
                detail="True if the grid has enough of each letter.",
                why="Having the letters isn't the same as having them adjacent in the right order.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- Graphs
    Question(
        slug="number-of-islands", number=200, title="Number of Islands",
        difficulty="Medium", topics=("grid",),
        summary="Count the connected groups of '1' cells (land) in a grid, connecting horizontally and vertically.",
        example="[[\"1\",\"1\",\"0\"],[\"1\",\"0\",\"0\"],[\"0\",\"0\",\"1\"]]  →  2",
        criterion="Which approach is the standard linear answer?",
        hint="When you find unvisited land, how do you claim the whole island at once?",
        choices=(
            Choice(
                "Flood fill (DFS/BFS) with marking", OPTIMAL, time="O(m·n)", space="O(m·n)", visual="graph-dfs",
                detail="On each unvisited '1', count an island and sink every connected land cell.",
                why="Each island is one connected component. Flood filling marks it so it's counted once, and each cell is visited a constant number of times.",
            ),
            Choice(
                "Count all '1' cells", INCORRECT, time="O(m·n)", space="O(1)", visual="counting",
                detail="Return the number of land cells.",
                why="An island of four cells counts as one island, not four.",
            ),
            Choice(
                "Count top-left corners", INCORRECT, time="O(m·n)", space="O(1)", visual="matrix",
                detail="Count land cells whose up and left neighbors are water.",
                why="A U-shaped island has two such 'corners'. Local checks can't see how cells connect further away.",
            ),
            Choice(
                "BFS per cell, no global marks", SUBOPTIMAL, time="O((m·n)²)", space="O(m·n)", visual="graph-bfs",
                detail="From every land cell, BFS its island and dedupe islands by their cell sets.",
                why="Correct in the end, but every cell re-explores its whole island. Marking once avoids the repetition.",
            ),
        ),
    ),
    Question(
        slug="course-schedule", number=207, title="Course Schedule",
        difficulty="Medium", topics=("graphs",),
        summary="Given course prerequisites as pairs, decide whether it is possible to finish every course.",
        example="n = 2, [[1,0],[0,1]]  →  false",
        criterion="Which approach is linear in courses + prerequisites?",
        hint="When is it impossible to take courses in some order?",
        choices=(
            Choice(
                "Topological sort (Kahn's BFS)", OPTIMAL, time="O(V+E)", space="O(V+E)", visual="topo",
                detail="Repeatedly take courses with no remaining prerequisites; success if all are taken.",
                why="A valid order exists exactly when the graph has no cycle. Kahn's algorithm peels off prerequisite-free courses and gets stuck only on a cycle.",
            ),
            Choice(
                "Check only mutual pairs", INCORRECT, time="O(E)", space="O(E)", visual="hashmap",
                detail="Fail if some a→b and b→a both exist.",
                why="Cycles can be longer: 0→1→2→0 has no mutual pair.",
            ),
            Choice(
                "DFS from every course without memo", SUBOPTIMAL, time="O(V·(V+E))", space="O(V)", visual="graph-dfs",
                detail="For each course, DFS to see if it can reach itself.",
                why="Correct, but the same subgraphs are re-explored from every start. Coloring nodes as done avoids that.",
            ),
            Choice(
                "Take courses in numeric order", INCORRECT, time="O(V)", space="O(1)", visual="sort",
                detail="Assume course numbers are a valid order.",
                why="Nothing says lower-numbered courses come first. [[0,1]] means 1 must precede 0.",
            ),
        ),
    ),
    Question(
        slug="rotting-oranges", number=994, title="Rotting Oranges",
        difficulty="Medium", topics=("grid",),
        summary="Each minute, rotten oranges rot their fresh 4-directional neighbors. Return the minutes until no fresh orange remains, or −1 if impossible.",
        example="[[2,1,1],[1,1,0],[0,1,1]]  →  4",
        criterion="Which approach is linear in the grid size?",
        hint="All rotten oranges spread at the same time.",
        choices=(
            Choice(
                "Multi-source BFS", OPTIMAL, time="O(m·n)", space="O(m·n)", visual="graph-bfs",
                detail="Enqueue every rotten orange at time 0, BFS level by level.",
                why="Starting BFS from all sources together simulates simultaneous spreading. Each level is one minute and each cell is processed once.",
            ),
            Choice(
                "Simulate minute by minute", SUBOPTIMAL, time="O((m·n)²)", space="O(m·n)", visual="matrix",
                detail="Each minute, scan the grid and rot neighbors of rotten cells.",
                why="Correct, but each minute rescans cells that can't change. A queue only touches the frontier.",
            ),
            Choice(
                "Deepest DFS from each rotten orange", INCORRECT, time="O(m·n)", space="O(m·n)", visual="graph-dfs",
                detail="Run DFS from each rotten cell; report the largest recursion depth.",
                why="DFS depth isn't shortest distance — it can snake along long paths. Rot spreads by shortest paths.",
            ),
            Choice(
                "Count the fresh oranges", INCORRECT, time="O(m·n)", space="O(1)", visual="counting",
                detail="Return the number of fresh oranges.",
                why="Many oranges can rot in the same minute. The answer is a time, not a count.",
            ),
        ),
    ),
    Question(
        slug="clone-graph", number=133, title="Clone Graph",
        difficulty="Medium", topics=("graphs",),
        summary="Return a deep copy of a connected undirected graph given one of its nodes.",
        example="adjacency [[2,4],[1,3],[2,4],[1,3]]  →  identical structure, new nodes",
        criterion="Which approach is linear and handles cycles?",
        hint="How do you avoid cloning the same node twice?",
        choices=(
            Choice(
                "DFS/BFS with old → new map", OPTIMAL, time="O(V+E)", space="O(V)", visual="graph-dfs",
                detail="Clone each node once; look up clones in a map when wiring neighbors.",
                why="The map says whether a node was already copied, which both stops infinite loops on cycles and makes shared neighbors point to one clone.",
            ),
            Choice(
                "Copy nodes, keep neighbor references", INCORRECT, time="O(V)", space="O(V)", visual="array-copy",
                detail="Create new nodes but reuse the original neighbor lists.",
                why="The copies would point at original nodes — that's a shallow copy, not a deep one.",
            ),
            Choice(
                "Recursive clone without memo", INCORRECT, time="∞ on cycles", space="—", visual="recursion",
                detail="clone(node) creates a node and clones each neighbor.",
                why="In an undirected graph, 1 → 2 → 1 → 2 … Without remembering visited nodes, does recursion ever stop?",
            ),
            Choice(
                "Serialize, then rebuild by searching", SUBOPTIMAL, time="O(V·E)", space="O(V+E)", visual="brute",
                detail="Write an adjacency list, create nodes, then find each neighbor by scanning the node list.",
                why="Correct, but each neighbor lookup is a linear search. A map makes it O(1).",
            ),
        ),
    ),
    # ---------------------------------------------------------------- Advanced Graphs
    Question(
        slug="network-delay-time", number=743, title="Network Delay Time",
        difficulty="Medium", topics=("graphs", "data-structures"),
        summary="A signal starts at node k in a directed graph with positive edge travel times. Return the time for all nodes to receive it, or −1.",
        example="times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2  →  2",
        criterion="Which approach is best for positive weights?",
        hint="You need the shortest weighted distance to every node; the answer is the largest of them.",
        choices=(
            Choice(
                "Dijkstra with a min-heap", OPTIMAL, time="O(E log V)", space="O(V+E)", visual="dijkstra",
                detail="Pop the closest unsettled node, relax its edges.",
                why="With positive weights, the closest unsettled node's distance is final. The heap always hands you that node next.",
            ),
            Choice(
                "Bellman–Ford", SUBOPTIMAL, time="O(V·E)", space="O(V)", visual="graph-bfs",
                detail="Relax every edge V−1 times.",
                why="Correct (and handles negative edges), but with positive weights that generality costs a factor of V.",
            ),
            Choice(
                "Plain BFS counting hops", INCORRECT, time="O(V+E)", space="O(V)", visual="graph-bfs",
                detail="BFS from k; the time is the number of levels.",
                why="Edges have different travel times. A two-hop path can be faster than a one-hop path.",
            ),
            Choice(
                "Floyd–Warshall", SUBOPTIMAL, time="O(V³)", space="O(V²)", visual="dp-2d",
                detail="All-pairs shortest paths, then read row k.",
                why="Correct, but it computes distances from every source. You only need one.",
            ),
        ),
    ),
    Question(
        slug="min-cost-to-connect-all-points", number=1584, title="Min Cost to Connect All Points",
        difficulty="Medium", topics=("graphs",),
        summary="Connect all 2-D points so any two are linked by some path, minimizing total Manhattan edge length.",
        example="[[0,0],[2,2],[3,10],[5,2],[7,0]]  →  20",
        criterion="Which approach is the standard answer?",
        hint="You need a minimum spanning tree over a complete graph.",
        choices=(
            Choice(
                "Prim's algorithm with a min-heap", OPTIMAL, time="O(n² log n)", space="O(n²)", visual="dijkstra",
                detail="Grow a tree from one point; always add the cheapest edge to a new point.",
                why="The cheapest edge leaving the current tree is always safe to add (cut property). A heap finds it quickly.",
            ),
            Choice(
                "Connect each point to its nearest", INCORRECT, time="O(n²)", space="O(n)", visual="greedy",
                detail="Add an edge from every point to its closest neighbor.",
                why="Two tight clusters far apart would each link internally and never connect to each other.",
            ),
            Choice(
                "Dijkstra tree from point 0", INCORRECT, time="O(n² log n)", space="O(n²)", visual="dijkstra",
                detail="Use shortest paths from point 0 as the network.",
                why="Shortest-path trees minimize distance from one source, not total edge length. They can cost more than the MST.",
            ),
            Choice(
                "Try all spanning trees", SUBOPTIMAL, time="O(n^(n−2))", space="O(n)", visual="brute",
                detail="Enumerate spanning trees and keep the cheapest.",
                why="Cayley's formula says there are n^(n−2) of them. Correct, but only for tiny n.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- Intervals
    Question(
        slug="merge-intervals", number=56, title="Merge Intervals",
        difficulty="Medium", topics=("greedy",),
        summary="Merge all overlapping intervals and return the non-overlapping result.",
        example="[[1,3],[2,6],[8,10],[15,18]]  →  [[1,6],[8,10],[15,18]]",
        criterion="Which approach is the standard answer?",
        hint="After a certain sort, which interval can the next one possibly overlap?",
        choices=(
            Choice(
                "Sort by start, merge in one pass", OPTIMAL, time="O(n log n)", space="O(n)", visual="intervals",
                detail="Extend the last merged interval if the next starts within it; otherwise append.",
                why="Sorted by start, an interval can only overlap the most recent merged block. One comparison per interval does the rest.",
            ),
            Choice(
                "Merge any overlapping pair repeatedly", SUBOPTIMAL, time="O(n³)", space="O(n)", visual="brute",
                detail="Scan pairs, merge overlaps, repeat until nothing changes.",
                why="Correct in the end, but each pass checks all pairs and many passes may be needed.",
            ),
            Choice(
                "Mark integers on a number line", INCORRECT, time="O(n + range)", space="O(range)", visual="array-copy",
                detail="Mark every covered integer, then read runs.",
                why="[1,2] and [3,4] don't overlap, but marking integers makes 1–4 look like one run.",
            ),
            Choice(
                "Sort by end, merge with the last", INCORRECT, time="O(n log n)", space="O(n)", visual="sort",
                detail="Sort by end point, then merge adjacent overlaps.",
                why="Try [[2,3],[4,5],[1,10]]: sorted by end, [1,10] only meets [4,5] and leaves [2,3] unmerged.",
            ),
        ),
    ),
    Question(
        slug="meeting-rooms-ii", number=253, title="Meeting Rooms II",
        difficulty="Medium", topics=("data-structures", "greedy"),
        summary="Given meeting time intervals, return the minimum number of rooms needed so no meetings overlap in the same room.",
        example="[[0,30],[5,10],[15,20]]  →  2",
        criterion="Which approach is the standard answer?",
        hint="When a meeting starts, which ongoing meeting will free its room first?",
        choices=(
            Choice(
                "Sort by start + min-heap of end times", OPTIMAL, time="O(n log n)", space="O(n)", visual="heap",
                detail="For each meeting, free the earliest-ending room if it's done, then push this end time.",
                why="The heap's top is the room that frees up soonest. If it's not free yet, no room is, so you need a new one. The heap size is the answer.",
            ),
            Choice(
                "Max pairwise-overlap count", INCORRECT, time="O(n²)", space="O(1)", visual="brute",
                detail="For each meeting, count meetings overlapping it; return the max + 1.",
                why="[0,5], [4,7], [6,10]: the middle meeting overlaps two others, so this answers 3 — but the outer two never overlap, so 2 rooms suffice.",
            ),
            Choice(
                "Timeline counter per minute", SUBOPTIMAL, time="O(n·T)", space="O(T)", visual="array-copy",
                detail="Increment every minute a meeting covers; return the max.",
                why="Correct, but the cost depends on the time range T, which can be huge. Only start and end events matter.",
            ),
            Choice(
                "Assign to first free room by scan", SUBOPTIMAL, time="O(n·r)", space="O(r)", visual="greedy",
                detail="Sort by start; scan rooms for one whose last meeting ended.",
                why="Correct, but scanning rooms is linear. A heap finds the earliest-free room in log time.",
            ),
        ),
    ),
    Question(
        slug="non-overlapping-intervals", number=435, title="Non-overlapping Intervals",
        difficulty="Medium", topics=("greedy",),
        summary="Return the minimum number of intervals to remove so the rest do not overlap.",
        example="[[1,2],[2,3],[3,4],[1,3]]  →  1",
        criterion="Which approach is best for n up to 10⁵?",
        hint="To fit as many intervals as possible, which one should you keep first?",
        choices=(
            Choice(
                "Sort by end, keep earliest finishers", OPTIMAL, time="O(n log n)", space="O(1)", visual="greedy",
                detail="Keep an interval if it starts after the last kept end; count the rest.",
                why="Finishing earliest leaves the most room for everything after. Keeping the maximum set means removing the minimum.",
            ),
            Choice(
                "Sort by start, keep the first", INCORRECT, time="O(n log n)", space="O(1)", visual="sort",
                detail="Keep each interval that starts after the last kept one; skip others.",
                why="[[1,100],[2,3],[4,5]] keeps [1,100] and removes two, but removing just [1,100] is enough.",
            ),
            Choice(
                "DP over sorted intervals (LIS-style)", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="dp-1d",
                detail="dp[i] = most compatible intervals ending with i.",
                why="Correct, but quadratic. The greedy exchange argument shows DP isn't needed.",
            ),
            Choice(
                "Remove the longest repeatedly", INCORRECT, time="O(n²)", space="O(n)", visual="brute",
                detail="While overlaps exist, remove the longest interval.",
                why="Length isn't what causes conflicts. A short interval can overlap many others.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- Greedy
    Question(
        slug="maximum-subarray", number=53, title="Maximum Subarray",
        difficulty="Medium", topics=("dp", "data-structures"),
        summary="Find the largest sum of any non-empty contiguous subarray.",
        example="[-2,1,-3,4,-1,2,1,-5,4]  →  6  ([4,-1,2,1])",
        criterion="Which approach is best for n up to 10⁵?",
        hint="When is a running prefix no longer worth keeping?",
        choices=(
            Choice(
                "Kadane's algorithm", OPTIMAL, time="O(n)", space="O(1)", visual="greedy",
                detail="cur = max(x, cur + x); track the best cur.",
                why="If the running sum drops below zero, would any future subarray want to include it? No — so restart. That's one pass.",
            ),
            Choice(
                "All subarrays with running sums", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="For each start, extend and track the best sum.",
                why="Correct, but many starts are never worth considering. Which ones can you discard?",
            ),
            Choice(
                "Divide and conquer", SUBOPTIMAL, time="O(n log n)", space="O(log n)", visual="recursion",
                detail="Best of left half, right half, or crossing the middle.",
                why="Correct and a classic, but it does log n levels of work that one linear pass avoids.",
            ),
            Choice(
                "Sum all positive numbers", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="Add every positive value.",
                why="The subarray must be contiguous. You can't skip the negative numbers in between.",
            ),
        ),
    ),
    Question(
        slug="jump-game", number=55, title="Jump Game",
        difficulty="Medium", topics=("greedy",),
        summary="Each value is the maximum jump length from that index. Decide whether you can reach the last index from the first.",
        example="[2,3,1,1,4] → true,  [3,2,1,0,4] → false",
        criterion="Which approach is best for n up to 10⁴?",
        hint="Instead of choosing jumps, track how far you could possibly reach.",
        choices=(
            Choice(
                "Greedy farthest reach", OPTIMAL, time="O(n)", space="O(1)", visual="greedy",
                detail="Scan; if i > reach fail, else reach = max(reach, i + nums[i]).",
                why="Every index up to reach is reachable, so you only need the maximum reach so far. One pass decides it.",
            ),
            Choice(
                "DP reachable array", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="dp-1d",
                detail="Mark each index reachable from any earlier reachable index.",
                why="Correct, but it checks every earlier index. The reachable set is always a prefix — one number describes it.",
            ),
            Choice(
                "Always take the maximum jump", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="From each index, jump as far as possible.",
                why="[2,3,0,1,4]: the max jump from index 0 lands on the 0 and gets stuck, while a 1-step jump reaches the 3 and then the end.",
            ),
            Choice(
                "Fail if the array contains a 0", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Any zero before the end blocks progress.",
                why="In [2,0,0], you can jump over the first 0 straight to the end.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- 1-D DP
    Question(
        slug="climbing-stairs", number=70, title="Climbing Stairs",
        difficulty="Easy", topics=("dp",),
        summary="You climb 1 or 2 steps at a time. Count the distinct ways to reach step n.",
        example="n = 3  →  3  (1+1+1, 1+2, 2+1)",
        criterion="Which approach is linear with O(1) space?",
        hint="How can you arrive at step n?",
        choices=(
            Choice(
                "Bottom-up DP with two variables", OPTIMAL, time="O(n)", space="O(1)", visual="dp-1d",
                detail="ways(n) = ways(n−1) + ways(n−2), keep only the last two.",
                why="Your last move was a 1-step or a 2-step, so ways(n) is the sum of the two previous counts. You only ever need two numbers.",
            ),
            Choice(
                "Plain recursion", SUBOPTIMAL, time="O(2ⁿ)", space="O(n)", visual="recursion",
                detail="Return f(n−1) + f(n−2) directly.",
                why="Correct, but f(n−2) is computed again inside f(n−1). The call tree explodes.",
            ),
            Choice(
                "Memoized recursion", SUBOPTIMAL, time="O(n)", space="O(n)", visual="recursion",
                detail="Cache f(k) as you recurse.",
                why="Linear time, but it keeps a cache and a call stack of size n. Do you need more than the last two values?",
            ),
            Choice(
                "n / 2 + 1", INCORRECT, time="O(1)", space="O(1)", visual="math",
                detail="Count how many 2-steps you could take.",
                why="That counts step mixes, not orderings: 1+2 and 2+1 are different ways.",
            ),
        ),
    ),
    Question(
        slug="house-robber", number=198, title="House Robber",
        difficulty="Medium", topics=("dp",),
        summary="Pick houses to rob for maximum money without ever robbing two adjacent houses.",
        example="[2, 7, 9, 3, 1]  →  12  (2 + 9 + 1)",
        criterion="Which approach is linear with O(1) space?",
        hint="At house i, you either rob it or you don't.",
        choices=(
            Choice(
                "DP rob/skip with two variables", OPTIMAL, time="O(n)", space="O(1)", visual="dp-1d",
                detail="best(i) = max(best(i−1), best(i−2) + money[i]).",
                why="Robbing i means you skipped i−1; skipping i means you keep best(i−1). Two running values capture both.",
            ),
            Choice(
                "Max of even vs. odd indices", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="Sum even-indexed houses and odd-indexed houses; take the larger.",
                why="[2,1,1,2]: evens = 3, odds = 3, but robbing houses 0 and 3 gives 4.",
            ),
            Choice(
                "Try all non-adjacent subsets", SUBOPTIMAL, time="O(2ⁿ)", space="O(n)", visual="backtrack",
                detail="Enumerate every valid selection.",
                why="Correct but exponential; the choices at i only depend on the best answers up to i−1 and i−2.",
            ),
            Choice(
                "Greedy: take the richest house first", INCORRECT, time="O(n log n)", space="O(n)", visual="greedy",
                detail="Repeatedly rob the largest remaining house and block its neighbors.",
                why="[3,4,3]: greedy takes 4, but 3 + 3 = 6 is better.",
            ),
        ),
    ),
    Question(
        slug="coin-change", number=322, title="Coin Change",
        difficulty="Medium", topics=("dp",),
        summary="Given coin denominations (unlimited supply) and an amount, return the fewest coins that sum to the amount, or −1.",
        example="coins = [1, 2, 5], amount = 11  →  3  (5 + 5 + 1)",
        criterion="Which approach is correct for arbitrary denominations?",
        hint="The best way to make amount a uses the best way to make a − c for some coin c.",
        choices=(
            Choice(
                "Bottom-up DP over amounts", OPTIMAL, time="O(amount·coins)", space="O(amount)", visual="dp-1d",
                detail="dp[a] = 1 + min(dp[a − c]) over coins c.",
                why="The last coin used is some c, and what remains must be made optimally. Filling amounts from 0 upward ensures every subproblem is ready.",
            ),
            Choice(
                "Greedy: largest coin first", INCORRECT, time="O(coins)", space="O(1)", visual="greedy",
                detail="Take as many of the largest coin as fit, then the next.",
                why="coins = [1,3,4], amount = 6: greedy gives 4+1+1 (3 coins), but 3+3 needs 2.",
            ),
            Choice(
                "Plain recursion over coins", SUBOPTIMAL, time="O(coins^amount)", space="O(amount)", visual="recursion",
                detail="Try every coin at every step, no caching.",
                why="Correct, but the same remaining amounts are solved again and again. Caching turns this into DP.",
            ),
            Choice(
                "DP using only the largest fitting coin", INCORRECT, time="O(amount)", space="O(amount)", visual="dp-1d",
                detail="dp[a] = 1 + dp[a − largest coin ≤ a].",
                why="That's the greedy choice dressed up as DP. It fails on the same [1,3,4], 6 example.",
            ),
        ),
    ),
    Question(
        slug="word-break", number=139, title="Word Break",
        difficulty="Medium", topics=("dp",),
        summary="Decide whether a string can be split into a sequence of dictionary words (words may be reused).",
        example="s = \"leetcode\", dict = [\"leet\", \"code\"]  →  true",
        criterion="Which approach is polynomial and correct?",
        hint="If the prefix s[0:i] can be split, what else do you need?",
        choices=(
            Choice(
                "DP over prefixes", OPTIMAL, time="O(n·W·L)", space="O(n)", visual="dp-1d",
                detail="dp[i] = true if some word w ends at i and dp[i − |w|] is true.",
                why="A split of s[0:i] ends with some word. If the part before it is splittable, so is s[0:i]. Each prefix is solved once.",
            ),
            Choice(
                "Greedy longest match", INCORRECT, time="O(n·W·L)", space="O(1)", visual="greedy",
                detail="Repeatedly strip the longest dictionary word from the front.",
                why="s = \"aaaaaa\", dict = [\"aaaa\", \"aaa\"]: greedy takes \"aaaa\" and is left with \"aa\", yet \"aaa\" + \"aaa\" works.",
            ),
            Choice(
                "Recursion without memoization", SUBOPTIMAL, time="O(2ⁿ)", space="O(n)", visual="recursion",
                detail="Try each word at the front and recurse on the rest.",
                why="Correct, but the same suffix is re-solved many times. Memoizing each start index gives the DP.",
            ),
            Choice(
                "Every character appears in some word", INCORRECT, time="O(n + W·L)", space="O(Σ)", visual="counting",
                detail="Check each letter occurs in the dictionary.",
                why="\"ab\" with dictionary [\"a\", \"bc\"] passes this check, but 'b' alone is not a word.",
            ),
        ),
    ),
    Question(
        slug="longest-increasing-subsequence", number=300, title="Longest Increasing Subsequence",
        difficulty="Medium", topics=("dp", "binary-search"),
        summary="Return the length of the longest strictly increasing subsequence (not necessarily contiguous).",
        example="[10, 9, 2, 5, 3, 7, 101, 18]  →  4  (2, 3, 7, 101)",
        criterion="The follow-up asks for better than O(n²). Which approach achieves it?",
        hint="For each length, keep the smallest possible tail value.",
        choices=(
            Choice(
                "Tails array + binary search", OPTIMAL, time="O(n log n)", space="O(n)", visual="binary-search",
                detail="tails[k] = smallest tail of an increasing run of length k+1; binary search to place each x.",
                why="A smaller tail can only help future extensions. tails stays sorted, so each value finds its slot by binary search.",
            ),
            Choice(
                "O(n²) DP", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="dp-1d",
                detail="dp[i] = 1 + max(dp[j]) for j < i with nums[j] < nums[i].",
                why="Correct and very common, but it doesn't meet the follow-up. Which information about earlier runs actually matters?",
            ),
            Choice(
                "Longest increasing contiguous run", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Scan for the longest stretch where each value increases.",
                why="A subsequence can skip elements: 2, 3, 7, 101 aren't adjacent in the input.",
            ),
            Choice(
                "Check every subsequence", SUBOPTIMAL, time="O(n·2ⁿ)", space="O(n)", visual="brute",
                detail="Enumerate all 2ⁿ subsequences.",
                why="Correct but exponential.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- 2-D DP
    Question(
        slug="unique-paths", number=62, title="Unique Paths",
        difficulty="Medium", topics=("dp",),
        summary="A robot moves only right or down on an m × n grid. Count the paths from the top-left to the bottom-right corner.",
        example="m = 3, n = 7  →  28",
        criterion="Which approach is the standard DP answer?",
        hint="How many ways are there to arrive at a cell?",
        choices=(
            Choice(
                "Grid DP (rolling row)", OPTIMAL, time="O(m·n)", space="O(n)", visual="dp-2d",
                detail="paths[r][c] = paths[r−1][c] + paths[r][c−1], keep one row.",
                why="You enter a cell from above or from the left, so its count is the sum of theirs. Each row only needs the previous row.",
            ),
            Choice(
                "Plain recursion", SUBOPTIMAL, time="O(2^(m+n))", space="O(m+n)", visual="recursion",
                detail="f(r, c) = f(r−1, c) + f(r, c−1) without caching.",
                why="Correct, but the same cells are recomputed exponentially many times.",
            ),
            Choice(
                "m × n", INCORRECT, time="O(1)", space="O(1)", visual="math",
                detail="Multiply the dimensions.",
                why="m·n counts cells, not paths. For a 3×7 grid, that's 21, but there are 28 paths.",
            ),
            Choice(
                "Only the two border paths", INCORRECT, time="O(1)", space="O(1)", visual="math",
                detail="Always 2: all right then down, or all down then right.",
                why="Paths can zig-zag: right, down, right, down … each is distinct.",
            ),
        ),
    ),
    Question(
        slug="longest-common-subsequence", number=1143, title="Longest Common Subsequence",
        difficulty="Medium", topics=("dp",),
        summary="Return the length of the longest subsequence common to two strings.",
        example="\"abcde\", \"ace\"  →  3  (\"ace\")",
        criterion="Which approach is the standard polynomial answer?",
        hint="Compare the last characters of the two prefixes.",
        choices=(
            Choice(
                "2-D DP over prefixes", OPTIMAL, time="O(m·n)", space="O(m·n)", visual="dp-2d",
                detail="dp[i][j] = dp[i−1][j−1] + 1 if chars match, else max(dp[i−1][j], dp[i][j−1]).",
                why="If the last characters match, they extend the LCS of the shorter prefixes; if not, one of them is dropped. Every prefix pair is solved once.",
            ),
            Choice(
                "Check every subsequence of one string", SUBOPTIMAL, time="O(2^m·n)", space="O(m)", visual="brute",
                detail="Enumerate subsequences of s1 and test each against s2.",
                why="Correct but exponential in m.",
            ),
            Choice(
                "Greedy first matches", INCORRECT, time="O(m·n)", space="O(1)", visual="greedy",
                detail="Walk s1; for each char, match its next occurrence in s2.",
                why="s1 = 'zabc', s2 = 'abcz': greedy matches 'z' to the end of s2 and finds nothing after it (1), but 'abc' gives 3.",
            ),
            Choice(
                "Longest common substring DP", INCORRECT, time="O(m·n)", space="O(m·n)", visual="dp-2d",
                detail="dp[i][j] = dp[i−1][j−1] + 1 on match, else 0.",
                why="Resetting to 0 forces contiguity. A subsequence may skip characters.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- Bit Manipulation
    Question(
        slug="single-number", number=136, title="Single Number",
        difficulty="Easy", topics=("bit-manipulation",),
        summary="Every value appears twice except one. Find the one that appears once.",
        example="[4, 1, 2, 1, 2]  →  4",
        criterion="Which approach is linear time with O(1) extra space?",
        hint="Which operation cancels a value with itself?",
        choices=(
            Choice(
                "XOR everything", OPTIMAL, time="O(n)", space="O(1)", visual="bits",
                detail="Fold the array with ^.",
                why="x ^ x = 0 and x ^ 0 = x, and XOR is order-independent. Every pair cancels, leaving the single value.",
            ),
            Choice(
                "Hash map counts", SUBOPTIMAL, time="O(n)", space="O(n)", visual="hashmap",
                detail="Count occurrences; return the value with count 1.",
                why="Correct, but it needs O(n) memory. Is there an operation where pairs cancel on their own?",
            ),
            Choice(
                "2·sum(set) − sum(array)", SUBOPTIMAL, time="O(n)", space="O(n)", visual="math",
                detail="Use distinct values to cancel duplicates arithmetically.",
                why="Clever and correct, but the set costs O(n) space.",
            ),
            Choice(
                "AND everything", INCORRECT, time="O(n)", space="O(1)", visual="bits",
                detail="Fold the array with &.",
                why="AND doesn't cancel duplicates: 4 & 1 & 2 & 1 & 2 = 0.",
            ),
        ),
    ),
    Question(
        slug="counting-bits", number=338, title="Counting Bits",
        difficulty="Easy", topics=("bit-manipulation", "dp"),
        summary="For every i from 0 to n, return the number of 1 bits in i.",
        example="n = 5  →  [0, 1, 1, 2, 1, 2]",
        criterion="The follow-up asks for a single O(n) pass. Which approach meets it?",
        hint="How does i relate to i >> 1?",
        choices=(
            Choice(
                "DP: bits[i] = bits[i >> 1] + (i & 1)", OPTIMAL, time="O(n)", space="O(n)", visual="bits",
                detail="Reuse the count of i with its last bit dropped.",
                why="Shifting right drops exactly the last bit. So i's count is its half's count plus that last bit — already computed.",
            ),
            Choice(
                "Count bits of each number", SUBOPTIMAL, time="O(n log n)", space="O(n)", visual="brute",
                detail="Loop over each bit of every i.",
                why="Correct, but it recounts bits that smaller numbers already counted.",
            ),
            Choice(
                "bits[i] = bits[i − 1] + 1", INCORRECT, time="O(n)", space="O(n)", visual="dp-1d",
                detail="Assume each increment adds one bit.",
                why="3 → 4 is 011 → 100: the count drops from 2 to 1. Carries clear bits.",
            ),
            Choice(
                "⌊log₂ i⌋ + 1", INCORRECT, time="O(n)", space="O(n)", visual="math",
                detail="Use the bit length.",
                why="That's how many bits i has, not how many are 1. 4 = 100 has length 3 but one 1.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- Math & Geometry
    Question(
        slug="rotate-image", number=48, title="Rotate Image",
        difficulty="Medium", topics=("math",),
        summary="Rotate an n × n matrix 90° clockwise in place.",
        example="[[1,2,3],[4,5,6],[7,8,9]]  →  [[7,4,1],[8,5,2],[9,6,3]]",
        criterion="The rotation must happen in place.",
        hint="Rotation can be decomposed into two simple reflections.",
        choices=(
            Choice(
                "Transpose, then reverse each row", OPTIMAL, time="O(n²)", space="O(1)", visual="matrix",
                detail="Swap across the diagonal, then reverse rows.",
                why="A transpose flips across the diagonal; reversing rows flips left–right. Together they make a clockwise rotation without extra memory.",
            ),
            Choice(
                "Copy into a new matrix", SUBOPTIMAL, time="O(n²)", space="O(n²)", visual="array-copy",
                detail="result[c][n−1−r] = m[r][c], then copy back.",
                why="Correct, but it uses a full second matrix, which the in-place requirement forbids.",
            ),
            Choice(
                "Reverse the rows only", INCORRECT, time="O(n²)", space="O(1)", visual="matrix",
                detail="Reverse each row.",
                why="That's a horizontal mirror, not a rotation. The first row stays on top.",
            ),
            Choice(
                "Transpose only", INCORRECT, time="O(n²)", space="O(1)", visual="matrix",
                detail="Swap across the diagonal.",
                why="A transpose is a reflection. 1 stays in the top-left corner, but a rotation moves it to the top-right.",
            ),
        ),
    ),
    Question(
        slug="powx-n", number=50, title="Pow(x, n)",
        difficulty="Medium", topics=("math", "bit-manipulation"),
        summary="Compute x raised to an integer power n, where n may be negative and as large as 2³¹ − 1 in magnitude.",
        example="x = 2.0, n = -2  →  0.25",
        criterion="Which approach handles |n| up to 2³¹?",
        hint="x⁸ = ((x²)²)².",
        choices=(
            Choice(
                "Exponentiation by squaring", OPTIMAL, time="O(log n)", space="O(1)", visual="bits",
                detail="Square x and halve n; multiply the result when n's low bit is 1. Invert for negative n.",
                why="Each squaring doubles the exponent covered, so about 31 steps reach 2³¹. Handling the sign by inverting x keeps it general.",
            ),
            Choice(
                "Multiply n times", SUBOPTIMAL, time="O(n)", space="O(1)", visual="brute",
                detail="Loop |n| times.",
                why="Correct, but 2³¹ multiplications is far too slow.",
            ),
            Choice(
                "Ignore the sign of n", INCORRECT, time="O(log n)", space="O(1)", visual="bits",
                detail="Compute x^|n|.",
                why="x^(−2) = 1/x². Dropping the sign returns x² instead.",
            ),
            Choice(
                "exp(n · ln x)", INCORRECT, time="O(1)", space="O(1)", visual="math",
                detail="Use logarithms.",
                why="ln x is undefined for negative x, so (−2)³ breaks; it also loses precision.",
            ),
        ),
    ),
]
