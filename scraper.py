import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_website():
    res = requests.get('https://quotes.toscrape.com')
    soup = BeautifulSoup(res.text, "html.parser")
    print(soup.prettify())  
    quotes = [q.text for q in soup.find_all("span", class_="text")]
    df = pd.DataFrame(quotes, columns=["Quotes"])
    return df

df = scrape_website()
print(df.head())
