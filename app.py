from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

COUNTRIES = {
    "France": "https://www.zara.com/fr",
    "Spain": "https://www.zara.com/es",
    "USA": "https://www.zara.com/us",
    "UAE": "https://www.zara.com/ae",
    "Saudi Arabia": "https://www.zara.com/sa",
    "Japan": "https://www.zara.com/jp",
    "UK": "https://www.zara.com/uk",
    "Germany": "https://www.zara.com/de"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def search_zara(country_url, item_name):
    try:
        search_url = f"{country_url}/en/search?searchTerm={item_name.replace(' ', '%20')}"
        r = requests.get(search_url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        product = soup.select_one('a._item')
        if not product:
            return None
        price = soup.select_one('span._price')
        return price.text.strip() if price else "Price not found"
    except Exception as e:
        return None

@app.route('/api/scrape')
def scrape():
    item = request.args.get("query", "")
    if not item:
        return jsonify({"error": "Missing item name"}), 400

    results = {}
    for country, url in COUNTRIES.items():
        price = search_zara(url, item)
        results[country] = price or "Not found"

    return jsonify({item: results})

if __name__ == '__main__':
     import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
