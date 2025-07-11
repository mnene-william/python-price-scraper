from bs4 import BeautifulSoup
import requests

BASE_URL = "https://books.toscrape.com"
NUM_PRODUCTS_TO_SCRAPE = 10

def scrape_products(num_products):

    products = []
    page_number = 1

    print(f"Scraping up to {num_products} products..")

    while len(products) < num_products:
        url = f"{BASE_URL}/catalogue/page-{page_number}.html"

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            books = soup.find_all('article', class_='product_pod')

            if not books:
                print('No books have been found!')
                break

            for book in books:
                if len(products) >= num_products:
                    break
                try:
                    title = book.find('h3').find('a')['title'].strip()
                    price = book.find('p', class_='price_color').text.strip()

                    products.append({'title': title, 'price': price})

                    print(f"The price of {title}  is {price}")
                except AttributeError:
                    print("An error has occurred")
                    continue
        except: 
            print("An error has occurred")

            

    
            

        



