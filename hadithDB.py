import json
import sqlite3

editionsFile = open("../hadith-api/editions.json", "r", encoding="utf-8")
editionsData = json.load(editionsFile)
collectionDict = []

for collectionList, collectionListDetails in editionsData.items():
    for collection in collectionListDetails["collection"]:
        collectionDict.append(
            {"name": collection["name"], "language": collection["name"][:3]}
        )
conn = sqlite3.connect("hadith_search_full.db")
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS hadith;")
cursor.execute("CREATE VIRTUAL TABLE IF NOT EXISTS hadith USING FTS5(hadithnumber,arabicnumber,text,grades,bookNumber,bookhadith,bookname,language,shortname, tokenize = 'porter unicode61 remove_diacritics 1');")

collectionsFile = open("../hadith-api/updates/collections/collections.min.json")
collectionsData = json.load(collectionsFile)
collectionShortNameDict = {}
for collectionCategories in collectionsData["collections"]:
    for collectionFileNameObject in collectionCategories["books"]:
        collectionShortNameDict[collectionFileNameObject["eng-name"]] = collectionFileNameObject["name"]
    
for collectionDetails in collectionDict:
    print(collectionDetails["name"])
    inputFile = open(
        "../hadith-api/editions/" + collectionDetails["name"] + ".json",
        # "../hadith-api/editions/ara-muslim.json",
        "r",
        encoding="utf-8",
    )
    data = json.load(inputFile)

    for hadith in data["hadiths"]:
        value = None
        if 'arabicnumber' in hadith.keys():
            value = hadith["arabicnumber"]
        gradings = ""
        for grades in hadith["grades"]:
            gradings = gradings + grades["name"] + "::" + grades["grade"] + " && "
        if(gradings.endswith(" && ")):
            gradings = gradings[:-4]
        cursor.execute(
            f"""INSERT INTO hadith
            (hadithnumber,arabicnumber,text,grades,bookNumber,bookhadith,bookname,language,shortname)
            VALUES(?,?,?,?,?,?,?,?,?);""",
            (
                hadith["hadithnumber"],value,hadith["text"],gradings,hadith["reference"]["book"],hadith["reference"]["hadith"],data["metadata"]["name"],collectionDetails["language"],collectionShortNameDict[data["metadata"]["name"]]
            ),
        )
    print("complete")
conn.commit()
conn.close()