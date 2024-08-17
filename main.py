import os
import subprocess
from get_inputs import get_initial_inputs, get_caption_info_and_pref
from download_captions import download_captions


def main():
    try:
        subprocess.run('ffmpeg -h', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        print("ffmpeg not installed")
        exit(1)

    inputs = get_initial_inputs()
    os.chdir(inputs.dest_dir)

    # TODO: parallel video & captions download
    # to limit max length of playlist
    if "playlist?list=" in inputs.url:
        if inputs.media_type == "mp3":
            from download_audio import download_playlist_audio
            download_playlist_audio(inputs.url)
        elif inputs.media_type == "mp4":
            from download_video import download_playlist_video
            download_playlist_video(inputs.url)
    else:
        if inputs.media_type == "mp3":
            from download_audio import download_audio
            download_audio(inputs.url)
        elif inputs.media_type == "mp3":
            from get_inputs import get_video_info_and_pref
            from download_video import download_video
            video_info_and_pref = get_video_info_and_pref(inputs.url)
            download_video(video_info_and_pref)
            download_captions(video_info_and_pref)
        elif inputs.media_type == "cc":
            caption_info_and_pref = get_caption_info_and_pref(inputs.url)
            download_captions(caption_info_and_pref)


if __name__ == '__main__':
    main()
