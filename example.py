import os
from dotenv import load_dotenv
from strands import Agent

# Cargar las variables de entorno desde el archivo .env
load_dotenv()
from strands.models.gemini import GeminiModel
from strands_tools import calculator, current_time

custom_model = GeminiModel(
    client_args={
        "api_key": os.getenv("GOOGLE_API_KEY"),
    },
    model_id="gemini-3.1-flash-lite", 
    params={
        "temperature": 0.7,
    }
)

agent = Agent(model=custom_model, tools=[calculator,current_time])

message = """"
I am born in 2003, tell me my age in days.
"""

agent(message)
