# vector-db README

## Overview
This repository contains three Python scripts that together create a pipeline for:

1. Fetching markdown files from a specified GitHub repository and splitting them into sections at each heading.
2. Retrieving embeddings for each section from the OpenAI API.
3. Storing the page URLs and their corresponding sections into tables on Supabase.

Each script is designed to be run independently and to pass data to the next script via JSON files.

## Scripts

1. `01-github-scraper.py`: Fetches markdown files from a GitHub repository, splits them into sections at each heading, and stores the results in a JSON file.

2. `02-get-embeddings.py`: Retrieves embeddings for each section of the markdown files from the OpenAI API and stores them in a JSON file.

3. `03-store-data.py`: Stores page URLs and their corresponding sections into tables on Supabase. Each page section will have the page URL as a foreign key.

## Setup

### Requirements

Python 3.6+ is required. All required Python packages can be installed via pip:

```
pip install -r requirements.txt
```

### Environment Variables

These scripts use environment variables to store sensitive information. Please create a `.env` file at the root of the repository and add the following variables:

```
GITHUB_TOKEN=<your_github_token>
OPENAI_API_KEY=<your_openai_api_key>
SUPABASE_URL=<your_supabase_url>
SUPABASE_KEY=<your_supabase_key>
```

Replace `<your_github_token>`, `<your_openai_api_key>`, `<your_supabase_url>`, and `<your_supabase_key>` with your actual GitHub token, OpenAI API key, Supabase URL, and Supabase key, respectively.

## Usage

After setting up the environment variables, you can run the scripts in the following order:

1. Run `01-github-scraper.py` to fetch markdown files from the GitHub repository and split them into sections. The results are stored in `output.json`.

```sh
python 01-github-scraper.py
```

2. Run `02-get-embeddings.py` to retrieve embeddings for each section of the markdown files from the OpenAI API. The results are stored in `embeddings.json`.

```sh
python 02-get-embeddings.py
```

3. Run `03-store-data.py` to store the page URLs and their corresponding sections into tables on Supabase.

```sh
python 03-store-data.py
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

MIT

## Contact

Feel free to reach out for any issues or concerns. Happy coding!
