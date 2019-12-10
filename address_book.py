import gc
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint


# alustetaan google sheets api, jotta python koodi pystyy kommunikoimaan google sheetsin kanssa
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(credentials)

# google sheets taulukko johon yhteystiedot lisätään
sheet = client.open("Addressbook").sheet1

# tulostaa taulukon olemassa olevan datan
all_data = sheet.get_all_records()

# "pretty print" moduuli muotoilee taulukossa olevan datan helpommin luettavaksi
pprint(all_data)

# lomake uuden yhteystiedon lisäämiseen

def main():

    answer = input('Do you want to add a new address? ')

    if answer == "yes":
        new_address()

    if answer == "no":
        finding_address()


def new_address():

    fname = input('First name: ')
    lname = input('Last name: ')
    address = input('Address: ')
    phone = int(input('Phone: '))

    # yhdistetään lomakkeen tiedot yhdeksi person muuttujaksi
    person = [fname,lname,address,phone]

    # alustetaan indeksiksi 2, jolloin lisättäessä sheets taulukkoon yhteystiedot järjestyvät uusimmasta vanhimpaan
    index = 2
    sheet.insert_row(person, index)
    print('New person and address added successfully')

def finding_address():

    person = input('Who do you want to find? ')

    cell = sheet.find(person)

    print('Found something at row %s' % (cell.row))
    print(sheet.row_values(cell.row))

def deleting_address():
    person = input('Which person you want to delete? ')
    cell = sheet.find(person)
    print('Found something at row %s' % (cell.row))
    print(sheet.row_values(cell.row))
    delete_person = input('Do you want to delete this person? (y/n) ')

    if delete_person == 'y':
        sheet.delete_row(cell.row)
        print('Person and address deleted successfully')
    elif delete_person == 'n':
        print("Okay we won't delete that person or address")

