from datetime import datetime, timedelta
import requests
import os
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
API_KEY_ALPHAVANTAGE = os.environ['ALPHAVANTAGE_API_KEY']
API_KEY_NEWS = os.environ['NEWSAPI_API+KEY']
TWILO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
client = Client(TWILO_ACCOUNT_SID, TWILO_AUTH_TOKEN)
FROM_NUMBER = "insert from number here"
TO_NUMBER = "insert to number here"

# Collecting data from https://www.alphavantage.co and tracking value difference for last 2 days
url = (f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK}&apikey={API_KEY_ALPHAVANTAGE}'
       f'&outputsize=compact')
response = requests.get(url=url)
response.raise_for_status()
print(response.status_code)
data = response.json()

last_day = datetime.strptime(data["Meta Data"]["3. Last Refreshed"],"%Y-%m-%d").date()
if last_day.weekday() == 0:
    # stockmarket is closed on weekend
    day_before = last_day - timedelta(days=3)
else:
    day_before = last_day - timedelta(days=1)

current_price = float(data["Time Series (Daily)"][str(last_day)]["4. close"])
print(f"{last_day} : {current_price}")
old_price = float(data["Time Series (Daily)"][str(day_before)]["4. close"])
print(f"{day_before} : {old_price}")

delta = abs(current_price - old_price)
delta_percent = round(100 * delta / old_price)
sign = ""
if current_price > old_price:
    delta = (100 * (1 - old_price / current_price))
    sign = "🔺"
    print(f"{STOCK}: {sign}{delta_percent}%")
else:
    sign = "🔻"
    delta = (100 * (old_price / current_price - 1))
    print(f"{STOCK}: {sign}{delta_percent}%")

def send_news():
    # Collects top news from https://newsapi.org with a company name in the article's title
    news_endpoint = "https://newsapi.org/v2/everything"
    news_params = {
        "apiKey": API_KEY_NEWS,
        "q": COMPANY_NAME,
        "searchIn": "title",
        "from": str(day_before),
        "to": str(last_day),
        "sortBy": "popularity",
        "pageSize": 3
    }

    news = requests.get(news_endpoint, params=news_params)
    news.raise_for_status()
    print(news.status_code)
    print(news.json())
    news_articles = news.json()["articles"]
    print(news_articles)

    formatted_articles = [
        (f"{STOCK}: {sign}{delta_percent}%\nHeadline: "
         f"{article['title']}. \nBrief: {article['description']}") for article in news_articles]

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=FROM_NUMBER,
            to=TO_NUMBER
        )

# When STOCK price increase/decreases by 5% sends separate sms
# with the percentage change and each article's title and description
# to your phone number via https://www.twilio.com.
if delta_percent >= 5:
    send_news()


