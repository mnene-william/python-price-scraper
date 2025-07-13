import requests
from bs4 import BeautifulSoup


BASE_URL = "https://books.toscrape.com/"
NUM_PRODUCTS_TO_SCRAPE = 10 

def scrape_products(num_products):
    """Scrapes product names and prices from books.toscrape.com."""
    products = [] 
    page_num = 1 

    print(f"Starting to scrape up to {num_products} products...")

    
    while len(products) < num_products:

        url = f"{BASE_URL}catalogue/page-{page_num}.html"
        print(f"Accessing URL: {url}")

        try:
            
            response = requests.get(url, timeout=10) 
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser') 

            book_articles = soup.find_all('article', class_='product_pod')

            if not book_articles:
        
                print("No more products found on this page or end of website reached.")
                break 

            
            for book in book_articles:
                if len(products) >= num_products:
                    break 

               
                title_tag = book.find('h3').find('a')
                title = title_tag['title'].strip() if title_tag else "N/A" 

                
                price_tag = book.find('p', class_='price_color')
                price_str = price_tag.get_text().strip() if price_tag else "£0.00" # Get the text content of the tag


                try:
                    original_price = float(price_str.replace('£', '')) 
                except ValueError:
                    original_price = 0.0 
                    print(f"Warning: Could not parse price for '{title}'. Original string: '{price_str}'")

                
                products.append({
                    "name": title,
                    "original_price": original_price,
                    "original_currency": "GBP" 
                })
            page_num += 1 

        except requests.exceptions.ConnectionError:
            print(f"Connection error occurred while accessing {url}. Please check your internet connection.")
            break
        except requests.exceptions.Timeout:
            print(f"Request timed out while accessing {url}. The server took too long to respond.")
            break
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request error occurred while accessing {url}: {e}")
            break
        except Exception as e:
            print(f"An unexpected error occurred during HTML parsing or data extraction: {e}")
            break 

    return products

if __name__ == "__main__":
    
    scraped_data = scrape_products(NUM_PRODUCTS_TO_SCRAPE)

    print("\n--- Scraped Products (Raw) ---")
    if scraped_data:
        for product in scraped_data:
            print(f"Name: {product['name']}, Price: {product['original_price']:.2f} {product['original_currency']}")
        print(f"\nSuccessfully scraped {len(scraped_data)} products.")
    else:
        print("No products were scraped.")

                    
            

    
            

        



