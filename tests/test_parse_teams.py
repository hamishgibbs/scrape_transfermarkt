from src.parse_teams_data import parse_teams_data

def test_parse_teams_data():

    parse_teams_data("tests/data/teams_data.html")

    assert False