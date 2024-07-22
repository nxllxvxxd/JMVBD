# **Jellyfin Backdrop Downloader**
A collection of Python scripts in order to automate the downloading and conversion (if you so choose) of backdrops for movies using the TMDB api, Python, ffmpeg and yt-dlp

## REQUIREMENTS
1. Python 3.11
2. ffmpeg (if you plan on using the conversion element)
3. yt-dlp python
4. requests python
5. TMDB


### REQUIREMENTS INSTALL
Run these prior to running the scripts

```cmd
pip install yt-dlp
```

```cmd
pip install requests
```

### Usage:

Steps:
1. Either clone the repository or download the individual files from this repo
2. Edit backdrops.py inputting your own TMDB API key [which you can get here](https://developer.themoviedb.org/v4/reference/intro/authentication)
3. Depending on preference either delete backdropsmkv.py and edit backdrops.bat to remove it (that python script converts all the files to x265 NVENC MKV with no audio) or keep if you want that
4. Drop the files at the head of your movie directory
5. Run backdrops.bat
6. And congratulations! (Note you will need to have backdrops enabled under general settings in the admin dashboard as well as enabling theme videos in general settings under your user preferences)
