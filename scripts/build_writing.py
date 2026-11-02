"""Rebuild the Writing section of index.html from Substack and LinkedIn.

Substack posts are read from the publication's RSS feed and cached in
writing/substack.json, so a failed fetch never empties the section.
LinkedIn has no public feed, so its posts are listed by hand in
writing/linkedin.json.

The section is written between the markers <!-- writing:start --> and
<!-- writing:end --> in index.html. Standard library only.
"""
import html
import json
import pathlib
import sys
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from datetime import date

ROOT = pathlib.Path(__file__).resolve().parent.parent
FEED = "https://soulbench.substack.com/feed"
PUBLICATION = "https://soulbench.substack.com"
CACHE = ROOT / "writing" / "substack.json"
LINKEDIN = ROOT / "writing" / "linkedin.json"
PAGE = ROOT / "index.html"
START, END = "<!-- writing:start -->", "<!-- writing:end -->"


def fetch_substack():
    req = urllib.request.Request(FEED, headers={"User-Agent": "Mozilla/5.0 (site build; +https://anagh-sinha.github.io)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        root = ET.fromstring(r.read())
    posts = []
    for item in root.iter("item"):
        link = (item.findtext("link") or "").split("?")[0]
        posts.append({
            "source": "Substack",
            "title": (item.findtext("title") or "").strip(),
            "summary": (item.findtext("description") or "").strip(),
            "date": parsedate_to_datetime(item.findtext("pubDate")).date().isoformat(),
            "url": link,
        })
    return posts


def load(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def render(posts):
    esc = html.escape
    out = []
    for p in posts:
        d = date.fromisoformat(p["date"])
        when = f'{d.strftime("%B %Y")}<br>{esc(p["source"])}'
        summary = f'\n        <p class="venue">{esc(p["summary"])}</p>' if p.get("summary") else ""
        out.append(f'''    <article class="entry">
      <p class="entry-when">{when}</p>
      <div class="entry-body">
        <h3><a href="{esc(p["url"])}">{esc(p["title"])}</a></h3>{summary}
      </div>
    </article>''')
    return "\n".join(out)


def main():
    try:
        substack = fetch_substack()
        CACHE.parent.mkdir(exist_ok=True)
        CACHE.write_text(json.dumps(substack, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    except Exception as e:  # keep the last good copy
        print(f"Substack fetch failed, using cache: {e}", file=sys.stderr)
        substack = load(CACHE)

    linkedin = [dict(p, source="LinkedIn") for p in load(LINKEDIN) if p.get("url") and p.get("title") and p.get("date")]
    posts = sorted(substack + linkedin, key=lambda p: p["date"], reverse=True)

    page = PAGE.read_text(encoding="utf-8")
    a, b = page.index(START) + len(START), page.index(END)
    page = page[:a] + "\n" + render(posts) + "\n    " + page[b:]
    PAGE.write_text(page, encoding="utf-8")
    print(f"{len(substack)} Substack, {len(linkedin)} LinkedIn")


if __name__ == "__main__":
    main()
