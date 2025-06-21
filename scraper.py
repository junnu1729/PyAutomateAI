import requests
from bs4 import BeautifulSoup
import pandas as pd
res = requests.get('https://quotes.toscrape.com')
soup = BeautifulSoup(res.text, "html.parser")
quotes = [q.text for q in soup.find_all("span", class_="text")]
df = pd.DataFrame(quotes, columns=["Quotes"])
print(df.head())