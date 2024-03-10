from openai import NotFoundError, OpenAI
from typing import Optional


class Thread:
    id: int
    client: OpenAI

    def __init__(self, client: OpenAI, thread_id: Optional[str] = None):
        self.client = client
        if thread_id == None:
            self.__create_new_thread()
        else:
            try:
                client.beta.threads.retrieve(thread_id)
            except NotFoundError:
                print("Thread with the given ID doesn't exist.")

            self.id = thread_id

    def __create_new_thread(self):
        thread = self.client.beta.threads.create()
        self.id = thread.id

    def __extract_messages_contents(self, messages: list[str]) -> list[str]:
        return [content.text.value for msg in messages for content in msg.content]

    def get_messages(self, before: Optional[str] = None):
        return self.client.beta.threads.messages.list(thread_id=self.id, before=before)

    def get_assistant_messages(self, before: Optional[str] = None):
        messages = self.get_messages(before)

        assistant_messages = list(
            filter(
                lambda msg: msg.role == "assistant",
                messages.data,
            )
        )

        return self.__extract_messages_contents(assistant_messages)

    def add_message(self, content: str):
        message = self.client.beta.threads.messages.create(
            thread_id=self.id, role="user", content=content
        )
        return message.id
