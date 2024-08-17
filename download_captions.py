import traceback

from pytube.exceptions import PytubeError

from utils_ import clean_filename


def download_captions(video_info_and_pref):
    try:
        if not video_info_and_pref.selected_caption_objs:
            return
        for caption_obj in video_info_and_pref.selected_caption_objs:
            # ignore deprecated warning
            captions = caption_obj.generate_srt_captions()
            f = open(f"{clean_filename(video_info_and_pref.title)} - {caption_obj.code}.srt", "w")
            f.write(captions)
            f.close()

    except PytubeError as e:
        traceback.print_exc()
