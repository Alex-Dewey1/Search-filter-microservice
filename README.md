# MS5 — Search & Filter Microservice

A **generic, project-agnostic** search and filter service. Drop in any dataset and query it by keyword, category, and two numeric range fields.

## What it does
- Keyword search across item names and tags
- Category filtering
- Two configurable numeric range filters (e.g. calories, price, rating, weight)
- Fault-tolerant: filter errors return empty results, not 500s
- Pagination built in

## Quick start
```bash
pip install -r requirements.txt
python app.py          # runs on port 5005
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/search` | Search with optional filters |
| GET | `/search/filters` | List available categories + field labels |
| POST | `/items` | Add an item to the dataset |

### Search params
| Param | Type | Example |
|-------|------|---------|
| `q` | string | `?q=chicken` |
| `category` | string | `?category=protein` |
| `min_num1` | float | `?min_num1=50` |
| `max_num1` | float | `?max_num1=200` |
| `min_num2` | float | `?min_num2=10` |
| `max_num2` | float | `?max_num2=30` |
| `limit` | int | `?limit=20` (max 200) |
| `offset` | int | `?offset=40` |

### Add an item
```json
POST /items
{
  "name": "Greek Yogurt",
  "category": "dairy",
  "tags": "protein,breakfast",
  "num1": 59,
  "num1_label": "calories",
  "num2": 10.0,
  "num2_label": "protein_g"
}
```

## Using it in your project

The `num1`/`num2` fields are intentionally generic. Map them to whatever makes sense:

| Project | num1 | num2 |
|---------|------|------|
| Calorie tracker | calories | protein_g |
| E-commerce | price | rating |
| Movie app | runtime_min | imdb_score |
| Book app | pages | avg_rating |

## Seed your data
```bash
# Example: calorie tracker foods
python seed_foods.py

# Or POST your own items via the API
```

## Environment variables
| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `5005` | Port to run on |
| `DB_PATH` | `data.db` | SQLite database path |
| `DEBUG` | `false` | Enable Flask debug mode |
