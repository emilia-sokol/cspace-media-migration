from generator import *
from extrator import *
from uploader import *


def do_full_media_migration(auth):
    # get objects ids from file or fetch all available ids from collection space
    ids = get_objects_ids(auth)
    for obj_id in ids:
        # get image file name from object's comment section saved in collection space
        images = extract_object_images(obj_id, auth)
        # filter out missing files and save that information to a file for further investigation
        existing_images = filter_existing_images(images, obj_id)

        for image in existing_images:
            # migrate each file to collection space and connect with object (add relation between media and object)
            migrate_media(obj_id, image, auth)

        # if some files were missing save that object id to a file for further investigation
        if len(existing_images) < len(images):
            with open(not_fully_migrated_ids_file_name, mode='at', encoding='utf-8') as file:
                file.write(obj_id + "\n")
            file.close()
        else:
            # else save that object id to another file so those files won't be migrated again
            with open(migrated_ids_file_name, mode='at', encoding='utf-8') as file:
                file.write(obj_id + "\n")
            file.close()


def filter_existing_images(images, obj_id):
    existing_images = []
    not_found = []
    for image in images:
        if image.get("file_name") == "":
            error = "[error] image with title " + image.get(
                "title") + " has no file name for object " + obj_id + "."
            not_found.append(image.get("title"))
            print(error)
        elif not exists("data/images/" + image.get("file_name")):
            error = "[error] image with file name " + image.get(
                "file_name") + " not found for object " + obj_id + "."
            not_found.append(image.get("file_name"))
            print(error)
        else:
            existing_images.append(image)
    if len(not_found) > 0:
        with open(img_error_file_name, mode='at', encoding='utf-8') as file:
            file.write(obj_id + " - " + ', '.join(not_found) + " - " + str(len(not_found)) + "/" + str(len(images)) + "\n")
        file.close()
    return existing_images


def migrate_media(obj_id, image, auth):
    # generate new id for media object (with id generator provided by collection space)
    new_id = generate_id(auth)
    # upload file and recevie blob id
    blob_id = upload_img(image.get("file_name"), auth)
    # upload additional media information with blob id and generated media id
    media_id = upload_media_data(image.get("title"), blob_id, new_id, auth)

    # relation needs to be bidirectional
    add_relation(obj_id, media_id, auth)
    add_relation(media_id, obj_id, auth)
