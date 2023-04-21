import sys
import pandas as pd

def main():

    games = pd.read_csv(sys.argv[1])

    match_sheets = pd.read_csv(sys.argv[2])

    stadiums = pd.read_csv(sys.argv[3])

    games = games.merge(match_sheets, on="match_sheet_id", how="left")

    stadiums = stadiums[["association", "season", "capacity", "x", "y"]]

    games = games.merge(stadiums, on=["association", "season"], how="left")

    games.drop(["association", "season", "stadium_url", "match_sheet_id"], axis=1, inplace=True)

    # Drop stadiums outside the UK based on OSGB bounding box: https://epsg.io/27700
    games = games[(games["x"] > -9) & (games["x"] < 2.01)]
    games = games[(games["y"] > 49.75) & (games["y"] < 61.01)]

    games.drop_duplicates(inplace=True)

    games.to_csv(sys.argv[-1], index=False)

if __name__ == "__main__":
    main()