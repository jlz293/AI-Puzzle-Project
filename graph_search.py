import math

class Node:
    def __init__(self, puzzle, goal, gn = 0, path_to_curr = None, last_move = None):
        self.puzzle = puzzle
        self.gn = gn
        self.hn = manhattan_distance(self.puzzle, goal)
        self.fn = self.gn + self.hn

        if not path_to_curr:
            self.path_to_curr = []
        else:
            self.path_to_curr = path_to_curr

        if last_move:
            self.last_move = last_move



def all_children(node):
    puzzle = node.puzzle
    zero_pos_pair = index_at_value(puzzle, 0)
    zero_i = zero_pos_pair[0]
    zero_j = zero_pos_pair[1]

    # Every move has a pair to be swapped: [Move, swap_pos[i][j], zero_pos[i][j]]
    moves = [

        ["L", [zero_i, zero_j - 1], [zero_i, zero_j]],
        ["R", [zero_i, zero_j + 1], [zero_i, zero_j]],
        ["U", [zero_i - 1, zero_j], [zero_i, zero_j]],
        ["D", [zero_i + 1, zero_j], [zero_i, zero_j]],
    ]

    # Delete the moves that would be out of bounds of the puzzle

    if zero_i == 0:
        moves.pop(0)
    if zero_i == 3:
        moves.pop(1)
    if zero_j == 0:
        moves.pop(2)
    if zero_j == 3:
        moves.pop(3)

    return moves








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

    return False




if __name__ == "__main__":
    initial = [[1,2,3,4], [5,6,0,7], [8,9,10,11], [12,13,14,15]]
    goal = [[8,2,3,4], [5,9,6,7], [12,13,0,11], [1,14,10,15]]
    print("The Manhattan Distance is: ", manhattan_distance(initial, goal))


