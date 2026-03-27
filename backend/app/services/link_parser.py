from urllib.parse import urlparse
import re

# Words that are useless for Reddit search
NOISE_WORDS = [
    "buy", "online", "amazon", "india", "new", "latest", "best", "price",
    "gb", "tb", "mb", "ram", "rom", "storage", "control", "pack", "combo",
    "edition", "version", "series", "model", "variant", "color", "colour",
    "black", "white", "blue", "red", "green", "silver", "gold", "grey", "gray",
    "with", "and", "for", "the", "official"
]

def extract_product_name(url: str) -> str:
    try:
        parsed = urlparse(url)
        path = parsed.path

        dp_match = re.search(r'/([^/]+)/dp/', path)
        if dp_match:
            slug = dp_match.group(1)
            # Split into words and remove noise
            words = slug.replace("-", " ").lower().split()
            cleaned = [w for w in words if w not in NOISE_WORDS and not w.isdigit() and len(w) > 1]
            # Keep only first 4 meaningful words max
            name = " ".join(cleaned[:4])
            if name:
                return name

        parts = [p for p in path.split("/") if p and not p.startswith("B0") and p not in ["dp", "gp", "product", "s"]]
        if parts:
            words = parts[0].replace("-", " ").lower().split()
            cleaned = [w for w in words if w not in NOISE_WORDS and not w.isdigit() and len(w) > 1]
            return " ".join(cleaned[:4])

        return "Unknown Product"

    except Exception:
        return "Unknown Product"