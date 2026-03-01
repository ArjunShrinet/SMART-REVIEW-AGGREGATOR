# 🔍 Smart Review Aggregator

An AI-powered product review aggregator that fetches real Reddit discussions and summarizes them using Groq's LLaMA AI — all from a single Amazon product URL.

---

## 🚀 What It Does

1. You paste an **Amazon product URL**
2. It extracts the **product name** from the URL
3. Fetches **real Reddit posts** about that product
4. Uses **Groq AI (LLaMA 3.3)** to summarize the reviews into:
   - Overall Sentiment
   - Pros
   - Cons
5. Displays everything in a clean UI with **clickable Reddit links**

---

## 🛠️ Tech Stack

### Frontend
| Tech | Purpose |
|------|---------|
| Next.js | React framework |
| Tailwind CSS | Styling |
| JavaScript (fetch) | Connects to backend |

### Backend
| Tech | Purpose |
|------|---------|
| FastAPI | Python web framework |
| Uvicorn | ASGI server |
| Pydantic | Request validation |
| python-dotenv | Loads environment variables |
| requests | Fetches Reddit JSON data |

### AI & Data
| Tech | Purpose |
|------|---------|
| Groq (LLaMA 3.3-70b) | AI summarization |
| Reddit Public JSON API | Real Reddit posts (no API key needed) |

---

## 📁 Project Structure

```
MINOR_PROJECT_PRODUCT/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py          # /analyze endpoint
│   │   ├── services/
│   │   │   ├── ai_summarizer.py   # Groq AI summarization
│   │   │   ├── link_parser.py     # Extracts product name from URL
│   │   │   └── reddit_scraper.py  # Fetches real Reddit posts
│   │   └── main.py                # FastAPI app entry point
│   ├── .env                       # API keys (not committed)
│   └── requirements.txt
├── frontend/
│   └── app/
│       └── page.js                # Main UI page
└── README.md
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- A free [Groq API key](https://console.groq.com)

---

### 1. Clone the repository

```bash
git clone https://github.com/your-username/smart-review-aggregator.git
cd smart-review-aggregator
```

---

### 2. Backend Setup

```bash
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn python-dotenv groq requests
```

Create a `.env` file inside the `backend/` folder:

```
GROQ_API_KEY=your_groq_api_key_here
```

Start the backend:

```bash
uvicorn app.main:app --reload
```

Backend runs at: `http://127.0.0.1:8000`

---

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: `http://localhost:3000`

---

## 🔑 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | ✅ Yes | Get free key at [console.groq.com](https://console.groq.com) |

---

## 📡 API

### `POST /analyze`

**Request:**
```json
{
  "product_url": "https://amazon.in/Apple-iPhone-15-Pro-Max/dp/B0CHX3QBCH"
}
```

**Response:**
```json
{
  "product": "Apple iPhone 15 Pro Max",
  "reviews": [
    {
      "text": "Review text here...",
      "url": "https://reddit.com/r/iphone/comments/...",
      "subreddit": "iphone",
      "author": "username"
    }
  ],
  "summary": "Overall Sentiment: Positive\n\nPros:\n- Great camera\n\nCons:\n- Expensive"
}
```

---

## 🌐 How It Works

```
Browser (Next.js)
      ↓  POST /analyze
FastAPI Backend
      ↓                    ↓
Reddit Public JSON      Groq AI
(real posts)         (summarizes them)
      ↓                    ↓
      └────── JSON back to Browser
```

---

## 📦 Requirements

Create a `requirements.txt` in your `backend/` folder:

```
fastapi
uvicorn
python-dotenv
groq
requests
pydantic
```

Install all at once:
```bash
pip install -r requirements.txt
```

---

## 🙌 Acknowledgements

- [Groq](https://groq.com) — Ultra-fast LLaMA inference
- [Reddit](https://reddit.com) — Public JSON search API
- [FastAPI](https://fastapi.tiangolo.com) — Modern Python web framework
- [Next.js](https://nextjs.org) — React framework

---

## 📄 License

MIT License — feel free to use and modify.
