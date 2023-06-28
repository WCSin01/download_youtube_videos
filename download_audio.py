import os
import traceback

from pytube import YouTube
from pydub import AudioSegment
from pytube.exceptions import PytubeError

from utils_ import utf8_decode, get_video_id, clean_filename


def download_audio(url):
    try:
        yt = YouTube(url)
        title = utf8_decode(yt.title)
        # remove illegal filename char
        title = clean_filename(title)
        video_id = get_video_id(url)

        print(f"downloading audio (128kbps): {title} ...")
        print("Pls do not touch the file until completed.")
        # cannot directly output file with unicode name
        yt.streams.get_by_itag(140).download(filename=f"{video_id}.m4a")
        convert_m4a_to_mp3(title, video_id)
        print(f"{title}.mp3 has been downloaded and converted.")

    except PytubeError as e:
        traceback.print_exc()


def download_playlist_audio(playlist_url):
    import re
    from pytube import Playlist

    playlist = Playlist(playlist_url)
    # fixes empty playlist.videos list
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

    playlist_urls = playlist.video_urls
    print(f"Number of videos in playlist: {len(playlist_urls)}")

    for video_url in playlist:
        download_audio(video_url)


# convert m4a to mp3 so it has ID3 tags
def convert_m4a_to_mp3(title, video_id):
    print(f"converting to mp3...")
    fake_mp3_audio = AudioSegment.from_file(f"{video_id}.m4a", format="m4a")
    fake_mp3_audio.export(f"{title}.mp3", format="mp3")
    os.remove(f"{video_id}.m4a")
