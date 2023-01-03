import csv

import requests
from bs4 import BeautifulSoup

# TODO: Go through each table for items as of now if there isnt a valid item, it wont add,
#  so occasionally after searching there will an indexerror as the book list will be len(20) but
#   another attribute will be len(18)

url = "https://www.audible.co.uk"


def scrape(keyword):
    search_params = f"/search?keywords={keyword}"
    # Scraping Audible.com
    #   https://www.audible.co.uk/search?
    #   keywords=horror+bread
    #   &pageSize=50

    response = requests.get(f"{url}{search_params}").text
    soup = BeautifulSoup(response, "html.parser")
    book_titles = [a.text for a in soup.select("li.bc-list-item h3 a")]
    # Not every book has a subtitle
    # book_subtitle = [a.text.strip("\n") for a in soup.select("li.bc-list-item.subtitle")]
    book_link = [f"{url}{a['href']}" for a in soup.select("li.bc-list-item h3 a")]
    book_author = [a.text for a in soup.select("li.bc-list-item.authorLabel a ")]
    book_narrator = [a.text for a in soup.select("li.bc-list-item.narratorLabel a")]
    book_length = [a.text.strip("Length: ") for a in soup.select("li.bc-list-item.runtimeLabel span")]
    book_release_date = [a.text.strip("Release date:").strip("\n").strip(" ")
                         for a in soup.select("li.bc-list-item.releaseDateLabel span")]
    book_star_rating = [a.text for a in soup.select("li.bc-list-item.ratingsLabel span.bc-text.bc-pub-offscreen")]
    book_num_ratings = [a.text for a in soup.select("li.bc-list-item.ratingsLabel span.bc-text.bc-size-small")]

    headers = ["Book", "Link", "Author", "Narrator", "Length", "Release Date", "Star Rating", "Number of Ratings"]
    books = []
    for i in range(len(book_titles)):
        book = [
            book_titles[i],
            # book_subtitle[i],
            book_link[i],
            book_author[i],
            book_narrator[i],
            book_length[i],
            book_release_date[i],
            book_star_rating[i],
            book_num_ratings[i],
        ]
        books.append(book)

    with open(f"{keyword}.csv", "w", encoding="UTF-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(books)

    print("Success!")


searching = True

while searching:
    search = input("What type of book would you like to search for?: ")
    scrape(search)
    again = input("Search again? (Y/N)").upper()
    if again == "N":
        searching = False



