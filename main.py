from fastapi import FastAPI, HTTPException
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# === API KEYS ===
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")

# === HEADERS ===
HEADERS = {"Accepts": "application/json"}

# === SYMBOL MAP for Binance ===
SYMBOL_MAP = {
    "solana": "SOLUSDT",
    "bitcoin": "BTCUSDT",
    "ethereum": "ETHUSDT",
    "dogecoin": "DOGEUSDT",
    "cardano": "ADAUSDT",
    "ripple": "XRPUSDT",
    "polkadot": "DOTUSDT",
    "chainlink": "LINKUSDT",
    "litecoin": "LTCUSDT",
    "avalanche": "AVAXUSDT",
    "tron": "TRXUSDT",
}


# === ROUTES ===

@app.get("/")
def home():
    return {"message": "Welcome to the AI Crypto Assistant"}


@app.get("/top-coins")
def get_top_50_coins():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 50,
        "page": 1
    }
    res = requests.get(url, headers=HEADERS, params=params)
    if res.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch top coins from CoinGecko")
    return res.json()


@app.get("/price/{coin}")
def get_price(coin: str):
    coin = coin.lower()
    if coin not in SYMBOL_MAP:
        raise HTTPException(status_code=404, detail="Coin not supported or not mapped to Binance")

    symbol = SYMBOL_MAP[coin]
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    res = requests.get(url)
    if res.status_code != 200:
        raise HTTPException(status_code=404, detail="Symbol not found on Binance")
    data = res.json()
    return {
        "coin": coin.capitalize(),
        "price": data["price"]
    }


@app.get("/marketcap/{coin}")
def get_market_cap(coin: str):
    url = f"https://api.coingecko.com/api/v3/coins/{coin.lower()}"
    res = requests.get(url)
    if res.status_code != 200:
        raise HTTPException(status_code=404, detail="Coin not found on CoinGecko")
    data = res.json()
    return {
        "coin": coin.capitalize(),
        "price": data["market_data"]["current_price"]["usd"],
        "market_cap": data["market_data"]["market_cap"]["usd"],
        "rank": data["market_cap_rank"]
    }


@app.get("/news/{coin}")
def get_news(coin: str):
    url = f"https://gnews.io/api/v4/search"
    params = {
        "q": coin,
        "token": GNEWS_API_KEY,
        "lang": "en",
        "max": 5
    }
    res = requests.get(url, params=params)

    print("GNews API status:", res.status_code)
    print("GNews API response:", res.text)  # <-- DEBUG INFO

    if res.status_code != 200:
        raise HTTPException(status_code=500, detail="GNews API failed")

    data = res.json()
    return {
        "coin": coin.capitalize(),
        "articles": [{"title": a["title"], "url": a["url"]} for a in data["articles"]]
    }

