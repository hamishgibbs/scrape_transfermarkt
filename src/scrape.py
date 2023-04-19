import sys
import requests

headers = {'User-Agent': 
               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

def scrape(url, out_fn):

    response = requests.get(url, headers=headers)
    
    with open(out_fn, "w") as f:
        f.write(response.text)

if __name__ == "__main__":
    scrape(url=sys.argv[1], out_fn=sys.argv[-1])