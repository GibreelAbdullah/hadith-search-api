import json
import sqlite3


editionsFile = open("../hadith-api/editions.json", "r", encoding="utf-8")
editionsData = json.load(editionsFile)
collectionDict = []
# setLang = set()

for collectionList, collectionListDetails in editionsData.items():
    for collection in collectionListDetails["collection"]:
        # if(collection["name"].split("-")[0] == "eng"):
        collectionDict.append(
            {"name": collection["name"], "language": collection["name"][:3]}
        )
#         setLang.add(1collection["name"].split("-")[0])
# # collectionDict = [{"name": "eng-malik", "language": "English"}]
# print(setLang)

conn = sqlite3.connect("hadith_search_full.db")
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS hadith;")
cursor.execute("CREATE VIRTUAL TABLE IF NOT EXISTS hadith USING FTS5(hadithnumber,text,grades,bookNumber,bookhadith,bookname,language);")

for collectionDetails in collectionDict:
    print(collectionDetails["name"])
    inputFile = open(
        "../hadith-api/editions/" + collectionDetails["name"] + ".json",
        "r",
        encoding="utf-8",
    )
    data = json.load(inputFile)

    for hadith in data["hadiths"]:
        # hadith["bookname"] = data["metadata"]["name"]
        # hadith["language"] = collectionDetails["language"]
        # hadith.pop("arabicnumber", None)  # remove arabic number, not needed
        # # hadith["url"] = (
        # #     collectionDetails["name"] + ".json:" + str(hadith["hadithnumber"])
        # # )
        # hadith["bookNumber"] = hadith["reference"]["book"]
        # hadith["bookhadith"] = hadith["reference"]["hadith"]
        gradings = ""
        for grades in hadith["grades"]:
            gradings = gradings + grades["name"] + ":" + grades["grade"] + " && "
        if(gradings.endswith(" && ")):
            gradings = gradings[:-4]
        # hadith["gradings"] = gradings
        # hadith.pop("arabicnumber", None)  # remove arabic number, not needed
        # hadith.pop(
        #     "reference", None
        # )  # remove reference object, added book and hadith separately
        # hadith.pop(
        #     "grades", None
        # )  # remove grades object, added grading as a single string
        cursor.execute(
            f"""INSERT INTO hadith
            (hadithnumber,text,grades,bookNumber,bookhadith,bookname,language)
            VALUES(?,?,?,?,?,?,?);""",
            (
                hadith["hadithnumber"],hadith["text"],gradings,hadith["reference"]["book"],hadith["reference"]["hadith"],data["metadata"]["name"],collectionDetails["language"]
            ),
        )
        # cursor.execute(
        #     f"""INSERT INTO hadith
        #     (data)
        #     VALUES(?);""",
        #     (
        #         (json.dumps(hadith),)
        #     ),
        # )
conn.commit()
conn.close()