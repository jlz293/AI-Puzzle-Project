import math     # Required to take the absolute value in the manhattan sum calculation
import heapq    # Required to take care of the priority list of the frontier
import copy     # Required to copy and deep copy arrays and 2d-arrays


class Node:
    def __init__(self, var, hor, vert):
        self.variables = var
        self.horizontal = hor
        self.vertical = vert


class Variable:
    def __init__(self, val):
        self.val = val
        self.domain = [1,2,3,4,5]
        self.greater_than = []
        self.less_than = []
    def add_greater_than(self, neighbor):
        self.greater_than.append(neighbor)

    def add_less_than(self, neighbor):
        self.less_than.append(neighbor)

    def update_domain(self):
        for neighbor in self.greater_than:
            for i in self.domain:
                if self.domain[i] <= neighbor.val:
                    self.domain.pop(i)
        for neighbor in self.less_than:
            for i in self.domain:
                if self.domain[i] >= neighbor.val:
                    self.domain.pop(i)

    def impossible(self):
        if len(self.domain) == 0:
            return True
        else:
            return False


def forward_checking():
    pass

def initialize_variables():
    pass


# Returns a string of a 2d-array
def string_puzzle(puzzle):
    string = ""
    for row in puzzle:
        for num in row:
            string += num
            string += " "
        string += "\n"
    return(string)



# Parses lines from the input file into an array
def lines_to_2d_array(lines):
    for i in range(len(lines)):
        lines[i] = lines[i].strip("\n").split(" ")

    return lines


# Parses the input file and initializes the root and goal node
def input(file_name):
    file = open(file_name, "r")
    list_of_lines = file.readlines()

    variables = lines_to_2d_array(list_of_lines[0:5])
    horizontal = lines_to_2d_array(list_of_lines[6:11])
    vertical = lines_to_2d_array(list_of_lines[12:16])
    file.close()

    return Node(variables, horizontal, vertical)

def backtracking



if __name__ == "__main__":

    input_file = "Input2.txt"
    node = input(input_file)

