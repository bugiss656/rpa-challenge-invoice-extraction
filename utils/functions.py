import io
import csv
import re
from datetime import datetime
import requests
from PIL import Image
import pytesseract




def get_table_data(row):
    '''
    Get data from table rows
    '''
    table_data = row.find_elements_by_tag_name('td') 
    table_data.pop(0)
    return [data.text for data in table_data]


def get_invoice_text(url):
    '''
    Extract text from invoice
    '''
    invoice_img_url = requests.get(url)
    invoice_img = Image.open(io.BytesIO(invoice_img_url.content))
    return pytesseract.image_to_string(invoice_img)


def extract_data_from_text(pattern, text):
    '''
    Extract specific data from text with regex pattern
    '''
    search = re.search(pattern, text)
    if search:
        return re.search(pattern, text)


def create_csv_file(field_names, data):
    '''
    Create .csv file with extracted invoice data
    '''
    with open('invoice_data.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(data)