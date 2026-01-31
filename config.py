import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FOLDER_PATH = os.path.join(BASE_DIR, 'data')
DB_PATH = os.path.join(DB_FOLDER_PATH, 'oferty.db')

if not os.path.exists(DB_FOLDER_PATH):
    os.makedirs(DB_FOLDER_PATH)

OLX_URL = "https://www.olx.pl/praca/informatyka/poznan/"
PRACA_PL_URL = "https://www.praca.pl/poznan.html?m=Poznań" 
ROCKET_URL = "https://rocketjobs.pl/oferty-pracy/poznan?keyword=it&radius=0"
NOFLUFF_URL = "https://nofluffjobs.com/pl/poznan?criteria=category%3Dsys-administrator,business-analyst,architecture,backend,data,ux,devops,erp,embedded,frontend,fullstack,game-dev,mobile,project-manager,security,support,testing,other"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"

DB_NAME = DB_PATH

ITEMS_PER_PAGE = 20