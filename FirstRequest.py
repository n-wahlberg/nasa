import requests
import json
import os

api_key = 'YiprgnpLK7YiDFJ8SasjxOZjCtiyeJhYuD9HhVn8'

"""
# retrieves the API key
def get_key():
    with open('API Key.txt', 'r') as f:
        key = f.read()
    return key

# generates the query url
def query_url(rover, sol, camera):
    api_key = get_key()
    url = f'https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos?sol={sol}&camera={camera}&api_key={api_key}'
    return url
"""
def retrieveImages(rover, sol, camera, path):
    query_url = f'https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos?sol={sol}&camera={camera}&api_key={api_key}'
    response = requests.get(query_url)

    dict = json.loads(response.content)

    count = 1

    for img in dict['photos']:
        jpg = requests.get(img['img_src'])
        with open(f'{path}/image_{count}.jpg', 'wb') as f:
            f.write(jpg.content)
        count += 1

    print (f'{count} images retrieved and saved locally')
