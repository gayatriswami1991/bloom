# Bloom Hair Transplant: ad landing pages (developer handoff)

Two static pages, no framework, no build step needed to deploy.

| File | Purpose |
|---|---|
| `index.html` | English landing page |
| `mr.html` | Marathi landing page |
| `guide-en.pdf`, `guide-mr.pdf` | Lead-magnet PDFs (direct download, no form) |
| `assets/source/` | Source material: all reel frames and website screenshots (not loaded by the pages) |
| `assets/img/` | Photos (frames from Bloom's reels), `logo.png`, `assets/reels/` reel clips + posters, `assets/celeb/` award/event photos |
| `share/` | Single-file builds with everything embedded (for emailing / previews) |

## Deploy
1. Upload the whole folder (keep `assets/` and the PDFs next to the HTML) to any static host or a subfolder of the WordPress site, e.g. `https://bloomhairtransplant.com/lp/`.
2. Point ads to `/lp/` (English) or `/lp/mr.html` (Marathi).
3. Optional but recommended: run `python3 fetch_site_images.py` on a machine that can reach bloomhairtransplant.com, then `python3 build.py`. It stores the logo, doctor photo and before/after pairs locally in `assets/site/`; otherwise they hotlink from the website.

## Things to configure (top of `build.py`)
- `FORM_ENDPOINT` — leads from the 4-step quiz. Empty = the result screen shows a "Send details on WhatsApp" button (WhatsApp prefilled). Set a URL (Zoho Flow / Apps Script / Formspree / your API) and the quiz POSTs JSON (`text/plain`, `no-cors`): `name, phone, clinic, time, concern, since, age, timing, prev, lang, page, utm_source, utm_medium, utm_campaign, utm_term, gclid`.
- `BASE_URL` — empty keeps the pages `noindex` (safe for ads). Set the final folder URL (with trailing slash) to make them indexable with canonical, hreflang and absolute Open Graph URLs.
- `CELEB_URLS` / `assets/celeb/` — award/event photos. `assets/ai/{repair,female,eyebrow,hero}.jpg` are optional image slots.
- Phone/WhatsApp number: `content.py` (`PHONE_*`). All visible copy (English + Marathi): `content.py`.

## Editing
Do not hand-edit the HTML. Change `content.py` / `build.py`, then run:
```
python3 build.py     # index.html + mr.html
python3 guide.py     # PDFs (needs Chromium/Chrome installed)
python3 share.py     # single-file builds in share/
```
Python 3 standard library only (no pip installs).

## Tracking
Paste GTM / Google Ads / Meta Pixel snippets at the marked comment in `<head>` (both HTML files, or in `build.py`). Events are pushed to `dataLayer` and, when present, `gtag`/`fbq`:
`lp_call, lp_whatsapp, lp_directions, lp_step1, lp_step3, lp_concern, lp_lead (fires fbq Lead), lp_guide, lp_reel, lp_youtube`. Each carries `lang`.
Mark `lp_lead` as the Google Ads conversion.

## Third-party requests
Google Fonts (Poppins, Playfair Display, Noto Sans Devanagari), YouTube thumbnails/embeds (`i.ytimg.com`, `youtube-nocookie.com`), and website-hosted images (`bloomhairtransplant.com/wp-content/uploads/...`) unless `assets/site/` is populated.

## Known limits / to confirm with the client
- Facts shown on the page: 4.9 rating / 407 reviews, cost range ₹30,000–₹1,50,000, clinic addresses and hours, "Iconic Hair Transplant Surgeon (Mid-Day)". Verify before spending on ads. No "success rate" or urgency claims are used.
- Award/event photos feature public figures: get the client's confirmation they may be used in advertising.
- Marathi copy should be proofread by a native speaker.
- Photos in `assets/img` are frames taken from Instagram reels and are low resolution; replace with originals when available (same filenames).
