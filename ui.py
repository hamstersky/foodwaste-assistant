import streamlit as st
import time
from assistant import Assistant
from openai import OpenAI
from thread import Thread
from run import Run


class UI:
    client: OpenAI
    assistant: Assistant
    thread: Thread

    def __init__(self, client: OpenAI):
        self.client = client
        self.state = st.session_state

    def initialize_state(self):
        self.messages = st.session_state.messages
        self.assistant = st.session_state.assistant
        self.thread = st.session_state.thread

    def __render_message(self, role: str, content: str):
        with st.chat_message(role):
            container = st.empty()
            if role == "assistant":
                container.write_stream(self.__simulate_stream(content))
            container.markdown(content)

    def __render_messages(self):
        for message in self.messages:
            self.__render_message(message["role"], message["content"])

    def __simulate_stream(self, text: str):
        for word in text.split():
            for letter in word.split():
                yield letter + " "
                time.sleep(0.02)

    def __get_prompt(self):
        if prompt := st.chat_input():
            self.__render_message("user", prompt)
            self.messages.append({"role": "user", "content": prompt})

            message_id = self.thread.add_message(prompt)

            run = None
            with st.spinner("Generating response..."):
                run = Run(self.client, self.assistant.id, self.thread.id)
                run.wait_for_run_completion()

            for response in self.thread.get_assistant_messages(before=message_id):
                self.__render_message("assistant", response)
                self.messages.append({"role": "assistant", "content": response})

            if not run.is_run_successful():
                st.error(
                    "Something went wrong with processing your request. Please try again.",
                    icon="🤖",
                )

    def render_ui(self):
        self.__render_messages()
        self.__get_prompt()
