https://github.com/user-attachments/assets/f3d083b1-259a-4d49-b420-9fdeb3839773


# **Jellyfin Video Backdrop Downloader**
A Python script in order to automate the downloading and conversion (if you so choose) of backdrops for movies using the TMDB api, Python, ffmpeg and yt-dlp

# LOOKING FOR HELP WITH MAKING A GUI IF YOU KNOW ANYTHING SEND A PULL REQUEST

## REQUIREMENTS
1. Python 3.11
2. ffmpeg (if you plan on using the conversion element)
3. TMDB API Key


### Usage:

Steps:
1. Either clone the repository, download the individual files from this repo, or download the latest release
2. Run ```pip install -r ./requirements.txt``` from within the same directory as your requirements.txt file 
3. Copy the files `mvbackdrops.bat` and `mvbackdrops.py` to the top of whichever movie directory you are looking to download backdrop videos for
4. Run either `mvbackdrops.bat` by double clicking it (You may get a unknown source prompt this is normal just run the batch) or open a command prompt window in the directory where you copied the files and run:

```cmd
py -3.11 ./mvbackdrops.py
```

5. You will be prompted for your TMDB API key, if you have not already provided it, [which you can get here](https://developer.themoviedb.org/v4/reference/intro/authentication) it will be saved in either your appdata folder or config folder, depending on your os, in a file named apikey.txt encoded in Base64

![image](https://github.com/user-attachments/assets/decbe685-6d56-455c-b530-bdffa55238ac)

5. Let the script run and you will be prompted if you want to convert to x265 NVENC MKV with no audio
6. Congrats! (**BE SURE TO GO TO JELLYFIN, GO TO USER SETTINGS AND ENABLE THEME VIDEOS OTHERWISE THIS WON'T SHOW ANYTHING**)
