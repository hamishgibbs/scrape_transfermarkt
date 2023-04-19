import os
import pandas as pd

seasons = [2016, 2017, 2018, 2019, 2020]
matchdays = range(1, 39)

rule all:
    input:
        "data/teams.csv",
        "data/stadiums.csv",
        "data/games.csv"

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
        temporary("data/games/html/season_{season}_matchday_{matchday}.html")
    params:
        url=get_game_url
    shell:
        "python {input} '{params.url}' {output}"

rule parse_games:
    input:
        "src/parse_games.py",
        "data/games/html/season_{season}_matchday_{matchday}.html"
    output:
        temporary("data/games/clean/season_{season}_matchday_{matchday}.csv")
    shell:
        "python {input} {output}"

rule concat_games:
    input:
        expand("data/games/clean/season_{season}_matchday_{matchday}.csv", season=seasons, matchday=matchdays)
    output:
        "data/games.csv"
    run:
        pd.concat([pd.read_csv(fn) for fn in input]).to_csv(output[0], index=False)

rule scrape_stadiums:
    input:
        "src/scrape.py"
    output:
        temporary("data/stadiums.html")
    params:
        url="https://www.transfermarkt.co.uk/premier-league/stadien/wettbewerb/GB1"
    shell:
        "python {input} {params.url} {output}"

rule parse_stadiums:
    input:
        "src/parse_stadiums.py",
        "data/stadiums.html"
    output:
        "data/stadiums.csv"
    shell:
        "python {input} {output}"

rule update_test_data:
    input: 
        "src/update_test_data.py"
    output:
        "tests/data/game_data.html",
        "tests/data/game_data_sold_out.html",
        "tests/data/game_data_attendance_missing.html",
        "tests/data/teams_data.html",
        "tests/data/stadium_data.html"
    params:
        "https://www.transfermarkt.co.uk/premier-league/spieltag/wettbewerb/GB1/saison_id/2019/spieltag/1",
        "https://www.transfermarkt.co.uk/premier-league/spieltag/wettbewerb/GB1/saison_id/2016/spieltag/1",
        "https://www.transfermarkt.co.uk/premier-league/spieltag/wettbewerb/GB1/saison_id/2019/spieltag/30",
        "https://www.transfermarkt.co.uk/premier-league/startseite/wettbewerb/GB1",
        "https://www.transfermarkt.co.uk/premier-league/stadien/wettbewerb/GB1"
    shell:
        "python {input} {params} {output}"