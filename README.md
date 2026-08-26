# E-commerce Demand Forecasting & Inventory Optimization

This project's main goal is to forecast product demand for an e-commerce business and use the forecasts to make better inventory decisions, such as how much inventory stock should be ther at any given time and when to reorder stock.

## Dataset

The project uses the **DataCo Supply Chain dataset** along with **Access Log Data**.

* DataCoSupplyChainDataset.csv - this is the main dataset
* tokenized_access_logs.csv - the access log data for the products/items
* DescriptionDataCoSupplyChain.csv - data dictionary of the main dataset

The datasets are not included in this GitHub repository because the files are large.

## Setup

Clone this repository

```bash
git clone <https://github.com/bhardwajharsh07/E-commerce-Demand-Forecasting>
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