import os
import sys
import requests

CURRENCY = sys.argv[1] if len(sys.argv) > 1 else 'BRL'
API_URL = f"https://api.exchangerate-api.com/v4/latest/{CURRENCY}"

response = requests.get(API_URL)
data = response.json()

output_dir = "/app/data"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(f"{output_dir}/exchange_rates_{CURRENCY}.json", "w") as f:
    f.write(response.text)

print(f"Exchange rates data for {CURRENCY} saved!")