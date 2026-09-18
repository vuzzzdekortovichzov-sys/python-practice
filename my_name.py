import json

x = {
    "name": "timur",
    "age": 16,
    "game":["tarkov","dst"]
}
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(x, f, ensure_ascii=False, indent=2)
with open("data.json", "r", encoding="utf-8") as f:
    xyz = json.load(f)
print(xyz)
print(xyz["name"])