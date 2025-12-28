import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_FOLDER_NAME = 'data'
DB_FILE_NAME = 'oferty.db'
DB_PATH = os.path.join(BASE_DIR, DB_FOLDER_NAME, DB_FILE_NAME)

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

OLX_URL = "https://www.olx.pl/praca/poznan/"
PRACA_PL_URL = "https://www.praca.pl/poznan.html"
ROCKET_URL = "https://rocketjobs.pl/oferty-pracy/poznan"