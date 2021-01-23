import scrape_language_list
import scrape_repo_names
import clone
import tokenize_code

if __name__ == "__main__" :
    x = input('Scrape list of languages from GitHub? [y/n]: ')
    if x.lower() in ['y', 'yes']:
        print("Scraping list of languages from GitHub...")
        scrape_language_list.scrape()

    print()
    x = input('Scrape names of repositories from GitHub? [y/n]: ')
    if x.lower() in ['y', 'yes']:
        print("Scraping names of repositories from GitHub...")
        scrape_repo_names.scrape()

    print()
    x = input('Clone the repositories from GitHub? [y/n]: ')
    if x.lower() in ['y', 'yes']:
        print("Cloning the repositories from GitHub...")
        clone.clone_languages()
