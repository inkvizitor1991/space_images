import datetime
import os
import pathlib
from os.path import splitext
from urllib.parse import urlsplit

import requests
from dotenv import load_dotenv


def get_extension(url):
    url_path = urlsplit(url).path
    extension = splitext(url_path)[1]
    return extension


def fetch_nasa_last_launch(combined_filepath, download_url_response):
    with open(combined_filepath, 'wb') as file:
        file.write(download_url_response.content)


if __name__ == '__main__':
    load_dotenv()
    token = os.environ['SPACE_TOKEN']
    filename = 'nasa'
    folder_images = 'images'

    url = f'https://api.nasa.gov/EPIC/api/natural/images?api_key={token}'
    pathlib.Path(folder_images).mkdir(parents=True, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    got_json = response.json()

    for link_number, link in enumerate(got_json, 1):
        params = {
            'api_key': token
        }
        image_name = link['image']
        date = link['date']
        date_time = datetime.datetime.fromisoformat(date)
        formatted_date = date_time.strftime("%Y/%m/%d")
        download_url = f'https://api.nasa.gov/EPIC/archive/natural/' \
            f'{formatted_date}/png/{image_name}.png'
        download_url_response = requests.get(download_url, params=params)
        download_url_response.raise_for_status()
        image_url = download_url_response.url
        extension = get_extension(image_url)
        combined_filepath = os.path.join(
            folder_images,
            f'{filename}{link_number}{extension}'
        )
        fetch_nasa_last_launch(combined_filepath, download_url_response)
