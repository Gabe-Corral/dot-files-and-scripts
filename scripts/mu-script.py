import argparse
import os
import glob
import eyed3
import vlc
import time


def sort_songs(path):
    songs = {}
    for file in glob.glob(f'{path}*.mp3'):
        song = eyed3.load(file)
        songs[song.tag.track_num[0]] = [
        file, song.tag.title, song.info.time_secs
        ]
    return sorted(songs.values())


def set_x_root(title, sec, tot_time):
    song_length = time.gmtime(tot_time)
    song_length = time.strftime("%M:%S", song_length)
    new_time = sec
    if sec >= 60:
        new_time = time.gmtime(new_time)
        new_time = time.strftime("%M:%S", new_time)
    os.system(f'xsetroot -name " {title} {new_time}/{song_length} "')


def play(path, title, tot_time, vol):
    media = vlc.MediaPlayer(path)
    media.audio_set_volume(vol)
    media.play()
    playing = 0
    while playing < int(tot_time):
        set_x_root(title, playing, tot_time)
        playing += 1
        time.sleep(1)
    media.stop()


def main(path, vol=10):
    try:
        if not path.endswith(".mp3"):
            songs = sort_songs(path)
            for song in songs:
                play(song[0], song[1], song[2], vol)
        else:
            song = eyed3.load(path)
            play(path, song.tag.title, song.info.time_secs, vol)
    finally:    
        os.system("xsetroot -name ' Fuck off! '")


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Play muisc.')
    parser.add_argument('path', type=str, help='Path to music file or folder.')
    parser.add_argument('vol', type=int, help='Music volume.')
    args = parser.parse_args()
    main(args.path, args.vol)
