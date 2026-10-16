#!/usr/bin/env python3
"""Run this on a machine that can reach bloomhairtransplant.com.
Downloads the website images used by the landing pages into assets/site/ so the pages load them locally
(build.py prefers assets/site/<file> over hotlinking). Afterwards run: python3 build.py"""
import pathlib, urllib.request
UP = "https://bloomhairtransplant.com/wp-content/uploads/"
FILES = ["2025/08/bloom-logo-h.png.webp", "2025/08/Dr.-Vinod-Sonawane.png.webp"]
for i in (1, 2, 4, 5):
    FILES += ["2025/08/Before-%d.jpg.webp" % i, "2025/08/after-%d.jpg.webp" % i]
out = pathlib.Path(__file__).parent / "assets" / "site"
out.mkdir(parents=True, exist_ok=True)
for f in FILES:
    name = f.rsplit("/", 1)[-1]
    try:
        req = urllib.request.Request(UP + f, headers={"User-Agent": "Mozilla/5.0"})
        (out / name).write_bytes(urllib.request.urlopen(req, timeout=30).read())
        print("ok  ", name)
    except Exception as e:
        print("FAIL", name, e)
