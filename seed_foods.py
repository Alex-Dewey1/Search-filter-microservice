"""
seed_foods.py — example seed for a calorie tracker project.
Run: python seed_foods.py

This is ONE possible use of ms5-search.
You can replace this with any dataset (products, movies, etc.)
"""

import requests

BASE = "http://localhost:5005"

FOODS = [
    {"name": "Greek Yogurt",   "category": "dairy",    "tags": "protein,breakfast", "num1": 59,  "num2": 10.0, "num1_label": "calories", "num2_label": "protein_g"},
    {"name": "Chicken Breast", "category": "protein",  "tags": "meat,lunch,dinner", "num1": 165, "num2": 31.0, "num1_label": "calories", "num2_label": "protein_g"},
    {"name": "Brown Rice",     "category": "grains",   "tags": "carbs,lunch,dinner","num1": 216, "num2": 4.5,  "num1_label": "calories", "num2_label": "protein_g"},
    {"name": "Banana",         "category": "fruit",    "tags": "snack,breakfast",   "num1": 89,  "num2": 1.1,  "num1_label": "calories", "num2_label": "protein_g"},
    {"name": "Eggs",           "category": "protein",  "tags": "breakfast,cheap",   "num1": 155, "num2": 13.0, "num1_label": "calories", "num2_label": "protein_g"},
    {"name": "Oats",           "category": "grains",   "tags": "breakfast,fiber",   "num1": 389, "num2": 17.0, "num1_label": "calories", "num2_label": "protein_g"},
    {"name": "Salmon",         "category": "protein",  "tags": "fish,dinner,omega3","num1": 208, "num2": 20.0, "num1_label": "calories", "num2_label": "protein_g"},
    {"name": "Broccoli",       "category": "vegetable","tags": "healthy,dinner",    "num1": 34,  "num2": 2.8,  "num1_label": "calories", "num2_label": "protein_g"},
    {"name": "Almonds",        "category": "nuts",     "tags": "snack,healthy",     "num1": 579, "num2": 21.0, "num1_label": "calories", "num2_label": "protein_g"},
    {"name": "Sweet Potato",   "category": "vegetable","tags": "carbs,dinner",      "num1": 86,  "num2": 1.6,  "num1_label": "calories", "num2_label": "protein_g"},
]

for food in FOODS:
    r = requests.post(f"{BASE}/items", json=food)
    print(r.status_code, food["name"])

print("Done! Try: GET /search?q=chicken or /search?max_num1=100&category=fruit")
