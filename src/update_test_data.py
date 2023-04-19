import sys
from scrape import scrape

if __name__ == "__main__":
    arg_len = int(len(sys.argv[1:])/2)
    for i in range(1, arg_len+1):
        scrape(
            url = sys.argv[i],
            out_fn = sys.argv[i+arg_len]
        )