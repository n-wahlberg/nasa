import requests
import json
import os
reponse = requests.get("https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&camera=fhaz&api_key=Ibh5wa8SoddBI5ekjRlVvgIKS6I4VYDuNGndsqwh")

print(reponse.json())

photos = []
for img in reponse.json()['photos']:
    photos.append(requests.get(img['img_src']).content)

count = 0
for photo in photos:
    f = open(f'photo{count}.JPG', "wb")
    f.write(photo)
    f.close()
    count += 1
