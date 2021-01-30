import bs4
import os
from urllib.request import urlopen as uReq 
from bs4 import BeautifulSoup as soup 
import pandas as pd

def scrape():
    myLangs = ['HTML', 'Java', 'Python', 'C', 'C++', 'Ruby', 'PHP']
    myLangsFormatted = ['html', 'java', 'python', 'c', 'c++', 'ruby', 'php']

    df = pd.read_csv('./repo-namelists/lang_list.csv')

    for i in range(len(myLangs)):
        language = myLangs[i]                   # C++
        langName = myLangsFormatted[i]          # c++

        # select rows of DataFrame from the lang_list.csv that match those in myLangs
        selected_data = df.loc[df['language'] == language]
        link = selected_data.iloc[0]['link']

        # get HTML for the link, then find all repo names in HTML
        uClient = uReq(link)
        page_html = uClient.read()
        page_soup = soup(page_html, "html.parser")
        containers = page_soup.findAll("h1", {"class" : "h3 lh-condensed"})

        # write to file e.g. "list_c++.csv"
        out_filename = f'./repo-namelists/list_{myLangsFormatted[i]}.csv'
        # if repo namelist has been created, do not create again
        if os.path.exists(out_filename):
            continue

        headers = "repo_name\n"
        f = open(out_filename, "w")
        f.write(headers)

        for container in containers:
            repo_name = container.a.text
            f.write("".join(repo_name.split()) + '\n')