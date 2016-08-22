import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'generated')
MAX_SOUND_LIFE = 60*60*12   # seconds of sound file storing

INSTALLED_APPS = [
    'rest_framework_swagger',
    'rest_framework',
    'django_speach_synthesizer',
]