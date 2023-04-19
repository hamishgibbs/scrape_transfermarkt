from bs4 import BeautifulSoup

def parse_team_name(td):
    return td.find_all('a')[0].get("title")

def parse_table(fn):
    
    with open(fn, "r") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    table = soup.find_all(class_="responsive-table")[0]
    
    return table.find_all('tbody')[0].find_all('tr')