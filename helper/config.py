from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)
model_env = os.getenv('GPT_MODEL')
log_file_path = '../log.csv'
instruction_path = '../instructions.json'
