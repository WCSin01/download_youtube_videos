## Purpose
Download YouTube mp3, mp4 and captions. Including playlists.

## Requirements
1. python
2. ffmpeg

## Install ffmpeg for Windows

1. Download & install a program that can decompress `.7z` (e.g. 7Zip, WinRAR)
2. Download latest ffmpeg to `C:/` (https://www.wikihow.com/Install-FFmpeg-on-Windows)
    1. https://ffmpeg.org/download.html
    2. Windows logo
    3. `Windows builds from gyan.dev`
    4. git section > `ffmpeg-git-full.7z`
    5. Right click > Extract here
    6. Rename folder as `ffmpeg`
3. Verify dependencies are installed
    1. enter `python --version` in cmd or powershell. If `is not recognized as an internal command` occurs, python has not been properly installed.
    2. enter `pip --version`
4. Run `setup.bat`

## Install ffmpeg for Linux Debian

```
sudo apt install ffmpeg
```

## Run

```
python main.py
```

## Configuration

You can create `default_settings.txt`:

```
filepath
"mp3" or "mp4"
```

E.g.

```
C:\Music
mp3
```