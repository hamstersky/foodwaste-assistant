import openai
import os
from dotenv import load_dotenv
from assistant import Assistant
from thread import Thread
from ui import UI

load_dotenv()


def setup(client, state):
    if "thread" not in state:
        state.thread = Thread(client)

    if "assistant" not in state:
        assistant_id = os.getenv("ASSISTANT_ID")
        state.assistant = Assistant(client, assistant_id)

    if "messages" not in state:
        state.messages = []


def main():
    client = openai.OpenAI()
    ui = UI(client)
    setup(client, ui.state)
    ui.initialize_state()
    ui.render_ui()


if __name__ == "__main__":
    main()
