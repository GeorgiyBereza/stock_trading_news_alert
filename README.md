<h2>Tracking stock prices, collecting news and sending sms</h2>
(project from Python bootcamp)
<br>

This project uses 3 different APIs:
<ol>
  <li>
    Collecting data from https://www.alphavantage.co and tracking stock prices difference for last 2 days
  </li>
    <li>
    If price change is more than 5%:
    gathering top news from https://newsapi.org with a company name in the article's title
  </li>
  <li>
    Sends separate sms with the percentage change and each article's title plus description to your phone number via https://www.twilio.com.
  </li>
</ol>

Message is formatted this way:
<br>
TSLA: 🔺12% or 🔻5%
<br>
Headline: Tesla, Inc. (NASDAQ:TSLA) Q4 2023 Earnings Call Transcript
<br>
Brief: January 24, 2024 Tesla, Inc. isn’t one of the 30 most popular stocks among hedge funds at the end ...
