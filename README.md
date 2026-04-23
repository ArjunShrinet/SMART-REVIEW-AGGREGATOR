# 🔍 Smart Review Aggregator

An AI-powered product review aggregator that fetches real Reddit discussions, summarizes them using Groq's LLaMA AI, compares prices across Indian e-commerce stores, and gives you everything you need to make a smart buying decision.

---

## 🚀 What It Does

1. Paste an **Amazon product URL** or just **type a product name**
2. App extracts the product name and fetches **real Reddit posts**
3. **Groq AI** gives its own expert opinion on the product
4. **Groq AI** summarizes Reddit community reviews into Pros, Cons & Sentiment
5. Shows a **Sentiment Score (0–100)** with a colored progress bar
6. Displays **clickable Reddit review cards** with subreddit and author
7. Click **"Get Best Price"** to compare prices across Indian stores via SerpAPI
8. Optionally **compare two products** side by side
9. **Search history** saved locally for quick re-searches

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
│   │   │   └── routes.py           # /analyze and /prices endpoints
│   │   ├── services/
│   │   │   ├── ai_summarizer.py    # Groq AI — opinion, summary, sentiment score
│   │   │   ├── link_parser.py      # Extracts product name from Amazon URL
│   │   │   ├── reddit_scraper.py   # Fetches real Reddit posts
│   │   │   └── price_scraper.py    # SerpAPI price comparison
│   │   └── main.py                 # FastAPI app entry point
│   ├── .env                        # API keys (not committed)
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   └── page.js                 # Main UI page
│   └── next.config.js              # Next.js config (allowedDevOrigins)
└── README.md
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- [Groq API key](https://console.groq.com) (free)
- [SerpAPI key](https://serpapi.com) (100 free searches/month)

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
pip install fastapi uvicorn python-dotenv groq requests beautifulsoup4 google-search-results
```

Create a `.env` file inside the `backend/` folder:

```
GROQ_API_KEY=your_groq_api_key_here
SERPAPI_KEY=your_serpapi_key_here
```

Start the backend:

```bash
# Desktop only
python -m uvicorn app.main:app --reload

# Desktop + Phone on same WiFi
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
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
| `SERPAPI_KEY` | ✅ Yes | Get free key at [serpapi.com](https://serpapi.com) — 100 searches/month free |

---

## 📡 API Endpoints

### `POST /analyze`

**Request:**
```json
{
  "product_url": "https://amazon.in/Apple-iPhone-16/dp/B0CHX3QBCH",
  "is_name": false
}
```

**Response:**
```json
{
  "product": "apple iphone 16",
  "reviews": [
    {
      "text": "Review text...",
      "url": "https://reddit.com/r/iphone/comments/...",
      "subreddit": "iphone",
      "author": "username"
    }
  ],
  "ai_opinion": "The iPhone 16 is Apple's latest...",
  "reddit_summary": "Overall Sentiment: Positive\n\nPros:\n...",
  "sentiment_score": 78,
  "sentiment_label": "Positive"
}
```

---

### `POST /prices`

**Request:**
```json
{
  "product_name": "iPhone 16"
}
```

**Response:**
```json
{
  "product": "iPhone 16",
  "prices": [
    {
      "store": "Flipkart",
      "title": "Apple iPhone 16 128GB Black",
      "price": 77499,
      "price_display": "₹77,499",
      "url": "https://www.flipkart.com/...",
      "logo": "🏪",
      "best": true
    },
    {
      "store": "Amazon.in",
      "price": 79900,
      "price_display": "₹79,900",
      "logo": "🛒"
    }
  ]
}
```

---

## 🌐 How It Works

```
Browser (Next.js at localhost:3000)
         ↓  POST /analyze
FastAPI Backend (0.0.0.0:8000)
         ↓                  ↓                 ↓
Reddit Public JSON      Groq AI (x4 calls)   SerpAPI
(real posts)        opinion + summary      price comparison
                    + reddit score         across stores
                    + ai score
                    = averaged final score
         ↓                  ↓                 ↓
         └──────────── JSON back to Browser ──┘
```

---

## 🏷️ Supported Price Comparison Stores

Amazon.in · Flipkart · Croma · Reliance Digital · Vijay Sales · TataCliq · JioMart · Samsung · Apple · OnePlus · Myntra · Nykaa · Ajio · Meesho · Snapdeal · ShopClues · boAt

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
- [SerpAPI](https://serpapi.com) — Google Shopping price data
- [FastAPI](https://fastapi.tiangolo.com) — Modern Python web framework
- [Next.js](https://nextjs.org) — React framework

---

## 👨‍💻 Developer

Built as a Minor Project at **SRM Institute of Science and Technology** by **Arjun**

---

## 📄 License

MIT License — feel free to use and modify.
