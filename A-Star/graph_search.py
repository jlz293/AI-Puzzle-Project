import math     # Required to take the absolute value in the manhattan sum calculation
import heapq    # Required to take care of the priority list of the frontier
import copy     # Required to copy and deep copy arrays and 2d-arrays


class Node:
    def __init__(self, puzzle, goal, gn, path_to_curr, last_move=None):

        # Initializing all the relevant attributes
        self.puzzle = puzzle
        self.path_to_curr = path_to_curr
        self.gn = gn

        self.hn = manhattan_distance(self.puzzle, goal)
        self.fn = self.gn + self.hn

        if last_move:
            self.last_move = last_move
        else:
            self.last_move = ""

    # This returns a string representation of the ordered moves that occurred to get to the current node
    def string_path_moves(self):
        path = ""
        for node in self.path_to_curr:
            path += node.last_move + " "
        path += self.last_move
        return path

    # This returns a string representation of the f(n) values along the path to get to the current node
    def string_path_fn_values(self):
        path = ""
        for node in self.path_to_curr:
            path += str(int(node.fn)) + " "
        path += str(int(self.fn))
        return path

    # This is required to be able to compare nodes to the goal and previously expanded nodes
    def __eq__(self, other):
        my_string = ""
        other_string = ""
        for i in range(len(self.puzzle)):
            for j in range(len(self.puzzle[i])):
                my_string += self.puzzle[i][j]
        for k in range(len(other.puzzle)):
            for m in range(len(other.puzzle[k])):
                other_string += other.puzzle[k][m]

        return my_string == other_string

    # These operators are necessary to utilize the heap.
    # Not entirely sure about the implementation of heapq so I defined both
    def __lt__(self, other):
        return self.fn < other.fn

    def __gt__(self, other):
        return self.fn > other.fn

    # This was mostly for debugging, made it easier to be able to print the node
    def __str__(self):
        string = string_puzzle(self.puzzle)
        path = ""
        for node in self.path_to_curr:
            path += node.last_move
        path += self.last_move
        string += "\nF(n) = " + str(self.fn) + "\nG(n) = " + str(self.gn) + "\nH(n) = " + str(self.hn) + "\nPath to Curr: " + str(path) + "\n"
        return string


# Returns a list of all possible moves and the swap that would consequently occur in the array
def all_children_list(node):
    puzzle = node.puzzle
    zero_i, zero_j = index_at_value(puzzle, "0")
    children = []

    # Every move has a pair to be swapped: [Move, swap_pos[i][j], zero_pos[i][j]]
    moves = [

        ["L", [zero_i, zero_j - 1], [zero_i, zero_j]],
        ["R", [zero_i, zero_j + 1], [zero_i, zero_j]],
        ["U", [zero_i - 1, zero_j], [zero_i, zero_j]],
        ["D", [zero_i + 1, zero_j], [zero_i, zero_j]],
    ]

    # Add the moves that are not out of bounds to the return list of possible moves

    # Left
    if zero_j != 0:
        children.append(moves[0])

    # Right
    if zero_j != 3:
        children.append(moves[1])

    # Up
    if zero_i != 0:
        children.append(moves[2])

    # Down
    if zero_i != 3:
        children.append(moves[3])

    return children


# Parses lines from the input file into an array
def lines_to_2d_array(lines):
    for i in range(len(lines)):
        lines[i] = lines[i].strip("\n").split(" ")

    return lines

# Returns a string of a 2d-array
def string_puzzle(puzzle):
    string = ""
    for row in puzzle:
        for num in row:
            string += num
            string += " "
        string += "\n"
    return(string)


# Calculates the manhattan distance between the root and goal
def manhattan_distance(root, goal):
    answer = 0
    for i in range(0, 4, 1):
        for j in range(0, 4, 1):
            root_ij = root[i][j]
            i_root = i
            j_root = j

            index_set = index_at_value(goal, root_ij)

            i_goal = index_set[0]
            j_goal = index_set[1]

            answer += (math.fabs(i_goal - i_root) + math.fabs(j_goal - j_root))

    return answer


# Finds the 2d-array index of a given val in a given array, useful primarily for the manhattan distance calculation
def index_at_value(puzzle, val):

    for i in range(0,4):
        for j in range(0,4):
            if puzzle[i][j] == val:
                return [i, j]
    print("Input Error: No 0 in puzzle, no movement possible.")
    raise


# Parses the input file and initializes the root and goal node
def input(file_name):
    file = open(file_name, "r")
    list_of_lines = file.readlines()

    puzzle_lines = list_of_lines[0:4]
    goal_lines = list_of_lines[5:9]
    root_array = lines_to_2d_array(puzzle_lines)
    goal_array = lines_to_2d_array(goal_lines)

    root_node = Node(root_array, goal_array, 0, [])
    goal_node = Node(goal_array, goal_array, -1, None, None)
    file.close()
    return [root_node, goal_node]


# Main algorithm
def a_star(root, goal):

    # Setup
    curr_node = root
    expanded_nodes = [root]
    frontier = []
    heapq.heapify(frontier)

    # Do
    while True:

    # Setup to generate children
        child_moves_lst = all_children_list(curr_node)
        children = []

        distance_to_child = curr_node.gn + 1

        path_to_child = copy.copy(curr_node.path_to_curr)
        path_to_child.append(curr_node)

    # Generate all possible children:
        for child_move in child_moves_lst:
            move = child_move[0]

            # Swap the 0 with the relevant tile according to the corresponding move direction
            child_puzzle = copy.deepcopy(curr_node.puzzle)
            zero_swap_partner = child_puzzle[child_move[1][0]][child_move[1][1]]
            child_puzzle[child_move[2][0]][child_move[2][1]] = zero_swap_partner
            child_puzzle[child_move[1][0]][child_move[1][1]] = "0"

            # Generate the new node
            new_node = Node(child_puzzle, goal.puzzle, distance_to_child, path_to_child, move)
            children.append(new_node)

    # Check if children have previously been generated and add to expanded_nodes and frontier:
        for node in children:
            if node not in expanded_nodes:
                expanded_nodes.append(node)
                frontier.append(node)
            if node == goal:
                return node, expanded_nodes

    # Find min_node, remove from frontier, and make curr_node
        heapq.heapify(frontier)
        min_node = heapq.heappop(frontier)
        curr_node = min_node


# Structures and creates the output file
def output(node, expanded, root, goal, input_file):
    output_file = "Output-" + input_file
    file = open(output_file, "w")
    file.write(string_puzzle(root.puzzle))
    file.write("\n")
    file.write(string_puzzle(goal.puzzle))
    file.write("\n")
    file.write(str(node.gn))
    file.write("\n")
    file.write(str(len(expanded)))
    file.write("\n")
    file.write(node.string_path_moves())
    file.write("\n")
    file.write(node.string_path_fn_values())
    file.close()


if __name__ == "__main__":

    input_file = "Input2.txt"

    root, goal = input(input_file)
    winner_node, list_of_nodes = a_star(root, goal)
    output(winner_node, list_of_nodes, root, goal, input_file)

