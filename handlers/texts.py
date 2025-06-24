import json

with open("static/text.json", "r", encoding="utf-8") as f:
    TEXTS = json.load(f)
