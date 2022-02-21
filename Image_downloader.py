import random
import time

from pyunsplash import PyUnsplash
import requests
import os
import add_text_and_logo

# instantiate PyUnsplash object
Unsplash_access_key = ""  # enter your unsplash key
pu = PyUnsplash(api_key=Unsplash_access_key)
directory = 'Unsplash_images'


def create_directory(directory_name):
    try:
        os.makedirs(directory_name, exist_ok=True)
        print("Directory '%s' created successfully" % directory)
        return True
    except OSError as error:
        print("Directory '%s' can not be created" % directory)
        return False


def download_images(number_of_images, target_directory="downloaded_images"):
    keyword = ["school", "study", "students", "essay writing", "university", "college", "learning", "reading",
               "assignment", "coursework", "writer", "thesis", "school thesis", "research paper", "dissertation"]
    if create_directory(target_directory):
        pass
    else:
        return False
    for i in range(0, number_of_images):
        file_name = directory + "/image_" + str(i) + ".png"
        photos = pu.photos(type_='random', count=1, featured=True, query=random.choice(keyword))
        [photo] = photos.entries
        print(photo.id, photo.link_download)
        response = requests.get(photo.link_download, allow_redirects=True)
        open(file_name, 'wb').write(response.content)


directory = "processed directory"

# quotes_option.main("processed_research_paper", "research paper")
"""for directory in directories:
    # download images and add text and logo on them
    download_images(45, directory)
    add_text_and_logo.main("processed_" + directory, directory)
    # sleep for one hour to avoid unsplush ip request limit
    time.sleep(3600)"""
