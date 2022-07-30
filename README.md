# Collection space media migration script
- Before running script go to ```constant.py``` and add url to your collection space instace -> collection_space
- Then add new folder ```data\images``` and put all files that need to be migrated there

## Expectations
1. Objects are already migrated into collection space
2. Each object has comment section that contains media information written in following format:

```xml
<IMAGE Iteration='1'>
    <TITLE>MPT.AH.902</TITLE>
    <LINK WIDTH='720' 
          HEIGHT='528' 
          PRINTABLE='1' 
          RequiresProcessing='0' 
          OryginalLocation='MPT.AH.902.jpg' 
          href='' 
          MediaSourceID='1' 
          PreviewId='7996' 
          PreviewOryginalLocation='MPT.AH13.jpg' 
          PREVWIDTH='300' 
          PREVHEIGHT='220' 
          prevhref='\\MPIT-S1\MusnetEXE\DB\media\previews\MPT.AH13.jpg' 
          xml-link='simple' 
          title='MPT.AH.902.jpg' 
          GUID='4A8736FC-7BDC-48AE-A056-575092F0FA5F'>7997</LINK>
    <DESC></DESC>
</IMAGE>
```
- media title will be taken from ```<TITLE></TITLE>``` tag
- media file name will be taken from ```<LINK>``` tag, attribute will be either ```title``` or ```prevhref```
- if changes are required please update ``` extract_object_images()``` function in ```extractor.py``` file
3. All images for migration are expected to be under ```data/images``` folder
4. When fetching objects list from collection space the response is expected in xml format with objects listed as following:

```xml 
<list-item>
    <csid>70c76d5d-e5d6-44e0-8440</csid>
    <uri>/collectionobjects/70c76d5d-e5d6-44e0-8440</uri>
    <refName>urn:cspace:arch.cs.ekomuzeum.pl:collectionobjects:id(70c76d5d-e5d6-44e0-8440)'MPT.AH.976'</refName>
    <updatedAt>2022-05-20T13:01:35.131Z</updatedAt>
    <workflowState>project</workflowState>
    <objectNumber>MPT.AH.976</objectNumber>
    <objectName>teczka</objectName>
    <title>Teczka „Naprawa STAR 266. rozdz. 14”</title>
    <responsibleDepartment>antiquities</responsibleDepartment>
</list-item>
```

## Notes
1. Objects that requires media migration will be listed in ```data/objects_ids.txt ``` in following format:

```txt
f9d42a00-0034-46c2-b3ca 
0f3ee458-cd4e-4e3b-9e67 
daf8bd74-bc55-4493-abd6 
80d54fa8-d94d-4541-808e 
```

where each line contains object's id from collection space
2. If file ```data/objects_ids.txt ``` is missing (e.g. has been deleted) script will get all objects ids from collection space and will pursue full migration (ids will be saved to file)

3. Migrated objects will be available in ```data/migrated_objects_ids.txt``` so if migration fails in progress and will be resumed, those objects won't be migrated again
4. In case some images cannot be found object id will be saved in ```data/not_fully_migrated_objects_ids.txt``` and in ```data/missing_images.txt``` there will be a list provided with all images there were missing in following format:

_object ID - missing-image1, missing-image2 ... - missing images count / all images count_
```txt
fd609613-b296-45ab-992b - MPT.AH.812 9.JPG, okładka.JPG - 2/11
4d921889-14fc-43db-b3ac - MPT.AH.811.JPG - 1/1
401612ee-9143-4d04-a552 - MPT.AH.810.JPG - 1/1
c67de1bc-3a15-43db-962f - MPT.AH.809.JPG - 1/1
4d01d444-9390-409e-a172 - MPT.AH.806.JPG, AH.806.JPG - 2/2
446c2070-7ed5-46fe-8a6b - AH.805.JPG, MPT.AH.805.JPG - 2/3
c4fe92e1-4f9d-4d8b-8881 - MPT.AH.804.JPG - 1/2
1fe57acf-1120-4453-9ccc - MPT.AH.772.jpg - 1/1
```
5. Objects saved in ```data/not_fully_migrated_objects_ids.txt``` won't be migrated during process as they potentially require some manual work, so once files are available for migration move ids from this file to ```data/objects_ids.txt``` and run script again
6. In ```constant.py``` file all constants can be updated such as collection space address, credentials, file names where data will be saved to or read from
7. To get better understanding of migration process look at file migration.py and read the comments
