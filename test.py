import copy

import Player
from AI import Node
from Game_Board import Board

player_3 = Player.Player(3, 100)
player_1 = Player.Player(1, 300)

maximizing_player = copy.copy(player_3)

board = Board.Board(0, 0, 10)
node = Node.Node(board, player_1, player_3)

node.set_value(maximizing_player)

print(node.value)
print("---------------------------------------")
print(player_3.score)
maximizing_player.add_score(1700)
print(player_3.score)
print(maximizing_player.score)
print("---------------------------------------")

print(float('-inf'))
bool = float('-inf') < (float('-inf') - 1)
print(bool)
print(float('inf'))

list_of_bs = [2, 3, 4, 5]


def test_recursive(test_depth, iters: int = 0):
    if test_depth <= 0:
        return "test", iters

    if test_depth % 2 == 0:
        for i in range(2):
            string, iters = test_recursive(test_depth - 1, iters + 1)

        return string, iters

    else:
        for i in range(2):
            string, iters = test_recursive(test_depth - 3, iters + 1)

        return string, iters


result = test_recursive(10)
print(result)

test_1 = (1, "no")
test_2 = (1, "no")

print("---------------------")
print(test_1 == test_2)

test_matrix = [[0, 1, 2, 1, 4], [1, 3, 0, 0, 1]]

for row in test_matrix:
    for tile in row:
        if tile == 0:
            print
            continue

        print(f"{tile}: yes")


def empty():
    return


null = []
print(null)
none = 2
if none is not None:
    null.append(none)
print(null)
