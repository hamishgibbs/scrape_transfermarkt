import pandas as pd

def test_all_teams_are_in_teams():
    
    teams = pd.read_csv("data/teams.csv")
    games = pd.read_csv("data/games.csv")

    print(len(list(set(games["home_team"]))))

    assert set(games["home_team"]) - set(teams["url_stub"]) == set()
    