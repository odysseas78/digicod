from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'