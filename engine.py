import scrape_language_list
import scrape_repo_names
import tokenise

if __name__ == "__main__" :
    scrape_language_list.scrape()
    scrape_repo_names.scrape()
    tokenise.tokenize_files()
