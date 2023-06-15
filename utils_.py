def get_video_id(url):
    import urllib.parse

    url_data = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(url_data.query)
    return query["v"][0]


def utf8_decode(string):
    replacements = [
        ['\u2019', '\''], ['\u2018', '\''], ['\u2026', '...'], ['\u2014', '-'],
        ['\x80', '{euro}'], ['\x81', ''], ['\x82', '\''], ['\x83', 'f'],
        ['\x84', '"'], ['\x85', '...'], ['\x86', '+'], ['\x87', '++'],
        ['\x88', '^'], ['\x89', '{mille}'], ['\x8a', 'S'], ['\x8b', '['],
        ['\x8c', 'OE'], ['\x8d', ''], ['\x8e', 'Z'], ['\x8f', ''],
        ['\x90', ''], ['\x91', '''], ['\x92', '''], ['\x93', '"'],
        ['\x94', '"'], ['\x95', '(.)'], ['\x96', '-'], ['\x97', '--'],
        ['\x98', '~'], ['\x99', '(tm)'], ['\x9a', 'S'], ['\x9b', ']'],
        ['\x9c', 'oe'], ['\x9d', ''], ['\x9e', 'z'], ['\x9f', 'Y'],
        ['\xa0', ''], ['\xa1', '!'], ['\xa2', '{cent}'], ['\xa3', '{pound}'],
        ['\xa4', '{currency}'], ['\xa5', '{yen}'], ['\xa6', '!'],
        ['\xa7', '{section}'], ['\xa8', '-'], ['\xa9', '(c)'], ['\xaa', 'a'],
        ['\xab', '[['], ['\xac', '{not}'], ['\xad', ''], ['\xae', '(R)'],
        ['\xaf', ''], ['\xb0', '{degrees}'], ['\xb1', '{+-}'],
        ['\xb2', '^2'], ['\xb3', '^3'], ['\xb4', '^'], ['\xb5', 'u'],
        ['\xb6', '{p}'], ['\xb7', '.'], ['\xb8', ''], ['\xb9', '^1'],
        ['\xba', 'O'], ['\xbb', ']]'], ['\xbc', '1/4'], ['\xbd', '1/2'],
        ['\xbe', '3/4'], ['\xbf', '?'], ['\xc0', 'A'], ['\xc1', 'A'],
        ['\xc2', 'A'], ['\xc3', 'A'], ['\xc4', 'A'], ['\xc5', 'A'],
        ['\xc6', 'AE'], ['\xc7', 'C'], ['\xc8', 'E'], ['\xc9', 'E'],
        ['\xca', 'E'], ['\xcb', 'E'], ['\xcc', 'I'], ['\xcd', 'I'],
        ['\xce', 'I'], ['\xcf', 'I'], ['\xd0', 'D'], ['\xd1', 'N'],
        ['\xd2', 'O'], ['\xd3', 'O'], ['\xd4', 'O'], ['\xd5', 'O'],
        ['\xd6', 'O'], ['\xd7', 'x'], ['\xd8', 'O'], ['\xd9', 'U'],
        ['\xda', 'U'], ['\xdb', 'U'], ['\xdc', 'U'], ['\xdd', 'Y'],
        ['\xde', 'b'], ['\xdf', 'b'], ['\xe0', 'a'], ['\xe1', 'a'],
        ['\xe2', 'a'], ['\xe3', 'a'], ['\xe4', 'a'], ['\xe5', 'a'],
        ['\xe6', 'ae'], ['\xe7', 'c'], ['\xe8', 'e'], ['\xe9', 'e'],
        ['\xea', 'e'], ['\xeb', 'e'], ['\xec', 'i'], ['\xed', 'i'],
        ['\xee', 'i'], ['\xef', 'i'], ['\xf0', '6'], ['\xf1', 'n'],
        ['\xf2', 'o'], ['\xf3', 'o'], ['\xf4', 'o'], ['\xf5', 'o'],
        ['\xf6', 'o'], ['\xf7', '{divided-by}'], ['\xf8', 'o'],
        ['\xf9', 'u'], ['\xfa', 'u'], ['\xfb', 'u'], ['\xfc', 'u'],
        ['\xfd', 'y'], ['\xfe', 'b'], ['\xff', 'y']
    ]

    str_copy = string
    for charFrom, charTo in replacements:
        str_copy = str_copy.replace(charFrom, charTo)
    return str_copy


def clean_filename(filename):
    import re

    reg_exp = re.compile(r"[\\<>\*\?/\$!\"\:@\+\`\|=]")
    if reg_exp.search(filename):
        print(f"File name contained characters disallowed for filenames. Original filename: {filename}")
    return re.sub(reg_exp, " ", filename)
