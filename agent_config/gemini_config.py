from json import load
from agents import OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env.dev",override=True)

gemini_api_key = os.getenv("GEMINI_API_KEY")
gemini_base_url = os.getenv("GEMINI_BASE_URL")
gemini_ai_model = os.getenv("GEMINI_MODEL")



external_client = AsyncOpenAI(api_key=gemini_api_key,base_url=gemini_base_url)

Model = OpenAIChatCompletionsModel(openai_client=external_client,model=gemini_ai_model)


