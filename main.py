import json
import requests
from twilio.rest import Client

# import private data
with open("priv.json") as f:
    priv = json.load(f)
    APIkey = priv["APIkey"]
    account_sid = priv["account_sid"]
    auth_token = priv["auth_token"]
    twilio_nr = priv["twilio_nr"]
    my_nr = priv["my_nr"]


btc_endpoint = "https://api.coingecko.com/api/v3/coins/bitcoin"

news_parameters = {
    "function": "NEWS_SENTIMENT",
    "tickers": "CRYPTO:BTC",
    "sortBy": "popularity",
    "apikey": APIkey,
    "time_from": "20231201T0000"
}
news_endpoint = "https://www.alphavantage.co/query?"

resp_btc = requests.get(btc_endpoint)
resp_btc.raise_for_status()
btc_data = resp_btc.json()["market_data"]["price_change_percentage_24h"]
print(btc_data)

resp_news = requests.get(news_endpoint, params=news_parameters)
resp_news.raise_for_status()
news = resp_news.json()
print(news)