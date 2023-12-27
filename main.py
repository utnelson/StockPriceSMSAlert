from twilio.rest import Client
import yfinance as yf
import requests
import os

pair = "TSLA"
data = yf.Ticker(pair)
hist = data.history(period="5d")

def calculate_diff(value1, value2):
    diff_abs = round(value1 - value2, 2)
    diff_rel = round(value1 / value2, 2)
    if diff_abs >= 0:
        symbol = "+"
    else:
        symbol = "-"
    print(f"Yesterday Close: ${value1} | Yesterday-1d Close: ${value2}")
    print(f"Difference abs: ${symbol}{diff_abs}")
    print(f"Difference rel: {symbol}{diff_rel}%")
    return [diff_abs, diff_rel]


print("=======================Stock Info=================================")
# Get Last 2 days values
yesterday_close = round(hist.iloc[-2]["Close"], 2)
dt_yesterday = hist.iloc[-2].name.date()
before_yesterday_close = round(hist.iloc[-3]["Close"], 2)
dt_before_yesterday = hist.iloc[-3].name.date()

diff = calculate_diff(yesterday_close, before_yesterday_close)

print("=======================News Info==================================")
#NewsAPI. https://newsapi.org/
APIKEY = os.environ['news_api']
url = ('https://newsapi.org/v2/top-headlines?'
       'q=Tesla&'
       'apiKey=' + APIKEY)

response = requests.get(url).json()
news_source_name = response["articles"][0]["source"]["name"]
news_title = response["articles"][0]["title"]
news_text = response["articles"][0]["description"]
news_url = response["articles"][0]["url"]
news = (f"{news_source_name} \n"
        f"{news_title} \n"
        f"{news_text}\n"
        f"{news_url}")
print(news)

print("=======================SMS========================================")
account_sid = os.environ['account_sid']
auth_token = os.environ['auth_token']
twilio_from = os.environ['twilio_from']
twilio_to = os.environ['twilio_to']
client = Client(account_sid, auth_token)

text = (f"〽️Tesla Price change: 🔺 {diff[1]}%: \n") + news

message = client.messages.create(from_=twilio_from,
                                 body=text,
                                 to=twilio_to
                                 )
print(message.sid)
