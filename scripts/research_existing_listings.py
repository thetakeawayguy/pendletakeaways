#!/usr/bin/env python3
"""Build a review-only CSV from the site's existing takeaway listings, offline."""
import csv, html, re
from pathlib import Path
source=Path("index.html").read_text(encoding="utf-8")
pattern=re.compile(r'<h3><a href="([^"]+\.html)">([^<]+)</a></h3>\s*<p class="small">([^<]+)</p>\s*<p>([^<]+)</p>',re.I)
rows=[]
for page,name,category,address in pattern.findall(source):
    town=category.split("·")[0].strip()
    if town.casefold()!="nelson":
        continue
    rows.append({"name":html.unescape(name),"category":html.unescape(category),"address":html.unescape(address),"website":"https://pendletakeaways.co.uk/"+page,"source":"Existing Pendle Takeaways listing","review_status":"Verify address and current trading status"})
out=Path("research")
out.mkdir(exist_ok=True)
with (out/"nelson-existing-listings.csv").open("w",newline="",encoding="utf-8") as file:
    writer=csv.DictWriter(file,fieldnames=["name","category","address","website","source","review_status"])
    writer.writeheader()
    writer.writerows(rows)
print(f"Created {len(rows)} Nelson research candidates from existing listings.",flush=True)
