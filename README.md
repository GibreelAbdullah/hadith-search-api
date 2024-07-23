# OLD ARCHIVED VERSION. USE [Hadith Search API 2.0](https://github.com/GibreelAbdullah/hadith-search-api-2.0)

## This service provides the Search functionality in hadithhub.com

## Reason for a separate service

HadithHub gets the hadith data using [hadith-api](https://github.com/GibreelAbdullah/hadith-api) which stores all the hadith data as json files. There is no server running. This is really convinient and economical but it has its downsides. We can't easily search the files, but search functionality is essential, so I had to create a separate service to cater to the search functionality.

## How it works

Prerequisite - hadith-api repo and this repo should both be present in the local system with both sharing the same parent directory.

hadithDB.py - It iterates through all the hadith files in hadith-api and creates a sqlite database with that data.

app.py - Open up a port which provides the search functionality.

## Docker Build Commands

Go to the root of the project
```bash
docker build -t gibreelabdullah/hadith-search-api:latest . &&

docker push gibreelabdullah/hadith-search-api:latest
```
put gibreelabdullah/hadith-search-api:latest in koyeb

----------------------------------------------------

To test locally run

```bash
docker run --publish 5000:5000 gibreelabdullah/hadith-search-api:latest
```
----------------------------------------------------

https://hadith-search-api-gibreelabdullah.koyeb.app/search?q=Allah

# NOTES

## FTS5 default (bm25)
- Used FTS5 search based on bm25 inverted index.
- Not giving accurate results for larger hadith which contain all the serach words. Known issue of bm25.
- In case of a search string with multiple words, each word has the same weight. So for a search term "A B", both "A" and "B" occur once in document X, and "A" occurs 5 times in documnt Y. Document Y will be ranked first. While common sense says that a complete match should be first.
- To mitigate this issue, I search for the complete string "A B" in the database and then append the results obtained by "A OR B", but it considerably slows down the speed.

## Meilisearch
- Memory consumption was too high. (8 GB)

## Apache Solr
- Still in consideration. Will check back on this.

## AI Search (KNN using FAISS)

- MBert (bert-base-multilingual-uncased)
    - The accuracy was extremely low

- MPnet (paraphrase-multilingual-mpnet-base-v2)
    - Accuracy is good, but really slow. For NVV (Non Vocabulary Words) it is not performing well.
