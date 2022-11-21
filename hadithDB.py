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
cursor.execute("CREATE VIRTUAL TABLE IF NOT EXISTS hadith USING FTS5(hadithnumber,text,grades,bookNumber,bookhadith,bookname,language,shortname);")

collectionsFile = open("../hadith-api/01-Collections/collections.json")
collectionsData = json.load(collectionsFile)
collectionShortNameDict = {}
for collectionFileNameObject in collectionsData["collections"]:
    collectionShortNameDict[collectionFileNameObject["eng-name"]] = collectionFileNameObject["name"]
    
for collectionDetails in collectionDict:
    print(collectionDetails["name"])
    inputFile = open(
        "../hadith-api/editions/" + collectionDetails["name"] + ".json",
        "r",
        encoding="utf-8",
    )
    data = json.load(inputFile)

    for hadith in data["hadiths"]:
        gradings = ""
        for grades in hadith["grades"]:
            gradings = gradings + grades["name"] + "::" + grades["grade"] + " && "
        if(gradings.endswith(" && ")):
            gradings = gradings[:-4]
        cursor.execute(
            f"""INSERT INTO hadith
            (hadithnumber,text,grades,bookNumber,bookhadith,bookname,language,shortname)
            VALUES(?,?,?,?,?,?,?,?);""",
            (
                hadith["hadithnumber"],hadith["text"],gradings,hadith["reference"]["book"],hadith["reference"]["hadith"],data["metadata"]["name"],collectionDetails["language"],collectionShortNameDict[data["metadata"]["name"]]
            ),
        )
conn.commit()
conn.close()