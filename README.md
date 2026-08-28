# E-commerce Demand Forecasting & Inventory Optimization

This project's main goal is to forecast product demand for an e-commerce business and use the forecasts to make better inventory decisions, such as how much inventory stock should be ther at any given time and when to reorder stock.

## Dataset

The project uses the **DataCo Supply Chain dataset** along with **Access Log Data**.

* DataCoSupplyChainDataset.csv - this is the main dataset
* tokenized_access_logs.csv - the access log data for the products/items
* DescriptionDataCoSupplyChain.csv - data dictionary of the main dataset

The datasets are not included in this GitHub repository because the files are large.

### Dataset Desctiption

- **Type:** Type of transaction made
- **Days for shipping (real):** Actual shipping days of the purchased product
- **Days for shipment (scheduled):** Days of scheduled delivery of the purchased product
- **Benefit per order:** Earnings per order placed
- **Sales per customer:** Total sales per customer made per customer
- **Delivery Status:** Delivery status of orders: Advance shipping , Late delivery , Shipping canceled , Shipping on time
- **Late_delivery_risk:** Categorical variable that indicates if sending is late (1), it is not late (0).
- **Category Id:** Product category code
- **Category Name:** Description of the product category
- **Customer City:** City where the customer made the purchase
- **Customer Country:** Country where the customer made the purchase
- **Customer Email:** Customer's email
- **Customer Fname:** Customer name
- **Customer Id:** Customer ID
- **Customer Lname:** Customer lastname
- **Customer Password:** Masked customer key
- **Customer Segment:** Types of Customers: Consumer , Corporate , Home Office
- **Customer State:** State to which the store where the purchase is registered belongs
- **Customer Street:** Street to which the store where the purchase is registered belongs
- **Customer Zipcode:** Customer Zipcode
- **Department Id:** Department code of store
- **Department Name:** Department name of store
- **Latitude:** Latitude corresponding to location of store
- **Longitude:** Longitude corresponding to location of store
- **Market:** Market to where the order is delivered : Africa , Europe , LATAM , Pacific Asia , USCA
- **Order City:** Destination city of the order
- **Order Country:** Destination country of the order
- **Order Customer Id:** Customer order code
- **order date (DateOrders):** Date on which the order is made
- **Order Id:** Order code
- **Order Item Cardprod Id:** Product code generated through the RFID reader
- **Order Item Discount:** Order item discount value
- **Order Item Discount Rate:** Order item discount percentage
- **Order Item Id:** Order item code
- **Order Item Product Price:** Price of products without discount
- **Order Item Profit Ratio:** Order Item Profit Ratio
- **Order Item Quantity:** Number of products per order
- **Sale:** Value in sales
- **Order Item Total:** Total amount per order
- **Order Profit Per Order:** Order Profit Per Order
- **Order Region:** Region of the world where the order is delivered: Southeast Asia, South Asia, Oceania, Eastern Asia, West Asia, West of USA, US Center, West Africa, Central Africa, North Africa, Western Europe, Northern, Caribbean, South America, East Africa, Southern Europe, East of USA, Canada, Southern Africa, Central Asia, Europe, Central America, Eastern Europe, South of USA
- **Order State:** State of the region where the order is delivered
- **Order Status:** COMPLETE, PENDING, CLOSED, PENDING_PAYMENT, CANCELED, PROCESSING, SUSPECTED_FRAUD, ON_HOLD, PAYMENT_REVIEW
- **Product Card Id:** Product code
- **Product Category Id:** Product category code
- **Product Description:** Product Description
- **Product Image:** Link of visit and purchase of the product
- **Product Name:** Product Name
- **Product Price:** Product Price
- **Product Status:** Status of the product stock :If it is 1 not available , 0 the product is available
- **Shipping date (DateOrders):** Exact date and time of shipment
- **Shipping Mode:** The following shipping modes are presented : Standard Class , First Class , Second Class , Same Day

## Setup

Clone this repository

```bash
git clone https://github.com/bhardwajharsh07/E-commerce-Demand-Forecasting
cd E-commerce-Demand-Forecasting
```

Create and activate a virtual environment:

```bash
python -m venv venv
```
Activate in Windows
```bash
venv\Scripts\activate
```
Activate in MacOS
```bash
source venv/bin/activate
```

Install the required libraries:

```bash
pip install -r requirements.txt
```

## Update 1

**Environment Setup** is done  
**Project Structure** is defined  
**Necessary files** required till now are created  

## Update 2

**Logging** is implemented  
**Custom Exception Handling** is implemented  
**Data Ingestion** is implemented with logging and exception handling  
**Git Branching & Pull Request Workflow** is completed  