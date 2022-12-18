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

