Right, so, you have an NxN sudoku you want to solve right?
And you are really, really lazy right?
Except you're not lazy enough to not enter a N^2 long string of characters into a computer program, right?
Oh, and the N elements that we are going to use which can't include 0?

Great!

Then all you have to do is to change the 'seed' variable at the bottom of the arbitrary solver to the values of the sudoku you want to solve as they appear in the puzzle, left to right, top to bottom, with each empty square being indicated by a 0. After that, choose your N favourite elements which have some correspondence to the ones in your puzzle, and change the 'elements' variable when your are down there as well.

And there you have it!

You'll get some printouts regarding the values the program is setting but other than that, provided you put everything in correct, you should get the solved sudoku back out after a while!
