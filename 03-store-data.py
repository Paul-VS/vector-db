"""
Store page URLS from a file into the primary key table on Supabase then store every section from each page into another table on Supabase.
Each page section will have the page URL as a foreign key.
"""

import json
import logging
import os
import supabase
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env.

# Initialize the Supabase client
client = supabase.create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

# Set up logging
logging.basicConfig(level=logging.INFO)

def main():
    # Load the input data
    logging.info("Loading input data...")
    with open("embeddings.json", "r") as file:
        data = json.load(file)

    for url, sections in data.items():
        # Insert data into the page table
        logging.info(f"Inserting page: {url}")
        page_response, count = client.table("page").insert({
            "path": url,
            "checksum": "12345",  # Update this with a real checksum
            "meta": {"key": "value"}  # Update this with real meta data
        }).execute()

        if page_response:
            logging.info(f"Inserted page: {url}") 
      
            for section in sections:
                # Insert data into the page_section table
                logging.info(f"Inserting page section: {section['string'][:20]}...")
                section_response, count = client.table("page_section").insert({                    
                    "page_id": url,
                    "content": section["string"],
                    "token_count": section["prompt_tokens"],
                    "embedding": section["embedding"]
                }).execute()

                if section_response:
                    logging.info(f"Inserted page section: {section['string'][:20]}...")
                else:
                    logging.error("Failed to insert page section.")
        else:
            logging.error("Failed to insert page.")

if __name__ == "__main__":
    main()
