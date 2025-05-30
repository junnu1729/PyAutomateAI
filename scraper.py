import requests
from bs4 import BeautifulSoup

def scrape_website():
    url = "https://quotes.toscrape.com/"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract all quotes inside <span class="text">
        quotes = [quote.get_text(strip=True) for quote in soup.find_all('span', class_='text')]
        return quotes

    except Exception as e:
        print("Scraping failed:", e)
        return []

# Run scraper directly
if __name__ == "__main__":
    quotes = scrape_website()
    if quotes:
        print("✅ Quotes scraped successfully:\n")
        for i, quote in enumerate(quotes, 1):
            print(f"{i}. {quote}")
    else:
        print("❌ No quotes found or scraping failed.")
