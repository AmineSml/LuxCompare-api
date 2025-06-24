from fastapi import FastAPI, Query
from playwright.async_api import async_playwright
import uvicorn
import os

app = FastAPI()

ZARA_DOMAINS = {
    "France": "https://www.zara.com/fr/",
    "UK": "https://www.zara.com/uk/",
    "Italy": "https://www.zara.com/it/",
    "Portugal": "https://www.zara.com/pt/",
    "UAE": "https://www.zara.com/ae/",
    "Saudi Arabia": "https://www.zara.com/sa/"
}

@app.get("/compare-prices")
async def compare_prices(item: str = Query(...)):
    results = {}
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        for country, url in ZARA_DOMAINS.items():
            try:
                page = await browser.new_page()
                await page.goto(url)
                await page.fill("input[type='search']", item)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(4000)

                price = await page.text_content("span.price._product-price")
                results[country] = price.strip() if price else "Not found"
            except Exception as e:
                results[country] = f"Error: {str(e)}"
        await browser.close()
    return results

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run(app, host="0.0.0.0", port=port)
