from parse_stadiums import parse_stadium_data

def test_parse_stadium_data():

    res = parse_stadium_data("tests/data/stadium_data.html")

    assert res.shape == (20, 4)
    assert res.iloc[0]["team"] == "manchester-united"
    assert res.iloc[0]["name"] == "Old Trafford"
    assert res.iloc[0]["capacity"] == "74879"
    assert res.iloc[0]["seats"] == "74879"
    assert res.iloc[-1]["team"] == "afc-bournemouth"
    assert res.iloc[-1]["name"] == "Vitality Stadium"
    assert res.iloc[-1]["capacity"] == "11329"
    assert res.iloc[-1]["seats"] == "11329"