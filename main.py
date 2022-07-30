# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from requests.auth import HTTPBasicAuth
from migration import *
import getpass


def authenticate():
    authenticated = False
    username = ""
    password = ""
    while authenticated is not True:
        print("Enter credentials")
        username = input("Username: ")
        password = getpass.getpass("Password: ")

        # check if credentials are valid
        api_url = cspace_services + "/collectionobjects"
        response = requests.get(api_url, auth=HTTPBasicAuth(username, password))
        if response.status_code == 200:
            authenticated = True
            print("Authentication succeeded")
        else:
            print("Try again. Status code: " + str(response.status_code) + ", " + response.text)

    return HTTPBasicAuth(username, password)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # if you are sure your credentials are correct add them below and uncomment that line instead of the line after that
    # auth = HTTPBasicAuth('sample@username.com', 'password')
    auth = authenticate()
    do_full_media_migration(auth)
