import time
from openai import OpenAI
from thread import Thread


class Run:
    POLL_INTERVAL = 5
    POLL_RETRIES = 20

    id: int
    thread_id: int
    client: OpenAI
    result: str

    def __init__(
        self,
        client: OpenAI,
        assistant_id: int,
        thread_id: int,
    ):
        self.thread_id = thread_id
        self.client = client
        self.id = client.beta.threads.runs.create(
            assistant_id=assistant_id,
            thread_id=thread_id,
        ).id

    def __get_run_status(self):
        return self.client.beta.threads.runs.retrieve(
            thread_id=self.thread_id, run_id=self.id
        ).status

    def wait_for_run_completion(self):
        retries = 0
        while retries < self.POLL_RETRIES:
            if (status := self.__get_run_status()) in ["completed", "failed"]:
                self.result = status
                return

            retries += 1
            time.sleep(self.POLL_INTERVAL)

        raise Exception("Run retrieval timeout.")

    def is_run_successful(self):
        return self.result == "completed"
