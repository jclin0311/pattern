"""Core route step 4: binary tree DFS (链表、树与回溯 §2.2 top-down, §2.3 bottom-up)."""

from .question_schema import INCORRECT, OPTIMAL, SUBOPTIMAL, Choice, Question

QUESTIONS = [
    # ---------------------------------------------------------------- §2.2 top-down DFS
    Question(
        slug="minimum-depth-of-binary-tree", number=111, title="Minimum Depth of Binary Tree",
        difficulty="Easy", topics=("trees",),
        summary="Return the number of nodes on the shortest path from the root down to a leaf (a node with no children).",
        example="[3, 9, 20, null, null, 15, 7]  →  2",
        criterion="Which approach can stop as soon as the answer is known, even on a very lopsided tree?",
        hint="Which traversal meets the shallowest leaf first?",
        choices=(
            Choice(
                "BFS, stop at the first leaf", OPTIMAL, time="O(n)", space="O(w)", visual="tree-bfs",
                detail="Process the tree level by level; return the depth of the first leaf dequeued.",
                why="Level order finishes depth d before touching depth d+1, so the first leaf you meet is the shallowest. Nothing deeper is ever visited.",
            ),
            Choice(
                "DFS: 1 + min(children)", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="depth(node) = 1 + min(depth(left), depth(right)), with depth(null) = 0.",
                why="A node with only a right child isn't a leaf, yet min(0, right) picks the missing side. Which nodes are allowed to end a path?",
            ),
            Choice(
                "DFS that skips missing children", SUBOPTIMAL, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Recurse; when one child is null, use only the other child's depth.",
                why="Correct, but it always explores the whole tree. If a leaf sits at depth 2 beside a path 10⁴ deep, why walk the long path?",
            ),
            Choice(
                "Follow the leftmost path", INCORRECT, time="O(h)", space="O(1)", visual="tree-dfs",
                detail="Walk left children from the root until null and count.",
                why="Is the left spine always shortest? It may also stop at a node that still has a right child — not a leaf at all.",
            ),
        ),
    ),
    Question(
        slug="path-sum", number=112, title="Path Sum",
        difficulty="Easy", topics=("trees",),
        summary="Decide whether some root-to-leaf path has node values that add up to targetSum. Values may be negative.",
        example="[5,4,8,11,null,13,4,7,2,null,null,null,1], targetSum = 22  →  true",
        criterion="Which approach is linear with O(h) extra space?",
        hint="What should a child be asked to find, given what its parent has already used up?",
        choices=(
            Choice(
                "DFS passing the remaining sum", OPTIMAL, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Subtract each value on the way down; at a leaf, check the remainder is 0.",
                why="The remainder carries everything the path above you contributed. Each node is visited once, and only the current path is on the stack.",
            ),
            Choice(
                "Collect every root-to-leaf path", SUBOPTIMAL, time="O(n·h)", space="O(n·h)", visual="array-copy",
                detail="Store each path as a list, then sum each list.",
                why="Correct, but copying paths costs up to n·h. A running number already says everything a stored path would.",
            ),
            Choice(
                "Prune once the sum overshoots", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Stop exploring a branch when the running sum exceeds targetSum.",
                why="Values can be negative. Can a path that overshoots come back down to the target?",
            ),
            Choice(
                "Accept a match at any node", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Return true as soon as the remaining sum reaches 0, leaf or not.",
                why="The path must end at a leaf. In [1, 2] with target 1, the root alone matches — but is it a leaf?",
            ),
        ),
    ),
    Question(
        slug="sum-root-to-leaf-numbers", number=129, title="Sum Root to Leaf Numbers",
        difficulty="Medium", topics=("trees",),
        summary="Each node holds a digit 0–9. Every root-to-leaf path spells a number. Return the sum of all those numbers.",
        example="[1, 2, 3]  →  12 + 13 = 25",
        criterion="Which approach is linear without building strings?",
        hint="Going one level down, how does the number spelled so far change?",
        choices=(
            Choice(
                "DFS carrying cur·10 + digit", OPTIMAL, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Pass the number so far down; at a leaf, add it to the total.",
                why="Appending a digit is cur·10 + d. Carry that down and each leaf already holds its whole number.",
            ),
            Choice(
                "Build path strings, parse at leaves", SUBOPTIMAL, time="O(n·h)", space="O(h)", visual="array-copy",
                detail="Append digits to a string and convert it at each leaf.",
                why="Correct, but every leaf parses a string of length h. Integer arithmetic does the same in O(1) per step.",
            ),
            Choice(
                "Add digit × 10^depth per node", INCORRECT, time="O(n)", space="O(h)", visual="math",
                detail="Weight each node's digit by its distance from the root.",
                why="A node shared by two paths belongs to both numbers, and its place value depends on how far below it each leaf is. Does one term per node capture that?",
            ),
            Choice(
                "Return each subtree's list of numbers", SUBOPTIMAL, time="O(n·L)", space="O(n)", visual="recursion",
                detail="Each subtree returns (value, length) pairs; the parent prefixes its digit.",
                why="Correct, but every list is rebuilt at every ancestor. Top-down, the prefix is known before you reach the leaf.",
            ),
        ),
    ),
    Question(
        slug="binary-tree-right-side-view", number=199, title="Binary Tree Right Side View",
        difficulty="Medium", topics=("trees",),
        summary="Return the values you would see looking at a binary tree from the right: the last node on each level, top to bottom.",
        example="[1, 2, 3, null, 5, null, 4]  →  [1, 3, 4]",
        criterion="Which approach is linear with O(h) extra space?",
        hint="If you always visit the right child first, which node is the first to reach each new depth?",
        choices=(
            Choice(
                "DFS, right child first", OPTIMAL, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Record a node when its depth equals the answer's length.",
                why="Going right first, the first node you meet at each depth is the rightmost one. Only the recursion stack is needed.",
            ),
            Choice(
                "BFS, last node per level", SUBOPTIMAL, time="O(n)", space="O(w)", visual="tree-bfs",
                detail="Process level by level and keep each level's last node.",
                why="Correct and common, but the queue holds a whole level — up to n/2 nodes in a full tree. Does that meet the space limit?",
            ),
            Choice(
                "Follow right children from the root", INCORRECT, time="O(h)", space="O(1)", visual="tree-dfs",
                detail="Walk the right spine and collect its values.",
                why="In [1, 2, 3, 4], node 4 hangs under the left child, yet it's the only node on its level. Is the right spine always what you see?",
            ),
            Choice(
                "BFS, first node per level", INCORRECT, time="O(n)", space="O(w)", visual="tree-bfs",
                detail="Process level by level and keep each level's first node.",
                why="The first node of each level is what you'd see from the left. Which end of the level faces right?",
            ),
        ),
    ),
    Question(
        slug="count-good-nodes-in-binary-tree", number=1448, title="Count Good Nodes in Binary Tree",
        difficulty="Medium", topics=("trees",),
        summary="A node is good if no node on the path from the root to it has a greater value. Count the good nodes.",
        example="[3, 1, 4, 3, null, 1, 5]  →  4",
        criterion="Which approach is linear with O(h) extra space?",
        hint="What single number summarizes everything a node needs to know about the path above it?",
        choices=(
            Choice(
                "DFS passing the path maximum", OPTIMAL, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="A node is good if its value ≥ the max so far; pass max(max, value) down.",
                why="Only the largest ancestor can disqualify a node, so the running max is the whole story. One visit per node.",
            ),
            Choice(
                "Re-scan ancestors per node", SUBOPTIMAL, time="O(n·h)", space="O(n)", visual="brute",
                detail="Keep parent pointers and walk up from every node to the root.",
                why="Correct, but every node repeats the walk its parent already did. What could the parent hand down instead?",
            ),
            Choice(
                "Compare with the parent only", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Count nodes whose value ≥ their parent's.",
                why="In 3 → 1 → 2, node 2 beats its parent but not the root. Is it good?",
            ),
            Choice(
                "Compare with the root only", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Count nodes whose value ≥ the root's.",
                why="In 3 → 5 → 4, node 4 ≥ 3 but sits below 5. Which ancestor actually matters?",
            ),
        ),
    ),
    Question(
        slug="sum-of-nodes-with-even-valued-grandparent", number=1315, title="Sum of Nodes with Even-Valued Grandparent",
        difficulty="Medium", topics=("trees",),
        summary="Return the sum of values of all nodes whose grandparent exists and has an even value.",
        example="[6,7,8,2,7,1,3,9,null,1,4,null,null,null,5]  →  18",
        criterion="Which approach is linear with O(h) extra space?",
        hint="What does a node need to know about the two levels directly above it?",
        choices=(
            Choice(
                "DFS passing parent and grandparent", OPTIMAL, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Carry (parent, grandparent) values down; shift them one level per step.",
                why="A node only needs its grandparent's parity. Passing two values down gives it that without any lookup structure.",
            ),
            Choice(
                "Parent map, then look up grandparents", SUBOPTIMAL, time="O(n)", space="O(n)", visual="hashmap",
                detail="Record every node's parent, then check each node's grandparent.",
                why="Correct, but the map stores every node. The recursion already knows the ancestors as it descends.",
            ),
            Choice(
                "Sum nodes with an even parent", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Add a node when its parent's value is even.",
                why="That's one level too close. Whose parity does the problem ask about?",
            ),
            Choice(
                "Sum even nodes at depth ≥ 2", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Add every even-valued node that has a grandparent.",
                why="The condition is on the grandparent's value, not the node's own value.",
            ),
        ),
    ),
    Question(
        slug="smallest-string-starting-from-leaf", number=988, title="Smallest String Starting From Leaf",
        difficulty="Medium", topics=("trees",),
        summary="Each node holds a letter (0 = 'a' … 25 = 'z'). Among strings read from a leaf up to the root, return the lexicographically smallest.",
        example="[0, 1, 2, 3, 4, 3, 4]  →  \"dba\"",
        criterion="Which approach always returns the right string?",
        hint="Is the smaller of two child strings still smaller once the parent's letter is appended to both?",
        choices=(
            Choice(
                "DFS with the path; compare at leaves", OPTIMAL, time="O(n·h)", space="O(h)", visual="tree-dfs",
                detail="Keep the root-to-node path; at each leaf, reverse it and keep the minimum.",
                why="The string starts at the leaf, so it's only fully known once you reach one. Comparing complete strings at the leaves avoids every shortcut's trap.",
            ),
            Choice(
                "Bottom-up: min(child strings) + letter", INCORRECT, time="O(n·h)", space="O(n·h)", visual="recursion",
                detail="Each node returns the smaller child string with its own letter appended.",
                why="'a' < 'ab', but after appending 'z': is 'az' < 'abz'? Appending can flip which string is smaller.",
            ),
            Choice(
                "Greedy: step to the smaller child letter", INCORRECT, time="O(h)", space="O(1)", visual="greedy",
                detail="From the root, always go to the child with the smaller letter.",
                why="The string is read from the leaf, so the root end matters least — and what do you do when both children have the same letter?",
            ),
            Choice(
                "Generate all leaf strings and sort", SUBOPTIMAL, time="O(L·h log L)", space="O(L·h)", visual="sort",
                detail="Build every leaf-to-root string, sort, take the first.",
                why="Correct, but you only need the minimum. Why sort them all?",
            ),
        ),
    ),
    Question(
        slug="maximum-difference-between-node-and-ancestor", number=1026, title="Maximum Difference Between Node and Ancestor",
        difficulty="Medium", topics=("trees",),
        summary="Return the largest |a.val − b.val| where node a is an ancestor of node b.",
        example="[8,3,10,1,6,null,14,null,null,4,7,13]  →  7",
        criterion="Which approach is linear with O(h) extra space?",
        hint="For a given node, which two ancestor values could produce the largest difference?",
        choices=(
            Choice(
                "DFS passing the path min and max", OPTIMAL, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Carry the smallest and largest value on the path; compare at each node.",
                why="The best ancestor for a node is either the smallest or the largest one above it. Two numbers passed down cover every ancestor.",
            ),
            Choice(
                "Compare each node with every ancestor", SUBOPTIMAL, time="O(n·h)", space="O(h)", visual="brute",
                detail="Keep the path in a list and scan it at every node.",
                why="Correct, but each scan repeats work. Do you need every ancestor, or only the extremes?",
            ),
            Choice(
                "Compare with the parent only", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Take the largest |node − parent|.",
                why="In 8 → 3 → 1, the best pair is 8 and 1, two levels apart. Can parent–child pairs find it?",
            ),
            Choice(
                "Global max minus global min", INCORRECT, time="O(n)", space="O(h)", visual="math",
                detail="Find the largest and smallest values in the whole tree.",
                why="The max and min can sit in different branches, where neither is an ancestor of the other.",
            ),
        ),
    ),
    Question(
        slug="sum-of-root-to-leaf-binary-numbers", number=1022, title="Sum of Root To Leaf Binary Numbers",
        difficulty="Easy", topics=("trees",),
        summary="Each node is 0 or 1. Every root-to-leaf path is a binary number with the root as the most significant bit. Return the sum.",
        example="[1, 0, 1, 0, 1, 0, 1]  →  22",
        criterion="Which approach is linear with O(h) extra space?",
        hint="Appending a bit to a binary number does what to its value?",
        choices=(
            Choice(
                "DFS carrying cur·2 + bit", OPTIMAL, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Pass (cur << 1) | bit down; add cur at each leaf.",
                why="Shifting left and adding the bit is how a binary number grows by one digit. Each leaf ends up holding its full value.",
            ),
            Choice(
                "Build bit strings, parse at leaves", SUBOPTIMAL, time="O(n·h)", space="O(h)", visual="array-copy",
                detail="Append '0'/'1' along the path and parse base 2 at each leaf.",
                why="Correct, but each leaf re-reads a string of length h. A running integer does the same in O(1) per step.",
            ),
            Choice(
                "Weight bits by tree height", INCORRECT, time="O(n)", space="O(h)", visual="math",
                detail="Add bit × 2^(height − depth) for every node.",
                why="That only works if every leaf is on the bottom level — and a shared node belongs to several paths, so one term isn't enough.",
            ),
            Choice(
                "Bottom-up: add own bit to child sums", INCORRECT, time="O(n)", space="O(h)", visual="recursion",
                detail="Each subtree returns its sum; the parent adds its bit once.",
                why="A parent's bit belongs to every path below it, at a different place value in each. Does adding it once account for that?",
            ),
        ),
    ),
    Question(
        slug="add-one-row-to-tree", number=623, title="Add One Row to Tree",
        difficulty="Medium", topics=("trees",),
        summary="Insert a row of nodes with value val at a given depth. Each node at depth − 1 gets two new children, and its old left and right subtrees move under the new left and right nodes. If depth is 1, the new node becomes the root.",
        example="root = [4,2,6,3,1,5], val = 1, depth = 2  →  [4,1,1,2,null,null,6,3,1,5]",
        criterion="Which approach is correct and touches only the nodes it must?",
        hint="Which nodes actually change their children?",
        choices=(
            Choice(
                "DFS to depth − 1 and splice", OPTIMAL, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Stop at depth − 1; insert new nodes between each node and its children. Handle depth 1 separately.",
                why="Only nodes at depth − 1 change. Splicing there moves whole subtrees by relinking — nothing below is visited.",
            ),
            Choice(
                "Rebuild the whole tree", SUBOPTIMAL, time="O(n)", space="O(n)", visual="array-copy",
                detail="Copy the tree recursively, inserting new nodes at the target depth.",
                why="Correct, but the subtrees below just move. Why copy nodes you could relink?",
            ),
            Choice(
                "Attach new nodes under depth-level nodes", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Give every node at depth new leaf children.",
                why="That adds the row one level too deep, under the old nodes. The old subtrees must hang beneath the new row.",
            ),
            Choice(
                "Splice at depth − 1, no special case", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Always insert under nodes at depth − 1.",
                why="When depth is 1, which node sits at depth 0? The new node has to become the root.",
            ),
        ),
    ),
    Question(
        slug="extract-kth-character-from-the-rope-tree", number=2689, title="Extract Kth Character From The Rope Tree",
        difficulty="Easy", topics=("trees",),
        summary="In a rope tree, leaves hold non-empty strings and each internal node stores the length of the string formed by its left subtree followed by its right subtree. Return the k-th character (1-indexed) of the root's string.",
        example="internal(len 5) → leaves \"ab\", \"cde\", k = 3  →  \"c\"",
        criterion="Which approach makes the best use of the stored lengths?",
        hint="Knowing the left part's length, can you tell which side holds position k?",
        choices=(
            Choice(
                "Descend by comparing k with the left length", OPTIMAL, time="O(h)", space="O(1)", visual="binary-search",
                detail="If k ≤ left length go left, else subtract it and go right.",
                why="The lengths tell you which half holds position k, like indexing into a split range. One path from root to leaf is enough.",
            ),
            Choice(
                "Build the full string", SUBOPTIMAL, time="O(n + |S|)", space="O(|S|)", visual="array-copy",
                detail="Concatenate the leaves in order, then index into it.",
                why="Correct, but it materializes the whole string. Why build what you only need one character of?",
            ),
            Choice(
                "In-order walk counting characters", SUBOPTIMAL, time="O(n + |S|)", space="O(h)", visual="tree-dfs",
                detail="Visit leaves left to right until k characters have passed.",
                why="Correct, but it reads everything before position k. The stored lengths let you skip whole subtrees.",
            ),
            Choice(
                "Pick leaf number ⌈k / leaves⌉", INCORRECT, time="O(n)", space="O(h)", visual="math",
                detail="Divide k by the number of leaves to choose a leaf.",
                why="Leaves hold strings of different lengths. Why would positions split evenly across them?",
            ),
        ),
    ),
    Question(
        slug="binary-tree-longest-consecutive-sequence", number=298, title="Binary Tree Longest Consecutive Sequence",
        difficulty="Medium", topics=("trees",),
        summary="Return the length of the longest downward path (parent to child) along which each value is exactly one more than the previous.",
        example="[1, null, 3, 2, 4, null, null, null, 5]  →  3  (3 → 4 → 5)",
        criterion="Which approach is linear with O(h) extra space?",
        hint="When a child is exactly parent + 1, what happens to the current run? And otherwise?",
        choices=(
            Choice(
                "DFS passing the current run length", OPTIMAL, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="If child = parent + 1, extend the run; else restart at 1. Track the max.",
                why="A run can only continue from its parent, so the parent's run length is all a child needs. One visit per node.",
            ),
            Choice(
                "Search downward from every node", SUBOPTIMAL, time="O(n²)", space="O(h)", visual="brute",
                detail="From each node, follow +1 children as far as possible.",
                why="Correct, but a node inside a long run is re-walked from every node above it. Can the run be carried instead?",
            ),
            Choice(
                "Sort all values, longest run", INCORRECT, time="O(n log n)", space="O(n)", visual="sort",
                detail="Collect the values, sort them and find the longest consecutive run.",
                why="Consecutive values anywhere in the tree don't make a parent-to-child path.",
            ),
            Choice(
                "Only runs starting at the root", INCORRECT, time="O(h)", space="O(h)", visual="tree-dfs",
                detail="Follow +1 children from the root.",
                why="In the example the best run 3 → 4 → 5 starts below the root. Where can a run begin?",
            ),
        ),
    ),
    Question(
        slug="check-if-a-string-is-a-valid-sequence-from-root-to-leaves-path-in-a-binary-tree", number=1430, title="Valid Sequence from Root to Leaf",
        difficulty="Medium", topics=("trees",),
        summary="Given an array arr, decide whether it equals the values along some root-to-leaf path of a binary tree.",
        example="root = [0,1,0,0,1,0,null,null,1,0,0], arr = [0,1,0,1]  →  true",
        criterion="Which approach explores only what can still match?",
        hint="At depth i, which nodes are still worth exploring?",
        choices=(
            Choice(
                "DFS with an index, prune mismatches", OPTIMAL, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Go deeper only while node.val = arr[i]; succeed at a leaf when i is the last index.",
                why="A mismatch kills the whole subtree, so most branches are cut early. The leaf check at the last index enforces 'root to leaf'.",
            ),
            Choice(
                "Enumerate every root-to-leaf path", SUBOPTIMAL, time="O(n·h)", space="O(n·h)", visual="array-copy",
                detail="Store all paths and compare each with arr.",
                why="Correct, but it builds paths that already failed at their first value. Why not stop there?",
            ),
            Choice(
                "Match without the leaf check", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Return true once all of arr has matched along a path.",
                why="arr may match a path that keeps going past its last element. Must the path end exactly there?",
            ),
            Choice(
                "Check arr[i] appears at depth i", INCORRECT, time="O(n)", space="O(w)", visual="tree-bfs",
                detail="For each i, look for any node with value arr[i] at depth i.",
                why="The right values at the right depths can sit on different branches. Do they form one path?",
            ),
        ),
    ),
    Question(
        slug="boundary-of-binary-tree", number=545, title="Boundary of Binary Tree",
        difficulty="Medium", topics=("trees",),
        summary="Return the boundary counter-clockwise from the root: the root, the left boundary (no leaves), all leaves left to right, then the right boundary (no leaves) bottom-up.",
        example="[1, null, 2, 3, 4]  →  [1, 3, 4, 2]",
        criterion="Which approach is linear and emits each node exactly once?",
        hint="Split the boundary into parts with clear start and stop rules.",
        choices=(
            Choice(
                "Left edge, leaves, reversed right edge", OPTIMAL, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Walk the left boundary from root.left (prefer left, else right) skipping leaves; DFS for leaves; collect the right boundary and reverse it.",
                why="Each part has a precise rule, and skipping leaves on the edges means no node is emitted twice.",
            ),
            Choice(
                "First and last node of each level", INCORRECT, time="O(n)", space="O(w)", visual="tree-bfs",
                detail="Level order; take each level's ends, then the whole last level.",
                why="A leaf on a middle level is on the boundary but may be neither first nor last on its level. Where would it come from?",
            ),
            Choice(
                "Left view + leaves + right view", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Combine the left and right side views with the leaves.",
                why="The left view can pick a node from the root's right subtree when the left side is shallow. Is that node on the left boundary?",
            ),
            Choice(
                "Collect all three, then dedupe", SUBOPTIMAL, time="O(n)", space="O(n)", visual="set",
                detail="Gather the edges and leaves loosely and remove repeats with a set.",
                why="It works, but the set patches over overlap that exact start and stop rules avoid — and it costs O(n) extra space.",
            ),
        ),
    ),
    # ---------------------------------------------------------------- §2.3 bottom-up DFS
    Question(
        slug="univalued-binary-tree", number=965, title="Univalued Binary Tree",
        difficulty="Easy", topics=("trees",),
        summary="Decide whether every node in a binary tree has the same value.",
        example="[1, 1, 1, 1, 1, null, 1]  →  true",
        criterion="Which approach is linear with O(h) extra space?",
        hint="What one value must every node match?",
        choices=(
            Choice(
                "DFS comparing with the root value", OPTIMAL, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Return false at the first node that differs.",
                why="Every node must equal the root, so one comparison per node, stopping at the first mismatch.",
            ),
            Choice(
                "Collect values into a set", SUBOPTIMAL, time="O(n)", space="O(n)", visual="set",
                detail="Insert every value; check the set has size 1.",
                why="Correct, but the set grows with the tree and never stops early.",
            ),
            Choice(
                "Check the root's children only", INCORRECT, time="O(1)", space="O(1)", visual="tree-dfs",
                detail="Compare root.left and root.right with the root.",
                why="What about the grandchildren and everything below?",
            ),
            Choice(
                "Sum equals count × root", INCORRECT, time="O(n)", space="O(h)", visual="math",
                detail="Compare the value sum with node count × root value.",
                why="Different values can balance out: root 2 with children 1 and 3 sums to 6 = 3 × 2.",
            ),
        ),
    ),
    Question(
        slug="same-tree", number=100, title="Same Tree",
        difficulty="Easy", topics=("trees",),
        summary="Decide whether two binary trees have the same shape and the same values in the same places.",
        example="[1, 2, 3] and [1, 2, 3]  →  true",
        criterion="Which approach is linear with O(h) extra space?",
        hint="If the roots match, what must be true of their subtrees?",
        choices=(
            Choice(
                "Walk both trees together", OPTIMAL, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Compare roots, then recurse on (left, left) and (right, right).",
                why="Two trees are equal exactly when roots match and both pairs of subtrees are equal. One lockstep walk checks that.",
            ),
            Choice(
                "Compare in-order traversals", INCORRECT, time="O(n)", space="O(n)", visual="array-copy",
                detail="Check that the in-order value lists are equal.",
                why="Root 1 with left child 2, and root 2 with right child 1, both read [2, 1] in order. Same tree?",
            ),
            Choice(
                "Serialize with null markers", SUBOPTIMAL, time="O(n)", space="O(n)", visual="array-copy",
                detail="Write both trees as strings including nulls and compare.",
                why="Correct, because nulls pin down the shape, but it builds two full strings. Comparing in place needs no copies.",
            ),
            Choice(
                "Compare sizes and value sums", INCORRECT, time="O(n)", space="O(h)", visual="math",
                detail="Equal if the node counts and sums match.",
                why="[1, 2] and [1, null, 2] have the same count and sum. Same shape?",
            ),
        ),
    ),
    Question(
        slug="symmetric-tree", number=101, title="Symmetric Tree",
        difficulty="Easy", topics=("trees",),
        summary="Decide whether a binary tree is a mirror image of itself around its center.",
        example="[1, 2, 2, 3, 4, 4, 3]  →  true",
        criterion="Which approach is linear with O(h) extra space?",
        hint="When comparing two mirrored subtrees, which child of one pairs with which child of the other?",
        choices=(
            Choice(
                "Mirror DFS on two pointers", OPTIMAL, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Compare (a.left, b.right) and (a.right, b.left) recursively.",
                why="A mirror pairs the outside children together and the inside children together. Walking both halves that way checks it in one pass.",
            ),
            Choice(
                "Each level is a palindrome", SUBOPTIMAL, time="O(n)", space="O(w)", visual="tree-bfs",
                detail="Level order with null placeholders; check each level reads the same backwards.",
                why="Correct if you keep the nulls, but it holds a whole level at once.",
            ),
            Choice(
                "Left subtree equals right subtree", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Run a same-tree check on root.left and root.right.",
                why="Equal isn't mirrored. In [1, 2, 2, 3, 4, 3, 4], the halves are equal — but is the tree symmetric?",
            ),
            Choice(
                "In-order is a palindrome", INCORRECT, time="O(n)", space="O(n)", visual="array-copy",
                detail="Check the in-order value list reads the same backwards.",
                why="[1, 2, 2, null, 2, null, 2] reads 2, 2, 1, 2, 2 in order, yet both 2s lean right. Mirror?",
            ),
        ),
    ),
    Question(
        slug="flip-equivalent-binary-trees", number=951, title="Flip Equivalent Binary Trees",
        difficulty="Medium", topics=("trees",),
        summary="A flip swaps a node's left and right children. Decide whether two trees with unique values can be made equal by flipping any set of nodes.",
        example="[1,2,3,4,5,6,null,null,null,7,8] and [1,3,2,null,6,4,5,null,null,null,null,8,7]  →  true",
        criterion="Which approach is linear?",
        hint="If the roots match, how many ways can their children pair up?",
        choices=(
            Choice(
                "Recurse: children straight or crossed", OPTIMAL, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Roots must match; then (l1~l2 and r1~r2) or (l1~r2 and r1~l2).",
                why="With unique values, at most one pairing has matching child roots, so the other fails at once. Each node pair is examined a constant number of times.",
            ),
            Choice(
                "Try every combination of flips", SUBOPTIMAL, time="O(2ⁿ·n)", space="O(n)", visual="brute",
                detail="Enumerate subsets of nodes to flip and compare.",
                why="Correct, but exponential. A flip at one node never affects whether its subtrees can match.",
            ),
            Choice(
                "Compare sorted value lists", INCORRECT, time="O(n log n)", space="O(n)", visual="sort",
                detail="Equal if both trees contain the same values.",
                why="Flips keep each node's parent. Do equal value sets guarantee equal parents?",
            ),
            Choice(
                "Same values on each level", INCORRECT, time="O(n)", space="O(w)", visual="tree-bfs",
                detail="Compare each level's values as a set.",
                why="A node can sit on the right level under a different parent — no flip can move it there.",
            ),
        ),
    ),
    Question(
        slug="find-a-corresponding-node-of-a-binary-tree-in-a-clone-of-that-tree", number=1379, title="Find a Corresponding Node in a Clone",
        difficulty="Easy", topics=("trees",),
        summary="You are given a binary tree, an exact copy of it, and a reference to a node in the original. Return the reference to the same node in the copy.",
        example="target = the node with value 3 in the original  →  the node with value 3 in the copy",
        criterion="Which approach still works when values repeat?",
        hint="How can you know where you are in the copy while walking the original?",
        choices=(
            Choice(
                "Walk both trees in lockstep", OPTIMAL, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="DFS both at once; when the original node is target (by reference), return the copy's node.",
                why="The copy has the same shape, so moving identically in both keeps you on corresponding nodes. Comparing references, not values, handles duplicates.",
            ),
            Choice(
                "Search the copy by value", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Find a node in the copy whose value equals target's.",
                why="With repeated values, which of the equal nodes did they mean?",
            ),
            Choice(
                "Parent map, then replay the path", SUBOPTIMAL, time="O(n)", space="O(n)", visual="hashmap",
                detail="Map parents in the original, rebuild target's root path, replay it on the copy.",
                why="Correct, but the map stores every node. Walking both trees together tracks the path for free.",
            ),
            Choice(
                "Return target itself", INCORRECT, time="O(1)", space="O(1)", visual="brute",
                detail="Hand back the reference you were given.",
                why="That node lives in the original tree. Which tree must the answer belong to?",
            ),
        ),
    ),
    Question(
        slug="balanced-binary-tree", number=110, title="Balanced Binary Tree",
        difficulty="Easy", topics=("trees",),
        summary="Decide whether a binary tree is height-balanced: at every node, the left and right subtree heights differ by at most one.",
        example="[3, 9, 20, null, null, 15, 7]  →  true",
        criterion="Which approach is linear?",
        hint="Could one recursive call return both a height and a verdict?",
        choices=(
            Choice(
                "Bottom-up: height or −1", OPTIMAL, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Return each subtree's height, or −1 as soon as any subtree is unbalanced.",
                why="Children report their heights once, and the parent checks the difference on the spot. A −1 short-circuits everything above it.",
            ),
            Choice(
                "Top-down: heights at every node", SUBOPTIMAL, time="O(n²)", space="O(h)", visual="recursion",
                detail="At each node compute both heights from scratch, then recurse.",
                why="Correct, but each subtree's height is recomputed for every ancestor — quadratic on a skewed tree.",
            ),
            Choice(
                "Check the root only", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Compare the root's left and right heights.",
                why="Both root subtrees can have equal height while one of them is badly lopsided inside.",
            ),
            Choice(
                "Max depth − min depth ≤ 1", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Compare the deepest and shallowest leaf.",
                why="Balanced trees can have leaves at depths 2 and 4. The rule is per node, not per leaf.",
            ),
        ),
    ),
    Question(
        slug="invert-binary-tree", number=226, title="Invert Binary Tree",
        difficulty="Easy", topics=("trees",),
        summary="Mirror a binary tree by swapping the left and right children of every node. Return the root.",
        example="[4, 2, 7, 1, 3, 6, 9]  →  [4, 7, 2, 9, 6, 3, 1]",
        criterion="Which approach is linear with O(h) extra space?",
        hint="Is a mirrored tree just every node with its children swapped?",
        choices=(
            Choice(
                "Recursive swap at every node", OPTIMAL, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Swap left and right, then invert both subtrees.",
                why="Mirroring is exactly a swap at every node. Recursion visits each once with only the current path on the stack.",
            ),
            Choice(
                "BFS swapping with a queue", SUBOPTIMAL, time="O(n)", space="O(w)", visual="tree-bfs",
                detail="Pop a node, swap its children, push them.",
                why="Correct, but the queue can hold a whole level — up to n/2 nodes.",
            ),
            Choice(
                "Swap the root's children only", INCORRECT, time="O(1)", space="O(1)", visual="tree-dfs",
                detail="Exchange root.left and root.right.",
                why="The subtrees move, but are they mirrored inside?",
            ),
            Choice(
                "Reverse each level's values", INCORRECT, time="O(n)", space="O(w)", visual="tree-bfs",
                detail="Collect each level and write its values back reversed.",
                why="Values move but the shape doesn't. In [1, 2, null, 3], where should the empty spots end up?",
            ),
        ),
    ),
    Question(
        slug="merge-two-binary-trees", number=617, title="Merge Two Binary Trees",
        difficulty="Easy", topics=("trees",),
        summary="Overlay two binary trees: where both have a node, sum the values; where only one does, use that node.",
        example="[1, 3, 2, 5] + [2, 1, 3, null, 4, null, 7]  →  [3, 4, 5, 5, 4, null, 7]",
        criterion="Which approach does the least work?",
        hint="When one side is missing, what can you return without looking further?",
        choices=(
            Choice(
                "DFS, reuse a subtree when the other is null", OPTIMAL, time="O(min(n₁, n₂))", space="O(min(h₁, h₂))", visual="tree-dfs",
                detail="If one node is null return the other; else sum and recurse.",
                why="Where one tree has nothing, the other's whole subtree is already the answer. Only overlapping nodes are visited.",
            ),
            Choice(
                "Copy both trees into a new one", SUBOPTIMAL, time="O(n₁ + n₂)", space="O(n₁ + n₂)", visual="array-copy",
                detail="Build a fresh tree visiting every node of both inputs.",
                why="Correct and leaves inputs untouched, but it visits every node, not just the overlap.",
            ),
            Choice(
                "Heap-indexed arrays, add elementwise", SUBOPTIMAL, time="O(2^h)", space="O(2^h)", visual="array-copy",
                detail="Place nodes at 2i+1 / 2i+2, add the arrays, rebuild.",
                why="Correct, but a skinny tree of depth 30 needs 2³⁰ slots. Pointers don't pay for empty space.",
            ),
            Choice(
                "Add in-order lists, rebuild", INCORRECT, time="O(n)", space="O(n)", visual="array-copy",
                detail="Sum the in-order traversals and rebuild a tree.",
                why="An in-order list alone can't pin down a tree's shape. Which tree would you rebuild?",
            ),
        ),
    ),
    Question(
        slug="evaluate-boolean-binary-tree", number=2331, title="Evaluate Boolean Binary Tree",
        difficulty="Easy", topics=("trees",),
        summary="Leaves are 0 (False) or 1 (True). Internal nodes are 2 (OR) or 3 (AND) and have two children. Return the value of the root.",
        example="[2, 1, 3, null, null, 0, 1]  →  true",
        criterion="Which approach is linear with O(h) extra space?",
        hint="What does an operator node need before it can produce its value?",
        choices=(
            Choice(
                "Post-order evaluation", OPTIMAL, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Evaluate both children, then apply OR or AND.",
                why="An operator needs its operands first — post-order gives exactly that, once per node.",
            ),
            Choice(
                "Read leaves left to right as an expression", INCORRECT, time="O(n)", space="O(n)", visual="array-copy",
                detail="Join the leaves with their parents' operators and evaluate left to right.",
                why="Grouping comes from the tree's shape. Does a flat left-to-right reading keep it?",
            ),
            Choice(
                "Majority of true leaves", INCORRECT, time="O(n)", space="O(h)", visual="counting",
                detail="Return true if more leaves are 1 than 0.",
                why="One AND over a false leaf makes its whole subtree false, however many trues it has.",
            ),
            Choice(
                "Collapse bottom operators repeatedly", SUBOPTIMAL, time="O(n·h)", space="O(h)", visual="brute",
                detail="Scan for operators with two leaf children, replace them, repeat.",
                why="Correct, but each pass rescans the tree. A single post-order does every collapse in order.",
            ),
        ),
    ),
    Question(
        slug="most-frequent-subtree-sum", number=508, title="Most Frequent Subtree Sum",
        difficulty="Medium", topics=("trees",),
        summary="A subtree sum is the sum of all values in a node's subtree. Return every subtree sum that occurs most often.",
        example="[5, 2, −3]  →  [2, −3, 4]",
        criterion="Which approach is linear?",
        hint="Can each node's subtree sum be built from its children's?",
        choices=(
            Choice(
                "Post-order sums + hash map counts", OPTIMAL, time="O(n)", space="O(n)", visual="hashmap",
                detail="Return each subtree sum upward and count it in a map.",
                why="sum(node) = val + sum(left) + sum(right), so post-order gets every sum in one pass. A map counts them as they appear.",
            ),
            Choice(
                "Recompute each subtree's sum", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="brute",
                detail="For every node, traverse its subtree to sum it.",
                why="Correct, but nodes deep down are summed again for every ancestor. Children already know their sums.",
            ),
            Choice(
                "Post-order, then sort the sums", SUBOPTIMAL, time="O(n log n)", space="O(n)", visual="sort",
                detail="Collect all sums, sort, count runs.",
                why="Correct, but sorting is only there to group equal sums. A hash map groups them in O(1) each.",
            ),
            Choice(
                "Count node values instead", INCORRECT, time="O(n)", space="O(n)", visual="hashmap",
                detail="Return the most frequent node value.",
                why="A subtree sum includes all descendants. Is a node's own value its subtree sum?",
            ),
        ),
    ),
    Question(
        slug="binary-tree-tilt", number=563, title="Binary Tree Tilt",
        difficulty="Easy", topics=("trees",),
        summary="A node's tilt is |sum of its left subtree − sum of its right subtree|. Return the sum of every node's tilt.",
        example="[4, 2, 9, 3, 5, null, 7]  →  15",
        criterion="Which approach is linear with O(h) extra space?",
        hint="What should each recursive call return so its parent can compute its own tilt?",
        choices=(
            Choice(
                "Post-order returning subtree sums", OPTIMAL, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Return the subtree sum; add |left − right| to a running total.",
                why="Tilt needs both children's subtree sums, which is exactly what post-order hands back. One pass computes all tilts.",
            ),
            Choice(
                "Recompute sums at every node", SUBOPTIMAL, time="O(n²)", space="O(h)", visual="brute",
                detail="For each node, sum its left and right subtrees from scratch.",
                why="Correct, but deep subtrees are summed once per ancestor.",
            ),
            Choice(
                "Tilt of the root only", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Return |sum(left) − sum(right)| at the root.",
                why="The answer adds every node's tilt, not just the root's.",
            ),
            Choice(
                "Use the children's values", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Add |left.val − right.val| at each node.",
                why="Tilt compares whole subtree sums. Does a child's own value stand for its entire subtree?",
            ),
        ),
    ),
    Question(
        slug="count-dominant-nodes-in-a-binary-tree", number=3997, title="Count Dominant Nodes in a Binary Tree",
        difficulty="Medium", topics=("trees",),
        url="https://leetcode.cn/problems/count-dominant-nodes-in-a-binary-tree/",
        summary="In a complete binary tree, a node is dominant if its value equals the maximum value in its subtree (itself and all descendants). Count the dominant nodes.",
        example="[5, 3, 8, 2, 4, 7, 1]  →  5",
        criterion="Which approach is linear?",
        hint="What single number should each subtree report to its parent?",
        choices=(
            Choice(
                "Post-order returning the subtree max", OPTIMAL, time="O(n)", space="O(log n)", visual="tree-dfs",
                detail="Each call returns max(val, left max, right max); count nodes with val ≥ both children's maxima.",
                why="A node is dominant exactly when nothing below it is larger, and the children's maxima say that in O(1). The tree is complete, so the stack is only log n deep.",
            ),
            Choice(
                "Recompute each subtree's max", SUBOPTIMAL, time="O(n log n)", space="O(log n)", visual="brute",
                detail="For every node, scan its whole subtree.",
                why="Correct, but each node is rescanned once per ancestor — log n times in a complete tree.",
            ),
            Choice(
                "Compare with the children's values", INCORRECT, time="O(n)", space="O(log n)", visual="tree-dfs",
                detail="Dominant if val ≥ both children's values.",
                why="A grandchild can be larger than both children. Do the children's own values rule it out?",
            ),
            Choice(
                "Strictly greater than everything below", INCORRECT, time="O(n)", space="O(log n)", visual="tree-dfs",
                detail="Dominant only if val beats every descendant.",
                why="Equal counts as the maximum. In [1, 2, 3, 1, 2], the 2 above another 2 is dominant.",
            ),
        ),
    ),
    Question(
        slug="construct-string-from-binary-tree", number=606, title="Construct String from Binary Tree",
        difficulty="Medium", topics=("trees",),
        summary="Write a binary tree as a pre-order string: each child in parentheses after its parent. Drop empty parentheses unless a node has a right child but no left one.",
        example="[1, 2, 3, null, 4]  →  \"1(2()(4))(3)\"",
        criterion="Which approach is correct and linear in the output size?",
        hint="When does an empty pair of parentheses carry information?",
        choices=(
            Choice(
                "Pre-order into one buffer", OPTIMAL, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Append val; add (left) if left or right exists; add (right) if right exists.",
                why="One shared buffer means each character is written once. The '()' is kept only when it marks a missing left child before a right one.",
            ),
            Choice(
                "Return and concatenate strings", SUBOPTIMAL, time="O(n·h)", space="O(n·h)", visual="recursion",
                detail="Each call returns its subtree's string; the parent joins them.",
                why="Correct, but each level copies its children's strings again — quadratic on a skewed tree.",
            ),
            Choice(
                "Always write both children", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Emit '()' for every missing child.",
                why="The rules drop empty pairs that aren't needed. Does a leaf need '()()'?",
            ),
            Choice(
                "Drop every empty pair", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Never emit '()'.",
                why="Then 1(2(4)) could mean 4 is a left or a right child. How would a reader tell?",
            ),
        ),
    ),
    Question(
        slug="count-nodes-equal-to-average-of-subtree", number=2265, title="Count Nodes Equal to Average of Subtree",
        difficulty="Medium", topics=("trees",),
        summary="Count nodes whose value equals the average of the values in their subtree, rounded down.",
        example="[4, 8, 5, 0, 1, null, 6]  →  5",
        criterion="Which approach is linear with O(h) extra space?",
        hint="What two numbers about a subtree let you compute its average?",
        choices=(
            Choice(
                "Post-order returning (sum, count)", OPTIMAL, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Combine the children's sums and counts; compare val with sum // count.",
                why="A subtree's sum and size come straight from its children's, so one pass gets every average.",
            ),
            Choice(
                "Recompute each subtree", SUBOPTIMAL, time="O(n²)", space="O(h)", visual="brute",
                detail="For every node, traverse its subtree to sum and count.",
                why="Correct, but deep nodes are re-summed once per ancestor.",
            ),
            Choice(
                "Average of the children only", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Compare val with the average of its children's values.",
                why="The average is over the whole subtree, including the node itself and every descendant.",
            ),
            Choice(
                "Compare with the exact average", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Use sum / count without rounding.",
                why="The average rounds down here. Node 2 over children 2 and 3 averages 7/3 → 2 — does an exact comparison count it?",
            ),
        ),
    ),
    Question(
        slug="k-th-largest-perfect-subtree-size-in-binary-tree", number=3319, title="K-th Largest Perfect Subtree Size in Binary Tree",
        difficulty="Medium", topics=("trees",),
        summary="A perfect binary tree has every internal node with two children and all leaves on one level. Return the size of the k-th largest perfect subtree, or −1 if there are fewer than k.",
        example="root = [5,3,6,5,2,5,7,1,8,null,null,6,8], k = 2  →  3",
        criterion="Which approach finds every perfect subtree in one pass?",
        hint="If both children are perfect, what else must hold for the parent to be perfect?",
        choices=(
            Choice(
                "Post-order height, then sort sizes", OPTIMAL, time="O(n log n)", space="O(n)", visual="tree-dfs",
                detail="Return a perfect subtree's height (−1 if not); size is 2^(h+1) − 1; sort the sizes.",
                why="A node is perfect exactly when both children are perfect with the same height. Children report that in O(1), so one pass finds them all.",
            ),
            Choice(
                "Check perfectness from every node", SUBOPTIMAL, time="O(n²)", space="O(n)", visual="brute",
                detail="For each node, walk its subtree to test it.",
                why="Correct, but every subtree is re-walked for each ancestor.",
            ),
            Choice(
                "Two children everywhere", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Call a subtree perfect if every internal node has two children.",
                why="Full isn't perfect: both children can exist with leaves at different depths.",
            ),
            Choice(
                "Size of the form 2ᵏ − 1", INCORRECT, time="O(n)", space="O(h)", visual="math",
                detail="Treat any subtree with 1, 3, 7, … nodes as perfect.",
                why="A chain of three nodes has size 3. Is it perfect?",
            ),
        ),
    ),
    Question(
        slug="maximum-product-of-splitted-binary-tree", number=1339, title="Maximum Product of Splitted Binary Tree",
        difficulty="Medium", topics=("trees",),
        summary="Remove one edge to split the tree in two. Maximize the product of the two parts' sums; return it modulo 10⁹ + 7.",
        example="[1, 2, 3, 4, 5, 6]  →  110",
        criterion="Which approach is linear and returns the true maximum?",
        hint="Cutting the edge above a node splits off exactly its subtree. What are the two sums?",
        choices=(
            Choice(
                "Total, then post-order subtree sums", OPTIMAL, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="First get the total T; then maximize s · (T − s) over subtree sums s.",
                why="Every cut separates one subtree with sum s from the rest, T − s. Post-order gives every s once; take the modulo only at the end.",
            ),
            Choice(
                "Recompute both sides per edge", SUBOPTIMAL, time="O(n²)", space="O(h)", visual="brute",
                detail="For each edge, sum both resulting trees.",
                why="Correct, but each cut rescans the tree. All subtree sums come from one pass.",
            ),
            Choice(
                "Compare products after the modulo", INCORRECT, time="O(n)", space="O(h)", visual="math",
                detail="Keep max(s · (T − s) mod 10⁹+7).",
                why="A larger product can wrap around to a smaller remainder. When should the modulo be applied?",
            ),
            Choice(
                "Cut only at the root", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Try the root's two edges.",
                why="The most even split may be deep inside a subtree.",
            ),
        ),
    ),
    Question(
        slug="finish-time-of-tasks-i", number=3965, title="Finish Time of Tasks I",
        difficulty="Medium", topics=("trees",),
        url="https://leetcode.cn/problems/finish-time-of-tasks-i/",
        summary="Tasks form a tree rooted at 0 (edges [parent, child]), each with a base time. A leaf finishes at its base time. Otherwise, with earliest and latest the children's finish times, the task takes (latest − earliest) + base and finishes at latest plus that. Return task 0's finish time.",
        example="edges = [[0,1],[0,2]], baseTime = [4,7,6]  →  12",
        criterion="Which approach is linear?",
        hint="What does a task need from its children before it can compute its own finish time?",
        choices=(
            Choice(
                "Post-order over child lists", OPTIMAL, time="O(n)", space="O(n)", visual="tree-dfs",
                detail="Build child lists; compute children first, then finish = 2·latest − earliest + base.",
                why="A task depends only on its children's finish times, so post-order computes each task once. An explicit stack avoids recursion limits on a 10⁵-deep chain.",
            ),
            Choice(
                "Repeated sweeps", SUBOPTIMAL, time="O(n·h)", space="O(n)", visual="brute",
                detail="Scan all tasks repeatedly, finishing any whose children are all done.",
                why="Correct, but each sweep may finish only one more level. Post-order gets the order right in one pass.",
            ),
            Choice(
                "Latest child plus base", INCORRECT, time="O(n)", space="O(n)", visual="tree-dfs",
                detail="finish = latest + base.",
                why="The task's own duration also grows by latest − earliest. Where did that term go?",
            ),
            Choice(
                "Sum of children's finish times", INCORRECT, time="O(n)", space="O(n)", visual="math",
                detail="finish = sum of children's finish times + base.",
                why="Children run side by side; only the earliest and latest matter. In the example, 7 + 6 + 4 = 17, not 12.",
            ),
        ),
    ),
    Question(
        slug="subtree-of-another-tree", number=572, title="Subtree of Another Tree",
        difficulty="Easy", topics=("trees", "strings"),
        summary="Decide whether subRoot is identical to the subtree rooted at some node of root (that node and all its descendants).",
        example="root = [3, 4, 5, 1, 2], subRoot = [4, 1, 2]  →  true",
        criterion="Which approach is linear in the size of both trees?",
        hint="If both trees were strings that keep their shape, what kind of search is this?",
        choices=(
            Choice(
                "Serialize with null markers, then KMP", OPTIMAL, time="O(m + n)", space="O(m + n)", visual="array-copy",
                detail="Pre-order both with nulls and delimiters; search with KMP.",
                why="Null markers and delimiters make the strings encode shape exactly, so a match is a subtree. KMP finds it in linear time.",
            ),
            Choice(
                "Same-tree check at every node", SUBOPTIMAL, time="O(m·n)", space="O(h)", visual="tree-dfs",
                detail="For each node of root, compare its subtree with subRoot.",
                why="The common answer, and correct, but each node can restart a full comparison.",
            ),
            Choice(
                "In-order strings, substring search", INCORRECT, time="O(m + n)", space="O(m + n)", visual="array-copy",
                detail="Search subRoot's in-order string in root's.",
                why="Without nulls, different shapes give the same in-order string. What does a match prove?",
            ),
            Choice(
                "Compare at the first matching value", INCORRECT, time="O(m + n)", space="O(h)", visual="tree-dfs",
                detail="Find the first node equal to subRoot's root and compare there.",
                why="Values repeat. If the first 4 doesn't match, could a later 4?",
            ),
        ),
    ),
    Question(
        slug="number-of-good-leaf-nodes-pairs", number=1530, title="Number of Good Leaf Nodes Pairs",
        difficulty="Medium", topics=("trees",),
        summary="Count pairs of leaves whose shortest path through the tree has length at most distance (distance ≤ 10).",
        example="root = [1, 2, 3, null, 4], distance = 3  →  1",
        criterion="Which approach uses the small distance bound best?",
        hint="Two leaves meet at their lowest common ancestor. What should each subtree tell that ancestor?",
        choices=(
            Choice(
                "Post-order leaf counts by distance", OPTIMAL, time="O(n·d²)", space="O(h·d)", visual="tree-dfs",
                detail="Each node returns how many leaves sit at each distance ≤ d; pair left and right counts.",
                why="Every pair is counted exactly once, at its lowest common ancestor, by combining two short arrays. The bound d keeps them tiny.",
            ),
            Choice(
                "Every pair through its LCA", SUBOPTIMAL, time="O(L²·h)", space="O(n)", visual="brute",
                detail="For each pair of leaves, find the LCA and the path length.",
                why="Correct, but the number of leaf pairs grows quadratically.",
            ),
            Choice(
                "BFS from every leaf", SUBOPTIMAL, time="O(L·n)", space="O(n)", visual="graph-bfs",
                detail="Treat the tree as a graph; BFS d steps from each leaf.",
                why="Correct, but each leaf explores its neighbourhood again. Combining counts at ancestors shares the work.",
            ),
            Choice(
                "Pairs of sibling leaves", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Count leaves that share a parent.",
                why="Siblings are at distance 2, but larger distances are allowed. What about cousins?",
            ),
        ),
    ),
    Question(
        slug="lcp-67-decorate-tree", number=None, title="Decorate the Tree",
        difficulty="Medium", topics=("trees",),
        ref="LCP 67", url="https://leetcode.cn/problems/KnLfVT/",
        summary="Insert a light (a node with value −1) on every parent–child edge of a binary tree. A light between x and its left child becomes x's left child, with the old child as the light's left child; the same on the right. Return the root.",
        example="[7, 5, 6]  →  [7, −1, −1, 5, null, null, 6]",
        criterion="Which approach is linear?",
        hint="For one node, what does decorating its left edge look like? Does that depend on anything below?",
        choices=(
            Choice(
                "Recurse, wrapping each child in a light", OPTIMAL, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="node.left = Light(left = decorate(node.left)); same on the right.",
                why="Each edge gets exactly one light, and decorating a subtree doesn't depend on anything above it. One visit per node.",
            ),
            Choice(
                "Walk from the root for every edge", SUBOPTIMAL, time="O(n·h)", space="O(h)", visual="brute",
                detail="For each original node, find its parent from the root and splice a light in.",
                why="Correct, but each splice repeats a walk down the tree. Recursion is already standing on the parent.",
            ),
            Choice(
                "Lights above leaves only", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Insert a light only between each leaf and its parent.",
                why="Every node with a parent gets a light, not just the leaves.",
            ),
            Choice(
                "Also wrap the root", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Put a light above the root as well.",
                why="The root has no parent, and the decorated root must keep the original value.",
            ),
        ),
    ),
    Question(
        slug="count-univalue-subtrees", number=250, title="Count Univalue Subtrees",
        difficulty="Medium", topics=("trees",),
        summary="Count subtrees (a node with all its descendants) in which every node has the same value.",
        example="[5, 1, 5, 5, 5, null, 5]  →  4",
        criterion="Which approach is linear with O(h) extra space?",
        hint="When is a node's subtree univalue, given its children's answers?",
        choices=(
            Choice(
                "Post-order, check both children", OPTIMAL, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Evaluate both children first; uni if both are uni and match the node's value.",
                why="Children report whether they're univalue, so the parent decides in O(1). Evaluating both before combining counts every subtree.",
            ),
            Choice(
                "Check every subtree from scratch", SUBOPTIMAL, time="O(n²)", space="O(h)", visual="brute",
                detail="For each node, walk its subtree comparing values.",
                why="Correct, but deep nodes are rechecked for every ancestor.",
            ),
            Choice(
                "Combine with a short-circuit and", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="return uni(left) and uni(right) and values match.",
                why="If the left side fails, the right call never runs — and its univalue subtrees never get counted.",
            ),
            Choice(
                "Count the leaves", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Every leaf is univalue; return the leaf count.",
                why="Leaves count, but so do larger subtrees like 5 → 5. What about those?",
            ),
        ),
    ),
    Question(
        slug="count-nodes-equal-to-sum-of-descendants", number=1973, title="Count Nodes Equal to Sum of Descendants",
        difficulty="Medium", topics=("trees",),
        summary="Count nodes whose value equals the sum of all their descendants' values (0 if they have none).",
        example="[10, 3, 4, 2, 1]  →  2",
        criterion="Which approach is linear with O(h) extra space?",
        hint="What should a child return so its parent knows the sum of everything below it?",
        choices=(
            Choice(
                "Post-order returning subtree sums", OPTIMAL, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Descendant sum = left sum + right sum; compare with val; return it + val.",
                why="The children's subtree sums are exactly the descendants' sum. One pass, constant work per node.",
            ),
            Choice(
                "Sum descendants at every node", SUBOPTIMAL, time="O(n²)", space="O(h)", visual="brute",
                detail="For each node, traverse below it to sum.",
                why="Correct, but deep nodes are added again for every ancestor.",
            ),
            Choice(
                "Compare with the children's values", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Count nodes where val = left.val + right.val.",
                why="Descendants include grandchildren and beyond. In 10 → 3 → (2, 1), does 10 equal 3 + its other child alone?",
            ),
            Choice(
                "Compare with the subtree sum", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Count nodes where val equals the sum including itself.",
                why="A sum that already contains val only equals val when the descendants add to 0.",
            ),
        ),
    ),
    Question(
        slug="equal-tree-partition", number=663, title="Equal Tree Partition",
        difficulty="Medium", topics=("trees",),
        summary="Decide whether removing exactly one edge can split the tree into two parts with equal sums. Values may be negative.",
        example="[5, 10, 10, null, null, 2, 3]  →  true",
        criterion="Which approach is linear and handles a total of 0 correctly?",
        hint="Which subtree sums correspond to an edge you can actually cut?",
        choices=(
            Choice(
                "Subtree sums except the root's", OPTIMAL, time="O(n)", space="O(n)", visual="hashmap",
                detail="Post-order every subtree sum, leaving out the whole tree's; check total/2 is among them.",
                why="Each cut separates a non-root subtree. Leaving out the root's sum matters when the total is 0, because there is no edge above the root.",
            ),
            Choice(
                "Recompute both sides per edge", SUBOPTIMAL, time="O(n²)", space="O(h)", visual="brute",
                detail="For each edge, sum both parts.",
                why="Correct, but each cut rescans the tree.",
            ),
            Choice(
                "All subtree sums, root included", INCORRECT, time="O(n)", space="O(n)", visual="hashmap",
                detail="Check whether total/2 appears among every subtree sum.",
                why="When the total is 0, the root's own sum 0 equals total/2. Which edge would you cut?",
            ),
            Choice(
                "Try the root's two edges", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Check only whether a child of the root has sum total/2.",
                why="The right cut can be deep in the tree, as in the example.",
            ),
        ),
    ),
    Question(
        slug="maximum-average-subtree", number=1120, title="Maximum Average Subtree",
        difficulty="Medium", topics=("trees",),
        summary="Return the maximum average value over all subtrees (a node with all its descendants).",
        example="[5, 6, 1]  →  6.0",
        criterion="Which approach is linear with O(h) extra space?",
        hint="What two numbers about a subtree combine cleanly with its sibling's?",
        choices=(
            Choice(
                "Post-order returning (sum, count)", OPTIMAL, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Combine sums and counts; track the best sum / count.",
                why="Sums and counts add across children, so each average comes in O(1). One pass covers every subtree.",
            ),
            Choice(
                "Recompute each subtree", SUBOPTIMAL, time="O(n²)", space="O(h)", visual="brute",
                detail="For each node, traverse its subtree to average it.",
                why="Correct, but nodes are recounted for every ancestor.",
            ),
            Choice(
                "Average of the children's averages", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Combine (val + avg(left) + avg(right)) / 3.",
                why="Subtrees of different sizes can't be averaged like that. A 1-node and a 9-node subtree shouldn't weigh the same.",
            ),
            Choice(
                "Largest value in the tree", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Return the maximum node value.",
                why="Only leaves stand alone as subtrees. In [10, 1], can 10 be averaged without 1?",
            ),
        ),
    ),
    Question(
        slug="count-nodes-that-are-great-enough", number=2792, title="Count Nodes That Are Great Enough",
        difficulty="Hard", topics=("trees", "data-structures"),
        summary="A node is great enough if its subtree has at least k nodes and its value is greater than the values of at least k nodes in its subtree. Count such nodes (k ≤ 10).",
        example="root = [7, 6, 5, 4, 3, 2, 1], k = 2  →  3",
        criterion="Which approach uses the small k best?",
        hint="To beat at least k values, which values of the subtree do you actually need to know?",
        choices=(
            Choice(
                "Post-order keeping the k smallest", OPTIMAL, time="O(n·k log k)", space="O(h·k)", visual="heap",
                detail="Each subtree returns its k smallest values (merge children's, add own, trim to k).",
                why="Beating k values means beating the k-th smallest. Merging two short lists per node keeps that information at O(k) size.",
            ),
            Choice(
                "Collect and sort every subtree", SUBOPTIMAL, time="O(n² log n)", space="O(n)", visual="sort",
                detail="For each node, gather all its subtree's values and sort them.",
                why="Correct, but each value is copied once per ancestor. Only the k smallest ever matter.",
            ),
            Choice(
                "Compare with the children only", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Great enough if val beats its children.",
                why="It needs to beat k values anywhere in its subtree — and the subtree must have at least k nodes.",
            ),
            Choice(
                "Node is its subtree's maximum", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Count nodes larger than everything below, with size ≥ k.",
                why="It only has to beat k values, not all of them.",
            ),
        ),
    ),
    Question(
        slug="largest-bst-subtree", number=333, title="Largest BST Subtree",
        difficulty="Medium", topics=("trees",),
        summary="Return the size of the largest subtree (a node with all its descendants) that is a valid binary search tree.",
        example="[10, 5, 15, 1, 8, null, 7]  →  3",
        criterion="Which approach is linear?",
        hint="What must a parent know about each child subtree to decide whether it is a BST?",
        choices=(
            Choice(
                "Post-order (isBST, min, max, size)", OPTIMAL, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="A node is a BST if both children are and left.max < val < right.min.",
                why="The children's min, max and size are all the parent needs, so each node is decided in O(1).",
            ),
            Choice(
                "Validate from every node", SUBOPTIMAL, time="O(n²)", space="O(h)", visual="brute",
                detail="Run a BST check on each node's subtree.",
                why="Correct, but every subtree is revalidated for each ancestor.",
            ),
            Choice(
                "Parent–child ordering only", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Count subtrees where every left child < parent < right child.",
                why="A node deep in the right subtree must still exceed the root. Do local checks see that?",
            ),
            Choice(
                "Longest increasing run in-order", INCORRECT, time="O(n)", space="O(n)", visual="array-copy",
                detail="Take the longest strictly increasing stretch of the in-order list.",
                why="An increasing stretch can mix nodes from different subtrees. Is it one subtree?",
            ),
        ),
    ),
    Question(
        slug="find-leaves-of-binary-tree", number=366, title="Find Leaves of Binary Tree",
        difficulty="Medium", topics=("trees",),
        summary="Repeatedly collect and remove all leaves until the tree is empty. Return the groups in removal order.",
        example="[1, 2, 3, 4, 5]  →  [[4, 5, 3], [2], [1]]",
        criterion="Which approach is linear without modifying the tree?",
        hint="In which round is a node removed, in terms of its children?",
        choices=(
            Choice(
                "Group by height (leaf = 0)", OPTIMAL, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Post-order height = 1 + max(children); append the node to group[height].",
                why="A node is removed one round after its last child, so its round is its height. One pass places every node.",
            ),
            Choice(
                "Simulate the rounds", SUBOPTIMAL, time="O(n·h)", space="O(h)", visual="brute",
                detail="Each round, find and detach the current leaves.",
                why="Correct, but every round rescans the tree — and it destroys it.",
            ),
            Choice(
                "Group by depth, deepest first", INCORRECT, time="O(n)", space="O(w)", visual="tree-bfs",
                detail="Level order, then reverse the levels.",
                why="Node 3 is at depth 1 but it's a leaf, so it goes in the first round. Does depth decide the round?",
            ),
            Choice(
                "Group by subtree size", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Order nodes by how many descendants they have.",
                why="A node above two leaves and a node above a single leaf are both removed in round 2, yet their sizes differ.",
            ),
        ),
    ),
    Question(
        slug="binary-tree-upside-down", number=156, title="Binary Tree Upside Down",
        difficulty="Medium", topics=("trees",),
        summary="Every right node is a leaf with a left sibling, or empty. Turn the tree upside down: each left child becomes the parent, its old parent the new right child, and the old right sibling the new left child.",
        example="[1, 2, 3, 4, 5]  →  [4, 5, 2, null, null, 3, 1]",
        criterion="Which approach uses O(1) extra space?",
        hint="Walk down the left spine. At each step, which three pointers need to change?",
        choices=(
            Choice(
                "Iterative relink down the left spine", OPTIMAL, time="O(n)", space="O(1)", visual="linked-list",
                detail="Track prev and prevRight; set node.left = prevRight, node.right = prev.",
                why="Like reversing a linked list along the left spine, carrying the old right sibling along. Only a few pointers are needed.",
            ),
            Choice(
                "Recursive relink", SUBOPTIMAL, time="O(n)", space="O(h)", visual="recursion",
                detail="Recurse to the leftmost node, then relink on the way back.",
                why="Correct and natural, but the recursion stack holds the whole left spine.",
            ),
            Choice(
                "Mirror the tree", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Swap the children of every node.",
                why="Mirroring keeps the root at the top. The leftmost node is supposed to become the new root.",
            ),
            Choice(
                "Repeated right rotations at the root", INCORRECT, time="O(n)", space="O(1)", visual="tree-dfs",
                detail="Rotate right until the leftmost node is at the top.",
                why="A right rotation moves 2's old right child under 1. In the upside-down tree, which nodes become 2's children?",
            ),
        ),
    ),
    Question(
        slug="check-if-two-expression-trees-are-equivalent", number=1612, title="Check If Two Expression Trees are Equivalent",
        difficulty="Medium", topics=("trees",),
        summary="Two expression trees use only '+' and single-letter variables. Decide whether they evaluate to the same value for every assignment of the variables.",
        example="a + (b + c)  and  (b + c) + a  →  true",
        criterion="Which approach is linear and always right?",
        hint="With only addition, what does an expression's value depend on?",
        choices=(
            Choice(
                "Count each variable's leaves", OPTIMAL, time="O(n)", space="O(h)", visual="counting",
                detail="Tally letters at the leaves of both trees and compare the 26 counts.",
                why="Addition is commutative and associative, so the value depends only on how many times each variable appears.",
            ),
            Choice(
                "Sort the leaves and compare", SUBOPTIMAL, time="O(n log n)", space="O(n)", visual="sort",
                detail="Collect both leaf lists, sort, compare.",
                why="Correct, but with only 26 letters, counting does the same without sorting.",
            ),
            Choice(
                "Structural match with child swaps", INCORRECT, time="O(n)", space="O(h)", visual="tree-dfs",
                detail="Equal if the trees match, allowing children to be swapped.",
                why="a + (b + c) and (a + b) + c are equal, but no swap turns one shape into the other.",
            ),
            Choice(
                "Evaluate on random values", INCORRECT, time="O(n)", space="O(h)", visual="math",
                detail="Assign random numbers to variables and compare the results.",
                why="Different expressions can agree on a particular assignment. Can a few trials prove equality?",
            ),
        ),
    ),
]
