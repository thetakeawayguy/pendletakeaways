#!/usr/bin/env python3
"""Discover Nelson food businesses from OpenStreetMap for owner review.
No customer reviews or photographs are copied. Nothing is auto-published.
"""
import csv, datetime, io, json, urllib.parse, urllib.request, urllib.error, time
from pathlib import Path

# Approximate Nelson town centre bounding box; review results before publication.
BBOX = (53.820, -2.245, 53.853, -2.182)
query = '''[out:json][timeout:18];
(
  nwr["amenity"~"^(fast_food|restaurant|cafe)$"](%s,%s,%s,%s);
  nwr["shop"="bakery"](%s,%s,%s,%s);
);
out center tags;''' % (BBOX + BBOX)
data = None
endpoints = (
    "https://overpass.nchc.org.tw/api/interpreter",
    "https://overpass.private.coffee/api/interpreter",
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
)
for endpoint in endpoints:
    try:
        print("Trying:", endpoint, flush=True)
        url = endpoint + "?" + urllib.parse.urlencode({"data": query})
        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; PendleTakeawaysResearch/1.0)", "Accept": "application/json"})
        with urllib.request.urlopen(request, timeout=28) as response:
            data = json.load(response)
        print("Data received successfully.", flush=True)
        break
    except (urllib.error.URLError, TimeoutError, ValueError, OSError) as error:
        print("Endpoint failed:", type(error).__name__, str(error), flush=True)
if data is None:
    print("All OpenStreetMap services unavailable. No data was changed.", flush=True)
    raise SystemExit(1)
rows = []
for item in data.get("elements", []):
    tags = item.get("tags", {})
    name = tags.get("name", "").strip()
    if not name:
        continue
    location = item.get("center", item)
    lat, lon = location.get("lat"), location.get("lon")
    if lat is None or lon is None:
        continue
    address = " ".join(x for x in [tags.get("addr:housenumber", ""), tags.get("addr:street", "")] if x)
    rows.append({
        "name":name,
        "category":tags.get("amenity", tags.get("shop", "")),
        "cuisine":tags.get("cuisine", ""),
        "address":address,
        "postcode":tags.get("addr:postcode", ""),
        "website":tags.get("website", tags.get("contact:website", "")),
        "phone":tags.get("phone", tags.get("contact:phone", "")),
        "latitude":lat,
        "longitude":lon,
        "osm_url":f"https://www.openstreetmap.org/{item['type']}/{item['id']}",
        "review_status":"Needs manual verification"
    })
rows.sort(key=lambda x:x["name"].casefold())
out = Path("research")
out.mkdir(exist_ok=True)
columns = ["name","category","cuisine","address","postcode","website","phone","latitude","longitude","osm_url","review_status"]
with (out/"nelson-business-candidates.csv").open("w", newline="", encoding="utf-8") as file:
    writer=csv.DictWriter(file, fieldnames=columns)
    writer.writeheader()
    writer.writerows(rows)
(out/"nelson-research-metadata.json").write_text(json.dumps({"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"candidate_count":len(rows),"source":"OpenStreetMap contributors (ODbL) via Overpass API","note":"Research candidates only. Verify before publication."}, indent=2)+"\n", encoding="utf-8")
print(f"Found {len(rows)} candidates for manual review.")
