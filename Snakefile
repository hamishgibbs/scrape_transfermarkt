import os
import pandas as pd

TEAM_DATA_PATH="data/teams.csv"

if os.path.exists(TEAM_DATA_PATH):
    team_urls = pd.read_csv("data/teams.csv")["url_stub"].to_list()
else:
    team_urls = []

seasons = [2016, 2017, 2018, 2019, 2020]

rule all:
    input:
        "data/teams.csv",
        expand("data/games/clean/{team}_{season}.csv", team=team_urls, season=seasons)

rule scrape_teams_data:
    input:
        "src/scrape.py"
    output:
        temporary("data/teams.html")
    params:
        url="https://www.transfermarkt.co.uk/premier-league/startseite/wettbewerb/GB1"
    shell:
        "python {input} {params.url} {output}"

rule parse_teams_data:
    input:
        "src/parse_teams_data.py",
        "data/teams.html"
    output:
        "data/teams.csv"
    shell:
        "python {input} {output}"

def get_game_url(wildcards):
    return f"https://www.transfermarkt.co.uk/{wildcards.team}/spielplandatum/verein/985/plus/1?saison_id={wildcards.season}&wettbewerb_id=&day=&heim_gast=&punkte=&datum_von=-&datum_bis=-"

rule scrape_game_data:
    input:
        "src/scrape.py"
    output:
        "data/games/html/{team}_{season}.html"
    params:
        url=get_game_url
    shell:
        "python {input} '{params.url}' {output}"

rule parse_game_data:
    input:
        "src/parse_game_data.py",
        "data/games/html/{team}_{season}.html"
    output:
        "data/games/clean/{team}_{season}.csv"
    shell:
        "python {input} {output}"

rule update_test_data:
    input: 
        "src/update_test_data.py"
    output:
        "tests/data/game_data.html",
        "tests/data/teams_data.html"
    shell:
        "python {input} {output}"