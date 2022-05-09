import json
import os
import requests
import math

# retrieves the api key
def get_key():
    with open('apikey.txt', 'r') as f:
        key = f.read()
    return key

# returns a dictionary according to the defined parameters, and the string variable imgState
# imgState == 'natural' or 'enhanced'
# date == 'most recent'; 'all'; or 'YYYY-MM-DD'
def query_api(imgState, date):
    api_key = get_key()
    if date == 'most recent':
        url = f'https://api.nasa.gov/EPIC/api/{imgState}?api_key={api_key}'
        return json.loads(requests.get(url).content), imgState
    elif date == 'all':
        url = f'https://api.nasa.gov/EPIC/api/{imgState}/all?api_key={api_key}'
        lst = []
        count = 900
        for item in json.loads(requests.get(url).content)[900:]:
            dateScroll = item['date']
            url = f'https://api.nasa.gov/EPIC/api/{imgState}/date/{dateScroll}?api_key={api_key}'
            for item in json.loads(requests.get(url).content):
                with open('Data/natural/database.json', 'a') as f:
                    f.write(json.dumps(item))
            print (item['date'])
            print ('itemCount: ', count)
            count += 1
        return lst, imgState

    else:
        url = f'https://api.nasa.gov/EPIC/api/{imgState}/date/{date}?api_key={api_key}'
        print (url)
        return json.loads(requests.get(url).content), imgState


def moonseeker(dict):
    luna = []
    for item in dict:
        if abs(item['dscovr_j2000_position']['x'] - item['lunar_j2000_position']['x']) <= 1:
            luna.append(item)
    if len(luna) > 0:
        print (len(luna), 'matching records')
        return True
    else:
        print ('no matching records')
        return False


# saves each image referenced in dict locally
# filePath == 'string' to name image destination in CWD
def save_images(dict, imgState, filePath):

    if filePath not in os.listdir():
        os.mkdir(filePath)

    count = 0
    for item in dict:
        year = item['date'][0:4]
        month = item['date'][5:7]
        day = item['date'][8:10]
        img_name = item['image']

        img = requests.get(f'https://epic.gsfc.nasa.gov/archive/{imgState}/{year}/{month}/{day}/jpg/{img_name}.jpg')

        with open(f'{filePath}/{year}_{month}_{day}_{imgState}_{count}.jpg', 'wb') as f:
            f.write(img.content)

        count += 1

# aligns and prints satellite and lunar positions
def print_coords(dict):
    for item in dict:
        dx = str(item['dscovr_j2000_position']['x'])
        dy = str(item['dscovr_j2000_position']['y'])
        dz = str(item['dscovr_j2000_position']['z'])
        lx = str(item['lunar_j2000_position']['x'])
        ly = str(item['lunar_j2000_position']['y'])
        lz = str(item['lunar_j2000_position']['z'])

        print ('%s  ::  %s  ::  %s' % (dx.ljust(15, '0'), dy.ljust(15, '0'), dz.ljust(15, '0')))
        print ('%s  ::  %s  ::  %s' % (lx.ljust(15, '0'), ly.ljust(15, '0'), lz.ljust(15, '0')))
        print ('\n')
