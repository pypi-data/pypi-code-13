#!/usr/bin/python
# coding=utf-8


import re
import os
import sys
import tempfile
import subprocess
import hashlib
from gtts import gTTS
from datetime import datetime


while True:
   line = sys.stdin.readline().strip()

   if line == '':
      break
   key, data = line.split(':')
   if key[:4] != 'agi_':
      #skip input that doesn't begin with agi_
      sys.stderr.write("Did not work!\n")
      sys.stderr.flush()
      continue
   key = key.strip()
   data = data.strip()
   if key != '':
      env[key] = data


def _speak_espeak(text):
    base_file_name = tempfile.named_temporary_file().name
    raw_file_name = tempfile.named_temporary_file().name + '-raw.wav'
    subprocess.call(['espeak', text, '-vbrazil-mbrola-4', '-g0.5', '-p60', '-s130', '-w', raw_file_name])
    subprocess.call(['sox', raw_file_name, base_file_name + '.wav', 'rate', '8k'])
    os.remove(raw_file_name)
    return base_file_name


def _speak_gtts(text):
    try:
        text.decode('utf-8')
    except:
        text = text.encode('utf-8')
    digest = '/tmp/' + hashlib.sha224(text).hexdigest()
    file_name = digest + '.mp3'
    if os.path.isfile(file_name):
        return file_name
    raw_file_name = digest + '-raw.mp3'
    tts = gTTS(text=text, lang='pt-br')
    tts.save(raw_file_name)
    subprocess.call(['lame', '--scale', '10', raw_file_name, file_name])
    os.remove(raw_file_name)
    return file_name


def busy(timeout):
    sys.stdout.write("EXEC Busy %s\n %timeout ")
    sys.stdout.flush()
    sys.stderr.write("EXEC Busy %s\n %timeout ")
    sys.stderr.flush()
    line = sys.stdin.readline()
    result = line.strip()
    return int(checkresult(result)) - 48


def checkresult (params):
   sys.stderr.write("checkresult: %s\n" % params)
   params = params.rstrip()
   if re.search('^200', params):
      result = re.search('result=(\d+)', params)
      if (not result):
         sys.stderr.write("FAIL ('%s')\n" % params)
         sys.stderr.flush()
         return -1
      else:
         result = result.group(1)
         sys.stderr.write("PASS (%s)\n" % result)
         sys.stderr.flush()
         return result
   else:
      sys.stderr.write("FAIL (unexpected result '%s')\n" % params)
      sys.stderr.flush()
      return -2


def hangup():
    sys.stdout.write("EXEC Hangup")
    sys.stdout.flush()
    sys.stderr.write("EXEC Hangup")
    sys.stderr.flush()
    line = sys.stdin.readline()
    result = line.strip()
    return int(checkresult(result)) - 48


def read_digit(timeout):
    sys.stdout.write("WAIT FOR DIGIT %s\n" %timeout )
    sys.stdout.flush()
    sys.stderr.write("WAIT FOR DIGIT %s\n" %timeout )
    sys.stderr.flush()
    line = sys.stdin.readline()
    sys.stderr.write('wait_for_digit line: %s\n' % line)
    result = line.strip()
    return int(checkresult(result)) - 48


def record(filepath):
    sys.stdout.write("EXEC MixMonitor " + filepath)
    sys.stdout.flush()
    sys.stderr.write("MixMonitor(wav, " + filepath +", mb)\n")
    sys.stderr.flush()
    line = sys.stdin.readline()
    result = line.strip()
    return int(checkresult(result)) - 48


def speak(text):
    try:
        file_name = _speak_gtts(text)
        sys.stdout.write("EXEC MP3Player %s\n" % file_name)
    except:
        print(sys.exc_info())
        file_name = _speak_espeak(text)
        sys.stdout.write("EXEC PLAYBACK %s\n" % file_name)
    sys.stdout.flush()
    result = sys.stdin.readline().strip()
    return checkresult(result)


def transfer(tech, dest):
    sys.stdout.write("EXEC DIAL %s/%s\n" % (tech,dest))
    sys.stdout.flush()
    result = sys.stdin.readline().strip()
    checkresult(result)
    monitor()


def wait_exten(timeout):
    sys.stdout.write("EXEC WaitExten %s\n %timeout ")
    sys.stdout.flush()
    sys.stderr.write("EXEC WaitExten %s\n %timeout ")
    sys.stderr.flush()
    line = sys.stdin.readline()
    result = line.strip()
    return int(checkresult(result)) - 48


def write_digit(digit, timeout, duration):
    if timeout is None and duration is None:
        sys.stdout.write("EXEC SendDTMF %s\n" % digit )
        sys.stdout.flush()
    elif duration is None:
        sys.stdout.write("EXEC SendDTMF %s/%s\n" % (digit, timeout) )
        sys.stdout.flush()
    elif timeout is None:
        sys.stdout.write("EXEC SendDTMF %s/%s\n" % (digit, duration) )
        sys.stdout.flush()
    else:
        sys.stdout.write("EXEC SendDTMF %s %s %s\n" % (digit, timeout, duration) )
        sys.stdout.flush()
    sys.stderr.write("EXEC SendDTMF %s/%s\n" % (digit, duration))
    sys.stderr.flush()
    line = sys.stdin.readline()
    result = line.strip()
    return int(checkresult(result)) - 48
