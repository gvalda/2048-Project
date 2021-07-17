from constants import BoardSize, GameStatus
from random import randint, choice


class Logic():

    def generate_matrix_for_new_game_and_start_it(self):
        self.create_empty_matrix()
        self.set_value_2_or_4_to_empty_cell()
        self.set_value_2_or_4_to_empty_cell()
        self.game_status = GameStatus.CONTINUE
        self.counter = 0
        return self.matrix

    def create_empty_matrix(self):
        self.matrix = [[0] * BoardSize.WIDTH for _ in range(BoardSize.HEIGHT)]

    def set_value_2_or_4_to_empty_cell(self):
        x, y = self.find_empty_cell_cords()
        self.matrix[y][x] = choice((2, 4))

    def find_empty_cell_cords(self):
        x = randint(0, BoardSize.WIDTH-1)
        y = randint(0, BoardSize.HEIGHT-1)
        while(self.matrix[y][x] != 0):
            x = randint(0, BoardSize.WIDTH-1)
            y = randint(0, BoardSize.HEIGHT-1)
        return x, y

    def move_left(self):
        self.transpose()
        self.merge_cells()
        self.transpose()
        if self.is_any_empty_cell():
            self.set_value_2_or_4_to_empty_cell()
        self.update_game_status()
        return self.matrix

    def move_right(self):
        self.mirror()
        self.transpose()
        self.merge_cells()
        self.transpose()
        self.mirror()
        if self.is_any_empty_cell():
            self.set_value_2_or_4_to_empty_cell()
        self.update_game_status()
        return self.matrix

    def move_up(self):
        self.turn_counterclockwise()
        self.transpose()
        self.merge_cells()
        self.transpose()
        self.turn_clockwise()
        if self.is_any_empty_cell():
            self.set_value_2_or_4_to_empty_cell()
        self.update_game_status()
        return self.matrix

    def move_down(self):
        self.turn_clockwise()
        self.transpose()
        self.merge_cells()
        self.transpose()
        self.turn_counterclockwise()
        if self.is_any_empty_cell():
            self.set_value_2_or_4_to_empty_cell()
        self.update_game_status()
        return self.matrix

    def transpose(self):
        transposed_matrix = []
        for row in self.matrix:
            new_row = []
            for value in row:
                if value != 0:
                    new_row.append(value)
            new_row.extend([0]*(len(self.matrix)-len(new_row)))
            transposed_matrix.append(new_row)
        self.matrix = transposed_matrix

    def mirror(self):
        mirrored_matrix = []
        for row in self.matrix:
            mirrored_matrix.append(row[::-1])
        self.matrix = mirrored_matrix

    def turn_counterclockwise(self):
        turned_matrix = []
        for column in range(len(self.matrix[0])-1, -1, -1):
            turned_matrix.append([self.matrix[row][column]
                                 for row in range(len(self.matrix))])
        self.matrix = turned_matrix

    def turn_clockwise(self):
        turned_matrix = []
        for column in range(len(self.matrix[0])):
            turned_matrix.append([self.matrix[row][column]
                                 for row in range(len(self.matrix)-1, -1, -1)])
        self.matrix = turned_matrix

    def merge_cells(self):
        for y in range(len(self.matrix)):
            for x in range(len(self.matrix[y])-1):
                if self.matrix[y][x] != 0 and self.matrix[y][x] == self.matrix[y][x+1]:
                    self.matrix[y][x] *= 2
                    self.counter += self.matrix[y][x]
                    self.matrix[y][x+1] = 0

    def update_game_status(self):
        if self.is_game_won():
            self.game_status = GameStatus.VICTORY
        elif self.is_any_empty_cell() or self.can_be_merged():
            self.game_status = GameStatus.CONTINUE
        else:
            self.game_status = GameStatus.LOSE

    def is_any_empty_cell(self):
        return any(0 in row for row in self.matrix)

    def is_game_won(self):
        return any(2048 in row for row in self.matrix)

    def can_be_merged(self):
        for y in range(len(self.matrix)-1):
            for x in range(len(self.matrix[y])-1):
                if self.matrix[y][x] == self.matrix[y][x+1] or self.matrix[y][x] == self.matrix[y+1][x]:
                    return True
        for x in range(len(self.matrix[-1])-1):
            if self.matrix[-1][x] == self.matrix[-1][x+1]:
                return True
        for y in range(len(self.matrix[-1])-1):
            if self.matrix[y][-1] == self.matrix[y+1][-1]:
                return True
        return False
