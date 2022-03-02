from bs4 import BeautifulSoup   # imports Beautiful soup class from bs4 module
import requests     # imports requests module that implements the requests to API.
from operator import itemgetter     # imports the item class form operator module


books = []  # a list that will be storing the books information
print("Gathering information from the website..")


# function to get the book details from Amazon website and store them
def get_books():
    try:
        url = "https://www.amazon.com/gp/bestsellers/books/ref=bsm_nav_pill_print/ref=s9_acss_bw_cg_bsmpill_1c1_w?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-1&pf_rd_r=JSFR919BB1373W4FETRV&pf_rd_t=101&pf_rd_p=65e3ce24-654c-43fb-a17b-86a554348820&pf_rd_i=16857165011"
        page_html_data = requests.get(url)    # uses get method of the requests module to fetch data from the amazon website
        soup = BeautifulSoup(page_html_data.content, "html.parser")   # creates a parser instance
        books_details = soup.find_all("li", class_="zg-item-immersion")    # variable to retrieve all books
        # the html data for books are embedded in the class "zg-item-immersion".

        # loop through the html data of all books to get each books details separately
        for book_details in books_details:
            book_name = book_details.find("div", class_="p13n-sc-truncate").text.strip()    # finds the name of the book
            book_price = book_details.find("span", class_="p13n-sc-price")     # finds the price of the book

            # adds "The book has no price"  in place of price when the price of the book was not found
            price = book_price.text.strip() if book_price else "The book has no price"
            book_reviews = book_details.find("a", class_="a-size-small a-link-normal")   # finds the reviews of the book

            # adds "The book has no reviews"  in place of reviews when the book has no reviews
            reviews = book_reviews.text.strip() if book_reviews else "The book has no reviews"

            if reviews != "The book has no reviews":
                if price != "The book has no price":
                    # appends the book name, reviews, and price to the books list
                    books.append([book_name, int(reviews.replace(",", "")), float(price.replace("$", ""))])
                else:
                    continue    # in case the book has no price the book will be skipped
            else:
                continue    # in case the book has no reviews the book will be skipped
    except requests.exceptions.RequestException as e:
        print("Couldn't carry out the request!", e)


# function to sort the books
def sort_books():
    # sorts the books by reviews using itemgetter in descending order
    sort_books_by_review = sorted(books, key=itemgetter(1), reverse=True)

    # sorts the most reviewed books by price using itemgetter in descending order
    sort_books_by_price = sorted(sort_books_by_review[0:10], key=itemgetter(2), reverse=True)
    ranking = 1
    print("\nTop 10 most expensive books in the most reviewed books on amazon")
    print("----------------------------------------------------------------\n")

    # loops through the books that are most expensive and print them out in order
    for book in sort_books_by_price[0:10]:

        # displays the book ranking, name, number of reviews and price
        print(f"{ranking}. Book name: {book[0]}\n   Book reviews: {book[1]}\n   Book price: ${book[2]}\n")
        ranking += 1    # increments the ranking variable


# calls the above functions
if __name__ == "__main__":
    get_books()
    sort_books()


# code for automating the process
# if __name__ == "__main__":
    #     while True:
    #         get_books()
    #         sort_books()
    #         rerun_time = 86400    # 86400secs = 24 hours
    #         print(f"The program will rerun after {rerun_time}")
    #         time.sleep(rerun_time)
