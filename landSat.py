import json
import requests
import os

# retrieves the API key
def get_key():
    with open('API Key.txt', 'r') as f:
        key = f.read()
    return key

def peek(lat, lon, dim, date):
    api_key = get_key()
    query_url = f'https://api.nasa.gov/planetary/earth/assets?lat={lat}&lon={lon}&dim={dim}&api_key={api_key}&date={date}'

    response = requests.get(query_url)

    print (response.json())
