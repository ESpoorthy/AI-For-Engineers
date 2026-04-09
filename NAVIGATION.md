# Navigation Guide — AI for Engineers

## Running the App

```bash
export $(cat .env | xargs) && python3 app.py
```

**URL**: http://localhost:8080

One URL. One command. UI and API both run here.

---

## Key Files

| File | Purpose |
|------|---------|
| `app.py` | Unified Flask application — start here |
| `ui/index.html` | Frontend — ChatGPT-like interface |
| `.env` | API keys (gitignored, never commit) |
| `requirements.txt` | Python dependencies |

---

## API Endpoints (all at localhost:8080)

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Serves the UI |
| `GET` | `/health` | Health check |
| `POST` | `/api/solve` | Solve a math question |
| `GET` | `/api/problem-types` | Supported problem types |
| `GET` | `/api/examples` | Example questions |
| `GET` | `/api/ai-status` | AI configuration status |

---

## Documentation

| Doc | What's in it |
|-----|-------------|
| [docs/QUICKSTART.md](docs/QUICKSTART.md) | Fastest path to running the app |
| [docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md) | Full installation + `.env` setup |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | How the app is structured |
| [docs/CURRENT_STATUS.md](docs/CURRENT_STATUS.md) | All completed features |
| [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Common issues and fixes |
| [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | Directory layout |

---

## Legacy Directories (not needed to run the app)

| Directory | Notes |
|-----------|-------|
| `api/` | Old standalone API servers |
| `frontend/` | Old React app (Vite) |
| `servers/` | Old separate UI server scripts |
| `demos/` | Standalone HTML demo files |
