import requests
import json
url = "https://catfact.ninja/fact"
responce = requests.get(url)
data = responce.json()

factis = data["fact"]
print("факт:", factis)