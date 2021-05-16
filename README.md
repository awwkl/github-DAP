# Programming Language Classifer
#### Data Associate Project (DAP) of SMU Business Intelligence & Analytics (SMUBIA)
* Contributors: Aw Khai Loong, Felice Png, Lee Yu Hao, Yap Bing Yu
* Mentor: Yar Khine Phyo

#### `dataframe-building/` contains the files for building our dataframe, used later for model training
- `code-repos/` directory houses the repos cloned from GitHub, which serve as our raw input data
- `processed_data/` directory contains the data after pre-processing
- `repo-namelists/` directory stores the names of GitHub repos we wish to clone, scrapped from `scrape_repo_names.py`
- `engine.py` can be executed to drive the process of scraping, cloning and preprocessing
- `scrape_language_list.py` scrapes the list of programming languages and their links from GitHub
- `scrape_repo_names.py` scrapes the names of trending GitHub repos for each language
- `clone.py` clones the repos listed in those files using https/ssh, with `depth=1` to shallow clone and avoid cloning previous revisions
- `preprocess.py` tokenizes the cloned repos and stores them as numerical vectors in `processed_data/*`

#### `model-training/` contains the files for training our ML models
- `*.ipynb` jupyter notebooks contain our machine learning code

#### How to Explore our code
- `git clone` this repo
- `cd dataframe-building/ && python engine.py` to test our python scripts for scraping, cloning and preprocessing of data
- `model-training/*.ipynb` jupyter notebooks for our model training code
- other features not implemented yet
