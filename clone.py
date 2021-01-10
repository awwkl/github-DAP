import os
import git
import pandas as pd

def clone_repos(lang):
    repo_list = pd.read_csv(f'./lists_of_repos/list_{lang}.csv')

    for id, repo_name in repo_list['repo_name'].items():
        git_url = f'git@github.com:{repo_name}.git'
        clone_dir = f'./repos/{lang}-{id}'

        # if repo has been cloned, do not clone again
        if os.path.exists(clone_dir):
            continue
        
        # clone the repo
        print(clone_dir, git_url)
        git.Repo.clone_from(git_url, clone_dir, depth=1)    # depth=1

languages = ['python', 'cpp']

for lang in languages:
    clone_repos(lang)
