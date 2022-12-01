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
    print(x)

# print(dataframe.groupby('Country').mean())



def InvoiceExists(invoiceNo):
    invoice = models.Invoice.objects.filter(invoice_no = invoiceNo).first()
    if invoice is not None:
        return True
    else:
        return False

def saveParentInvoice(invoice_no, invoice_date, invoice_country):
    invoice = models.Invoice.objects.create(
        invoice_no   = invoice_no,
        invoice_date = invoice_date,
        country      = invoice_country
    )
    print(invoice)
    return invoice
    # try:

    # except:
    #     print("Désoler une erruer est survenue !")




def saveInvoice(invoice_row):
    parent_invoice = InvoiceExists(invoice_row['InvoiceNo'])

    if not parent_invoice:
        print('must save invoice first')
        parent_invoice = saveParentInvoice(invoice_row['InvoiceNo'], invoice_row['InvoiceDate'], invoice_row['Country']) 
        print(parent_invoice)
    else:
        print(parent_invoice)
    


def lector(file):
    dataframe = pd.read_csv(file)

    # Remove duplicated rows
    dataframe = dataframe.drop_duplicates()

    # print(dataframe.groupby('Country').mean())


    # Aply validation function 
    dataframe['InvoiceNo']   = dataframe['InvoiceNo'].apply(valideInvoiceNo)
    dataframe['StockCode']   = dataframe['StockCode'].apply(validateStockCode)
    

    ## Get can insert data in db
    true_data  = dataframe.dropna(subset=['InvoiceNo', 'StockCode'])   

    irreparable_data =  dataframe[~dataframe.index.isin(true_data.index)]

    for index, row in true_data.iterrows():
        saveInvoice(row)

    return {
        "rows_inserted":    len(true_data),
        "rows_irreparable": len(irreparable_data)
    }

