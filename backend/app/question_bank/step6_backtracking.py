"""Core route step 6: backtracking (链表、树与回溯 §2.7, §4)."""

from .question_schema import INCORRECT, OPTIMAL, SUBOPTIMAL, Choice, Question

QUESTIONS = [
    # ---------------------------------------------------------------- §2.7 backtracking on a binary tree
    Question(
        slug="binary-tree-paths", number=257, title="Binary Tree Paths",
        difficulty="Easy", topics=("trees",),
        summary="Return every root-to-leaf path of a binary tree as a string like \"1->2->5\".",
        example="[1,2,3,null,5]  →  [\"1->2->5\", \"1->3\"]",
        criterion="Which approach keeps extra space at O(h), not counting the output?",
        hint="Do you need a fresh copy of the path at every node, or only at the leaves?",
        choices=(
            Choice(
                "DFS with one shared path", OPTIMAL, time="O(n·h)", space="O(h)", visual="backtrack",
                detail="Push the node, recurse into children, pop on the way back; join the path at each leaf.",
                why="The path on the stack is always exactly root-to-current. Popping on return lets one list serve every branch, and only leaves pay for a copy.",
            ),
            Choice(
                "BFS carrying a path copy per node", SUBOPTIMAL, time="O(n·h)", space="O(n·h)", visual="tree-bfs",
                detail="Each queue entry holds its own copy of the path so far.",
                why="Correct, but a wide level puts up to n/2 paths of length h in the queue at once.",
            ),
            Choice(
                "Emit when a child is missing", INCORRECT, time="O(n·h)", space="O(h)", visual="tree-dfs",
                detail="Record the path whenever a node has a null left or right child.",
                why="In the example, node 2 has no left child but isn't a leaf. Should \"1->2\" be in the answer?",
            ),
            Choice(
                "Join the in-order traversal", INCORRECT, time="O(n)", space="O(n)", visual="recursion",
                detail="Visit nodes in order and split the sequence at leaves.",
                why="In-order visits 2 before 5 and 1 after it. Does any root-to-leaf path start anywhere but the root?",
            ),
        ),
    ),
    Question(
        slug="path-sum-ii", number=113, title="Path Sum II",
        difficulty="Medium", topics=("trees",),
        summary="Return every root-to-leaf path whose node values sum to targetSum. Values may be negative.",
        example="[5,4,8,11,null,13,4,7,2,null,null,5,1], 22  →  [[5,4,11,2], [5,8,4,5]]",
        criterion="Which approach keeps extra space at O(h), not counting the output?",
        hint="What do you carry down so a leaf can decide on its own?",
        choices=(
            Choice(
                "DFS with a shared path and remaining sum", OPTIMAL, time="O(n·h)", space="O(h)", visual="backtrack",
                detail="Subtract each value on the way down; at a leaf with 0 left, copy the path; pop on return.",
                why="The remaining sum tells each leaf whether its path works. Only matching paths are copied, and the shared path never grows past h.",
            ),
            Choice(
                "Collect all paths, then filter", SUBOPTIMAL, time="O(n·h)", space="O(n·h)", visual="tree-dfs",
                detail="Store every root-to-leaf path, then keep those that sum to the target.",
                why="Correct, but it stores paths that will be thrown away. How many leaves can a tree have?",
            ),
            Choice(
                "Prune when the sum passes the target", INCORRECT, time="O(n·h)", space="O(h)", visual="backtrack",
                detail="Stop going down once the running sum exceeds targetSum.",
                why="Values can be negative. Could 30 − 8 still reach 22 further down?",
            ),
            Choice(
                "Stop at the first match", INCORRECT, time="O(n·h)", space="O(h)", visual="tree-dfs",
                detail="Return the first root-to-leaf path that sums to the target.",
                why="The example has two matching paths. Which one would be missing?",
            ),
        ),
    ),
    Question(
        slug="pseudo-palindromic-paths-in-a-binary-tree", number=1457, title="Pseudo-Palindromic Paths in a Binary Tree",
        difficulty="Medium", topics=("trees",),
        summary="Node values are digits 1–9. A root-to-leaf path is pseudo-palindromic if its values can be rearranged into a palindrome. Count such paths.",
        example="[2,3,1,3,1,null,1]  →  2",
        criterion="Which approach is linear with O(h) extra space?",
        hint="A multiset can form a palindrome when at most how many values appear an odd number of times?",
        choices=(
            Choice(
                "DFS with a parity bitmask", OPTIMAL, time="O(n)", space="O(h)", visual="bits",
                detail="Flip bit v on entering a node; at a leaf, check mask & (mask − 1) == 0.",
                why="Only the parity of each digit matters. Nine bits hold it, flipping a bit is O(1), and the check passes when at most one bit is set.",
            ),
            Choice(
                "Recount the path at each leaf", SUBOPTIMAL, time="O(n·h)", space="O(h)", visual="counting",
                detail="Keep the path on a stack and count digit frequencies at every leaf.",
                why="Correct, but each leaf recounts up to h values the parent already saw.",
            ),
            Choice(
                "Check the path reads as a palindrome", INCORRECT, time="O(n·h)", space="O(h)", visual="two-pointers",
                detail="Compare the path with its reverse at each leaf.",
                why="2→3→3 isn't a palindrome, but 3,2,3 is. Is rearranging allowed?",
            ),
            Choice(
                "Require every count to be even", INCORRECT, time="O(n)", space="O(h)", visual="bits",
                detail="Count a leaf only when the mask is 0.",
                why="2→1→1 rearranges to 1,2,1. What sits in the middle of an odd-length palindrome?",
            ),
        ),
    ),
    Question(
        slug="path-sum-iii", number=437, title="Path Sum III",
        difficulty="Medium", topics=("trees",),
        summary="Count downward paths (starting at any node, ending at any descendant or itself) whose values sum to targetSum. Values may be negative.",
        example="[10,5,-3,3,2,null,11,3,-2,null,1], 8  →  3",
        criterion="Which approach is linear?",
        hint="A downward path is the difference of two root-to-node sums on the same branch.",
        choices=(
            Choice(
                "Prefix sums in a map, undone on return", OPTIMAL, time="O(n)", space="O(n)", visual="prefix",
                detail="At each node, add count[sum − target]; record sum, recurse, then remove it.",
                why="Every earlier prefix on the current branch is a possible start. Removing a prefix on the way back keeps sums from other branches out of the map.",
            ),
            Choice(
                "Path sums from every node", SUBOPTIMAL, time="O(n·h)", space="O(h)", visual="brute",
                detail="For each node, DFS down counting paths that start there.",
                why="Correct, but a node at depth d is re-added d times. On a chain, that's O(n²).",
            ),
            Choice(
                "Sliding window on the branch", INCORRECT, time="O(n)", space="O(h)", visual="sliding-window",
                detail="Shrink the window from the top while its sum exceeds the target.",
                why="With −3 and −2 in the tree, can adding a node make the sum smaller?",
            ),
            Choice(
                "One prefix map for the whole tree", INCORRECT, time="O(n)", space="O(n)", visual="hashmap",
                detail="Record every prefix sum ever seen and never remove it.",
                why="A prefix from a left branch would pair with a node on the right. Is that a downward path?",
            ),
        ),
    ),
    Question(
        slug="maximum-distinct-path-sum-in-a-binary-tree", number=3879, title="Maximum Distinct Path Sum in a Binary Tree",
        difficulty="Medium", topics=("trees",),
        summary="A path may start and end at any nodes; no value may repeat along it. Return the largest path sum. n ≤ 1000, values may be negative.",
        example="[1,-2,5,null,null,3,5]  →  9",
        criterion="Which approach is O(n²) and respects the distinct-value rule?",
        hint="With values allowed to repeat, can a single bottom-up pass know which values a path already uses?",
        choices=(
            Choice(
                "DFS from every node with a value set", OPTIMAL, time="O(n²)", space="O(n)", visual="backtrack",
                detail="Treat the tree as an undirected graph; from each start, extend while the next value is unused, adding and removing it from a set.",
                why="Each start explores at most n nodes, and the set makes the repeat check O(1). The set is undone on return, so branches don't see each other's values.",
            ),
            Choice(
                "Walk the path for every pair", SUBOPTIMAL, time="O(n²·h)", space="O(h)", visual="brute",
                detail="For each pair of nodes, find the path through their LCA and check it.",
                why="Correct, but the paths from one start share prefixes. Why rebuild each from scratch?",
            ),
            Choice(
                "Max path sum, single pass", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Return the best downward sum per node and combine two children, as in Max Path Sum.",
                why="It would take 1 → 5 → 5 for 11. Does that path repeat a value?",
            ),
            Choice(
                "Skip repeated values", INCORRECT, time="O(n)", space="O(n)", visual="set",
                detail="Run the single pass but treat a repeated value as 0.",
                why="A path is contiguous. Can it pass through the second 5 without using it?",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §4.1 subset backtracking
    Question(
        slug="subsets", number=78, title="Subsets",
        difficulty="Medium", topics=("trees",),
        summary="Given distinct integers, return every subset (the power set) in any order.",
        example="[1,2,3]  →  [[], [1], [2], [1,2], [3], [1,3], [2,3], [1,2,3]]",
        criterion="Which approach runs in O(n·2ⁿ)?",
        hint="For each element there are two choices. How many leaves does that tree have?",
        choices=(
            Choice(
                "Include or skip each element", OPTIMAL, time="O(n·2ⁿ)", space="O(n)", visual="backtrack",
                detail="At index i, recurse once without nums[i] and once with it; record the path at i = n.",
                why="Each subset is one leaf of a depth-n binary tree, reached exactly once. Copying it costs O(n).",
            ),
            Choice(
                "Permute, then dedupe as sets", SUBOPTIMAL, time="O(n·n!)", space="O(n·2ⁿ)", visual="brute",
                detail="Take every prefix of every permutation, sort it and add it to a set.",
                why="Correct, but n! orderings collapse to 2ⁿ subsets. Does order matter in a subset?",
            ),
            Choice(
                "All contiguous slices", INCORRECT, time="O(n³)", space="O(n)", visual="sliding-window",
                detail="Return nums[i..j] for every i ≤ j, plus the empty set.",
                why="Where is [1, 3]?",
            ),
            Choice(
                "Every pair plus singles", INCORRECT, time="O(n²)", space="O(n)", visual="brute",
                detail="Return the empty set, each element, and each pair.",
                why="Where is [1, 2, 3]?",
            ),
        ),
    ),
    Question(
        slug="sum-of-all-subset-xor-totals", number=1863, title="Sum of All Subset XOR Totals",
        difficulty="Easy", topics=("trees",),
        summary="The XOR total of an array is the XOR of its elements (0 if empty). Return the sum of XOR totals over every subset of nums. n ≤ 12.",
        example="[5,1,6]  →  28",
        criterion="Which approach is linear?",
        hint="Take one bit that some element has. In how many subsets is that bit set in the XOR?",
        choices=(
            Choice(
                "OR of all, times 2ⁿ⁻¹", OPTIMAL, time="O(n)", space="O(1)", visual="bits",
                detail="Return (nums[0] | nums[1] | …) << (n − 1).",
                why="For a bit some element has, flipping that element's membership toggles the bit, so exactly half of the 2ⁿ subsets have it. Bits no element has are never set.",
            ),
            Choice(
                "Backtrack with a running XOR", SUBOPTIMAL, time="O(2ⁿ)", space="O(n)", visual="backtrack",
                detail="Include or skip each element, carrying the XOR so far; add it at each leaf.",
                why="Correct and fine for n ≤ 12, but it visits all 2ⁿ subsets to add up something one OR already tells you.",
            ),
            Choice(
                "XOR of all, times 2ⁿ⁻¹", INCORRECT, time="O(n)", space="O(1)", visual="bits",
                detail="Return (nums[0] ^ nums[1] ^ …) << (n − 1).",
                why="For [1, 1], the subsets give 0 + 1 + 1 + 0 = 2. What does this formula give?",
            ),
            Choice(
                "Sum of all, times 2ⁿ⁻¹", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="Each element appears in half the subsets, so add it that many times.",
                why="That's the total of subset sums. Does 1 XOR 1 equal 1 + 1?",
            ),
        ),
    ),
    Question(
        slug="letter-case-permutation", number=784, title="Letter Case Permutation",
        difficulty="Medium", topics=("trees",),
        summary="Return every string you can make by changing letters of s to upper or lower case. Digits stay as they are.",
        example="\"a1b2\"  →  [\"a1b2\", \"a1B2\", \"A1b2\", \"A1B2\"]",
        criterion="Which approach does work proportional to the output?",
        hint="Which characters actually create a choice?",
        choices=(
            Choice(
                "Branch only on letters", OPTIMAL, time="O(n·2ᴸ)", space="O(n)", visual="backtrack",
                detail="Walk the string; at a letter, recurse with each case; at a digit, just move on.",
                why="With L letters there are exactly 2ᴸ results, and each leaf is one of them. No branch is wasted on digits.",
            ),
            Choice(
                "Toggle every position, then dedupe", SUBOPTIMAL, time="O(n·2ⁿ)", space="O(n·2ⁿ)", visual="set",
                detail="Branch on every character, digits too, and remove duplicates with a set.",
                why="Correct, but each digit doubles the work and then the duplicates are thrown away.",
            ),
            Choice(
                "All-lower and all-upper", INCORRECT, time="O(n)", space="O(n)", visual="brute",
                detail="Return s.lower() and s.upper().",
                why="Where is \"a1B2\"?",
            ),
            Choice(
                "Flip one letter at a time", INCORRECT, time="O(n²)", space="O(n)", visual="brute",
                detail="Return s plus one string per letter with only that letter's case changed.",
                why="That gives 3 strings for \"a1b2\". How many does the example list?",
            ),
        ),
    ),
    Question(
        slug="valid-binary-strings-with-cost-limit", number=3955, title="Valid Binary Strings With Cost Limit",
        difficulty="Medium", topics=("trees",),
        summary="A binary string's cost is the sum of indices holding '1'. Return every length-n string with no two adjacent 1s and cost ≤ k. n ≤ 12.",
        example="n = 3, k = 1  →  [\"000\", \"010\", \"100\"]",
        criterion="Which approach spends time only on prefixes that can still be valid?",
        hint="When placing a '1' at index i, what do you already know about the previous character and the cost?",
        choices=(
            Choice(
                "Backtrack with both checks on placement", OPTIMAL, time="O(n·output)", space="O(n)", visual="backtrack",
                detail="At index i, always try '0'; try '1' only if the previous char is '0' and cost + i ≤ k.",
                why="Both rules can be checked the moment a '1' is placed. Every prefix that survives extends to at least one valid string (all zeros after it), so no branch is wasted.",
            ),
            Choice(
                "Enumerate all 2ⁿ strings, then filter", SUBOPTIMAL, time="O(n·2ⁿ)", space="O(n)", visual="brute",
                detail="Build every binary string and keep those that pass both rules.",
                why="Correct for n ≤ 12, but a prefix \"11…\" is already dead. Why finish it?",
            ),
            Choice(
                "Fill the lowest indices first", INCORRECT, time="O(n)", space="O(n)", visual="greedy",
                detail="Place 1s at 0, 2, 4, … until the cost would pass k.",
                why="That builds one string. The task asks for how many?",
            ),
            Choice(
                "Count them with DP", INCORRECT, time="O(n·k)", space="O(n·k)", visual="dp-2d",
                detail="dp[i][c] = number of valid prefixes of length i with cost c.",
                why="It gives how many strings there are. Does the task want the number or the strings?",
            ),
        ),
    ),
    Question(
        slug="partition-array-into-two-equal-product-subsets", number=3566, title="Partition Array into Two Equal Product Subsets",
        difficulty="Medium", topics=("trees",),
        summary="Given distinct positive integers and a target, decide whether nums can be split into two non-empty groups (each element in exactly one) whose products both equal target. n ≤ 12.",
        example="nums = [3,1,6,8,4], target = 24  →  true",
        criterion="Which approach does O(1) work per subset tried?",
        hint="If you assign elements one at a time, what do you know about each group's product so far?",
        choices=(
            Choice(
                "Assign each element to A or B, prune overflow", OPTIMAL, time="O(2ⁿ)", space="O(n)", visual="backtrack",
                detail="Carry both products; stop a branch once either exceeds target; at the end check both equal it.",
                why="Each assignment updates one product in O(1), and products only grow, so a branch over target can never recover.",
            ),
            Choice(
                "Every mask, products from scratch", SUBOPTIMAL, time="O(n·2ⁿ)", space="O(1)", visual="bits",
                detail="For each mask, multiply its elements and the rest's elements.",
                why="Correct, but neighbouring masks differ by one element. Why remultiply all n?",
            ),
            Choice(
                "Check total product == target²", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="Return true when the product of all elements is target squared.",
                why="[2, 8] with target 4 gives 16 = 4². Can you split it into two groups of product 4?",
            ),
            Choice(
                "Sorted halves", INCORRECT, time="O(n log n)", space="O(1)", visual="sort",
                detail="Sort, then try each split point between a prefix and a suffix.",
                why="Sorted, the example is [1,3,4,6,8]. No prefix has product 24, yet {3,8} and {1,4,6} work. Must a group be contiguous?",
            ),
        ),
    ),
    Question(
        slug="count-number-of-maximum-bitwise-or-subsets", number=2044, title="Count Number of Maximum Bitwise-OR Subsets",
        difficulty="Medium", topics=("trees",),
        summary="Find the largest bitwise OR any non-empty subset can reach, and count the subsets that reach it. n ≤ 16.",
        example="[3,1]  →  2",
        criterion="Which approach does O(1) work per subset?",
        hint="Which subset is guaranteed to reach the maximum OR?",
        choices=(
            Choice(
                "Backtrack with a running OR", OPTIMAL, time="O(2ⁿ)", space="O(n)", visual="backtrack",
                detail="The target is the OR of all elements; include or skip each one, counting leaves whose OR equals it.",
                why="OR never decreases, so the full set reaches the maximum. Carrying the OR down the recursion makes each subset cost O(1).",
            ),
            Choice(
                "Every mask, OR from scratch", SUBOPTIMAL, time="O(n·2ⁿ)", space="O(1)", visual="bits",
                detail="For each mask, OR its elements and compare.",
                why="Correct, but each mask redoes the work its parent already did.",
            ),
            Choice(
                "Count subsets with the largest element", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="Every subset containing max(nums) qualifies.",
                why="For [1, 2], the largest OR is 3. Does {2} reach it?",
            ),
            Choice(
                "Only the full set", INCORRECT, time="O(n)", space="O(1)", visual="bits",
                detail="Return 1.",
                why="In the example, {3} alone also gives 3.",
            ),
        ),
    ),
    Question(
        slug="lcp-51-cooking", number=None, title="Cooking",
        difficulty="Easy", topics=("trees",),
        ref="LCP 51", url="https://leetcode.cn/problems/UEcfPD/",
        summary="You hold amounts of 5 ingredients. Each of up to 8 dishes needs given amounts and gives (taste, fullness); each dish can be made at most once. With fullness ≥ limit, return the most taste, or −1.",
        example="materials = [3,2,4,1,2], cookbooks = [[1,1,0,1,2],[2,1,4,0,0],[3,2,4,1,0]], attribute = [[3,2],[2,4],[7,6]], limit = 5  →  7",
        criterion="Which approach is correct and tries each set of dishes once?",
        hint="With 8 dishes, how many sets of dishes are there?",
        choices=(
            Choice(
                "Make or skip each dish", OPTIMAL, time="O(2ᵐ)", space="O(m)", visual="backtrack",
                detail="Subtract ingredients when making a dish and restore them on return; skip a dish you can't afford.",
                why="At most 256 sets. Carrying the remaining ingredients down the recursion checks each choice in O(5), and unaffordable branches stop early.",
            ),
            Choice(
                "Try every cooking order", SUBOPTIMAL, time="O(m·m!)", space="O(m)", visual="brute",
                detail="Permute the dishes and cook greedily along each order.",
                why="Correct, but the order you cook in doesn't change what's left. 8! is 40320 orders for 256 sets.",
            ),
            Choice(
                "Knapsack on fullness", INCORRECT, time="O(m·limit)", space="O(limit)", visual="dp-1d",
                detail="0/1 knapsack maximizing taste over fullness ≥ limit.",
                why="Where do the five ingredient limits go?",
            ),
            Choice(
                "Greedy by taste", INCORRECT, time="O(m log m)", space="O(1)", visual="greedy",
                detail="Cook the tastiest affordable dish first, repeat.",
                why="In example 2, dish 2 alone (taste 10) uses everything, but dishes 0 and 1 give 11.",
            ),
        ),
    ),
    Question(
        slug="remove-all-ones-with-row-and-column-flips-ii", number=2174, title="Remove All Ones With Row and Column Flips II",
        difficulty="Medium", topics=("trees",),
        summary="In a binary grid with m·n ≤ 15, one operation picks a cell holding 1 and sets its whole row and column to 0. Return the fewest operations that clear the grid.",
        example="[[1,1,1],[1,1,1],[0,1,0]]  →  2",
        criterion="Which approach avoids solving the same grid twice?",
        hint="With 15 cells, how many different grids can appear?",
        choices=(
            Choice(
                "Search over grid bitmasks with memo", OPTIMAL, time="O(2ᵐⁿ·mn)", space="O(2ᵐⁿ)", visual="backtrack",
                detail="Encode the grid as a mask; try each 1-cell, recurse on the cleared mask, cache the best per mask.",
                why="Different orders of operations reach the same grid. Caching by mask solves each of the ≤ 2¹⁵ grids once.",
            ),
            Choice(
                "Backtrack over every order", SUBOPTIMAL, time="O((mn)!)", space="O(mn)", visual="brute",
                detail="Try every sequence of operations without remembering results.",
                why="Correct, but clearing (0,0) then (1,1) gives the same grid as the reverse. How often does that repeat?",
            ),
            Choice(
                "Clear the cell that removes the most 1s", INCORRECT, time="O((mn)²)", space="O(1)", visual="greedy",
                detail="Repeatedly pick the cell whose row and column hold the most 1s.",
                why="A greedy pick can split the remaining 1s so they need more steps later. What guarantees the first choice is part of a best plan?",
            ),
            Choice(
                "Count rows that contain a 1", INCORRECT, time="O(mn)", space="O(1)", visual="matrix",
                detail="Each operation clears one row, so that's the answer.",
                why="An operation also clears a column. The example has 3 such rows. What's the answer?",
            ),
        ),
    ),
    Question(
        slug="generalized-abbreviation", number=320, title="Generalized Abbreviation",
        difficulty="Medium", topics=("trees",),
        summary="Return every generalized abbreviation of word: replace any set of non-overlapping, non-adjacent substrings by their lengths.",
        example="\"ab\"  →  [\"2\", \"1b\", \"a1\", \"ab\"]",
        criterion="Which approach builds each abbreviation exactly once?",
        hint="Look at one character at a time. What are its two options?",
        choices=(
            Choice(
                "Keep or abbreviate each character", OPTIMAL, time="O(n·2ⁿ)", space="O(n)", visual="backtrack",
                detail="Carry a running count of abbreviated chars; flush it as a number before a kept char and at the end.",
                why="Each character is either kept or counted, and adjacent counted chars merge into one number. That's a bijection with the 2ⁿ results.",
            ),
            Choice(
                "Pick substrings, then dedupe", SUBOPTIMAL, time="O(n·4ⁿ)", space="O(n·2ⁿ)", visual="set",
                detail="Choose any set of substrings to replace, build the string, keep it if valid, dedupe with a set.",
                why="Correct, but \"2\" can be built from one substring or two, and invalid adjacent picks are built only to be rejected.",
            ),
            Choice(
                "Replace one substring", INCORRECT, time="O(n³)", space="O(n)", visual="brute",
                detail="For each substring, replace it with its length.",
                why="\"word\" has the abbreviation \"1o1d\". How many substrings did that replace?",
            ),
            Choice(
                "Digit or letter at each spot", INCORRECT, time="O(n·2ⁿ)", space="O(n)", visual="backtrack",
                detail="Each character becomes either itself or \"1\".",
                why="That builds \"11\" for \"ab\". Is that a valid abbreviation?",
            ),
        ),
    ),
    Question(
        slug="factor-combinations", number=254, title="Factor Combinations",
        difficulty="Medium", topics=("trees",),
        summary="Return every way to write n as a product of factors in [2, n − 1], each combination once (order doesn't matter).",
        example="12  →  [[2,6], [2,2,3], [3,4]]",
        criterion="Which approach is correct and only tries factors up to the square root?",
        hint="If the next factor is larger than √rest, what must rest be?",
        choices=(
            Choice(
                "Non-decreasing factors up to √rest", OPTIMAL, time="O(output·√n)", space="O(log n)", visual="backtrack",
                detail="For i from start while i·i ≤ rest: if i divides rest, emit path + [i, rest/i] and recurse on rest/i from i.",
                why="Keeping factors non-decreasing lists each combination once. A factor past √rest would leave a smaller one after it, breaking the order.",
            ),
            Choice(
                "Non-decreasing factors up to rest", SUBOPTIMAL, time="O(output·n)", space="O(log n)", visual="recursion",
                detail="Try every i from start to rest.",
                why="Correct, but every i between √rest and rest except rest itself is wasted.",
            ),
            Choice(
                "Prime factorization", INCORRECT, time="O(√n)", space="O(log n)", visual="math",
                detail="Return the list of prime factors.",
                why="That gives [2, 2, 3]. Where are [2, 6] and [3, 4]?",
            ),
            Choice(
                "Any order of factors", INCORRECT, time="O(output·√n)", space="O(log n)", visual="backtrack",
                detail="Try every divisor at every step.",
                why="That yields [2, 6] and [6, 2]. Are they different combinations?",
            ),
        ),
    ),
    Question(
        slug="combination-sum", number=39, title="Combination Sum",
        difficulty="Medium", topics=("trees",),
        summary="Given distinct positive candidates, return every combination (each candidate usable any number of times) that sums to target, each combination once.",
        example="[2,3,6,7], 7  →  [[2,2,3], [7]]",
        criterion="Which approach is correct without deduplicating afterwards?",
        hint="How do you stop [2,2,3] and [3,2,2] from both appearing?",
        choices=(
            Choice(
                "Backtrack from a start index, reusing it", OPTIMAL, time="O(n^(t/m))", space="O(t/m)", visual="backtrack",
                detail="Sort; at index i, try candidates[j] for j ≥ i and recurse from j; break once one exceeds the remainder. (t = target, m = smallest candidate.)",
                why="Choosing only from j onward lists each multiset in one order. Recursing from j (not j + 1) allows reuse, and sorting makes the break safe.",
            ),
            Choice(
                "Try all candidates each step, then dedupe", SUBOPTIMAL, time="O(n^(t/m)·t/m)", space="O(output)", visual="set",
                detail="Recurse over every candidate at every step, sort each result and add it to a set.",
                why="Correct, but each combination of k items is built up to k! times.",
            ),
            Choice(
                "Recurse from j + 1", INCORRECT, time="O(2ⁿ)", space="O(n)", visual="backtrack",
                detail="Move to the next candidate after picking one.",
                why="Can [2, 2, 3] use 2 twice then?",
            ),
            Choice(
                "Greedy from the largest", INCORRECT, time="O(n log n)", space="O(1)", visual="greedy",
                detail="Take the largest candidate that fits, repeat.",
                why="That finds [7] only. Where is [2, 2, 3]?",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §4.2 partition backtracking
    Question(
        slug="palindrome-partitioning", number=131, title="Palindrome Partitioning",
        difficulty="Medium", topics=("trees",),
        summary="Return every way to cut s into pieces that are all palindromes.",
        example="\"aab\"  →  [[\"a\",\"a\",\"b\"], [\"aa\",\"b\"]]",
        criterion="Which approach checks each candidate piece in O(1)?",
        hint="The same substring is tested in many branches. Could you answer it once?",
        choices=(
            Choice(
                "Precompute palindromes, then backtrack cuts", OPTIMAL, time="O(n·2ⁿ)", space="O(n²)", visual="backtrack",
                detail="Fill isPal[i][j] by DP; from index i, recurse after every j with isPal[i][j].",
                why="isPal[i][j] = s[i] == s[j] and isPal[i+1][j−1], filled in O(n²). After that, each piece is checked in O(1) however often it's tried.",
            ),
            Choice(
                "Backtrack, checking pieces with two pointers", SUBOPTIMAL, time="O(n²·2ⁿ)", space="O(n)", visual="two-pointers",
                detail="From index i, try each end j and test s[i..j] by comparing from both ends.",
                why="Correct, but s[i..j] is rechecked in every branch that reaches i.",
            ),
            Choice(
                "Longest palindrome prefix first", INCORRECT, time="O(n²)", space="O(n)", visual="greedy",
                detail="Repeatedly cut off the longest palindromic prefix.",
                why="That produces one partition. How many does the task ask for?",
            ),
            Choice(
                "Single characters only", INCORRECT, time="O(n)", space="O(n)", visual="brute",
                detail="Every character is a palindrome, so return that partition.",
                why="Where is [\"aa\", \"b\"]?",
            ),
        ),
    ),
    Question(
        slug="find-the-punishment-number-of-an-integer", number=2698, title="Find the Punishment Number of an Integer",
        difficulty="Medium", topics=("trees",),
        summary="Sum i² over 1 ≤ i ≤ n where the decimal string of i² can be cut into pieces whose integer values add up to i. n ≤ 1000.",
        example="10  →  182    (1 + 81 + 100: 81 = 8 + 1, 100 = 10 + 0)",
        criterion="Which approach abandons a split as soon as it can't work?",
        hint="If the pieces so far already add up to more than i, can later pieces help?",
        choices=(
            Choice(
                "Backtrack cuts, prune when over i", OPTIMAL, time="O(n·2ᵈ)", space="O(d)", visual="backtrack",
                detail="From position p, take each next piece, add it, recurse; stop when the total passes i.",
                why="Pieces are non-negative, so a total over i stays over i. Pruning cuts most of the 2ᵈ⁻¹ splits of a d-digit square.",
            ),
            Choice(
                "Check every cut mask", SUBOPTIMAL, time="O(n·d·2ᵈ)", space="O(d)", visual="bits",
                detail="For each of the 2ᵈ⁻¹ ways to cut, parse the pieces and sum them.",
                why="Correct, but every split is parsed in full, even after the first piece is already too big.",
            ),
            Choice(
                "Digit sum equals i", INCORRECT, time="O(n·d)", space="O(1)", visual="math",
                detail="Count i when the digits of i² add up to i.",
                why="That only allows one-digit pieces. 10² = 100 qualifies as 10 + 0. What is its digit sum?",
            ),
            Choice(
                "Split into two pieces", INCORRECT, time="O(n·d)", space="O(1)", visual="brute",
                detail="Try every single cut of i² into two parts.",
                why="36² = 1296 qualifies as 1 + 29 + 6. How many pieces is that?",
            ),
        ),
    ),
    Question(
        slug="restore-ip-addresses", number=93, title="Restore IP Addresses",
        difficulty="Medium", topics=("trees",),
        summary="Insert three dots into a digit string to form valid IPv4 addresses (four parts, each 0–255, no leading zeros). Return all of them.",
        example="\"25525511135\"  →  [\"255.255.11.135\", \"255.255.111.35\"]",
        criterion="Which approach only builds parts that can be valid?",
        hint="How long can one part be, and when is a part with a leading zero allowed?",
        choices=(
            Choice(
                "Backtrack four parts of 1–3 digits", OPTIMAL, time="O(3⁴·n)", space="O(1)", visual="backtrack",
                detail="Take 1–3 digits, skip a leading zero unless the part is \"0\", stop past 255; also stop if the rest can't fill the remaining parts.",
                why="At most 3⁴ = 81 branches, each part checked as it's cut. Length checks prune strings that are too short or too long right away.",
            ),
            Choice(
                "Try every cut set, keep four valid parts", SUBOPTIMAL, time="O(n·2ⁿ)", space="O(n)", visual="bits",
                detail="Enumerate every way to cut the string and validate each.",
                why="Correct, but only cuts into exactly four short parts can work. Why generate the rest?",
            ),
            Choice(
                "Allow leading zeros", INCORRECT, time="O(3⁴·n)", space="O(1)", visual="backtrack",
                detail="Accept any part with value ≤ 255.",
                why="Is \"1.01.1.1\" a valid address?",
            ),
            Choice(
                "Greedy longest part ≤ 255", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Take 3 digits when their value fits, else 2, else 1.",
                why="That builds one address at most. The example has two.",
            ),
        ),
    ),
    Question(
        slug="word-break-ii", number=140, title="Word Break II",
        difficulty="Hard", topics=("trees",),
        summary="Return every way to add spaces to s so each word is in wordDict.",
        example="\"catsanddog\", [\"cat\",\"cats\",\"and\",\"sand\",\"dog\"]  →  [\"cats and dog\", \"cat sand dog\"]",
        criterion="Which approach never re-explores a suffix that can't be split?",
        hint="Try \"aaaa…ab\" with words \"a\", \"aa\". How much work before you learn it fails?",
        choices=(
            Choice(
                "DFS on start index with memo", OPTIMAL, time="O(n² + n·output)", space="O(n·output)", visual="recursion",
                detail="sentences(i) tries each dictionary word starting at i and caches the results; an empty result means dead.",
                why="Each suffix is solved once. A dead suffix returns [] from the cache, so the exponential search only happens when the output itself is exponential.",
            ),
            Choice(
                "Plain backtracking", SUBOPTIMAL, time="O(2ⁿ)", space="O(n)", visual="backtrack",
                detail="Try each word at the current index, recurse, record the sentence at the end.",
                why="Correct, but on \"aaaa…ab\" it tries every split of the a's before learning the b can't be matched, even though there are no answers.",
            ),
            Choice(
                "Greedy longest word", INCORRECT, time="O(n²)", space="O(n)", visual="greedy",
                detail="Take the longest dictionary word at each index.",
                why="Greedy takes \"cats\", then must take \"and\". Where is \"cat sand dog\"?",
            ),
            Choice(
                "Boolean DP", INCORRECT, time="O(n²)", space="O(n)", visual="dp-1d",
                detail="dp[i] = whether s[0..i) can be split.",
                why="That answers whether a split exists. Does the task want a yes or the sentences?",
            ),
        ),
    ),
    Question(
        slug="word-pattern-ii", number=291, title="Word Pattern II",
        difficulty="Medium", topics=("trees",),
        summary="Decide whether s matches pattern: each pattern letter maps to a non-empty substring, different letters to different substrings, and replacing letters gives s.",
        example="pattern = \"abab\", s = \"redblueredblue\"  →  true",
        criterion="Which approach is correct and rejects a mapping as soon as it breaks?",
        hint="Once 'a' is bound to \"red\", what must the next occurrence of 'a' match?",
        choices=(
            Choice(
                "Backtrack with a map and a used set", OPTIMAL, time="O(nᵏ·n)", space="O(k + n)", visual="backtrack",
                detail="A bound letter must match its string next; an unbound one tries each unused prefix; unbind on return. (k = distinct letters.)",
                why="Bound letters cost one comparison. The used set keeps two letters from sharing a string, and a mismatch stops the branch right away.",
            ),
            Choice(
                "Try every substring for every letter", SUBOPTIMAL, time="O(n²ᵏ·n)", space="O(k + n)", visual="brute",
                detail="Assign each distinct letter any substring of s, expand the pattern and compare with s.",
                why="Correct, but a letter's string must start where the previous one ended. Why try substrings from anywhere else?",
            ),
            Choice(
                "Only map letters to strings", INCORRECT, time="O(nᵏ·n)", space="O(k + n)", visual="hashmap",
                detail="Check letter → string consistency, but let two letters share a string.",
                why="With pattern \"ab\" and s \"xx\", would 'a' and 'b' both become \"x\"?",
            ),
            Choice(
                "Bind each new letter to one character", INCORRECT, time="O(n)", space="O(m)", visual="greedy",
                detail="Give every new letter the shortest possible string.",
                why="In the example, 'a' needs \"red\". Can one character work?",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §4.3 combination backtracking
    Question(
        slug="combinations", number=77, title="Combinations",
        difficulty="Medium", topics=("trees",),
        summary="Return every combination of k numbers chosen from 1..n.",
        example="n = 4, k = 2  →  [[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]",
        criterion="Which approach only explores branches that can still reach k numbers?",
        hint="If you need d more numbers and only fewer than d remain, is the branch worth entering?",
        choices=(
            Choice(
                "Increasing picks with a count prune", OPTIMAL, time="O(k·C(n, k))", space="O(k)", visual="backtrack",
                detail="Pick the next number above the last one, stopping when too few numbers remain to finish.",
                why="Increasing order lists each set once, and the prune means every branch ends in a real combination, so work tracks the output.",
            ),
            Choice(
                "All subsets, keep size k", SUBOPTIMAL, time="O(n·2ⁿ)", space="O(n)", visual="bits",
                detail="Enumerate every subset of 1..n and keep those with k elements.",
                why="Correct, but for n = 20, k = 2 it walks a million subsets to keep 190.",
            ),
            Choice(
                "Ordered picks", INCORRECT, time="O(k·n!/(n−k)!)", space="O(k)", visual="backtrack",
                detail="Pick any unused number at each step.",
                why="That yields [1,2] and [2,1]. Are they different combinations?",
            ),
            Choice(
                "Windows of k consecutive numbers", INCORRECT, time="O(n·k)", space="O(k)", visual="sliding-window",
                detail="Return [i, i+1, …, i+k−1] for each i.",
                why="Where is [1, 3]?",
            ),
        ),
    ),
    Question(
        slug="combination-sum-iii", number=216, title="Combination Sum III",
        difficulty="Medium", topics=("trees",),
        summary="Return every set of k distinct digits from 1–9 that sums to n.",
        example="k = 3, n = 7  →  [[1,2,4]]",
        criterion="Which approach cuts branches that can't reach n?",
        hint="With the digits picked so far, what's the most and least the remaining picks can add?",
        choices=(
            Choice(
                "Increasing digits with sum bounds", OPTIMAL, time="O(k·C(9, k))", space="O(k)", visual="backtrack",
                detail="Pick digits in increasing order; stop when the sum passes n or the count can't be filled.",
                why="Digits only add, so a sum over n stays over. Increasing order lists each set once.",
            ),
            Choice(
                "Check all 512 subsets", SUBOPTIMAL, time="O(9·2⁹)", space="O(1)", visual="bits",
                detail="For each mask of 1–9, keep it if it has k digits summing to n.",
                why="Correct and tiny, but it checks every subset, even those whose first digits already overshoot.",
            ),
            Choice(
                "Allow repeated digits", INCORRECT, time="O(9ᵏ)", space="O(k)", visual="backtrack",
                detail="Recurse from the same digit after picking it.",
                why="That produces [1,1,5]. Are the digits distinct?",
            ),
            Choice(
                "Greedy smallest digits", INCORRECT, time="O(k)", space="O(k)", visual="greedy",
                detail="Take 1..k−1, then whatever digit makes up the rest.",
                why="For k = 3, n = 9 that gives [1,2,6]. Where are [1,3,5] and [2,3,4]?",
            ),
        ),
    ),
    Question(
        slug="iterator-for-combination", number=1286, title="Iterator for Combination",
        difficulty="Medium", topics=("trees",),
        summary="Design an iterator over the length-k combinations of a sorted string of distinct letters, in lexicographic order: next() and hasNext().",
        example="\"abc\", 2: next → \"ab\", next → \"ac\", hasNext → true, next → \"bc\", hasNext → false",
        criterion="Which approach uses O(k) memory?",
        hint="Think of the combination as k increasing indices. How does the next one differ from the current?",
        choices=(
            Choice(
                "Advance an index array", OPTIMAL, time="O(k) per call", space="O(k)", visual="two-pointers",
                detail="Find the rightmost index that can move right, bump it, and reset the ones after it to follow consecutively.",
                why="This is the odometer step for increasing indices. It produces exactly the next combination in order, holding only the current one.",
            ),
            Choice(
                "Precompute all with backtracking", SUBOPTIMAL, time="O(k·C(n, k))", space="O(k·C(n, k))", visual="backtrack",
                detail="Generate every combination in the constructor, then serve them from a list.",
                why="Correct, but it stores every combination even if next() is called twice.",
            ),
            Choice(
                "Count a bitmask up from 0", INCORRECT, time="O(n) per call", space="O(1)", visual="bits",
                detail="Increment a mask and return it when it has k bits, letter i for bit i.",
                why="For \"abcd\", k = 2, masks 3, 5, 6, 9 give \"ab\", \"ac\", \"bc\", \"ad\". Is that lexicographic?",
            ),
            Choice(
                "Next permutation", INCORRECT, time="O(k) per call", space="O(k)", visual="sort",
                detail="Advance like next_permutation on the current k letters.",
                why="After \"ab\" that gives \"ba\". Is that a new combination?",
            ),
        ),
    ),
    Question(
        slug="generate-parentheses", number=22, title="Generate Parentheses",
        difficulty="Medium", topics=("trees",),
        summary="Return every well-formed string of n pairs of parentheses.",
        example="3  →  [\"((()))\", \"(()())\", \"(())()\", \"()(())\", \"()()()\"]",
        criterion="Which approach never builds an invalid prefix?",
        hint="When is adding '(' allowed? When is adding ')' allowed?",
        choices=(
            Choice(
                "Add '(' or ')' while counts allow", OPTIMAL, time="O(4ⁿ/√n)", space="O(n)", visual="backtrack",
                detail="Add '(' if fewer than n are open; add ')' if fewer close than open.",
                why="Every prefix built this way can still be finished, so the search tree has one leaf per answer (the Catalan number).",
            ),
            Choice(
                "All 2²ⁿ strings, then validate", SUBOPTIMAL, time="O(n·4ⁿ)", space="O(n)", visual="brute",
                detail="Build every string of n '(' and n ')' characters and keep the balanced ones.",
                why="Correct, but a prefix like \")\" is already hopeless. Why finish it?",
            ),
            Choice(
                "Wrap or prefix the smaller answers", INCORRECT, time="O(n·Cₙ)", space="O(n·Cₙ)", visual="recursion",
                detail="From each answer r for n − 1, add \"(\" + r + \")\" and \"()\" + r.",
                why="From n = 2, which of these builds \"(())()\"?",
            ),
            Choice(
                "Nested and side-by-side only", INCORRECT, time="O(n)", space="O(n)", visual="brute",
                detail="Return \"(((…)))\" and \"()()…()\".",
                why="The example has five strings for n = 3. Which three are missing?",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §4.4 permutation backtracking
    Question(
        slug="permutations", number=46, title="Permutations",
        difficulty="Medium", topics=("trees",),
        summary="Return every permutation of an array of distinct integers.",
        example="[1,2,3]  →  [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]",
        criterion="Which approach does work proportional to the output?",
        hint="At each position, which values are still allowed?",
        choices=(
            Choice(
                "Fill positions from unused values", OPTIMAL, time="O(n·n!)", space="O(n)", visual="backtrack",
                detail="Mark a value used, recurse to the next position, unmark on return.",
                why="Each level has one fewer choice, so there are exactly n! leaves, one per permutation.",
            ),
            Choice(
                "All n-length sequences, keep distinct ones", SUBOPTIMAL, time="O(n·nⁿ)", space="O(n)", visual="brute",
                detail="Try every value at every position and keep sequences with no repeats.",
                why="Correct, but for n = 6, that's 46656 sequences for 720 permutations.",
            ),
            Choice(
                "All rotations", INCORRECT, time="O(n²)", space="O(n)", visual="array-copy",
                detail="Return the array rotated by 0..n−1.",
                why="That's n results. Is [1,3,2] a rotation of [1,2,3]?",
            ),
            Choice(
                "Swap each adjacent pair", INCORRECT, time="O(n²)", space="O(n)", visual="array-copy",
                detail="Return the array plus one copy per adjacent swap.",
                why="That gives n results. How many permutations does the example list?",
            ),
        ),
    ),
    Question(
        slug="word-squares-ii", number=3799, title="Word Squares II",
        difficulty="Medium", topics=("trees",),
        summary="From up to 15 distinct 4-letter words, pick 4 distinct words top, left, right, bottom so that the square's corners match: top[0] = left[0], top[3] = right[0], bottom[0] = left[3], bottom[3] = right[3]. Return all, sorted by (top, left, right, bottom).",
        example="[\"able\",\"area\",\"echo\",\"also\"]  →  [[\"able\",\"area\",\"echo\",\"also\"], [\"area\",\"able\",\"also\",\"echo\"]]",
        criterion="Which approach checks each corner as soon as both of its words are placed?",
        hint="If you sort the words and place them in the order top, left, right, bottom, is the output already sorted?",
        choices=(
            Choice(
                "Sorted words, place in order, check each corner", OPTIMAL, time="O(n⁴)", space="O(1)", visual="backtrack",
                detail="Loop top, then left with left[0] = top[0], then right with right[0] = top[3], then bottom with both bottom corners; skip reused words.",
                why="Each pick is checked against the corners it closes, so bad prefixes stop early. Looping over sorted words in tuple order emits results already sorted.",
            ),
            Choice(
                "All 4-word arrangements, then check and sort", SUBOPTIMAL, time="O(n⁴·log n)", space="O(output)", visual="brute",
                detail="Build every ordered choice of 4 distinct words, keep valid ones, sort.",
                why="Correct, but a top/left pair that already disagrees is still paired with every right and bottom.",
            ),
            Choice(
                "Classic word square", INCORRECT, time="O(n⁴)", space="O(1)", visual="matrix",
                detail="Require row i to equal column i.",
                why="Here only the four corners must match. Must \"able\" read the same down the left side?",
            ),
            Choice(
                "Allow a word twice", INCORRECT, time="O(n⁴)", space="O(1)", visual="backtrack",
                detail="Check the corners but let the same word fill two sides.",
                why="The four words must be distinct. Could \"area\" be both top and left?",
            ),
        ),
    ),
    Question(
        slug="n-queens", number=51, title="N-Queens",
        difficulty="Hard", topics=("trees",),
        summary="Place n queens on an n×n board so none attack each other. Return every board.",
        example="4  →  [[\".Q..\",\"...Q\",\"Q...\",\"..Q.\"], [\"..Q.\",\"Q...\",\"...Q\",\".Q..\"]]",
        criterion="Which approach checks each placement in O(1)?",
        hint="Which two quantities are constant along each diagonal?",
        choices=(
            Choice(
                "Row by row with column and diagonal sets", OPTIMAL, time="O(n!)", space="O(n)", visual="backtrack",
                detail="Place one queen per row; a column c is allowed if c, r + c and r − c are all unused.",
                why="One queen per row is forced. Anti-diagonals share r + c and diagonals share r − c, so three set lookups replace a board scan.",
            ),
            Choice(
                "Row by row, scanning the board", SUBOPTIMAL, time="O(n·n!)", space="O(n²)", visual="matrix",
                detail="Before placing, walk up the column and both diagonals looking for a queen.",
                why="Correct, but each check costs O(n) for facts three sets already know.",
            ),
            Choice(
                "First safe column, no undo", INCORRECT, time="O(n²)", space="O(n)", visual="greedy",
                detail="In each row, take the leftmost safe column and never go back.",
                why="For n = 4, row 0 col 0, row 1 col 2, then row 2 has no safe column. What now?",
            ),
            Choice(
                "Permutations of columns", INCORRECT, time="O(n·n!)", space="O(n)", visual="backtrack",
                detail="Every permutation gives one queen per row and column.",
                why="The identity permutation puts all queens on one diagonal. Do they attack?",
            ),
        ),
    ),
    Question(
        slug="n-queens-ii", number=52, title="N-Queens II",
        difficulty="Hard", topics=("trees",),
        summary="Return the number of ways to place n non-attacking queens on an n×n board.",
        example="4  →  2",
        criterion="Which approach counts without building any board?",
        hint="If you only need a count, what's the least state each row needs?",
        choices=(
            Choice(
                "Backtrack with three bitmasks", OPTIMAL, time="O(n!)", space="O(n)", visual="bits",
                detail="Carry masks of attacked columns and diagonals; shift the diagonal masks each row; free = ~(cols | d1 | d2).",
                why="Shifting the diagonal masks by one each row tracks attacks in O(1), and lowbit tricks iterate only free columns. Nothing is copied.",
            ),
            Choice(
                "Solve N-Queens, count the boards", SUBOPTIMAL, time="O(n!·n²)", space="O(n²)", visual="matrix",
                detail="Reuse the N-Queens solver and return the list length.",
                why="Correct, but each solution builds n strings of length n only to be counted.",
            ),
            Choice(
                "Count column permutations", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="One queen per row and column gives n! ways.",
                why="For n = 4 that's 24. The answer is 2. What attack is ignored?",
            ),
            Choice(
                "Greedy placement", INCORRECT, time="O(n²)", space="O(n)", visual="greedy",
                detail="Count 1 if leftmost-safe placement succeeds, else 0.",
                why="The answer can be more than 1. And can greedy fail even when solutions exist?",
            ),
        ),
    ),
    Question(
        slug="sudoku-solver", number=37, title="Sudoku Solver",
        difficulty="Hard", topics=("trees",),
        summary="Fill a 9×9 Sudoku grid in place; the puzzle has exactly one solution.",
        example="A standard puzzle with 51 blanks  →  the completed grid",
        criterion="Which approach prunes the search the most?",
        hint="Which empty cell should you fill next?",
        choices=(
            Choice(
                "Backtrack the most constrained cell, with bitmasks", OPTIMAL, time="O(9ᵇ) worst", space="O(b)", visual="backtrack",
                detail="Keep row, column and box masks; always fill the empty cell with the fewest candidates; undo on failure.",
                why="A cell with one candidate is forced, and one with none fails at once. Picking the tightest cell keeps the tree narrow, and masks give candidates in O(1).",
            ),
            Choice(
                "Backtrack in reading order, scanning for conflicts", SUBOPTIMAL, time="O(9ᵇ·27) worst", space="O(b)", visual="recursion",
                detail="Fill cells left to right, top to bottom; check each digit by scanning its row, column and box.",
                why="Correct, but it may branch on a wide-open cell while a forced one waits, and each check rescans 27 cells.",
            ),
            Choice(
                "Fill only forced cells", INCORRECT, time="O(81²)", space="O(1)", visual="greedy",
                detail="Repeatedly fill cells with a single candidate until none remain.",
                why="Hard puzzles reach a point where every empty cell has two or more candidates. What then?",
            ),
            Choice(
                "Smallest valid digit, no undo", INCORRECT, time="O(81·9)", space="O(1)", visual="greedy",
                detail="Put the smallest digit that fits in each cell, in order.",
                why="An early choice can leave a later cell with no digit. How do you recover without undoing?",
            ),
        ),
    ),
    Question(
        slug="permutations-iii", number=3437, title="Permutations III",
        difficulty="Medium", topics=("trees",),
        summary="Return, in lexicographic order, every permutation of 1..n in which adjacent numbers have different parity. n ≤ 10.",
        example="4  →  [[1,2,3,4],[1,4,3,2],[2,1,4,3],[2,3,4,1],[3,2,1,4],[3,4,1,2],[4,1,2,3],[4,3,2,1]]",
        criterion="Which approach only builds prefixes that alternate?",
        hint="When the last number is odd, which numbers may come next?",
        choices=(
            Choice(
                "Backtrack in increasing order, alternating parity", OPTIMAL, time="O(n·output)", space="O(n)", visual="backtrack",
                detail="Try unused numbers from small to large, only those with parity different from the last.",
                why="Trying values in increasing order emits permutations in lexicographic order, and the parity check rejects a bad prefix immediately.",
            ),
            Choice(
                "All permutations, then filter", SUBOPTIMAL, time="O(n·n!)", space="O(n)", visual="brute",
                detail="Generate permutations in order and keep those that alternate.",
                why="Correct, but for n = 10 that's 3.6 million permutations for 28800 answers.",
            ),
            Choice(
                "Always start with an odd number", INCORRECT, time="O(n·output)", space="O(n)", visual="backtrack",
                detail="Fix odd, even, odd, … by position.",
                why="For n = 4, [2,1,4,3] alternates. Where does it start?",
            ),
            Choice(
                "Interleave sorted odds and evens", INCORRECT, time="O(n)", space="O(n)", visual="two-pointers",
                detail="Return [1,2,3,4,…].",
                why="That's one permutation. The example has eight.",
            ),
        ),
    ),
    Question(
        slug="palindrome-permutation-ii", number=267, title="Palindrome Permutation II",
        difficulty="Medium", topics=("trees",),
        summary="Return every distinct palindrome that is a permutation of s (empty if none).",
        example="\"aabb\"  →  [\"abba\", \"baab\"]",
        criterion="Which approach generates each palindrome once, without a dedupe set?",
        hint="Once the left half is fixed, how much of the palindrome is left to choose?",
        choices=(
            Choice(
                "Permute half the counts, mirror", OPTIMAL, time="O(n·(n/2)!)", space="O(n)", visual="backtrack",
                detail="Fail if more than one char has an odd count; permute half of each count, skipping equal chars at the same depth; mirror around the odd char.",
                why="The left half decides the palindrome. Permuting the multiset of half-counts with same-depth skipping yields each distinct half once.",
            ),
            Choice(
                "Permute s, keep distinct palindromes", SUBOPTIMAL, time="O(n·n!)", space="O(n·n!)", visual="set",
                detail="Generate all permutations of s, keep palindromes, dedupe.",
                why="Correct, but n! permutations for at most (n/2)! halves, and most aren't palindromes.",
            ),
            Choice(
                "Permute the half without skipping", INCORRECT, time="O(n·(n/2)!)", space="O(n)", visual="backtrack",
                detail="Treat the half's characters as distinct.",
                why="For \"aaaa\" the half is \"aa\". How many times would \"aaaa\" be listed?",
            ),
            Choice(
                "Return s if it's a palindrome", INCORRECT, time="O(n)", space="O(1)", visual="two-pointers",
                detail="Check s itself.",
                why="\"aabb\" isn't a palindrome, yet the answer has two.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §4.5 backtracking with duplicates
    Question(
        slug="subsets-ii", number=90, title="Subsets II",
        difficulty="Medium", topics=("trees",),
        summary="Return every distinct subset of an array that may contain duplicates.",
        example="[1,2,2]  →  [[], [1], [1,2], [1,2,2], [2], [2,2]]",
        criterion="Which approach produces each subset once, without a dedupe set?",
        hint="After sorting, when would picking nums[i] at some depth repeat a branch you've already explored?",
        choices=(
            Choice(
                "Sort, skip equal values at the same depth", OPTIMAL, time="O(n·2ⁿ)", space="O(n)", visual="backtrack",
                detail="From start, try each i, but skip i > start with nums[i] == nums[i − 1].",
                why="Choosing the first or second 2 as the next element leads to the same subsets. Sorting groups equal values so the skip catches every repeat.",
            ),
            Choice(
                "All subsets, sorted into a set", SUBOPTIMAL, time="O(n log n·2ⁿ)", space="O(n·2ⁿ)", visual="set",
                detail="Generate every subset by index, sort it and add it to a set.",
                why="Correct, but duplicates are built and then thrown away. With many equal values, most of the work is wasted.",
            ),
            Choice(
                "Dedupe the input first", INCORRECT, time="O(n·2ⁿ)", space="O(n)", visual="set",
                detail="Remove duplicates, then generate subsets.",
                why="Where would [2, 2] come from?",
            ),
            Choice(
                "Skip equal neighbours, unsorted", INCORRECT, time="O(n·2ⁿ)", space="O(n)", visual="backtrack",
                detail="Apply the same-depth skip without sorting first.",
                why="In [2,1,2], the two 2s aren't adjacent. Will [2,1] and [1,2] both appear?",
            ),
        ),
    ),
    Question(
        slug="combination-sum-ii", number=40, title="Combination Sum II",
        difficulty="Medium", topics=("trees",),
        summary="Candidates may repeat; each may be used once. Return every distinct combination that sums to target.",
        example="[10,1,2,7,6,1,5], 8  →  [[1,1,6], [1,2,5], [1,7], [2,6]]",
        criterion="Which approach is correct without deduplicating afterwards?",
        hint="Once sorted, both 1s look the same. When does taking the second one first create a repeat?",
        choices=(
            Choice(
                "Sort, recurse from i + 1, skip same-depth repeats", OPTIMAL, time="O(n·2ⁿ)", space="O(n)", visual="backtrack",
                detail="Skip i > start with equal value; break once candidates[i] exceeds the remainder.",
                why="Same-depth skipping lists each multiset once, recursing from i + 1 uses each element once, and sorting makes the break safe.",
            ),
            Choice(
                "All subsets summing to target, then dedupe", SUBOPTIMAL, time="O(n·2ⁿ)", space="O(n·2ⁿ)", visual="set",
                detail="Backtrack by index without skipping and add sorted results to a set.",
                why="Correct, but equal values make the same combination many times. Ten 1s and target 5 build C(10,5) = 252 copies of one answer.",
            ),
            Choice(
                "Allow reuse", INCORRECT, time="O(n^(t/m))", space="O(t)", visual="backtrack",
                detail="Recurse from i after picking candidates[i].",
                why="That builds [1,1,1,…]. How many 1s are there to use?",
            ),
            Choice(
                "Dedupe candidates first", INCORRECT, time="O(n·2ⁿ)", space="O(n)", visual="set",
                detail="Remove repeated values, then backtrack.",
                why="Where would [1,1,6] come from?",
            ),
        ),
    ),
    Question(
        slug="non-decreasing-subsequences", number=491, title="Non-decreasing Subsequences",
        difficulty="Medium", topics=("trees",),
        summary="Return every distinct non-decreasing subsequence of length at least 2.",
        example="[4,6,7,7]  →  [[4,6],[4,6,7],[4,6,7,7],[4,7],[4,7,7],[6,7],[6,7,7],[7,7]]",
        criterion="Which approach is correct without a global set of results?",
        hint="You can't sort here. How do you avoid picking the same value twice at one depth?",
        choices=(
            Choice(
                "Per-depth set of used values", OPTIMAL, time="O(n·2ⁿ)", space="O(n²)", visual="backtrack",
                detail="At each depth, skip values already tried there or smaller than the last pick.",
                why="Two equal values at the same depth lead to the same subsequences. A small set per level catches repeats anywhere in the array, not just adjacent ones.",
            ),
            Choice(
                "Generate all, dedupe with a set", SUBOPTIMAL, time="O(n·2ⁿ)", space="O(n·2ⁿ)", visual="set",
                detail="Build every non-decreasing subsequence by index and store tuples in a set.",
                why="Correct, but duplicates are built in full and the set holds every result.",
            ),
            Choice(
                "Sort, then Subsets II", INCORRECT, time="O(n·2ⁿ)", space="O(n)", visual="sort",
                detail="Sort to group equal values and skip same-depth repeats.",
                why="Sorting [4,7,6,7] makes [6,7,7] look like a subsequence. Is it one?",
            ),
            Choice(
                "Skip if equal to the previous element", INCORRECT, time="O(n·2ⁿ)", space="O(n)", visual="backtrack",
                detail="At a depth, skip nums[i] when it equals nums[i − 1].",
                why="In [4,7,6,7], the 7s aren't adjacent. How many times does [4,7] appear?",
            ),
        ),
    ),
    Question(
        slug="permutations-ii", number=47, title="Permutations II",
        difficulty="Medium", topics=("trees",),
        summary="Return every distinct permutation of an array that may contain duplicates.",
        example="[1,1,2]  →  [[1,1,2], [1,2,1], [2,1,1]]",
        criterion="Which approach produces each permutation once, without a dedupe set?",
        hint="Among equal values, which copy should go first?",
        choices=(
            Choice(
                "Sort, use equal values in order", OPTIMAL, time="O(n·n!)", space="O(n)", visual="backtrack",
                detail="Skip nums[i] if it equals nums[i − 1] and nums[i − 1] isn't used yet.",
                why="Forcing equal copies to be placed left to right makes the copies indistinguishable, so each distinct permutation has exactly one path.",
            ),
            Choice(
                "All permutations into a set", SUBOPTIMAL, time="O(n·n!)", space="O(n·n!)", visual="set",
                detail="Treat values as distinct and dedupe the results.",
                why="Correct, but [1,1,1,1,2] builds 120 permutations for 5 answers.",
            ),
            Choice(
                "Skip any value equal to its neighbour", INCORRECT, time="O(n·n!)", space="O(n)", visual="backtrack",
                detail="Skip nums[i] whenever it equals nums[i − 1].",
                why="Then the second 1 can never be placed. Can [1,1,2] be completed?",
            ),
            Choice(
                "Dedupe the input first", INCORRECT, time="O(n·n!)", space="O(n)", visual="set",
                detail="Remove repeated values, then permute.",
                why="That permutes [1,2]. Are the results the right length?",
            ),
        ),
    ),
    Question(
        slug="remove-invalid-parentheses", number=301, title="Remove Invalid Parentheses",
        difficulty="Hard", topics=("trees",),
        summary="Remove the fewest parentheses from s (which may contain letters) to make it valid. Return every distinct result.",
        example="\"()())()\"  →  [\"(())()\", \"()()()\"]",
        criterion="Which approach only tries removals of the minimum size?",
        hint="One left-to-right pass can tell you how many '(' and ')' must go. How?",
        choices=(
            Choice(
                "Count removals, then backtrack exactly that many", OPTIMAL, time="O(n·2ⁿ) worst", space="O(n)", visual="backtrack",
                detail="Scan to count unmatched '(' and ')'; remove exactly those counts, skipping equal adjacent chars; validate at the end.",
                why="Knowing the exact counts bounds the search to minimum-size removals. Skipping a char equal to its predecessor avoids building the same string twice.",
            ),
            Choice(
                "BFS by number of removals", SUBOPTIMAL, time="O(n·2ⁿ)", space="O(n·2ⁿ)", visual="queue",
                detail="Remove one char from each string per level; stop at the first level with a valid string.",
                why="Correct, but each level holds every string with k removals, valid or not, in memory.",
            ),
            Choice(
                "Greedy one-pass fix", INCORRECT, time="O(n)", space="O(n)", visual="stack",
                detail="Drop each unmatched ')' while scanning, then unmatched '(' from the right.",
                why="That returns one string. The example has two.",
            ),
            Choice(
                "Remove all parentheses", INCORRECT, time="O(n)", space="O(n)", visual="brute",
                detail="An empty-bracket string is always valid.",
                why="Valid, yes. Is it the fewest removals?",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §4.6 search
    Question(
        slug="letter-combinations-of-a-phone-number", number=17, title="Letter Combinations of a Phone Number",
        difficulty="Medium", topics=("trees",),
        summary="Given digits 2–9, return every letter string they could spell on a phone keypad.",
        example="\"23\"  →  [\"ad\",\"ae\",\"af\",\"bd\",\"be\",\"bf\",\"cd\",\"ce\",\"cf\"]",
        criterion="Which approach generates only the strings in the answer?",
        hint="Position i of the result can only be a letter of digit i.",
        choices=(
            Choice(
                "One letter per digit, depth = position", OPTIMAL, time="O(n·4ⁿ)", space="O(n)", visual="backtrack",
                detail="At depth i, try each letter of digits[i]; record the string at depth n.",
                why="Each root-to-leaf path picks one letter per digit, so every leaf is an answer and every answer is a leaf.",
            ),
            Choice(
                "All letter strings, keep matching ones", SUBOPTIMAL, time="O(n·26ⁿ)", space="O(n)", visual="brute",
                detail="Generate every length-n string over a–z and keep those whose letters map to the digits.",
                why="Correct, but for \"23\" it builds 676 strings to keep 9.",
            ),
            Choice(
                "Combinations of all the letters", INCORRECT, time="O(C(3n, n))", space="O(n)", visual="backtrack",
                detail="Pool the letters of every digit and choose n of them.",
                why="That includes \"ab\" for \"23\". Is 'b' on the 3 key?",
            ),
            Choice(
                "First letter of each digit", INCORRECT, time="O(n)", space="O(n)", visual="greedy",
                detail="Return the string of first letters.",
                why="That's \"ad\". The example has nine strings.",
            ),
        ),
    ),
    Question(
        slug="generate-binary-strings-without-adjacent-zeros", number=3211, title="Generate Binary Strings Without Adjacent Zeros",
        difficulty="Medium", topics=("trees",),
        summary="Return every length-n binary string in which every length-2 substring contains at least one '1' (no two adjacent 0s). n ≤ 18.",
        example="3  →  [\"010\",\"011\",\"101\",\"110\",\"111\"]",
        criterion="Which approach does work proportional to the output?",
        hint="When is a '0' allowed at the next position?",
        choices=(
            Choice(
                "Place '0' only after '1'", OPTIMAL, time="O(n·output)", space="O(n)", visual="backtrack",
                detail="Always try '1'; try '0' only at the start or after a '1'.",
                why="Every prefix built this way extends to a valid string (append 1s), so the search never dead-ends. The output grows like φⁿ, far below 2ⁿ.",
            ),
            Choice(
                "All 2ⁿ masks, then filter", SUBOPTIMAL, time="O(n·2ⁿ)", space="O(n)", visual="bits",
                detail="Keep x when ~x & (~x >> 1) has no bits in the low n positions.",
                why="Correct and neat, but for n = 18 it checks 262144 masks to keep 6765.",
            ),
            Choice(
                "Forbid adjacent 1s", INCORRECT, time="O(n·output)", space="O(n)", visual="backtrack",
                detail="Place '1' only after '0'.",
                why="That swaps the rule. Is \"111\" in the example answer?",
            ),
            Choice(
                "Alternating strings", INCORRECT, time="O(n)", space="O(n)", visual="brute",
                detail="Return \"0101…\" and \"1010…\".",
                why="Where are \"011\" and \"111\"?",
            ),
        ),
    ),
    Question(
        slug="numbers-with-same-consecutive-differences", number=967, title="Numbers With Same Consecutive Differences",
        difficulty="Medium", topics=("trees",),
        summary="Return every n-digit number (no leading zero) whose adjacent digits differ by exactly k.",
        example="n = 3, k = 7  →  [181, 292, 707, 818, 929]",
        criterion="Which approach is correct and does work proportional to the output?",
        hint="Given the last digit, how many choices are there for the next one?",
        choices=(
            Choice(
                "Extend by last ± k", OPTIMAL, time="O(n·2ⁿ)", space="O(n)", visual="backtrack",
                detail="Start from 1–9; append last + k and last − k when in 0–9, once if k = 0.",
                why="Each digit has at most two successors, and every branch that stays in range is an answer. The k = 0 check stops +0 and −0 from duplicating.",
            ),
            Choice(
                "Check every n-digit number", SUBOPTIMAL, time="O(n·10ⁿ)", space="O(1)", visual="brute",
                detail="Loop from 10ⁿ⁻¹ to 10ⁿ − 1 and test each.",
                why="Correct, but for n = 9 that's 900 million numbers for at most 9·2⁸ answers.",
            ),
            Choice(
                "Extend by ± k always", INCORRECT, time="O(n·2ⁿ)", space="O(n)", visual="backtrack",
                detail="Append last + k and last − k without special cases.",
                why="With k = 0, how many times is 111 produced?",
            ),
            Choice(
                "Start from 0–9", INCORRECT, time="O(n·2ⁿ)", space="O(n)", visual="backtrack",
                detail="Allow the first digit to be 0.",
                why="Is 070 a 3-digit number?",
            ),
        ),
    ),
    Question(
        slug="finding-3-digit-even-numbers", number=2094, title="Finding 3-Digit Even Numbers",
        difficulty="Easy", topics=("trees",),
        summary="Given digits (with repeats), return in sorted order every distinct 3-digit even number (no leading zero) you can form, using each given digit at most once.",
        example="[2,1,3,0]  →  [102,120,130,132,210,230,302,310,312,320]",
        criterion="Which approach is linear in the number of digits?",
        hint="How many 3-digit even numbers are there in total?",
        choices=(
            Choice(
                "Count digits, test 100..998 even", OPTIMAL, time="O(n + 450)", space="O(1)", visual="counting",
                detail="Count each digit; for each even x from 100 to 998, check its digits fit the counts.",
                why="There are only 450 candidates, each checked in O(1) against the counts. Iterating in order also gives a sorted, distinct result for free.",
            ),
            Choice(
                "Triple loop over indices, then dedupe", SUBOPTIMAL, time="O(n³)", space="O(n³)", visual="brute",
                detail="Try every ordered triple of distinct indices, keep valid numbers in a set, sort.",
                why="Correct, but with 100 digits that's about a million triples for at most 450 answers.",
            ),
            Choice(
                "Reuse a digit freely", INCORRECT, time="O(450)", space="O(1)", visual="counting",
                detail="Check that each digit of x appears in the input at all.",
                why="With one 2, would 222 be allowed?",
            ),
            Choice(
                "Skip the leading-zero check", INCORRECT, time="O(n + 450)", space="O(1)", visual="counting",
                detail="Test every even x from 0 to 998 with digit counts.",
                why="Is 012 a 3-digit number?",
            ),
        ),
    ),
    Question(
        slug="unique-3-digit-even-numbers", number=3483, title="Unique 3-Digit Even Numbers",
        difficulty="Easy", topics=("trees",),
        summary="Given digits (with repeats), count the distinct 3-digit even numbers (no leading zero) you can form, using each given digit at most once.",
        example="[1,2,3,4]  →  12",
        criterion="Which approach is linear in the number of digits?",
        hint="Could you test candidates instead of building them?",
        choices=(
            Choice(
                "Count digits, test 100..998 even", OPTIMAL, time="O(n + 450)", space="O(1)", visual="counting",
                detail="Count each digit; count the even x in 100..998 whose digits fit the counts.",
                why="450 candidates, each an O(1) check. Testing numbers rather than index triples makes each number count once.",
            ),
            Choice(
                "Triple loop with a set", SUBOPTIMAL, time="O(n³)", space="O(n³)", visual="set",
                detail="Try every ordered triple of distinct indices and add valid numbers to a set.",
                why="Correct, but repeated digits build the same number many times before the set removes them.",
            ),
            Choice(
                "Count index triples", INCORRECT, time="O(n³)", space="O(1)", visual="brute",
                detail="Count valid ordered triples of distinct indices.",
                why="With [0,2,2], the triples (1,0,2) and (2,0,1) both make 202. Is that two numbers?",
            ),
            Choice(
                "Permutation formula", INCORRECT, time="O(1)", space="O(1)", visual="math",
                detail="Evens × (n − 1) × (n − 2).",
                why="For [0,0,2] it gives 6, but only 200 works. What did it count?",
            ),
        ),
    ),
    Question(
        slug="the-k-th-lexicographical-string-of-all-happy-strings-of-length-n", number=1415, title="The k-th Lexicographical String of All Happy Strings of Length n",
        difficulty="Medium", topics=("trees",),
        summary="A happy string uses only 'a', 'b', 'c' with no two equal adjacent letters. Return the k-th happy string of length n in lexicographic order, or \"\" if there are fewer than k.",
        example="n = 3, k = 9  →  \"cab\"",
        criterion="Which approach is linear in n?",
        hint="How many happy strings share a given first letter?",
        choices=(
            Choice(
                "Pick each letter by block size", OPTIMAL, time="O(n)", space="O(n)", visual="math",
                detail="Each choice at position i covers 2ⁿ⁻ⁱ⁻¹ strings; divide k − 1 by that to pick among the allowed letters.",
                why="After the first letter, every position has exactly two options, so the strings form equal blocks. Dividing k − 1 by the block size picks the letter directly.",
            ),
            Choice(
                "Generate in order, stop at the k-th", SUBOPTIMAL, time="O(n·k)", space="O(n)", visual="backtrack",
                detail="Backtrack trying 'a', 'b', 'c' in order, counting leaves until k.",
                why="Correct and fine for small k, but it builds k − 1 strings it doesn't need.",
            ),
            Choice(
                "Base-3 digits of k − 1", INCORRECT, time="O(n)", space="O(n)", visual="math",
                detail="Write k − 1 in base 3 and map 0, 1, 2 to a, b, c.",
                why="For k = 1 that gives \"aaa\". Is that happy?",
            ),
            Choice(
                "All strings over a, b, c", INCORRECT, time="O(n·3ⁿ)", space="O(n·3ⁿ)", visual="brute",
                detail="Generate every string in order and return the k-th.",
                why="The 2nd string is \"aab\". Is it happy?",
            ),
        ),
    ),
    Question(
        slug="path-with-maximum-gold", number=1219, title="Path with Maximum Gold",
        difficulty="Medium", topics=("trees",),
        summary="In a grid of gold amounts (at most 25 cells hold gold), walk up, down, left or right through gold cells without revisiting any, starting and stopping anywhere. Return the most gold you can collect.",
        example="[[0,6,0],[5,8,7],[0,9,0]]  →  24",
        criterion="Which approach is correct and fits the limit of 25 gold cells?",
        hint="A path can't revisit a cell. What do you undo when you back out of a step?",
        choices=(
            Choice(
                "DFS from each gold cell, undo marks", OPTIMAL, time="O(G·3ᴳ)", space="O(G)", visual="backtrack",
                detail="Zero a cell when entering, explore its neighbours, restore it on return; track the best total.",
                why="Each step has at most 3 new directions, and tight grids keep paths short. Restoring the cell lets other paths use it.",
            ),
            Choice(
                "DP over visited sets", SUBOPTIMAL, time="O(2ᴳ·G²)", space="O(2ᴳ·G)", visual="dp-2d",
                detail="dp[mask][cell] = best gold for a path covering mask that ends at cell.",
                why="Correct, but 2²⁵ masks times 25 cells is about 800 million states, almost all unreachable.",
            ),
            Choice(
                "Greedy richest neighbour", INCORRECT, time="O(G²)", space="O(1)", visual="greedy",
                detail="From each start, step to the neighbour with the most gold.",
                why="A rich neighbour can lead into a dead end. Does local greed see the 9 behind the 8?",
            ),
            Choice(
                "Largest connected region total", INCORRECT, time="O(G)", space="O(G)", visual="graph-dfs",
                detail="Flood fill and return the biggest region sum.",
                why="The example's region holds 35, but the answer is 24. Can a single path visit all five cells?",
            ),
        ),
    ),
    Question(
        slug="word-search", number=79, title="Word Search",
        difficulty="Medium", topics=("trees",),
        summary="Decide whether word can be traced through 4-directionally adjacent cells of a letter grid, using each cell at most once.",
        example="[[A,B,C,E],[S,F,C,S],[A,D,E,E]], \"ABCCED\"  →  true",
        criterion="Which approach tracks used cells in O(1) per step?",
        hint="When a branch fails, what must you undo so other branches can reuse those cells?",
        choices=(
            Choice(
                "DFS marking cells in place", OPTIMAL, time="O(m·n·3ᴸ)", space="O(L)", visual="backtrack",
                detail="From each cell matching word[0], overwrite the cell with a marker, try its neighbours for the next letter, then restore it.",
                why="The marker blocks reuse in O(1), and restoring it on return frees the cell for other paths. After the first step only 3 directions are new.",
            ),
            Choice(
                "DFS copying a visited set", SUBOPTIMAL, time="O(m·n·3ᴸ·L)", space="O(L²)", visual="set",
                detail="Pass a fresh copy of the visited set into each recursive call.",
                why="Correct, but each step copies up to L cells that undo-on-return would have handled for free.",
            ),
            Choice(
                "Check letter counts", INCORRECT, time="O(m·n + L)", space="O(1)", visual="counting",
                detail="Return true if the grid has enough of every letter in word.",
                why="The letters could be scattered. Must they be adjacent?",
            ),
            Choice(
                "DFS without marking", INCORRECT, time="O(m·n·4ᴸ)", space="O(L)", visual="graph-dfs",
                detail="Follow matching neighbours without tracking used cells.",
                why="For \"ABA\" on a grid with just [A,B], the path A→B→A reuses a cell. Should that count?",
            ),
        ),
    ),
    Question(
        slug="matchsticks-to-square", number=473, title="Matchsticks to Square",
        difficulty="Medium", topics=("trees",),
        summary="Use every matchstick exactly once, without breaking any, to form a square. Return whether it's possible. n ≤ 15.",
        example="[1,1,2,2,2]  →  true",
        criterion="Which approach has the best worst-case bound?",
        hint="If you fill sides one at a time, what does a set of used sticks tell you about the side in progress?",
        choices=(
            Choice(
                "DP over subsets of used sticks", OPTIMAL, time="O(n·2ⁿ)", space="O(2ⁿ)", visual="bits",
                detail="Fill sides in order; dp[mask] = length of the current side after using mask, or −1; add stick i only if it fits.",
                why="The sticks used fix how much of the current side is filled (total mod side). So each of the 2ⁿ sets is solved once, whatever order built it.",
            ),
            Choice(
                "Backtrack sticks into four sides", SUBOPTIMAL, time="O(4ⁿ)", space="O(n)", visual="backtrack",
                detail="Sort descending, place each stick on a side that fits, skip sides of equal length.",
                why="Correct and often fast with those prunes, but its worst case is still 4ⁿ, far above n·2ⁿ.",
            ),
            Choice(
                "Greedy: longest stick to shortest side", INCORRECT, time="O(n log n)", space="O(1)", visual="greedy",
                detail="Sort descending and add each stick to the currently shortest side.",
                why="For [6,6,3,3,2,2,2] (side 6), it puts the two 3s on different sides and ends with 7 and 5. Yet 3 + 3 and 2 + 2 + 2 work.",
            ),
            Choice(
                "Check the total and the longest stick", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="True if the total is divisible by 4 and no stick is longer than a side.",
                why="[3,3,3,3,4] totals 16 with no stick over 4. Can a 3 be part of a side of 4?",
            ),
        ),
    ),
    Question(
        slug="word-search-ii", number=212, title="Word Search II",
        difficulty="Hard", topics=("trees",),
        summary="Return every word from a list that can be traced through 4-directionally adjacent cells of a letter grid, using each cell at most once per word.",
        example="[[o,a,a,n],[e,t,a,e],[i,h,k,r],[i,f,l,v]], [\"oath\",\"pea\",\"eat\",\"rain\"]  →  [\"eat\", \"oath\"]",
        criterion="Which approach searches the grid once for all words?",
        hint="Many words share prefixes. What structure lets one DFS follow all of them at once?",
        choices=(
            Choice(
                "Trie of words, one DFS per cell", OPTIMAL, time="O(m·n·3ᴸ)", space="O(total letters)", visual="trie",
                detail="Walk the grid and the trie together; record a word at its end node and prune finished branches.",
                why="The trie answers 'can any word continue here?' in O(1), so dead prefixes stop at once, and shared prefixes are explored once for all words.",
            ),
            Choice(
                "Word Search once per word", SUBOPTIMAL, time="O(W·m·n·3ᴸ)", space="O(L)", visual="backtrack",
                detail="Run the single-word DFS for each word.",
                why="Correct, but \"oath\" and \"oat\" both re-walk o→a→t from scratch, and the grid is scanned W times.",
            ),
            Choice(
                "Check letter counts per word", INCORRECT, time="O(m·n + total)", space="O(1)", visual="counting",
                detail="Keep a word if the grid has enough of each of its letters.",
                why="Letters must form a path. Could \"rain\" pass this test without being traceable?",
            ),
            Choice(
                "Trie DFS without marking cells", INCORRECT, time="O(m·n·4ᴸ)", space="O(total letters)", visual="trie",
                detail="Follow the trie through the grid but allow revisiting cells.",
                why="A word like \"aba\" could bounce between two cells. Is reuse allowed?",
            ),
        ),
    ),
    Question(
        slug="shopping-offers", number=638, title="Shopping Offers",
        difficulty="Medium", topics=("trees",),
        summary="Items have unit prices; special offers sell fixed bundles at a fixed price. Buy exactly the needed amounts (no extras) at the lowest cost. At most 6 items, need ≤ 10 each.",
        example="price = [2,5], special = [[3,0,5],[1,2,10]], needs = [3,2]  →  14",
        criterion="Which approach solves each remaining-needs state once?",
        hint="After a few offers, the same needs vector can be reached in different orders.",
        choices=(
            Choice(
                "DFS on needs with memo", OPTIMAL, time="O(S·k·n)", space="O(S)", visual="recursion",
                detail="cost(needs) = min(buy the rest at unit price, offer + cost(needs − offer) for each offer that fits); cache by needs. (S = needs vectors, k = offers.)",
                why="At most 11⁶ needs vectors exist, and caching solves each once. Unit prices cover whatever offers can't.",
            ),
            Choice(
                "DFS without memo", SUBOPTIMAL, time="O(kᵈ)", space="O(d)", visual="backtrack",
                detail="Try every sequence of offers, recomputing shared states.",
                why="Correct, but using offer A then B and B then A both solve the same remaining needs from scratch.",
            ),
            Choice(
                "Best saving offer first", INCORRECT, time="O(k·n·d)", space="O(n)", visual="greedy",
                detail="Repeatedly take the offer with the largest saving that fits.",
                why="A big-saving offer can use up items that two smaller offers would have covered better. What guarantees greed is safe here?",
            ),
            Choice(
                "Allow buying extras", INCORRECT, time="O(S·k·n)", space="O(S)", visual="recursion",
                detail="Apply an offer even if it exceeds the needs, clamping at 0.",
                why="The rules say exactly the needed amounts. Would a cheap oversized bundle count?",
            ),
        ),
    ),
    Question(
        slug="24-game", number=679, title="24 Game",
        difficulty="Hard", topics=("trees",),
        summary="Given 4 cards (1–9), decide whether + − × ÷ and parentheses can combine them into 24. Division is real, not integer.",
        example="[4,1,8,7]  →  true    ((8 − 4) × (7 − 1))",
        criterion="Which approach covers every parenthesization without listing them?",
        hint="Any expression's last step combines two values. What's left after you combine two cards?",
        choices=(
            Choice(
                "Combine any two, recurse on the rest", OPTIMAL, time="O(1)", space="O(1)", visual="backtrack",
                detail="Pick an ordered pair, replace it with a op b for each op, recurse until one value; compare with 24 within ε.",
                why="Every expression tree is built by repeatedly merging two values, so this reaches all of them. With 4 cards the search is a few thousand steps.",
            ),
            Choice(
                "Build expression strings and evaluate", SUBOPTIMAL, time="O(1)", space="O(1)", visual="brute",
                detail="List every order × operators × the 5 bracket shapes as text and parse each.",
                why="Correct if the bracket shapes are all listed, but it builds and parses strings for work the merge recursion does with numbers.",
            ),
            Choice(
                "Left to right, no parentheses", INCORRECT, time="O(1)", space="O(1)", visual="brute",
                detail="Try every order and operator, evaluating left to right.",
                why="[3,3,8,8] needs 8 ÷ (3 − 8 ÷ 3). Can left-to-right build that?",
            ),
            Choice(
                "Integer division", INCORRECT, time="O(1)", space="O(1)", visual="backtrack",
                detail="Same search, but a ÷ b uses integer division.",
                why="8 ÷ 3 must stay 2.67 in 8 ÷ (3 − 8 ÷ 3). What does it become?",
            ),
        ),
    ),
    Question(
        slug="expression-add-operators", number=282, title="Expression Add Operators",
        difficulty="Hard", topics=("trees",),
        summary="Insert +, − or × between the digits of num (operands may have several digits, no leading zeros) so the expression equals target. Return all such expressions.",
        example="\"123\", 6  →  [\"1*2*3\", \"1+2+3\"]",
        criterion="Which approach evaluates each expression as it's built?",
        hint="When you append × x, which part of the running value has to change?",
        choices=(
            Choice(
                "Backtrack with value and last term", OPTIMAL, time="O(n·4ⁿ)", space="O(n)", visual="backtrack",
                detail="Carry the value and the last term; for × x, value − last + last·x and last becomes last·x.",
                why="× binds to the previous term only. Keeping that term lets you undo and redo it in O(1), so no expression is re-parsed.",
            ),
            Choice(
                "Build every string, then evaluate", SUBOPTIMAL, time="O(n²·4ⁿ)", space="O(n)", visual="brute",
                detail="Generate all expressions as text and parse each with precedence.",
                why="Correct, but each of the 4ⁿ strings is parsed from scratch.",
            ),
            Choice(
                "Evaluate left to right", INCORRECT, time="O(n·4ⁿ)", space="O(n)", visual="backtrack",
                detail="Apply each operator to the running value as it's appended.",
                why="1 + 2 × 3 would give 9. What's the real value?",
            ),
            Choice(
                "Allow leading zeros", INCORRECT, time="O(n·4ⁿ)", space="O(n)", visual="backtrack",
                detail="Let operands like \"05\" through.",
                why="Is \"1*05\" a valid expression here?",
            ),
        ),
    ),
    Question(
        slug="word-ladder-ii", number=126, title="Word Ladder II",
        difficulty="Hard", topics=("trees",),
        summary="Return every shortest transformation sequence from beginWord to endWord, changing one letter at a time, with each intermediate word in the list.",
        example="hit → cog, [hot,dot,dog,lot,log,cog]  →  [[hit,hot,dot,dog,cog], [hit,hot,lot,log,cog]]",
        criterion="Which approach only builds sequences of the shortest length?",
        hint="BFS finds the shortest distance. What would you need to remember to rebuild every shortest path?",
        choices=(
            Choice(
                "Layered BFS, then backtrack parents", OPTIMAL, time="O(N·L·26 + output)", space="O(N·L)", visual="graph-bfs",
                detail="BFS level by level, recording every parent from the previous level; stop after the level that reaches endWord; DFS back from endWord.",
                why="Edges only between consecutive BFS levels form exactly the shortest-path DAG. Walking it backwards from endWord visits only words on some shortest path.",
            ),
            Choice(
                "DFS all paths with a depth limit", SUBOPTIMAL, time="O(bᵈ)", space="O(d)", visual="backtrack",
                detail="Find the shortest length first, then DFS every path of that length.",
                why="Correct, but the DFS wanders into branches that BFS already knows can't reach endWord in time.",
            ),
            Choice(
                "BFS with one parent per word", INCORRECT, time="O(N·L·26)", space="O(N)", visual="graph-bfs",
                detail="Store the first parent that reaches each word.",
                why="Both dog and log are reached at the same level and both lead to cog. Which sequence survives?",
            ),
            Choice(
                "First path found by DFS", INCORRECT, time="O(N·L·26)", space="O(N)", visual="graph-dfs",
                detail="Return the path DFS finds first.",
                why="Is the first DFS path the shortest? And the task wants all of them.",
            ),
        ),
    ),
    Question(
        slug="stickers-to-spell-word", number=691, title="Stickers to Spell Word",
        difficulty="Hard", topics=("trees",),
        summary="Each sticker is a word; you may use any sticker any number of times and cut out its letters. Return the fewest stickers needed to spell target, or −1. target ≤ 15 letters.",
        example="[\"with\",\"example\",\"science\"], \"thehat\"  →  3",
        criterion="Which approach solves each set of covered letters once?",
        hint="Number the target's letters. What state fully describes your progress?",
        choices=(
            Choice(
                "DP over target-letter masks", OPTIMAL, time="O(2ᵀ·S·T)", space="O(2ᵀ)", visual="bits",
                detail="dp[mask] = fewest stickers to cover mask; from each mask, apply each sticker greedily to uncovered positions.",
                why="Progress is just which target positions are covered: 2¹⁵ states. Applying a sticker to a mask is deterministic, so each state is relaxed once per sticker.",
            ),
            Choice(
                "Backtrack stickers without memo", SUBOPTIMAL, time="O(Sᵀ)", space="O(T)", visual="backtrack",
                detail="Try each sticker on the remaining letters and recurse.",
                why="Correct, but using \"with\" then \"example\" reaches the same remaining letters as the reverse, and both are solved again.",
            ),
            Choice(
                "Sticker covering the most letters first", INCORRECT, time="O(S·T²)", space="O(T)", visual="greedy",
                detail="Repeatedly use the sticker that covers the most remaining letters.",
                why="A sticker that covers many letters now can leave a set that needs more stickers later. Why would greed be safe?",
            ),
            Choice(
                "Max over letters of need / supply", INCORRECT, time="O(S·T)", space="O(1)", visual="counting",
                detail="For each letter, divide how many target needs by the most any sticker has; take the max.",
                why="Each letter is counted as if it had its own stickers. Can one sticker serve two letters at once?",
            ),
        ),
    ),
    Question(
        slug="zuma-game", number=488, title="Zuma Game",
        difficulty="Hard", topics=("trees",),
        summary="Insert balls from your hand (≤ 5) anywhere in a row (≤ 16); any group of 3+ same-coloured balls vanishes, with chain reactions. Return the fewest insertions to clear the row, or −1.",
        example="board = \"WWRRBBWW\", hand = \"WRBRW\"  →  2",
        criterion="Which approach finds the fewest insertions without revisiting states?",
        hint="A state is the row plus what's left in your hand. Which search returns the first state reached with the fewest moves?",
        choices=(
            Choice(
                "BFS over (row, sorted hand) with a seen set", OPTIMAL, time="O(states·b·h)", space="O(states)", visual="queue",
                detail="Each move inserts one hand ball at a position and collapses groups; skip duplicate states; stop at the first empty row.",
                why="BFS explores by number of insertions, so the first cleared row is optimal. Sorting the hand merges states that differ only in hand order.",
            ),
            Choice(
                "DFS over every insertion, no memo", SUBOPTIMAL, time="O((b·h)ʰ)", space="O(h)", visual="backtrack",
                detail="Try each ball at each position, recurse, keep the minimum.",
                why="Correct, but the same row and hand are reached by many insertion orders and solved again each time.",
            ),
            Choice(
                "Greedy: finish the cheapest group", INCORRECT, time="O(b·h)", space="O(b)", visual="greedy",
                detail="Always complete the group that needs the fewest hand balls.",
                why="Clearing one group first can merge neighbours into a bigger chain, or break one. Does cheapest-now mean fewest overall?",
            ),
            Choice(
                "Insert without chain reactions", INCORRECT, time="O(states·b·h)", space="O(states)", visual="queue",
                detail="Remove only the group the inserted ball completes.",
                why="In the example, clearing RR then BB lets WWWW meet. Should that vanish too?",
            ),
        ),
    ),
    Question(
        slug="lcp-58-cube-assembly", number=None, title="Cube Assembly",
        difficulty="Hard", topics=("trees",),
        ref="LCP 58", url="https://leetcode.cn/problems/De4qBB/",
        summary="Six N×N pieces (N ≤ 10, solid inside, ragged edges) may be rotated and flipped. Decide whether they fit together as the six faces of a solid N×N×N cube, each piece centred on its face.",
        example="Six 3×3 pieces from the problem's first example  →  true",
        criterion="Which approach is correct and avoids trying symmetric copies of the same cube?",
        hint="A cube can be turned freely. Does it matter which way the first piece is placed?",
        choices=(
            Choice(
                "Fix piece 0, backtrack faces with a 3D occupancy grid", OPTIMAL, time="O(5!·8⁵·N²)", space="O(N³)", visual="backtrack",
                detail="Place piece 0 on the bottom as given; for each remaining face, try each unused piece in its 8 orientations, mark its boundary cells, and back out on overlap.",
                why="Turning the whole cube maps any solution to one with piece 0 on the bottom in a fixed pose, so fixing it loses nothing. Overlaps are caught as each face is placed.",
            ),
            Choice(
                "All assignments and orientations, check at the end", SUBOPTIMAL, time="O(6!·8⁶·N²)", space="O(N³)", visual="brute",
                detail="Try every piece-to-face map and orientation for all six pieces, then test the cube.",
                why="Correct, but it builds 48 symmetric copies of each cube and checks overlaps only after all six faces are placed.",
            ),
            Choice(
                "Count the cells", INCORRECT, time="O(N²)", space="O(1)", visual="counting",
                detail="True if the pieces' 1s add up to the cube's surface cell count, 6N² − 12N + 8.",
                why="Two edges that both stick out can't share a cell. Does the total see that?",
            ),
            Choice(
                "Rotations only", INCORRECT, time="O(5!·4⁵·N²)", space="O(N³)", visual="backtrack",
                detail="Same search, but try only the 4 rotations of each piece.",
                why="The rules allow flipping a piece over. Can a mirrored edge be matched without it?",
            ),
        ),
    ),
    Question(
        slug="word-rectangle-lcci", number=None, title="Word Rectangle",
        difficulty="Hard", topics=("trees",),
        ref="面试题 17.25", url="https://leetcode.cn/problems/word-rectangle-lcci/",
        summary="From a word list, build the largest-area rectangle of letters in which every row and every column is a word from the list.",
        example="[\"this\",\"real\",\"hard\",\"trh\",\"hea\",\"iar\",\"sld\"]  →  [\"this\",\"real\",\"hard\"]",
        criterion="Which approach rejects a partial rectangle as soon as a column can't become a word?",
        hint="After placing some rows, each column is a prefix. What structure checks prefixes quickly?",
        choices=(
            Choice(
                "Rows by length, trie-checked column prefixes", OPTIMAL, time="Exponential, heavily pruned", space="O(total letters)", visual="trie",
                detail="Group words by length; for each width, add rows from that group while every column prefix is in the trie; skip sizes that can't beat the best area.",
                why="A column prefix missing from the trie can't be completed, so the branch stops at the row that broke it. Bounding by area skips hopeless sizes.",
            ),
            Choice(
                "Pick all rows, then check columns", SUBOPTIMAL, time="Exponential, no pruning", space="O(rows·width)", visual="brute",
                detail="Choose a full stack of rows and only then test whether each column is a word.",
                why="Correct, but a stack whose first two rows already break a column is still filled out.",
            ),
            Choice(
                "Longest words as rows", INCORRECT, time="O(W·L)", space="O(W)", visual="greedy",
                detail="Stack the longest words and stop when a column fails.",
                why="The longest words may never form valid columns. Does greed pick the largest valid rectangle?",
            ),
            Choice(
                "Squares only", INCORRECT, time="Exponential", space="O(total letters)", visual="trie",
                detail="Search only rectangles whose height equals the width.",
                why="The example answer is 3 rows of 4 letters. Is that a square?",
            ),
        ),
    ),
    Question(
        slug="the-knights-tour", number=2664, title="The Knight’s Tour",
        difficulty="Medium", topics=("trees",),
        summary="On an m×n board (m, n ≤ 5), starting at a given cell, return a board numbering the cells 0..m·n − 1 in the order a knight visits each exactly once. A tour is guaranteed.",
        example="m = 3, n = 4, start (0, 0)  →  a 3×4 board with 0 at (0, 0)",
        criterion="Which approach is always correct and hits the fewest dead ends?",
        hint="Which next square is most likely to be stranded if you don't visit it soon?",
        choices=(
            Choice(
                "Backtracking, fewest onward moves first", OPTIMAL, time="O(8ᵐⁿ) worst", space="O(m·n)", visual="backtrack",
                detail="Try moves in order of how many unvisited squares they lead to (Warnsdorff); undo on failure.",
                why="Squares with few exits get used before they're cut off, so dead ends are rare. Backtracking keeps it correct when the rule guesses wrong.",
            ),
            Choice(
                "Backtracking in fixed move order", SUBOPTIMAL, time="O(8ᵐⁿ) worst", space="O(m·n)", visual="recursion",
                detail="Try the 8 knight moves in the same order every time.",
                why="Correct, but it happily strands corner squares and then searches long branches that can't finish.",
            ),
            Choice(
                "Warnsdorff without undo", INCORRECT, time="O(m·n·8)", space="O(m·n)", visual="greedy",
                detail="Always move to the square with the fewest onward moves and never back up.",
                why="On small boards the rule can tie and pick wrong. What happens when it walks into a dead end?",
            ),
            Choice(
                "BFS distances from the start", INCORRECT, time="O(m·n)", space="O(m·n)", visual="graph-bfs",
                detail="Number each square by its knight distance from the start.",
                why="Many squares share a distance. Is that an order of single moves?",
            ),
        ),
    ),
    Question(
        slug="sequential-grid-path-cover", number=3565, title="Sequential Grid Path Cover",
        difficulty="Medium", topics=("trees",),
        summary="In a small grid, k cells hold 1..k and the rest hold 0. Return a path of 4-directional moves that visits every cell exactly once and meets the numbered cells in order 1, 2, …, k, or [] if none exists.",
        example="[[1,0,0],[0,0,2]], k = 2  →  [[0,0],[1,0],[1,1],[0,1],[0,2],[1,2]]",
        criterion="Which approach rejects a path as soon as it meets a number out of order?",
        hint="Track the next number you expect. When may the path step onto a numbered cell?",
        choices=(
            Choice(
                "DFS with a visited mask and next expected number", OPTIMAL, time="O(m·n·3ᵐⁿ)", space="O(m·n)", visual="backtrack",
                detail="Step only onto unvisited cells that are 0 or exactly the next number; succeed when all cells are visited.",
                why="An out-of-order number kills the branch at the step it happens, long before the path is complete.",
            ),
            Choice(
                "All Hamiltonian paths, then check order", SUBOPTIMAL, time="O(m·n·4ᵐⁿ)", space="O(m·n)", visual="brute",
                detail="Enumerate every path covering all cells and test the numbers at the end.",
                why="Correct, but a path that hits 2 before 1 is still walked to the end.",
            ),
            Choice(
                "Shortest paths between consecutive numbers", INCORRECT, time="O(k·m·n)", space="O(m·n)", visual="graph-bfs",
                detail="BFS from 1 to 2, 2 to 3, … and join them.",
                why="Must the path cover every cell exactly once? Shortest hops skip cells and may cross each other.",
            ),
            Choice(
                "Snake through the rows", INCORRECT, time="O(m·n)", space="O(1)", visual="matrix",
                detail="Visit row 0 left to right, row 1 right to left, and so on.",
                why="That covers every cell, but who checks that 1 comes before 2?",
            ),
        ),
    ),
    Question(
        slug="strobogrammatic-number-ii", number=247, title="Strobogrammatic Number II",
        difficulty="Medium", topics=("trees",),
        summary="A strobogrammatic number reads the same rotated 180°. Return all of length n (no leading zero unless n = 1).",
        example="2  →  [\"11\", \"69\", \"88\", \"96\"]",
        criterion="Which approach does work proportional to the output?",
        hint="Which digit pairs map onto each other when rotated?",
        choices=(
            Choice(
                "Build from the outside in with pairs", OPTIMAL, time="O(n·5^(n/2))", space="O(n)", visual="backtrack",
                detail="Fill positions i and n−1−i with (0,0), (1,1), (6,9), (8,8), (9,6), no 0 outside; the middle of odd n uses 0, 1 or 8.",
                why="Each choice fixes two positions with a pair that rotates correctly, so every leaf is an answer.",
            ),
            Choice(
                "Test every n-digit number", SUBOPTIMAL, time="O(n·10ⁿ)", space="O(1)", visual="brute",
                detail="Rotate each number and compare.",
                why="Correct, but for n = 10 that's 9 billion numbers for 2500 answers.",
            ),
            Choice(
                "Allow 0 on the outside", INCORRECT, time="O(n·5^(n/2))", space="O(n)", visual="backtrack",
                detail="Use all five pairs at every layer.",
                why="That builds \"00\" and \"0690\". Are those length-n numbers?",
            ),
            Choice(
                "Only symmetric digits 0, 1, 8", INCORRECT, time="O(n·3^(n/2))", space="O(n)", visual="backtrack",
                detail="Mirror digits that look the same rotated.",
                why="Where are \"69\" and \"96\"?",
            ),
        ),
    ),
    Question(
        slug="strobogrammatic-number-iii", number=248, title="Strobogrammatic Number III",
        difficulty="Hard", topics=("trees",),
        summary="Count strobogrammatic numbers in [low, high], given as strings of up to 15 digits.",
        example="low = \"50\", high = \"100\"  →  3",
        criterion="Which approach is independent of the size of the range?",
        hint="How many strobogrammatic numbers have 15 digits, compared with how many numbers do?",
        choices=(
            Choice(
                "Generate by length, compare at the edges", OPTIMAL, time="O(n·5^(n/2))", space="O(n)", visual="backtrack",
                detail="For each length from len(low) to len(high), build all strobogrammatic strings and count those within range.",
                why="There are only about 5^(n/2) candidates per length, and string comparison handles the bounds without overflow.",
            ),
            Choice(
                "Test every number in the range", SUBOPTIMAL, time="O(n·(high − low))", space="O(1)", visual="brute",
                detail="Loop from low to high and check each.",
                why="Correct, but the range can hold 10¹⁵ numbers.",
            ),
            Choice(
                "Count per length by formula", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="Add the full count for each length between the bounds.",
                why="For low = \"50\", that counts 11, which is below 50. What about the partial lengths?",
            ),
            Choice(
                "Only symmetric digits 0, 1, 8", INCORRECT, time="O(n·3^(n/2))", space="O(n)", visual="backtrack",
                detail="Build numbers from digits that look the same rotated.",
                why="The example's answers are 69, 88 and 96. How many would this find?",
            ),
        ),
    ),
    Question(
        slug="minimum-unique-word-abbreviation", number=411, title="Minimum Unique Word Abbreviation",
        difficulty="Hard", topics=("trees",),
        summary="Find a shortest abbreviation of target (letters kept, runs of skipped letters as numbers; length counts both) that is not also an abbreviation of any dictionary word.",
        example="target = \"apple\", dictionary = [\"blade\"]  →  \"a4\"",
        criterion="Which approach tests a candidate against a dictionary word in O(1)?",
        hint="Only same-length words can clash. For one of them, which kept positions would tell it apart from target?",
        choices=(
            Choice(
                "Difference masks, search kept-position masks", OPTIMAL, time="O(2ᵐ·n)", space="O(n)", visual="bits",
                detail="For each same-length word, set bits where it differs from target; a kept-position mask is unique if it hits every difference mask. Search masks by abbreviation length.",
                why="An abbreviation fails only if every kept letter also matches the dictionary word. That's mask & diff == 0, one AND per word.",
            ),
            Choice(
                "Generate abbreviations, match as strings", SUBOPTIMAL, time="O(2ᵐ·n·m)", space="O(2ᵐ·m)", visual="backtrack",
                detail="List every abbreviation of target and test it against each word letter by letter.",
                why="Correct, but each test walks the strings, and words of other lengths are compared for nothing.",
            ),
            Choice(
                "Just the length", INCORRECT, time="O(1)", space="O(1)", visual="math",
                detail="Return str(len(target)).",
                why="\"5\" also abbreviates \"blade\". Is it unique?",
            ),
            Choice(
                "Keep the first differing letter per word", INCORRECT, time="O(n·m)", space="O(m)", visual="greedy",
                detail="For each dictionary word, keep the first position where it differs from target.",
                why="For [\"bpplx\", \"aqplz\"] it keeps a and p (\"ap3\"), but keeping only the e gives \"4e\". Which is shorter?",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §4.7 meet in the middle
    Question(
        slug="target-sum", number=494, title="Target Sum",
        difficulty="Medium", topics=("trees",),
        summary="Put + or − before each number so the expression equals target. Count the ways. n ≤ 20, sum ≤ 1000.",
        example="[1,1,1,1,1], 3  →  5",
        criterion="Which approach is polynomial in n and the total sum?",
        hint="If P is the set with +, then sum(P) − (S − sum(P)) = target. What must sum(P) be?",
        choices=(
            Choice(
                "Count subsets summing to (S + target) / 2", OPTIMAL, time="O(n·S)", space="O(S)", visual="dp-1d",
                detail="Return 0 if S + target is odd or |target| > S; otherwise 0/1-knapsack count of subsets with that sum.",
                why="Choosing signs is choosing the + set P, and sum(P) is fixed by the algebra. Counting subsets by sum is a classic O(n·S) DP.",
            ),
            Choice(
                "Meet in the middle", SUBOPTIMAL, time="O(2^(n/2)·n)", space="O(2^(n/2))", visual="hashmap",
                detail="Count signed sums of each half in a map; for each left sum s, add count[target − s] from the right.",
                why="Correct and fine for n = 20, but exponential in n. With the sum capped at 1000, n·S is the smaller bound.",
            ),
            Choice(
                "Halve without checking parity", INCORRECT, time="O(n·S)", space="O(S)", visual="dp-1d",
                detail="Count subsets with sum (S + target) // 2.",
                why="For [1], target 2: (1 + 2) // 2 = 1, and {1} sums to 1. Can ±1 make 2?",
            ),
            Choice(
                "Greedy signs", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Add a number if the running total is below target, else subtract it.",
                why="That builds one assignment. The example has five.",
            ),
        ),
    ),
    Question(
        slug="lcp-82-tree-of-all-souls", number=None, title="Tree of All Souls",
        difficulty="Hard", topics=("trees",),
        ref="LCP 82", url="https://leetcode.cn/problems/cnHoX6/",
        summary="Arrange n ≤ 9 gems as the leaves of a full binary tree (shapes and leaf orders both count). A traversal writes 1 on entering a node, the gem's value at a leaf, and 9 on leaving. Count arrangements whose written number ≡ target (mod p).",
        example="gem = [2,3], p = 100000007, target = 11391299  →  1",
        criterion="Which approach is fast enough for 9 gems?",
        hint="The digits a subtree writes have a length fixed by which gems it holds. So a subtree is described by its gem set and its remainder mod p.",
        choices=(
            Choice(
                "Subset DP of remainders, matched at the root", OPTIMAL, time="O(3ⁿ·K²)", space="O(2ⁿ·K)", visual="hashmap",
                detail="For each gem set, a map remainder → count built from every split into left and right sets; at the root, for each left remainder look up the one right remainder that completes target.",
                why="Each subset's maps are built once and reused by every parent. The root's map would be the largest, so meeting in the middle there skips building it.",
            ),
            Choice(
                "Enumerate every tree and leaf order", SUBOPTIMAL, time="O(n·n!·Cₙ₋₁)", space="O(n)", visual="brute",
                detail="Build every shape and every assignment of gems to leaves and compute the number mod p.",
                why="Correct, but for n = 9 that's 1430 shapes × 362880 orders, half a billion numbers.",
            ),
            Choice(
                "Merge gems with equal values", INCORRECT, time="O(3ⁿ·K²)", space="O(2ⁿ·K)", visual="set",
                detail="Treat gems with the same value as one kind.",
                why="The rules count different gem numbers as different arrangements even with equal values. What happens to example 2's 3s?",
            ),
            Choice(
                "Concatenate leaf values only", INCORRECT, time="O(n·n!)", space="O(n)", visual="brute",
                detail="Ignore the 1s and 9s and count leaf orders whose concatenation hits target.",
                why="The 1s and 9s depend on the tree's shape. Do [2,3] in two different shapes write the same number?",
            ),
        ),
    ),
]
