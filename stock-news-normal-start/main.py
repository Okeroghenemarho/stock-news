import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

api_key = "8FM60DKCUKSUCL9F"
parameter = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": api_key
}
response = requests.get(url=STOCK_ENDPOINT, params=parameter)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key,value) in data.items()]
yesterday_closing_price = float(data_list[0]["4. close"])
previous_day_closing_price = float(data_list[1]["4. close"])
stock_difference = abs(yesterday_closing_price-previous_day_closing_price)
percentage_difference = round((stock_difference/yesterday_closing_price)*100)

if percentage_difference >= 1:

    news_api = "ff0c58d58bea419d9c938b207d3adeb8"
    news_params = {
        "qInTitle": COMPANY_NAME,
        "apiKey": news_api,
    }
    news_request = requests.get(url=NEWS_ENDPOINT, params=news_params)
    news = news_request.json()
    articles = news["articles"]
    first_3_articles = articles[:3]
    news_articles = [(article['title'],article['description']) for article in first_3_articles]

    for newss in news_articles:
        account_sid = 'ACf66c19eed938f4ad366955daaef7cca5'
        auth_token = '0a2783b22ae92a2d75f121e36c963c12'
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=f"{STOCK_NAME}: 🔺{percentage_difference}%\nHeadline:{newss[0]}\nBrief:{newss[1]}",
            from_='+18643127487',
            to='+2349026324907'
        )
