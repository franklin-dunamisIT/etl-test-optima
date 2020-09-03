from bs4 import BeautifulSoup                            # module for web scraping/parsing
from selenium import webdriver                           # selenium modules are used for creating/simulating a web browser 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui  import WebDriverWait
from selenium.webdriver.support import expected_conditions 
import pymongo                                           # mongodb client module
from db_config import *                                  # importing config parameters for mongodb access
import time                                              # time module to call sleep
from selenium.webdriver.common.by import By


# Function to extract critical products data from the sample url
# input: take in the url to scraper
# output: returns a list of the critical products on the url
def extract_data(url ):  
    critical_products_inventory = []

    # return an empty list if url is an empty string
    if not url: return []
    try:
        # Set the options to create a headless browser instance for ease of automation
        opts = Options()
        opts.headless = True

        # create an instances of Firebox browser to access the web content
        browser = webdriver.Firefox(options=opts, executable_path='c:/Users/frank/Downloads/geckodriver-v0.27.0-win64/geckodriver.exe') 
        browser.get(url)
        
        # Because the website provided contains dynamic pages, its content
        # may not have been rendered before attempting to retrieve the page source, 
        # this wait call will handle that concern.
        # This will wait until the data of interest (i.e. the critical products) are available to be extracted
        # This is more efficient than using a sleep command as for this, we'll wait only as long as required and no more
        browser.implicitly_wait(5)
        critical_products_container_checker = browser.find_element_by_class_name("product-title-container")
        print (critical_products_container_checker)

        # Retrieve the page source from the browser instance
        page_source =  browser.page_source

        # Create an instance of BeautifulSoup with html5lib parser
        # to simplify the scraping/parsing of the page source
        parsed_web_content = BeautifulSoup(page_source, 'html5lib')
 
        # Extract the product inventory from the div tag of class product-title-container
        critical_products_container = parsed_web_content.find_all('div', attrs={"class":"product-title-container"})

        # Traverse the product-title-container tag to retrieve the critical products as well as their available quantity
        for product_div in critical_products_container:
            product =  product_div.find('div', attrs={"class": "product-title"}).get_text()
            available_quantity = product_div.find('div', attrs={"class": "detail available"}).get_text().replace('units','')
            critical_products_inventory.append((product, available_quantity))
            
    except Exception as e :
        print ('Error while scraping web page: %s', str(e))
        exit()
    finally:
        # Close browser instance
        browser.close()
        return critical_products_inventory
    

# Function to load the products inventory into the database
# input: takes a list of the critical products and their available count
# output: 0 if successful or 1 otherwise
def ingest_data_into_db(inventory):
    try:
        # Database properties to access the mongodb
        mongodb_client =  pymongo.MongoClient("mongodb://%s:%d" % (DB_HOST,int(DB_PORT)),
                                                authSource=DB_NAME,
                                                username=DB_USER,
                                                password=DB_PASSWORD
                            )
        database = mongodb_client[DB_NAME]
        product_collection = database[COLLECTION]
    
        for product, quantity in inventory:
            print ("Inserting %s %s into product collection" % (product, quantity))
            product_collection.insert_one({'name': product, 'available_qty':quantity})

        # close db connection
        mongodb_client.close()
        return 0
    except Exception as e:
        print ('Error while writing to database: %s'% str(e))
        return 1

    

# main method
if __name__ == "__main__":
    # Extract data from sample url
    print('Extracting products data  from source...')
    product_inventory = extract_data('https://www.rrpcanada.org/#/')

    # Load data into the database
    print('Ingesting data into the db...')
    if product_inventory:
        ingest_data_into_db(product_inventory)

