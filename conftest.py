def pytest_addoption(parser):
    parser.addoption("--teams_fn", action="store", default="default teams_fn")
    parser.addoption("--games_fn", action="store", default="default games_fn")
    parser.addoption("--stadiums_fn", action="store", default="default stadiums_fn")
    parser.addoption("--stadiums_geo_fn", action="store", default="default stadiums_geo_fn")

def pytest_generate_tests(metafunc):
    option_value = metafunc.config.option.teams_fn
    if 'teams_fn' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("teams_fn", [option_value])
    
    option_value = metafunc.config.option.games_fn
    if 'games_fn' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("games_fn", [option_value])
    
    option_value = metafunc.config.option.stadiums_fn
    if 'stadiums_fn' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("stadiums_fn", [option_value])
    
    option_value = metafunc.config.option.stadiums_geo_fn
    if 'stadiums_geo_fn' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("stadiums_geo_fn", [option_value])