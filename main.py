import time
import os
from datetime import datetime
from selenium.webdriver import Chrome

from utils.regex import *
from utils.functions import *


# Path to tesseract.exe file
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def main():
    driver = Chrome()
    driver.get('https://rpachallengeocr.azurewebsites.net/')


    start_btn = driver.find_element_by_id('start')
    start_btn.click()
    time.sleep(1)
    

    table_data_keys = ['ID', 'DueDate']
    invoice_data_keys = ['InvoiceNo', 'InvoiceDate', 'CompanyName', 'TotalDue']
    csv_fieldnames = ['ID', 'DueDate', 'InvoiceNo', 'InvoiceDate', 'CompanyName', 'TotalDue']
    invoice_table_data = []
    invoice_img_data = []
    invoice_data = []


    table_paginate = driver.find_element_by_id('tableSandbox_paginate')
    paginate_btn_container = table_paginate.find_element_by_tag_name('span')
    table_pages = paginate_btn_container.find_elements_by_tag_name('a')


    # Iterating over the data pages
    for page in table_pages:
        table_body = driver.find_element_by_tag_name('tbody')
        table_rows = table_body.find_elements_by_tag_name('tr')
        invoice_links = driver.find_elements_by_css_selector('tr td a')
        invoice_img_urls = [url.get_attribute('href') for url in invoice_links]
        next_btn = driver.find_element_by_id('tableSandbox_next')


        # Iterating over the table rows
        for row in table_rows: 
            invoice_table_data.append(dict(zip(table_data_keys, get_table_data(row))))


        # Iterating over the invoice images to extract data
        for url in invoice_img_urls: 
            invoice_extracted_text = get_invoice_text(url) 
            invoice_extracted_data = []

            for pattern in INVOICE_NR_PATTERNS:
                invoice_nr = extract_data_from_text(pattern, invoice_extracted_text.replace(' ', ''))
                if invoice_nr != None:
                    invoice_extracted_data.append(invoice_nr.group(1))

            for pattern in DATE_PATTERNS:
                invoice_date = extract_data_from_text(pattern, invoice_extracted_text)
                if invoice_date != None:
                    invoice_extracted_data.append(invoice_date.group())

            for pattern in COMPANY_NAME_PATTERNS:
                company_name = extract_data_from_text(pattern, invoice_extracted_text)
                if company_name != None:
                    invoice_extracted_data.append(company_name.group())

            for pattern in TOTAL_DUE_PATTERNS:
                total_due = extract_data_from_text(pattern, invoice_extracted_text.replace(' ', ''))
                if total_due != None:
                    invoice_extracted_data.append(total_due.group(2))

            invoice_img_data.append(dict(zip(invoice_data_keys, invoice_extracted_data)))
            
        
        next_btn.click()
    

    # Merging invoice_table_data with invoice_img_data to a single dict
    for index, data in enumerate(invoice_table_data):
        invoice_data.append({**invoice_table_data[index], **invoice_img_data[index]})


    # List of invoice data where due date has passed or is today
    filtered_invoices = [invoice_data[invoice] for invoice in range(len(invoice_data)) if datetime.strptime(invoice_data[invoice]['DueDate'], '%d-%m-%Y').date() <= datetime.now().date()]
    

    # Convert invoice date string
    for invoice in filtered_invoices:
        for key in invoice.keys():
            if key == 'InvoiceDate':
                if re.match(DATE_PATTERNS[0], invoice['InvoiceDate']):
                    invoice['InvoiceDate'] = datetime.strptime(invoice['InvoiceDate'], '%Y-%m-%d').strftime('%d-%m-%Y')
                elif re.match(DATE_PATTERNS[1], invoice['InvoiceDate']):
                    invoice['InvoiceDate'] = datetime.strptime(invoice['InvoiceDate'], '%b %d, %Y').strftime('%d-%m-%Y')


    create_csv_file(csv_fieldnames, filtered_invoices)

    file_input = driver.find_element_by_name('csv')
    
    # Send absolute path to file input
    file_input.send_keys(os.path.abspath('invoice_data.csv'))

    time.sleep(5)

    driver.quit()

    
    
    
if __name__ == '__main__':
    main()