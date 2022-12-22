import pandas as pd
import numpy as np
import datetime

from Site import models
# dataframe = pd.read_csv('./data-csv/data.csv')

# Remove duplicated rows
#    dataframe = dataframe.drop_duplicates()

# dataframe = dataframe.drop_duplicates(subset=['InvoiceNo'])

# pays = ['United Kingdom', '']



def valideInvoiceNo(x):
    try: 
        int(x)
        return x
    except:
        if(type(x) == str):
            try:
                int(x[1:])
                return x
            except:
                return np.nan
        else:
            return np.nan

def valideDateTime(x):
    # print(type(x))
    try:
        datetime.datetime.strptime(x, '%m/%d/%Y %H:%M')
        return x
    except ValueError:
        # print('date nop')
        return np.nan

def validateStockCode(x):
    try: 
        int(x)
        return x
    except:
        if(type(x) == str):
            try:
                int(x[:-1])
                return x
            except:
                return np.nan
        else:
            return np.nan

def checkRegion(x):
    if x == 'Unspecified':
        return np.nan
    else:
        return x

def checkQuantity(x):
    if x > 0:
        return x
    else: 
        return np.nan

def checkTest(row):
    
    true_data  = pd.DataFrame(columns=['InvoiceNo', 'StockCode', 'Description', 'Quantity', 'InvoiceDate', 'UnitPrice', 'CustomerID', 'Country'])
    false_data = pd.DataFrame(columns=['InvoiceNo', 'StockCode', 'Description', 'Quantity', 'InvoiceDate', 'UnitPrice', 'CustomerID', 'Country'])
    
    print(row)
    if valideInvoiceNo(row['InvoiceNo']) is np.nan:
        false_data = pd.concat([true_data, row], ignore_index=True)
    else:
        true_data  = pd.concat([false_data, row], ignore_index=True)

    if validateStockCode(row['StockCode']) is np.nan:
        false_data = pd.concat([true_data, row], ignore_index=True)
    else:
        true_data = pd.concat([false_data, row], ignore_index=True)
    # if checkRegion(row['Country']) is np.nan:
    #     row = None
    # if checkQuantity(row['Quantity']):
    #     row = None

    return true_data

def getCountry(country_name):
    country = models.Region.objects.filter(region_name = country_name).first()
    if country is None:
        country = models.Region.objects.create(region_name = country_name)

    return country


def InvoiceExists(invoiceNo):
    invoice = models.Invoice.objects.filter(invoice_no = invoiceNo).first()
    if invoice is not None:
        return invoice
    else:
        return False

def saveParentInvoice(invoice_no, invoice_date, invoice_country, customer_id):
    date  =  datetime.datetime.strptime(invoice_date, '%m/%d/%Y %H:%M')
    
    country = getCountry(invoice_country)

    invoice = models.Invoice.objects.create(
        invoice_no   = invoice_no,
        invoice_date = date,
        country      = country,
        customer_id  = customer_id,
    )
    return invoice

def saveProduct(stockCode, description, price):
    product = models.Product.objects.filter(stock_code = stockCode).first()
    if product is None:
        product = models.Product.objects.create(
            stock_code = stockCode,
            unit_price = price,
            description = description
        )
    return product

def saveInvoieDetails(parent_invoice, product, invoice):
    print()


def saveInvoice(invoice_row):
    parent_invoice = InvoiceExists(invoice_row['InvoiceNo'])
    product        = saveProduct(invoice_row['StockCode'], invoice_row['Description'], invoice_row['UnitPrice'])

    if not parent_invoice:
        parent_invoice = saveParentInvoice(invoice_row['InvoiceNo'], invoice_row['InvoiceDate'], invoice_row['Country'], invoice_row['CustomerID']) 

    detail = models.InvoiceDetails.objects.filter(
        quantity = invoice_row['Quantity'],
        invoice  = parent_invoice,
        product  = product
    )

    if len(detail) == 0:
        invoice_details = models.InvoiceDetails.objects.create(
            quantity = invoice_row['Quantity'],
            invoice  = parent_invoice,
            product  = product
        )

def saveFailed(failed_rows):
    fails = models.FailInvoice.objects.create(
        invoice_no   = failed_rows['InvoiceNo'],
        invoice_date = failed_rows['InvoiceDate'],
        country      = failed_rows['Country'],
        stock_code   = failed_rows['StockCode'],
        description  = failed_rows['Description'],
        unit_price   = failed_rows['UnitPrice'],
        customer_id  = failed_rows['CustomerID'],
        quantity     = failed_rows['Quantity']
    )


def lector(file):
    dataframe = pd.read_csv(file)           # Read the CSV file as dataframe
    dataframe = dataframe.drop_duplicates() # Remove duplicated rows
    '''
        # Group by an dataframe
        # print(dataframe.groupby('Country').mean())

        # Apply validation functions on entire row
        # row = dataframe.apply(checkTest, axis=2)
    '''
    # Apply cleanup functions on the dataframe to determine if certain field hve error
    dataframe['InvoiceNo']   = dataframe['InvoiceNo'].apply(valideInvoiceNo)
    dataframe['StockCode']   = dataframe['StockCode'].apply(validateStockCode)
    dataframe['Country']     = dataframe['Country'].apply(checkRegion)
    dataframe['Quantity']    = dataframe['Quantity'].apply(checkQuantity)

    ## Get all data without errors in new dataframe
    true_data = dataframe.dropna(subset=['InvoiceNo', 'StockCode', 'Quantity', 'CustomerID', 'Country']) 

    ## Make difference between the initial dataframe and the true_data dataframe to get all ros with errors in new datafame
    irreparable_data = dataframe[~dataframe.index.isin(true_data.index)]
    
    
    for index, row in true_data.iterrows():
        saveInvoice(row)
    
    
    for index, row in irreparable_data.iterrows():
        saveInvoice(row)
        
    # true_data.apply(saveInvoice)       # Save rows without errors in database
    # irreparable_data.apply(saveFailed) # Save rows with errors in database

    # return import log
    return { "rows_inserted": len(true_data), "rows_irreparable": len(irreparable_data) }


def getDataframe(csv_data):
    dataframe = pd.DataFrame(columns=['InvoiceNo', 'StockCode', 'Description', 'Quantity', 'InvoiceDate', 'UnitPrice', 'CustomerID', 'Country'])

    for fail in csv_data:
        row = {
            'InvoiceNo':   fail.invoice_no,
            'StockCode':   fail.stock_code,
            'Description': fail.description,
            'Quantity':    fail.quantity,
            'InvoiceDate': fail.invoice_date,
            'UnitPrice':   fail.unit_price,
            'CustomerID':  fail.customer_id,
            'Country':     fail.country
        }
        dataframe = dataframe.append(row, ignore_index=True)
    
    print(dataframe)
    return dataframe