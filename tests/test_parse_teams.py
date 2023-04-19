from parse_teams import parse_teams_data

def test_parse_teams_data():

    res = parse_teams_data("tests/data/teams_data.html")

    assert res.shape == (20, 2)