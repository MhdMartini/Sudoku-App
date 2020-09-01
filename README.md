This is an ongoing project. The hard part about creating a Sudoku game is to create a "proper" game, meaning a game which only has one solution. My goal here is to learn GUI development in Kivy, and to create a Sudoku game without the need for backtracking, on the hope of achieving better performance such that the game is easily scalable to 16x16 or 25x25 or even bigger! There is a lot that is unknown about Sudoku; after digging very deep into the math of it, it turned out that creating a unique Sudoku puzzle without brute force is as hard as calculating how many possible Sudoku puzzles are there without brute force, which has not been achieved yet! That being said, I might end up using backtracking with some tweeks to identify the number or unique solutions, but before then, I need to do my best. 

WHAT I LEARNED:
1- Kivy GUI development.
  - Kivy is a vast library with MANY options for GUI development which makes it suitable even for professionals. 
  - Kivy relies heavily on class inheritance, and quite often you will need to "hijack" a class and add your own attributes to it, or inherit two or more classes and add other   attributes to them to create a unique hybrid. The opportunities are vast.

2- Sudoku math.
  - Creating a proper Sudoku puzzle is actually the hard part about building a Sudoku game. I have done a lot of research to understand the patterns of a Sudoku sheet and be able to control its outcome; it is not a trivial task.

3- Algorithms for pattern finding
  - Some patterns contribute to the unpredictibility of a Sudoku sheet. Clues that form these patterns need to be exposed or otherwise there would be more than one unique solution. To identify all these pattern-forming-clues is to be able to calculate how many different Sudoku sheets can be made from a single Sudoku sheet. 
  - Most of the time spent making this project was spend on trying to identify these patterns, and it was a great practice on building complex algorithms that are also efficient.
  - However, after being able to capture all the patterns I identified by eye, I was faced with occasional other patterns which were too subtle to characterize. Thus, I opted for creating a rotationally symmetrical puzzle, which gave about the same percentage of improper puzzles but without any complex calculations.
  - Current plan is to create a Sudoku solver which generates proper Sudoku puzzles, possibly with backtracking, and look further into the patterns at some point later. 
