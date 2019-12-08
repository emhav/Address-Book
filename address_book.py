import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

client = gspread.authorize(credentials)

sheet = client.open("Addressbook").sheet1

data = sheet.get_all_records()

pprint(data)

def new_address():

    name = input('Name: ')
    address = input('Address: ')
    phone = int(input('Phone: '))

    person = [name,address,phone]

    index = 2

    sheet.insert_row(person, index)
    print('New person and address added successfully')
    
new_address()

