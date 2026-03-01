from urllib.parse import urlparse
import re

def extract_product_name(url: str) -> str:
    try:
        parsed = urlparse(url)
        path = parsed.path

        # Amazon URL patterns:
        # /dp/ASIN  or  /product-name/dp/ASIN  or  /gp/product/ASIN
        # The product name is always the segment BEFORE /dp/ or /gp/product/

        # Try to get the human-readable slug before /dp/
        dp_match = re.search(r'/([^/]+)/dp/', path)
        if dp_match:
            slug = dp_match.group(1)
            # Clean it up
            name = slug.replace("-", " ").strip()
            if name and not name.startswith("B0"):  # Not an ASIN
                return name

        # Fallback: get from query param or title segment
        parts = [p for p in path.split("/") if p and not p.startswith("B0") and p not in ["dp", "gp", "product", "s"]]
        if parts:
            return parts[0].replace("-", " ").strip()

        return "Unknown Product"

    except Exception:
        return "Unknown Product"