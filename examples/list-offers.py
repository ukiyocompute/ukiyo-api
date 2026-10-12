"""List rentable GPUs and prices. Public endpoint: no API key needed. Python 3.8+, no dependencies."""
import json
import urllib.request

with urllib.request.urlopen("https://pay.u-kiyo.ai/api/v1/offers", timeout=20) as response:
    offers = json.load(response)["data"]

for offer in sorted(offers, key=lambda o: o["pricePerHourMinor"])[:10]:
    print(f'{offer["name"]:<28} x{offer["gpuCount"]}  ${offer["pricePerHourMinor"] / 100:.2f}/hour  {offer["id"]}')
