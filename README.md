# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?

There are two main steps for solving the naked twins problem:
* First is iterating through a unit and finding the number of boxes each possible value has.
* Second is iterating each possible value and finding if there is a naked twins, based on the size and the values
assigned.

The definition of Constraint Propagation, presented in Udacity Nanodegree Program "Artifical Intelligence" is "using 
local constraints in a space (in the case of Sudoku, the constraints of each square) to dramatically reduce the search 
space" and thus reducing the number of possibilities.

The naked twin scenario is a clear case of Constraint Propagation, since when twins are found we can propagate this 
constraint to both peers and reduce the search space in the algorithm with this new updated picture. For instance:
* if we find __23__ naked twin twice, we can assign in one box _2_ and _3_ in another, reducing the possible paths to
investigate and propagating this constraint to its peers, eliminating both numbers.
* if we find _378_ naked twin twice, we try out using _3_ and _7_, _3_ and _8_ and finally _7_ and _8_.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  

For solving diagonal Sudoku problem, the process is exactly the same in the regular sudoku. The difference is the
existence of a third unit group, the diagonals, which affects the units in general and also the peers.
Redifining this, we can apply constant propagation using the diagonals to reduce the possibilities as well.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.