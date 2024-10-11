# Real Estate Scraper Project

This project is a web scraping tool designed to extract real estate community and home data from multiple websites using Python. The scraper supports asynchronous processing via APIs, with the scraping process triggered asynchronously. It uses Flask and Blueprint for creating a REST API layer, and Selenium WebDriver for interacting with web pages.

## Table of Contents
- [Real Estate Scraper Project](#real-estate-scraper-project)
  - [Table of Contents](#table-of-contents)
  - [Technologies Used](#technologies-used)
  - [Setup](#setup)
  - [Configuration](#configuration)
  - [API Endpoints](#api-endpoints)
    - [POST `/api/scrape/start`](#post-apiscrapestart)
  - [Running the Scraper](#running-the-scraper)


## Technologies Used
- **Python 3.12.x**
- **Selenium** for web scraping.
- **Flask** for REST API creation.
- **Blueprint** for modular API routes.
- **dotenv** for loading configuration from `.env` files.
- **Logging** for maintaining logs in a configurable manner.

## Setup

1. **Clone the Repository**
    ```bash
    git clone https://github.com/your-repo/real_estate_scraper.git
    cd real_estate_scraper
    ```

2. **Create a Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate 
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Create the .env File**
    Copy the provided `.env.example` file to create your `.env` file:
    ```bash
    cp .env.example .env
    ```

5. **Configure the .env File**
    In the `.env` file, set the required environment variables:
    ```bash
    CHROMEDRIVER_PATH=/path/to/chromedriver
    LOGGING_LEVEL=DEBUG  # Options: DEBUG, INFO, WARNING, ERROR
    LOGGING_FORMAT=basic  # Options: basic, detailed
    ```

## Configuration

- **ChromeDriver Path**: Set the path to your ChromeDriver in the `.env` file.
- **Logging**: You can configure logging to either output to stdout or a log file. You can also set the log level and format via the `.env` file.

## API Endpoints

### POST `/api/scrape/start`
Triggers the scraping process asynchronously.

**Request**:  
```json
{
  "scraper": "lennar",
  "url": "https://www.lennar.com/new-homes/north-carolina/raleigh",
  "search": "city_name or zip-code"
}
```

## Running the Scraper
1. **Run the scraper directly from cli**
    ```bash
    python main.py <vendor_name>   #vendor_name example drhorton, lennar
    ```

2. **Run via Flask API server**
   ```bash
    python app.py # start the flask application
   ```
3. **Trigger a scrape request via API You can trigger the scraping using Postman** or `curl`
   
    ```bash
    curl -X POST http://127.0.0.1:5000/api/scrape/start \
    -H "Content-Type: application/json" \
    -d '{"scraper": "lennar", "url": "https://www.lennar.com/new-homes/north-carolina/raleigh/knightdale/stoneriver", "search": "raleigh"}'
    
    ```