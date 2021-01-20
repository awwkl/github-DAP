import bs4
from urllib.request import urlopen as uReq 
from bs4 import BeautifulSoup as soup 

def scrape():
    github_url = 'https://github.com'
    my_url = 'https://github.com/trending/python?since=monthly'

    uClient = uReq(my_url)
    page_html = uClient.read()
    page_soup = soup(page_html, "html.parser")
    menu = page_soup.find("div", {"id" : "languages-menuitems"})

    containers = menu.findAll("a", {"class" : "select-menu-item"})

    out_filename = "./repo-namelists/lang_list.csv"
    headers = "language,link\n"

    f = open(out_filename, "w")
    f.write(headers)

    for container in containers:
        lang = container.find("span" , {"class" : "select-menu-item-text"}).text.strip()
        lang_url = github_url + container['href']
        f.write(lang + "," + lang_url + "\n")
