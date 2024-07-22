import os
import re
import requests
import logging
import sys
from yt_dlp import YoutubeDL

if sys.version_info[:2] != (3, 11):
    sys.stderr.write("This script requires Python 3.11\n")
    sys.exit(1)

# Replace 'your_api_key' with your actual TMDB API key
TMDB_API_KEY = 'YOURAPIKEY'
BASE_URL = 'https://api.themoviedb.org/3'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_movie_title(title):
    cleaned_title = re.sub(r'\(\d{4}\)', '', title).strip()
    return cleaned_title

def get_movie_id(title):
    search_url = f"{BASE_URL}/search/movie"
    params = {
        'api_key': TMDB_API_KEY,
        'query': title
    }
    response = requests.get(search_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            logger.info(f"TMDB returned movie: {data['results'][0]['title']}")
            return data['results'][0]['id']
    return None

def get_trailer_url(movie_id):
    trailer_url = f"{BASE_URL}/movie/{movie_id}/videos"
    params = {
        'api_key': TMDB_API_KEY
    }
    response = requests.get(trailer_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            for video in data['results']:
                if video['site'] == 'YouTube' and video['type'] == 'Trailer':
                    trailer_link = f"https://www.youtube.com/watch?v={video['key']}"
                    logger.info(f"Trailer URL: {trailer_link}")
                    return trailer_link
    return None

def download_trailer(url, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    video_file = os.path.join(dest_folder, 'video1.mp4')
    ydl_opts = {
        'format': 'best',
        'outtmpl': video_file,
        'quiet': True,
        'no_warnings': True
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        logger.info(f"Trailer downloaded to {video_file}")
        return video_file
    except Exception as e:
        logger.error(f"Error downloading trailer: {e}")
    return None

def process_movie_directories(base_dir):
    for root, dirs, files in os.walk(base_dir):
        for dir in dirs:
            if dir.lower() == 'backdrops':
                continue
            movie_dir = os.path.join(root, dir)
            backdrops_folder = os.path.join(movie_dir, 'backdrops')
            if os.path.exists(os.path.join(backdrops_folder, 'video1.mp4')) or os.path.exists(os.path.join(backdrops_folder, 'video1.mkv')):
                logger.info(f"Trailer already exists for {dir}. Skipping download.")
                print(f"Trailer already exists for {dir}.")
                continue
            original_title = dir
            cleaned_title = clean_movie_title(original_title.replace('_', ' ').replace('.', ' '))
            movie_id = get_movie_id(cleaned_title)
            if movie_id:
                trailer_url = get_trailer_url(movie_id)
                if trailer_url:
                    download_trailer(trailer_url, backdrops_folder)

if __name__ == "__main__":
    current_directory = os.path.dirname(os.path.abspath(__file__))
    process_movie_directories(current_directory)
