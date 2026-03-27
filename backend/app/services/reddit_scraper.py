import requests
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv()

def get_reddit_reviews(product_name: str) -> list:
    try:
        headers = {"User-Agent": "smart-review-aggregator/1.0"}

        # Search exactly like a user would type in Reddit search
        query = quote(f"{product_name} review")
        url = f"https://www.reddit.com/search.json?q={query}&sort=relevance&limit=15&t=all&type=link"

        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()

        posts = data["data"]["children"]
        reviews = []

        product_keywords = product_name.lower().split()

        for post in posts:
            p = post["data"]

            title = p.get("title", "").lower()

            # Skip posts where title shares NO keywords with product name
            match_count = sum(1 for word in product_keywords if word in title)
            if match_count == 0:
                continue

            text = p.get("selftext", "").strip()
            if not text or text in ("[removed]", "[deleted]"):
                text = p.get("title", "")
            if len(text) < 20:
                text = p.get("title", "")
            if len(text) < 20:
                continue

            reviews.append({
                "text": text[:300],
                "url": f"https://reddit.com{p['permalink']}",
                "subreddit": p["subreddit"],
                "author": p.get("author", "deleted")
            })

        return reviews[:5] if reviews else _fallback(product_name)

    except Exception as e:
        return _fallback(product_name)


def _fallback(product_name: str) -> list:
    return [{
        "text": f"Could not fetch Reddit reviews for {product_name}.",
        "url": "https://reddit.com",
        "subreddit": "unknown",
        "author": "system"
    }]