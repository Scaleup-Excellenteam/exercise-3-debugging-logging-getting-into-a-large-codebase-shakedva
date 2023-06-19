import pytest

import ai_engine
from unittest.mock import Mock
from Piece import Knight, King, Rook
from enums import Player, GameStatus
import chess_engine

"""
Unit tests
"""


@pytest.fixture
def game_state_mock():
    return Mock()


# Tests for the function get_valid_peaceful_moves in class Knight

def test_knight_middle_empty(game_state_mock: Mock):
    """
    The knight is in the middle, all the surrounding squares are empty
    :param game_state_mock: unittest chess game mock
    """
    game_state_mock.get_piece = Mock(return_value=Player.EMPTY)
    white_knight = Knight('n', 3, 4, Player.PLAYER_1)
    result = white_knight.get_valid_peaceful_moves(game_state_mock)
    expected_moves = {(1, 3), (1, 5), (2, 2), (2, 6), (4, 2), (4, 6), (5, 3), (5, 5)}
    assert set(result) == expected_moves


def test_knight_right_empty(game_state_mock: Mock):
    """
    The knight is on the left side of the board, half of the squares are empty (from the right side)
    and the rest are off the board
    :param game_state_mock: unittest chess game mock
    """
    game_state_mock.get_piece = Mock(return_value=Player.EMPTY)
    white_knight = Knight('n', 2, 0, Player.PLAYER_1)
    result = white_knight.get_valid_peaceful_moves(game_state_mock)
    result = [i for i in result if 0 <= i[0] < 8 and 0 <= i[1] < 8]
    expected_moves = {(0, 1), (1, 2), (3, 2), (4, 1)}
    assert set(result) == expected_moves


def test_knight_upper_empty(game_state_mock: Mock):
    """
    The knight is on the bottom of the board, half of the squares off the board, one of the squares contain an enemy
    piece and the rest are empty
    :param game_state_mock: unittest chess game mock
    """

    def get_piece_side_effect(row: int, col: int):
        if (row, col) in [(6, 3)]:
            return Knight('n', row, col, Player.PLAYER_1)
        return Player.EMPTY

    game_state_mock.get_piece = get_piece_side_effect
    black_knight = Knight('n', 7, 5, Player.PLAYER_2)
    result = black_knight.get_valid_peaceful_moves(game_state_mock)
    result = [i for i in result if 0 <= i[0] < 8 and 0 <= i[1] < 8]
    expected_moves = {(5, 4), (5, 6), (6, 7)}
    assert set(result) == expected_moves


# Tests for the function get_valid_piece_takes in class Knight

def test_knight_only_take_moves(game_state_mock: Mock):
    """
    The knight is in the middle, all the surrounding squares contain enemy pieces
    :param game_state_mock: unittest chess game mock
    """

    def is_valid_piece_side_effect(row: int, col: int):
        return 0 <= row < 8 and 0 <= col < 8

    def get_piece_side_effect(row: int, col: int):
        if (row, col) in [(1, 2), (1, 4), (2, 1), (2, 5), (4, 1), (4, 5), (5, 2), (5, 4)]:
            return Knight('n', row, col, Player.PLAYER_2)
        return Player.EMPTY

    game_state_mock.is_valid_piece = is_valid_piece_side_effect
    game_state_mock.get_piece = get_piece_side_effect

    white_knight = Knight('n', 3, 3, Player.PLAYER_1)
    result = white_knight.get_valid_piece_takes(game_state_mock)

    # assert that all the available squares have a black knight on them
    assert all(game_state_mock.get_piece(row, col).get_player() == Player.PLAYER_2 for row, col in result)


def test_knight_upper_take_moves(game_state_mock: Mock):
    """
    The knight is on the bottom of the board, half of the squares off the board, one of the squares contain an enemy
    piece and the rest are empty
    :param game_state_mock: unittest chess game mock
    """

    def is_valid_piece_side_effect(row: int, col: int):
        return 0 <= row < 8 and 0 <= col < 8 and (row, col) != (6, 5)

    def get_piece_side_effect(row: int, col: int):
        if (row, col) in [(5, 2), (6, 1), (5, 4)]:
            return Knight('n', row, col, Player.PLAYER_2)
        return Player.EMPTY

    game_state_mock.is_valid_piece = is_valid_piece_side_effect
    game_state_mock.get_piece = get_piece_side_effect

    white_knight = Knight('n', 7, 3, Player.PLAYER_1)
    result = white_knight.get_valid_piece_takes(game_state_mock)
    assert all(game_state_mock.get_piece(row, col).get_player() == Player.PLAYER_2 for row, col in result)


"""
Integration tests
"""


def test_knight_get_valid_piece_moves(game_state_mock: Mock):
    """
    The knight is in the middle of the board. Some contain enemy pieces, some empty.
    Test the function get_valid_piece_moves
    :param game_state_mock: unittest chess game mock
    """

    def is_valid_piece_side_effect(row: int, col: int):
        return 0 <= row < 8 and 0 <= col < 8 and ((row, col) in [(1, 2), (2, 5), (4, 1)])

    def get_piece_side_effect(row: int, col: int):
        if (row, col) in [(1, 2), (2, 5), (4, 1)]:
            return Knight('n', row, col, Player.PLAYER_2)
        return Player.EMPTY

    game_state_mock.is_valid_piece = is_valid_piece_side_effect
    game_state_mock.get_piece = get_piece_side_effect

    white_knight = Knight('n', 3, 3, Player.PLAYER_1)

    take_moves = white_knight.get_valid_piece_takes(game_state_mock)
    peaceful_moves = white_knight.get_valid_peaceful_moves(game_state_mock)
    all_moves = white_knight.get_valid_piece_moves(game_state_mock)
    assert set(take_moves) == {(1, 2), (2, 5), (4, 1)}
    assert set(peaceful_moves) == {(1, 4), (2, 1), (4, 5), (5, 2), (5, 4)}
    assert set(take_moves) | set(peaceful_moves) == set(all_moves)


def test_evaluate_board_white_ai(game_state_mock: Mock):
    """
    The AI is white player, there are also 2 black pieces.
    Check chess_ai function evaluate_board.
    :param game_state_mock: unittest chess game mock
    """

    def is_valid_piece_side_effect(row: int, col: int):
        return 0 <= row < 8 and 0 <= col < 8 and ((row, col) in [(4, 5), (6, 2)])

    def get_piece_side_effect(row, col):
        if (row, col) == (6, 2):
            return King('k', 6, 2, Player.PLAYER_2)
        elif (row, col) == (4, 5):
            return Rook('r', 4, 5, Player.PLAYER_2)
        else:
            return Player.EMPTY

    game_state_mock.is_valid_piece = is_valid_piece_side_effect
    game_state_mock.get_piece = get_piece_side_effect

    ai = ai_engine.chess_ai()
    evaluate = ai.evaluate_board(game_state_mock, Player.PLAYER_2)  # AI is white player
    assert evaluate == -1050  # black king is -1000, black rook is -50


"""
System tests
"""


def test_fools_mate():
    """
    Black plays fools mate
    """
    game_state = chess_engine.game_state()
    moves = [
        ((1, 2), (2, 2)),  # f3
        ((6, 3), (5, 3)),  # e6
        ((1, 1), (3, 1)),  # g4
        ((7, 4), (3, 0))  # Qh4#
    ]
    for (start_pos, end_pos) in moves:
        game_state.move_piece(start_pos, end_pos, False)
    assert game_state.checkmate_stalemate_checker() == GameStatus.BLACK_WON
