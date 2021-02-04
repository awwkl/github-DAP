import sys
import os
import git
import pandas as pd

def clone_repos(option, lang_ext, max_repos_per_lang):
    repo_list = pd.read_csv(f'./repo-namelists/list_{lang_ext}.csv')

    if (option.lower() == "https"):
        git_url_prefix = "https://github.com/"
    elif (option.lower() == "ssh"):
        git_url_prefix = "git@github.com:"

    for id, repo_name in repo_list['repo_name'].items():
        if id >= max_repos_per_lang:
            break

        git_url = f'{git_url_prefix}{repo_name}'
        clone_dir = f'./code-repos/{lang_ext}/{id}'
        clone = f'git clone --quiet {git_url} {clone_dir}'

        # if repo has been cloned, do not clone again
        if os.path.exists(clone_dir):
            continue

        # clone the repo
        print(clone_dir, git_url)
        os.system(clone)

def clone_languages(option, langs_extension, max_repos_per_lang):
    for lang in langs_extension:
        clone_repos(option, lang, max_repos_per_lang)
