import openai
import os
from dotenv import load_dotenv
from assistant import Assistant
from foodwaste_api import FoodwasteAPI
from thread import Thread
from ui import UI

load_dotenv()


def setup(openai_client, state):
    if "thread" not in state:
        state.thread = Thread(openai_client)

    if "assistant" not in state:
        assistant_id = os.getenv("ASSISTANT_ID")
        state.assistant = Assistant(openai_client, assistant_id)

    if "messages" not in state:
        state.messages = []


def main():
    openai_client = openai.OpenAI()
    foodwaste_client = FoodwasteAPI(os.getenv("SALLING_GROUP_API_TOKEN"))
    ui = UI(openai_client, foodwaste_client)
    setup(openai_client, ui.state)
    ui.initialize_state()
    ui.render_ui()


if __name__ == "__main__":
    main()
