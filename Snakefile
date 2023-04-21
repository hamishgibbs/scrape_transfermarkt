import os
import pandas as pd

seasons = [2015, 2016, 2017, 2018, 2019, 2020]

rule all:
    input:
        "output/games.csv",
        "output/stadiums.geojson",
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
    return f"https://www.transfermarkt.co.uk/{wildcards.team}/spielplandatum/verein/{wildcards.association}/plus/0?saison_id={wildcards.season}&wettbewerb_id=&day=&heim_gast=&punkte=&datum_von=-&datum_bis=-"

rule scrape_games:
    input:
        "src/scrape.py",
        "data/teams.csv"
    output:
        "data/games/html/{team}_{association}_{season}.html"
    params:
        url=get_game_url
    shell:
        "python {input[0]} '{params.url}' {output}"

rule parse_games:
    input:
        "src/parse_games.py",
        "data/games/html/{team}_{association}_{season}.html"
    output:
        temporary("data/games/clean/{team}_{association}_{season}.csv")
    shell:
        "python {input} {output}"

def get_team_names():
    fn = "data/teams.csv"
    if os.path.exists(fn):
        teams = pd.read_csv(fn)
        return (teams["url_stub"] + "_" + teams["association"].astype(str)).to_list()
    else:
        return []

rule concat_games:
    input:
        "src/concat_games.py",
        "data/teams.csv",
        expand("data/games/clean/{team_association}_{season}.csv", team_association=get_team_names(), season=seasons)
    output:
        "data/games_concat.csv"
    shell:
        "python {input} {output}"

rule games_qa:
    input:
        "tests/qa/test_games_qa.py",
        "data/teams.csv",
        "data/games_concat.csv",
    output:
        "data/games_qa_success.txt"
    shell:
        "python -m pytest {input[0]} -vv --teams_fn {input[1]} --games_fn {input[2]} | tee {output}"

def get_match_sheet_url(wildcards):
    return f"https://www.transfermarkt.co.uk/spielbericht/index/spielbericht/{wildcards.id}"

rule scrape_match_sheets:
    input:
        "src/scrape.py",
        "data/games_concat.csv"
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
    fn = "data/games_concat.csv"
    if os.path.exists(fn):
        return pd.read_csv("data/games_concat.csv")["match_sheet_id"].to_list()
    else:
        return []

rule concat_match_sheets:
    input:
        "data/games_concat.csv",
        expand("data/match_sheets/clean/match_sheet_{id}.csv", id=get_match_sheet_ids())
    output:
        "data/match_sheets.csv"
    run:
        pd.concat([pd.read_csv(fn) for fn in input[1:]]).to_csv(output[0], index=False)

def get_stadium_url(wildcards):
    return f"https://www.transfermarkt.co.uk/stadion/stadion/verein/{wildcards.association}/saison_id/{wildcards.season}"

rule scrape_stadiums:
    input:
        "src/scrape.py",
        "data/match_sheets.csv"
    output:
        "data/stadiums/html/stadium_{association}_{season}.html"
    params:
        url=get_stadium_url
    shell:
        "python {input[0]} {params.url} {output}"

rule parse_stadiums:
    input:
        "src/parse_stadiums.py",
        "data/stadiums/html/stadium_{association}_{season}.html"
    output:
        temporary("data/stadiums/clean/stadium_{association}_{season}.csv")
    shell:
        "python {input} {output}"

def get_stadium_names():
    fn = "data/match_sheets.csv"
    if os.path.exists(fn):
        match_sheets = pd.read_csv(fn)
        return (match_sheets["association"].astype(str) + "_" + match_sheets["season"].astype(str)).to_list()
    else:
        return []
    
rule concat_stadiums:
    input:
        "data/match_sheets.csv",
        expand("data/stadiums/clean/stadium_{association_season}.csv", association_season=get_stadium_names())
    output:
        "data/stadiums_concat.csv"
    run:
        pd.concat([pd.read_csv(fn) for fn in input[1:]]).drop_duplicates().to_csv(output[0], index=False)

rule fill_missing_stadium_coords:
    input:
        "src/fill_missing_stadium_coords.py",
        "data/stadiums_concat.csv",
        "data/geo/stadium_missing_coord_lookup.csv"
    output:
        "data/stadiums.csv"
    shell:
        "python {input} {output}"

rule join_games_stadiums:
    input:
        "src/join_games_stadiums.py",
        "data/games_concat.csv",
        "data/match_sheets.csv",
        "data/stadiums.csv"
    output:
        "output/games.csv"
    shell:
        "python {input} {output}"

rule scrape_stadiums_geo:
    input:
        "src/osm_stadiums.R",
        "data/stadiums.csv",
        "data/geo/osm_stadium_name_lookup.csv"
    output:
        "output/stadiums.geojson"
    shell:
        "Rscript {input} {output}"

rule update_test_data:
    input: 
        "src/update_test_data.py"
    output:
        "tests/data/teams_data.html",
        "tests/data/tottenham-hotspur_game_data.html",
        "tests/data/match_sheet_data_3194823.html",
        "tests/data/stadium_data_3299_2015.html",
        "tests/data/stadium_data_3008_2018.html"
    params:
        "'https://www.transfermarkt.co.uk/premier-league/startseite/wettbewerb/GB1'",
        "'https://www.transfermarkt.co.uk/tottenham-hotspur/spielplandatum/verein/148/plus/0?saison_id=2019&wettbewerb_id=&day=&heim_gast=&punkte=&datum_von=-&datum_bis=-'",
        "'https://www.transfermarkt.co.uk/spielbericht/index/spielbericht/3194823'",
        "'https://www.transfermarkt.co.uk/stadion/stadion/verein/3299/saison_id/2015'",
        "'https://www.transfermarkt.co.uk/stadion/stadion/verein/3008/saison_id/2018'"
    shell:
        "python {input} {params} {output}"

rule rulegraph:
    input:
        "Snakefile"
    output:
        "rulegraph.svg"
    shell:
        "snakemake --rulegraph | dot -Tsvg > {output}"