## 08 Dec
It can now clearly aim for that bottom left corner, and it mostly manages to keep it there.
I'm running it on depth 4 and it seems to be doing quite good. only issue is that it ocassionally gets stuck and tries to play an invalid move for some reason, but then since it will give the same output from the same position, it essentially forces an infinite loop.

UPDATE:
I just realised it does that whenever it's about to lose. I don't know what's happening in the code yet, but it's funny to interpret as being salty:

 4  2  ○  ○ 
 16  32  4  16 
 128  2  64  32 
 4  16  128  2 


 ○  2  4  2 
 16  32  4  16 
 128  2  64  32 
 4  16  128  2 

after reaching that position it "gives up" and starts spamming an illegal move

# 11 Dec
Added a check to see how far away the big piece is from the corner to get it to stop moving up and stuff. kinda worked. still sometimes makes stupid decisions and is then forced to spend ages trying to fix its mess, and it some times gets 2s and stuff stuck in bottom row, but it is doing slightly better.

Update: Much later in now but HOW DO I GET THIS THING TO STOP GOING UP ALL THE TIME???
I don't get it, cuz my minimax function seems fine ive looked at it a lot and i dont see anything wrong with it. cleanness definitely isnt the best but in terms of functionality it seems like it is fine.   I'll try to refactor as much as i can to eliminate any hidden issues, cuz it keeps playing well then shifting or moving up, or basically just breaking the rules in [here](https://gaming.stackexchange.com/questions/160761/what-is-the-optimal-strategy-for-2048). It seems to play well 80% of the time, but then those eventual mess ups end up costing it a lot. and greater depth for some reason doesn't seem to have an effect