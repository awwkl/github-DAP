import re
import collections
import pandas as pd

lang_exts_with_dot = []
top_tokens = {'all': []}
path_top_tokens_per_lang = './files/top_tokens_per_lang.csv'

def setup():
    global lang_exts_with_dot, top_tokens
    langs_extension = ['html', 'java', 'py', 'c', 'cpp', 'rb', 'php']
    lang_exts_with_dot = [f'.{x}' for x in langs_extension]

    df_top_tokens = pd.read_csv(path_top_tokens_per_lang)
    for x in lang_exts_with_dot:
        top_tokens[x] = list(df_top_tokens[x])
        top_tokens['all'] += top_tokens[x]

    # remove duplicated tokens from top_tokens['all']
    top_tokens['all'] = list(set(top_tokens['all']))

def get_top_tokens():
    return top_tokens

def tokenize(text):
    # split by non-word characters, keep the matched pattern/delimiters
    tokens = re.split('(\W)', text)
    tokens = [x for x in tokens if (x != None and x.strip() != "")]
    return tokens

def vectorize(tokens):
    num_tokens = len(tokens)

    counter = collections.Counter(tokens)
    vector = [counter[token] for token in top_tokens['all']]
    return vector

