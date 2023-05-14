import httpx
import asyncio
from lxml import etree
import logging
import re
import html2text

# obtain urls with a command like this:
# curl -s "https://kit.svelte.dev/docs/introduction" | grep -o 'href="[^"]*"' | grep -o '/docs/[^"]*' | awk -v domain="https://kit.svelte.dev" '{print domain $0}' 

# Set up logging configuration
logging.basicConfig(filename='web-scraper.log', level=logging.INFO, filemode='w')

# Function to fetch the HTML content of a given URL
async def fetch_page_content(url):
    try:
        async with httpx.AsyncClient(timeout=10.0, limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)) as client:
            r = await client.get(url)
            return r.text
    except Exception as e:
        logging.error(f"Error fetching {url}: {e}")


# Function to parse the HTML content and extract the page text
def parse_html(content, url):
    try:
        # Remove encoding declaration
        content = re.sub(r'<\?xml.*\?>', '', content)
        
        html = etree.HTML(content)
        divs = html.xpath('//div[starts-with(@class, "text content")]')

        if not divs:
            logging.warning(f"No divs found on {url}")
            return

        # Create a html2text.HTML2Text object
        h = html2text.HTML2Text()

        # For each matching div, extract all the text
        markdowns = []
        for div in divs:
            # Convert the HTML within the div to Markdown
            markdown = h.handle(etree.tostring(div, pretty_print=True, encoding='unicode'))
            markdowns.append(markdown)

        return ' '.join(markdowns)
    except Exception as e:
        logging.error(f"Error parsing HTML from {url}: {e}")



# Main function to loop through the list of page URLs, fetch and parse their content,
# extract the content, and write it to a file
async def main():
    # URLs of the pages to include in the .txt file
    with open('urls.txt', 'r') as f:
        page_urls = f.read().splitlines()

    # Initialize a string to store the content
    docs_text = ''

    # Loop through the list of page URLs
    for i, url in enumerate(page_urls):
        # Log the current page being processed
        logging.info(f"Processing page {i+1}: {url}")

        # Fetch the HTML content of the page
        content = await fetch_page_content(url)

        # If the content could not be fetched, continue to the next page
        if not content:
            continue

        # Parse the HTML content and extract the maincol div
        paragraphs = parse_html(content, url)

        # If the page container could not be found, continue to the next page
        if not paragraphs:
            continue

        # Append the content to the string storing all content
        docs_text += paragraphs

        print(f'Successfully parsed page {i+1}')

        # Sleep for politeness
        await asyncio.sleep(0.5)

    # Write the content to a file
    try:
        with open('web-scraper-results.txt', 'w', encoding='utf-8') as f:
            f.write(docs_text)
            logging.info(f"Successfully wrote {len(page_urls)} pages to file.")
    except OSError as e:
        logging.error(f"Error writing to file: {e}")
    
    print("Script execution completed successfully.")

if __name__ == '__main__':
    asyncio.run(main())
