import json
from datetime import datetime, timedelta

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

PRICE_DIFF = 5
btc_endpoint = "https://api.coingecko.com/api/v3/coins/bitcoin"
last24h = datetime.strftime(datetime.now() - timedelta(1), "%Y%m%dT%H%M")

news_parameters = {
    "function": "NEWS_SENTIMENT",
    "tickers": "CRYPTO:BTC",
    "sortBy": "popularity",
    "apikey": APIkey,
    "time_from": f"{last24h}",
}
news_endpoint = "https://www.alphavantage.co/query"

resp_btc = requests.get(btc_endpoint)
resp_btc.raise_for_status()
btc_change = resp_btc.json()["market_data"]["price_change_percentage_24h"]

if abs(btc_change) >= PRICE_DIFF:
    resp_news = requests.get(news_endpoint, params=news_parameters)
    resp_news.raise_for_status()
    news_data = resp_news.json()["feed"][:3]
    for _ in range(3):
        sentiment_score = f"{news_data[_]['overall_sentiment_label']} | Price change: {btc_change:.2f}%"
        headline = news_data[_]["title"]
        summary = news_data[_]["summary"]
        sms_text = (
            f"Sentiment: {sentiment_score}\nHeadline: {headline}\nSummary: {summary}"
        )

        client = Client(account_sid, auth_token)
        message = client.messages.create(
            from_=twilio_nr,
            body=sms_text,
            to=my_nr,
        )
