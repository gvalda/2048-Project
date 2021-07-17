import tkinter as tk
from tkinter import Frame, Label, CENTER
from constants import GUIColors, GUISettings, BoardSize, GUIStyles, Keys, GameStatus
from logic import Logic


class App(Frame):

    class Cell():
        def __init__(self, frame, label):
            self.frame = frame
            self.label = label

        def set_value(self, value):
            if value:
                self.label['text'] = str(value)
                self.set_colors_from_value_number(value)
            else:
                self.label['text'] = ''
                self.set_empty_colors()

        def set_colors_from_value_number(self, value):
            try:
                value = int(value)
                self.frame['bg'] = GUIColors.CELL_COLOR_DICT[value]
                self.label['bg'] = GUIColors.CELL_COLOR_DICT[value]
            except ValueError:
                print('Failed to set background for value {}. ' +
                      'It will be replaced with empty cell background'.format(value))
                self.set_empty_colors()

        def set_empty_colors(self):
            self.frame['bg'] = GUIColors.BACKGROUND_COLOR_CELL_EMPTY
            self.label['bg'] = GUIColors.BACKGROUND_COLOR_CELL_EMPTY

        def is_not_empty(self):
            return not self.is_empty()

        def is_empty(self):
            return self.label['text'] == ''

        def get_value(self):
            return self.label['text']

    def __init__(self, master=None):
        super().__init__(master)
        self.logic = Logic()
        self.build_GUI()
        self.start_new_game()
        self.master.bind("<Key>", self.key_pressed)

        self.mainloop()

    def build_GUI(self):
        self.create_foundation()
        self.create_menu()
        self.create_score_counter()
        self.create_board()
        self.generate_cells_on_board()

    def create_foundation(self):
        self.master.title(GUISettings.TITLE)
        self.grid()

    def create_menu(self):
        self.menu = self.create_menu_frame()
        self.menu.grid(sticky=tk.EW)

    def create_menu_frame(self):
        menu = Frame(self, bg=GUIColors.BACKGROUND_COLOR_MENU,
                     height=GUISettings.MENU_HEIGHT)
        return menu

    def create_score_counter(self):
        self.create_score_label()
        self.create_counter()

    def create_score_label(self):
        self.score = Label(self.menu, text=GUISettings.MENU_SCORE_LABEL,
                           bg=GUIColors.BACKGROUND_COLOR_MENU,
                           font=GUIStyles.MENU_FONT, fg=GUIColors.TEXT_COLOR)
        self.score.grid(column=0, row=0)

    def create_counter(self):
        self.counter = Label(self.menu, text=0,
                             bg=GUIColors.BACKGROUND_COLOR_MENU,
                             font=GUIStyles.MENU_FONT, fg=GUIColors.TEXT_COLOR)
        self.counter.grid(column=1, row=0)

    def create_board(self):
        self.board = self.create_board_frame()
        self.board.grid(sticky=tk.S)

    def create_board_frame(self):
        board = Frame(self, bg=GUIColors.BACKGROUND_COLOR_BOARD,
                      height=GUISettings.BOARD_SIZE)
        return board

    def generate_cells_on_board(self):
        cells_matrix = []
        for row in range(BoardSize.WIDTH):
            cells_row = []
            for column in range(BoardSize.HEIGHT):
                cell_frame = self.create_empty_frame()
                cell_frame.grid(row=row, column=column, padx=GUISettings.GRID_PADDING,
                                pady=GUISettings.GRID_PADDING)
                cell_label = self.create_empty_label()
                cell_label.grid(row=row, column=column)
                cell = self.Cell(cell_frame, cell_label)
                cells_row.append(cell)
            cells_matrix.append(cells_row)
        self.matrix = cells_matrix

    def create_empty_frame(self):
        return Frame(self.board, bg=GUIColors.BACKGROUND_COLOR_CELL_EMPTY,
                     width=GUISettings.CELL_SIZE, height=GUISettings.CELL_SIZE)

    def create_empty_label(self):
        return Label(self.board, text='',
                     bg=GUIColors.BACKGROUND_COLOR_CELL_EMPTY,
                     font=GUIStyles.FONT, fg=GUIColors.TEXT_COLOR)

    def start_new_game(self):
        self.game_status = GameStatus.CONTINUE
        self.values_matrix = self.logic.generate_matrix_for_new_game_and_start_it()
        self.update_GUI()
        self.update_counter_GUI()

    def update_GUI(self):
        for y, row in enumerate(self.values_matrix):
            for x, value in enumerate(row):
                self.matrix[y][x].set_value(value)

    def key_pressed(self, event):
        key = repr(event.char)
        if self.is_game_end() or key in Keys.RESTART:
            self.restart_game()
        else:
            if key in Keys.UP:
                self.key_up_pressed()
            elif key in Keys.DOWN:
                self.key_down_pressed()
            elif key in Keys.LEFT:
                self.key_left_pressed()
            elif key in Keys.RIGHT:
                self.key_right_pressed()
            else:
                return
            self.game_status = self.logic.game_status
            if self.is_game_end():
                self.make_alert_of_end_game()
            self.update_GUI()
            self.update_counter_GUI()

    def key_up_pressed(self):
        self.values_matrix = self.logic.move_up()

    def key_down_pressed(self):
        self.values_matrix = self.logic.move_down()

    def key_left_pressed(self):
        self.values_matrix = self.logic.move_left()

    def key_right_pressed(self):
        self.values_matrix = self.logic.move_right()

    def update_counter_GUI(self):
        self.counter_value = self.logic.counter
        self.counter['text'] = self.counter_value

    def is_game_end(self):
        return not GameStatus.is_continue(self.game_status)

    def restart_game(self):
        self.clear_alerts_and_game_status()
        self.start_new_game()

    def clear_alerts_and_game_status(self):
        self.game_status = GameStatus.CONTINUE
        if hasattr(self, 'alert'):
            self.alert.destroy()
            del self.alert

    def make_alert_of_end_game(self):
        self.alert = Label(self, font=GUIStyles.ALERT_FONT, fg=GUIColors.TEXT_COLOR,
                           bg=GUIColors.BACKGROUND_COLOR_ALERT,
                           text='You {} the game'.format(
                               'win' if self.game_status == GameStatus.VICTORY else 'lose'))

        self.alert.place(relx=0.5, rely=0.5, anchor=CENTER)


def main():
    App()


if __name__ == '__main__':
    main()
