from src.parse_game_data import parse_game_data

def test_parse_game_data():

    parse_game_data("tests/data/game_data.html")

    assert False