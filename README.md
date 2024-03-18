# Food waste cooking assistant

This project is a simple prototype chatbot application integrating OpenAI's Assistant API. The project aims to explore ways to reduce food waste by utilizing current food offers from local stores, fetched through an external API, and generating recipes that use these products.

## Features

- Retrieve Offers: Automatically fetches current food offers from local stores.
- Recipe Generation: Utilizes GPT to generate recipes using the products that are currently on offer.
- User Interface: Utilizes Streamlit for a straightforward and user-friendly interface.

## Installation

Follow these steps to set up the application:

1. Clone the repository:

```bash
git clone https://github.com/hamstersky/foodwaste-assistant.git
cd foodwaste-assistant
```

2. Install necessary dependencies:

```bash
pip install -r requirements.txt
```

3. Set up API keys for the stores API and OpenAI's Assistant API in a .env file in the root directory:

```
OPENAI_API_KEY=<Your-API-Key>
SALLING_GROUP_API_TOKEN=<Your-API-Key>
```

After the first run it is recommended adding the ID of the created assistant to avoid creating one on every run:

```
ASSISTANT_ID=<Your-Assistant-ID>
```

## Usage

Run the application with the following command:

```bash
streamlit run main.py
```

Open the provided URL in your browser to interact with the chatbot and find recipes based on local offers.

## Limitations

It turns out that GPT is not very good at generating sensible recipes in general but that ability is even inferior when it has to pick from a list of ingredients. When asked to provide sources for the recipes, GPT hallucinates links to pages that don't exist.
