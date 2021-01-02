###########################################################################################################
#
# I think I have found a better way of parsing data from the Stardew Wiki. It is better and more scalable.
#
###########################################################################################################
import time

from bs4 import BeautifulSoup
from os import path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

stardew_fish_url = 'https://stardewvalleywiki.com/Fish'
headers = {
    'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}


def main():
    print('Retrieving Resources, Only Better.... sigh')
    if path.exists(r'resources/fish_wiki.html'):
        with open(r'resources/fish_wiki.html', 'r', encoding='utf-8') as html_cache:
            raw_html = html_cache.read()
    else:
        raw_html = request_raw_html_from_wiki()
        with open(r'resources/fish_wiki.html', 'w', encoding='utf-8') as html_cache:
            html_cache.write(raw_html)
    wiki_items_table = find_items_table_in_html(raw_html)
    thead = wiki_items_table.thead

    table_headers = [f'{h.string}'.strip() for h in thead.tr.find_all('th')]
    print(f'Headers: {table_headers}')

    #table_contents = [f'{i.string}'.strip() for i in wiki_items_table.tbody.tr.find_all('td')]
    table_contents = wiki_items_table.tbody
    print(f'Fish Entries: {table_contents}')


def find_items_table_in_html(raw_html):
    html_parser = BeautifulSoup(raw_html, 'html.parser')
    parsed_html_tables = html_parser.find_all(id='roundedborder')
    wiki_items_table = parsed_html_tables[0]
    return wiki_items_table


def request_raw_html_from_wiki() -> str:
    service = Service('./chromedriver/chromedriver')
    service.start()
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Remote(service.service_url, options=options)
    driver.get(stardew_fish_url)
    page = driver.page_source
    driver.quit()
    return page


if __name__ == '__main__':
    main()
