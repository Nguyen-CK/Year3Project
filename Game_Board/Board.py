import pygame
import time

from Game_Board.Arrow import Arrow
from Game_Board.Square import Square
from Game_Board.Box import Box
from Game_Board.Direction import Direction


class Board:
    def __init__(self, x_position, y_position, side):
        self.width = side * 7
        self.height = side * 2

        self.square_side = side

        self.x_position = x_position
        self.y_position = y_position

        """
        Variables for the game board tiles
        """
        self.layout = self.fill_board()
        self.row_matrix = self.layout[1]
        self.left_box = self.layout[0]
        self.right_box = self.layout[2]
        # generate the board

        self.selected_square = None
        self.turn = 1

        self.left_arrow = None
        self.right_arrow = None

    def fill_board(self):
        top_row: list[Square] = []
        bottom_row: list[Square] = []

        current_x = self.x_position
        current_y = self.y_position

        left_box = Box(current_x, self.y_position, self.square_side)
        current_x = current_x + self.square_side

        for row in range(2):
            if row == 0:
                current_row = top_row
                current_player = 2
            else:
                current_row = bottom_row
                current_player = 1

            for col in range(5):
                square = Square(current_x, current_y, col, row, self.square_side, current_player)
                # square.start_fill()
                current_row.append(square)
                current_x = current_x + self.square_side

            current_x = self.x_position + self.square_side
            current_y = current_y + self.square_side

        current_x = self.x_position + (self.square_side * 6)
        right_box = Box(current_x, self.y_position, self.square_side)

        board = (left_box, [top_row, bottom_row], right_box)

        return board

    def draw_board(self, screen):
        for row in self.row_matrix:
            for square in row:
                square.draw(screen)
        self.right_box.draw(screen)
        self.left_box.draw(screen)

        if self.left_arrow is not None and self.right_arrow is not None:
            self.left_arrow.draw(screen)
            self.right_arrow.draw(screen)

    def get_square_from_pos(self, x, y):
        for row in self.row_matrix:
            for tile in row:
                if tile.rel_x == x and tile.rel_y == y:
                    return tile

    def handle_click(self, mx, my):
        row_start_x = self.x_position + self.square_side
        row_start_y = self.y_position

        clicked_square = None

        x = (mx - row_start_x) // self.square_side
        y = (my - row_start_y) // self.square_side
        str = f"m_x: {x}     m_y: {y}"
        print(str)

        if 0 <= x < 5 and 0 <= y < 2:
            clicked_square = self.get_square_from_pos(x, y)

        if self.selected_square is None:
            if clicked_square is not None and not clicked_square.is_empty():
                # print(clicked_square.rel_x)
                if clicked_square.player == self.turn:
                    self.selected_square = clicked_square
                    self.selected_square.is_highlighted = True
                    y_off_set = 0
                    if self.turn == 1:
                        y_off_set = self.selected_square.y + self.selected_square.side + 10
                    else:
                        y_off_set = self.selected_square.y - 10

                    x_off_set = self.selected_square.x + self.selected_square.side

                    self.left_arrow = Arrow(self.selected_square.x, y_off_set, self.turn, Direction.LEFT)
                    self.right_arrow = Arrow(x_off_set, y_off_set, self.turn, Direction.RIGHT)
                    # print(self.selected_square.rel_x)
                    # print(self.selected_square.rel_y)
        else:
            if self.left_arrow.is_in_bound(mx, my):
                print("MOVING LEFT")  # MOVE LEFT
                return self.left_arrow.handle_click(), self.selected_square
            elif self.right_arrow.is_in_bound(mx, my):
                print("MOVING RIGHT")  # MOVE RIGHT
                return self.right_arrow.handle_click(), self.selected_square
            else:
                self.selected_square.is_highlighted = False
                self.selected_square = None

                self.right_arrow = None
                self.left_arrow = None

        return None, None

    def is_game_over(self):
        if self.left_box.no_stone() and self.right_box.no_stone():
            return True

        return False

    def move(self, current_tile, direction: Direction, previous_tile=None):
        next_x = 0
        current_x = 0
        current_y = 0
        if isinstance(current_tile, Box):
            next_pos = self.get_next_pos_from_box(current_tile, previous_tile)
            next_x = next_pos[0]
            current_y = next_pos[1]

        else:
            current_x = current_tile.rel_x
            current_y = current_tile.rel_y

            next_x = current_x + direction.value

        if next_x < 0:  # move to left box
            self.left_box.add_pebble()
            tile = self.left_box
            return tile, False
        elif next_x > 4:  # move to right box
            self.right_box.add_pebble()
            tile = self.right_box
            return tile, False
        else:
            tile = self.get_square_from_pos(next_x, current_y)
            self.get_square_from_pos(next_x, current_y).add_pebble()
            return tile, True

    def full_move(self, current_square: Square, direction: Direction):
        """
        Move the pebble(s) from a Tile in a Direction in a full turn
        :param current_square: Tile to move from
        :param direction: Direction to move to
        :return: Tuple containing 2 Boolean:
                        1st: True if End turn, False if not
                        2nd: True if capture is available, False if End on Box or Double empty
                        and the Tile that can be capture
                        and the direction the move is currently on
                        and the previous adjacent Tile that it stopped on
        """
        num_of_moves = current_square.pebble_stored
        current_square.empty()
        current = current_square
        previous = None

        while num_of_moves >= 0:
            """
            ## DEBUG PRINT
            print(f"Current Direction: {direction}")
            if isinstance(current, Box):
                if current == self.left_box:
                    print(f"LEFT BOX: {self.left_box.pebble_stored}")
                elif current == self.right_box:
                    print(f"RIGHT BOX: {self.right_box.pebble_stored}")
            else:
                print(f"Current X: {current.rel_x}    Current Y: {current.rel_y}    Pebble: {current.pebble_stored}")
            print(f"{num_of_moves} moves left")
            """
            # When out of pebbles(moves)
            if num_of_moves == 0:
                next_square = None
                if isinstance(current, Box):
                    next_pos = self.get_next_pos_from_box(current, previous)
                    next_x = next_pos[0]
                    next_y = next_pos[1]

                    next_square = self.get_square_from_pos(next_x, next_y)
                else:
                    if current.rel_x == 0 and direction == Direction.LEFT and not self.left_box.is_empty():
                        return True, False, None, direction, previous  # End turn on non-empty left Box

                    elif current.rel_x == 4 and direction == Direction.RIGHT and not self.right_box.is_empty():
                        return True, False, None, direction, previous  # End turn on non-empty right Box

                    if current.rel_x == 0 and direction == Direction.LEFT:
                        next_square = self.left_box
                    elif current.rel_x == 4 and direction == Direction.RIGHT:
                        next_square = self.right_box
                    else:
                        next_square = self.get_square_from_pos((current.rel_x + direction.value), current.rel_y)

                if not next_square.is_empty():
                    num_of_moves = next_square.pebble_stored
                    next_square.empty()
                    current = next_square
                    continue
                else:
                    is_cap, cap_tile, direct = self.is_capture_available(current, direction, previous)
                    if is_cap:
                        return True, True, cap_tile, direct, previous  # End turn on capture
                    else:
                        return True, False, None, direction, previous  # End turn on double empty Tile

            result = self.move(current, direction, previous)
            previous = current
            current = result[0]
            num_of_moves -= 1
            # self.draw_board(screen)

            is_same_direction = result[1]
            if not is_same_direction:
                direction = direction.swap()
            # print("--------------")

        return False, False, None, direction, previous  # ERROR

    def capture(self, current_square: Square, direction: Direction, previous_tile):
        value = 0
        current = current_square
        capture_available = True

        while capture_available:
            if isinstance(current, Box):
                value += current.capture_box()
            else:
                value += current.capture_square()
            result = self.is_capture_available(current, direction, previous_tile)
            capture_available = result[0]
            current = result[1]
            direction = result[2]

        return value

    def is_capture_available(self, current_tile, direction: Direction, previous_tile):
        adj_tile = None
        capture_tile = None
        next_x = 0
        # next_y = 0
        if isinstance(current_tile, Box):
            next_pos = self.get_next_pos_from_box(current_tile, previous_tile)
            next_x = next_pos[0]
            next_y = next_pos[1]
            adj_tile = self.get_square_from_pos(next_x, next_y)
        else:
            next_x = current_tile.rel_x + direction.value
            if next_x < 0:  # hit left box
                adj_tile = self.left_box
                direction = direction.swap()
            elif next_x > 4:  # hit right box
                adj_tile = self.right_box
                direction = direction.swap()
            else:
                adj_tile = self.get_square_from_pos(next_x, current_tile.rel_y)

        if adj_tile.is_empty():
            if isinstance(adj_tile, Box):
                if adj_tile == self.left_box:
                    if current_tile.rel_y == 1:
                        capture_tile = self.get_square_from_pos(0, 0)
                    else:
                        capture_tile = self.get_square_from_pos(0, 1)

                elif adj_tile == self.right_box:
                    if current_tile.rel_y == 1:
                        capture_tile = self.get_square_from_pos(4, 0)
                    else:
                        capture_tile = self.get_square_from_pos(4, 1)

            else:
                if adj_tile.rel_x == 0 and direction == Direction.LEFT:  # hit left box
                    capture_tile = self.left_box
                elif adj_tile.rel_x == 4 and direction == Direction.RIGHT:  # hit right box
                    capture_tile = self.right_box
                else:
                    cap_x = adj_tile.rel_x + direction.value
                    capture_tile = self.get_square_from_pos(cap_x, adj_tile.rel_y)

            if capture_tile.is_empty():
                return False, capture_tile, direction  # Double empty
            else:
                return True, capture_tile, direction  # Capture Available

        return False, None, direction

    def get_next_pos_from_box(self, box: Box, previous_tile: Square):
        next_x = 0
        next_y = 0
        assert previous_tile is not None
        if previous_tile.rel_y == 0:
            next_y = 1
        elif previous_tile.rel_y == 1:
            next_y = 0

        if box == self.right_box:
            next_x = 4
        elif box == self.left_box:
            next_x = 0

        return next_x, next_y

    def check_row_empty(self):
        row = None
        if self.turn == 1:
            row = self.row_matrix[1]
        elif self.turn == 2:
            row = self.row_matrix[0]
        else:
            return None

        for tile in row:
            if not tile.is_empty():
                return False

        return True

    def refill_row(self, player):
        to_fill = player.borrow_pebble()
        if player.num == 1:
            for tile in self.row_matrix[1]:
                tile.add_pebble()
        elif player.num == 2:
            for tile in self.row_matrix[0]:
                tile.add_pebble()

    def clear_row(self, player):
        row = None
        value = 0
        if player.num == 1:
            row = self.row_matrix[1]
        elif player.num == 2:
            row = self.row_matrix[0]

        for tile in row:
            if not tile.is_empty():
                value += tile.capture_square()

        return value

    def end_turn(self):
        if self.turn == 1:
            self.turn = 2
        elif self.turn == 2:
            self.turn = 1
        else:
            return
