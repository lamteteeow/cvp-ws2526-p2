# Computational Visual Perception - Project 2

Experiments with visual illusions using Google's Gemini API.

## Scripts

| Script | Purpose |
|--------|---------|
| `main.py` | Image generation of optical illusions (Penrose stairs, Escher-style) |
| `main2.py` | Image-to-image generation with reference images for other testing purposes |
| `main3.py` | Hybrid illusion analysis - detects hidden entities in hybrid images |

## Setup

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Set environment variable:
   ```bash
   export GOOGLE_CLOUD_API_KEY="your-api-key"
   ```

## Usage

### Analyze Hybrid Illusion

```bash
uv run python main3.py
```

Analyzes `ref/hybrid.jpeg` and appends results to `output/hybrid_analysis.md` with timestamps.

### Generate Optical Illusions

```bash
uv run python main.py
```

Generates Penrose stairs and Escher-style illusions to `output/`.

## Project Structure

```
├── ref/                  # Reference images
│   ├── hybrid.jpeg       # Hybrid illusion input
│   ├── penrose_stairway.png
│   └── escher_waterfall.png
├── output/               # Generated outputs
└── main*.py              # Scripts
```

## Requirements

- Python 3.x
- `google-genai` SDK
- `Pillow`
