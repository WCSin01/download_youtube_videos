def xml_caption_to_srt(self, xml_captions: str) -> str:
    """Convert xml caption tracks to "SubRip Subtitle (srt)".

    :param str xml_captions:
        XML formatted caption tracks.
    """
    segments = []
    root = ElementTree.fromstring(xml_captions)[0]
    i = 0
    for child in list(root):
        if child.tag == 'p':
            caption = child.text
            caption = unescape(caption.replace("\n", " ").replace("  ", " "), )
            try:
                duration = float(child.attrib["d"]) / 1000.0
            except KeyError:
                duration = 0.0
            start = float(child.attrib["t"]) / 1000.0
            end = start + duration
            sequence_number = i + 1  # convert from 0-indexed to 1.
            line = "{seq}\n{start} --> {end}\n{text}\n".format(
                seq=sequence_number,
                start=self.float_to_srt_time_format(start),
                end=self.float_to_srt_time_format(end),
                text=caption,
            )
            segments.append(line)
            i += 1
    return "\n".join(segments).strip()