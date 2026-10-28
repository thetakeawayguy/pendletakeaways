#!/usr/bin/env python3
"""Build a branding research queue. Inspect official sites only when supplied.
No third-party logo or photo downloading and no automated publication.
"""
import csv, html, re, urllib.parse, urllib.request
from pathlib import Path
from html.parser import HTMLParser

class Metadata(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title=""
        self.meta={}
        self.icons=[]
        self._title=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=="title": self._title=True
        if tag=="meta":
            key=a.get("property",a.get("name","")).lower()
            if key: self.meta[key]=a.get("content","")
        if tag=="link" and "icon" in a.get("rel","").lower():
            self.icons.append(a.get("href",""))
    def handle_endtag(self,tag):
        if tag=="title":self._title=False
    def handle_data(self,data):
        if self._title:self.title+=data

source=Path("research/nelson-branding-tracker.csv")
with source.open(encoding="utf-8-sig",newline="") as f:
    entries=list(csv.DictReader(f))
output=[]
for entry in entries:
    name=entry["business"].strip()
    url=(entry.get("official_website") or "").strip()
    search="https://www.google.com/search?"+urllib.parse.urlencode({"q":name+" Nelson Lancashire official takeaway logo menu"})
    row={"business":name,"research_search_url":search,"official_website":url,"website_title":"","theme_colour_candidate":"","icon_url_candidate":"","image_url_candidate":"","research_note":"Find and verify official website manually"}
    if url.startswith("https://") or url.startswith("http://"):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"PendleTakeawaysBrandResearch/1.0"})
            with urllib.request.urlopen(req,timeout=12) as resp:
                final=resp.geturl()
                if urllib.parse.urlsplit(final).hostname!=urllib.parse.urlsplit(url).hostname:
                    raise ValueError("Redirected to another hostname; review manually")
                content=resp.read(250000).decode("utf-8","replace")
            parsed=Metadata()
            parsed.feed(content)
            row["website_title"]=parsed.title.strip()[:180]
            row["theme_colour_candidate"]=parsed.meta.get("theme-color","")[:30]
            row["icon_url_candidate"]=urllib.parse.urljoin(url,parsed.icons[0]) if parsed.icons else ""
            image=parsed.meta.get("og:image","")
            row["image_url_candidate"]=urllib.parse.urljoin(url,image) if image else ""
            row["research_note"]="Metadata candidates only; verify ownership and reuse permission"
        except Exception as error:
            row["research_note"]="Site unavailable or blocked: "+type(error).__name__
    output.append(row)
out=Path("research/nelson-branding-research.csv")
with out.open("w",encoding="utf-8",newline="") as f:
    writer=csv.DictWriter(f,fieldnames=list(output[0]))
    writer.writeheader()
    writer.writerows(output)
print("Branding research queue created for",len(output),"businesses.",flush=True)
print("Official website links must be added to branding tracker before metadata checks.",flush=True)
