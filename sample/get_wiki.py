import requests
from bs4 import BeautifulSoup


# gets the title of a random Wikipedia article
def get_random_wiki_title():
    page = requests.get("https://en.wikipedia.org/wiki/Special:Random")
    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find("title")
    title = str(title)[7:]
    title = title[:len(title) - 20]

    return title


# finds the link for the article that matches the title
def convert_title_to_link(title):
    title_words = []

    counter = 0
    last_stop = 0
    for c in title:
        if c == " ":
            title_words.append(title[last_stop:counter])
            last_stop = counter + 1
        if counter == len(title) - 1:
            title_words.append(title[last_stop:])
        counter += 1

    link = "https://en.wikipedia.org/wiki/"
    for w in title_words:
        link = link + w + "_"

    link = link[:len(link) - 1]

    return link


# combines get_random_wiki_title() and convert_title_to_link()
def get_random_wiki_link():
    random_title = get_random_wiki_title()
    link = convert_title_to_link(random_title)
    return link


# demonstrates intended use
def main():
    random_title = get_random_wiki_title()
    print(random_title)

    print(convert_title_to_link(random_title))


if __name__ == '__main__':
    main()
