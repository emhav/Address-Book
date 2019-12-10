# tuodaan gspread kirjasto jotta google sheets api toimii
import gspread
# autetikointia varten, credentiaaleissa määritetty owner status jotta käytettävää google sheetsiä pystyy muokkaamaan
from oauth2client.service_account import ServiceAccountCredentials
#pretty print datan muotoilemista varten
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

#main funktio joka kutsuu muita funktioita käyttötarpeen mukaan
def main():

    print("\n1. Add a new address \n2. Find existing address \n3. Delete existing address \n4. Edit existing address")
    option = input("What do you want to do? (1-4): ")

    if option == "1":
        new_address()
    elif option == "2":
        find_address()
    elif option == "3":
        delete_address()
    elif option == "4":
        edit_address()

# funktio uuden oisoitteen lisäämiseksi
def new_address():

    print("Creating a new address")
    fname = input("First name: ")
    lname = input("Last name: ")
    address = input("Address: ")
    pcode = input("Postal code: ")
    city = input("City: ")
    country = input("Country: ")

    # yhdistetään lomakkeen tiedot yhdeksi person muuttujaksi
    person = [fname,lname,address,pcode,city,country]

    # alustetaan indeksiksi 2, jolloin lisättäessä sheets taulukkoon yhteystiedot järjestyvät uusimmasta vanhimpaan
    index = 2
    sheet.insert_row(person, index)
    print("A new address added successfully")

    # käyttäjällä mahdollisuus joko lopettaa ohjelma tai jatkaa käyttöä
    cont = input("Do you need to do something else? (y/n): ")

    if cont == "y":
        main()
    else:
        print("Goodbye")

# funktio tietyn osoitteen löytämiseksi
def find_address():

    address = input("Address or last name of the person you want to find: ")
    # etsii solun mistä haluttu tieto löytyy
    cell = sheet.find(address)
    #kertoo miltä riviltä etsitty osoite löytyy + tulostaa rivin datan kokonaisuudessaan
    print("Found an address at row %s" % (cell.row))
    print(sheet.row_values(cell.row))

    cont = input("Do you need to do something else? (y/n): ")

    if cont == "y":
        main()
    else:
        print("Goodbye")

# funktio tietyn osoitteen poistamiseksi
def delete_address():

    address = input("Address or last name of the person you want to delete: ")
    cell = sheet.find(address)
    print("Found an address at row %s" % (cell.row))
    print(sheet.row_values(cell.row))

    delete_addr = input("Do you want to delete this address? (y/n) ")

    #poistetaan tai säilytetään osoite
    if delete_addr == "y":
        #poisaa kokonaan rivin josta haluttu nimi/osite löytyi
        sheet.delete_row(cell.row)
        print("Person and address deleted successfully")
    elif delete_addr == "n":
        print("Okay we wont delete this address")

    cont = input("Do you need to do something else? (y/n): ")

    if cont == "y":
        main()
    else:
        print("Goodbye")

# funktio tietyn osoitteen muokkaamiseen
def edit_address():

    address = input("Address or last name of the person you want to edit: ")
    cell = sheet.find(address)
    print("Found an address at row %s" % (cell.row))
    print(sheet.row_values(cell.row))

    # uuden ositteen lisäys
    new_address = input("Insert a new address: ")
    # päivittää tietyn solun annetulla arvolla
    sheet.update_cell(cell.row,3,new_address)

    new_pcode = input("Insert a new postal code: ")
    sheet.update_cell(cell.row,4,new_pcode)

    #tarvittaessa pystyy myös muuttamaan tietyn ositteen kaupungin ja maan
    edit_more = input("Do you need to edit the city? (y/n) ")

    if edit_more == "y":
        new_city = input("Insert a new city: ")
        sheet.update_cell(cell.row,5,new_city)

        edit_further = input("Do you need to edit the country? (y/n) ")

        if edit_further == "y":
            new_country = input("Insert a new country: ")
            sheet.update_cell(cell.row,6,new_country)
            print("Updates saved")

        else:
            print("Updates saved")

    else:
        print("Updates saved")

    cont = input("Do you need to do something else? (y/n): ")

    if cont == "y":
        main()
    else:
        print("Goodbye")

main()