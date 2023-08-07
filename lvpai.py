import os 
import re
import time
import random
import requests
import threading
import subprocess
from bs4 import BeautifulSoup

response = requests.get("https://www.bj520.com/photo-show-1870.html")
data = response.text
soup = BeautifulSoup(data)

city = soup.find(class_="city-title-list")
city_dict = dict([(i.text, re.findall("/photo-show-(\d+).html", i["href"])[0]) for i in city.find_all("a")])

city_photo = {}
for city, idx in city_dict.items():
    response = requests.get(f"https://www.bj520.com/photo-show-{idx}.html")
    data = response.text
    soup = BeautifulSoup(data)
    photos = [i["data-source"] for i in soup.find_all(class_="lightbox-pic")]
    city_photo.setdefault(city, []).extend(photos)
    print(f"city: {city}, photo_number: {len(photos)}")
    time.sleep(random.randint(1,3))

    
def download_city_photos(city, photo_list):
    print(f"city: {city} start")
    path = f"city_photo/{city}/"
    os.makedirs(path)
    for idx, photo in enumerate(photo_list):
        subprocess.call(["wget", '-O', path+str(idx)+'.jpg', photo])


threads = []
for city, photo_list in city_photo.items():
    thread = threading.Thread(target=download_city_photos, args=(city, photo_list,))
    thread.start()
    threads.append(thread)
for thread in threads:
    thread.join()