# Programming Language Classifer
#### Data Associate Project (DAP) of SMU Business Intelligence & Analytics (SMUBIA)
#### Contributors: Aw Khai Loong, Felice Png, Lee Yu Hao, Yap Bing Yu
#### Mentor: Yar Khine Phyo

#### Files for preprocessing
- `code-repos/` directory houses the repos cloned from GitHub, which serve as our raw input data
- `processed_data/` directory contains the data after pre-processing
- `repo-namelists/` directory stores the names of GitHub repos we wish to clone, scrapped from `scrape_repo_names.py`
- `engine.py` can be executed to drive the process of scraping, cloning and preprocessing
- `scrape_language_list.py` scrapes the list of programming languages and their links from GitHub
- `scrape_repo_names.py` scrapes the names of trending GitHub repos for each language
- `clone.py` clones the repos listed in those files using https/ssh, with `depth=1` to shallow clone and avoid cloning previous revisions
- `preprocess.py` tokenizes the cloned repos and stores them as numerical vectors in `processed_data/*`

#### Files for machine learning
- `ml_*.ipynb` jupyter notebooks contain our machine learning code

#### How to Use
- `git clone` this repo
- `python engine.py` to drive the process of scraping, cloning and preprocessing
- other features not implemented yet
