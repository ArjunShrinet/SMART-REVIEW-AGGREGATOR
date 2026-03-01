from fastapi import APIRouter
from pydantic import BaseModel
from app.services.link_parser import extract_product_name
from app.services.reddit_scraper import get_reddit_reviews
from app.services.ai_summarizer import summarize_reviews

router = APIRouter()

class ProductRequest(BaseModel):
    product_url: str

@router.post("/analyze")
def analyze_product(request: ProductRequest):
    product_name = extract_product_name(request.product_url)
    reviews = get_reddit_reviews(product_name)
    review_texts = [r["text"] for r in reviews]
    summary = summarize_reviews(review_texts)

    return {
        "product": product_name,
        "reviews": reviews,
        "summary": summary
    }