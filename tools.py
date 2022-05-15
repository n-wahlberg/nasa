import json
import requests
from datetime import datetime
import sys
import csv
import os
import pandas as pd
import sqlite3 as sql


def get_key():
    with open('apikeys/apikey.txt') as f:
        return f.read()


class Query:
    query_timestamp = datetime.now()
    url_base = "https://api.nasa.gov/EPIC/api"
    api_key = get_key()
    img_type = 'jpg'

    # Takes basic params and generates url for the query
    def __init__(self, img_state="natural", date="all"):
        self.img_state = img_state
        if date != "all":
            self.year = date[:4]
            self.month = date[5:7]
            self.day = date[8:10]
            self.url = f"{self.url_base}/{img_state}/date/{self.year}-{self.month}-{self.day}?api_key={self.api_key}"
            self.query_type = "specific"
        else:
            self.url = f"{self.url_base}/{img_state}/all?api_key={self.api_key}"
            self.query_type = "general"

    def __repr__(self):
        if hasattr(self, 'payload'):  # checks to see if the query has a payload
            return f"{self.query_type} query created {self.query_timestamp}\npayload status: {self.payload.status_code}"
        else:
            return f"{self.query_type} query created {self.query_timestamp}\npayload status: NO DATA YET RETRIEVED"

    # Performs an api request and stores the payload in the Query object
    def retrieve_data(self):
        self.payload = requests.get(self.url)
        if self.payload.status_code == 200:
            print(f"Successfully retrieved '{self.query_type}' payload")
        else:
            print(f"Query Failure - Status Code: {self.payload.status_code}")


# returns a list of dates for which there is NO existing data
def check_house(query):
    if query.query_type == "general":
        old_dates = []
        target_dates = []
        with open("Data/natural/rawData.json") as existingData:
            old_data = json.load(existingData)
        for old_date in old_data:
            if old_date['date'][:10] not in old_dates:
                old_dates.append(old_date['date'][:10])
        for new_date in query.payload.json():
            if new_date['date'] not in old_dates:
                target_dates.append(new_date['date'])
        return target_dates


# downloads image data for dates not found in the rawData.json file
def update_inhouse_data(query):
    new_data_list = []
    for target_date in check_house(query):
        q = Query(query.img_state, target_date)
        q.retrieve_data()
        if len(q.payload.json()) > 0:
            for item in q.payload.json():
                new_data_list.append(item)
                print(f"Data retrieved for {target_date}")
        else:
            print(f"No data available for {target_date}")
    with open('Data/natural/newRawData.json', 'w') as f:
        json.dump(new_data_list, f)


# merges rawData.json and newRawData.json into updated rawData.json - removes newRawData.json
def clean_up():
    full_data = []
    with open('Data/natural/newRawData.json') as f:
        l1 = json.load(f)
        for item in l1:
            full_data.append(item)

    with open('Data/natural/rawData.json') as f:
        l2 = json.load(f)
        for item in l2:
            full_data.append(item)

    with open('Data/natural/rawData.json', 'w') as f:
        json.dump(full_data, f)

    os.remove('Data/natural/newRawData.json')


# locally saves images associated with an EPIC query
def save_images(query):
    s = query.payload.json()
    for location in s:
        url = "https://api.nasa.gov/EPIC/archive/{0}/{1}/{2}/{3}/{4}/{5}.jpg?api_key={6}" \
            .format(query.img_state, query.year, query.month, query.day, query.img_type, location['image'],
                    query.api_key)
        img = requests.get(url)
        with open(f"images/{location['image']}.jpg", "wb") as f:
            f.write(img.content)
