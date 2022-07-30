import requests
from constant import *


def upload_img(img_path, auth):
    print("uploading img " + img_path + " ...")
    api_url = cspace_services + "/blobs"
    try:
        with open("data/images/" + img_path, 'rb') as payload:
            response = requests.post(api_url, files={"file": payload}, auth=auth)
            if response.status_code != 201:
                print(
                    "[error] file " + img_path + " couldn't be uploaded, message " + str(response.text))
                raise SystemExit()
            print("success\n")
            payload.close()
            # there should be new blob id in the location header
            return response.headers.get("Location").rsplit('/', 1)[-1]
    except requests.exceptions.RequestException as e:
        print(
            "[error] file " + img_path + " couldn't be uploaded, message " + str(e))
        raise SystemExit(e)


def upload_media_data(img_title, blob_id, generated_id, auth):
    print("uploading media data for " + img_title + " ...")
    api_url = cspace_services + "/media"
    payload = {
        "document": {
            "ns2:media_common": {
                "@xmlns:ns2": "http://collectionspace.org/services/media",
                "dateGroupList": {
                    "dateGroup": {
                        "scalarValuesComputed": False
                    }
                },
                "blobCsid": blob_id,
                "identificationNumber": generated_id,
                "title": img_title,
                "description": img_title
            }
        }
    }

    try:
        response = requests.post(api_url, json=payload, auth=auth)
        if response.status_code != 201:
            print(
                "[error] Media information for " + img_title + " couldn't be saved, message " + str(response.text))
            raise SystemExit()
        print("success\n")
        # there should be new media id in the location header
        return response.headers.get("Location").rsplit('/', 1)[-1]
    except requests.exceptions.RequestException as e:
        print(
            "[error] Media information for " + img_title + " couldn't be saved, message " + str(e))
        raise SystemExit(e)


def add_relation(object_id, subject_id, auth):
    print("adding relation " + object_id + " > " + subject_id + " ...")
    api_url = cspace_services + "/relations"
    payload = {
        "document": {
            "rel:relations_common": {
                "@xmlns:rel": "http://collectionspace.org/services/relation",
                "subjectCsid": subject_id,
                "objectCsid": object_id,
                "relationshipType": "affects"
            }
        }
    }

    try:
        response = requests.post(api_url, json=payload, auth=auth)
        if response.status_code != 201:
            print(
                "[error] Relation between " + object_id + " and " + subject_id + " couldn't be saved, message " + str(
                    response.text))
            raise SystemExit()
    except requests.exceptions.RequestException as e:
        print(
            "[error] Relation between " + object_id + " and " + subject_id + " couldn't be saved, message " + str(e))
        raise SystemExit(e)
    print("success\n")
