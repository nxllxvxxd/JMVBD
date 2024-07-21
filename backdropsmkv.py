import os
import logging
import sys
import subprocess

if sys.version_info[:2] != (3, 11):
    sys.stderr.write("This script requires Python 3.11\n")
    sys.exit(1)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def convert_video_to_x265(input_file):
    output_file = input_file.replace('.mp4', '.mkv')
    command = [
        'ffmpeg',
        '-y',
        '-i', input_file,
        '-c:v', 'hevc_nvenc',
        '-an',
        output_file
    ]
    try:
        logger.info(f"Running command: {' '.join(command)}")
        subprocess.run(command, check=True)
        if os.path.exists(output_file):
            os.remove(input_file)
            logger.info(f"Converted video to {output_file} using x265 NVENC and removed audio")
        else:
            logger.error(f"Conversion failed, output file not found: {output_file}")
        return output_file
    except subprocess.CalledProcessError as e:
        logger.error(f"Error converting video: {e}")
    return None

def process_movie_directories(base_dir):
    for root, dirs, files in os.walk(base_dir):
        for dir in dirs:
            if dir.lower() == 'backdrops':
                video_file = os.path.join(root, dir, 'video1.mp4')
                if os.path.exists(video_file):
                    convert_video_to_x265(video_file)

if __name__ == "__main__":
    try:
        subprocess.run(['ffmpeg', '-version'], check=True)
        logger.info("ffmpeg is installed and available")
    except subprocess.CalledProcessError as e:
        logger.error("ffmpeg is not installed or not available in PATH")
        sys.exit(1)

    current_directory = os.path.dirname(os.path.abspath(__file__))
    process_movie_directories(current_directory)
