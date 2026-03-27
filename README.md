# 🔥 FLAMES Game

> *The ultimate school-era relationship calculator — animated, AI-powered, and themed!*

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green?style=for-the-badge&logo=fastapi)
![JavaScript](https://img.shields.io/badge/JavaScript-Vanilla-yellow?style=for-the-badge&logo=javascript)
![Groq](https://img.shields.io/badge/Groq-LLaMA3-purple?style=for-the-badge)
![Free](https://img.shields.io/badge/Cost-FREE-brightgreen?style=for-the-badge)

---

## ✨ What is FLAMES?

**F**riends · **L**oves · **A**ffection · **M**arriage · **E**nemies · **S**iblings

A full-stack web app that calculates your FLAMES relationship with anyone — with animated letter-by-letter breakdown, dynamic themed backgrounds, funny disclaimers, BGM suggestions, and optional AI-generated stories!

---

## 👥 Team Responsibilities

| Role | Person | Files |
|------|--------|-------|
| 🎨 **UI / Frontend** | You | `frontend/index.html`, `frontend/style.css`, `frontend/app.js` |
| ⚙️ **Backend / API** | Friend 1 | `backend/app.py`, `backend/flames_engine.py` |
| 🤖 **AI / Model** | Friend 2 | `model/story_generator.py` |

---

## 📁 Project Structure

```
flames_game/
│
├── backend/
│   ├── flames_engine.py        ← Core FLAMES algorithm
│   ├── app.py                  ← FastAPI REST API
│   ├── requirements.txt
│   └── __init__.py
│
├── frontend/
│   ├── index.html              ← Main UI page
│   ├── style.css               ← Animations + themes
│   └── app.js                  ← API calls + letter animation
│
├── model/
│   ├── story_generator.py      ← Groq AI story generation
│   └── __init__.py
│
├── tests/
│   └── test_flames_engine.py
│
├── FLAMES_README.html          ← 🌟 Open in browser for animated docs!
├── .env.example
├── .gitignore
└── README.md
```

---

## 🚀 How to Run

### 1. Install backend dependencies
```bash
cd flames_game/backend
pip install -r requirements.txt
```

### 2. Set up your Groq API key
```bash
# Copy the example env file
cp .env.example .env

# Open .env and paste your key:
GROQ_API_KEY=gsk_your_key_here
```

> 📖 **How to get a free Groq key** → see section below

### 3. Start the backend (Terminal 1 — keep open)
```bash
cd flames_game/backend
uvicorn app:app --reload
# ✅ Running on http://localhost:8000
```

### 4. Open the frontend (Terminal 2 / VS Code)
```
Open frontend/index.html → Right click → Open with Live Server
# ✅ Running on http://127.0.0.1:5500
```

> ⚠️ **Both must run simultaneously** — backend on port `8000`, frontend on port `5500`

---

## 🔑 How to Get Your FREE Groq API Key

> **Groq is completely free.** No credit card. No hidden charges.

| Step | Action |
|------|--------|
| 1 | Go to **[console.groq.com](https://console.groq.com)** |
| 2 | Click **Sign Up** → use Google account (30 seconds) |
| 3 | Left sidebar → click **"API Keys"** |
| 4 | Click **"Create API Key"** → name it `flames-game` |
| 5 | ⚠️ **Copy the key immediately** — shown only once! |
| 6 | Paste into your `.env` file: `GROQ_API_KEY=gsk_xxx...` |
| 7 | Toggle **"Enable AI Story ✨"** in the app and enjoy! |

### Free Tier Limits

| Model | Requests/Day | Cost |
|-------|-------------|------|
| LLaMA 3 8B | 14,400 | ✅ FREE |
| LLaMA 3 70B | 14,400 | ✅ FREE |

> 💡 14,400 requests/day = you'd have to calculate FLAMES non-stop all day to hit the limit!

---

## 🔌 API Reference

### `POST /api/flames`
Calculate FLAMES result for two names.

**Request:**
```json
{
  "name1": "Akash",
  "name2": "Priya",
  "generate_story": true
}
```

**Response:**
```json
{
  "winner": "A",
  "label": "Affection",
  "emoji": "🥰",
  "common_letters": ["A"],
  "remaining_name1": "KASH",
  "remaining_name2": "PRIY",
  "total_count": 8,
  "elimination_order": ["F", "L", "M", "E", "S"],
  "story": "AI generated story here...",
  "steps": [...]
}
```

### `GET /api/flames/options`
Returns all 6 FLAMES outcomes.

### `GET /health`
Health check → `{"status": "ok"}`

> 📄 Auto-generated API docs at: `http://localhost:8000/docs`

---

## 🧠 How the Algorithm Works

```
Step 1 — Remove common letters
  Akash → A K A S H
  Priya → P R I Y A
  Common: A (once) → removed from both

Step 2 — Count remaining
  KASH = 4 letters
  PRIY = 4 letters
  Total = 8

Step 3 — FLAMES circular elimination
  F L A M E S  → count 8 → eliminate S
  F L A M E    → count 8 → eliminate L
  ...
  Winner = A (Affection 🥰)
```

---

## 🎨 UI Features

- 🎬 **Letter-by-letter animation** — names spread out, common letters glow, get struck through
- 🎭 **Dynamic themes** — entire page changes color per outcome
- ⚠️ **Funny disclaimers** — unique warning per result before revealing
- 🎵 **BGM suggestions** — YouTube links for outcome-specific music
- 🌊 **Floating emoji background** — changes per outcome (hearts, fire, rakhi...)
- 🎊 **Particle effects** — petals for Love, confetti for Marriage, rage particles for Enemies

---

## 🧪 Running Tests

```bash
pip install pytest
cd flames_game
pytest tests/ -v
```

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Backend | Python 3.11+, FastAPI, Uvicorn |
| AI Model | Groq API (LLaMA 3 8B) |
| Testing | pytest |

---

## 🌟 Animated README

For a much cooler experience, open **`FLAMES_README.html`** in your browser — it has a dark starfield background, glowing animations, scroll reveal effects, and the full Groq setup guide!

---

*Built with ❤️ for school-era nostalgia · FLAMES Game v2.0*