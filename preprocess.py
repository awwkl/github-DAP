import re
import os
import collections
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

# some global vars that are used by the functions, can be easily changed
num_tokens_per_lang = 40
num_tokens_to_show = 20

# path_curr = os.path.dirname(__file__)   # pathname of this module
# path_repos = os.path.join(path_curr, path_repos)

path_df_train = 'processed_data/df_train.csv'
path_df_test = 'processed_data/df_test.csv'
path_repos = './code-repos'
path_dir_for_processed_data = './processed_data/'
path_file_list_full = path_dir_for_processed_data + 'file_list_full.csv'
path_file_list_train = path_dir_for_processed_data + 'file_list_train.csv'
path_file_list_test = path_dir_for_processed_data + 'file_list_test.csv'
path_top_tokens_per_lang = path_dir_for_processed_data + 'top_tokens_per_lang.csv'

desired_file_extensions = ['.html', '.java', '.py', '.c', '.cpp', '.rb', '.php']
counter_html = collections.Counter()
counter_java = collections.Counter()
counter_py = collections.Counter()
counter_c = collections.Counter()
counter_cpp = collections.Counter()
counter_rb = collections.Counter()
counter_php = collections.Counter()
num_files = {'.html': 0, '.java': 0, '.py': 0, '.c': 0, '.cpp': 0, '.rb': 0, '.php': 0}
top_tokens = {'.html': [], '.java': [], '.py': [], '.c': [], '.cpp': [], '.rb': [], '.php': [], 'all': []}

# if __name__ == "__main__":
def preprocess_repos():
    generate_file_lists()
    build_token_dicts()
    build_dataset()

def generate_file_lists():
    file_list_full = []
    for root, subdir, files in os.walk(path_repos):
        for file in files:
            ext = os.path.splitext(file)[-1].lower()
            if not ext in ['.html', '.java', '.py', '.c', '.cpp', '.rb', '.php']:
                continue
            if num_files[ext] >= 2000:  # max 1000 files for each lang
                continue
            num_files[ext] += 1
            filepath = os.path.join(root, file)
            file_list_full.append(filepath)

    df_file_list_full = pd.DataFrame()
    df_file_list_full['filepaths'] = file_list_full
    df_file_list_full.to_csv(path_file_list_full)

    df_file_list_train = pd.DataFrame()
    df_file_list_test = pd.DataFrame()
    df_file_list_train['filepaths'], df_file_list_test['filepaths'] = train_test_split(df_file_list_full['filepaths'])
    df_file_list_train.to_csv(path_file_list_train)
    df_file_list_test.to_csv(path_file_list_test)

def tokenize(filepath):
    f = open(filepath, 'rb')
    text = f.read().decode(errors='replace')

    # split by non-word characters, keep the matched pattern/delimiters
    tokens = re.split('(\W)', text)
    tokens = [x for x in tokens if (x != None and x.strip() != "")]
    return tokens

def build_token_dicts(dir_search='./code-repos'):
    df = pd.read_csv(path_file_list_train)
    filepaths = df['filepaths']

    for filepath in filepaths:
        ext = os.path.splitext(filepath)[-1].lower()
        if not ext in ['.html', '.java', '.py', '.c', '.cpp', '.rb', '.php']:
            continue
        try:
            tokens = tokenize(filepath)
        except:
            continue
        lang_counters = {
            ".html": counter_html,
            ".java": counter_java,
            ".py": counter_py,
            ".c": counter_c,
            ".cpp": counter_cpp,
            ".rb": counter_rb,
            ".php": counter_php,
        }
        lang_counters[ext].update(tokens)
    
    df = pd.DataFrame()
    for lang, counter in lang_counters.items():
        print("Files with extension {%s}: %d" % (lang, num_files[lang]))
        df[lang] = [token for (token, count) in counter.most_common(num_tokens_per_lang)]
        
    df.to_csv(path_top_tokens_per_lang)
    print("These are the top %d tokens for the 7 languages" % (num_tokens_to_show))
    print(df.head(n=num_tokens_to_show))
    print()

def numerical_vector(filepath):
    tokens = tokenize(filepath)
    num_tokens = len(tokens)

    counter = collections.Counter(tokens)
    vector = [counter[token] for token in top_tokens['all']]
    return vector

def build_dataset():
    df_top_tokens = pd.read_csv(path_top_tokens_per_lang)
    for x in ['.html', '.java', '.py', '.c', '.cpp', '.rb', '.php']:
        top_tokens[x] = list(df_top_tokens[x])
        top_tokens['all'] += top_tokens[x]

    num_features = len(top_tokens['all'])

    df_train = pd.DataFrame()
    X_train = np.empty((0, num_features))
    y_train = []

    df_test = pd.DataFrame()
    X_test = np.empty((0, num_features))
    y_test = []

    df = pd.read_csv(path_file_list_train)
    filepaths = df['filepaths']
    for filepath in filepaths:
        ext = os.path.splitext(filepath)[-1].lower()
        if not ext in ['.html', '.java', '.py', '.c', '.cpp', '.rb', '.php']:
            continue

        y_train.append(ext)
        vector = numerical_vector(filepath)
        X_train = np.vstack((X_train, vector))

    df_train = pd.DataFrame(
        data=X_train,
        columns=list(range(num_features))
    )
    df_train['label'] = y_train
    df_train.to_csv(path_df_train, index=False)
    print(df_train)

    df = pd.read_csv(path_file_list_test)
    filepaths = df['filepaths']
    for filepath in filepaths:
        ext = os.path.splitext(filepath)[-1].lower()
        if not ext in ['.html', '.java', '.py', '.c', '.cpp', '.rb', '.php']:
            continue

        y_test.append(ext)
        vector = numerical_vector(filepath)
        X_test = np.vstack((X_test, vector))

    df_test = pd.DataFrame(
        data=X_test,
        columns=list(range(num_features))
    )
    df_test['label'] = y_test
    df_test.to_csv(path_df_test, index=False)
    print(df_test)
