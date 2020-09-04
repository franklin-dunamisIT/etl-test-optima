# etl-test-optima
## Overview of project
This project contains python and php files.

The webscraping component is done in Python while the web application piece is written in PHP

## Files/folders breakdown

-  web_scraper.py :  the Python script that scrapes the website provided and ingests the data into a Mongodb instance
-  db_config.py: contains the Mongodb credentials (the actual values have been replaced by placeholder)
-  requirements.py:  Dependencies to complete the web scraping with Python
-  critical-products-app:  The Lavarel web application folder, containing the  php data loader

## Project Flow
<img src="https://github.com/franklin-dunamisIT/etl-test-optima/blob/master/images/ETL%20Optima%20image.JPG"/>

#### Extract phase
- The python script (web_scraper.py) crawls through 'https://ww.rrpcanada.org/#/' and retrieves a list of the critical products as well as their available counts. It then creates a connection to a Mongodb instance installed on the local machine. 
- Because the web page has some dynamic contain, proper code was put in place to ensure that the key data has been rendered before attempt is made to pull the page source.
- The python script hit the web page freqently at a polling it at a time between 10 -120 secs just so there's no pathern to make it too suspicious it's a spider/bot. The db is also updated freqently this way to ensure the data in always up to date.

#### Storage phase
- For the purpose of the test, Mongodb was installed on the test machine to store the data from the extract phase. 
```
$ mongo
MongoDB shell version v4.4.0
connecting to: mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb
Implicit session: session { "id" : UUID("0547abec-9cf1-47ef-b64c-49e64422f628") }
MongoDB server version: 4.4.0
---
The server generated these startup warnings when booting:
        2020-09-02T16:16:17.572-04:00: Access control is not enabled for the database. Read and write access to data and configuration is unrestricted
---
---
        Enable MongoDB's free cloud-based monitoring service, which will then receive and display
        metrics about your deployment (disk utilization, CPU, operation statistics, etc).

        The monitoring data will be available on a MongoDB website with a unique URL accessible to you
        and anyone you share the URL with. MongoDB may use this information to make product
        improvements and to suggest MongoDB products and deployment options to you.

        To enable free monitoring, run the following command: db.enableFreeMonitoring()
        To permanently disable this reminder, run the following command: db.disableFreeMonitoring()
---
> use challenge_db
switched to db challenge_db> db.createUser({user:'optima',pwd: '<PWD>', roles:[{role: "readWrite", db:"challenge_db"}] } )
Successfully added user: {
        "user" : "optima",
        "roles" : [
                {
                        "role" : "readWrite",
                        "db" : "challenge_db"
                }
        ]
}
> use challenge_db
switched to db challenge_db
> show collections
>

```

After running the python script, the content of the db looks like this
```
switched to db challenge_db
> show collections
products to db challenge_db
> db.products.find({})
{ "_id" : ObjectId("5f51b7022c927c320159bcf5"), "name" : "Surgical & Reusable Masks", "available_qty" : " 376,905,263  ", "last_updated" : ISODate("2020-09-03T23:39:46.715Z") }
{ "_id" : ObjectId("5f51b7032c927c320159bcf6"), "name" : "Disposable Gloves", "available_qty" : " 64,886,093  ", "last_updated" : ISODate("2020-09-03T23:39:46.715Z") }
{ "_id" : ObjectId("5f51b7032c927c320159bcf7"), "name" : "Gowns and Coveralls", "available_qty" : " 40,522,145  ", "last_updated" : ISODate("2020-09-03T23:39:46.715Z") }
{ "_id" : ObjectId("5f51b7032c927c320159bcf8"), "name" : "Respirators", "available_qty" : " 22,189,173  ", "last_updated" : ISODate("2020-09-03T23:39:46.715Z") }
{ "_id" : ObjectId("5f51b7032c927c320159bcf9"), "name" : "Surface Wipes", "available_qty" : " 20,649,881  ", "last_updated" : ISODate("2020-09-03T23:39:46.715Z") }
{ "_id" : ObjectId("5f51b7032c927c320159bcfa"), "name" : "Face Shields", "available_qty" : " 16,535,736  ", "last_updated" : ISODate("2020-09-03T23:39:46.715Z") }
{ "_id" : ObjectId("5f51b7032c927c320159bcfb"), "name" : "Hand Sanitizer", "available_qty" : " 11,152,902 L  ", "last_updated" : ISODate("2020-09-03T23:39:46.715Z") }
{ "_id" : ObjectId("5f51b7032c927c320159bcfc"), "name" : "Thermometers", "available_qty" : " 8,457,998  ", "last_updated" : ISODate("2020-09-03T23:39:46.715Z") }
{ "_id" : ObjectId("5f51b7032c927c320159bcfd"), "name" : "Testing Kits", "available_qty" : " 2,110,815  ", "last_updated" : ISODate("2020-09-03T23:39:46.715Z") }
{ "_id" : ObjectId("5f51b7032c927c320159bcfe"), "name" : "Surface Solutions", "available_qty" : " 107,462 L  ", "last_updated" : ISODate("2020-09-03T23:39:46.715Z") }
{ "_id" : ObjectId("5f51b7032c927c320159bcff"), "name" : "Protective Barriers", "available_qty" : " 10,858  ", "last_updated" : ISODate("2020-09-03T23:39:46.715Z") }
{ "_id" : ObjectId("5f51b7032c927c320159bd00"), "name" : "Ventilators", "available_qty" : " 410  ", "last_updated" : ISODate("2020-09-03T23:39:46.715Z") }

```

#### Loading phase
- Laravel was installed on the test machine and set up accordingly (e.g. a Model, Controller, View were created for the products; mongodb was replaced as the default db for the framework;). The workspace for that is `critical-projects-app`. THe require dependencies are found in composer.json/composer.lock. 
- The web page autorefresh regularly to pick up the latest date from the db
Some key files include:
- critical-products-app\app\Product.php - the product model
- critical-products-app\resources\views\productIndex.blade.php - the product view
- critical-products-app\app\Http\Controllers\ProductController.php -  the product controller
- critical-products-app\database\migrations\2020_09_03_065904_create_products_collection.php - db migration for products collection
- critical-products-app\routes\web.php -  the route which link the model function with url route


<img src="https://github.com/franklin-dunamisIT/etl-test-optima/blob/master/images/critical%20products%20img%20-%20latest.JPG"/>


