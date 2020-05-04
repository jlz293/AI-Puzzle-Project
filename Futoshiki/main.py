import math     # Required to take the absolute value in the manhattan sum calculation
import heapq    # Required to take care of the priority list of the frontier
import copy     # Required to copy and deep copy arrays and 2d-arrays

class Variable:
    def __init__(self, val):
        self.val = val
        self.domain = [1, 2, 3, 4, 5]
        self.greater_than = []
        self.less_than = []

    def add_greater_than(self, neighbor):
        if neighbor not in self.greater_than:
            self.greater_than.append(neighbor)

    def add_less_than(self, neighbor):
        if neighbor not in self.less_than:
            self.less_than.append(neighbor)

    def update_domain(self):
        to_remove = []

        for neighbor in self.greater_than:
            for option in self.domain:
                if option <= int(neighbor.val) and neighbor.val != "0":
                    to_remove.append(option)

        for neighbor in self.less_than:
            for opt in self.domain:
                if opt >= int(neighbor.val) and neighbor.val != "0":
                    to_remove.append(opt)

        for a in to_remove:
            self.domain.remove(a)
        return
    def update_val(self):
        if self.val == '0' and len(self.domain) == 1:
            self.val = str(self.domain[0])
            return True
        return False

    def impossible(self):
        if len(self.domain) == 0:
            return True
        else:
            return False




class Node:
    def __init__(self, var, hor, vert):
        self.variables = var
        self.horizontal = hor
        self.vertical = vert
        self.initialize_horizontals()
        self.initialize_verticals()

    def initialize_horizontals(self):
        for i in range(len(self.horizontal)):
            for j in range(len(self.horizontal[i])):

                left_var = self.variables[i][j]
                right_var = self.variables[i][j+1]

                if self.horizontal[i][j] == '<':
                    left_var.add_less_than(right_var)
                    right_var.add_greater_than(left_var)
                elif self.horizontal[i][j] == '>':
                    left_var.add_greater_than(right_var)
                    right_var.add_less_than(left_var)

        return


    def initialize_verticals(self):
        for i in range(len(self.vertical)):
            for j in range(len(self.vertical[i])):

                up_var = self.variables[i][j]
                down_var = self.variables[i+1][j]

                if self.vertical[i][j] == '^':
                    up_var.add_less_than(down_var)
                    down_var.add_greater_than(up_var)

                elif self.vertical[i][j] == 'v':
                    up_var.add_greater_than(down_var)
                    down_var.add_less_than(up_var)

        return

    def forward_check(self):
        continue_flag = False
        for i in range(len(self.variables)):
            for j in range(len(self.variables[i])):
                self.variables[i][j].update_domain()
                if self.variables[i][j].update_val():
                    continue_flag = True
                if self.variables[i][j].impossible():
                    raise Exception("Puzzle Can not be Solved. IMPOSSIBLE")

        return continue_flag


    def forward(self):
        flag = True
        while flag:
            flag = self.forward_check()
            self.initialize_verticals()
            self.initialize_horizontals()
        if self.done():
            return True
        return False


    def done(self):
        answer = True
        for i in range(len(self.variables)):
            for j in range(len(self.variables[i])):
                if self.variables[i][j] == 0:
                    answer = False
        return answer

    def select_unassigned_variable(self):
        for i in range(len(self.variables)):


    def __repr__(self):
        string = ""
        for row in self.variables:
            for var in row:
                string += var.val
                string += " "
            string += "\n"
        return string




def initialize_variables(variables):

    for i in range(len(variables)):
        for j in range(len(variables[i])):
            obj = Variable(variables[i][j])
            variables[i][j] = obj
    return variables






# Parses lines from the input file into an array
def lines_to_2d_array(lines):
    for i in range(len(lines)):
        lines[i] = lines[i].strip("\n").strip("\r").strip(" ").split(" ")

    return lines


# Parses the input file and initializes the root and goal node
def input(file_name):
    file = open(file_name, "r")
    list_of_lines = file.readlines()

    variables = lines_to_2d_array(list_of_lines[0:5])
    variables = initialize_variables(variables)
    horizontal = lines_to_2d_array(list_of_lines[6:11])
    vertical = lines_to_2d_array(list_of_lines[12:16])
    file.close()

    return Node(variables, horizontal, vertical)





def backtracking():
    pass




if __name__ == "__main__":

    input_file = "Input2.txt"
    node = input(input_file)
    node.forward()
    print(node)

