import chess_engine
from unittest.mock import patch, Mock
from Piece import Knight
from enums import Player

"""
Tests for the function get_valid_peaceful_moves in class Knight
"""


def test_knight_middle_empty():
    game_state_mock = Mock()
    game_state_mock.get_piece = Mock(return_value=Player.EMPTY)
    white_knight = Knight('n', 3, 4, Player.PLAYER_1)
    result = white_knight.get_valid_peaceful_moves(game_state_mock)
    assert set(result) == {(1, 3), (1, 5), (2, 2), (2, 6), (4, 2), (4, 6), (5, 3), (5, 5)}


def test_knight_right_empty():
    game_state_mock = Mock()
    game_state_mock.get_piece = Mock(return_value=Player.EMPTY)
    white_knight = Knight('n', 2, 0, Player.PLAYER_1)
    result = white_knight.get_valid_peaceful_moves(game_state_mock)
    result = [i for i in result if 0 <= i[0] < 8 and 0 <= i[1] < 8]
    assert set(result) == {(0, 1), (1, 2), (3, 2), (4, 1)}


def test_knight_upper_empty():
    game_state_mock = Mock()
    game_state_mock.get_piece = Mock(return_value=Player.EMPTY)
    black_knight = Knight('n', 7, 5, Player.PLAYER_2)
    result = black_knight.get_valid_peaceful_moves(game_state_mock)
    result = [i for i in result if 0 <= i[0] < 8 and 0 <= i[1] < 8]
    assert set(result) == {(5, 4), (5, 6), (6, 3), (6, 7)}


"""
Tests for the function get_valid_piece_takes in class Knight
"""


def test_knight_only_take_moves():
    game_state_mock = Mock()

    def get_piece_side_effect(row, col):
        if row == 3 and col == 3:
            return Player.PLAYER_1
        else:
            return Player.PLAYER_2

    # game_state_mock.get_piece = Mock(return_value=get_piece_side_effect)
    # game_state_mock.is_valid_piece = Mock(return_value=True)
    # game_state_mock.get_player = Mock(return_value=Player.PLAYER_2)
    # white_knight = Knight('n', 3, 3, Player.PLAYER_1)
    # result = white_knight.get_valid_piece_takes(game_state_mock)
    # result = [i for i in result if 0 <= i[0] < 8 and 0 <= i[1] < 8]
    # assert set(result) == {}

