from constant import *
import requests
from bs4 import BeautifulSoup


def generate_id(auth):
    print("generating new id ...")
    api_url = cspace_services + "/idgenerators/cd91d8b8-f346-4925-a425-93e02bd1c5c9"
    additional_params = "?wf_deleted=false"
    response = requests.get(api_url + additional_params, auth=auth)
    bs_generator = BeautifulSoup(response.text, "xml")
    new_id = ""

    # TODO: [important] revise this logic after reaching ID MR2022.999999.999999
    children = list(filter(lambda x: x.find("currentValue") is not None, bs_generator.find("parts").findChildren()))
    children.reverse()
    check_max = True
    for child in children:
        current = child.find("currentValue").text
        if (child.find("maxLength") is not None) & check_max:
            if (int(len(current)) == int(child.find("maxLength").text)) & all(ch in current for ch in "9"):
                new_id = child.find("initialValue").text + new_id
            else:
                check_max = False
                try:
                    new_id = str(int(child.find("currentValue").text) + 1) + new_id
                except:
                    print("new id can't be generated, possibly all numbers were used")
        else:
            check_max = False
            new_id = child.find("currentValue").text + new_id

    try:
        requests.post(api_url + "/ids", data=new_id, auth=auth)
        if response.status_code != 200:
            print(
                "[error] new id " + new_id + " couldn't be created, message " + str(response.text))
            raise SystemExit()
    except requests.exceptions.RequestException as e:
        print(
            "[error] new id " + new_id + " couldn't be created, message " + str(e))
        raise SystemExit(e)

    print("success\n")
    return new_id
