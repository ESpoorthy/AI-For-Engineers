# Setup Guide — AI for Engineers

## Prerequisites

- Python 3.8+ (3.10+ recommended)
- pip
- API keys: Google Gemini (up to 3 keys) and/or OpenAI

## Step 1: Clone the Repository

```bash
git clone https://github.com/ESpoorthy/AI-For-Engineers.git
cd AI-For-Engineers
```

## Step 2: Create a Virtual Environment (Recommended)

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

## Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

Key packages:

| Package | Purpose |
|---------|---------|
| `flask` | Web server (UI + API) |
| `flask-cors` | Cross-origin request support |
| `google-genai` | Google Gemini AI |
| `openai` | OpenAI GPT fallback |
| `requests` | HTTP calls |
| `python-dotenv` | Load `.env` file |
| `tensorflow` | ML model training (optional) |

## Step 4: Configure API Keys

Create a `.env` file in the project root:

```env
GEMINI_KEY_1=your_first_gemini_api_key
GEMINI_KEY_2=your_second_gemini_api_key
GEMINI_KEY_3=your_third_gemini_api_key
OPENAI_API_KEY=your_openai_api_key
```

**Rules:**
- No spaces around `=`
- No quotes around values
- Never commit this file (already in `.gitignore`)
- Keys are loaded via environment variables only — never hardcoded

### Getting API Keys

- **Gemini**: [Google AI Studio](https://aistudio.google.com/app/apikey) — free tier available, add billing for higher quota
- **OpenAI**: [platform.openai.com](https://platform.openai.com/api-keys) — requires billing for GPT-3.5

> The app works with just Gemini keys. OpenAI is only used as a fallback.

## Step 5: Run the Application

```bash
export $(cat .env | xargs) && python3 app.py
```

**Windows (PowerShell):**
```powershell
Get-Content .env | ForEach-Object {
  $name, $value = $_ -split '=', 2
  [System.Environment]::SetEnvironmentVariable($name, $value)
}
python app.py
```

## Step 6: Access the App

Open **http://localhost:8080** in your browser.

The unified app serves both the UI and all API endpoints from this single URL.

---

## Verifying the Setup

**Health check:**
```bash
curl http://localhost:8080/health
```

Expected:
```json
{"status": "healthy", "ai_enabled": true, "message": "Single-URL unified application"}
```

**Test a question:**
```bash
curl -X POST http://localhost:8080/api/solve \
  -H "Content-Type: application/json" \
  -d '{"question": "What is sin(90°)?"}'
```

---

## Docker Deployment (Alternative)

```bash
docker-compose -f deployment/docker-compose.yml up --build
```

Make sure your `.env` file is present — Docker Compose picks it up automatically.

---

## Optional: ML Model Training

The app works without training a custom model (it uses Gemini/OpenAI). To train the local transformer:

```bash
python training/test_model.py    # verify architecture
python training/train_model.py   # train on dataset
```

Output goes to `models/saved_models/` and `models/checkpoints/`.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError` | Activate venv and re-run `pip install -r requirements.txt` |
| `Address already in use` | Change `port=8080` in `app.py` |
| Gemini API errors | Check keys in `.env` are valid and have quota |
| UI not loading | Confirm `ui/index.html` exists |
| Voice input not working | Use Chrome browser |

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for more.
