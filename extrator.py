import requests
import xml.etree.ElementTree as ET

from constant import *
from os.path import exists
from bs4 import BeautifulSoup
from html import unescape


def get_objects_ids(auth):
    if exists(ids_file_name):
        print("ids were saved, fetching won't be executed - in case that is required please delete file "
              + ids_file_name)
        file = open(ids_file_name, 'r')
        to_migrate = file.read().splitlines()

        # don't migrate files for object that were migrated before
        if exists(migrated_ids_file_name):
            migrated_file = open(migrated_ids_file_name, 'r')
            migrated = migrated_file.read().splitlines()
            to_migrate = [x for x in to_migrate if x not in migrated]

        # don't migrate files for object that were migrated before with some issues that need to be resolved manually
        if exists(not_fully_migrated_ids_file_name):
            not_migrated_file = open(not_fully_migrated_ids_file_name, 'r')
            not_migrated = not_migrated_file.read().splitlines()
            to_migrate = [x for x in to_migrate if x not in not_migrated]
        return to_migrate
    else:
        # get all object ids from collection space and save to file
        ids = fetch_objects_ids(0, 100, auth)
        with open(ids_file_name, mode='wt', encoding='utf-8') as file:
            file.write('\n'.join(ids))
        file.close()
        return ids


def fetch_objects_ids(pg_num, pg_size, auth):
    api_url = cspace_services + "/collectionobjects"
    additional_params = "?pgNum=" + str(pg_num) + "&pgSz=" + str(pg_size) + "&wf_deleted=false"
    response = requests.get(api_url + additional_params, auth=auth)
    print("http call: " + api_url + additional_params + " with response: " + str(response.status_code))
    bs_data = BeautifulSoup(response.text, "xml")
    items = bs_data.find_all('list-item')
    items_in_page = bs_data.find_all('itemsInPage')[0].string
    total_items = bs_data.find_all('totalItems')[0].string

    ids = []
    for item in items:
        ids.append(item.findChildren("csid", recursive=False)[0].string)

    if int(items_in_page) < pg_size | (int(total_items) % pg_size == 0 & pg_size * pg_num == total_items):
        return ids
    else:
        additional_ids = fetch_objects_ids(pg_num + 1, pg_size)
        return ids + additional_ids


# Edit or override this function if images extraction should work differently with your particular dataset
def extract_object_images(obj_id, auth):
    api_url = cspace_services + "/collectionobjects/" + obj_id
    response = requests.get(api_url, auth=auth)
    bs_data = BeautifulSoup(response.text, "xml")
    comments = bs_data.find_all('comment')
    # there is an expectation that there will be only one comment
    comment_text = unescape(comments[0].string)
    tree = ET.ElementTree(ET.fromstring("<comment>" + comment_text + "</comment>"))
    root = tree.getroot()

    images = []
    for img in root.iter('IMAGE'):
        title = img.find('TITLE').text
        file_name = img.find('LINK').attrib["title"]

        if file_name == "":
            file_name = (img.find('LINK').attrib["prevhref"]).rsplit('\\', 1)[-1]

        images.append({"title": title, "file_name": file_name, "obj_id": obj_id})

    return images
