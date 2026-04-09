# Project Structure — AI for Engineers

## Directory Layout

```
AI-For-Engineers/
│
├── app.py                    # Unified Flask app — UI + API, single entry point
├── .env                      # API keys (gitignored)
├── requirements.txt          # Python dependencies
│
├── ui/
│   └── index.html            # Main frontend (ChatGPT-like, no build step)
│
├── docs/                     # Documentation
│   ├── QUICKSTART.md         # 5-minute setup
│   ├── SETUP_GUIDE.md        # Full installation guide
│   ├── ARCHITECTURE.md       # System design
│   ├── CURRENT_STATUS.md     # Completed features
│   ├── TROUBLESHOOTING.md    # Common issues
│   └── ...
│
├── training/                 # ML model training (research / offline)
│   ├── model.py              # Transformer architecture (8.2M params)
│   ├── train_model.py        # Training loop with checkpointing
│   ├── inference.py          # Autoregressive generation
│   ├── data_pipeline.py      # Data loading and preprocessing
│   └── config.py             # Hyperparameters
│
├── data/
│   └── processed/            # JSON training datasets
│       ├── engineering_math_dataset.json
│       ├── comprehensive_math_dataset.json
│       ├── calculus_problems.json
│       ├── linear_algebra_problems.json
│       └── merged_training_data.json
│
├── models/
│   ├── saved_models/         # Trained weights, tokenizer, config
│   └── checkpoints/          # Per-epoch model snapshots
│
├── deployment/
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── logs/                     # TensorBoard training logs
│
├── NAVIGATION.md             # Quick reference for URLs and files
├── PROJECT_STRUCTURE.md      # This file
├── README.md                 # Main documentation
├── LICENSE
└── .gitignore
```

## Legacy Directories

These were used in earlier development phases. The app no longer requires them to run.

| Directory | Notes |
|-----------|-------|
| `api/` | Old standalone Flask API servers |
| `frontend/` | Old React app (Vite + Node.js) |
| `servers/` | Old separate UI server scripts |
| `demos/` | Standalone HTML demo files |
| `examples/` | Code usage examples |
| `scripts/` | Utility/verification scripts |

---

## How to Run

```bash
export $(cat .env | xargs) && python3 app.py
# → http://localhost:8080
```

See [docs/QUICKSTART.md](docs/QUICKSTART.md) for full setup.
