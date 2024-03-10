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
