from bs4 import BeautifulSoup                            # module for web scraping/parsing
from selenium import webdriver                           # selenium modules are used for creating/simulating a web browser 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui  import WebDriverWait
from selenium.webdriver.support import expected_conditions 
import pymongo                                           # mongodb client module
from db_config import *                                  # importing config parameters for mongodb access
import time                                              # time module to call sleep
import datetime
from random import seed, randint                         # to generate a random number for POLL_WAIT_TIME

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
        critical_products_container_checker = browser.find_element_by_class_name("critical-product-table-container")
 
        # Retrieve the page source from the browser instance
        page_source =  browser.page_source

        # Create an instance of BeautifulSoup with html5lib parser
        # to simplify the scraping/parsing of the page source
        parsed_web_content = BeautifulSoup(page_source, 'html5lib')
        # Extract the product inventory from the table within the critical-product-container
        critical_products_container = parsed_web_content.find('div', attrs={"class":"table shorten hide-mobile"})

        products_div_list = critical_products_container.find_all('div', attrs={"class":"line-item"})

        # Traverse the product-title-container tag to retrieve the critical products as well as their available quantity
        for product_div in products_div_list:
            product =  product_div.find('div', attrs={"class": "line-item-title"}).get_text()
            available_quantity = product_div.find('div', attrs={"class": "line-item-bold available"}).get_text().replace('available','')
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
    current_datetime = datetime.datetime.now()

    try:
 
        # Database properties to access the mongodb
        mongodb_client =  pymongo.MongoClient("mongodb://%s:%d" % (DB_HOST,int(DB_PORT)),
                                                authSource=DB_NAME,
                                                username=DB_USER,
                                                password=DB_PASSWORD
                            )
        database = mongodb_client[DB_NAME]
        # drop the collection if already exists
        database[COLLECTION].drop()
        product_collection = database[COLLECTION]
        
        for product, quantity in inventory:
            print ("Inserting %s %s into product collection" % (product, quantity))
            product_collection.insert_one({'name': product, 'available_qty':quantity, 'last_updated': current_datetime})


    except Exception as e:
        print ('Error while writing to database: %s'% str(e))
        return 1
    finally:
        # close db connection
        mongodb_client.close()
    
    return 0

# main method
if __name__ == "__main__":
    # An ideal best practice for scraping is to follow the standard crawl-delay which is 10secs
    # (adhered to by Google and Yahoo bots, for example) or otherwise specified in the robots.txt for the site. 
    # This is to ensure that the web pages being crawled don't get overwhelmed with too frequent hits. 
    # Aside from that, varying the frequency of the hit will also help reduce any suspicion that it's a bot/script
    # that's crawling the site. For that reason, the POLL_WAIT_TIME will be a randomly generated number
    # between 10 secs (being the minimum standard) and 120 secs so there's no set pattern. 
    # However, when done at scale,the following tactics can be added: spoofing, using proxy services/rotating IPs or even crawling the site during off-peak time; 
    # These will reduce the chances of the crawler being detected and blocked 

    while True:
        POLL_WAIT_TIME = randint(10, 120) 
        print (    POLL_WAIT_TIME)
        # Extract data from sample url
        print('Extracting products data  from source...')
        product_inventory = extract_data('https://www.rrpcanada.org/#/')

        # Load data into the database
        print('Ingesting data into the db...')
        if product_inventory:
            ingest_data_into_db(product_inventory)


        time.sleep(POLL_WAIT_TIME)

