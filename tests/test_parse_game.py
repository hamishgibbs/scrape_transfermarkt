from parse_games import parse_game_data

def test_parse_game_data():

    res = parse_game_data("tests/data/game_data.html")

    assert res.shape == (10, 5)
    assert res.iloc[0]["home_team"] == "fc-liverpool"
    assert res.iloc[-1]["away_team"] == "fc-chelsea"
    assert res.iloc[4]["attendance"] == "19784"