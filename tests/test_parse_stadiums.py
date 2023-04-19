from parse_stadiums import parse_stadium_data

def test_parse_stadium_data():

    res = parse_stadium_data("tests/data/stadium_data.html")

    assert res.shape == (1, 2)
    assert res.iloc[0]["name"] == "Anfield"
    assert res.iloc[0]["total_capacity"] == "54074"