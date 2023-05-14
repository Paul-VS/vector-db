"""
This script retrieves text embeddings from OpenAI API for a given set of documents and stores the embeddings along with the text in a new JSON file.
"""

import json
import os
import openai
import logging
from ratelimiter import RateLimiter
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()  # Load environment variables from .env.

openai.api_key = os.getenv("OPENAI_API_KEY")

# Validate API key
if not openai.api_key:
    logging.error("Missing OpenAI API key. Please set it as an environment variable.")
    raise ValueError("Missing OpenAI API key. Please set it as an environment variable.")

RATE_LIMIT = 3000  # requests per minute

# Create a rate limiter
rate_limiter = RateLimiter(max_calls=RATE_LIMIT, period=60)

def get_embedding(text):
    """
    This function retrieves the text embedding for the given text using the OpenAI API.
    It also rate limits the API calls to the specified limit.

    Args:
    text (str): The text to retrieve the embedding for.

    Returns:
    list, int: The embedding vector as a list of floats, and the number of prompt tokens.
    """
    with rate_limiter:
        try:
            response = openai.Embedding.create(
                model="text-embedding-ada-002",
                input=text
            )
            return response['data'][0]['embedding'], response['usage']['prompt_tokens']
        except openai.Error as e:
            logging.error(f"Failed to get embeddings: {e}")
            return None, None

def main():
    """
    Main function. Loads the input data, retrieves the embeddings for each text, and stores the results in a new JSON file.
    """
    try:
        # Load the input data
        with open("output.json", "r") as file:
            data = json.load(file)
    except IOError:
        logging.error("Failed to open input file.")
        return

    output = {}

    for url, strings in data.items():
        logging.info(f"Processing URL: {url}")
        output[url] = []
        for string in strings:
            logging.info(f"Getting embedding for string: {string[:20]}...")  # Log first 50 characters
            embedding, prompt_tokens = get_embedding(string)
            if embedding is not None and prompt_tokens is not None:
                output[url].append({
                    "string": string,
                    "embedding": embedding,
                    "prompt_tokens": prompt_tokens
                })

    try:
        # Save the output data
        with open("embeddings.json", "w") as file:
            json.dump(output, file)
    except IOError:
        logging.error("Failed to write output file.")

if __name__ == "__main__":
    main()


