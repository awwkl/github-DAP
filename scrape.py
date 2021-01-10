import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = 'https://github.com/trending/python?since=monthly'

# open connection, grab page
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

# html parsing
page_soup = soup(page_html, 'html.parser')

# find all repo names
repo_names = page_soup.findAll()