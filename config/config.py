import os
from dotenv import load_dotenv

# 根据需要加载相应的 .env 文件
env_file = os.getenv('ENV_FILE', '.env.dev')
load_dotenv(env_file)

class Config:
    BASE_URL = os.getenv('BASE_URL', 'https://d.huehubtest.xyz')
    API_TOKEN = os.getenv('API_TOKEN', 'default_api_token')
    WS_URL = os.getenv('WS_URL', 'wss://default-websocket-endpoint.com')
