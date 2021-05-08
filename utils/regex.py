COMPANY_NAME_PATTERNS = ['Aenean LLC', 'Sit Amet Corp.']


INVOICE_NR_PATTERNS = [
    '#([0-9]+)'
]


DATE_PATTERNS = [
    '[0-9]{4,4}-[0-9]{2,2}-[0-9]{2,2}',
    '[A-z]{3,3}\s[0-9]{1,2},\s[0-9]{4,4}'
]


TOTAL_DUE_PATTERNS = [
    '(Total|Total:)(\d+\.\d+)',
    '(Total\$|Total:\$)(\d+\,\d+\.\d+|\d+\.\d+)'
]