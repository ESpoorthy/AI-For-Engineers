# Architecture — AI for Engineers

## Overview

The application is a **unified Flask app** that serves both the frontend UI and all API endpoints from a single process on port 8080. No separate servers, no React build step, no proxy configuration needed.

```
Browser
  │
  │  GET /           → serves ui/index.html
  │  POST /api/solve → answer engine
  │  GET  /health    → status check
  │
  ▼
┌──────────────────────────────────────┐
│        app.py  (Flask, port 8080)    │
│                                      │
│  ┌──────────────┐  ┌──────────────┐  │
│  │  UI Route    │  │  API Routes  │  │
│  │  GET /       │  │  POST /api/* │  │
│  └──────┬───────┘  └──────┬───────┘  │
│         │                 │          │
│         ▼                 ▼          │
│   ui/index.html     Answer Engine   │
└──────────────────────────────────────┘
```

---

## Answer Engine (Priority Order)

```
Question
   │
   ▼
┌──────────────────────────────────┐
│  1. Built-in Knowledge Base      │  ← 30+ topics, instant, no API call
│     (keyword pattern matching)   │
└──────────────┬───────────────────┘
               │ no match
               ▼
┌──────────────────────────────────┐
│  2. Google Gemini AI             │  ← gemini-2.5-flash
│     Rotates: KEY_1 → KEY_2 → KEY_3 │
└──────────────┬───────────────────┘
               │ quota / error
               ▼
┌──────────────────────────────────┐
│  3. OpenAI GPT-3.5               │  ← OPENAI_API_KEY
└──────────────┬───────────────────┘
               │ error
               ▼
┌──────────────────────────────────┐
│  4. Structured Fallback          │  ← generic step-by-step response
└──────────────────────────────────┘
               │
               ▼
         JSON Response
```

---

## API Keys

Keys stored in `.env`, loaded as environment variables at startup:

```
GEMINI_KEY_1, GEMINI_KEY_2, GEMINI_KEY_3  → rotated per request
OPENAI_API_KEY                             → used as fallback
```

Keys are never hardcoded in source files. The `.env` file is gitignored.

---

## Core Files

```
app.py              ← entry point; Flask app with all routes + answer engine
ui/index.html       ← full frontend (HTML/CSS/JS, no build step)
.env                ← API keys (gitignored)
requirements.txt    ← Python dependencies
```

---

## UI Architecture

`ui/index.html` is a self-contained single-page app (no framework, no build step):

- **Sidebar**: chat history, games, user profile — managed via localStorage
- **Chat area**: scrollable, renders rich answer cards with MathJax
- **Answer cards**: built from JSON response:
  - Gradient banner (source badge + confidence)
  - Question box (blue), summary box (green)
  - Collapsible step list with numbered circles + emoji icons
  - Concept tags, verification box (yellow), tips box (purple)
  - Slide-in animation
- **Games**: Step Builder, Concept Matcher, Formula Quest, Visual Solver — all in-page
- **Profiles**: multi-user support with progress tracking and badges
- **Charts**: weekly progress (bar + line) using Canvas API
- **Theme**: dark / light / system via CSS class switching

API calls use relative paths (`/api/solve`) — always hit the same Flask server.

---

## Legacy Directories

These exist from earlier development phases and are not required to run the app:

| Directory | Original Purpose |
|-----------|-----------------|
| `api/` | Standalone Flask API servers |
| `frontend/` | React app (Vite + Node.js) |
| `servers/` | Separate UI server scripts |

---

## ML Model (Research / Training)

A custom transformer model is included for research. It is not used in the live answer engine (Gemini/OpenAI handle that), but the training pipeline is fully functional.

```
training/
├── model.py          ← Transformer (6 layers, 8 heads, 256 dim, 8.2M params)
├── train_model.py    ← Training loop with checkpointing
├── inference.py      ← Autoregressive generation
└── config.py         ← Hyperparameters

data/processed/       ← JSON training datasets
models/
├── saved_models/     ← Final weights + tokenizer
└── checkpoints/      ← Per-epoch snapshots
```

---

## Deployment

### Local
```bash
export $(cat .env | xargs) && python3 app.py
# → http://localhost:8080
```

### Docker
```bash
docker-compose -f deployment/docker-compose.yml up --build
```
