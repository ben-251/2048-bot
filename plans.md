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
5. This row ***REEALLY*** shouldn't have anything, so we multiply by even more, 8, let's say. giving 4*8
6. Final score = 46-22-20-32= -28

So this says that the score isn't good at all. I think there's a nice way to set the parameters (1,2,8, the row weights) such that we get a nice definition of a drawn position (a static evaluation of 0), but I can't find one atm. Thankfully it doesn't actually matter that much. what matters more is whether a move increases or decreases this number, not what the number is specifically.

## Implications of this static eval system
1. that 4 in the top row is now priority, so even by moving left once, even though we don't remove anything, after the computer's best move (i.e the one that gives us the worst position), we still end up able to go down next move and rid oursleves of the 4 at the top (and even though the 4 hasn't actually disappeared, it's now part of a nicer row)

2. chains that lead to big numbers are nice (but that doesnt need to be explicitly defined because):
	1. that leads to a big number in bottom row
	2. that leads to not many anywhere else, which is what we want (downside is that super long chains would require a high depth for it to see the true advantage, but that can't be helped)
so this helps maximise the static eval in **two** ways!

3. Certain positions (for example a row with all the same number) would be static-evaluated to be bad, but after the opponent's best move, and our best move, it turns out to be good. This is why depth matters a **lot**.

### One More Issue
As I said earlier, it doesn't yet take into account corners. It _seeems_ easy enough. Just make a full weight paint:

```python
weights = [
	[7.6], [7.8], [8.0], [8.0],
	[1.4], [1.6], [1.8], [2.0],
	[0.6], [0.8], [1.0], [1.4],
]
```

But the issue is that if the biggest tile in the biggest row/column is not in a corner, then there's no clear way to define this.

If I find a way to make this part work it'll be absolutely amazing, because then i can just do this:

```python
weights = [
	[-7.6], [-7.8], [-8.0], [-8.0],
	[-1.4], [-1.6], [-1.8], [-2.0],
	[-1.0], [-0.8], [-0.4], [-0.2],
	[+1.0], [+0.8], [+0.6], [+0.4]
]
```
And then multiply each value in board with the corresponding weight and bam (could even find a linear algebraic way to speed all this up potentially).

Also note I've created a sort of zig-zag now. The bottom row prefers to have the bottom left bigger, then the second (from the bottom) row prefers to have the right the biggest, then the next prefers the left, then finally the right. 

So the best way to arrange 2,4,8,...,2048 according to this, is:

```python
board = [
	[ ],    [ ],    [ ]    [ ],
	[8],    [4],    [2],   [ ],
	[16],   [32],   [64],  [128], 
	[2048], [1024], [512], [256], 
]
```
Which would be amazing! Only issue is that now it would think that a similar situation where the three rows are exactly even is also good, even though that would force an up. 

SOO we can just add that in manually. 

If we end up with 2 rows or 3 rows (but not 1 row) and nothing else, then that's very bad. decrease the score by 60% or something drastic like that. even though an issue like this can be solved by increasing the depth by one, this could end up as the end position of even a deep tree. interestingly we would probably only ever see this when the computer chooses to spawn in a way that traps us into that flat state. unfortunately our algorithm only works by assuming the computer will pick the worst state for us, so we can't do any sort of gambling with figuring out what risks are safe. maybe later, but that's a lot of probability theory that I am not getting into rn.

**!!BTW IT IS IMPERATIVE THAT THE BOTTOM ROW IS NOT THE ONLY DIRECTION ALLOWED!!**
because otherwise, if the computer gets into trouble and is forced to move up or something, it won't be able to switch and think on its feet. it'll be forced to try to go back to bottom left.


So there we have it! My random swishy swashy idea actually has pretty good prospects.



# BTW
***please don't say "ghost" player and stuff, say things like "simulated" to better reflect the idea of creating a fake version of something***