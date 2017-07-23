from bs4 import BeautifulSoup
import requests

domain = 'https://www.babynames.net'

def get_categories():
    endpoint = 'https://www.babynames.net/categories'
    links = get_pagination_links(endpoint)
    categories = []

    for link in links:
        items = get_items(link, '.result-list')
        for item in items:
            try:
                categories.append(item.contents[0].strip(' '))
            except:
                pass
    return list(set(categories))


def get_names(category):
    endpoint = 'https://www.babynames.net/all/' + category.lower()
    links = []
    for i in range(22):
        links.append(endpoint + "?page=" + str(i+1))

    #links = get_pagination_links(endpoint)
    names = []
    
    for link in links:
        items = get_items(link, '.even, .odd')
        for item in items:
            try:
                name = item.find("span", {"class":"result-name"}).contents[0]
                gender = item.find("span", {"class":"result-gender"}).get("class")[1]
                desc = item.find("span", {"class":"result-desc"}).contents[0]
                names.append((name, gender, desc))
            except:
                pass
    return names


def get_pagination_links(endpoint):
    items = get_items(endpoint, '.pagination a')
    links = [domain + item['href'] for item in items]
    return links[1:] # The first is always junk


def get_items(endpoint, selector):
    result = requests.get(endpoint)
    soup = BeautifulSoup(result.text)
    return soup.select(selector)


# Read pagination on categories to get each page
# Go through each category page and grab title
# Expose function for getting a list of possible categories
# Write generic function for grabbing all names from a category
# Go to first page of category, grab pagination, loop over pages getting name + gender

