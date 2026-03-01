import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def summarize_reviews(reviews: list):

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return "Groq API key not configured."

    try:
        client = Groq(api_key=api_key)

        prompt = f"""
        Summarize the following Reddit reviews:

        {reviews}

        Give:
        - Overall sentiment
        - Pros
        - Cons
        """

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI summarization failed: {str(e)}"