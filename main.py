import openai
import os
from dotenv import load_dotenv
from assistant import Assistant

load_dotenv()


def main():
    client = openai.OpenAI()
    assistant_id = os.getenv("ASSISTANT_ID")
    assistant = Assistant(client, assistant_id)


if __name__ == "__main__":
    main()
