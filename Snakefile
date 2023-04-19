import os
import pandas as pd

seasons = [2016, 2017, 2018, 2019, 2020]
matchdays = range(1, 39)

rule all:
    input:
        "data/stadiums.csv",
        expand("data/games/clean/season_{season}_matchday_{matchday}.csv", season=seasons, matchday=matchdays)

rule scrape_teams:
    input:
        "src/scrape.py"
    output:
        temporary("data/teams.html")
    params:
        url="https://www.transfermarkt.co.uk/premier-league/startseite/wettbewerb/GB1"
    shell:
        "python {input} {params.url} {output}"

rule parse_teams:
    input:
        "src/parse_teams.py",
        "data/teams.html"
    output:
        "data/teams.csv"
    shell:
        "python {input} {output}"

def get_game_url(wildcards):
    return f"https://www.transfermarkt.co.uk/premier-league/spieltag/wettbewerb/GB1/saison_id/{wildcards.season}/spieltag/{wildcards.matchday}"

rule scrape_games:
    input:
        "src/scrape.py"
    output:
        "data/games/html/season_{season}_matchday_{matchday}.html"
    params:
        url=get_game_url
    shell:
        "python {input} '{params.url}' {output}"

rule parse_games:
    input:
        "src/parse_games.py",
        "data/games/html/season_{season}_matchday_{matchday}.html"
    output:
        "data/games/clean/season_{season}_matchday_{matchday}.csv"
    shell:
        "python {input} {output}"

rule scrape_stadiums:
    input:
        "src/scrape_stadiums.py",
        "data/teams.csv"
    output:
        "data/stadiums.csv"
    shell:
        "python {input} {output}"


rule update_test_data:
    input: 
        "src/update_test_data.py"
    output:
        "tests/data/game_data.html",
        "tests/data/teams_data.html",
        "tests/data/stadium_data.html"
    params:
        "https://www.transfermarkt.co.uk/premier-league/spieltag/wettbewerb/GB1/saison_id/2019/spieltag/1",
        "https://www.transfermarkt.co.uk/premier-league/startseite/wettbewerb/GB1",
        "https://www.transfermarkt.co.uk/fc-liverpool/stadion/verein/31/saison_id/2019"
    shell:
        "python {input} {params} {output}"