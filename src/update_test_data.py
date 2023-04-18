import sys
from scrape import scrape

if __name__ == "__main__":
    scrape(
        url = "https://www.transfermarkt.co.uk/manchester-united/spielplandatum/verein/985/plus/1?saison_id=2019&wettbewerb_id=&day=&heim_gast=&punkte=&datum_von=-&datum_bis=-",
        out_fn = sys.argv[-2]
    )

    scrape(
        url = "https://www.transfermarkt.co.uk/premier-league/startseite/wettbewerb/GB1",
        out_fn = sys.argv[-1]
    )