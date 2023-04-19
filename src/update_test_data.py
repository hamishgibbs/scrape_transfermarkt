import sys
from scrape import scrape

if __name__ == "__main__":
    scrape(
        url = "https://www.transfermarkt.co.uk/premier-league/spieltag/wettbewerb/GB1/saison_id/2019/spieltag/1",
        out_fn = sys.argv[-2]
    )

    scrape(
        url = "https://www.transfermarkt.co.uk/premier-league/startseite/wettbewerb/GB1",
        out_fn = sys.argv[-1]
    )