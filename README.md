# AI-Puzzle-Project
This repository maintains the files for Project 1: 15-Puzzle Problem in Artificial Intelligence using A-Star

The main functional code for this project is in the file called graph_search.py

The code runs like any python file, simply run it through the terminal. The input file that is to be operated on can be changed in the code itself. To do this simply go to line 239 in graph_search.py, here the input_file defined. It is currently set to run Input4.txt if you want to change this, simply change the string to the title of the file you would like to input. 

The A* (A-Star) algorithm was used to find the goal sequence.

The heuristic used is the sum of the manhattan distances (taxicab distance) between the tiles of the root and the goal state puzzle. 

