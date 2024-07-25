import os
import re
import requests
import logging
import sys
import sqlite3
from yt_dlp import YoutubeDL
import base64
import subprocess

if sys.version_info[:2] != (3, 11):
    sys.stderr.write("\033[91mThis script requires Python 3.11\n\033[0m")
    sys.exit(1)

# Determine the appropriate app data path based on the operating system
if os.name == 'nt':  # Windows
    appdata_path = os.getenv('APPDATA')
    if appdata_path is None:
        raise ValueError("The APPDATA environment variable is not set. Please set it to continue.")
else:  # macOS or Linux
    appdata_path = os.path.expanduser('~/.config')

db_path = os.path.join(appdata_path, 'mvbackdrops', 'processed_folders.db')
api_key_path = os.path.join(appdata_path, 'mvbackdrops', 'apikey.txt')

def get_tmdb_api_key():
    if os.path.exists(api_key_path):
        with open(api_key_path, 'r') as file:
            encoded_key = file.read().strip()
            if encoded_key:
                decoded_key = base64.b64decode(encoded_key).decode('utf-8')
                return decoded_key
    return None

def prompt_for_tmdb_api_key():
    api_key = input("You have not input your TMDB API key. Please provide it now: ").strip()
    if api_key:
        encoded_key = base64.b64encode(api_key.encode('utf-8')).decode('utf-8')
        os.makedirs(os.path.dirname(api_key_path), exist_ok=True)
        with open(api_key_path, 'w') as file:
            file.write(encoded_key)
        return api_key
    else:
        sys.stderr.write("\033[91mTMDB API key is required. Exiting...\n\033[0m")
        sys.exit(1)

def initialize_database():
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS processed_folders (folder TEXT PRIMARY KEY)''')
    conn.commit()
    conn.close()

def is_folder_processed(folder):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT 1 FROM processed_folders WHERE folder = ?', (folder,))
    result = c.fetchone()
    conn.close()
    return result is not None

def mark_folder_as_processed(folder):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO processed_folders (folder) VALUES (?)', (folder,))
    conn.commit()
    conn.close()

TMDB_API_KEY = get_tmdb_api_key()
if not TMDB_API_KEY:
    TMDB_API_KEY = prompt_for_tmdb_api_key()

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
            if is_folder_processed(movie_dir):
                logger.info(f"Folder {movie_dir} already processed. Skipping download.")
                continue
            if os.path.exists(os.path.join(backdrops_folder, 'video1.mp4')) or os.path.exists(os.path.join(backdrops_folder, 'video1.mkv')):
                logger.info(f"Trailer already exists for {dir}. Skipping download.")
                mark_folder_as_processed(movie_dir)
                continue
            original_title = dir
            cleaned_title = clean_movie_title(original_title.replace('_', ' ').replace('.', ' '))
            movie_id = get_movie_id(cleaned_title)
            if movie_id:
                trailer_url = get_trailer_url(movie_id)
                if trailer_url:
                    downloaded_file = download_trailer(trailer_url, backdrops_folder)
                    if downloaded_file:
                        mark_folder_as_processed(movie_dir)

def convert_to_x265(input_file, output_file):
    command = [
        "ffmpeg",
        "-i", input_file,
        "-c:v", "hevc_nvenc",
        "-an",
        output_file
    ]
    subprocess.run(command)

def convert_backdrops(base_dir):
    for root, dirs, files in os.walk(base_dir):
        for dir in dirs:
            if dir.lower() == 'backdrops':
                continue
            backdrops_folder = os.path.join(root, dir, 'backdrops')
            if os.path.exists(backdrops_folder):
                for filename in os.listdir(backdrops_folder):
                    if filename.endswith(".mp4"):  # Adjust as necessary for your specific case
                        input_file = os.path.join(backdrops_folder, filename)
                        output_file = os.path.join(backdrops_folder, f"{os.path.splitext(filename)[0]}.mkv")
                        convert_to_x265(input_file, output_file)
                        os.remove(input_file)

def main():
    print("\033[91m                     __  __                                                 __ \033[0m")
    print("\033[91m                    /  |/  |                                               /  |\033[0m")
    print("\033[91m _______   __    __ $$ |$$ | __    __  __     __  __    __  __    __   ____$$ |\033[0m")
    print("\033[91m/       \ /  \  /  |$$ |$$ |/  \  /  |/  \   /  |/  \  /  |/  \  /  | /    $$ |\033[0m")
    print("\033[91m$$$$$$$  |$$  \/$$/ $$ |$$ |$$  \/$$/ $$  \ /$$/ $$  \/$$/ $$  \/$$/ /$$$$$$$ |\033[0m")
    print("\033[91m$$ |  $$ | $$  $$<  $$ |$$ | $$  $$<   $$  /$$/   $$  $$<   $$  $$<  $$ |  $$ |\033[0m")
    print("\033[91m$$ |  $$ | /$$$$  \ $$ |$$ | /$$$$  \   $$ $$/    /$$$$  \  /$$$$  \ $$ \__$$ |\033[0m")
    print("\033[91m$$ |  $$ |/$$/ $$  |$$ |$$ |/$$/ $$  |   $$$/    /$$/ $$  |/$$/ $$  |$$    $$ |\033[0m")
    print("\033[91m$$/   $$/ $$/   $$/ $$/ $$/ $$/   $$/     $/     $$/   $$/ $$/   $$/  $$$$$$$/\033[0m")

    current_directory = os.path.dirname(os.path.abspath(__file__))
    initialize_database()
    process_movie_directories(current_directory)

    user_input = input("Do you want to convert the backdrops to x265 NVENC MKV with audio removed? (y/n): ").strip().lower()
    if user_input == 'y':
        convert_backdrops(current_directory)
    else:
        print("Skipping conversion script execution")

if __name__ == "__main__":
    main()
