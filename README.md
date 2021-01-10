# DAP project stuff
<!-- ### Collaboration
- with Felice Png, Lee Yu Hao, Yap Bing Yu from Singapore Management University -->

### Explanation
- `lists_of_repos/*` stores the names of github repos we wish to clone
- `clone.py` clones the repos listed in those files, with `depth=1` to shallow clone and avoid cloning previous revisions
- `repos/*` will house the newly cloned repos
- `.gitignore` ignores the `repos/` directory
- `process.py` is incomplete, meant to process the cloned repos
- `scrape.py` is incomplete, meant to build our list of github repos we wish to clone into `lists_of_repos/*`

### Use
- `git clone` this repo
- `python clone.py` to test the cloning of repos
- other features not implemented yet