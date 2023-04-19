import pandas as pd

def test_all_teams_in_games_are_in_teams(teams_fn, games_fn):
    
    teams = pd.read_csv(teams_fn)
    games = pd.read_csv(games_fn)

    print(len(list(set(games["home_team"]))))

    assert set(games["home_team"]) - set(teams["url_stub"]) == set()
    assert set(teams["url_stub"]) - set(games["home_team"]) == set()
    assert set(games["away_team"]) - set(teams["url_stub"]) == set()
    assert set(teams["url_stub"]) - set(games["away_team"]) == set()
    
def test_all_attendances_are_lte_max_attendance_per_stadium(games_fn, stadiums_fn):

    # Maximum level of overselling allowed
    MAX_ATTENDANCE_THRESHOLD = 1.01

    games = pd.read_csv(games_fn)
    stadiums = pd.read_csv(stadiums_fn)

    games = pd.merge(games, stadiums, how="left", left_on="home_team", right_on="team")

    games.dropna(subset=["attendance"], inplace=True)

    pd.set_option('display.max_columns', None)

    games["attendance_proportion"] = (games["attendance"] - games["capacity"]) / games["capacity"]

    print(games[~(games["attendance_proportion"] <= MAX_ATTENDANCE_THRESHOLD)])

    assert games["attendance_proportion"].max() <= MAX_ATTENDANCE_THRESHOLD