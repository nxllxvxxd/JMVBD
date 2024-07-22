![2024-07-21 22 11 14,998](https://github.com/user-attachments/assets/5c68d2e7-1d36-4d0d-bb7c-ff0e892a3039)

# **Jellyfin Video Backdrop Downloader**
A Python script in order to automate the downloading and conversion (if you so choose) of backdrops for movies using the TMDB api, Python, ffmpeg and yt-dlp

# LOOKING FOR HELP WITH MAKING A GUI IF YOU KNOW ANYTHING SEND A PULL REQUEST

## REQUIREMENTS
1. Python 3.11
2. ffmpeg (if you plan on using the conversion element)
3. yt-dlp python
4. requests python
5. TMDB API Key


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
2. Copy the files `backdrops.bat` and `backdrops.py` to the top of whichever movie directory you are looking to download backdrop videos for
3. Run either `backdrops.bat` by double clicking it (You may get a unknown source prompt this is normal just run the batch) or open a command prompt window in the directory where you copied the files and run:
```cmd
py -3.11 ./backdrops.py
```
4. You will be prompted for you TMDB API key [which you can get here](https://developer.themoviedb.org/v4/reference/intro/authentication) it will be saved next to the python script in a file named apikey.txt encoded in Base64 (be sure to copy this alongside the python script so you don't have to keep re-entering it)

![image](https://github.com/user-attachments/assets/decbe685-6d56-455c-b530-bdffa55238ac)

5. Let the script run and you will be prompted if you want to convert to x265 NVENC MKV with no audio
6. Congrats! (**BE SURE TO GO TO JELLYFIN, GO TO USER SETTINGS AND ENABLE THEME VIDEOS OTHERWISE THIS WON'T SHOW ANYTHING**)
