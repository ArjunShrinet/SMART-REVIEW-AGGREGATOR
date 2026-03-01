import requests
from dotenv import load_dotenv

load_dotenv()

def get_reddit_reviews(product_name: str) -> list:
    try:
        headers = {"User-Agent": "smart-review-aggregator/1.0"}

        url = f"https://www.reddit.com/search.json?q={product_name}+review&sort=relevance&limit=10&t=year"

        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()

        posts = data["data"]["children"]
        reviews = []

        for post in posts:
            p = post["data"]
            text = p.get("selftext", "").strip()
            if not text or text == "[removed]" or text == "[deleted]":
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