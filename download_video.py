# can be more DRY
import os
import traceback

from pytubefix import YouTube
from pytube.exceptions import PytubeError

from utils_ import get_video_id, utf8_decode, progress


def download_video(video_info_and_pref):
    try:
        title = video_info_and_pref.title
        selected_stream = video_info_and_pref.video_stream

        print(f"downloading video at {selected_stream.resolution}: {title} ...")
        print("Pls do not touch the file until completed.")

        # is_progressive = has audio
        if selected_stream.is_progressive:
            selected_stream.download()
        else:
            download_video_audio_separately(video_info_and_pref)

        print(f"{title}.mp4 has been downloaded.")

    except PytubeError as e:
        traceback.print_exc()


# Todo: use parallel process to speed things up
# Todo: add captions, set default resolution, captions lang in txt
def download_playlist_video(playlist_url):
    try:
        import re
        from pytube import Playlist

        playlist = Playlist(playlist_url)
        # fixes empty playlist.videos list
        playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

        playlist_urls = playlist.video_urls
        print(f"Number of videos in playlist: {len(playlist_urls)}")

        for video_url in playlist_urls:
            yt = YouTube(video_url, on_progress_callback=progress)
            title = utf8_decode(yt.title)
            print(f"downloading video (up to 720p): {title} ...")
            print("Pls do not touch the file until completed.")
            # get highest resolution with audio (max 720p)
            yt.streams.get_highest_resolution().download()

    except PytubeError as e:
        traceback.print_exc()


def download_video_audio_separately(video_info_and_pref):
    url = video_info_and_pref.url
    title = video_info_and_pref.title
    selected_stream = video_info_and_pref.video_stream
    audio_stream = video_info_and_pref.audio_stream

    import subprocess

    video_id = get_video_id(url)
    selected_stream.download(
        filename=f"{video_id}-mute.mp4"
    )
    audio_stream.download(
        filename=f"{video_id}.mp3"
    )
    # merge files
    # cannot directly output file with unicode name
    cmd = f"ffmpeg -i {video_id}.mp3 -i {video_id}-mute.mp4 -c copy {video_id}.mp4"
    # std options to silence output
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.rename(f"{video_id}.mp4", f"{title}.mp4")
    # delete separate files
    os.remove(f"{video_id}.mp3")
    os.remove(f"{video_id}-mute.mp4")
