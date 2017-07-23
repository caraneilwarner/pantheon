"""Scrape the webstite babynames.net to produce (name,gender,meaning) tuples.
Write these to files for future use.
"""
from bs4 import BeautifulSoup
import csv
import json
import requests

base_domain = 'https://www.babynames.net'

def get_categories():
    """Scrape the homepage of babynames.net. Retrieve links to each category of
    names. Categories are things like Arabic, Chinese, and Danish, or Aristocrat
    and Nature, or Top 1920s and Top 1950s.
    """
    categories = []
    result = requests.get(base_domain)
    soup = BeautifulSoup(result.text, 'lxml')
    items = soup.select('.names-list li > a')
    for item in items:
        categories.append((item.contents[0].lower(), item['href']))
    return categories


def get_names_old(category):
    """Scrape babynames.net for names in the specified category."""
    endpoint = base_domain + [link for label,link in get_categories() if label == category.lower()][0]
    if not endpoint: return "Invalid category"

    links = get_pagination_links(endpoint)
    if len(links) == 0: links = [endpoint] # Only one page, no pagination

    names = []

    for link in links:
        result = requests.get(link)
        soup = BeautifulSoup(result.text, 'lxml')
        items = soup.select('.even, .odd')
        for name in items:
            try:
                name = item.find("span", {"class":"result-name"}).contents[0]
                gender = item.find("span", {"class":"result-gender"}).get("class")[1]
                desc = item.find("span", {"class":"result-desc"}).contents[0]
                names.append((name, gender, desc))
            except:
                pass
    return names


def get_names(category):
    """Scrape babynames.net for names in the specified category."""
    endpoint = base_domain + [link for label,link in get_categories() if label == category.lower()][0]
    if not endpoint: return "Invalid category"

    names = scrape(endpoint)
    return names


def scrape(endpoint):
    names = []
    result = requests.get(endpoint)
    soup = BeautifulSoup(result.text, 'lxml')
    items = soup.select('.even, .odd')
    for name in items:
        try:
            name = item.find("span", {"class":"result-name"}).contents[0]
            gender = item.find("span", {"class":"result-gender"}).get("class")[1]
            desc = item.find("span", {"class":"result-desc"}).contents[0]
            names.append((name, gender, desc))
        except:
            pass

    # try:
    #     next = soup.select('.pagination a')[-1]
    #     names += scrape(next['href'])
    # except:
    #     pass

    return names


def get_pagination_links(endpoint):
    result = requests.get(endpoint)
    soup = BeautifulSoup(result.text, 'lxml')
    items = soup.select('.pagination a')[1:-1] # Skip "Previous" and "Next"
    links = [base_domain + link['href'] for link in items]
    return links


def load_names(category):
    category = category.lower()
    if not 'json' in category:
        # Then input is the category label
        link = [ link for label,link in get_categories() if label == category ]
        if not link: return "Invalid category"
        filename = category_filename(link)
    elif not '../../src/names' in category:
        # Then input is the filename -- it's not relative
        filename = '../../src/names/' + category
    else:
        # Then input is the correct path
        filename = category

    with open(filename, 'r') as injson:
        names = json.load(injson)
        return [ tuple(name.split(',')) for name in names ]


def save_names(check=False):
    for label,link in get_categories():
        print("retrieving names from category: " + label)
        names = get_names(label)
        filename = category_filename(link)
        with open(filename, 'w') as outjson:
            json.dump([ ','.join(name) for name in names ], outjson)
        if check: return # Quit early because this is a dry run


def category_filename(link):
    return '../src/names/%s.json' % link.rsplit('/',1)[-1]
