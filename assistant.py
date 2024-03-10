import json
from typing import Optional
from openai import NotFoundError, OpenAI


class Assistant:
    id: int

    def __init__(self, client: OpenAI, assistant_id: Optional[str] = None):
        if assistant_id == None:
            self.__create_new_assistant(client)
        else:
            try:
                client.beta.assistants.retrieve(assistant_id)
            except NotFoundError:
                print("Assitant with the given ID doesn't exist.")

            self.id = assistant_id

    def __create_new_assistant(self, client):
        assistant_config = self.__load_assistant_config()
        assistant = client.beta.assistants.create(**assistant_config)
        self.id = assistant.id

    def __load_assistant_config(self):
        with open("assistant.json") as file:
            return json.load(file)
