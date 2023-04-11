import chess_engine
import logging
from Piece import Knight
from enums import Player
LOG_FILENAME = '../ex3 backup/exercise-3-debugging-logging-getting-into-a-large-codebase/python-chess/chess_debug.log'
# Empty log file every time we run the demo
open(LOG_FILENAME, 'w').close()

logging.basicConfig(
    filename=LOG_FILENAME,
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S'
)
logger = logging.getLogger(__name__)

game_state = chess_engine.game_state()
# 09-04-2023 16:33:34 DEBUG chess_engine Moving: (0, 6) -> (2, 5)
# 09-04-2023 16:33:37 DEBUG chess_engine Moving: (7, 6) -> (5, 5)
# 09-04-2023 16:33:43 DEBUG chess_engine Moving: (2, 5) -> (3, 3)
# 09-04-2023 16:33:46 DEBUG chess_engine Moving: (5, 5) -> (4, 3)
# 09-04-2023 16:33:52 DEBUG chess_engine Moving: (1, 6) -> (2, 6)
# 09-04-2023 16:33:55 DEBUG chess_engine Moving: (4, 3) -> (2, 2)

for starting_square, ending_square in [
    ((0, 6), (2, 5)),
    ((7, 6), (5, 5)),
    ((2, 5), (3, 3)),
    ((5, 5), (4, 3)),
    ((1, 6), (2, 6)),
    ((4, 3), (2, 2)),
]:
    game_state.move_piece(starting_square, ending_square, is_ai=False)
# Check why the white knight in (3,3) has no moves
white_knight_at_3_3 = Knight('white_k', 3, 3, Player.PLAYER_1)
white_knight_at_3_3.get_valid_piece_moves(game_state)



# 11-04-2023 11:31:00 DEBUG Piece Knight at (3, 3) valid moves: [(2, 1), (2, 5), (4, 1), (4, 5), (5, 4), (5, 2)]
