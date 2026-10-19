"""Core route step 1: sliding window (滑动窗口与双指针 §1, §2)."""

from .question_schema import INCORRECT, OPTIMAL, SUBOPTIMAL, Choice, Question

QUESTIONS = [
    # ---------------------------------------------------------------- §1.1 fixed-length window
    Question(
        slug="maximum-number-of-vowels-in-a-substring-of-given-length", number=1456, title="Maximum Number of Vowels in a Substring of Given Length",
        difficulty="Medium", topics=("sliding-window",),
        summary="Return the most vowels in any substring of s of length k.",
        example="\"abciiidef\", k = 3  →  3",
        criterion="Which approach is linear with O(1) extra space?",
        hint="Moving the window one step changes which two characters?",
        choices=(
            Choice(
                "Slide a fixed window, update the count", OPTIMAL, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Add 1 if the entering char is a vowel, subtract 1 if the leaving one was; track the max.",
                why="Neighbouring windows share k − 1 characters, so only the one entering and the one leaving change the count.",
            ),
            Choice(
                "Recount every window", SUBOPTIMAL, time="O(n·k)", space="O(1)", visual="brute",
                detail="For each start, count vowels in the next k characters.",
                why="Correct, but it recounts k − 1 characters the previous window already counted.",
            ),
            Choice(
                "Longest vowel run, capped at k", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Find the longest run of consecutive vowels and return min(run, k).",
                why="For \"aba\", k = 3, the longest run is 1. How many vowels does the whole window hold?",
            ),
            Choice(
                "Count the first window only", INCORRECT, time="O(k)", space="O(1)", visual="brute",
                detail="Return the vowel count of s[0..k).",
                why="In the example, \"abc\" has 1 vowel. Where are the three i's?",
            ),
        ),
    ),
    Question(
        slug="maximum-average-subarray-i", number=643, title="Maximum Average Subarray I",
        difficulty="Easy", topics=("sliding-window",),
        summary="Return the largest average of any contiguous subarray of length k.",
        example="[1,12,-5,-6,50,3], k = 4  →  12.75",
        criterion="Which approach is linear with O(1) extra space?",
        hint="With a fixed length, maximizing the average is the same as maximizing what?",
        choices=(
            Choice(
                "Sliding sum of length k", OPTIMAL, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Add nums[i], subtract nums[i − k], keep the best sum; divide by k at the end.",
                why="With k fixed, the best average is the best sum. Each step updates the sum in O(1).",
            ),
            Choice(
                "Sum each window from scratch", SUBOPTIMAL, time="O(n·k)", space="O(1)", visual="brute",
                detail="For each start, add up k elements.",
                why="Correct, but neighbouring windows share k − 1 elements.",
            ),
            Choice(
                "Average of the k largest", INCORRECT, time="O(n log n)", space="O(1)", visual="sort",
                detail="Sort and average the top k values.",
                why="12 and 50 aren't adjacent. Must the subarray be contiguous?",
            ),
            Choice(
                "Kadane, then divide", INCORRECT, time="O(n)", space="O(1)", visual="dp-1d",
                detail="Find the max-sum subarray of any length and divide by its length.",
                why="The length must be exactly k. Kadane might return [50, 3].",
            ),
        ),
    ),
    Question(
        slug="number-of-sub-arrays-of-size-k-and-average-greater-than-or-equal-to-threshold", number=1343, title="Number of Sub-arrays of Size K and Average Greater than or Equal to Threshold",
        difficulty="Medium", topics=("sliding-window",),
        summary="Count subarrays of length k whose average is at least threshold.",
        example="[2,2,2,2,5,5,5,8], k = 3, threshold = 4  →  3",
        criterion="Which approach is linear with O(1) extra space?",
        hint="Average ≥ threshold is the same as sum ≥ what?",
        choices=(
            Choice(
                "Sliding sum against k·threshold", OPTIMAL, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Maintain the window sum and count windows with sum ≥ k·threshold.",
                why="Multiplying out the average avoids division, and the sum updates in O(1) per step.",
            ),
            Choice(
                "Sum each window from scratch", SUBOPTIMAL, time="O(n·k)", space="O(1)", visual="brute",
                detail="For each start, add up k elements and compare.",
                why="Correct, but each window repeats k − 1 additions.",
            ),
            Choice(
                "Count elements ≥ threshold", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Count positions whose own value reaches the threshold.",
                why="The question is about windows, not elements. [2,5,5] averages 4 with a 2 in it.",
            ),
            Choice(
                "Every element ≥ threshold", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Count windows with no element below threshold.",
                why="[2,5,5] has a 2 but averages exactly 4. Does it count?",
            ),
        ),
    ),
    Question(
        slug="k-radius-subarray-averages", number=2090, title="K Radius Subarray Averages",
        difficulty="Medium", topics=("sliding-window",),
        summary="For each index i, return the integer (floor) average of nums[i − k..i + k], or −1 if that range leaves the array.",
        example="[7,4,3,9,1,8,5,2,6], k = 3  →  [-1,-1,-1,5,4,4,-1,-1,-1]",
        criterion="Which approach is linear?",
        hint="The window always has 2k + 1 elements. What changes when i moves by one?",
        choices=(
            Choice(
                "Sliding sum of width 2k + 1", OPTIMAL, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Keep a 64-bit window sum; once it holds 2k + 1 elements, write sum / (2k + 1) at the centre.",
                why="Each step adds one element and drops one. A 64-bit sum avoids overflow (10⁵ values up to 10⁵).",
            ),
            Choice(
                "Sum each radius from scratch", SUBOPTIMAL, time="O(n·k)", space="O(1)", visual="brute",
                detail="For each centre, add the 2k + 1 elements around it.",
                why="Correct, but with k near n/2 this is quadratic.",
            ),
            Choice(
                "Average what's available near the edges", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Near the ends, average the shorter range instead of writing −1.",
                why="The rules say −1 when fewer than k elements exist on a side. What does index 0 need?",
            ),
            Choice(
                "Average of nums[i..i + 2k]", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Write each window's average at its left end.",
                why="The window is centred on i. Where should 5 appear in the example?",
            ),
        ),
    ),
    Question(
        slug="minimum-recolors-to-get-k-consecutive-black-blocks", number=2379, title="Minimum Recolors to Get K Consecutive Black Blocks",
        difficulty="Easy", topics=("sliding-window",),
        summary="Blocks are 'W' or 'B'. One operation recolours a white block black. Return the fewest operations to get k consecutive black blocks.",
        example="\"WBBWWBBWBW\", k = 7  →  3",
        criterion="Which approach is linear with O(1) extra space?",
        hint="For a fixed window of k blocks, how many recolours does it need?",
        choices=(
            Choice(
                "Fewest whites in any length-k window", OPTIMAL, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Slide a window of k, keeping its white count; return the minimum.",
                why="Making a window all black costs its white count. Updating that count as the window slides is O(1) per step.",
            ),
            Choice(
                "Count whites in each window from scratch", SUBOPTIMAL, time="O(n·k)", space="O(1)", visual="brute",
                detail="For each start, count the W's in the next k blocks.",
                why="Correct, but each window recounts k − 1 blocks.",
            ),
            Choice(
                "k minus the longest black run", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Extend the longest existing black run.",
                why="The longest run is 2, giving 5. Is there a window with only 3 whites?",
            ),
            Choice(
                "Total whites", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Recolour every white block.",
                why="Only one window of k needs to be black. Why touch blocks outside it?",
            ),
        ),
    ),
    Question(
        slug="maximum-sum-of-almost-unique-subarray", number=2841, title="Maximum Sum of Almost Unique Subarray",
        difficulty="Medium", topics=("sliding-window",),
        summary="Among subarrays of length k with at least m distinct values, return the largest sum (0 if none).",
        example="[2,6,7,3,1,7], m = 3, k = 4  →  18",
        criterion="Which approach is linear?",
        hint="How do you know a value has left the window if it appears twice in it?",
        choices=(
            Choice(
                "Slide with a count map and a sum", OPTIMAL, time="O(n)", space="O(k)", visual="sliding-window",
                detail="Increment the entering value's count, decrement the leaving one's and delete it at 0; check map size ≥ m.",
                why="Counts let you tell whether the last copy left. The map's size is the distinct count, updated in O(1) per step.",
            ),
            Choice(
                "Build a set per window", SUBOPTIMAL, time="O(n·k)", space="O(k)", visual="set",
                detail="For each window, collect its values in a fresh set and sum them.",
                why="Correct, but each window rebuilds what the previous one mostly had.",
            ),
            Choice(
                "Slide with a plain set", INCORRECT, time="O(n)", space="O(k)", visual="set",
                detail="Add the entering value, remove the leaving value.",
                why="If the window is [7,3,1,7] and the first 7 leaves, is 7 gone from the window?",
            ),
            Choice(
                "Require all values distinct", INCORRECT, time="O(n)", space="O(k)", visual="sliding-window",
                detail="Only accept windows with k distinct values.",
                why="m can be less than k. [6,7,3,1] works, but would [7,3,1,7] with m = 3?",
            ),
        ),
    ),
    Question(
        slug="maximum-sum-of-distinct-subarrays-with-length-k", number=2461, title="Maximum Sum of Distinct Subarrays With Length K",
        difficulty="Medium", topics=("sliding-window",),
        summary="Return the largest sum of a length-k subarray whose elements are all distinct, or 0 if none exists.",
        example="[1,5,4,2,9,9,9], k = 3  →  15",
        criterion="Which approach is linear?",
        hint="A window of k elements is all distinct exactly when it has how many distinct values?",
        choices=(
            Choice(
                "Slide with a count map and a sum", OPTIMAL, time="O(n)", space="O(k)", visual="sliding-window",
                detail="Maintain counts and the sum; a window qualifies when the map has k keys.",
                why="k keys in a k-element window means no repeats. Each step adjusts one count in, one out.",
            ),
            Choice(
                "Check each window with a set", SUBOPTIMAL, time="O(n·k)", space="O(k)", visual="set",
                detail="For each start, build a set of k elements and compare its size with k.",
                why="Correct, but rebuilds k − 1 shared elements every time.",
            ),
            Choice(
                "k largest distinct values", INCORRECT, time="O(n log n)", space="O(n)", visual="sort",
                detail="Sum the k largest distinct values.",
                why="That's 9 + 5 + 4. Are they contiguous?",
            ),
            Choice(
                "Slide with a plain set", INCORRECT, time="O(n)", space="O(k)", visual="set",
                detail="Add and remove values from a set as the window moves.",
                why="With two 9s in the window, removing the leaving 9 drops the other one too. Is the set still accurate?",
            ),
        ),
    ),
    Question(
        slug="maximum-points-you-can-obtain-from-cards", number=1423, title="Maximum Points You Can Obtain from Cards",
        difficulty="Medium", topics=("sliding-window",),
        summary="Take exactly k cards, each from the left or right end of the row. Return the largest total.",
        example="[1,2,3,4,5,6,1], k = 3  →  12",
        criterion="Which approach does O(k) work?",
        hint="Whatever you take, i cards come from the left and k − i from the right. How does the total change as i drops by one?",
        choices=(
            Choice(
                "Trade a left card for a right card, k times", OPTIMAL, time="O(k)", space="O(1)", visual="sliding-window",
                detail="Start with the first k cards; repeatedly drop the rightmost left card and add the next right card; keep the max.",
                why="The taken cards always form one window that wraps around the end. Moving it one step changes two cards, and there are only k + 1 positions.",
            ),
            Choice(
                "Minimum window of n − k left behind", SUBOPTIMAL, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Total minus the smallest sum of n − k consecutive cards.",
                why="Correct, but it slides over n − k cards. When k is small and n is huge, that's far more work.",
            ),
            Choice(
                "Greedy larger end", INCORRECT, time="O(k)", space="O(1)", visual="greedy",
                detail="Take whichever end card is larger, k times.",
                why="For [2,100,1,1,3], k = 2, greedy takes 3 then 2. What does taking 2 then 100 give?",
            ),
            Choice(
                "k largest cards", INCORRECT, time="O(n log n)", space="O(1)", visual="sort",
                detail="Sum the k largest values.",
                why="Can you reach a card in the middle without taking those before it?",
            ),
        ),
    ),
    Question(
        slug="diet-plan-performance", number=1176, title="Diet Plan Performance",
        difficulty="Easy", topics=("sliding-window",),
        summary="For every k consecutive days, total the calories T: score −1 if T < lower, +1 if T > upper, else 0. Return the total score.",
        example="[1,2,3,4,5], k = 1, lower = 3, upper = 3  →  0",
        criterion="Which approach is linear with O(1) extra space?",
        hint="Every k-day window is scored, so consecutive windows overlap.",
        choices=(
            Choice(
                "Sliding k-day sum", OPTIMAL, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Update the sum by one day in and one out; score each full window.",
                why="Each window shares k − 1 days with the previous one, so the sum updates in O(1).",
            ),
            Choice(
                "Sum each window from scratch", SUBOPTIMAL, time="O(n·k)", space="O(1)", visual="brute",
                detail="For each start day, add k days and score.",
                why="Correct, but repeats k − 1 additions per window.",
            ),
            Choice(
                "Score each day alone", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Compare each day's calories with lower and upper.",
                why="That's only right for k = 1. What about k = 2?",
            ),
            Choice(
                "Non-overlapping blocks", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Score days 0..k−1, then k..2k−1, and so on.",
                why="Every consecutive k-day stretch counts, including those starting at day 1.",
            ),
        ),
    ),
    Question(
        slug="find-k-length-substrings-with-no-repeated-characters", number=1100, title="Find K-Length Substrings With No Repeated Characters",
        difficulty="Medium", topics=("sliding-window",),
        summary="Count the length-k substrings of s (by position) with no repeated characters.",
        example="\"havefunonleetcode\", k = 5  →  6",
        criterion="Which approach is linear?",
        hint="Keep character counts for the window. What single number tells you it has no repeats?",
        choices=(
            Choice(
                "Fixed window with counts and a repeat tally", OPTIMAL, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Track how many characters have count > 1; a window counts when that's 0.",
                why="The tally changes only when a count crosses 1↔2, so each step costs O(1). (For k > 26 the answer is 0.)",
            ),
            Choice(
                "Set per window", SUBOPTIMAL, time="O(n·k)", space="O(k)", visual="set",
                detail="For each start, insert k characters into a set and compare sizes.",
                why="Correct, but rebuilds the window each time.",
            ),
            Choice(
                "Count distinct substrings", INCORRECT, time="O(n·k)", space="O(n·k)", visual="set",
                detail="Collect qualifying substrings in a set and return its size.",
                why="The count is by position. If the same substring appears twice, how many does the task count?",
            ),
            Choice(
                "First and last characters differ", INCORRECT, time="O(n)", space="O(1)", visual="two-pointers",
                detail="Count windows whose ends are different.",
                why="\"abca\" has equal ends; \"abcb\" doesn't. Does either have repeats?",
            ),
        ),
    ),
    Question(
        slug="distinct-numbers-in-each-subarray", number=1852, title="Distinct Numbers in Each Subarray",
        difficulty="Medium", topics=("sliding-window",),
        summary="Return an array whose i-th value is the number of distinct values in nums[i..i + k − 1].",
        example="[1,2,3,2,2,1,3], k = 3  →  [3,2,2,2,3]",
        criterion="Which approach is linear?",
        hint="When a value leaves the window, is it really gone?",
        choices=(
            Choice(
                "Slide with a count map", OPTIMAL, time="O(n)", space="O(k)", visual="sliding-window",
                detail="Increment the entering value, decrement the leaving one and delete it at 0; record the map size.",
                why="Counts know whether another copy remains. The map size is the distinct count, maintained in O(1).",
            ),
            Choice(
                "Set per window", SUBOPTIMAL, time="O(n·k)", space="O(k)", visual="set",
                detail="Build a fresh set for each window.",
                why="Correct, but repeats k − 1 insertions per window.",
            ),
            Choice(
                "Slide with a plain set", INCORRECT, time="O(n)", space="O(k)", visual="set",
                detail="Add the entering value, remove the leaving one.",
                why="Window [2,3,2] → the first 2 leaves. Is 2 still present?",
            ),
            Choice(
                "Count value changes", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Count positions where nums[j] ≠ nums[j − 1] inside the window, plus 1.",
                why="[1,2,1] has two changes, so 3. How many distinct values does it hold?",
            ),
        ),
    ),
    Question(
        slug="minimum-swaps-to-group-all-1s-together", number=1151, title="Minimum Swaps to Group All 1's Together",
        difficulty="Medium", topics=("sliding-window",),
        summary="A binary array can swap any two elements. Return the fewest swaps that put all 1s in one contiguous block.",
        example="[1,0,1,0,1]  →  1",
        criterion="Which approach is linear with O(1) extra space?",
        hint="If there are c ones, the final block has length c. Which spot needs the fewest swaps?",
        choices=(
            Choice(
                "Window of length c with the most 1s", OPTIMAL, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Count c, slide a window of length c, and return c − (most 1s in a window).",
                why="Each 0 inside the chosen block must be swapped with a 1 outside it, one swap each. Fewest 0s inside means fewest swaps.",
            ),
            Choice(
                "Count each window from scratch", SUBOPTIMAL, time="O(n·c)", space="O(1)", visual="brute",
                detail="For each start, count the 1s in the next c elements.",
                why="Correct, but repeats c − 1 positions per window.",
            ),
            Choice(
                "Zeros between the first and last 1", INCORRECT, time="O(n)", space="O(1)", visual="two-pointers",
                detail="Count the 0s inside the span of 1s.",
                why="That gives 2. Can one swap fix [1,0,1,0,1]?",
            ),
            Choice(
                "Bubble the 1s left", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Count adjacent swaps to move every 1 to the front.",
                why="Swaps can be between any two positions, and the block can be anywhere.",
            ),
        ),
    ),
    Question(
        slug="number-of-unique-flavors-after-sharing-k-candies", number=2107, title="Number of Unique Flavors After Sharing K Candies",
        difficulty="Medium", topics=("sliding-window",),
        summary="You must give away k consecutive candies. Return the most distinct flavors you can keep.",
        example="[1,2,2,3,4,3], k = 3  →  3",
        criterion="Which approach is linear?",
        hint="Start with counts of everything you own. What does giving away a window do to those counts?",
        choices=(
            Choice(
                "Slide the given-away window over full counts", OPTIMAL, time="O(n)", space="O(n)", visual="sliding-window",
                detail="Begin with counts of all candies; moving the window removes one entering candy from your stock and returns one leaving candy; track distinct flavors left.",
                why="What you keep is everything outside the window. Each move changes two counts, so the number of flavors with count > 0 updates in O(1).",
            ),
            Choice(
                "Recount the kept candies per window", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="brute",
                detail="For each window, count flavors outside it from scratch.",
                why="Correct, but each window rescans the whole array.",
            ),
            Choice(
                "Distinct flavors inside the window", INCORRECT, time="O(n)", space="O(k)", visual="sliding-window",
                detail="Maximize the distinct flavors given away.",
                why="You keep what's outside. Should you give away variety?",
            ),
            Choice(
                "Give away the most common flavor", INCORRECT, time="O(n)", space="O(n)", visual="counting",
                detail="Pick k candies of the most frequent flavor.",
                why="The k candies must be consecutive. Are the copies of one flavor next to each other?",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §1.2 fixed-length window, further practice
    Question(
        slug="grumpy-bookstore-owner", number=1052, title="Grumpy Bookstore Owner",
        difficulty="Medium", topics=("sliding-window",),
        summary="Customers arrive each minute; in grumpy minutes they leave unsatisfied. Once, the owner can stay calm for minutes consecutive minutes. Return the most satisfied customers.",
        example="customers = [1,0,1,2,1,1,7,5], grumpy = [0,1,0,1,0,1,0,1], minutes = 3  →  16",
        criterion="Which approach is linear with O(1) extra space?",
        hint="Split the answer into customers already satisfied and the extra the calm window rescues.",
        choices=(
            Choice(
                "Base satisfied plus best rescued window", OPTIMAL, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Sum customers in non-grumpy minutes; slide a window summing customers in grumpy minutes only; add the max.",
                why="The calm window only matters where the owner was grumpy. Counting just those customers turns it into a fixed-window max.",
            ),
            Choice(
                "Recompute satisfaction per window", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="For each window, recount every minute with the window applied.",
                why="Correct, but every placement rescans all n minutes.",
            ),
            Choice(
                "Window with the most customers", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Place the calm window where the most customers arrive.",
                why="Customers in calm minutes were satisfied anyway. Does the window gain anything there?",
            ),
            Choice(
                "Calm during the busiest grumpy minutes", INCORRECT, time="O(n log n)", space="O(n)", visual="sort",
                detail="Pick the grumpy minutes with the most customers, up to minutes of them.",
                why="The calm stretch must be consecutive.",
            ),
        ),
    ),
    Question(
        slug="minimum-discards-to-balance-inventory", number=3679, title="Minimum Discards to Balance Inventory",
        difficulty="Medium", topics=("sliding-window",),
        summary="Day i brings an item of type arrivals[i]; you keep or discard it that day. In every window of w days, each type may appear at most m times among kept items. Return the fewest discards.",
        example="arrivals = [1,2,3,3,3,4], w = 3, m = 2  →  1",
        criterion="Which approach is linear?",
        hint="Keeping an item whenever the rule allows is optimal. What do you need to know about the last w days?",
        choices=(
            Choice(
                "Keep greedily, slide counts of kept items", OPTIMAL, time="O(n)", space="O(n)", visual="sliding-window",
                detail="Before day i, drop day i − w from the counts if it was kept; keep today's item if its count is below m, else discard.",
                why="Keeping an item never hurts later days more than discarding it would help. Counting only kept items in the last w days makes the check O(1).",
            ),
            Choice(
                "Recount kept items in the window each day", SUBOPTIMAL, time="O(n·w)", space="O(n)", visual="brute",
                detail="For each day, scan the previous w − 1 days for kept items of the same type.",
                why="Correct, but every day rescans up to w days.",
            ),
            Choice(
                "Count every arrival in the window", INCORRECT, time="O(n)", space="O(n)", visual="sliding-window",
                detail="Include discarded items in the window counts.",
                why="A discarded item isn't in the inventory. Should it block a later arrival?",
            ),
            Choice(
                "Keep at most m of each type overall", INCORRECT, time="O(n)", space="O(n)", visual="counting",
                detail="Discard every arrival past the m-th of its type.",
                why="The limit is per w-day window. In example 1, three 1s are all kept.",
            ),
        ),
    ),
    Question(
        slug="defuse-the-bomb", number=1652, title="Defuse the Bomb",
        difficulty="Easy", topics=("sliding-window",),
        summary="In a circular array, replace each element with the sum of the next k elements if k > 0, the previous |k| if k < 0, or 0 if k = 0.",
        example="[5,7,1,4], k = 3  →  [12,10,16,13]",
        criterion="Which approach is linear?",
        hint="As i moves right by one, which element enters the summed range and which leaves?",
        choices=(
            Choice(
                "Circular sliding window", OPTIMAL, time="O(n)", space="O(n)", visual="sliding-window",
                detail="Sum the first range; for each i, add the element entering and subtract the one leaving, indexing mod n.",
                why="Both ranges keep a fixed width |k| and shift by one as i does, so each update is O(1).",
            ),
            Choice(
                "Sum each range from scratch", SUBOPTIMAL, time="O(n·|k|)", space="O(n)", visual="brute",
                detail="For each i, add |k| elements mod n.",
                why="Correct, but neighbours share |k| − 1 elements.",
            ),
            Choice(
                "Ignore the wrap", INCORRECT, time="O(n)", space="O(n)", visual="sliding-window",
                detail="Sum only the elements that exist without going past the ends.",
                why="For the last element, the next 3 are 5, 7, 1. Where do they come from?",
            ),
            Choice(
                "Next |k| even when k < 0", INCORRECT, time="O(n)", space="O(n)", visual="sliding-window",
                detail="Always sum forward.",
                why="k = −2 means the two before. Does direction matter?",
            ),
        ),
    ),
    Question(
        slug="count-rotations-with-exactly-k-equal-adjacent-pairs", number=4043, title="Count Rotations With Exactly K Equal Adjacent Pairs",
        difficulty="Easy", topics=("sliding-window",),
        summary="A rotation's score is the number of adjacent equal character pairs in it. Count the rotations of s (there are n) whose score equals k.",
        example="\"aab\", k = 1  →  2",
        criterion="Which approach is linear?",
        hint="Each rotation is a length-n window of s + s. How many adjacent pairs change when the window slides by one?",
        choices=(
            Choice(
                "Length-n window over s + s", OPTIMAL, time="O(n)", space="O(n)", visual="sliding-window",
                detail="Count equal pairs in the first window; each slide drops the pair leaving at the front and adds the pair entering at the back.",
                why="Neighbouring rotations share n − 2 of their n − 1 pairs, so the score updates in O(1).",
            ),
            Choice(
                "Build and score each rotation", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="brute",
                detail="Form every rotation and count its pairs.",
                why="Correct, but each rotation recounts pairs the previous one already knew.",
            ),
            Choice(
                "Score s once", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Assume every rotation has the same score as s.",
                why="\"aab\" scores 1, \"aba\" scores 0. Are they all the same?",
            ),
            Choice(
                "Count the cyclic pairs", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Include the pair between the last and first characters for every rotation.",
                why="A rotation is a straight string. Is its last character next to its first?",
            ),
        ),
    ),
    Question(
        slug="count-good-cyclic-rotations", number=4044, title="Count Good Cyclic Rotations",
        difficulty="Medium", topics=("sliding-window",),
        summary="nums has even length n. A rotation is good if the sum of its first n/2 elements is strictly greater than the sum of its last n/2. Count good rotations.",
        example="[1,2,3,4,5,6]  →  3",
        criterion="Which approach is linear?",
        hint="If you know the total and the first half's sum, what's the second half's sum?",
        choices=(
            Choice(
                "Circular window of length n/2", OPTIMAL, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Slide a window of n/2 around the circle; a rotation is good when 2·window > total.",
                why="The first half of each rotation is a circular window, and the second half is total minus it. Each slide is O(1).",
            ),
            Choice(
                "Sum both halves per rotation", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="For each rotation, add up both halves.",
                why="Correct, but every rotation re-adds n numbers.",
            ),
            Choice(
                "Use ≥ instead of >", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Count rotations where the first half is at least the second.",
                why="Example 2 has equal halves everywhere and answers 0. What would this give?",
            ),
            Choice(
                "Compare pairs nums[i] and nums[i + n/2]", INCORRECT, time="O(n)", space="O(1)", visual="two-pointers",
                detail="Count i where nums[i] > nums[i + n/2].",
                why="The rule compares sums of halves, not single pairs.",
            ),
        ),
    ),
    Question(
        slug="best-time-to-buy-and-sell-stock-using-strategy", number=3652, title="Best Time to Buy and Sell Stock using Strategy",
        difficulty="Medium", topics=("sliding-window",),
        summary="Profit is Σ strategy[i]·prices[i] with strategy values −1, 0, 1. At most once, pick k (even) consecutive days and set the first half to 0 and the second half to 1. Return the best profit.",
        example="prices = [4,2,8], strategy = [-1,0,1], k = 2  →  10",
        criterion="Which approach is linear?",
        hint="How much does modifying a window change the profit, in terms of sums over that window?",
        choices=(
            Choice(
                "Base profit plus the best window gain", OPTIMAL, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Gain = Σ prices over the window's second half − Σ strategy·price over the window; slide both sums; answer = base + max(0, best gain).",
                why="Outside the window nothing changes. Inside, the old terms are removed and the second half's prices are added, and both sums slide in O(1).",
            ),
            Choice(
                "Recompute profit per window", SUBOPTIMAL, time="O(n·k)", space="O(1)", visual="brute",
                detail="For each window, recompute its contribution from scratch.",
                why="Correct, but neighbouring windows share almost everything.",
            ),
            Choice(
                "Always modify once", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Return base + best gain even when that gain is negative.",
                why="In example 2, every modification lowers the profit. Is the change required?",
            ),
            Choice(
                "Add sold prices only", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Gain = Σ prices over the second half, without removing the window's old terms.",
                why="The old strategy inside the window is overwritten. What happens to an old sell there?",
            ),
        ),
    ),
    Question(
        slug="permutation-in-string", number=567, title="Permutation in String",
        difficulty="Medium", topics=("sliding-window",),
        summary="Return whether s2 contains a permutation of s1 as a substring.",
        example="s1 = \"ab\", s2 = \"eidbaooo\"  →  true",
        criterion="Which approach is linear in |s2|?",
        hint="A permutation is the same letter counts. Which window length must you check?",
        choices=(
            Choice(
                "Fixed window with counts and a match tally", OPTIMAL, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Slide a window of |s1| over s2, adjusting 26 counts and how many letters match s1's counts.",
                why="Each slide changes two counts, which can change the match tally by at most two. All 26 matching means a permutation.",
            ),
            Choice(
                "Sort each window", SUBOPTIMAL, time="O(n·m log m)", space="O(m)", visual="sort",
                detail="Sort every length-|s1| substring and compare with sorted s1.",
                why="Correct, but each window is sorted from scratch.",
            ),
            Choice(
                "All letters appear in s2", INCORRECT, time="O(n + m)", space="O(1)", visual="counting",
                detail="Check s2 has at least the letter counts of s1.",
                why="For \"ab\" and \"aob\", the letters exist but not together.",
            ),
            Choice(
                "s1 or its reverse is a substring", INCORRECT, time="O(n·m)", space="O(1)", visual="brute",
                detail="Search for s1 and reversed s1.",
                why="For s1 = \"abc\", is \"bca\" one of those two?",
            ),
        ),
    ),
    Question(
        slug="find-all-anagrams-in-a-string", number=438, title="Find All Anagrams in a String",
        difficulty="Medium", topics=("sliding-window",),
        summary="Return every start index in s where an anagram of p begins.",
        example="s = \"cbaebabacd\", p = \"abc\"  →  [0, 6]",
        criterion="Which approach is linear in |s|?",
        hint="All anagrams of p have length |p| and the same letter counts.",
        choices=(
            Choice(
                "Fixed window with letter counts", OPTIMAL, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Slide a window of |p|, updating counts and the number of letters that still differ; record starts where none differ.",
                why="Each slide changes two counts, so the 'differing letters' tally updates in O(1).",
            ),
            Choice(
                "Sort each window", SUBOPTIMAL, time="O(n·m log m)", space="O(m)", visual="sort",
                detail="Sort every length-|p| substring and compare with sorted p.",
                why="Correct, but sorts m letters per window.",
            ),
            Choice(
                "Compare character-code sums", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="A window matches if its letter codes add up to p's.",
                why="\"ad\" and \"bc\" have the same sum. Are they anagrams?",
            ),
            Choice(
                "Search for sorted p", INCORRECT, time="O(n·m)", space="O(m)", visual="brute",
                detail="Find occurrences of p's letters in sorted order.",
                why="\"cba\" at index 0 is an anagram. Does it contain \"abc\" literally?",
            ),
        ),
    ),
    Question(
        slug="substring-with-concatenation-of-all-words", number=30, title="Substring with Concatenation of All Words",
        difficulty="Hard", topics=("sliding-window",),
        summary="All words have the same length L. Return every start index in s of a substring that is all the words concatenated in some order, each used exactly as often as listed.",
        example="s = \"barfoothefoobarman\", words = [\"foo\",\"bar\"]  →  [0, 9]",
        criterion="Which approach does O(n·L) work?",
        hint="Read s in L-length chunks. How many different chunk alignments are there?",
        choices=(
            Choice(
                "Word-chunk window per offset", OPTIMAL, time="O(n·L)", space="O(m·L)", visual="sliding-window",
                detail="For each offset 0..L−1, slide a window of chunks with word counts, shrinking when a chunk is over-used or unknown.",
                why="Within one offset, each chunk enters and leaves the window once. L offsets cover every alignment.",
            ),
            Choice(
                "Check each start from scratch", SUBOPTIMAL, time="O(n·m·L)", space="O(m·L)", visual="brute",
                detail="For every index, split the next m·L characters into chunks and compare counts.",
                why="Correct, but starts that share chunks redo all the comparisons.",
            ),
            Choice(
                "Anagram of the joined words", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Look for windows with the same letters as the words combined.",
                why="\"rabfoo\" has the right letters. Is it made of whole words?",
            ),
            Choice(
                "Use a set of words", INCORRECT, time="O(n·L)", space="O(m·L)", visual="set",
                detail="Ignore how many times each word is listed.",
                why="With words [\"a\",\"a\"], must the window contain two a's?",
            ),
        ),
    ),
    Question(
        slug="sum-of-weighted-modes-in-subarrays", number=3672, title="Sum of Weighted Modes in Subarrays",
        difficulty="Medium", topics=("sliding-window",),
        summary="For each window of length k, take its mode (most frequent value, smallest on ties) times its frequency. Return the sum over all windows.",
        example="[1,2,2,3], k = 3  →  8",
        criterion="Which approach finds each window's mode without rescanning it?",
        hint="When a value leaves, its frequency drops. What structure still gives you the top (frequency, value) quickly?",
        choices=(
            Choice(
                "Counts plus an ordered set of (−freq, value)", OPTIMAL, time="O(n log n)", space="O(n)", visual="heap",
                detail="On each slide, update two counts and their entries; read the mode from the top.",
                why="Only two values change frequency per slide. Re-inserting them keeps the order correct, and the top gives the mode with the smallest value on ties.",
            ),
            Choice(
                "Recount every window", SUBOPTIMAL, time="O(n·k)", space="O(k)", visual="brute",
                detail="Build counts for each window and scan for the mode.",
                why="Correct, but each window redoes k − 1 counts.",
            ),
            Choice(
                "Keep a running best that only improves", INCORRECT, time="O(n)", space="O(n)", visual="hashmap",
                detail="Update the mode when a count beats it, never when counts drop.",
                why="When copies of the mode slide out, its frequency falls. Is it still the mode?",
            ),
            Choice(
                "Break ties by the larger value", INCORRECT, time="O(n log n)", space="O(n)", visual="heap",
                detail="Same structure, but prefer the larger value on equal frequency.",
                why="The rules break ties toward the smaller value.",
            ),
        ),
    ),
    Question(
        slug="number-of-equal-count-substrings", number=2067, title="Number of Equal Count Substrings",
        difficulty="Medium", topics=("sliding-window",),
        summary="A substring is equal-count if every letter in it appears exactly count times. Count such substrings of s.",
        example="s = \"aaabcbbcc\", count = 3  →  3",
        criterion="Which approach is linear (times the alphabet)?",
        hint="If a substring has u distinct letters, how long must it be?",
        choices=(
            Choice(
                "One fixed window per distinct-letter count", OPTIMAL, time="O(26·n)", space="O(1)", visual="sliding-window",
                detail="For u = 1..26, slide a window of length u·count and track how many letters have exactly count.",
                why="The length is forced by u, so each u is a fixed-length window. A tally of letters at exactly count updates in O(1).",
            ),
            Choice(
                "Check every substring", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="Extend from each start, updating counts and testing.",
                why="Correct, but only 26 lengths can possibly work.",
            ),
            Choice(
                "Windows of length count only", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Look for a single letter repeated count times.",
                why="\"bcbbcc\" works with two letters. What's its length?",
            ),
            Choice(
                "Every letter a–z exactly count times", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Require all 26 letters to appear count times.",
                why="Letters that don't appear are fine. Does \"aaa\" qualify?",
            ),
        ),
    ),
    Question(
        slug="maximum-frequency-score-of-a-subarray", number=2524, title="Maximum Frequency Score of a Subarray",
        difficulty="Hard", topics=("sliding-window",),
        summary="A window's frequency score is Σ x^freq(x) over its distinct values, mod 10⁹ + 7. Return the largest score among windows of length k.",
        example="[1,1,1,2,1,2], k = 3  →  5",
        criterion="Which approach updates the score in O(log k) per slide?",
        hint="When x's frequency goes from f to f + 1, its term goes from x^f to what?",
        choices=(
            Choice(
                "Slide with counts, adjust one term each way", OPTIMAL, time="O(n log k)", space="O(k)", visual="sliding-window",
                detail="On entry, replace x^f by x^(f+1); on exit, replace x^f by x^(f−1) (fast power mod p).",
                why="Only two values change per slide, and each change swaps one power term. Fast exponentiation makes each swap O(log k).",
            ),
            Choice(
                "Recompute each window's score", SUBOPTIMAL, time="O(n·k)", space="O(k)", visual="brute",
                detail="Count the window and add up powers from scratch.",
                why="Correct, but redoes k − 1 elements each slide.",
            ),
            Choice(
                "Sum of x × freq", INCORRECT, time="O(n)", space="O(k)", visual="sliding-window",
                detail="Weight each value by its count.",
                why="For [2,1,2] that gives 5, which matches, but [2,2,2] gives 6 instead of 8. Which is the score?",
            ),
            Choice(
                "Compare scores before taking the mod", INCORRECT, time="O(n·k)", space="O(k)", visual="math",
                detail="Track the true (huge) scores and reduce only the winner.",
                why="The task compares the modded values. Can a bigger true score have a smaller remainder?",
            ),
        ),
    ),
    Question(
        slug="find-all-k-distant-indices-in-an-array", number=2200, title="Find All K-Distant Indices in an Array",
        difficulty="Easy", topics=("sliding-window",),
        summary="Return, sorted, every index i that is within distance k of some index j with nums[j] = key.",
        example="[3,4,9,1,3,9,5], key = 9, k = 1  →  [1,2,3,4,5,6]",
        criterion="Which approach is linear?",
        hint="Each key covers the range [j − k, j + k]. How do you emit the union without repeats?",
        choices=(
            Choice(
                "Extend coverage from each key", OPTIMAL, time="O(n)", space="O(1)", visual="two-pointers",
                detail="For each key at j, emit indices from max(next unemitted, j − k) to min(n − 1, j + k).",
                why="Keys are seen left to right, so remembering the next index not yet emitted keeps every index emitted once.",
            ),
            Choice(
                "Scan the radius around each index", SUBOPTIMAL, time="O(n·k)", space="O(1)", visual="brute",
                detail="For each i, check nums[i − k..i + k] for the key.",
                why="Correct, but overlapping ranges are rescanned.",
            ),
            Choice(
                "Indices of the key", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Return the positions where nums[j] = key.",
                why="Index 1 isn't 9 but is next to one. Does it count?",
            ),
            Choice(
                "Distance to the nearest key on the left", INCORRECT, time="O(n)", space="O(1)", visual="two-pointers",
                detail="Include i if the last key before it is within k.",
                why="Index 1 is just left of a key. Is it included?",
            ),
        ),
    ),
    Question(
        slug="check-if-a-string-contains-all-binary-codes-of-size-k", number=1461, title="Check If a String Contains All Binary Codes of Size K",
        difficulty="Medium", topics=("sliding-window",),
        summary="Return whether every binary string of length k appears as a substring of s.",
        example="\"00110110\", k = 2  →  true",
        criterion="Which approach is linear in |s|?",
        hint="A length-k window of bits is a number below 2ᵏ. How does it change when you slide?",
        choices=(
            Choice(
                "Rolling k-bit integer with a seen table", OPTIMAL, time="O(n)", space="O(2ᵏ)", visual="bits",
                detail="code = ((code << 1) | bit) & (2ᵏ − 1); mark it; succeed when 2ᵏ codes are marked.",
                why="Shift-and-mask updates the window value in O(1), and a bit array of 2ᵏ flags records codes without hashing strings.",
            ),
            Choice(
                "Set of substrings", SUBOPTIMAL, time="O(n·k)", space="O(n·k)", visual="set",
                detail="Add every length-k substring to a set and compare its size with 2ᵏ.",
                why="Correct, but slicing and hashing each substring costs O(k).",
            ),
            Choice(
                "Enough windows", INCORRECT, time="O(1)", space="O(1)", visual="math",
                detail="True if n − k + 1 ≥ 2ᵏ.",
                why="\"0000\" has 3 windows of length 2. Does it contain \"01\"?",
            ),
            Choice(
                "Search each code separately", INCORRECT, time="O(2ᵏ)", space="O(1)", visual="brute",
                detail="For each code, check the counts of 0s and 1s in s.",
                why="Counts don't say where the bits are. Does \"0011\" contain \"10\"?",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §2.1 variable window: longest
    Question(
        slug="longest-substring-without-repeating-characters", number=3, title="Longest Substring Without Repeating Characters",
        difficulty="Medium", topics=("sliding-window",),
        summary="Return the length of the longest substring of s with no repeated character.",
        example="\"abcabcbb\"  →  3",
        criterion="Which approach is linear?",
        hint="When the new character is already in the window, where must the left edge move?",
        choices=(
            Choice(
                "Grow right, shrink left past the repeat", OPTIMAL, time="O(n)", space="O(Σ)", visual="sliding-window",
                detail="Keep counts (or last positions); while s[r] repeats, move left forward; track r − l + 1.",
                why="If a window has a repeat, every wider window does too, so the left edge never moves back. Each index enters and leaves once.",
            ),
            Choice(
                "Extend from every start", SUBOPTIMAL, time="O(n·Σ)", space="O(Σ)", visual="brute",
                detail="From each start, extend until a repeat appears.",
                why="Correct, but each start rescans characters the previous start already checked.",
            ),
            Choice(
                "Count distinct characters", INCORRECT, time="O(n)", space="O(Σ)", visual="set",
                detail="Return the number of different characters in s.",
                why="\"pwwkew\" has 4 distinct letters, but the answer is 3 (\"wke\"). Must the letters be together?",
            ),
            Choice(
                "Restart at a repeat", INCORRECT, time="O(n)", space="O(Σ)", visual="greedy",
                detail="When s[r] repeats, start a new window at r.",
                why="For \"dvdf\", restarting at the second d loses \"vdf\". Where should the window really start?",
            ),
        ),
    ),
    Question(
        slug="maximum-length-substring-with-two-occurrences", number=3090, title="Maximum Length Substring With Two Occurrences",
        difficulty="Easy", topics=("sliding-window",),
        summary="Return the length of the longest substring in which every character appears at most twice.",
        example="\"bcbbbcba\"  →  4",
        criterion="Which approach is linear?",
        hint="Only the character just added can break the rule. How far must the left edge move?",
        choices=(
            Choice(
                "Grow right, shrink while a count exceeds 2", OPTIMAL, time="O(n)", space="O(Σ)", visual="sliding-window",
                detail="Increment count[s[r]]; while it's 3, decrement count[s[l]] and advance l.",
                why="A valid window stays valid when shrunk, so the left edge only moves forward. Each index enters and leaves once.",
            ),
            Choice(
                "Check every substring", SUBOPTIMAL, time="O(n²)", space="O(Σ)", visual="brute",
                detail="From each start, extend with counts until a third copy appears.",
                why="Correct, but starts close together redo the same counting.",
            ),
            Choice(
                "Restart at the third copy", INCORRECT, time="O(n)", space="O(Σ)", visual="greedy",
                detail="Clear the window when a character appears a third time.",
                why="In \"bcbbbcba\", restarting at the third b drops letters that could stay. What's the longest window ending later?",
            ),
            Choice(
                "Sum of min(count, 2) over s", INCORRECT, time="O(n)", space="O(Σ)", visual="counting",
                detail="Each letter contributes at most two characters.",
                why="That ignores where the letters are. Must the substring be contiguous?",
            ),
        ),
    ),
    Question(
        slug="longest-subarray-of-1s-after-deleting-one-element", number=1493, title="Longest Subarray of 1's After Deleting One Element",
        difficulty="Medium", topics=("sliding-window",),
        summary="Delete exactly one element from a binary array, then return the length of the longest run of 1s.",
        example="[0,1,1,1,0,1,1,0,1]  →  5",
        criterion="Which approach is linear with O(1) extra space?",
        hint="Which windows become all 1s after deleting one element?",
        choices=(
            Choice(
                "Longest window with at most one 0, minus 1", OPTIMAL, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Shrink while the window holds two 0s; answer = max(r − l + 1) − 1.",
                why="Deleting one element from a window with at most one 0 leaves all 1s. The deletion is mandatory, so subtract 1 even with no 0.",
            ),
            Choice(
                "Try deleting each element", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="For each index, find the longest 1-run with it removed.",
                why="Correct, but each deletion rescans the whole array.",
            ),
            Choice(
                "Skip the deletion when all are 1", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Return n if the array has no 0.",
                why="For [1,1,1], you must still delete one. What's left?",
            ),
            Choice(
                "Longest run plus one", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Find the longest run of 1s and add 1 for the deleted 0.",
                why="Deleting a 0 joins two runs. In the example, which two runs join?",
            ),
        ),
    ),
    Question(
        slug="minimum-removals-to-balance-array", number=3634, title="Minimum Removals to Balance Array",
        difficulty="Medium", topics=("sliding-window",),
        summary="An array is balanced if its maximum is at most k times its minimum. Return the fewest elements to remove (leaving at least one) to make nums balanced.",
        example="[1,6,2,9], k = 3  →  2",
        criterion="Which approach is O(n log n)?",
        hint="After sorting, the kept elements can be taken as a contiguous block. Why?",
        choices=(
            Choice(
                "Sort, then longest window with max ≤ k·min", OPTIMAL, time="O(n log n)", space="O(1)", visual="sliding-window",
                detail="Sort; for each right end, advance left while a[r] > k·a[l] (64-bit); answer = n − longest.",
                why="Once a min and max are chosen, keeping everything between them is free. In sorted order the left edge only moves forward.",
            ),
            Choice(
                "Sort, then scan right from each min", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="For each i, walk j forward while a[j] ≤ k·a[i].",
                why="Correct, but each start rescans elements the previous one already passed.",
            ),
            Choice(
                "Window without sorting", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Run the window on the original order.",
                why="Removal can take any elements. In [1,6,2,9], are 6 and 2 adjacent once 1 and 9 are gone?",
            ),
            Choice(
                "Peel off the worse end", INCORRECT, time="O(n log n)", space="O(1)", visual="greedy",
                detail="Sort; while unbalanced, remove whichever end is farther from the median.",
                why="A local rule can remove the wrong end first. Which block is the longest valid one?",
            ),
        ),
    ),
    Question(
        slug="get-equal-substrings-within-budget", number=1208, title="Get Equal Substrings Within Budget",
        difficulty="Medium", topics=("sliding-window",),
        summary="Changing s[i] to t[i] costs |s[i] − t[i]|. Return the longest substring length you can make equal within maxCost.",
        example="s = \"abcd\", t = \"bcdf\", maxCost = 3  →  3",
        criterion="Which approach is linear with O(1) extra space?",
        hint="Costs are non-negative. What happens to a window's cost when you shrink it?",
        choices=(
            Choice(
                "Longest window with cost sum ≤ maxCost", OPTIMAL, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Add cost[r]; while the sum exceeds maxCost, subtract cost[l] and advance l.",
                why="With non-negative costs, shrinking never raises the sum, so the left edge only moves forward.",
            ),
            Choice(
                "Prefix sums, check every window", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="prefix",
                detail="Compute prefix costs and test every (l, r).",
                why="Correct, but most windows are obviously too long or too short.",
            ),
            Choice(
                "Cheapest positions first", INCORRECT, time="O(n log n)", space="O(n)", visual="greedy",
                detail="Sort costs and take as many as fit.",
                why="The changed positions must form one substring.",
            ),
            Choice(
                "Restart when over budget", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Reset the window to empty when the cost passes maxCost.",
                why="Dropping only the leftmost cost might be enough. Why throw away the rest?",
            ),
        ),
    ),
    Question(
        slug="fruit-into-baskets", number=904, title="Fruit Into Baskets",
        difficulty="Medium", topics=("sliding-window",),
        summary="Walking right from any tree, you pick one fruit per tree into two baskets, each holding one type. Return the most fruit you can pick: the longest subarray with at most 2 distinct values.",
        example="[1,2,3,2,2]  →  4",
        criterion="Which approach is linear?",
        hint="When a third type enters, which fruit has to leave the window?",
        choices=(
            Choice(
                "Window with at most two types", OPTIMAL, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Count types in the window; while there are 3, drop from the left.",
                why="A window with ≤ 2 types stays valid when shrunk, so the left edge only moves forward.",
            ),
            Choice(
                "Extend from every start", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="From each tree, walk right until a third type appears.",
                why="Correct, but overlapping walks redo the same trees.",
            ),
            Choice(
                "Two most common types", INCORRECT, time="O(n)", space="O(n)", visual="counting",
                detail="Add up the counts of the two most frequent fruits.",
                why="The fruit must come from consecutive trees. Do common types sit together?",
            ),
            Choice(
                "Longest run of one type, doubled", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Find the longest single-type run and add the run next to it.",
                why="[1,2,1,2,1] alternates. How long are its runs, and what's the answer?",
            ),
        ),
    ),
    Question(
        slug="maximum-erasure-value", number=1695, title="Maximum Erasure Value",
        difficulty="Medium", topics=("sliding-window",),
        summary="Erase one subarray of distinct elements and score its sum. Return the best score.",
        example="[4,2,4,5,6]  →  17",
        criterion="Which approach is linear?",
        hint="This is the longest-without-repeats window, but you keep a sum instead of a length.",
        choices=(
            Choice(
                "Distinct window with a running sum", OPTIMAL, time="O(n)", space="O(n)", visual="sliding-window",
                detail="Add nums[r]; while it repeats, remove nums[l] from the set and the sum; track the max sum.",
                why="Values are positive, so the best window ending at r is the longest valid one. The left edge only moves forward.",
            ),
            Choice(
                "Extend from every start", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="brute",
                detail="From each index, extend while values are new, summing as you go.",
                why="Correct, but overlapping scans repeat work.",
            ),
            Choice(
                "Sum of distinct values", INCORRECT, time="O(n)", space="O(n)", visual="set",
                detail="Add each different value once.",
                why="For [1,2,1,1,3], that gives 6. Which subarray of distinct elements reaches 6?",
            ),
            Choice(
                "Kadane's maximum subarray", INCORRECT, time="O(n)", space="O(1)", visual="dp-1d",
                detail="Take the largest-sum subarray.",
                why="With all positive values Kadane takes everything, repeats included. Is [4,2,4] allowed?",
            ),
        ),
    ),
    Question(
        slug="length-of-longest-subarray-with-at-most-k-frequency", number=2958, title="Length of Longest Subarray With at Most K Frequency",
        difficulty="Medium", topics=("sliding-window",),
        summary="Return the length of the longest subarray in which no value appears more than k times.",
        example="[1,2,3,1,2,3,1,2], k = 2  →  6",
        criterion="Which approach is linear?",
        hint="Only the newly added value can exceed k. How far must the left edge go?",
        choices=(
            Choice(
                "Grow right, shrink while count[x] > k", OPTIMAL, time="O(n)", space="O(n)", visual="sliding-window",
                detail="After adding x = nums[r], drop from the left until count[x] ≤ k.",
                why="A good window stays good when shrunk, so the left edge only advances. Each element enters and leaves once.",
            ),
            Choice(
                "Extend from every start", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="brute",
                detail="From each start, extend until some count exceeds k.",
                why="Correct, but repeats the counting for every start.",
            ),
            Choice(
                "Restart when a count exceeds k", INCORRECT, time="O(n)", space="O(n)", visual="greedy",
                detail="Begin a new window at r when nums[r] is over the limit.",
                why="Dropping just the first copy of that value would fix it. How much does restarting lose?",
            ),
            Choice(
                "Sum of min(count, k)", INCORRECT, time="O(n)", space="O(n)", visual="counting",
                detail="Each value contributes at most k elements.",
                why="Must the elements be contiguous?",
            ),
        ),
    ),
    Question(
        slug="maximize-the-confusion-of-an-exam", number=2024, title="Maximize the Confusion of an Exam",
        difficulty="Medium", topics=("sliding-window",),
        summary="Answers are 'T' or 'F'. Change at most k of them to maximize the longest run of equal answers.",
        example="\"TTFF\", k = 2  →  4",
        criterion="Which approach is linear?",
        hint="A run of T's after changes is a window with at most k F's. What about runs of F's?",
        choices=(
            Choice(
                "Window with ≤ k of the minority, both ways", OPTIMAL, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Shrink while the window has more than k T's and more than k F's; track the length.",
                why="A window can be made uniform if either letter appears at most k times. That condition only gets easier as the window shrinks.",
            ),
            Choice(
                "Try each start", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="From each index, extend while one letter count stays ≤ k.",
                why="Correct, but overlapping scans repeat work.",
            ),
            Choice(
                "Only turn F into T", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Longest window with at most k F's.",
                why="For \"TFFT\", k = 1, that gives 2. What does turning one T into F give?",
            ),
            Choice(
                "Longest run plus k", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Add k to the longest existing run, capped at n.",
                why="Changing a letter between two runs joins them. Is that counted?",
            ),
        ),
    ),
    Question(
        slug="max-consecutive-ones-iii", number=1004, title="Max Consecutive Ones III",
        difficulty="Medium", topics=("sliding-window",),
        summary="Flip at most k zeros in a binary array; return the longest run of 1s.",
        example="[1,1,1,0,0,0,1,1,1,1,0], k = 2  →  6",
        criterion="Which approach is linear with O(1) extra space?",
        hint="After flipping, which windows become all 1s?",
        choices=(
            Choice(
                "Longest window with at most k zeros", OPTIMAL, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Count zeros in the window; shrink while there are more than k.",
                why="Any window with ≤ k zeros can be turned into 1s, and that stays true when it shrinks, so the left edge only advances.",
            ),
            Choice(
                "Prefix zeros and binary search", SUBOPTIMAL, time="O(n log n)", space="O(n)", visual="binary-search",
                detail="For each right end, binary search the leftmost start with ≤ k zeros.",
                why="Correct, but the left edge only moves forward, so the search is unnecessary.",
            ),
            Choice(
                "Longest run plus k", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Add k to the longest run of 1s.",
                why="Flipping zeros between runs joins them, and k may exceed the zeros nearby. Is run + k always reachable?",
            ),
            Choice(
                "Flip the first k zeros", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Flip zeros from the left until k are used.",
                why="In the example, the best flips are at the end. Does left-first find them?",
            ),
        ),
    ),
    Question(
        slug="longest-semi-repeating-subarray", number=3641, title="Longest Semi-Repeating Subarray",
        difficulty="Medium", topics=("sliding-window",),
        summary="A subarray is semi-repeating if at most k distinct values appear in it more than once. Return the longest such subarray's length.",
        example="[1,2,3,1,2,3,4], k = 2  →  6",
        criterion="Which approach is linear?",
        hint="Keep counts in the window. When does the number of repeating values change?",
        choices=(
            Choice(
                "Window with a repeating-values tally", OPTIMAL, time="O(n)", space="O(n)", visual="sliding-window",
                detail="When a count goes 1 → 2, the tally rises; 2 → 1 lowers it; shrink while the tally exceeds k.",
                why="The tally only changes when a count crosses 2, so it updates in O(1). Shrinking never adds repeats, so the left edge only advances.",
            ),
            Choice(
                "Extend from every start", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="brute",
                detail="From each start, extend until more than k values repeat.",
                why="Correct, but every start recounts from scratch.",
            ),
            Choice(
                "Count repeated elements, not values", INCORRECT, time="O(n)", space="O(n)", visual="sliding-window",
                detail="Shrink while more than k elements are extra copies.",
                why="[1,1,1] has one repeating value but two extra copies. Which does the rule limit?",
            ),
            Choice(
                "At most k extra occurrences total", INCORRECT, time="O(n)", space="O(n)", visual="counting",
                detail="Allow each value up to one repeat, at most k such values in all of nums.",
                why="The limit applies inside the subarray, not to the whole array.",
            ),
        ),
    ),
    Question(
        slug="find-the-longest-semi-repetitive-substring", number=2730, title="Find the Longest Semi-Repetitive Substring",
        difficulty="Medium", topics=("sliding-window",),
        summary="A digit string is semi-repetitive if it has at most one pair of adjacent equal digits. Return the longest semi-repetitive substring's length.",
        example="\"52233\"  →  4",
        criterion="Which approach is linear?",
        hint="Track adjacent equal pairs inside the window. When there are two, where must left go?",
        choices=(
            Choice(
                "Window with at most one equal pair", OPTIMAL, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Increment the pair count when s[r] = s[r − 1]; while it's 2, advance l and decrement when s[l] = s[l − 1] leaves.",
                why="Shrinking never adds a pair, so the left edge only moves forward. Each step is O(1).",
            ),
            Choice(
                "Check every substring", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="From each start, extend until a second pair appears.",
                why="Correct, but repeats the scan per start.",
            ),
            Choice(
                "Split at every equal pair", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Cut between equal neighbours and take the longest piece.",
                why="One pair is allowed. \"5223\" keeps the 22 pair. Would splitting allow it?",
            ),
            Choice(
                "Distinct digits only", INCORRECT, time="O(n)", space="O(1)", visual="set",
                detail="Longest substring without repeated digits.",
                why="\"5225\" repeats digits but has only one equal pair. Is it semi-repetitive?",
            ),
        ),
    ),
    Question(
        slug="maximum-beauty-of-an-array-after-applying-operation", number=2779, title="Maximum Beauty of an Array After Applying Operation",
        difficulty="Medium", topics=("sliding-window",),
        summary="Each element may be replaced once by any value within k of it. Return the longest subsequence of equal elements you can create.",
        example="[4,6,1,2], k = 2  →  3",
        criterion="Which approach is O(n log n)?",
        hint="Two elements can meet if their ranges overlap. In sorted order, what does that mean for the smallest and largest in a group?",
        choices=(
            Choice(
                "Sort, longest window with max − min ≤ 2k", OPTIMAL, time="O(n log n)", space="O(1)", visual="sliding-window",
                detail="Sort; advance left while a[r] − a[l] > 2k; track the window length.",
                why="A group can share a value exactly when all ranges overlap, i.e. max − min ≤ 2k. Order doesn't matter for a subsequence, so sort.",
            ),
            Choice(
                "Try each element as the group's minimum", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="For each element a, count elements in [a, a + 2k].",
                why="Correct, but each element scans the whole array.",
            ),
            Choice(
                "max − min ≤ k", INCORRECT, time="O(n log n)", space="O(1)", visual="sliding-window",
                detail="Sort; longest window with spread at most k.",
                why="Both ends can move: 1 can rise to 3 and 6 can drop to 4. With k = 2, can 2 and 6 meet?",
            ),
            Choice(
                "Window without sorting", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Run the spread check on the original order.",
                why="A subsequence can skip elements. Must the group be contiguous?",
            ),
        ),
    ),
    Question(
        slug="maximum-subarray-with-equal-products", number=3411, title="Maximum Subarray With Equal Products",
        difficulty="Easy", topics=("sliding-window",),
        summary="A subarray is product-equivalent if its product equals lcm × gcd. Return the longest such subarray. Values are 1–10.",
        example="[2,3,4,5,6]  →  3",
        criterion="Which approach is linear?",
        hint="For length ≥ 3, the equation holds exactly when no prime divides two elements. Length 2 always works.",
        choices=(
            Choice(
                "Window with no shared prime factor", OPTIMAL, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Track counts of primes 2, 3, 5, 7 in the window; shrink while any is above 1; answer = max(longest, 2).",
                why="With pairwise coprime elements, the lcm is the product and the gcd is 1. A shared prime makes the lcm smaller than the product. Any two elements satisfy the equation.",
            ),
            Choice(
                "Every subarray with running gcd, lcm and product", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="From each start, extend while updating gcd, lcm and the product.",
                why="Correct for n ≤ 100, but the coprime window answers the same question in one pass.",
            ),
            Choice(
                "All elements distinct", INCORRECT, time="O(n)", space="O(1)", visual="set",
                detail="Longest window with no repeated value.",
                why="2 and 4 are distinct but share the prime 2. Does [2,3,4] satisfy the equation?",
            ),
            Choice(
                "gcd equals 1", INCORRECT, time="O(n²)", space="O(1)", visual="math",
                detail="Longest window whose gcd is 1.",
                why="[2,3,4] has gcd 1. Its product is 24 and lcm × gcd is 12.",
            ),
        ),
    ),
    Question(
        slug="longest-substring-with-at-least-k-repeating-characters", number=395, title="Longest Substring with At Least K Repeating Characters",
        difficulty="Medium", topics=("sliding-window",),
        summary="Return the length of the longest substring in which every character appears at least k times.",
        example="\"ababbc\", k = 2  →  5",
        criterion="Which approach is linear (times the alphabet)?",
        hint="A plain window can't decide when to shrink. What if you also fixed how many distinct letters the window may hold?",
        choices=(
            Choice(
                "One window per distinct-letter count", OPTIMAL, time="O(26·n)", space="O(1)", visual="sliding-window",
                detail="For u = 1..26, keep windows with at most u distinct letters; when exactly u letters all have count ≥ k, record the length.",
                why="Fixing u makes 'too many letters' a condition that shrinking fixes, so each pass is a normal window.",
            ),
            Choice(
                "Check every substring", SUBOPTIMAL, time="O(26·n²)", space="O(1)", visual="brute",
                detail="From each start, extend with counts and test all letters.",
                why="Correct, but quadratic in n.",
            ),
            Choice(
                "Shrink while some letter is below k", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Grow right; whenever a letter has fewer than k, advance left.",
                why="A new letter always starts below k. Adding more of it later could fix that. Is shrinking the right response?",
            ),
            Choice(
                "Sum counts of letters with count ≥ k", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Add up the letters that are frequent enough in s.",
                why="The letters must be contiguous, and a rare letter between them breaks the substring.",
            ),
        ),
    ),
    Question(
        slug="longest-nice-substring", number=1763, title="Longest Nice Substring",
        difficulty="Easy", topics=("sliding-window",),
        summary="A string is nice if every letter in it appears in both upper and lower case. Return the longest nice substring (the earliest on ties), or \"\".",
        example="\"YazaAay\"  →  \"aAa\"",
        criterion="Which approach is linear (times the alphabet)?",
        hint="As with \"at least k repeating\", fix how many distinct letters (ignoring case) the window holds.",
        choices=(
            Choice(
                "One window per distinct-letter count", OPTIMAL, time="O(26·n)", space="O(1)", visual="sliding-window",
                detail="For u = 1..26, keep at most u distinct letters; when all u appear in both cases, record the window.",
                why="With u fixed, shrinking is the right move when a new letter arrives, so each pass is linear.",
            ),
            Choice(
                "Every substring with case bitmasks", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="bits",
                detail="From each start, extend with lower and upper masks; nice when they're equal.",
                why="Correct and simple, but quadratic.",
            ),
            Choice(
                "Letters nice in all of s", INCORRECT, time="O(n)", space="O(1)", visual="set",
                detail="Keep the longest run of letters whose both cases appear somewhere in s.",
                why="In \"YazaAay\", 'y' and 'Y' both appear, but not near each other. Is \"Yaz…\" nice?",
            ),
            Choice(
                "Equal upper and lower counts", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="A substring is nice if it has as many upper as lower letters.",
                why="\"aB\" has one of each. Is it nice?",
            ),
        ),
    ),
    Question(
        slug="max-consecutive-ones-ii", number=487, title="Max Consecutive Ones II",
        difficulty="Medium", topics=("sliding-window",),
        summary="Flip at most one 0 in a binary array; return the longest run of 1s.",
        example="[1,0,1,1,0]  →  4",
        criterion="Which approach is linear with O(1) extra space?",
        hint="Which windows become all 1s after one flip?",
        choices=(
            Choice(
                "Window with at most one 0", OPTIMAL, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Shrink while the window holds two zeros.",
                why="One flip fixes a window with one 0, and that stays true as it shrinks, so left only advances.",
            ),
            Choice(
                "Try flipping each 0", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="For each zero, measure the run it would create.",
                why="Correct, but each try rescans the array.",
            ),
            Choice(
                "Longest run plus one", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Add 1 to the longest run of 1s.",
                why="Flipping the 0 between [1] and [1,1] joins them into 4. Does run + 1 see that?",
            ),
            Choice(
                "Flip the first 0", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Flip the leftmost zero and measure.",
                why="For [1,0,1,1,0,1,1,1], flipping the first 0 gives 4, the second gives 6.",
            ),
        ),
    ),
    Question(
        slug="longest-substring-with-at-most-two-distinct-characters", number=159, title="Longest Substring with At Most Two Distinct Characters",
        difficulty="Medium", topics=("sliding-window",),
        summary="Return the length of the longest substring with at most two distinct characters.",
        example="\"eceba\"  →  3",
        criterion="Which approach is linear?",
        hint="When a third character enters, what must leave?",
        choices=(
            Choice(
                "Window with ≤ 2 distinct", OPTIMAL, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Count characters; while 3 are present, drop from the left.",
                why="Shrinking never adds a character, so the left edge only advances.",
            ),
            Choice(
                "Extend from every start", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="From each index, extend until a third character appears.",
                why="Correct, but overlapping scans repeat work.",
            ),
            Choice(
                "Two most common characters", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Sum the counts of the two most frequent characters.",
                why="They might not be next to each other. Must the substring be contiguous?",
            ),
            Choice(
                "Restart at a third character", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Start a new window at the character that made three.",
                why="In \"abaac\", restarting at c loses \"aac\". Should only the old letter be dropped?",
            ),
        ),
    ),
    Question(
        slug="longest-substring-with-at-most-k-distinct-characters", number=340, title="Longest Substring with At Most K Distinct Characters",
        difficulty="Medium", topics=("sliding-window",),
        summary="Return the length of the longest substring with at most k distinct characters.",
        example="\"eceba\", k = 2  →  3",
        criterion="Which approach is linear?",
        hint="Shrinking a window can only lower its distinct count.",
        choices=(
            Choice(
                "Window with ≤ k distinct", OPTIMAL, time="O(n)", space="O(k)", visual="sliding-window",
                detail="Count characters in a map; while it has more than k keys, drop from the left.",
                why="The left edge only moves forward, so each character enters and leaves once.",
            ),
            Choice(
                "Extend from every start", SUBOPTIMAL, time="O(n²)", space="O(k)", visual="brute",
                detail="From each index, extend until k + 1 distinct appear.",
                why="Correct, but every start recounts.",
            ),
            Choice(
                "Slide with a plain set", INCORRECT, time="O(n)", space="O(k)", visual="set",
                detail="Remove s[l] from the set as the left edge passes it.",
                why="If another copy of s[l] is still in the window, is that letter gone?",
            ),
            Choice(
                "k most common characters", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Sum the counts of the k most frequent characters.",
                why="Those characters might be scattered. Is that one substring?",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §2.2 variable window: shortest
    Question(
        slug="minimum-size-subarray-sum", number=209, title="Minimum Size Subarray Sum",
        difficulty="Medium", topics=("sliding-window",),
        summary="Given positive integers, return the length of the shortest subarray with sum ≥ target, or 0.",
        example="target = 7, [2,3,1,2,4,3]  →  2",
        criterion="Which approach is linear with O(1) extra space?",
        hint="Once the window reaches the target, how far can you shrink it from the left?",
        choices=(
            Choice(
                "Grow right, shrink while sum ≥ target", OPTIMAL, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Add nums[r]; while the sum reaches target, record the length and drop nums[l].",
                why="With positive values, a longer window has a larger sum. The shortest valid window ending at r starts no earlier than the one for r − 1.",
            ),
            Choice(
                "Prefix sums and binary search", SUBOPTIMAL, time="O(n log n)", space="O(n)", visual="binary-search",
                detail="For each start, binary search the first prefix that reaches target.",
                why="Correct, but monotonicity already lets both edges sweep once.",
            ),
            Choice(
                "Largest elements first", INCORRECT, time="O(n log n)", space="O(1)", visual="sort",
                detail="Sort descending and count how many reach the target.",
                why="4 and 3 are adjacent here by luck. Must the subarray be contiguous?",
            ),
            Choice(
                "Restart when the target is reached", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Record the length and reset the sum to 0.",
                why="Elements just before the reset could start a shorter window. Are they reconsidered?",
            ),
        ),
    ),
    Question(
        slug="minimum-subarray-length-with-distinct-sum-at-least-k", number=3795, title="Minimum Subarray Length With Distinct Sum At Least K",
        difficulty="Medium", topics=("sliding-window",),
        summary="A subarray's distinct sum adds each different value once. Return the shortest subarray with distinct sum ≥ k, or −1.",
        example="[2,2,3,1], k = 4  →  2",
        criterion="Which approach is linear?",
        hint="When does adding or removing an element change the distinct sum?",
        choices=(
            Choice(
                "Window with counts and a distinct sum", OPTIMAL, time="O(n)", space="O(n)", visual="sliding-window",
                detail="Add x to the sum when its count goes 0 → 1, subtract when 1 → 0; shrink while the sum ≥ k.",
                why="Widening a window never lowers its distinct sum, so the shortest valid window behaves like the positive-sum case.",
            ),
            Choice(
                "Extend from every start", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="brute",
                detail="From each index, extend until the distinct sum reaches k.",
                why="Correct, but each start rebuilds its set.",
            ),
            Choice(
                "Plain sum", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Shortest window with ordinary sum ≥ k.",
                why="[2,2] sums to 4 but its distinct sum is 2. Does it count?",
            ),
            Choice(
                "Largest distinct values", INCORRECT, time="O(n log n)", space="O(n)", visual="sort",
                detail="Take distinct values from largest down until k is reached.",
                why="They must sit inside one subarray. Are they adjacent?",
            ),
        ),
    ),
    Question(
        slug="shortest-and-lexicographically-smallest-beautiful-string", number=2904, title="Shortest and Lexicographically Smallest Beautiful String",
        difficulty="Medium", topics=("sliding-window",),
        summary="A substring of binary s is beautiful if it has exactly k ones. Among the shortest beautiful substrings, return the lexicographically smallest, or \"\".",
        example="\"100011001\", k = 3  →  \"11001\"",
        criterion="Which approach only compares the shortest candidates?",
        hint="A shortest beautiful substring starts and ends with '1'. How do you slide between them?",
        choices=(
            Choice(
                "Window over exactly k ones, compare equal lengths", OPTIMAL, time="O(n²)", space="O(n)", visual="sliding-window",
                detail="Keep k ones in the window, trim leading zeros; keep the shorter, or the smaller on equal length.",
                why="The candidates are windows from one '1' to the k-th '1' after it, so there are at most n of them. Only those are compared.",
            ),
            Choice(
                "All substrings, filter and sort", SUBOPTIMAL, time="O(n³ log n)", space="O(n²)", visual="brute",
                detail="Collect every substring with k ones, sort by (length, string).",
                why="Correct, but builds and sorts O(n²) strings.",
            ),
            Choice(
                "First shortest found", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Return the leftmost shortest window.",
                why="Two windows of the same length can differ. Is the leftmost always smallest?",
            ),
            Choice(
                "Shortest window with at least k ones", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Minimize length with ones ≥ k, then return it.",
                why="That finds the length, but which of the equal-length windows is lexicographically smallest?",
            ),
        ),
    ),
    Question(
        slug="minimum-window-substring", number=76, title="Minimum Window Substring",
        difficulty="Hard", topics=("sliding-window",),
        summary="Return the shortest substring of s containing every character of t (with multiplicity), or \"\".",
        example="s = \"ADOBECODEBANC\", t = \"ABC\"  →  \"BANC\"",
        criterion="Which approach is linear in |s| + |t|?",
        hint="Track how many required characters are still missing. When it hits zero, how far can left move?",
        choices=(
            Choice(
                "Window with need counts and a missing tally", OPTIMAL, time="O(m + n)", space="O(Σ)", visual="sliding-window",
                detail="Decrement need[s[r]] and the tally when it was positive; while nothing is missing, record and drop s[l].",
                why="The tally tells validity in O(1). A valid window stays valid when widened, so both edges only move forward.",
            ),
            Choice(
                "Check each window's counts", SUBOPTIMAL, time="O(n²·Σ)", space="O(Σ)", visual="brute",
                detail="For each start, extend and compare full count arrays.",
                why="Correct, but comparing all counts at every step is slow.",
            ),
            Choice(
                "Ignore repeats in t", INCORRECT, time="O(m + n)", space="O(Σ)", visual="set",
                detail="Only require each distinct letter of t once.",
                why="For t = \"AA\", is \"A\" enough?",
            ),
            Choice(
                "First and last required letters", INCORRECT, time="O(n)", space="O(1)", visual="two-pointers",
                detail="Span from the first to the last occurrence of t's letters.",
                why="That covers almost all of s. Is it the shortest?",
            ),
        ),
    ),
    Question(
        slug="smallest-range-covering-elements-from-k-lists", number=632, title="Smallest Range Covering Elements from K Lists",
        difficulty="Hard", topics=("sliding-window",),
        summary="Given k sorted lists, return the smallest range [a, b] that includes at least one number from each list.",
        example="[[4,10,15,24,26],[0,9,12,20],[5,18,22,30]]  →  [20, 24]",
        criterion="Which approach is O(N log k) for N numbers in total?",
        hint="If you hold one pointer per list, which pointer is worth advancing?",
        choices=(
            Choice(
                "Min-heap of one element per list", OPTIMAL, time="O(N log k)", space="O(k)", visual="heap",
                detail="Track the current max; pop the min, record [min, max], push the next element of that list.",
                why="The range is limited by the minimum. Advancing any other pointer only widens it, so only the min's list moves. The heap holds k items.",
            ),
            Choice(
                "Merge all, then sliding window", SUBOPTIMAL, time="O(N log N)", space="O(N)", visual="sliding-window",
                detail="Sort all (value, list) pairs; find the shortest window covering all k lists.",
                why="Correct, but sorting all N values ignores that each list is already sorted.",
            ),
            Choice(
                "Max of mins to min of maxes", INCORRECT, time="O(k)", space="O(1)", visual="math",
                detail="Return [max of first elements, min of last elements].",
                why="That gives [5, 26]. It covers each list, but is it the smallest?",
            ),
            Choice(
                "Range of the first elements", INCORRECT, time="O(k)", space="O(1)", visual="greedy",
                detail="Return [min, max] of each list's first element.",
                why="That's [0, 5]. It covers each list, but is it the smallest?",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §2.3 counting subarrays
    Question(
        slug="subarray-product-less-than-k", number=713, title="Subarray Product Less Than K",
        difficulty="Medium", topics=("sliding-window",),
        summary="Given positive integers, count the contiguous subarrays whose product is strictly less than k.",
        example="[10,5,2,6], k = 100  →  8",
        criterion="Which approach is linear with O(1) extra space?",
        hint="If [l..r] qualifies, so does every subarray ending at r that starts after l. How many is that?",
        choices=(
            Choice(
                "Shrink while product ≥ k, add r − l + 1", OPTIMAL, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Multiply in nums[r]; divide out nums[l] while the product is ≥ k; count r − l + 1 subarrays ending at r. Return 0 when k ≤ 1.",
                why="Shorter is better here, so all starts from l to r work. Each element is multiplied in and divided out once.",
            ),
            Choice(
                "Multiply out from every start", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="From each start, extend while the product stays below k.",
                why="Correct, but overlapping products are recomputed from scratch.",
            ),
            Choice(
                "Count windows, not subarrays", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Add 1 for each valid window instead of r − l + 1.",
                why="[5,2] qualifies, and so does [2] inside it. Who counts [2]?",
            ),
            Choice(
                "Count elements below k", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Each element < k is one valid subarray.",
                why="That counts only length 1. Where does [5,2,6] go?",
            ),
        ),
    ),
    Question(
        slug="count-substrings-that-satisfy-k-constraint-i", number=3258, title="Count Substrings That Satisfy K-Constraint I",
        difficulty="Easy", topics=("sliding-window",),
        summary="A binary substring satisfies the k-constraint if it has at most k zeros or at most k ones. Count such substrings.",
        example="\"10101\", k = 1  →  12",
        criterion="Which approach is linear?",
        hint="Shrinking a substring can't break the constraint. So for each right end, valid starts form what?",
        choices=(
            Choice(
                "Shrink while both counts exceed k", OPTIMAL, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Add s[r]; while zeros > k and ones > k, drop s[l]; count r − l + 1.",
                why="Every start from l to r gives a valid substring ending at r, and the left edge only advances.",
            ),
            Choice(
                "Check every substring", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="From each start, extend and count.",
                why="Correct, but rescans overlapping substrings.",
            ),
            Choice(
                "Require both counts ≤ k", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Shrink while zeros > k or ones > k.",
                why="\"111\" has no zeros, so it satisfies the rule for k = 1. Would 'and' accept it?",
            ),
            Choice(
                "Only substrings of length ≤ 2k + 1", INCORRECT, time="O(n·k)", space="O(1)", visual="brute",
                detail="Count substrings short enough that one count must be ≤ k.",
                why="Long runs of one digit also satisfy it. What about \"1111\" with k = 1?",
            ),
        ),
    ),
    Question(
        slug="lcp-68-beautiful-bouquet", number=None, title="Beautiful Bouquet",
        difficulty="Medium", topics=("sliding-window",),
        ref="LCP 68", url="https://leetcode.cn/problems/1GxJYY/",
        summary="Count the contiguous ranges of flowers in which no variety appears more than cnt times.",
        example="[1,2,3,2], cnt = 1  →  8",
        criterion="Which approach is linear?",
        hint="If a range is fine, so is every shorter range ending at the same place.",
        choices=(
            Choice(
                "Shrink while the new flower exceeds cnt", OPTIMAL, time="O(n)", space="O(n)", visual="sliding-window",
                detail="Add flowers[r]; while its count > cnt, drop flowers[l]; count r − l + 1.",
                why="Only the newest flower can break the limit, and every start from l to r works once it's fixed.",
            ),
            Choice(
                "Extend from every start", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="brute",
                detail="From each start, extend until some variety exceeds cnt.",
                why="Correct, but each start recounts.",
            ),
            Choice(
                "Count the longest window only", INCORRECT, time="O(n)", space="O(n)", visual="sliding-window",
                detail="Add 1 per right end for its longest valid range.",
                why="Ending at index 2, [1,2,3], [2,3] and [3] are all fine. How many does this add?",
            ),
            Choice(
                "n·(n + 1)/2 minus bad pairs", INCORRECT, time="O(n)", space="O(n)", visual="math",
                detail="Subtract one range for each pair of equal flowers.",
                why="A range can hold several equal pairs, and one bad pair spoils many ranges. Does one subtraction per pair match?",
            ),
        ),
    ),
    Question(
        slug="count-substrings-without-repeating-character", number=2743, title="Count Substrings Without Repeating Character",
        difficulty="Medium", topics=("sliding-window",),
        summary="Count the substrings (by position) of s that have no repeated character.",
        example="\"abcd\"  →  10",
        criterion="Which approach is linear?",
        hint="This is Longest Substring Without Repeating Characters, but you count instead of measure.",
        choices=(
            Choice(
                "No-repeat window, add its length each step", OPTIMAL, time="O(n)", space="O(Σ)", visual="sliding-window",
                detail="Maintain the longest repeat-free window ending at r; add r − l + 1.",
                why="Every start from l to r gives a repeat-free substring ending at r, and l only moves forward.",
            ),
            Choice(
                "Extend from every start", SUBOPTIMAL, time="O(n·Σ)", space="O(Σ)", visual="brute",
                detail="From each index, extend until a repeat and count the steps.",
                why="Correct, but overlapping scans repeat work.",
            ),
            Choice(
                "Count distinct substrings", INCORRECT, time="O(n²)", space="O(n²)", visual="set",
                detail="Collect qualifying substrings in a set.",
                why="For \"aa\", the two \"a\"s are at different positions. How many does the task count?",
            ),
            Choice(
                "Triangular number of the longest", INCORRECT, time="O(n)", space="O(Σ)", visual="math",
                detail="Find the longest window L and return L·(L + 1)/2.",
                why="For \"abab\" the longest is 2, giving 3. Counting by hand gives 7.",
            ),
        ),
    ),
    Question(
        slug="number-of-substrings-containing-all-three-characters", number=1358, title="Number of Substrings Containing All Three Characters",
        difficulty="Medium", topics=("sliding-window",),
        summary="s has only 'a', 'b', 'c'. Count the substrings that contain at least one of each.",
        example="\"abcabc\"  →  10",
        criterion="Which approach is linear?",
        hint="If [l..r] contains all three, so does every substring that starts earlier and ends at r.",
        choices=(
            Choice(
                "Shrink while all three are present, add l", OPTIMAL, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Add s[r]; while the window has all three, drop s[l]; then add l (the number of valid starts).",
                why="After shrinking, starts 0..l − 1 all give valid substrings ending at r. Longer is better here, so this counts them in O(1).",
            ),
            Choice(
                "Check every substring", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="From each start, extend and count once all three appear.",
                why="Correct, but each start scans forward again.",
            ),
            Choice(
                "Windows of length 3", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Count length-3 windows containing a, b and c.",
                why="\"abca\" contains all three too. Is it counted?",
            ),
            Choice(
                "Add r − l + 1", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Count the window's length as with 'at most' problems.",
                why="Here longer substrings are the valid ones. Which starts work for a given r?",
            ),
        ),
    ),
    Question(
        slug="count-substrings-with-k-frequency-characters-i", number=3325, title="Count Substrings With K-Frequency Characters I",
        difficulty="Medium", topics=("sliding-window",),
        summary="Count the substrings in which at least one character appears at least k times.",
        example="\"abacb\", k = 2  →  4",
        criterion="Which approach is linear?",
        hint="Once a substring qualifies, does extending it to the left keep it qualified?",
        choices=(
            Choice(
                "Shrink while s[r] has count ≥ k, add l", OPTIMAL, time="O(n)", space="O(Σ)", visual="sliding-window",
                detail="Add s[r]; while count[s[r]] ≥ k, drop s[l]; then add l.",
                why="Only the newest character can newly reach k. After shrinking, every start before l works.",
            ),
            Choice(
                "Check every substring", SUBOPTIMAL, time="O(n²)", space="O(Σ)", visual="brute",
                detail="From each start, extend until some count hits k; the rest of that start's substrings all qualify.",
                why="Correct, but each start scans forward again.",
            ),
            Choice(
                "Every character at least k times", INCORRECT, time="O(n)", space="O(Σ)", visual="counting",
                detail="Count substrings where all characters reach k.",
                why="\"aba\" qualifies for k = 2 because of a. Does b need two copies?",
            ),
            Choice(
                "Count substrings of length ≥ k", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="Long enough substrings must repeat something.",
                why="\"abc\" has length 3 but nothing appears twice.",
            ),
        ),
    ),
    Question(
        slug="count-vowel-substrings-of-a-string", number=2062, title="Count Vowel Substrings of a String",
        difficulty="Easy", topics=("sliding-window",),
        summary="Count substrings made only of vowels that contain all five vowels.",
        example="\"aeiouu\"  →  2",
        criterion="Which approach is linear?",
        hint="A consonant splits the string. Inside a vowel-only stretch, what kind of window counting is this?",
        choices=(
            Choice(
                "At-least window inside each vowel run", OPTIMAL, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Restart at consonants; within a run, shrink while all five are present and add the number of valid starts.",
                why="Consonants can't be inside, so runs are independent. Within a run, having all five only gets easier as the window grows.",
            ),
            Choice(
                "Check every substring", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="From each start, extend until a consonant, counting when all five appear.",
                why="Correct, but each start rescans.",
            ),
            Choice(
                "Ignore consonants", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Count substrings containing all five vowels.",
                why="\"aeixou\" has all five but also an x. Does it count?",
            ),
            Choice(
                "Exactly five letters", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Count length-5 windows with all five vowels.",
                why="\"aeiouu\" is longer than 5 and still qualifies.",
            ),
        ),
    ),
    Question(
        slug="count-complete-subarrays-in-an-array", number=2799, title="Count Complete Subarrays in an Array",
        difficulty="Medium", topics=("sliding-window",),
        summary="A subarray is complete if it has as many distinct values as the whole array. Count complete subarrays.",
        example="[1,3,1,2,2]  →  4",
        criterion="Which approach is linear?",
        hint="Let D be the number of distinct values. Extending a complete subarray keeps it complete.",
        choices=(
            Choice(
                "Shrink while the window has D values, add l", OPTIMAL, time="O(n)", space="O(n)", visual="sliding-window",
                detail="Add nums[r]; while the map has D keys, drop nums[l]; then add l.",
                why="After shrinking, every start before l gives a complete subarray ending at r. Both edges move forward only.",
            ),
            Choice(
                "Extend from every start", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="brute",
                detail="From each start, extend until D distinct appear; everything after counts.",
                why="Correct, but each start rebuilds its set.",
            ),
            Choice(
                "Windows of length D", INCORRECT, time="O(n)", space="O(n)", visual="sliding-window",
                detail="Count length-D windows with D distinct values.",
                why="[1,3,1,2] is complete with length 4. Is it counted?",
            ),
            Choice(
                "Add r − l + 1", INCORRECT, time="O(n)", space="O(n)", visual="sliding-window",
                detail="Count window lengths as in 'at most' problems.",
                why="Here longer subarrays are the complete ones. Which starts work?",
            ),
        ),
    ),
    Question(
        slug="number-of-subarrays-having-even-product", number=2495, title="Number of Subarrays Having Even Product",
        difficulty="Medium", topics=("sliding-window",),
        summary="Count the subarrays whose product is even.",
        example="[9,6,7,13]  →  6",
        criterion="Which approach is linear with O(1) extra space?",
        hint="A product is even exactly when the subarray contains what?",
        choices=(
            Choice(
                "Add (last even index + 1) at each end", OPTIMAL, time="O(n)", space="O(1)", visual="two-pointers",
                detail="Track the latest index e with an even value; subarrays ending at r with start ≤ e are even.",
                why="One even element makes the product even, so any start up to the latest even index works.",
            ),
            Choice(
                "Check every subarray", SUBOPTIMAL, time="O(n²)", space="O(1)", visual="brute",
                detail="From each start, extend and track parity.",
                why="Correct, but parity is decided by a single position.",
            ),
            Choice(
                "Subarrays ending at an even element", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="For each even element at i, add i + 1.",
                why="[6,7] ends at 7 but contains 6. Is it counted?",
            ),
            Choice(
                "Subarrays starting at an even element", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="For each even element at i, add n − i.",
                why="[9,6] starts at 9 but contains 6. Is it counted?",
            ),
        ),
    ),
    Question(
        slug="binary-subarrays-with-sum", number=930, title="Binary Subarrays With Sum",
        difficulty="Medium", topics=("sliding-window",),
        summary="Count the subarrays of a binary array whose sum equals goal.",
        example="[1,0,1,0,1], goal = 2  →  4",
        criterion="Which approach is linear with O(1) extra space?",
        hint="'Exactly goal' = 'at least goal' − 'at least goal + 1'.",
        choices=(
            Choice(
                "Two at-least windows, subtracted", OPTIMAL, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Count subarrays with sum ≥ goal and with sum ≥ goal + 1 by sliding windows; subtract.",
                why="Each 'at least' count is a monotone window. Their difference is exactly goal, without storing prefix sums.",
            ),
            Choice(
                "Prefix sums in a hash map", SUBOPTIMAL, time="O(n)", space="O(n)", visual="prefix",
                detail="For each prefix p, add count[p − goal].",
                why="Correct and linear, but it stores up to n prefix counts.",
            ),
            Choice(
                "One window, count when sum == goal", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Shrink while sum > goal; add 1 when it equals goal.",
                why="Leading zeros give several starts with the same sum. [0,1,0,1] has how many with sum 2?",
            ),
            Choice(
                "Choose goal ones", INCORRECT, time="O(n)", space="O(1)", visual="math",
                detail="C(number of ones, goal).",
                why="The chosen ones must be contiguous, and zeros around them multiply the count.",
            ),
        ),
    ),
    Question(
        slug="count-number-of-nice-subarrays", number=1248, title="Count Number of Nice Subarrays",
        difficulty="Medium", topics=("sliding-window",),
        summary="Count the subarrays containing exactly k odd numbers.",
        example="[1,1,2,1,1], k = 3  →  2",
        criterion="Which approach is linear with O(1) extra space?",
        hint="Treat odd as 1 and even as 0. Have you seen this problem before?",
        choices=(
            Choice(
                "At least k minus at least k + 1", OPTIMAL, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Count subarrays with ≥ k odds and with ≥ k + 1 odds via windows; subtract.",
                why="With odds as 1s, it's Binary Subarrays With Sum. Each 'at least' count is monotone and O(1) space.",
            ),
            Choice(
                "Prefix odd counts in a map", SUBOPTIMAL, time="O(n)", space="O(n)", visual="prefix",
                detail="Add count[p − k] for each prefix odd count p.",
                why="Correct and linear, but it stores the prefix counts.",
            ),
            Choice(
                "Windows with exactly k odds, once each", INCORRECT, time="O(n)", space="O(1)", visual="sliding-window",
                detail="Shrink while odds > k; add 1 when odds == k.",
                why="Evens at the edges create several subarrays with the same odds. Are they all counted?",
            ),
            Choice(
                "Count odd numbers", INCORRECT, time="O(n)", space="O(1)", visual="counting",
                detail="Return the number of odd elements minus k + 1.",
                why="That's the number of ways to pick k consecutive odds, ignoring the evens around them.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §2.4 other windows
    Question(
        slug="friends-of-appropriate-ages", number=825, title="Friends Of Appropriate Ages",
        difficulty="Medium", topics=("sliding-window",),
        summary="Person x requests y (x ≠ y) unless age[y] ≤ 0.5·age[x] + 7, age[y] > age[x], or age[y] > 100 > age[x]. Count requests. Ages are 1–120.",
        example="[16,17,18]  →  2",
        criterion="Which approach is O(n + A) for ages up to A = 120?",
        hint="Requests depend only on ages. For one age, which range of ages can it request?",
        choices=(
            Choice(
                "Age counts with prefix sums", OPTIMAL, time="O(n + A)", space="O(A)", visual="prefix",
                detail="Count people per age; for each age a, add count[a] × (people with age in (0.5a + 7, a]) − count[a].",
                why="The rules reduce to a contiguous age range per sender. Prefix sums answer each range in O(1); subtracting count[a] removes self-requests.",
            ),
            Choice(
                "Sort, then a sliding window", SUBOPTIMAL, time="O(n log n)", space="O(1)", visual="sliding-window",
                detail="Sort ages; for each person, move a window over valid partners.",
                why="Correct, but sorting n people is slower than counting 120 ages.",
            ),
            Choice(
                "Count self-requests too", INCORRECT, time="O(n + A)", space="O(A)", visual="prefix",
                detail="Same prefix sums without subtracting count[a].",
                why="For [16, 16], each 16 would request itself. What's the answer?",
            ),
            Choice(
                "Only the age > 100 rule", INCORRECT, time="O(n)", space="O(1)", visual="brute",
                detail="Skip the 0.5·age + 7 bound.",
                why="Could a 20-year-old request a 10-year-old?",
            ),
        ),
    ),
    Question(
        slug="longest-repeating-character-replacement", number=424, title="Longest Repeating Character Replacement",
        difficulty="Medium", topics=("sliding-window",),
        summary="Replace at most k characters of an uppercase string to make the longest run of one letter. Return its length.",
        example="\"AABABBA\", k = 1  →  4",
        criterion="Which approach is linear with O(26) space?",
        hint="A window works if its length minus its most frequent letter's count is ≤ k.",
        choices=(
            Choice(
                "Window with a non-decreasing max frequency", OPTIMAL, time="O(n)", space="O(26)", visual="sliding-window",
                detail="Track the highest count seen; if length − maxFreq > k, slide left by one.",
                why="The answer only grows when maxFreq grows, so a stale maxFreq never inflates the answer. The window never shrinks, it just slides.",
            ),
            Choice(
                "One window per target letter", SUBOPTIMAL, time="O(26·n)", space="O(1)", visual="sliding-window",
                detail="For each letter, find the longest window with ≤ k other letters.",
                why="Correct, but 26 passes where one suffices.",
            ),
            Choice(
                "Longest run plus k", INCORRECT, time="O(n)", space="O(1)", visual="greedy",
                detail="Add k to the longest existing run.",
                why="Replacing one B in \"AABA\" joins runs on both sides. Does run + k see that?",
            ),
            Choice(
                "Most frequent letter overall plus k", INCORRECT, time="O(n)", space="O(26)", visual="counting",
                detail="min(n, maxCount + k).",
                why="The letters must be contiguous after replacing. Are all the A's together?",
            ),
        ),
    ),
    Question(
        slug="lcr-180-file-combination", number=None, title="File Combination",
        difficulty="Easy", topics=("sliding-window",),
        ref="LCR 180", url="https://leetcode.cn/problems/he-wei-sde-lian-xu-zheng-shu-xu-lie-lcof/",
        summary="Return every run of at least two consecutive positive integers summing to target, ordered by first number.",
        example="18  →  [[3,4,5,6], [5,6,7]]",
        criterion="Which approach is O(√target)?",
        hint="If a run has length L and starts at a, its sum is L·a + L(L − 1)/2.",
        choices=(
            Choice(
                "Solve for the start at each length", OPTIMAL, time="O(√target)", space="O(1)", visual="math",
                detail="For L from the largest feasible down to 2, a = (target − L(L − 1)/2) / L must be a positive integer.",
                why="The sum grows like L², so only O(√target) lengths are possible. Longer runs start lower, so descending L gives ascending starts.",
            ),
            Choice(
                "Two-pointer window over 1..target", SUBOPTIMAL, time="O(target)", space="O(1)", visual="sliding-window",
                detail="Grow the right end while the sum is small, shrink the left while it's large.",
                why="Correct, but both pointers walk up to target/2 numbers.",
            ),
            Choice(
                "Include [target] itself", INCORRECT, time="O(√target)", space="O(1)", visual="math",
                detail="Allow runs of length 1.",
                why="The task requires at least two numbers.",
            ),
            Choice(
                "Only odd divisors", INCORRECT, time="O(√target)", space="O(1)", visual="math",
                detail="One run per odd length that divides target.",
                why="[3,4,5,6] has even length 4. Where does it come from?",
            ),
        ),
    ),
    Question(
        slug="kth-smallest-subarray-sum", number=1918, title="Kth Smallest Subarray Sum",
        difficulty="Medium", topics=("sliding-window",),
        summary="Given positive integers, return the k-th smallest sum among all contiguous subarrays.",
        example="[2,1,3], k = 4  →  3",
        criterion="Which approach is O(n log S), where S is the total sum?",
        hint="Can you count how many subarrays have sum ≤ x without listing them?",
        choices=(
            Choice(
                "Binary search the sum, count with a window", OPTIMAL, time="O(n log S)", space="O(1)", visual="binary-search",
                detail="Find the smallest x with at least k subarray sums ≤ x; count them by a sliding window adding r − l + 1.",
                why="With positive values, the count is monotone in x and computed in O(n). Binary search over 1..S needs log S counts.",
            ),
            Choice(
                "List all sums and sort", SUBOPTIMAL, time="O(n² log n)", space="O(n²)", visual="sort",
                detail="Compute every subarray sum, sort, pick the k-th.",
                why="Correct, but n² sums for one answer.",
            ),
            Choice(
                "k-th smallest element", INCORRECT, time="O(n log n)", space="O(1)", visual="sort",
                detail="Sort the array and return its k-th value.",
                why="Single elements are only some of the subarrays. Where do sums like 3 = 2 + 1 go?",
            ),
            Choice(
                "Binary search, count only windows", INCORRECT, time="O(n log S)", space="O(1)", visual="binary-search",
                detail="Count one subarray per right end when its window sum ≤ x.",
                why="Every start inside the window also has sum ≤ x. Are they counted?",
            ),
        ),
    ),
]
