import bs4
import os
from urllib.request import urlopen as uReq 
from bs4 import BeautifulSoup as soup 
import pandas as pd

def scrape(langs_name, langs_extension, langs_url):
    num_of_langs = len(langs_name)
    # df = pd.read_csv('./repo-namelists/lang_list.csv', index_col=0)

    for i in range(num_of_langs):
        lang_name = langs_name[i]
        lang_url = langs_url[i]

        for index in range(1, 11):
        # Get link for trending github repositories of current language
            link = f'https://github.com/search?l={lang_url}&p={index}&q=language%3A{lang_url}&ref=advsearch&type=Repositories'

            # get HTML for the link, then find all repo names in HTML
            uClient = uReq(link)
            page_html = uClient.read()
            page_soup = soup(page_html, "html.parser")
            containers = page_soup.findAll("a", {"class" : "v-align-middle"})

            # write to file e.g. "list_c++.csv"
            out_filename = f'./repo-namelists/list_{langs_extension[i]}.csv'
            # if repo namelist has been created, do not create again
            if os.path.exists(out_filename):
                continue

            headers = "repo_name\n"
            f = open(out_filename, "w+")
            f.write(headers)

            for container in containers:
                repo_name = container.text
                f.write("".join(repo_name.split()) + '\n')