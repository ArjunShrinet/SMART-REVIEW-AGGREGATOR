import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

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

        # Call 1 — AI's own opinion
        opinion_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{
                "role": "user",
                "content": f"""You are a knowledgeable product expert. Based on your training data, give your own honest opinion about "{product_name}".

Cover:
- What kind of product is this
- Who is it best suited for
- Key strengths
- Key weaknesses
- Overall verdict

Keep it concise, 4-6 sentences. Speak confidently as an expert."""
            }]
        )

        # Call 2 — Reddit summary
        reddit_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{
                "role": "user",
                "content": f"""Summarize the following Reddit reviews for "{product_name}":

{reviews}

Give:
- Overall sentiment
- Pros
- Cons"""
            }]
        )

        # Call 3 — Sentiment score
        score_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{
                "role": "user",
                "content": f"""Based on these Reddit reviews for "{product_name}":

{reviews}

Return ONLY a JSON object like this, nothing else:
{{"score": 74, "label": "Positive"}}

Rules:
- score is a number from 0 to 100
- label is one of: "Very Positive", "Positive", "Neutral", "Negative", "Very Negative"
- Base it purely on the sentiment of the reviews"""
            }]
        )

        # Parse score safely
        import json, re
        score_text = score_response.choices[0].message.content.strip()
        match = re.search(r'\{.*?\}', score_text, re.DOTALL)
        if match:
            score_data = json.loads(match.group())
            sentiment_score = int(score_data.get("score", 50))
            sentiment_label = score_data.get("label", "Neutral")
        else:
            sentiment_score = 50
            sentiment_label = "Neutral"

        return {
            "ai_opinion": opinion_response.choices[0].message.content,
            "reddit_summary": reddit_response.choices[0].message.content,
            "sentiment_score": sentiment_score,
            "sentiment_label": sentiment_label
        }

    except Exception as e:
        return {
            "ai_opinion": f"AI opinion failed: {str(e)}",
            "reddit_summary": f"AI summarization failed: {str(e)}",
            "sentiment_score": 50,
            "sentiment_label": "Neutral"
        }