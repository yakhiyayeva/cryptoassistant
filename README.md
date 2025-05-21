AI Crypto Assistant

This project is a web application that provides information about cryptocurrencies. The application uses the API of GNews  and Binance to obtain data on cryptocurrencies.

Functions

Getting a list of the top 50 cryptocurrencies by market capitalization
Getting the current cryptocurrency price
Obtaining the market capitalization of cryptocurrencies
Getting news about Cryptocurrencies
API

/: Returns the message "Welcome to the AI Crypto Assistant"
/top-coins: Returns a list of the top 50 cryptocurrencies by market capitalization
/price/{coin}: Returns the current price of the cryptocurrency
/marketcap/{coin}: Returns the market capitalization of the cryptocurrency
/news/{coin}: Returns news about cryptocurrencies
Installation

Clone a repository
Install dependencies using pip install -r requirements.txt
Create a file .env with environment variables
Launch the application using uvicorn main:app --reload
Environment variables

GNEWS_API_KEY: The GNews API key


Python 3.8+
FastAPI
requests
dotenv


