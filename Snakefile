import os
import pandas as pd

seasons = [2016, 2017, 2018, 2019, 2020]
matchdays = range(1, 39)

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