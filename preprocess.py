import re
import os
import collections
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

# some global vars that are used by the functions, can be easily changed
num_tokens_per_lang = 20
num_tokens_to_show = 20

# path_curr = os.path.dirname(__file__)   # pathname of this module
# path_repos = os.path.join(path_curr, path_repos)

path_df_train = 'processed_data/df_train.csv'
path_df_valid = 'processed_data/df_valid.csv'
path_df_test = 'processed_data/df_test.csv'
path_repos = './code-repos'
path_dir_for_processed_data = './processed_data/'
path_file_list_full = path_dir_for_processed_data + 'file_list_full.csv'
path_file_list_subset = path_dir_for_processed_data + 'file_list_subset.csv'
path_file_list_train = path_dir_for_processed_data + 'file_list_train.csv'
path_file_list_valid = path_dir_for_processed_data + 'file_list_valid.csv'
path_file_list_test = path_dir_for_processed_data + 'file_list_test.csv'
path_top_tokens_per_lang = path_dir_for_processed_data + 'top_tokens_per_lang.csv'

# desired_file_extensions = ['.html', '.java', '.py', '.c', '.cpp', '.rb', '.php']
# counter_html = collections.Counter()
# counter_java = collections.Counter()
# counter_py = collections.Counter()
# counter_c = collections.Counter()
# counter_cpp = collections.Counter()
# counter_rb = collections.Counter()
# counter_php = collections.Counter()
# num_files = {'.html': 0, '.java': 0, '.py': 0, '.c': 0, '.cpp': 0, '.rb': 0, '.php': 0}
# top_tokens = {'.html': [], '.java': [], '.py': [], '.c': [], '.cpp': [], '.rb': [], '.php': [], 'all': []}

lang_exts_with_dot = []             # will be set by preprocess_repos(), the entry function for this module
num_files = {}
top_tokens = {'all': []}
lang_counters = {}


# if __name__ == "__main__":
def preprocess_repos(langs_extension):
    setup_global_vars(langs_extension)
    # print_global_vars()
    generate_file_lists()
    build_token_dicts()
    build_dataset()

def setup_global_vars(langs_extension):
    global lang_exts_with_dot
    lang_exts_with_dot = [f'.{x}' for x in langs_extension]
    for lang_ext in lang_exts_with_dot:
        num_files[lang_ext] = 0
        top_tokens[lang_ext] = []
        lang_counters[lang_ext] = collections.Counter()

# def print_global_vars():
#     print(lang_exts_with_dot)
#     print(num_files)
#     print(top_tokens)
#     print(lang_counters)


def generate_file_lists():
    file_list_full = []
    labels_full = []
    for root, subdir, files in os.walk(path_repos):
        for file in files:
            ext = os.path.splitext(file)[-1].lower()
            if not ext in lang_exts_with_dot:
                continue
            # if num_files[ext] >= 2000:  # max 2000 files for each lang
            #     continue
            num_files[ext] += 1
            filepath = os.path.join(root, file)
            file_list_full.append(filepath)
            labels_full.append(ext)

    df_file_list_full = pd.DataFrame()
    df_file_list_full['filepaths'] = file_list_full
    df_file_list_full['label'] = labels_full
    df_file_list_full.to_csv(path_file_list_full)

    num_files_per_lang = min(num_files.values()) // 100 * 100   # round down to next 100
    num_files_per_lang = min(2000, num_files_per_lang)          # do not use more than 2000
    df_file_list_subset = df_file_list_full.groupby('label').sample(num_files_per_lang)
    df_file_list_subset.to_csv(path_file_list_subset)
    
    # df_file_list_train = pd.DataFrame()
    # df_file_list_valid = pd.DataFrame()
    # df_file_list_test = pd.DataFrame()

    # produces a 60%, 20%, 20% split for training, validation and test sets
    # df_file_list_train['filepaths'], df_file_list_valid['filepaths'], df_file_list_test['filepaths'] = np.split(df_file_list_full['filepaths'].sample(frac=1), [int(.6*len(df_file_list_full['filepaths'])), int(.8*len(df_file_list_full['filepaths']))])

    df_file_list_train, df_file_list_test = train_test_split(df_file_list_subset, test_size=0.2, random_state=42)
    df_file_list_train, df_file_list_valid = train_test_split(df_file_list_train, test_size=0.25, random_state=42)

    df_file_list_train.to_csv(path_file_list_train)
    df_file_list_valid.to_csv(path_file_list_valid)
    df_file_list_test.to_csv(path_file_list_test)

    # print(df_file_list_full['label'].value_counts())
    # print(df_file_list_subset['label'].value_counts())
    # print(df_file_list_train['label'].value_counts())
    # print(df_file_list_valid['label'].value_counts())
    # print(df_file_list_test['label'].value_counts())

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
        if not ext in lang_exts_with_dot:
            continue
        try:
            tokens = tokenize(filepath)
        except:
            continue
        lang_counters[ext].update(tokens)
    
    df = pd.DataFrame()
    for lang, counter in lang_counters.items():
        print("Files with extension {%s}: %d" % (lang, num_files[lang]))
        df[lang] = [token for (token, count) in counter.most_common(num_tokens_per_lang)]
        
    df.to_csv(path_top_tokens_per_lang)
    print("These are the top %d tokens for the %d languages" % (num_tokens_to_show, len(lang_exts_with_dot)))
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
    for x in lang_exts_with_dot:
        top_tokens[x] = list(df_top_tokens[x])
        top_tokens['all'] += top_tokens[x]

    num_features = len(top_tokens['all'])

    df_train = pd.DataFrame()
    X_train = np.empty((0, num_features), dtype=np.uint32)
    y_train = []

    df_valid = pd.DataFrame()
    X_valid = np.empty((0, num_features), dtype=np.uint32)
    y_valid = []

    df_test = pd.DataFrame()
    X_test = np.empty((0, num_features), dtype=np.uint32)
    y_test = []

    df = pd.read_csv(path_file_list_train)
    filepaths = df['filepaths']
    for filepath in filepaths:
        ext = os.path.splitext(filepath)[-1].lower()
        if not ext in lang_exts_with_dot:
            continue

        try:
            vector = numerical_vector(filepath)
        except:
            continue
        y_train.append(ext)
        X_train = np.vstack((X_train, vector))

    df_train = pd.DataFrame(
        data=X_train,
        columns=top_tokens['all']
    )
    df_train['label'] = y_train
    df_train.to_csv(path_df_train, index=False)

    df = pd.read_csv(path_file_list_valid)
    filepaths = df['filepaths']
    for filepath in filepaths:
        ext = os.path.splitext(filepath)[-1].lower()
        if not ext in lang_exts_with_dot:
            continue

        try:
            vector = numerical_vector(filepath)
        except:
            continue
        y_valid.append(ext)
        X_valid = np.vstack((X_valid, vector))

    df_valid = pd.DataFrame(
        data=X_valid,
        columns=top_tokens['all']
    )
    df_valid['label'] = y_valid
    df_valid.to_csv(path_df_valid, index=False)

    df = pd.read_csv(path_file_list_test)
    filepaths = df['filepaths']
    for filepath in filepaths:
        ext = os.path.splitext(filepath)[-1].lower()
        if not ext in lang_exts_with_dot:
            continue

        try:
            vector = numerical_vector(filepath)
        except:
            continue
        y_test.append(ext)
        X_test = np.vstack((X_test, vector))

    df_test = pd.DataFrame(
        data=X_test,
        columns=top_tokens['all']
    )
    df_test['label'] = y_test
    df_test.to_csv(path_df_test, index=False)

    print("df_train.csv:")
    print(df_train['label'].value_counts())
    print("df_valid.csv:")
    print(df_valid['label'].value_counts())
    print("df_test.csv:")
    print(df_test['label'].value_counts())
