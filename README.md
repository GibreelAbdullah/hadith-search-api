# This service provides the Search functionality in hadithhub.com

## Reason for a separate service

HadithHub gets the hadith data using [hadith-api](https://github.com/GibreelAbdullah/hadith-api) which stores all the hadith data as json files. There is no server running. This is really convinient and economical but it has its downsides. We can't easily search the files, but search functionality is essential, so I had to create a separate service to cater to the search functionality.

## How it works

Prerequisite - hadith-api repo and this repo should both be present in the local system with both sharing the same parent directory.

hadithDB.py - It iterates through all the hadith files in hadith-api and creates a sqlite database with that data.

app.py - Open up a port which provides the search functionality.

## Docker Build Commands

Go to the root of the project

docker build -t gibreelabdullah/hadith-search-api:latest . &&

docker push gibreelabdullah/hadith-search-api:latest

----------------------------------------------------

put gibreelabdullah/hadith-search-api:latest in koyeb
