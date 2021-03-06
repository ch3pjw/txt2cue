#!/usr/bin/python3
"""
 Python script to read a simple text file from stdin
 containing the Artist, Album Title, Flac audio file full path
 and track listings, one per line and output to stdout a cue sheet
 in a format suitable for split2flac.

 Input example:
    # This is a comment
    artist=James Taylor
    album=Sweet Baby James
    file=/home/user/Music/James_Taylor/Sweet_Baby_James/test.flac
    Sweet Baby James|00:00:00
    Lo And Behold|02:54:00

 Output from the above:
    PERFORMER "James Taylor"
    TITLE "Sweet Baby James"
    FILE /home/user/Music/James_Taylor/Sweet_Baby_James/test.flac
    TRACK 01 AUDIO
    FLAGS PRE
    TITLE "Sweet Baby James"
    PERFORMER "James Taylor"
    INDEX 01 00:00:00
    TRACK 02 AUDIO
    FLAGS PRE
    TITLE "Lo And Behold"
    PERFORMER "James Taylor"
    INDEX 01 02:54:00
"""
import sys


def process_key_val_pair(line):
    key, value = line.split('=')
    return key.strip(), value.strip()


def parse_input(file_obj):
    output = []
    track = 0
    for line in file_obj.readlines():
        line = line.strip()
        if line.startswith("#"):
            # Ignore comments
            continue
        elif line.startswith("album="):
            _, album = process_key_val_pair(line)
            output.append('TITLE "{}"'.format(album))
        elif line.startswith("artist="):
            _, artist = process_key_val_pair(line)
            output.append('PERFORMER "{}"'.format(artist))
        elif line.startswith("file="):
            _, file_name = process_key_val_pair(line)
            output.append('FILE ' + file_name)
        elif line:
            title, start_time = line.split('|')
            track += 1
            output.append(
                'TRACK {track:02d} AUDIO\n'
                'FLAGS PRE\n'
                'TITLE "{title}"\n'
                'PERFORMER "{artist}"\n'
                'INDEX 01 {start_time}'.format(
                    track=track, title=title, artist=artist,
                    start_time=start_time))
    return '\n'.join(output)

if __name__ == '__main__':
    sys.stdout.write(parse_input(sys.stdin))
