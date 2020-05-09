import copy

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
        initial_domain = [1, 2, 3, 4, 5]
        for neighbor in self.greater_than:
            for option in self.domain:
                if option <= int(neighbor.val) and neighbor.val != "0":
                    to_remove.append(option)

        for neighbor in self.less_than:
            for opt in self.domain:
                if opt >= int(neighbor.val) and neighbor.val != "0":
                    to_remove.append(opt)

        to_remove = list(set(to_remove))
        for a in to_remove:
            initial_domain.remove(a)
        self.domain = initial_domain
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

    def consistent(self):
        if self.val != '0':
            for opt in self.greater_than:
                if self.val <= opt.val and opt.val != '0':
                    return False
            for opt in self.less_than:
                if self.val >= opt.val and opt.val != '0':
                    return False

        return True



class Node:
    def __init__(self, var, hor, vert, copy_flag=False):
        self.variables = var
        self.horizontal = hor
        self.vertical = vert
        if not copy_flag:
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
                if self.variables[i][j].val == '0':
                    answer = False
        return answer

    def select_unassigned_variable(self):
        i_index = 0
        j_index = 0
        first_zero_flag = True
        mult_index = []
        for i in range(len(self.variables)):
            for j in range(len(self.variables[i])):
                if self.variables[i][j].val == '0':
                    if first_zero_flag:
                        first_zero_flag = False
                        i_index = i
                        j_index = j
                        mult_index.append([i, j])
                    elif len(self.variables[i_index][j_index].domain) > len(self.variables[i][j].domain):
                        mult_index = []
                        mult_index.append([i, j])
                        i_index = i
                        j_index = j
                    elif len(self.variables[i_index][j_index].domain) == len(self.variables[i][j].domain):
                        mult_index.append([i, j])

        if len(mult_index) > 1:
            max_neighbors = 0
            max_index = mult_index[0]
            for pair in mult_index:
                neighbors = len(self.variables[pair[0]][pair[1]].less_than) + len(self.variables[pair[0]][pair[1]].greater_than)
                if max_neighbors < neighbors:
                    max_neighbors = neighbors
                    max_index = pair
            return self.variables[max_index[0]][max_index[1]]
        else:
            return self.variables[i_index][j_index]


    def impossible(self):
        answer = False
        for row in self.variables:
            for var in row:
                if var.impossible():
                    answer = True
        return answer


    def update_domains(self):
        for row in self.variables:
            for var in row:
                var.update_domain()

        return

    def consistent(self):
        for row in self.variables:
            for var in row:
                if not var.consistent():
                    return False
        return True

    def __repr__(self):
        string = ""
        for row in self.variables:
            for var in row:
                string += str(var.val)
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





def backtracking_search(node):
    if not node.consistent():
        return False
    if node.done():
        return node

    curr_var = node.select_unassigned_variable()
    curr_domain = curr_var.domain

    for value in curr_domain:
        curr_var.val = str(value)
        node.update_domains()
        # print(node)
        result = backtracking_search(node)
        if result:
            return result
        else:
            curr_var.val = "0"
            node.update_domains()

    return False

if __name__ == "__main__":

    input_file = "Input3.txt"
    node = input(input_file)
    node.forward()


    print(node)
    print(backtracking_search(node))
