from enum import Enum


class GUISettings:
    TITLE = '2048™'
    MENU_SCORE_LABEL = 'Score:'
    MENU_HEIGHT = 100
    BOARD_SIZE = 400
    CELL_SIZE = 100
    GRID_PADDING = 10


class BoardSize:
    WIDTH = 4
    HEIGHT = 4


class GUIColors:
    BACKGROUND_COLOR_MENU = '#FAE1DD'
    BACKGROUND_COLOR_BOARD = '#FEC5BB'
    BACKGROUND_COLOR_CELL_EMPTY = '#FCD5CE'
    BACKGROUND_COLOR_ALERT = '#EFD6D2'

    CELL_COLOR_DICT = {2: '#F8EDEB', 4: '#E8E8E4', 8: '#D8E2DC', 16: '#D0DCD5',
                       32: '#C4D4CB', 64: '#B8CCC0', 128: '#ACC3B5',
                       256: '#A0BAAA', 512: '#95B2A0', 1024: '#89A995',
                       2048: '#7DA18B',
                       }

    TEXT_COLOR = '#F27202'


class GUIStyles:
    FONT = ('Verdana', 20, 'bold')
    ALERT_FONT = ('Verdana', 30, 'bold')
    MENU_FONT = ('Verdana', 25, 'bold')


class Keys:
    UP = ["'w'"]
    DOWN = ["'s'"]
    LEFT = ["'a'"]
    RIGHT = ["'d'"]
    RESTART = ["'r'"]


class GameStatus(Enum):
    CONTINUE = 0
    VICTORY = 1
    LOSE = 2

    @classmethod
    def is_continue(cls, status):
        return status == cls.CONTINUE
