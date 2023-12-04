gonna make it using minimax-type logic.

### The players
The "2 players" will be:
	1. the human. Move choices: some subset of {up, down, left, right}
	2. the computer. Choices: some subset of {{2,4} for each cell}

And the static evaluation is defined to be positive when the human is "winning", and negative when the human is "losing".

### But what do winning and losing even mean??
Well, one way we can answer this, is to consider the cases for which the human has done something 
which is obviously "bad", and when they've done something obviously "good".

For example, losing is very bad. (-inf)
Getting ANY 2048 block (even if the position is otherwise not very good and won't last long) is very good. (+inf)

A few other ideas:
- making bigger blocks is good if they are neighboured by other big blocks (can define later but it's tricky since we can't just stick with "bottom row" since it could decide to play sideways, or by keeping big blocks on the top, and those are all equivalent.)
- chains that lead to big numbers are nice (but that doesnt need to be explicitly defined because):
	1. that leads to a big number, so we can just say we like a big score
	2. that leads to a big number and not that many tiles, so we can say that having not a lot of tiles on screen is good? or something similar

Another nice idea is that with alphabeta pruning ("there are lives on those branches ahhhh"), it's useful to find ways to order the moves in decreasing likelihood of being good (roughly). 

_(That's just like how in chess you consider checks, captures, attacks before quiet moves, especially when you "smell" a tactic)_

This means that even if there are concepts that don't have clear implications for static evaluation, those concepts **can** stil work towards making more prunes, so they'll increase efficiency.