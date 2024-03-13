import json
import time
from openai import OpenAI
from thread import Thread

from foodwaste_api import FoodwasteAPI


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
        foodwaste_client: FoodwasteAPI,
        assistant_id: int,
        thread_id: int,
    ):
        self.thread_id = thread_id
        self.client = client
        self.foodwaste_client = foodwaste_client
        self.id = client.beta.threads.runs.create(
            assistant_id=assistant_id,
            thread_id=thread_id,
        ).id

    def __get_run(self):
        return self.client.beta.threads.runs.retrieve(
            thread_id=self.thread_id, run_id=self.id
        )

    def wait_for_run_completion(self):
        retries = 0
        while retries < self.POLL_RETRIES:
            run = self.__get_run()
            if run.status in ["completed", "failed"]:
                self.result = run.status
                return
            elif run.status == "requires_action":
                tool_outputs = self.call_functions(
                    run.required_action.submit_tool_outputs.tool_calls
                )

                run = self.client.beta.threads.runs.submit_tool_outputs(
                    thread_id=self.thread_id, run_id=run.id, tool_outputs=tool_outputs
                )

            retries += 1
            time.sleep(self.POLL_INTERVAL)

        raise Exception("Run retrieval timeout.")

    def call_functions(self, tool_calls):
        tool_outputs = []
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_arguments = json.loads(tool_call.function.arguments)
            func = getattr(self.foodwaste_client, function_name)
            output = func(**function_arguments)
            tool_outputs.append({"tool_call_id": tool_call.id, "output": str(output)})

        return tool_outputs

    def is_run_successful(self):
        return self.result == "completed"
