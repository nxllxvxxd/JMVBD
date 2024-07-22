import os
import re
import requests
import logging
import sys
from yt_dlp import YoutubeDL
import base64

# Ensure the script is running with Python 3.11
if sys.version_info[:2] != (3, 11):
    sys.stderr.write("This script requires Python 3.11\n")
    sys.exit(1)

# File to store the TMDB API key
API_KEY_FILE = 'apikey.txt'

# Function to get TMDB API key from the file
def get_tmdb_api_key():
    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, 'r') as file:
            encoded_key = file.read().strip()
            if encoded_key:
                decoded_key = base64.b64decode(encoded_key).decode('utf-8')
                return decoded_key
    return None

# Function to prompt the user for TMDB API key and save it to the file
def prompt_for_tmdb_api_key():
    api_key = input("You have not input your TMDB API key. Please provide it now: ").strip()
    if api_key:
        encoded_key = base64.b64encode(api_key.encode('utf-8')).decode('utf-8')
        with open(API_KEY_FILE, 'w') as file:
            file.write(encoded_key)
        return api_key
    else:
        sys.stderr.write("TMDB API key is required. Exiting...\n")
        sys.exit(1)

# Get TMDB API key from file or prompt for it
TMDB_API_KEY = get_tmdb_api_key()
if not TMDB_API_KEY:
    TMDB_API_KEY = prompt_for_tmdb_api_key()

BASE_URL = 'https://api.themoviedb.org/3'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to clean movie title by removing the year in parentheses
def clean_movie_title(title):
    cleaned_title = re.sub(r'\(\d{4}\)', '', title).strip()
    return cleaned_title

# Function to get the movie ID from the title
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

# Function to get the trailer URL for the movie
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

# Function to download the YouTube trailer using yt-dlp
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

# Main function to process movie directories
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
