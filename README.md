# DAP project stuff
<!-- ### Collaboration
- with Felice Png, Lee Yu Hao, Yap Bing Yu from Singapore Management University -->

### Explanation
- `repo-namelists/*` stores the names of github repos we wish to clone, scrapped from `scrape_repo_names.py`
- `clone.py` clones the repos listed in those files using https/ssh, with `depth=1` to shallow clone and avoid cloning previous revisions
- `code-repos/*` will house the newly cloned repos
- `.gitignore` ignores the `repos/` directory
- `preprocess.py` tokenizes the cloned repos and stores them as numerical vectors in `processed_data/*`

### Use
- `git clone` this repo
- `python engine.py` to run the program
- other features not implemented yet
