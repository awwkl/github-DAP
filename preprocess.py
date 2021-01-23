import re
import os
import collections
import numpy as np
import pandas as pd

num_tokens_per_lang = 40
num_tokens_to_show = 15

counter_html = collections.Counter()
counter_java = collections.Counter()
counter_py = collections.Counter()
num_files = {'.html': 0, '.java': 0, '.py': 0}
top_tokens = {'.html': [], '.java': [], '.py': [], 'all': []}

def tokenize(filepath):
    f = open(filepath, 'rb')
    text = f.read().decode(errors='replace')

    # split by non-word characters, keep the matched pattern/delimiters
    tokens = re.split('(\W)', text)
    tokens = [x for x in tokens if (x != None and x.strip() != "")]
    return tokens

def build_token_dicts(dir_search='./code-repos'):
    dir_curr = os.path.dirname(__file__)                # pathname of this module
    root_dir = os.path.join(dir_curr, dir_search)
    
    for root, subdir, files in os.walk(root_dir):
        for file in files:
            ext = os.path.splitext(file)[-1].lower()
            if not ext in ['.html', '.java', '.py']:
                continue

            filepath = os.path.join(root, file)
            tokens = tokenize(filepath)
            
            num_files[ext] += 1
            lang_counters = {
                ".html": counter_html,
                ".java": counter_java,
                ".py": counter_py,
            }
            lang_counters[ext].update(tokens)

    
    df = pd.DataFrame()
    for lang, counter in lang_counters.items():
        print("Files with extension {%s}: %d" % (lang, num_files[lang]))
        df[lang] = [token for (token, count) in counter.most_common(num_tokens_per_lang)]
        
    df.to_csv('processed_data/top_tokens.csv')
    print("These are the top %d tokens for the 3 languages" % (num_tokens_to_show))
    print(df.head(n=num_tokens_to_show))
    print()

def numerical_vector(filepath):
    tokens = tokenize(filepath)
    num_tokens = len(tokens)

    counter = collections.Counter(tokens)
    vector = [counter[token] for token in top_tokens['all']]
    return vector

def build_dataset(dir_search='./code-repos'):
    top_tokens_df = pd.read_csv('processed_data/top_tokens.csv')
    for x in ['.html', '.java', '.py']:
        top_tokens[x] = list(top_tokens_df[x])
        top_tokens['all'] += top_tokens[x]
    
    dir_curr = os.path.dirname(__file__)            # pathname of this module
    root_dir = os.path.join(dir_curr, dir_search)

    num_features = len(top_tokens['all'])
    X = np.empty((0, num_features), dtype=np.int64)
    final_df = pd.DataFrame()
    labels = []

    for root, subdir, files in os.walk(root_dir):
        for file in files:
            ext = os.path.splitext(file)[-1].lower()
            if not ext in ['.html', '.java', '.py']:
                continue

            labels.append(ext)

            filepath = os.path.join(root, file)
            vector = numerical_vector(filepath)
            X = np.vstack((X, vector))

    final_df = pd.DataFrame(
        data=X,
        columns=list(range(num_features))
    )
    final_df['label'] = labels
    final_df.to_csv('processed_data/final_df.csv')
    print(final_df)

# if __name__ == "__main__":
def preprocess_repos():
    build_token_dicts('./code-repos')
    build_dataset()
