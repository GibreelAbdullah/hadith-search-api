# start by pulling the python image
FROM python:bullseye

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY ./app.py /app/app.py
COPY ./query.py /app/query.py
# COPY ./fts5stemmer.so /app/fts5stemmer.so
COPY ./hadith_search_full.db /app/hadith_search_full.db
# COPY ./app.py /app/app.py

# configure the container to run in an executed manner
ENTRYPOINT [ "python3" ]

CMD ["app.py" ]