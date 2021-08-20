import datetime
import os
import pathlib
from os.path import splitext
from urllib.parse import urlsplit, unquote

import requests
from dotenv import load_dotenv


def get_extension(url):
    unquoted_url = unquote(url)
    url_path = urlsplit(unquoted_url).path
    extension = splitext(url_path)[1]
    return extension


def get_epic_links(url, token):
    params = {'api_key': token}
    response = requests.get(url, params=params)
    response.raise_for_status()
    epic_links = response.json()
    return (epic_links)


def download_epic_images(epic_links, image_folder, epic_name, token):
    for link_number, link in enumerate(epic_links, 1):
        image_name = link['image']
        date = link['date']
        date_time = datetime.datetime.fromisoformat(date)
        formatted_date = date_time.strftime("%Y/%m/%d")
        download_url = f'https://api.nasa.gov/EPIC/archive/natural/' \
                       f'{formatted_date}/png/{image_name}.png'
        extension = get_extension(download_url)
        combined_filepath = os.path.join(
            image_folder,
            f'{epic_name}{link_number}{extension}'
        )
        download_image(combined_filepath, download_url, token)


def get_apod_links(url, token, download_start_date):
    params = {
        'api_key': token,
        'start_date': download_start_date
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    apod_links = response.json()
    return (apod_links)


def download_apod_images(apod_links, image_folder, apod_name, token):
    for link_number, link in enumerate(apod_links, 1):
        image_url = link['url']
        extension = get_extension(image_url)
        combined_filepath = os.path.join(
            image_folder,
            f'{apod_name}{link_number}{extension}'
        )
        download_image(combined_filepath, image_url, token)


def download_image(combined_filepath, download_url, token):
    params = {'api_key': token}
    download_url_response = requests.get(download_url, params=params)
    download_url_response.raise_for_status()
    with open(combined_filepath, 'wb') as file:
        file.write(download_url_response.content)


if __name__ == '__main__':
    load_dotenv()
    token = os.environ['SPACE_TOKEN']
    image_folder = 'images'
    epic_name = 'epic'
    apod_name = 'apod'
    download_start_date = '2021-07-18'
    epic_url = 'https://api.nasa.gov/EPIC/api/natural'
    apod_url = 'https://api.nasa.gov/planetary/apod'
    pathlib.Path(image_folder).mkdir(parents=True, exist_ok=True)
    epic_links = get_epic_links(epic_url, token)
    apod_links = get_apod_links(apod_url, token, download_start_date)
    download_epic_images(epic_links, image_folder, epic_name, token)
    download_apod_images(apod_links, image_folder, apod_name, token)
