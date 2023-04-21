import pandas as pd
import numpy as np
from parse_match_sheet import parse_match_sheet
from datetime import datetime

def test_parse_match_sheet():

    res = parse_match_sheet("tests/data/match_sheet_data_3194823.html")

    expected = pd.Series({
        "match_sheet_id": "3194823",
        "stadium_name": "Tottenham Hotspur Stadium",
        "stadium_url": "https://www.transfermarkt.co.uk/stadion/stadion/verein/148/saison_id/2019",
        "association": "148", 
        "season": "2019"
    }, name=0)

    assert res.shape == (1, 5)
    pd.testing.assert_series_equal(res.iloc[0, :], expected)