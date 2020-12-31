###########################################################################################################
#
# I think I have found a better way of parsing data from the Stardew Wiki. It is better and more scalable.
#
###########################################################################################################
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

stardew_fish_url = 'https://stardewvalleywiki.com/Fish'
headers = {
    'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}


def main():
    print('Retrieving Resources, Only Better.... sigh')
    raw_html = request_raw_html_from_wiki()
    wiki_items_table = find_items_table_in_html(raw_html)
    print(f'Headers: {wiki_items_table.thead}')
    # print(wiki_items_table)


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
