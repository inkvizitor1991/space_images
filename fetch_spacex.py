import os
import pathlib

import requests
from downloading_photos import download_image


def get_spacex_links():
    url = 'https://api.spacexdata.com/v4/launches/latest'
    response = requests.get(url)
    response.raise_for_status()
    spacex_links = response.json()['links']['flickr']['original']
    return spacex_links


def download_spacex_images(spacex_links, image_folder, filename):
    for link_number, link in enumerate(spacex_links, 1):
        filepath = os.path.join(
            image_folder,
            f'{filename}{link_number}.jpg'
        )
        download_image(filepath, link)


if __name__ == '__main__':
    filename = 'spacex'
    image_folder = 'images'
    pathlib.Path(image_folder).mkdir(parents=True, exist_ok=True)
    spacex_links = get_spacex_links()
    download_spacex_images(spacex_links, image_folder, filename)
