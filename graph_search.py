import math
import heapq
import copy


class Node:
    def __init__(self, puzzle, goal, gn, path_to_curr, last_move=None):
        self.puzzle = puzzle
        self.path_to_curr = path_to_curr
        self.gn = gn
        self.hn = manhattan_distance(self.puzzle, goal)

        self.fn = self.gn + self.hn

        if last_move:
            self.last_move = last_move
        else:
            self.last_move = ""

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

    def __lt__(self, other):
        return self.fn < other.fn

    def __gt__(self, other):
        return self.fn > other.fn

    def __str__(self):
        string = string_puzzle(self.puzzle)
        path = ""
        for node in self.path_to_curr:
            path += node.last_move
        path += self.last_move
        string += "\nF(n) = " + str(self.fn) + "\nG(n) = " + str(self.gn) + "\nH(n) = " + str(self.hn) + "\nPath to Curr: " + str(path) + "\n"
        return string

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

    # Add the moves that are not out of bounds

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


def lines_to_2d_array(lines):
    for i in range(len(lines)):
        lines[i] = lines[i].strip("\n").split(" ")

    return lines


def string_puzzle(puzzle):
    string = ""
    for row in puzzle:
        for num in row:
            string += num
            string += " "
        string += "\n"
    return(string)


def manhattan_distance(puzzle, goal):

    answer = 0
    for i in range(0, 4, 1):
        for j in range(0, 4, 1):
            puzzle_ij = puzzle[i][j]
            i_puzzle = i
            j_puzzle = j

            index_set = index_at_value(goal, puzzle_ij)

            i_goal = index_set[0]
            j_goal = index_set[1]


            answer += (math.fabs(i_goal - i_puzzle) + math.fabs(j_goal - j_puzzle))

    return answer


def index_at_value(puzzle, val):

    for i in range(0,4):
        for j in range(0,4):
            if puzzle[i][j] == val:
                return [i, j]
    print("Input Error: No 0 in puzzle, no movement possible.")
    raise


def input(file_name):
    file = open(file_name, "r")
    list_of_lines = file.readlines()

    puzzle_lines = list_of_lines[0:4]
    goal_lines = list_of_lines[5:9]
    root_array = lines_to_2d_array(puzzle_lines)
    goal_array = lines_to_2d_array(goal_lines)

    root_node = Node(root_array, goal_array, 0, [])
    goal_node = Node(goal_array, goal_array, -1, None, None)

    return [root_node, goal_node]


def a_star(root, goal):

    def goal_reached(winner, expanded_nodes):
        print(winner)
        print("Number of Nodes: ", len(expanded_nodes))
        print("Depth: ", len(winner.path_to_curr))
        print("Last Move: ", winner.last_move)
        return

    curr_node = root
    expanded_nodes = [root]
    frontier = []
    heapq.heapify(frontier)

    while True:
        child_moves_lst = all_children_list(curr_node)
        children = []

        distance_to_child = curr_node.gn + 1

        path_to_child = copy.copy(curr_node.path_to_curr)
        path_to_child.append(curr_node)

    # Generate all possible children:
        for child_move in child_moves_lst:
            move = child_move[0]
            child_puzzle = copy.deepcopy(curr_node.puzzle)
            zero_swap_partner = child_puzzle[child_move[1][0]][child_move[1][1]]
            child_puzzle[child_move[2][0]][child_move[2][1]] = zero_swap_partner
            child_puzzle[child_move[1][0]][child_move[1][1]] = "0"

            new_node = Node(child_puzzle, goal.puzzle, distance_to_child, path_to_child, move)
            children.append(new_node)

    # Check if children have previously been generated and add to expanded_nodes and frontier:
        for node in children:
            if node not in expanded_nodes:
                expanded_nodes.append(node)
                frontier.append(node)
            if node == goal:
                print("Hurray")
                goal_reached(node, expanded_nodes)
                return

    # Find min_node, and make curr_node
        heapq.heapify(frontier)
        min_node = heapq.heappop(frontier)
        curr_node = min_node





if __name__ == "__main__":

    root, goal = input("Input1.txt")
    a_star(root, goal)

