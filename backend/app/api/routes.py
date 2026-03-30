from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.services.link_parser import extract_product_name
from app.services.reddit_scraper import get_reddit_reviews
from app.services.ai_summarizer import summarize_reviews
from app.services.price_scraper import get_best_prices

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