from __future__ import unicode_literals
import youtube_dl, os, subprocess

def download(url):
    path='D:/DC++Share/Songs/pyDirect'
    os.chdir(path)
    options = {
        'format': 'bestaudio/best', # choice of quality
        'extractaudio' : True,      # only keep the audio
        'audioformat' : "mp3",      # convert to mp3
        'outtmpl' : '%(title)s.%(ext)s',
        'noplaylist' : True,        # only download single song, not playlist
    }
    ydl = youtube_dl.YoutubeDL(options)
    with ydl:
        ydl.download([url])
    print ("Download Finished. Keep smiling. :-)")
    return None

if __name__=="__main__":
    url = raw_input("Input song's url - ")
    download(url)
