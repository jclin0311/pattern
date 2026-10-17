"""Core route step 5: grid DFS (网格图 §1)."""

from .question_schema import INCORRECT, OPTIMAL, SUBOPTIMAL, Choice, Question

QUESTIONS = [
    Question(
        slug="max-area-of-island", number=695, title="Max Area of Island",
        difficulty="Medium", topics=("grid",),
        summary="In a grid of 0s (water) and 1s (land), return the number of cells in the largest island (4-directionally connected land), or 0.",
        example="[[1,1,0],[0,1,0],[0,0,1]]  →  3",
        criterion="Which approach is linear in the grid size?",
        hint="When you step onto unvisited land, how do you measure its whole island at once?",
        choices=(
            Choice(
                "Flood fill returning the area", OPTIMAL, time="O(m·n)", space="O(m·n)", visual="graph-dfs",
                detail="DFS from each unvisited land cell, marking cells and adding up their count.",
                why="Each island is one connected component. Marking cells as you go means every cell is counted once, by exactly one flood fill.",
            ),
            Choice(
                "Flood fill per cell, no global marks", SUBOPTIMAL, time="O((m·n)²)", space="O(m·n)", visual="brute",
                detail="From every land cell, explore its island from scratch.",
                why="Correct, but every cell of a big island re-explores the whole island.",
            ),
            Choice(
                "Count all land cells", INCORRECT, time="O(m·n)", space="O(1)", visual="counting",
                detail="Return the number of 1s.",
                why="Two separate islands of 3 cells would give 6. Is that one island?",
            ),
            Choice(
                "Longest run in a row or column", INCORRECT, time="O(m·n)", space="O(1)", visual="matrix",
                detail="Find the longest straight line of 1s.",
                why="Islands bend. An L-shape of 3 cells has no straight run of 3.",
            ),
        ),
    ),
    Question(
        slug="count-islands-with-total-value-divisible-by-k", number=3619, title="Count Islands With Total Value Divisible by K",
        difficulty="Medium", topics=("grid",),
        summary="Cells hold non-negative integers; positive cells are land, 4-directionally connected into islands. Count islands whose total value is divisible by k.",
        example="[[2,3,0],[0,0,4],[1,0,6]], k = 5  →  2",
        criterion="Which approach is linear in the grid size?",
        hint="What one number does each island need to report?",
        choices=(
            Choice(
                "Flood fill summing values", OPTIMAL, time="O(m·n)", space="O(m·n)", visual="graph-dfs",
                detail="DFS each unvisited island, add its values, check sum % k == 0.",
                why="The test is on the island's total, so each island must be gathered whole. One flood fill per island visits each cell once.",
            ),
            Choice(
                "Re-explore the island from every cell", SUBOPTIMAL, time="O((m·n)²)", space="O(m·n)", visual="brute",
                detail="For each land cell, flood fill its island and test it, deduplicating islands.",
                why="Correct after deduplication, but big islands are explored once per cell.",
            ),
            Choice(
                "Count cells divisible by k", INCORRECT, time="O(m·n)", space="O(1)", visual="counting",
                detail="Count land cells whose own value is a multiple of k.",
                why="2 and 3 aren't multiples of 5, but together they make an island worth 5.",
            ),
            Choice(
                "Sum each row's land runs", INCORRECT, time="O(m·n)", space="O(1)", visual="matrix",
                detail="Treat each horizontal run of land as an island.",
                why="In the example, 4 and 6 are stacked vertically. Are they separate islands?",
            ),
        ),
    ),
    Question(
        slug="maximum-number-of-fish-in-a-grid", number=2658, title="Maximum Number of Fish in a Grid",
        difficulty="Medium", topics=("grid",),
        summary="Cells are land (0) or water holding that many fish. A fisher starts on any water cell, catches every fish there and may move to adjacent water cells. Return the most fish one fisher can catch.",
        example="[[0,2,1,0],[4,0,0,3],[1,0,0,4],[0,3,2,0]]  →  7",
        criterion="Which approach is linear in the grid size?",
        hint="Once the fisher is in a connected water region, what can they reach?",
        choices=(
            Choice(
                "Flood fill summing each region", OPTIMAL, time="O(m·n)", space="O(m·n)", visual="graph-dfs",
                detail="DFS each unvisited water region; keep the largest fish total.",
                why="The fisher can sweep a whole connected water region, so the answer is the best region total. One flood fill per region.",
            ),
            Choice(
                "Re-explore from every water cell", SUBOPTIMAL, time="O((m·n)²)", space="O(m·n)", visual="brute",
                detail="Start a fresh search from each water cell.",
                why="Correct, but every cell of a region recomputes the same total.",
            ),
            Choice(
                "Richest single cell", INCORRECT, time="O(m·n)", space="O(1)", visual="counting",
                detail="Return the largest cell value.",
                why="The fisher can keep moving to adjacent water. Why stop at one cell?",
            ),
            Choice(
                "All the fish in the grid", INCORRECT, time="O(m·n)", space="O(1)", visual="counting",
                detail="Sum every water cell.",
                why="Land separates regions. Can the fisher cross it?",
            ),
        ),
    ),
    Question(
        slug="pond-sizes-lcci", number=None, title="Pond Sizes",
        difficulty="Medium", topics=("grid",),
        ref="面试题 16.19", url="https://leetcode.cn/problems/pond-sizes-lcci/",
        summary="In a terrain matrix, 0 is water. Water cells touching horizontally, vertically or diagonally form a pond. Return every pond's size in ascending order.",
        example="[[0,2,1,0],[0,1,0,1],[1,1,0,1],[0,1,0,1]]  →  [1, 2, 4]",
        criterion="Which approach is correct and linear in the grid size (plus sorting the sizes)?",
        hint="How many neighbours does a cell have here?",
        choices=(
            Choice(
                "8-direction flood fill, then sort", OPTIMAL, time="O(m·n + p log p)", space="O(m·n)", visual="graph-dfs",
                detail="Fill each unvisited pond through all 8 neighbours; collect sizes and sort them.",
                why="Diagonal contact joins ponds, so each fill must look in 8 directions. Every cell is visited once; only the p sizes get sorted.",
            ),
            Choice(
                "4-direction flood fill", INCORRECT, time="O(m·n)", space="O(m·n)", visual="graph-dfs",
                detail="Fill through up, down, left and right only.",
                why="In the example, (0,3) and (1,2) touch only at a corner. Are they one pond?",
            ),
            Choice(
                "Re-explore from every water cell", SUBOPTIMAL, time="O((m·n)²)", space="O(m·n)", visual="brute",
                detail="Start a fresh search at each 0 and deduplicate ponds.",
                why="Correct after deduplication, but each pond is explored once per cell.",
            ),
            Choice(
                "Count zeros per row", INCORRECT, time="O(m·n)", space="O(1)", visual="matrix",
                detail="Treat each row's water cells as one pond.",
                why="Ponds span rows, and two zeros in one row can belong to different ponds.",
            ),
        ),
    ),
    Question(
        slug="lcs-03-theme-spaces", number=None, title="Theme Spaces",
        difficulty="Medium", topics=("grid",),
        ref="LCS 03", url="https://leetcode.cn/problems/YesdPw/",
        summary="A venue grid uses '0' for corridors and '1'–'5' for theme spaces; same-character cells connected up, down, left or right form one space. Everything outside the grid is corridor. Return the largest area of a space not adjacent to any corridor, or 0.",
        example="[\"110\", \"231\", \"221\"]  →  1",
        criterion="Which approach is correct and linear?",
        hint="A space is disqualified by any one of its cells. Can you stop at that cell?",
        choices=(
            Choice(
                "Flood fill, flag corridor contact", OPTIMAL, time="O(m·n)", space="O(m·n)", visual="graph-dfs",
                detail="Fill each same-character space fully; mark it if any cell touches '0' or the edge; keep the best unmarked area.",
                why="The whole space must be filled even after contact is found, so its cells aren't revisited as a new space later.",
            ),
            Choice(
                "Ignore the outside", INCORRECT, time="O(m·n)", space="O(m·n)", visual="graph-dfs",
                detail="Disqualify a space only when it touches a '0' cell.",
                why="Outside the grid is corridor too. What about spaces on the edge?",
            ),
            Choice(
                "Stop at the first corridor contact", INCORRECT, time="O(m·n)", space="O(m·n)", visual="graph-dfs",
                detail="Abandon the fill as soon as a cell touches a corridor.",
                why="The unvisited rest of that space is found later as if it were a separate, clean space.",
            ),
            Choice(
                "Join all non-corridor cells", INCORRECT, time="O(m·n)", space="O(m·n)", visual="graph-dfs",
                detail="Treat every non-'0' cell as part of one connected area regardless of character.",
                why="A '2' next to a '3' belongs to a different space.",
            ),
        ),
    ),
    Question(
        slug="island-perimeter", number=463, title="Island Perimeter",
        difficulty="Easy", topics=("grid",),
        summary="A grid contains exactly one island of 1s with no lakes inside. Return the island's perimeter.",
        example="[[0,1,0,0],[1,1,1,0],[0,1,0,0],[1,1,0,0]]  →  16",
        criterion="Which approach is linear with O(1) extra space?",
        hint="Each land cell has 4 edges. When does an edge stop counting?",
        choices=(
            Choice(
                "Count cells and shared edges", OPTIMAL, time="O(m·n)", space="O(1)", visual="counting",
                detail="perimeter = 4·land − 2·(land pairs sharing an edge), checking right and down neighbours.",
                why="Every shared edge hides one side of each of its two cells. A single scan counts both quantities without any traversal.",
            ),
            Choice(
                "DFS counting edges to water", SUBOPTIMAL, time="O(m·n)", space="O(m·n)", visual="graph-dfs",
                detail="Flood fill the island; add one for each neighbour that is water or off-grid.",
                why="Correct, but the recursion and visited marks cost O(m·n) space. Do you need connectivity at all when there is only one island?",
            ),
            Choice(
                "4 × number of land cells", INCORRECT, time="O(m·n)", space="O(1)", visual="counting",
                detail="Each cell contributes 4.",
                why="Two adjacent cells share an edge that isn't on the outside.",
            ),
            Choice(
                "Bounding-box perimeter", INCORRECT, time="O(m·n)", space="O(1)", visual="matrix",
                detail="Return 2·(width + height) of the island's bounding box.",
                why="A plus shape has the same bounding box as a full square but more edge. Does the box see the notches?",
            ),
        ),
    ),
    Question(
        slug="flood-fill", number=733, title="Flood Fill",
        difficulty="Easy", topics=("grid",),
        summary="Recolor the starting pixel and every pixel 4-directionally connected to it with the same original color. Return the image.",
        example="[[1,1,1],[1,1,0],[1,0,1]], start (1,1), color 2  →  [[2,2,2],[2,2,0],[2,0,1]]",
        criterion="Which approach is correct and linear?",
        hint="What happens if the new color equals the old one?",
        choices=(
            Choice(
                "DFS recolor; exit if colors are equal", OPTIMAL, time="O(m·n)", space="O(m·n)", visual="graph-dfs",
                detail="If the original equals the new color return; else recolor matching neighbours recursively.",
                why="Recoloring marks a pixel as visited. The early exit matters because when the colors are equal, recolored pixels still match.",
            ),
            Choice(
                "DFS recolor without the check", INCORRECT, time="O(m·n)", space="O(m·n)", visual="graph-dfs",
                detail="Recolor and recurse into neighbours with the original color.",
                why="With new color = old color, every recolored pixel still looks unvisited. When does the search stop?",
            ),
            Choice(
                "Recolor every original-colored pixel", INCORRECT, time="O(m·n)", space="O(1)", visual="matrix",
                detail="Scan the image and change all pixels of that color.",
                why="Pixels of the same color elsewhere aren't connected to the start. Should they change?",
            ),
            Choice(
                "Sweep until nothing changes", SUBOPTIMAL, time="O((m·n)²)", space="O(1)", visual="brute",
                detail="Repeatedly recolor pixels next to recolored ones.",
                why="Correct, but each sweep may only grow the region by one step. A search grows it all at once.",
            ),
        ),
    ),
    Question(
        slug="coloring-a-border", number=1034, title="Coloring A Border",
        difficulty="Medium", topics=("grid",),
        summary="Take the 4-directionally connected component of grid[row][col] (same color). Its border is the cells adjacent to a cell outside the component or on the grid edge. Color the border and return the grid.",
        example="[[1,1],[1,2]], row 0, col 0, color 3  →  [[3,3],[3,2]]",
        criterion="Which approach is correct and linear?",
        hint="If you recolor a cell while still exploring, what will its neighbours think?",
        choices=(
            Choice(
                "DFS with visited, recolor afterwards", OPTIMAL, time="O(m·n)", space="O(m·n)", visual="graph-dfs",
                detail="Explore the component, collect border cells, then recolor them all at the end.",
                why="The border test compares against the original colors, so it must finish before anything changes. Collect first, paint second.",
            ),
            Choice(
                "Recolor during the DFS", INCORRECT, time="O(m·n)", space="O(m·n)", visual="graph-dfs",
                detail="Paint border cells as soon as you find them.",
                why="An interior cell next to a freshly painted cell now sees a different color and looks like border too.",
            ),
            Choice(
                "Color the whole component", INCORRECT, time="O(m·n)", space="O(m·n)", visual="graph-dfs",
                detail="Paint every cell of the component.",
                why="Only the border should change. What about the interior cells?",
            ),
            Choice(
                "Color component cells on the grid edge", INCORRECT, time="O(m·n)", space="O(m·n)", visual="matrix",
                detail="Paint only cells in the outermost rows and columns.",
                why="Cells next to a different color are border too, even in the middle of the grid.",
            ),
        ),
    ),
    Question(
        slug="number-of-enclaves", number=1020, title="Number of Enclaves",
        difficulty="Medium", topics=("grid",),
        summary="Count land cells from which you cannot walk off the grid by moving 4-directionally through land.",
        example="[[0,0,0,0],[1,0,1,0],[0,1,1,0],[0,0,0,0]]  →  3",
        criterion="Which approach is linear in the grid size?",
        hint="Instead of asking whether each cell can escape, which cells can you prove escape?",
        choices=(
            Choice(
                "Flood fill from border land", OPTIMAL, time="O(m·n)", space="O(m·n)", visual="graph-dfs",
                detail="Sink all land connected to the edge; count the land that remains.",
                why="A cell escapes exactly when it's connected to edge land. Starting from the edge marks all of them in one sweep.",
            ),
            Choice(
                "Search from every land cell", SUBOPTIMAL, time="O((m·n)²)", space="O(m·n)", visual="brute",
                detail="For each land cell, DFS to see whether it reaches the edge.",
                why="Correct, but cells of the same island repeat the same search.",
            ),
            Choice(
                "Land not on the edge", INCORRECT, time="O(m·n)", space="O(1)", visual="matrix",
                detail="Count land cells outside the outer ring.",
                why="An interior cell connected to edge land can still walk off.",
            ),
            Choice(
                "Islands that don't touch the edge", INCORRECT, time="O(m·n)", space="O(m·n)", visual="graph-dfs",
                detail="Count enclosed islands.",
                why="The question counts cells, not islands.",
            ),
        ),
    ),
    Question(
        slug="maximum-number-of-moves-in-a-grid", number=2684, title="Maximum Number of Moves in a Grid",
        difficulty="Medium", topics=("grid", "dp"),
        summary="Start at any cell in the first column. From (r, c) you may move to (r−1, c+1), (r, c+1) or (r+1, c+1) if that cell's value is strictly larger. Return the most moves possible.",
        example="[[2,4,3,5],[5,4,9,3],[3,4,2,11],[10,9,13,15]]  →  3",
        criterion="Which approach is linear in the grid size with O(m) extra space?",
        hint="Moves always go one column right. What do you need to know about column c to fill in column c + 1?",
        choices=(
            Choice(
                "Sweep columns of reachable cells", OPTIMAL, time="O(m·n)", space="O(m)", visual="dp-1d",
                detail="Track which cells of the current column are reachable; derive the next column; stop when none are.",
                why="Every move advances one column, so reachability spreads column by column. The last column with a reachable cell is the answer.",
            ),
            Choice(
                "DFS with memo", SUBOPTIMAL, time="O(m·n)", space="O(m·n)", visual="graph-dfs",
                detail="Longest path from each cell, cached in an m×n table.",
                why="Correct and linear, but the cache and recursion use O(m·n) space.",
            ),
            Choice(
                "DFS from every start, no memo", SUBOPTIMAL, time="O(m·3ⁿ)", space="O(n)", visual="brute",
                detail="Try every path from each first-column cell.",
                why="Correct, but paths branch three ways per step. Many reach the same cell repeatedly.",
            ),
            Choice(
                "Greedy: smallest larger neighbour", INCORRECT, time="O(m + n)", space="O(1)", visual="greedy",
                detail="Always step to the smallest strictly larger option.",
                why="A small step now can lead into a dead end that a bigger step avoids.",
            ),
        ),
    ),
    Question(
        slug="number-of-closed-islands", number=1254, title="Number of Closed Islands",
        difficulty="Medium", topics=("grid",),
        summary="Here 0 is land and 1 is water. A closed island is a group of land cells completely surrounded by water, so it never touches the grid edge. Count closed islands.",
        example="[[1,1,1,1,1,1,1,0],[1,0,0,0,0,1,1,0],[1,0,1,0,1,1,1,0],[1,0,0,0,0,1,0,1],[1,1,1,1,1,1,1,0]]  →  2",
        criterion="Which approach is correct and linear?",
        hint="If a search stops the moment it touches the edge, what happens to the rest of that island?",
        choices=(
            Choice(
                "Sink edge islands, then count", OPTIMAL, time="O(m·n)", space="O(m·n)", visual="graph-dfs",
                detail="Flood fill land touching the edge first; every remaining island is closed.",
                why="Removing edge-connected land leaves only closed islands, which a normal island count then finds — each cell visited a constant number of times.",
            ),
            Choice(
                "DFS that stops at the edge", INCORRECT, time="O(m·n)", space="O(m·n)", visual="graph-dfs",
                detail="Return false as soon as the search reaches the edge.",
                why="Stopping early leaves part of that island unmarked. Later it's found again and may be miscounted as a closed island.",
            ),
            Choice(
                "Check only the starting cell", INCORRECT, time="O(m·n)", space="O(m·n)", visual="graph-dfs",
                detail="Count islands whose first-found cell isn't on the edge.",
                why="An island can start inside and still reach the edge further along.",
            ),
            Choice(
                "Re-explore per land cell", SUBOPTIMAL, time="O((m·n)²)", space="O(m·n)", visual="brute",
                detail="For each land cell, BFS its whole island and test whether it touches the edge.",
                why="Correct after deduplication, but large islands are explored many times.",
            ),
        ),
    ),
    Question(
        slug="surrounded-regions", number=130, title="Surrounded Regions",
        difficulty="Medium", topics=("grid",),
        summary="Capture every region of 'O' cells that is completely surrounded by 'X' by flipping it to 'X'. Regions connected to the edge stay.",
        example="[[\"X\",\"X\",\"X\",\"X\"],[\"X\",\"O\",\"O\",\"X\"],[\"X\",\"X\",\"O\",\"X\"],[\"X\",\"O\",\"X\",\"X\"]]  →  only the edge O at (3,1) remains",
        criterion="Which approach is linear in the grid size?",
        hint="Which 'O' cells are definitely safe?",
        choices=(
            Choice(
                "Mark edge-connected O's, flip the rest", OPTIMAL, time="O(m·n)", space="O(m·n)", visual="graph-dfs",
                detail="Flood fill from every edge 'O'; then flip unmarked 'O' to 'X'.",
                why="A region survives exactly when it touches the edge. Marking from the edge finds every survivor in one sweep.",
            ),
            Choice(
                "Search from every O", SUBOPTIMAL, time="O((m·n)²)", space="O(m·n)", visual="brute",
                detail="For each 'O', DFS to see if it reaches the edge.",
                why="Correct, but cells of one region repeat the same search.",
            ),
            Choice(
                "Flip every interior O", INCORRECT, time="O(m·n)", space="O(1)", visual="matrix",
                detail="Change all 'O' not on the outer ring.",
                why="An interior 'O' connected to an edge 'O' isn't surrounded.",
            ),
            Choice(
                "Flip O's with X on all four sides", INCORRECT, time="O(m·n)", space="O(1)", visual="matrix",
                detail="Change an 'O' if its four neighbours are 'X'.",
                why="A surrounded region of two 'O's has an 'O' neighbour each. Would either flip?",
            ),
        ),
    ),
    Question(
        slug="count-sub-islands", number=1905, title="Count Sub Islands",
        difficulty="Medium", topics=("grid",),
        summary="Given two grids of the same size, count the islands in grid2 whose every cell is also land in grid1.",
        example="grid1 = [[1,1],[0,1]], grid2 = [[1,0],[0,1]]  →  2",
        criterion="Which approach is correct and linear?",
        hint="To mark an island as visited, how much of it must the search cover?",
        choices=(
            Choice(
                "Flood fill each grid2 island fully", OPTIMAL, time="O(m·n)", space="O(m·n)", visual="graph-dfs",
                detail="Visit every cell of the island; it's a sub-island if no cell is water in grid1.",
                why="The search keeps going after a bad cell so the whole island is marked, and records whether any cell failed.",
            ),
            Choice(
                "Stop at the first bad cell", INCORRECT, time="O(m·n)", space="O(m·n)", visual="graph-dfs",
                detail="Return false as soon as a cell is water in grid1.",
                why="The unvisited rest of that island gets found again later — and may be counted as its own sub-island.",
            ),
            Choice(
                "Overlaps grid1 land", INCORRECT, time="O(m·n)", space="O(m·n)", visual="graph-dfs",
                detail="Count grid2 islands with at least one cell on grid1 land.",
                why="Overlap isn't containment. Every cell must be land in grid1.",
            ),
            Choice(
                "Islands of grid1 AND grid2", INCORRECT, time="O(m·n)", space="O(m·n)", visual="matrix",
                detail="Count islands in the cellwise AND of the two grids.",
                why="The AND can cut one grid2 island into pieces and count each. Is a cut-up island a sub-island?",
            ),
        ),
    ),
    Question(
        slug="minesweeper", number=529, title="Minesweeper",
        difficulty="Medium", topics=("grid",),
        summary="Apply one click to a Minesweeper board: a mine becomes 'X'; an empty cell shows its count of adjacent mines (8 directions), or, if that is 0, becomes 'B' and reveals its neighbours recursively.",
        example="click (3, 0) on a 4×5 board with one mine at (1, 2)  →  everything revealed except the cells boxed in by the 1s",
        criterion="Which approach reveals exactly the right cells with the least work?",
        hint="Which revealed cells keep the cascade going?",
        choices=(
            Choice(
                "DFS that expands only from blanks", OPTIMAL, time="O(m·n)", space="O(m·n)", visual="graph-dfs",
                detail="Count adjacent mines; if 0 mark 'B' and recurse into unrevealed neighbours, else write the digit.",
                why="Only zero-count cells open their neighbours, which is the game's rule. Each cell is counted and revealed at most once.",
            ),
            Choice(
                "Also expand from numbered cells", INCORRECT, time="O(m·n)", space="O(m·n)", visual="graph-dfs",
                detail="Recurse into the neighbours of every revealed cell.",
                why="A numbered cell borders a mine. If it opened its neighbours, what might get revealed?",
            ),
            Choice(
                "Reveal every non-mine cell", INCORRECT, time="O(m·n)", space="O(1)", visual="matrix",
                detail="Replace all 'E' with digits or 'B'.",
                why="Cells walled off by numbered cells stay hidden after a click.",
            ),
            Choice(
                "Precompute all mine counts first", SUBOPTIMAL, time="O(m·n)", space="O(m·n)", visual="matrix",
                detail="Count adjacent mines for every cell, then run the cascade.",
                why="Correct, but it counts mines around cells the click never reaches.",
            ),
        ),
    ),
    Question(
        slug="pacific-atlantic-water-flow", number=417, title="Pacific Atlantic Water Flow",
        difficulty="Medium", topics=("grid",),
        summary="Rain flows from a cell to a neighbour of equal or lower height. The Pacific touches the top and left edges, the Atlantic the bottom and right. Return every cell from which water can reach both oceans.",
        example="[[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]  →  [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]",
        criterion="Which approach is linear in the grid size?",
        hint="Rather than following water down from every cell, where could you start and walk uphill?",
        choices=(
            Choice(
                "Reverse flood fill from each ocean", OPTIMAL, time="O(m·n)", space="O(m·n)", visual="graph-dfs",
                detail="From each ocean's edge, DFS uphill (to ≥ heights); return cells reached from both.",
                why="Reversing the flow turns 'which oceans can I reach' into two searches from the coasts. Each cell is visited at most twice.",
            ),
            Choice(
                "Downhill search from every cell", SUBOPTIMAL, time="O((m·n)²)", space="O(m·n)", visual="brute",
                detail="For each cell, DFS downhill and note which oceans it reaches.",
                why="Correct, but every search may cover the whole grid.",
            ),
            Choice(
                "Cells touching both coasts", INCORRECT, time="O(m + n)", space="O(1)", visual="matrix",
                detail="Return the top-right and bottom-left corner regions.",
                why="Water can travel across the grid. In the example, (2,2) sits in the middle.",
            ),
            Choice(
                "Walk uphill to strictly higher only", INCORRECT, time="O(m·n)", space="O(m·n)", visual="graph-dfs",
                detail="Reverse flood fill, but only into strictly higher cells.",
                why="Water also flows across equal heights. What happens on a flat stretch?",
            ),
        ),
    ),
    Question(
        slug="lcp-63-marble-game", number=None, title="Marble Game",
        difficulty="Medium", topics=("grid",),
        ref="LCP 63", url="https://leetcode.cn/problems/EXvqDp/",
        summary="A board has holes 'O', counter-clockwise turners 'W', clockwise turners 'E' and empty cells. A marble may be shot in from any empty non-corner edge cell, perpendicular to that edge, and moves at most num steps. Return every start from which it falls into a hole.",
        example="num = 4, plate = [\"..E.\", \".EOW\", \"..W.\"]  →  [[2, 1]]",
        criterion="Which approach is fastest when num can be 10⁶?",
        hint="Movement is deterministic and every turner can be undone. Can two different shots ever share a (cell, direction) state?",
        choices=(
            Choice(
                "Simulate each shot, capped at num", OPTIMAL, time="O(N·M)", space="O(1)", visual="matrix",
                detail="From every valid edge start, follow the marble until a hole, the edge or num steps.",
                why="Each state has exactly one predecessor, so paths from different starts never merge or loop. Together they cover each (cell, direction) at most once — O(N·M) in total, whatever num is.",
            ),
            Choice(
                "Memo table of outcomes", SUBOPTIMAL, time="O(N·M)", space="O(N·M)", visual="dp-2d",
                detail="Cache, for every cell and direction, where the marble ends and after how many steps.",
                why="Correct, but the cache only helps if paths share states — and they never do. It costs O(N·M) memory for nothing.",
            ),
            Choice(
                "Shortest path to a hole", INCORRECT, time="O(N·M) per start", space="O(N·M)", visual="graph-bfs",
                detail="BFS from each start toward the nearest hole.",
                why="The marble doesn't choose its route; it goes where the turners send it.",
            ),
            Choice(
                "Ignore the step limit", INCORRECT, time="O(N·M)", space="O(1)", visual="matrix",
                detail="Simulate until the marble stops, regardless of num.",
                why="A marble that reaches a hole after more than num steps doesn't count.",
            ),
        ),
    ),
    Question(
        slug="number-of-islands-ii", number=305, title="Number of Islands II",
        difficulty="Hard", topics=("grid", "data-structures"),
        summary="An m×n grid starts as all water. Positions are turned into land one at a time (possibly repeating). After each addition, report the number of islands.",
        example="m = 3, n = 3, positions = [[0,0],[0,1],[1,2],[2,1]]  →  [1, 1, 2, 3]",
        criterion="Which approach handles k additions fastest?",
        hint="A new cell can only merge islands. How do you know whether two neighbours already share one?",
        choices=(
            Choice(
                "Union-find", OPTIMAL, time="O(k·α(m·n))", space="O(m·n)", visual="union-find",
                detail="Skip repeats; count +1, then union with land neighbours, −1 per successful union.",
                why="Union-find answers 'same island?' in near-constant time, and each successful union merges two islands into one.",
            ),
            Choice(
                "Recount with flood fill each time", SUBOPTIMAL, time="O(k·m·n)", space="O(m·n)", visual="graph-dfs",
                detail="After each addition, count islands from scratch.",
                why="Correct, but each step rescans the whole grid for one changed cell.",
            ),
            Choice(
                "+1 minus land neighbours", INCORRECT, time="O(k)", space="O(m·n)", visual="counting",
                detail="Add 1, subtract the number of adjacent land cells.",
                why="Two neighbours may already be on the same island. Subtracting both merges it twice.",
            ),
            Choice(
                "Treat every position as new", INCORRECT, time="O(k·α(m·n))", space="O(m·n)", visual="union-find",
                detail="Union-find, but process repeated positions again.",
                why="Re-adding an existing land cell counts +1 for an island that doesn't exist.",
            ),
        ),
    ),
    Question(
        slug="number-of-spaces-cleaning-robot-cleaned", number=2061, title="Number of Spaces Cleaning Robot Cleaned",
        difficulty="Medium", topics=("grid",),
        summary="A robot starts at the top-left of a room (0 = empty, 1 = object) facing right. It moves straight, cleaning cells, and turns 90° clockwise whenever the next cell is blocked or outside. It runs forever. Count the cells it cleans.",
        example="[[0,0,0],[1,1,0],[0,0,0]]  →  7",
        criterion="Which approach stops exactly when nothing new can happen?",
        hint="When is the robot guaranteed to repeat itself forever?",
        choices=(
            Choice(
                "Simulate until a (cell, direction) repeats", OPTIMAL, time="O(m·n)", space="O(m·n)", visual="graph-dfs",
                detail="Track visited states; stop at the first repeated state.",
                why="Movement depends only on position and heading. Once a state repeats, the robot loops forever, so nothing new can be cleaned.",
            ),
            Choice(
                "Stop when a cell repeats", INCORRECT, time="O(m·n)", space="O(m·n)", visual="graph-dfs",
                detail="End the simulation at the first revisited cell.",
                why="Passing a cell again in a different direction can lead somewhere new.",
            ),
            Choice(
                "Simulate 4·m·n steps", SUBOPTIMAL, time="O(m·n)", space="O(m·n)", visual="brute",
                detail="Run a fixed number of steps, counting distinct cells.",
                why="Correct, since there are only 4·m·n states, but it keeps going long after the path has started repeating.",
            ),
            Choice(
                "Count reachable empty cells", INCORRECT, time="O(m·n)", space="O(m·n)", visual="graph-dfs",
                detail="Flood fill from the start and count.",
                why="The robot only goes straight and turns right at obstacles. Can it steer into every reachable cell?",
            ),
        ),
    ),
    Question(
        slug="sum-of-remoteness-of-all-cells", number=2852, title="Sum of Remoteness of All Cells",
        difficulty="Medium", topics=("grid",),
        summary="Cells are blocked (−1) or hold a positive value. A cell's remoteness is the sum of values of the open cells it cannot reach. Return the total remoteness over all open cells.",
        example="[[−1,1,−1],[5,−1,4],[−1,3,−1]]  →  39",
        criterion="Which approach is linear in the grid size?",
        hint="Do two cells in the same region have the same remoteness?",
        choices=(
            Choice(
                "Per region: (total − region sum) × size", OPTIMAL, time="O(m·n)", space="O(m·n)", visual="graph-dfs",
                detail="Flood fill each region for its sum s and size c; add (T − s)·c.",
                why="A cell can't reach exactly the cells outside its region, so every cell in a region shares one remoteness. One fill per region suffices.",
            ),
            Choice(
                "Search from every cell", SUBOPTIMAL, time="O((m·n)²)", space="O(m·n)", visual="brute",
                detail="For each open cell, explore its region and sum the rest.",
                why="Correct, but cells in the same region repeat the same search.",
            ),
            Choice(
                "Total minus each cell's own value", INCORRECT, time="O(m·n)", space="O(1)", visual="math",
                detail="Add (T − value) for every open cell.",
                why="A cell reaches its whole region, not only itself.",
            ),
            Choice(
                "Count unreachable cells", INCORRECT, time="O(m·n)", space="O(m·n)", visual="counting",
                detail="Add the number of cells each cell can't reach.",
                why="Remoteness adds values, not cells.",
            ),
        ),
    ),
    Question(
        slug="robot-room-cleaner", number=489, title="Robot Room Cleaner",
        difficulty="Hard", topics=("grid", "trees"),
        summary="Control a robot in an unknown room through move(), turnLeft(), turnRight() and clean(). You don't know the layout or your position. Clean every reachable cell.",
        example="An unseen room with obstacles; the robot starts somewhere open  →  every reachable cell cleaned",
        criterion="Which approach is guaranteed to clean every reachable cell?",
        hint="After exploring in one direction, how does the robot get back to where it was?",
        choices=(
            Choice(
                "Backtracking DFS with relative coordinates", OPTIMAL, time="O(N)", space="O(N)", visual="backtrack",
                detail="Track visited (x, y) from the start; try 4 directions; after each move, turn around, move back and restore the heading.",
                why="Relative coordinates replace the unknown map. Physically retracing each step restores the robot's state, so the DFS can continue from the previous cell.",
            ),
            Choice(
                "DFS without stepping back", INCORRECT, time="O(N)", space="O(N)", visual="graph-dfs",
                detail="Recurse into new cells but never return the robot.",
                why="When the recursion returns, the robot is still somewhere else. Which cell does the next try start from?",
            ),
            Choice(
                "Spiral outward", INCORRECT, time="O(N)", space="O(1)", visual="matrix",
                detail="Move in a growing spiral until blocked.",
                why="Obstacles break the spiral, and rooms behind them never get visited.",
            ),
            Choice(
                "Random walk until idle", INCORRECT, time="O(?)", space="O(N)", visual="brute",
                detail="Move randomly; stop after a long stretch with no new cells.",
                why="However long you wait, can you be sure no cell is left?",
            ),
        ),
    ),
]
