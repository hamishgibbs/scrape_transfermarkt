import re
import sys

def main():

    languages = ["R", "py"]

    with open(sys.argv[1], "r") as f:
        snakefile = f.read()
    
    with open(sys.argv[2], "r") as f:
        svg = f.read()
    
    targets = re.findall(r'rule (.*?):\n.*?input:\n.*?[\"|\'](.*?)[\"|\'],', snakefile)

    for target in targets:
        ext = target[1].split(".")[-1]
        if ext in languages:

            try:
                text_element = re.findall(f'(<text .*?{target[0]}<\/text>)', svg)[0]
                
                svg = svg.replace(text_element, f'<a href="/{target[1]}">{text_element}</a>')
            except IndexError:
                pass
        
    with open(sys.argv[-1], "w") as f:
        f.write(svg)

    
if __name__ == "__main__":
    main()
