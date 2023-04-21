import pandas as pd
import numpy as np
from parse_stadiums import parse_stadium_data

def test_parse_stadium_data():

    res = parse_stadium_data("tests/data/stadium_data_3299_2015.html")

    expected = pd.Series({
        "association": "3299",
        "season": "2015",
        "name": "Wembley Stadium",
        "capacity": 90000,
        "seats": 90000,
        "x": -0.2795188,
        "y": 51.5560208
    }, name=0)

    assert res.shape == (1, 7)
    pd.testing.assert_series_equal(res.iloc[0, :], expected)

    res = parse_stadium_data("tests/data/stadium_data_3008_2018.html")

    expected = pd.Series({
        "association": "3008",
        "season": "2018",
        "name": "MKM Stadium",
        "capacity": 25586,
        "seats": 25586,
        "x": np.nan,
        "y": np.nan
    }, name=0)

    assert res.shape == (1, 7)
    pd.testing.assert_series_equal(res.iloc[0, :], expected)

