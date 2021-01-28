import scrape_language_list
import scrape_repo_names
import clone
import preprocess

if __name__ == "__main__" :
    # Scrape list of languages
    x = input('Scrape list of languages from GitHub? [y/n]: ')
    if x.lower() in ['y', 'yes']:
        print("Scraping list of languages from GitHub...")
        scrape_language_list.scrape()

    # Scrape names of repositories
    print()
    x = input('Scrape names of repositories from GitHub? [y/n]: ')
    if x.lower() in ['y', 'yes']:
        print("Scraping names of repositories from GitHub...")
        scrape_repo_names.scrape()

    # Clone repositories
    print()
    x = input('Clone the repositories from GitHub? [y/n]: ')
    if x.lower() in ['y', 'yes']:
        print("Cloning the repositories from GitHub...")
        clone.clone_languages()

    # Preprocess the textual data (source files) into numerical data
    print()
    x = input('Preprocess the textual data (source files) into numerical data? [y/n]: ')
    if x.lower() in ['y', 'yes']:
        print("Preprocessing the data...")
        preprocess.preprocess_repos()
