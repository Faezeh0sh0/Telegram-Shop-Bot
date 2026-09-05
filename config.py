import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))