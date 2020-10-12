import re

import requests
from bs4 import BeautifulSoup

stardew_fish_url = 'https://stardewvalleywiki.com/Fish'
blank_line_regex = r'^\s*$'


def main():
    print('Retrieving Resources')
    formatted_fish_data = retrieve_fish_item_data_from_wiki()
    print('\n'.join(formatted_fish_data))


def retrieve_fish_item_data_from_wiki():
    raw_html = request_raw_html_from_wiki()
    formatted_fish_data = parse_fish_item_data_from_raw_html(raw_html)
    return formatted_fish_data


def request_raw_html_from_wiki() -> str:
    try:
        response = requests.get(stardew_fish_url)
        return response.text
    except:
        print('Unable to retrieve html from stardew wiki')


def parse_fish_item_data_from_raw_html(raw_html: str) -> list:
    fish_data_text = retrieve_text_from_fish_html_table(raw_html)
    parsed_fish_lines = fish_data_text.split('\n')
    return parsed_fish_lines


def retrieve_text_from_fish_html_table(raw_html: str):
    parsed_fish_table = retrieve_first_html_table_by_id(raw_html, html_id='roundedborder')
    formatted_fish_table_text = remove_blank_lines_from_text(parsed_fish_table.text)
    return formatted_fish_table_text


def retrieve_first_html_table_by_id(raw_html: str, html_id: str):
    html_parser = BeautifulSoup(raw_html, 'html.parser')
    parsed_html_tables = html_parser.find_all(id=html_id)
    first_found_table = parsed_html_tables[0]
    return first_found_table


def remove_blank_lines_from_text(text: str) -> str:
    non_blank_lines = list([line for line in text.split('\n') if not re.match(blank_line_regex, line)])
    return '\n'.join(non_blank_lines)


class Item:
    pass


if __name__ == '__main__':
    main()
