# Computational Visual Perception - Project 2

Experiments with visual illusions using Google's Gemini API.

## Scripts

| Script | Purpose |
|--------|---------|
| `main.py` | Generate optical illusions (Penrose stairs) |
| `main2.py` | Generate optical illusions (Escher waterfall) |
| `main3.py` | Hybrid illusion analysis - detect hidden entities |
| `main4.py` | Explore illusion analysis - detect hidden entities |

## Usage

```bash
# Analyze hybrid illusion (gemini-3-pro-preview with thinking mode)
uv run python main3.py

# Generate optical illusions (gemini-3-pro-image-preview)
uv run python main.py
```

Requires `GOOGLE_CLOUD_API_KEY` environment variable.
