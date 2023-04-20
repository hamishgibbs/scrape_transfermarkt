import os
import pandas as pd

seasons = [2015, 2016, 2017, 2018, 2019, 2020]

rule all:
    input:
        "data/qa_success.txt",
        "rulegraph.svg"

def get_teams_url(wildcards):
    return f"https://www.transfermarkt.co.uk/premier-league/startseite/wettbewerb/GB1/plus/?saison_id={wildcards.season}"

rule scrape_teams:
    input:
        "src/scrape.py"
    output:
        temporary("data/teams_{season}.html")
    params:
        url=get_teams_url
    shell:
        "python {input} {params.url} {output}"

rule parse_teams:
    input:
        "src/parse_teams.py",
        "data/teams_{season}.html"
    output:
        temporary("data/teams_{season}.csv")
    shell:
        "python {input} {output}"

rule concat_teams:
    input:
        expand("data/teams_{season}.csv", season=seasons)
    output:
        "data/teams.csv"
    run:
        pd.concat([pd.read_csv(fn) for fn in input]).drop_duplicates().to_csv(output[0], index=False)

def get_game_url(wildcards):
    return f"https://www.transfermarkt.co.uk/{wildcards.team}/spielplandatum/verein/148/plus/0?saison_id={wildcards.season}&wettbewerb_id=&day=&heim_gast=&punkte=&datum_von=-&datum_bis=-"

rule scrape_games:
    input:
        "src/scrape.py",
        "data/teams.csv"
    output:
        "data/games/html/{team}_{season}.html"
    params:
        url=get_game_url
    shell:
        "python {input[0]} '{params.url}' {output}"

rule parse_games:
    input:
        "src/parse_games.py",
        "data/games/html/{team}_{season}.html"
    output:
        temporary("data/games/clean/{team}_{season}.csv")
    shell:
        "python {input} {output}"

def get_team_names():
    teams = pd.read_csv("data/teams.csv")
    return teams["url_stub"].to_list()

rule concat_games:
    input:
        expand("data/games/clean/{team}_{season}.csv", team=get_team_names(), season=seasons)
    output:
        "data/games.csv"
    run:
        pd.concat([pd.read_csv(fn) for fn in input]).to_csv(output[0], index=False)

def get_match_sheet_url(wildcards):
    return f"https://www.transfermarkt.co.uk/spielbericht/index/spielbericht/{wildcards.id}"

rule scrape_match_sheets:
    input:
        "src/scrape.py",
        "data/games.csv"
    output:
        "data/match_sheets/html/match_sheet_{id}.html"
    params:
        url=get_match_sheet_url
    shell:
        "python {input[0]} '{params.url}' {output}"

rule parse_match_sheets:
    input:
        "src/parse_match_sheet.py",
        "data/match_sheets/html/match_sheet_{id}.html"
    output:
        temporary("data/match_sheets/clean/match_sheet_{id}.csv")
    shell:
        "python {input} {output}"

def get_match_sheet_ids():
    fn = "data/games.csv"
    if os.path.exists(fn):
        return pd.read_csv("data/games.csv")["match_sheet_id"].to_list()
    else:
        return []

rule concat_match_sheets:
    input:
        expand("data/match_sheets/clean/match_sheet_{id}.csv", id=get_match_sheet_ids())
    output:
        "data/match_sheets.csv"
    run:
        pd.concat([pd.read_csv(fn) for fn in input]).to_csv(output[0], index=False)

def get_stadium_url(wildcards):
    return f"https://www.transfermarkt.co.uk/premier-league/stadien/wettbewerb/GB1/plus/?saison_id={wildcards.season}"

rule scrape_stadiums:
    input:
        "src/scrape.py"
    output:
        temporary("data/stadiums_{season}.html")
    params:
        url=get_stadium_url
    shell:
        "python {input} {params.url} {output}"

rule parse_stadiums:
    input:
        "src/parse_stadiums.py",
        "data/stadiums_{year}.html"
    output:
        temporary("data/stadiums_{year}.csv")
    shell:
        "python {input} {output}"

rule concat_stadiums:
    input:
        expand("data/stadiums_{season}.csv", season=seasons)
    output:
        "data/stadiums.csv"
    run:
        pd.concat([pd.read_csv(fn) for fn in input]).drop_duplicates().to_csv(output[0], index=False)

rule scrape_stadiums_geo:
    input:
        "src/osm_stadiums.R",
        "data/stadiums.csv",
        "data/geo/osm_stadium_name_lookup.csv"
    output:
        "data/geo/stadiums.geojson"
    shell:
        "Rscript {input} {output}"

rule update_test_data:
    input: 
        "src/update_test_data.py"
    output:
        "tests/data/teams_data.html",
        "tests/data/tottenham-hotspur_game_data.html",
        "tests/data/match_sheet_data_3194823.html",
        "tests/data/stadium_data.html"
    params:
        "'https://www.transfermarkt.co.uk/premier-league/startseite/wettbewerb/GB1'",
        "'https://www.transfermarkt.co.uk/tottenham-hotspur/spielplandatum/verein/148/plus/0?saison_id=2019&wettbewerb_id=&day=&heim_gast=&punkte=&datum_von=-&datum_bis=-'",
        "'https://www.transfermarkt.co.uk/spielbericht/index/spielbericht/3194823'",
        "'https://www.transfermarkt.co.uk/premier-league/stadien/wettbewerb/GB1'"
    shell:
        "python {input} {params} {output}"

rule qa:
    input:
        "tests/qa/test_games_qa.py",
        "tests/qa/test_stadiums_qa.py",
        "data/teams.csv",
        "data/games.csv",
        "data/stadiums.csv",
        "data/geo/stadiums.geojson"
    output:
        "data/qa_success.txt"
    shell:
        "python -m pytest tests/qa -k _qa -vv --teams_fn {input[2]} --games_fn {input[3]} --stadiums_fn {input[4]} --stadiums_geo_fn {input[5]} | tee {output}"

rule rulegraph:
    input:
        "Snakefile"
    output:
        "rulegraph.svg"
    shell:
        "snakemake --rulegraph | dot -Tsvg > {output}"