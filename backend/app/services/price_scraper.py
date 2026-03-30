import os
from urllib.parse import quote
from dotenv import load_dotenv
from serpapi import GoogleSearch

load_dotenv()

STORE_LOGOS = {
    "amazon":           "🛒",
    "flipkart":         "🏪",
    "croma":            "🏬",
    "reliance digital": "🔵",
    "vijay sales":      "🟡",
    "tatacliq":         "🔴",
    "myntra":           "🛍️",
    "meesho":           "🟣",
    "snapdeal":         "💠",
}

STORE_SEARCH_URLS = {
    "amazon":           "https://www.amazon.in/s?k=",
    "flipkart":         "https://www.flipkart.com/search?q=",
    "croma":            "https://www.croma.com/searchB?q=",
    "reliance digital": "https://www.reliancedigital.in/search?q=",
    "vijay sales":      "https://www.vijaysales.com/search/",
    "tatacliq":         "https://www.tatacliq.com/search/?searchCategory=all&text=",
    "myntra":           "https://www.myntra.com/",
    "meesho":           "https://www.meesho.com/search?q=",
    "snapdeal":         "https://www.snapdeal.com/search?keyword=",
}

def get_logo(source: str) -> str:
    for key, logo in STORE_LOGOS.items():
        if key in source.lower():
            return logo
    return "🏷️"

def build_fallback_url(source: str, product_name: str) -> str:
    """Build a direct search URL for a known store."""
    encoded = quote(product_name)
    for key, url in STORE_SEARCH_URLS.items():
        if key in source.lower():
            return url + encoded
    # Unknown store — search Google for it
    return f"https://www.google.com/search?q={quote(product_name + ' ' + source)}"

def clean_url(url: str, source: str, product_name: str) -> str:
    """
    SerpAPI returns Google redirect URLs like:
    /url?q=https://amazon.in/...
    or https://www.google.com/shopping/...
    
    Extract the actual destination URL.
    """
    if not url:
        return build_fallback_url(source, product_name)

    # Already a direct store URL
    if url.startswith("http") and "google.com" not in url:
        return url

    # Google redirect: /url?q=https://...
    if "/url?q=" in url:
        try:
            actual = url.split("/url?q=")[1].split("&")[0]
            if actual.startswith("http"):
                return actual
        except:
            pass

    # Relative URL or google.com URL — use fallback
    return build_fallback_url(source, product_name)


def get_best_prices(product_name: str) -> list:
    api_key = os.getenv("SERPAPI_KEY")

    if not api_key:
        return []

    try:
        params = {
            "engine": "google_shopping",
            "q": product_name,
            "api_key": api_key,
            "gl": "in",
            "hl": "en",
            "num": "20",
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        shopping_results = results.get("shopping_results", [])

        if not shopping_results:
            return []

        prices = []
        seen_stores = set()

        for item in shopping_results:
            source = item.get("source", "").strip()
            price  = item.get("extracted_price")
            title  = item.get("title", product_name)
            thumb  = item.get("thumbnail", "")

            if not price or not source:
                continue
            if source.lower() in seen_stores:
                continue

            seen_stores.add(source.lower())

            # Try all possible URL fields SerpAPI provides
            raw_url = (
                item.get("product_link") or   # direct product page (best)
                item.get("store_link") or      # store page
                item.get("link") or            # generic link (often Google redirect)
                ""
            )

            direct_url = clean_url(raw_url, source, product_name)

            prices.append({
                "store":         source,
                "title":         title[:70],
                "price":         int(price),
                "price_display": f"₹{int(price):,}",
                "url":           direct_url,
                "logo":          get_logo(source),
                "thumbnail":     thumb,
            })

        # Sort cheapest first
        prices.sort(key=lambda x: x["price"])

        # Mark best price
        if prices:
            prices[0]["best"] = True

        return prices[:5]

    except Exception as e:
        return []