from pytube import Playlist
import subprocess
import os
import glob
import eyed3
import re

class YTEcoder:
    def __init__(self, url):
        self.download_dir = '/home/gabe/Downloads/Frailty/'
        self.playlist = Playlist(url)
        self.videos = self.playlist.videos
        self.playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
        self.artist = "dltzk"
        self.album = "Frailty"

    def download_files(self):
        for video in self.videos:
            audioStream = video.streams.get_by_itag('140')
            audioStream.download(output_path=self.download_dir)

    def show_titles(self):
        return {i+1: v.title for i,v in enumerate(self.videos)}

    def convert_mp3(self):
        for file in self.show_titles().values():
            file = f"{self.download_dir}{file}"
            print(f'{file}.mp4')
            subprocess.call(['ffmpeg', '-i', f'{file}.mp4',
                            f'{file}.mp3'])

    def remove_mp4_files(self):
        for file in glob.glob(self.download_dir+"*.mp4"):
            os.remove(file)

    def encode_files(self):
        for k,v in self.show_titles().items():
            file = f"{self.download_dir}{v}.mp3"
            song = eyed3.load(file).tag
            song.artist = self.artist
            song.album = self.album
            song.track_num = k
            song.title = v
            song.save()

    def main(self):
        self.download_files()
        #self.encode_files()
        #self.convert_mp3()
        #self.remove_mp4_files()

if __name__=='__main__':
    yt = YTEcoder("https://www.youtube.com/watch?v=CVEkYvkJN5A&list=PLGOxRA_tU285lBasd5KCnnrUDsE7jWnYB")
    yt.main()
