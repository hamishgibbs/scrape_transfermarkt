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

    # Drop stadiums outside the UK based on OSGB bounding box: https://epsg.io/27700
    stadiums[(stadiums["x"] > -9) & (stadiums["x"] < 2.01)]
    stadiums[(stadiums["y"] > 49.75) & (stadiums["y"] < 61.01)]

    stadiums.to_csv(sys.argv[-1], index=False)

if __name__ == "__main__":
    main()