import sys
import pandas as pd

def main():

    stadiums = pd.read_csv(sys.argv[1])

    missing_coord_lu = pd.read_csv(sys.argv[2])

    missing_coord_lu.set_index("name", inplace=True)

    missing_stadiums = stadiums[pd.isna(stadiums["x"])]
    
    missing_stadiums.loc[:, "x"] = missing_coord_lu.loc[missing_stadiums["name"], "x"].to_list()
    missing_stadiums.loc[:, "y"] = missing_coord_lu.loc[missing_stadiums["name"], "y"].to_list()

    stadiums = pd.concat([stadiums[~pd.isna(stadiums["x"])], missing_stadiums])

    stadiums.to_csv(sys.argv[-1], index=False)

if __name__ == "__main__":
    main()