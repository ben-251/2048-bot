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
Added a check to see how far away the big piece is from the corner to get it to stop moving up and stuff. kinda worked. still sometimes makes stupid decisions and is then forced to spend ages trying to fix its mess, and it some times gets 2s and stuff stuck in bottom row, but it is doing slightly better