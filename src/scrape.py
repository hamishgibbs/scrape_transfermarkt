import requests

def scrape(url, out_fn):

    headers = {'User-Agent': 
               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    response = requests.get(url, headers=headers)
    
    with open(out_fn, "w") as f:
        f.write(response.text)