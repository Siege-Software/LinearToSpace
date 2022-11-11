import os

from dotenv import load_dotenv

load_dotenv()

jetbrains_key = os.getenv('JETBRAINS_KEY')
jetbrains_endpoint = os.getenv('JETBRAINS_ENDPOINT')
jetbrains_headers = {'Authorization': f'Bearer {jetbrains_key}'}