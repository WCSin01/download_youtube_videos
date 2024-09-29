import os
import traceback
from collections import namedtuple
from pytubefix import YouTube, Stream, CaptionQuery, Caption
from pytube.exceptions import PytubeError

from utils_ import utf8_decode, clean_filename


class VideoInfoAndPreference:
    # python does not set to undefined
    def __init__(
            self,
            url: str,
            title: str,
            video_stream: Stream | None,
            audio_stream: Stream | None,
            selected_caption_objs=None):
        self.url = url
        self.title = title
        self.video_stream = video_stream
        self.audio_stream = audio_stream
        self.selected_caption_objs = selected_caption_objs


def get_initial_inputs():
    inputs = namedtuple("inputs", ["url", "media_type", "dest_dir"])
    if os.path.exists("default_settings.txt"):
        f = open("default_settings.txt", "r")
        url = input("URL: ")
        dest_dir, media_type = f.read().splitlines()
        return inputs(url, media_type, dest_dir)
    else:
        url = input("URL: ")
        dest_dir = get_dest_dir()
        media_type = get_media_type_input()
    return inputs(url, media_type, dest_dir)


def get_media_type_input():
    while True:
        media_type = input("MP3 or MP4 or cc: ").lower()
        if media_type == "mp3" or media_type == "mp4" or media_type == "cc":
            return media_type
        else:
            print("Invalid file type specified.")


def get_dest_dir():
    import os

    while True:
        dest_dir = input("Directory to save (Leave empty to save to Downloads): ") \
                   or os.path.join(os.environ['USERPROFILE'], "Downloads")
        if os.path.isdir(dest_dir):
            return dest_dir
        else:
            print(
                "Directory does not exist. Please create directory first or try another directory.")


def get_video_info_and_pref(url):
    try:
        yt = YouTube(url, "WEB_CREATOR")
        title = utf8_decode(yt.title)
        title = clean_filename(title)
        streams = yt.streams

        filtered_streams = filter_streams_by_resolution(streams)
        print_resolutions(filtered_streams)
        selected_stream = get_selected_resolution(filtered_streams)
        # pass audio_stream whether needed. Could be optimised.
        audio_stream = streams.get_by_itag(140)
        selected_caption_objs = None

        if should_get_captions():
            captions_obj_list = yt.captions
            print_caption_langs(captions_obj_list)
            selected_caption_objs = get_selected_caption_objs(captions_obj_list)

        return VideoInfoAndPreference(url, title, selected_stream, audio_stream, selected_caption_objs)

    except PytubeError as e:
        traceback.print_exc()


# similar to get_video_info_and_pref. refactor.
def get_caption_info_and_pref(url):
    try:
        yt = YouTube(url, "WEB_CREATOR")
        title = utf8_decode(yt.title)
        title = clean_filename(title)

        captions_obj_list = yt.captions
        print_caption_langs(captions_obj_list)
        selected_caption_objs = get_selected_caption_objs(captions_obj_list)

        return VideoInfoAndPreference(url, title, None, None, selected_caption_objs)

    except PytubeError as e:
        traceback.print_exc()


def filter_streams_by_resolution(streams: YouTube.streams) -> list[Stream]:
    # Todo: add more resolutions
    filtered_streams = [
        streams.get_by_itag(18),
        streams.get_by_itag(22),
        streams.get_by_itag(135),
        streams.get_by_itag(137),
        streams.get_by_itag(271)
    ]
    # remove None
    filtered_streams = [stream for stream in filtered_streams if stream]
    return filtered_streams


def print_resolutions(streams: list[Stream]):
    print("Available resolutions: ")
    for stream in streams:
        print(f"  {stream.resolution}")


def get_selected_resolution(filtered_streams: list[Stream]) -> Stream | None:
    while True:
        selected_resolution_input = input("Resolution: ").lower()
        selected_resolution: list = [
            stream
            for stream in filtered_streams
            if stream.resolution == selected_resolution_input
        ]
        if len(selected_resolution) == 1:
            return selected_resolution[0]
        else:
            print("Invalid resolution specified.")


def should_get_captions():
    should_get_captions_input = input("Get captions? (y/N): ")
    if should_get_captions_input and should_get_captions_input.lower() == "y":
        return True
    return False


def print_caption_langs(captions_obj_list):
    if not len(captions_obj_list):
        print("No captions found.")
        exit(0)
    for captions_obj in captions_obj_list:
        code = captions_obj.code
        lang = captions_obj.name
        print(f"{code}: {lang}")


def get_selected_caption_objs(captions_obj_list: CaptionQuery) -> list[Caption] | None:
    import re

    while True:
        selected_langs_input = \
            input("Language code (if more than 1, separate with comma e.g. en, zh-Hans): ").lower()
        selected_langs: list = re.split(", |,", selected_langs_input)

        filtered_captions_objs = []
        for selected_lang in selected_langs:
            filtered_captions_objs.append(captions_obj_list[selected_lang])
        # remove None
        filtered_captions_objs = [captions_obj for captions_obj in filtered_captions_objs if captions_obj]

        if len(filtered_captions_objs):
            return filtered_captions_objs
        else:
            print("Invalid resolution specified.")
