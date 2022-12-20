from dotenv import load_dotenv
import os

load_dotenv()


HEADERS = {
    # "Connection": 'keep-alive',
    'Authorization': 'Bearer ' + os.getenv('FACEIT_TOKEN'),
    # 'Content-Type': 'application/json'
}

DOMEN = 'https://open.faceit.com/data/v4'

PLAYERS_LIST = 'players.txt'
PLAYERS_FULL_STATISTIC_DIR = 'players_info'
PLAYERS_NEW_STATS_DIR = 'players_new_info'

CHECK_UPDATE_PERIOD = 1  # days
