import sys
import pandas as pd

def main():

    teams = pd.read_csv(sys.argv[1])

    games = pd.concat([pd.read_csv(x) for x in sys.argv[2:-1]])

    games_pl_teams = games[games["team_2"].isin(teams["url_stub"])]
    
    games_pl_teams.to_csv(sys.argv[-1], index=False)


if __name__ == "__main__":
    main()
