import bs4
import os
from urllib.request import urlopen as uReq 
from bs4 import BeautifulSoup as soup 
import pandas as pd
import time
import requests
import random

def scrape(langs_name, langs_extension, langs_url):
    num_of_langs = len(langs_name)
    # df = pd.read_csv('./repo-namelists/lang_list.csv', index_col=0)

    agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36', 
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36', 
        'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.83 Safari/537.1'
    ]

    for i in range(5, num_of_langs):
        lang_name = langs_name[i]
        lang_url = langs_url[i]

        for index in range(1, 101):
        # Get link for trending github repositories of current language
            link = f'https://github.com/search?l={lang_url}&p={index}&q=language%3A{lang_url}&ref=advsearch&type=Repositories'
            print(link)
            # get HTML for the link, then find all repo names in HTML
            agent_index = index % 10
            uClient = requests.get(link, headers = {'User-agent': agents[agent_index]})
            page_html = uClient.text
            page_soup = soup(page_html, "html.parser")
            # print(page_soup)
            containers = page_soup.findAll("a", {"class" : "v-align-middle"})

            # write to file e.g. "list_c++.csv"
            out_filename = f'./repo-namelists/list_{langs_extension[i]}.csv'
            # if repo namelist has been created, do not create again
            if os.path.exists(out_filename):
                pass
            else:
                with open(out_filename, "a+") as f:
                    headers = "repo_name\n"
                    f.write(headers)
            #     continue

            with open(out_filename, "a+") as f:
                for container in containers:
                    # print(container)
                    repo_name = container.text
                    print(repo_name)
                    f.write("".join(repo_name.split()) + '\n')
            print(random.randint(1, 10))
            time.sleep(random.randint(1, 10))