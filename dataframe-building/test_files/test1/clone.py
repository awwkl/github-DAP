import os
import git
import pandas as pd

def clone_repos(lang):
    repo_list = pd.read_csv(f'./repo-namelists/list_{lang}.csv')

    for id, repo_name in repo_list['repo_name'].items():
        git_url = f'git@github.com:{repo_name}.git'
        clone_dir = f'./code-repos/{lang}-{id}'

        # if repo has been cloned, do not clone again
        if os.path.exists(clone_dir):
            continue
        
        # clone the repo
        print(clone_dir, git_url)
        git.Repo.clone_from(git_url, clone_dir, depth=1)    # depth=1

languages = ['python', 'c++', 'html', 'java']

for lang in languages:
    clone_repos(lang)
