import csv
from datetime import datetime

def validateDate(date_text):
    try:
        if date_text != datetime.strptime(date_text, "%m/%d/%Y ").strftime('%Y-%m-%d'):
            raise ValueError
        return True
    except ValueError:
        return False

        
lines = open('./data-csv/data.csv').read().splitlines()

del lines[0]

_datas = []


def validLine(line):    
    line_items = line.split(',')


    InvoiceNo   = line_items[0]
    StockCode   = line_items[1]
    Description = line_items[2]
    Quantity    = line_items[3]
    InvoiceDate = line_items[4]
    UnitPrice   = line_items[5]
    CustomerID  = line_items[6]
    Country     = line_items[7]

    print(InvoiceDate)
    
    # if(InvoiceNo != '' and StockCode != '' and Quantity != 0 or Quantity != '0' and InvoiceDate):
    #     print(InvoiceNo.isnumeric(), InvoiceNo)

for line in lines:
    validLine(line)