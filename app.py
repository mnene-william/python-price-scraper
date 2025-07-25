import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import pandas as pd
from tabulate import tabulate


BASE_URL = "https://books.toscrape.com/"
NUM_PRODUCTS_TO_SCRAPE = 10 

API_KEY = "0bb79d78e72ea8dc02f2d698"
ORIGINAL_CURRENCY = "GBP"
TARGET_CURRENCY = "KES"


def get_exchange_rate(api_key, from_currency, to_currency):

    try:
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{from_currency}"
        print(f"Fetching echange rate from: {url}")
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        if data["result"] == "success":
            rate = data["conversion_rates"].get(to_currency)
            if rate is None:
                print(f"Error: Target currency '{to_currency}' not found in conversion rates.")
            return rate
        else:
            print(f"Error from currency API: {data.get('error-type', 'Unknown error')}")
            return None
    except:
        print("Connection error occurred while fetching exchange rate.Check your internet connection.")
        return None


def scrape_products(num_products):

    products = [] 
    page_num = 1 

    print(f"Starting to scrape up to {num_products} products...")

    
    while len(products) < num_products:

        url = f"{BASE_URL}catalogue/page-{page_num}.html"
        print(f"Accessing URL: {url}")

        try:
            
            response = requests.get(url, timeout=10) 
            response.encoding = 'utf-8'
 
            soup = BeautifulSoup(response.text, 'html.parser') 

            book_articles = soup.find_all('article', class_='product_pod')

            if not book_articles:
        
                print("No more products found on this page or end of website reached.")
                break 

            
            for book in book_articles:
                if len(products) >= num_products:
                    break 

               
                title_tag = book.find('h3').find('a')
                title = title_tag['title'].strip()  

                
                price_tag = book.find('p', class_='price_color')
                price_str = price_tag.get_text().strip() 


                try:
                    original_price = float(price_str.replace('£', '')) 
                except:
                    original_price = 0.0 
                    print(f"Could not parse price for '{title}'. Original string: '{price_str}'")

                
                products.append({
                    "name": title,
                    "original_price": original_price,
                    "original_currency": "GBP" 
                })
            page_num += 1 

        except:
            print(f"Connection error occurred while accessing {url}. Please check your internet connection.")
            

    return products

if __name__ == "__main__":
    
    print(f"Scraping {NUM_PRODUCTS_TO_SCRAPE} products from {BASE_URL}")
    scraped_products = scrape_products(NUM_PRODUCTS_TO_SCRAPE)

    if not scraped_products:
        print(f"No products scraped.")
        exit()

    exchange_rate = get_exchange_rate(API_KEY, ORIGINAL_CURRENCY, TARGET_CURRENCY)
    
    if exchange_rate is None:
        print("Could not retrieve exchange rate.Cannot perform currency conversion")
        exit()

    

        print(f"Current Exchange Rate is {ORIGINAL_CURRENCY} = {exchange_rate}{TARGET_CURRENCY}")


    converted_products = []
    for product in scraped_products:
        converted_price = round(product["original_price"] * exchange_rate, 2)
        converted_products.append({
            "name": product["name"],

            "original_price": f"{product['original_price']} {product['original_currency']}",
            "converted_price": f"{converted_price} {TARGET_CURRENCY}",
            "conversion_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    df = pd.DataFrame(converted_products)
    print("\n Book articles Prices")
    print(tabulate(df[['name', 'original_price', 'converted_price', 'conversion_timestamp']],
                   headers='keys',
                   tablefmt='pipe')) 


    file_name = f"prices.json"
    try:
        with open(file_name, 'w') as f:
            json.dump(converted_products, f, indent=4)
        print(f"Data successfully saved to {file_name}")
    except:
        print(f"An error occured while saving data to {file_name}")

            

    
            

        



