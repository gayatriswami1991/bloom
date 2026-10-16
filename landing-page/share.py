#!/usr/bin/env python3
"""Builds single-file versions (share/*.html) with every local image, the guide PDF and short reel clips embedded,
so the file can be e-mailed / sent on WhatsApp and still show everything. Run after build.py:  python3 share.py
Website-hosted images (logo, doctor, before/after) and YouTube thumbnails still need internet, unless you ran fetch_site_images.py first."""
import base64, pathlib, re
HERE = pathlib.Path(__file__).parent
out = HERE / "share"; out.mkdir(exist_ok=True)
def b64(p, mime): return "data:%s;base64,%s" % (mime, base64.b64encode(p.read_bytes()).decode())
MIME = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp", ".pdf": "application/pdf", ".mp4": "video/mp4"}
for src, name in (("index.html", "Bloom_Landing_English.html"), ("mr.html", "Bloom_Landing_Marathi.html")):
    h = (HERE / src).read_text(encoding="utf-8")
    def sub(m):
        rel = m.group(2)
        if rel.startswith("assets/reels/") and rel.endswith(".mp4"):
            rel = rel.replace("assets/reels/", "assets/reels/small/")
        p = HERE / rel
        return m.group(1) + b64(p, MIME[p.suffix.lower()]) + m.group(3) if p.exists() else m.group(0)
    h = re.sub(r'((?:src|href|data-v)=")(assets/[^"]+\.(?:jpg|jpeg|png|webp|mp4))(")', sub, h)
    h = re.sub(r'(href=")(guide-(?:en|mr)\.pdf)(")', lambda m: m.group(1) + b64(HERE / m.group(2), "application/pdf") + m.group(3), h)
    h = h.replace('<link rel="preload" as="image" href="assets/img/rec1.jpg" fetchpriority="high">', "")
    (out / name).write_text(h, encoding="utf-8")
    print(name, round((out / name).stat().st_size / 1e6, 1), "MB")
