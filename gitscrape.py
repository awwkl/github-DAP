import bs4 
from urllib.request import urlopen as uReq 
from bs4 import BeautifulSoup as soup 
import pandas as pd

languages = ["C++", "HTML", "Java", "JavaScript"]
langName = ["c++", "html", "java", "javascript"]
df = pd.read_csv('langList.csv')
df = df[df['language'].isin(languages)]
li = df[' link '].tolist()

for i in range(len(li) - 1):
    uClient = uReq(li[i])
    page_html = uClient.read()
    page_soup = soup(page_html, "html.parser")

    containers = page_soup.findAll("h1", {"class" : "h3 lh-condensed"})

    out_filename = f'list_{langName[i]}.csv'
    headers = "repo_name\n"

    f = open(out_filename, "w")
    f.write(headers)

    for container in containers:
        repo_name = container.a.text
        f.write("".join(repo_name.split()) + '\n')


