import os
import pathlib
from os.path import splitext
from urllib.parse import urlsplit

import requests
from dotenv import load_dotenv


def fetch_spacex_last_launch(combined_filepath, download_url_response):
    with open(combined_filepath, 'wb') as file:
        file.write(download_url_response.content)


def get_extension(url):
    url_path = urlsplit(url).path
    extension = splitext(url_path)[1]
    return extension


if __name__ == '__main__':
    load_dotenv()
    token = os.environ['SPACE_TOKEN']
    filename = 'spacex'
    folder_images = 'images'
    start_download_images = '2021-07-18'
    url = 'https://api.nasa.gov/planetary/apod'
    pathlib.Path(folder_images).mkdir(parents=True, exist_ok=True)

    params = {
        'api_key': token,
        'start_date': start_download_images
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    got_json = response.json()

    for link_number, link in enumerate(got_json, 1):
        image_url = link['url']
        extension = get_extension(image_url)
        download_url_response = requests.get(image_url)
        download_url_response.raise_for_status()
        combined_filepath = os.path.join(
            folder_images,
            f'{filename}{link_number}{extension}'
        )
        fetch_spacex_last_launch(combined_filepath, download_url_response)
