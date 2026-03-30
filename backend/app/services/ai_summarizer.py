import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def get_label(score: int) -> str:
    if score >= 75: return "Very Positive"
    if score >= 55: return "Positive"
    if score >= 40: return "Neutral"
    if score >= 25: return "Negative"
    return "Very Negative"

def extract_score(text: str, fallback: int = 50) -> int:
    try:
        match = re.search(r'\{.*?\}', text, re.DOTALL)
        if match:
            data = json.loads(match.group())
            score = int(data.get("score", fallback))
            return max(0, min(100, score))
    except:
        pass
    # fallback: find any number 0-100 in response
    nums = re.findall(r'\b([0-9]{1,3})\b', text)
    for n in nums:
        n = int(n)
        if 0 <= n <= 100:
            return n
    return fallback

def summarize_reviews(reviews: list, product_name: str = "this product"):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return {
            "ai_opinion": "Groq API key not configured.",
            "reddit_summary": "Groq API key not configured.",
            "sentiment_score": 50,
            "sentiment_label": "Neutral"
        }

    try:
        client = Groq(api_key=api_key)

        # ── Call 1: AI expert opinion ──────────────────────────────────────
        opinion_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{
                "role": "user",
                "content": f"""You are a strict, unbiased product reviewer. Based on your training data, give your honest opinion about "{product_name}".

Cover:
- What kind of product this is
- Who it is best suited for
- Key strengths
- Key weaknesses
- Overall verdict

Be honest. If the product has real flaws, mention them clearly. 4-6 sentences."""
            }]
        )

        # ── Call 2: Reddit community summary ──────────────────────────────
        reddit_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{
                "role": "user",
                "content": f"""Summarize the following Reddit reviews for "{product_name}":

{reviews}

Give:
- Overall sentiment
- Pros
- Cons

Be specific and accurate. Do not generalize."""
            }]
        )

        # ── Call 3: Reddit sentiment score ─────────────────────────────────
        reddit_score_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{
                "role": "user",
                "content": f"""Carefully read these Reddit reviews for "{product_name}":

{reviews}

Count how many reviews are positive, negative, or neutral.
Then give an honest sentiment score from 0 to 100 based ONLY on what these reviews say.

Scoring guide:
- 0-20 = overwhelmingly negative
- 21-40 = mostly negative
- 41-60 = mixed or neutral
- 61-80 = mostly positive
- 81-100 = overwhelmingly positive

DO NOT default to 70. Carefully analyze the actual tone of each review.
Return ONLY this JSON and nothing else:
{{"score": <number between 0 and 100>}}"""
            }]
        )

        # ── Call 4: AI knowledge score ─────────────────────────────────────
        ai_score_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{
                "role": "user",
                "content": f"""Based on your own knowledge about "{product_name}", give it an honest quality score from 0 to 100.

Scoring guide:
- 0-20 = very poor, widely criticized, avoid
- 21-40 = below average, significant issues
- 41-60 = average, mixed reputation
- 61-80 = good, well regarded by most users
- 81-100 = excellent, highly recommended

Be strict and realistic. A budget product should not score the same as a flagship.
DO NOT default to 70. Different products must get different scores.
Return ONLY this JSON and nothing else:
{{"score": <number between 0 and 100>}}"""
            }]
        )

        # ── Parse both scores and average them ────────────────────────────
        reddit_score = extract_score(
            reddit_score_response.choices[0].message.content.strip()
        )
        ai_score = extract_score(
            ai_score_response.choices[0].message.content.strip()
        )

        final_score = round((reddit_score + ai_score) / 2)
        final_label = get_label(final_score)

        return {
            "ai_opinion": opinion_response.choices[0].message.content,
            "reddit_summary": reddit_response.choices[0].message.content,
            "sentiment_score": final_score,
            "sentiment_label": final_label
        }

    except Exception as e:
        return {
            "ai_opinion": f"AI opinion failed: {str(e)}",
            "reddit_summary": f"AI summarization failed: {str(e)}",
            "sentiment_score": 50,
            "sentiment_label": "Neutral"
        }