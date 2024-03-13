import streamlit as st
import time
from assistant import Assistant
from openai import OpenAI
from foodwaste_api import FoodwasteAPI, Store
from thread import Thread
from run import Run


class UI:
    openai_client: OpenAI
    assistant: Assistant
    thread: Thread

    def __init__(self, open_api: OpenAI, foodwaste_client: FoodwasteAPI):
        self.openai_client = open_api
        self.foodwaste_client = foodwaste_client
        self.state = st.session_state

    def initialize_state(self):
        self.messages = st.session_state.messages
        self.assistant = st.session_state.assistant
        self.thread = st.session_state.thread

    def __render_message(self, role: str, content: str, stream: bool = True):
        with st.chat_message(role):
            container = st.empty()
            if role == "assistant" and stream:
                container.write_stream(self.__simulate_stream(content))
            container.markdown(content)

    def __render_messages(self):
        for message in self.messages:
            self.__render_message(message["role"], message["content"], stream=False)

    def __simulate_stream(self, text: str):
        for word in text.split():
            for letter in word.split():
                yield letter + " "
                time.sleep(0.02)

    def __get_store_zipcode(self):
        with st.form(key="zipcode"):
            zipcode = st.text_input(
                "Write the zip code where you want to find a store:"
            )
            submitted = st.form_submit_button(label="Submit")

            if submitted:
                st.session_state.zip = zipcode
                st.rerun()

    def __render_store_picker(self):
        stores = self.foodwaste_client.get_stores(st.session_state.zip)
        options = list(map(lambda store: store.id, stores))
        stores_by_id = {store.id: store for store in stores}
        format_func = (
            lambda store_id: f"{stores_by_id[store_id].name}, {stores_by_id[store_id].address}"
        )
        selection = st.selectbox(
            label="Select a specific store:", options=options, format_func=format_func
        )
        if selection:
            st.session_state.store_id = selection

    def __get_prompt(self):
        if prompt := st.chat_input():
            self.__render_message("user", prompt)
            self.messages.append({"role": "user", "content": prompt})

            message_id = self.thread.add_message(prompt)
            self.__create_run()
            self.__render_responses(message_id)

    def __create_run(self):
        run = None
        with st.spinner("Generating response..."):
            run = Run(
                self.openai_client,
                self.foodwaste_client,
                self.assistant.id,
                self.thread.id,
            )
            run.wait_for_run_completion()

        if not run.is_run_successful():
            st.error(
                "Something went wrong with processing your request. Please try again.",
                icon="🤖",
            )

    def __render_responses(self, message_id):
        for response in self.thread.get_assistant_messages(before=message_id):
            self.__render_message("assistant", response)
            self.messages.append({"role": "assistant", "content": response})

    def __initialize_chat(self):
        initial_instructions = f"Give me some recipe suggestions based on today's offers. The store_id is {st.session_state.store_id}"

        message_id = self.thread.add_message(initial_instructions)
        self.__create_run()
        self.__render_responses(message_id)
        st.session_state.session_started = True
        self.__get_prompt()

    def render_ui(self):
        if "zip" not in st.session_state:
            self.__get_store_zipcode()
        elif "store_id" not in st.session_state:
            self.__render_store_picker()
        elif "session_started" not in st.session_state:
            self.__initialize_chat()
        else:
            self.__render_messages()
            self.__get_prompt()
