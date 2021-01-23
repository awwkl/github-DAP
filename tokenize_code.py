import re
import os
import collections
import numpy as np

def tokenize(filepath):
    print(filepath)
    f = open(filepath, 'rb')
    text = f.read().decode(errors='replace')

    # split by non-word characters, keep the matched pattern/delimiters
    tokens = re.split('(\W)', text)
    tokens = [x for x in tokens if (x != None and x.strip() != "")]

    # for token in tokens:
    #     print(token)
    return tokens        

def build_token_dicts(dir_search='./code-repos'):
    dir_curr = os.path.dirname(__file__)                # pathname of this module
    root_dir = os.path.join(dir_curr, dir_search)

    counter_html = collections.Counter()
    counter_java = collections.Counter()
    counter_py = collections.Counter()

    for root, subdir, files in os.walk(root_dir):
        for file in files:
            ext = os.path.splitext(file)[-1].lower()
            if not ext in ['.html', '.java', '.py']:
                continue

            filepath = os.path.join(root, file)
            tokens = tokenize(filepath)
            
            lang_counters = {
                ".html": counter_html,
                ".java": counter_java,
                ".py": counter_py,
            }
            lang_counters[ext].update(tokens)

    for lang, counter in lang_counters.items():
        print("These are the top tokens in files with extension {%s}" %lang)
        for token, count in counter.most_common(50):
            print("%s: %03d" %(token, count))
        print()

if __name__ == "__main__":
    build_token_dicts('./code-repos')
