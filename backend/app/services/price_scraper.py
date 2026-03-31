import os
import re
from urllib.parse import quote, unquote
from dotenv import load_dotenv
from serpapi import GoogleSearch

load_dotenv()

# ── Trusted Indian stores ─────────────────────────────────────────────────────

TRUSTED_STORES = [
    "amazon", "flipkart", "croma", "reliance digital",
    "vijay sales", "tatacliq", "myntra", "snapdeal",
    "samsung", "apple", "mi store", "oneplus",
    "jiomart", "nykaa", "ajio", "meesho", "shopclues", "boat",
]

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
    "samsung":          "🔷",
    "apple":            "🍎",
    "mi store":         "🟠",
    "oneplus":          "🔴",
    "boat":             "🎧",
    "jiomart":          "🔵",
    "nykaa":            "🩷",
    "ajio":             "👗",
    "shopclues":        "🛍️",
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
    "samsung":          "https://www.samsung.com/in/search/?searchvalue=",
    "apple":            "https://www.apple.com/in/search/",
    "jiomart":          "https://www.jiomart.com/search#q=",
    "nykaa":            "https://www.nykaa.com/search/result/?q=",
    "ajio":             "https://www.ajio.com/search/?text=",
    "shopclues":        "https://www.shopclues.com/search?q=",
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def is_trusted(source: str) -> bool:
    return any(store in source.lower() for store in TRUSTED_STORES)

def get_logo(source: str) -> str:
    for key, logo in STORE_LOGOS.items():
        if key in source.lower():
            return logo
    return "🏷️"

def build_store_search_url(source: str, product_name: str) -> str:
    encoded = quote(product_name)
    for key, base_url in STORE_SEARCH_URLS.items():
        if key in source.lower():
            return base_url + encoded
    return f"https://www.google.com/search?q={quote(product_name + ' ' + source)}"

def extract_direct_url(item: dict, source: str, product_name: str) -> str:
    candidates = []
    for field in ["product_link", "store_link", "link"]:
        val = item.get(field, "")
        if val and isinstance(val, str):
            candidates.append(val)

    for url in candidates:
        if not url or url in ("null", "None", ""):
            continue
        if "serpapi.com" in url:
            continue
        if "/url?q=" in url:
            try:
                extracted = unquote(url.split("/url?q=")[1].split("&")[0])
                if extracted.startswith("http") and "google.com" not in extracted:
                    return extracted
            except:
                continue
        if url.startswith("http") and "google.com" not in url:
            return url

    return build_store_search_url(source, product_name)

def title_matches_product(title: str, product_name: str) -> bool:
    """
    Check if the result title actually matches the product searched.
    Strips common noise words and checks keyword overlap.
    """
    NOISE = {
        "buy", "online", "best", "price", "india", "new", "latest",
        "with", "and", "for", "the", "in", "at", "on", "of", "a",
        "inch", "cm", "gb", "tb", "mb", "ram", "rom", "pack", "combo",
        "review", "sale", "offer", "discount", "deal", "get", "shop",
    }

    def clean_words(text):
        words = re.sub(r'[^a-z0-9\s]', ' ', text.lower()).split()
        return {w for w in words if w not in NOISE and len(w) > 1}

    product_words = clean_words(product_name)
    title_words   = clean_words(title)

    if not product_words:
        return True

    # Count how many product keywords appear in the title
    matches = product_words & title_words
    match_ratio = len(matches) / len(product_words)

    # Need at least 50% of product keywords to appear in title
    return match_ratio >= 0.5

# ── Main ──────────────────────────────────────────────────────────────────────

def get_best_prices(product_name: str) -> list:
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        return []

    try:
        # Use exact product name with "buy india" to get specific results
        search_query = f"{product_name} buy india"

        params = {
            "engine":  "google_shopping",
            "q":       search_query,
            "api_key": api_key,
            "gl":      "in",
            "hl":      "en",
            "num":     "20",
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        shopping_results = results.get("shopping_results", [])

        if not shopping_results:
            return []

        prices      = []
        seen_stores = set()

        for item in shopping_results:
            source = item.get("source", "").strip()
            price  = item.get("extracted_price")
            title  = item.get("title", "")
            thumb  = item.get("thumbnail", "")

            # ── Filters ──────────────────────────────────────────────────────

            # Must have price and source
            if not price or not source:
                continue

            # Must be a trusted store
            if not is_trusted(source):
                continue

            # Must not be a duplicate store
            if source.lower() in seen_stores:
                continue

            # ── KEY FIX: title must actually match the searched product ──────
            if not title_matches_product(title, product_name):
                continue

            # ─────────────────────────────────────────────────────────────────

            seen_stores.add(source.lower())

            direct_url = extract_direct_url(item, source, product_name)

            prices.append({
                "store":         source,
                "title":         title[:70],
                "price":         int(price),
                "price_display": f"₹{int(price):,}",
                "url":           direct_url,
                "logo":          get_logo(source),
                "thumbnail":     thumb,
            })

        prices.sort(key=lambda x: x["price"])

        if prices:
            prices[0]["best"] = True

        return prices[:5]

    except Exception as e:
        return []