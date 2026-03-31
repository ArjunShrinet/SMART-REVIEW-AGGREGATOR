from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.services.link_parser import extract_product_name
from app.services.reddit_scraper import get_reddit_reviews
from app.services.ai_summarizer import summarize_reviews
from app.services.price_scraper import get_best_prices
import os
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

class ProductRequest(BaseModel):
    product_url: str
    is_name: Optional[bool] = False

class PriceRequest(BaseModel):
    product_name: str

@router.post("/analyze")
def analyze_product(request: ProductRequest):
    if request.is_name:
        product_name = request.product_url.strip()
    else:
        product_name = extract_product_name(request.product_url)

    reviews = get_reddit_reviews(product_name)
    review_texts = [r["text"] for r in reviews]
    summary = summarize_reviews(review_texts, product_name)

    return {
        "product": product_name,
        "reviews": reviews,
        "ai_opinion": summary["ai_opinion"],
        "reddit_summary": summary["reddit_summary"],
        "sentiment_score": summary["sentiment_score"],
        "sentiment_label": summary["sentiment_label"]
    }

@router.post("/prices")
def get_prices(request: PriceRequest):
    prices = get_best_prices(request.product_name)
    return {
        "product": request.product_name,
        "prices": prices
    }

@router.post("/debug-prices")
def debug_prices(request: PriceRequest):
    """
    Temporary debug endpoint — shows raw SerpAPI response
    so we can see exactly what URL fields are returned.
    Visit: POST http://127.0.0.1:8000/debug-prices
    """
    api_key = os.getenv("SERPAPI_KEY")
    params = {
        "engine": "google_shopping",
        "q": request.product_name,
        "api_key": api_key,
        "gl": "in",
        "hl": "en",
        "num": "5",
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    shopping = results.get("shopping_results", [])

    # Return first 3 raw items so we can inspect all fields
    return {
        "raw_items": [
            {k: v for k, v in item.items()}
            for item in shopping[:3]
        ]
    }