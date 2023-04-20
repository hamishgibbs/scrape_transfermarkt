import pandas as pd

def test_only_pl_teams_are_in_games(teams_fn, games_fn):
    
    teams = pd.read_csv(teams_fn)
    games = pd.read_csv(games_fn)

    assert set(games["team_1"]) - set(teams["url_stub"]) == set()
    assert set(teams["url_stub"]) - set(games["team_1"]) == set()
    assert set(games["team_2"]) - set(teams["url_stub"]) == set()
    assert set(teams["url_stub"]) - set(games["team_2"]) == set()
    
def test_all_match_sheet_ids_are_repeated_lte_twice(games_fn):

    games = pd.read_csv(games_fn)

    assert all(games["match_sheet_id"].value_counts() <= 2)
