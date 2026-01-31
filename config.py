import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FOLDER_PATH = os.path.join(BASE_DIR, 'data')
DB_PATH = os.path.join(DB_FOLDER_PATH, 'oferty.db')

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
ROCKET_URL = "https://rocketjobs.pl/oferty-pracy/poznan"

ITEMS_PER_PAGE = 15