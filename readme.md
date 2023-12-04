2048 bot using minimax logic.

### The players
The "2 players" will be:
1. Human. Move choices: some subset of {up, down, left, right}
2. Computer. Choices: some subset of {{2,4} for each cell}

And the static evaluation is defined to be positive when the human is "winning", and negative when the human is "losing".

### But what do winning and losing even mean??
Well, one way we can answer this, is to consider the cases for which the human has done something 
which is obviously "bad", and when they've done something obviously "good".

For example, losing is very bad. (-inf)
Getting ANY **2048** block (even if the position is otherwise not very good and won't last long) is very good. (+inf) (if you wanted to go further, it could always adjust and aim for a new block)

### Rigorous definitions of rough ideas:
**Intuition:** keeping big blocks at the bottom is nice. or top if you choose to keep them at the top. or side.
**Slight improvement:** if there are big blocks at the bottom row (or bottom two), we don't want big blocks in the top 2 rows.
**Better Development:** define the heavy section to be the biggest edge row or edge column, somehow favouring the corners. from there, any blocks that exist anywhere other than that row can be treated as bad. we essentially pretend we want an isolated row or column, which actually isn't bad (cuz you'd think being forced up was bad), it just means we switch from building from bottom to building from top, since there literally is nothing else on the board. and if IS something on the second row, we can now move side to side.

This would then mean that you can take that bottom row (from now I'll pretend it's always working with the bottom row, just hold in your head that the other 3 are equivalent) and total the blocks for the initial "score".

this is the cool part. you then deduct from that score based on the other rows. 

For example in this board:

```python
[
	[ ],  [4], [ ], [ ],
	[4],  [2], [4], [ ],
	[16], [4], [2], [ ],
	[32], [8], [2], [4]
]
```
1. The bottom row is the biggest, so it's our base
2. The initial score is 32+8+2+4 = 46
3. The 3rd row has a total of 22, so we deduct 22*1 from the score
4. The next row has a total of 10, so we deduct 10*2 from the score
5. This row ***REEALLY*** shouldn't have anything, so we multiply by even more, 8, let's say. giving 2*8
6. Final score = 46-22-20-16= -12

So this says that the score isn't good at all. I think there's a nice way to set the parameters (1,2,8, the row weights) such that we get a nice definition of a drawn position (a static evaluation of 0), but I can't find one atm. Thankfully it doesn't actually matter that much. what matters more is whether a move increases or decreases this number, not what the number is specifically.

Other interesting things to note about this system:
1. that 4 in the top row is now priority, so even by moving left once, even though we don't remove anything, after the computer's best move (i.e the one that gives us the worst position), we still end up

2. chains that lead to big numbers are nice (but that doesnt need to be explicitly defined because):
	1. that leads to a big number in bottom row
	2. that leads to not many anywhere else, which is what we want (downside is that super long chains would require a high depth for it to see the true advantage, but that can't be helped)
so this helps maximise the static eval in **two** ways!

So there we have it! My random swishy swashy idea actually has pretty good prospects.

Another nice idea is that with alphabeta pruning ("there are lives on those branches ahhhh"), it's useful to find ways to order the moves in decreasing likelihood of being good (roughly). 

_(That's just like how in chess you consider checks, captures, attacks before quiet moves, especially when you "smell" a tactic)_

This means that even if there are concepts that don't have clear implications for static evaluation, those concepts **can** stil work towards making more prunes, so they'll increase efficiency.

