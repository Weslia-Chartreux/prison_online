import os
import yaml

BOT_TOKEN = os.getenv('BOT_TOKEN')

OPENAI_TOKEN = os.getenv('OPENAI_TOKEN')

with open("src/chat_modes.yml", 'r', encoding='UTF-8') as f:
    chat_modes = yaml.safe_load(f)
