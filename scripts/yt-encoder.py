#!/usr/bin/env python3
from pytube import Playlist
import subprocess
import os
import glob
import eyed3
import re
import argparse


def fold_name(album):
    return "".join([i.replace(" ", "-") for i in album]) 


def download_videos(url, album):
    videos = []
    path = fold_name(album)
    os.mkdir(path)
    for i,v in enumerate(Playlist(url).videos):
        v.streams.get_by_itag('140').download(path)
        videos.append((v.title, i+1))
    return videos


def convert_to_mp3(videos, album):
    for v in videos:
        mp4 = f"{fold_name(album)}/{v[0]}.mp4"
        mp3 = f"{fold_name(album)}/{v[0]}.mp3"
        subprocess.call(["ffmpeg", "-i", mp4, mp3])
        os.remove(mp4)


def encode_files(artist, album, files):
    for f in files:
        song = eyed3.load(f"{fold_name(album)}/{f[0]}.mp3").tag
        song.artist = artist
        song.album = album
        song.title = f[0]
        song.track_num = f[1]
        song.save()
    
        
def main(artist, album, url):
    videos = download_videos(url, album)
    convert_to_mp3(videos, album)
    encode_files(artist, album, videos)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Download YT playlists.')
    parser.add_argument('artist', type=str, help='Artist name.')
    parser.add_argument('album', type=str, help='Album name.')
    parser.add_argument('url', type=str, help='URL')
    args = parser.parse_args()
    main(args.artist, args.album, args.url)
