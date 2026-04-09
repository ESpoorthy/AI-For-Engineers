# Quick Start — AI for Engineers

## Prerequisites

- Python 3.8+
- API keys for Gemini and/or OpenAI

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Set Up API Keys

Create a `.env` file in the project root:

```env
GEMINI_KEY_1=your_first_gemini_key
GEMINI_KEY_2=your_second_gemini_key
GEMINI_KEY_3=your_third_gemini_key
OPENAI_API_KEY=your_openai_key
```

> Keys are loaded via environment variables only. The `.env` file is gitignored — never commit it.

Get Gemini keys free at [Google AI Studio](https://aistudio.google.com/app/apikey).

## 3. Run the App

```bash
export $(cat .env | xargs) && python3 app.py
```

## 4. Open the App

Go to **http://localhost:8080**

One URL. One command. UI and API both run here — no separate servers needed.

---

## Try These Questions

- `Find the polar form of z = 1 + i`
- `Solve dy/dx + 2y = 4`
- `What is a Laplace transform?`
- `What is a DFA?`
- `Find the 12th term of the AP: 4, 9, 14, ...`
- `Explain eigenvalues`
- `Solve x³ - 6x² + 11x - 6 = 0`

---

## Quick API Test

```bash
curl -X POST http://localhost:8080/api/solve \
  -H "Content-Type: application/json" \
  -d '{"question": "What is sin(90°)?"}'
```

```bash
curl http://localhost:8080/health
```

---

## Troubleshooting

**Port already in use**: Edit `app.py` and change `port=8080` to another port.

**Keys not loading**: Make sure `.env` has no spaces around `=` and no quotes around values.

**Missing module**: Run `pip install -r requirements.txt` again.

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for more.
