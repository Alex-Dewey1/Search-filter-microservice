"""
Search & Filter Microservice
Configure via environment variables or seed the database.
"""

import os
import sqlite3
import time
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_PATH = os.environ.get("DB_PATH", "data.db")


# Database helpers

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                name      TEXT NOT NULL,
                category  TEXT,
                tags      TEXT,          -- comma-separated
                data      TEXT,          -- JSON blob; any extra fields you want
                num1      REAL,          -- generic numeric field (e.g. price, calories)
                num2      REAL,          -- generic numeric field (e.g. rating, weight)
                num1_label TEXT,         -- human label for num1 (e.g. "calories")
                num2_label TEXT          -- human label for num2 (e.g. "protein_g")
            )
        """)
        db.execute("CREATE INDEX IF NOT EXISTS idx_name     ON items(name)")
        db.execute("CREATE INDEX IF NOT EXISTS idx_category ON items(category)")
        db.commit()


# Routes

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "ms5-search"})


@app.route("/search")
def search():
    """
    GET /search
    Query params (all optional):
      q          – keyword, matched against name and tags
      category   – exact category match
      min_num1   – lower bound on num1 (e.g. min_calories)
      max_num1   – upper bound on num1
      min_num2   – lower bound on num2
      max_num2   – upper bound on num2
      limit      – max results (default 50)
      offset     – pagination offset (default 0)
    """
    start = time.time()

    q        = request.args.get("q", "").strip().lower()
    category = request.args.get("category", "").strip()
    min_num1 = request.args.get("min_num1", type=float)
    max_num1 = request.args.get("max_num1", type=float)
    min_num2 = request.args.get("min_num2", type=float)
    max_num2 = request.args.get("max_num2", type=float)
    limit    = min(request.args.get("limit", 50, type=int), 200)
    offset   = request.args.get("offset", 0, type=int)

    sql    = "SELECT * FROM items WHERE 1=1"
    params = []

    if q:
        sql += " AND (LOWER(name) LIKE ? OR LOWER(tags) LIKE ?)"
        params += [f"%{q}%", f"%{q}%"]
    if category:
        sql += " AND category = ?"
        params.append(category)
    if min_num1 is not None:
        sql += " AND num1 >= ?"
        params.append(min_num1)
    if max_num1 is not None:
        sql += " AND num1 <= ?"
        params.append(max_num1)
    if min_num2 is not None:
        sql += " AND num2 >= ?"
        params.append(min_num2)
    if max_num2 is not None:
        sql += " AND num2 <= ?"
        params.append(max_num2)

    try:
        with get_db() as db:
            total  = db.execute(
                f"SELECT COUNT(*) FROM ({sql})", params
            ).fetchone()[0]
            rows   = db.execute(
                sql + f" ORDER BY name LIMIT {limit} OFFSET {offset}", params
            ).fetchall()
    except Exception as e:
        # Fault tolerance: return empty results, not a crash
        return jsonify({
            "results": [],
            "count": 0,
            "total": 0,
            "error": "Filter error — returning empty results",
            "detail": str(e)
        }), 200

    elapsed_ms = round((time.time() - start) * 1000, 1)

    return jsonify({
        "results":    [dict(r) for r in rows],
        "count":      len(rows),
        "total":      total,
        "offset":     offset,
        "elapsed_ms": elapsed_ms
    })


@app.route("/search/filters")
def list_filters():
    """GET /search/filters — returns available categories and numeric field labels."""
    try:
        with get_db() as db:
            categories = [r[0] for r in db.execute(
                "SELECT DISTINCT category FROM items WHERE category IS NOT NULL ORDER BY category"
            ).fetchall()]
            labels_row = db.execute(
                "SELECT num1_label, num2_label FROM items LIMIT 1"
            ).fetchone()
            num1_label = labels_row["num1_label"] if labels_row else "num1"
            num2_label = labels_row["num2_label"] if labels_row else "num2"
    except Exception:
        return jsonify({"categories": [], "num1_label": "num1", "num2_label": "num2"})

    return jsonify({
        "categories": categories,
        "num1_label": num1_label,
        "num2_label": num2_label
    })


@app.route("/items", methods=["POST"])
def add_item():
    """
    POST /items — add a new searchable item.
    Body (JSON):
      name, category, tags, data, num1, num2, num1_label, num2_label
    """
    body = request.get_json(force=True)
    required = ["name"]
    if not all(k in body for k in required):
        return jsonify({"error": "name is required"}), 400

    with get_db() as db:
        cur = db.execute(
            """INSERT INTO items (name, category, tags, data, num1, num2, num1_label, num2_label)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                body.get("name"),
                body.get("category"),
                body.get("tags"),
                body.get("data"),
                body.get("num1"),
                body.get("num2"),
                body.get("num1_label", "num1"),
                body.get("num2_label", "num2"),
            )
        )
        db.commit()

    return jsonify({"id": cur.lastrowid, "status": "created"}), 201


# Startup

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5005))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("DEBUG", "false") == "true")
