import sys
import os
import git
import pandas as pd

# for https
def clone_repos(lang, max_repos_per_lang=10):
    repo_list = pd.read_csv(f'./repo-namelists/list_{lang}.csv')

    for id, repo_name in repo_list['repo_name'].items():
        if id >= max_repos_per_lang:
            break
        git_url = f'https://github.com/{repo_name}'
        clone_dir = f'./code-repos/{lang}/{id}'
        clone = f'git clone --quiet {git_url} {clone_dir}'

        # if repo has been cloned, do not clone again
        if os.path.exists(clone_dir):
            continue
        
        # clone the repo
        print(clone_dir, git_url)
        os.system(clone)

def clone_languages(languages = ['html', 'java', 'python', 'c', 'c++', 'ruby', 'php']):
    for lang in languages:
        clone_repos(lang)
