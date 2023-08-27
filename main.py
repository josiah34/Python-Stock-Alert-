import requests
from twilio.rest import Client

STOCK_NAME = ""  # Enter the stock name here
COMPANY_NAME = ""  # Enter the company name here
STOCK_API_KEY = ""  # Enter the stock API key here SEE: https://www.alphavantage.co/documentation/
NEWS_KEY = ""  # Enter the news API key here SEE: https://newsapi.org/
TWILIO_ACCOUNT_SID = ""  # Enter TWILIO_ACCOUNT_SID here SEE: https://www.twilio.com/docs/iam/keys/api-key
TWILIO_API_KEY = ""  # Enter TWILIO API KEY


def get_stock_data():
    # Replace the "demo" API key below with your own key from https://www.alphavantage.co/support/#api-key
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK_NAME}&apikey={STOCK_API_KEY}"
    r = requests.get(url)
    data = r.json()
    return [value for (key, value) in data["Time Series (Daily)"].items()]


def get_yesterday_closing_price(data_list):
    return data_list[0]["4. close"]


def get_day_before_yesterday_closing_price(data_list):
    return data_list[1]["4. close"]


def get_difference_in_percentage(yesterday_closing_price, day_before_yesterday_closing_price):
    abs_diff = abs(
        float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
    )
    percentage_change = (abs_diff / float(yesterday_closing_price)) * 100
    percentage_change = round(percentage_change, 2)

    if float(yesterday_closing_price) > float(day_before_yesterday_closing_price):
        return f"{STOCK_NAME} stock increased by {percentage_change}%"
    elif float(yesterday_closing_price) < float(day_before_yesterday_closing_price):
        return f"{STOCK_NAME} stock decreased by {percentage_change}%"
    else:
        return None


def get_company_articles():
    news_url = f"https://newsapi.org/v2/everything?q={COMPANY_NAME}&apiKey=0a7a418e75e64db499b95356eaceab37"
    r = requests.get(news_url)
    news_data = r.json()
    return news_data["articles"][:3]


def SEND_SMS(sid, TWILIO_API_KEY, articles, message):
    """Send SMS using the Twilio API. Please set 'from_' and 'to' of message body parameter to your Twilio account phone number and your phone number respectively."""  
    three_articles = articles
    formatted_articles = [
        f"Headline: {article['title']}. \nBrief: {article['description']}"
        for article in three_articles
    ]

    # Send Message
    client = Client(sid, TWILIO_API_KEY)
    # Modify the 'body' parameter to change the message sent to your phone using your Twilio account phone number
    message = client.messages.create(
        from_="", body=f"{message}", to=""
    )

    print(message.sid)

    for article in formatted_articles:
        message = client.messages.create(
            body=article, from_="", to=""
        )

    print(message.status)


def main():
    stock_data = get_stock_data()
    yesterdays_closing_price = get_yesterday_closing_price(stock_data)
    print(yesterdays_closing_price)
    day_before_yesterday_closing_price = get_day_before_yesterday_closing_price(
        stock_data
    )
    difference_in_percentage = get_difference_in_percentage(yesterdays_closing_price, day_before_yesterday_closing_price)

    if difference_in_percentage != None:
        articles = get_company_articles()
        SEND_SMS(TWILIO_ACCOUNT_SID, TWILIO_API_KEY, articles, difference_in_percentage)


if __name__ == "__main__":
    main()
