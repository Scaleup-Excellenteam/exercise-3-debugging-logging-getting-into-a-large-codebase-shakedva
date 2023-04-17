class Player:
    PLAYER_1 = 'white'
    PLAYER_2 = 'black'
    EMPTY = -9
    PIECES = ['white_r', 'white_n', 'white_b', 'white_q', 'white_k', 'white_p',
              'black_r', 'black_n', 'black_b', 'black_q', 'black_k', 'black_p']


class GameStatus:
    BLACK_WON = 0
    WHITE_WON = 1
    STALEMATE = 2
    IN_PROGRESS = 3
