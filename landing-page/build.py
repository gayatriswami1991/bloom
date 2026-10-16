#!/usr/bin/env python3
"""Generates index.html (English) and mr.html (Marathi). Copy lives in content.py.
Run:  python3 build.py

Optional images (auto-detected, section is hidden if empty):
  assets/celeb/*.jpg|png|webp   celebrity / cricketer photos already used on the Bloom website
  CELEB_URLS below              or paste direct image URLs from the website
"""
import json, pathlib, urllib.parse
from content import EN, MR, PHONE_DISPLAY, PHONE_TEL, PHONE_WA

# ------------------------------------------------------------- CONFIG
FORM_ENDPOINT = ""   # Zoho / Apps Script / Formspree URL. Empty = result screen shows a 1-tap "Send details on WhatsApp" button.
CELEB_URLS = []      # e.g. ["https://bloomhairtransplant.com/wp-content/uploads/....jpg"]
SITE = "https://bloomhairtransplant.com"
UP = SITE + "/wp-content/uploads/"
LOGO0 = UP + "2025/08/bloom-logo-h.png.webp"
DOCTOR0 = UP + "2025/08/Dr.-Vinod-Sonawane.png.webp"
BA0 = [(UP + "2025/08/Before-%d.jpg.webp" % i, UP + "2025/08/after-%d.jpg.webp" % i) for i in (1, 2, 4, 5)]
HERE = pathlib.Path(__file__).parent
YT = ["Dn2N_gUN1oY", "I_VeRpoS5QI", "U-SsAY2cG7w", "lVhENxRkblw", "EIHWzzx5JyY", "FNbbMlcLFNk"]  # YouTube patient videos used on the Bloom website


def site(url):
    """Use assets/site/<file> (see fetch_site_images.py) when present, else hotlink the website image."""
    local = HERE / "assets" / "site" / url.rsplit("/", 1)[-1]
    return "assets/site/" + local.name if local.exists() else url


LOGO, DOCTOR = site(LOGO0), site(DOCTOR0)
BA = [(site(a), site(z)) for a, z in BA0]



# ------------------------------------------------------------- DIAGRAMS (inline SVG)
def head(extra=""):
    return ('<svg viewBox="0 0 320 200" class="dia" aria-hidden="true"><defs><linearGradient id="gg" x1="0" x2="1"><stop offset="0" stop-color="#e6c477"/><stop offset="1" stop-color="#b98a2e"/></linearGradient></defs>'
            '<path d="M90 170c-10-30-12-70 8-100 18-27 50-38 80-30 36 9 58 40 54 80-2 20-8 35-10 50" fill="none" stroke="#7a6a4c" stroke-width="3" stroke-linecap="round"/>' + extra + '</svg>')
def strands(pts, dx=5, dy=-12):
    return '<g stroke="#e6c477" stroke-width="2.4" stroke-linecap="round">' + "".join('<path d="M%d %d l%d %d"/>' % (x, y, dx, dy) for x, y in pts) + '</g>'
T = 'fill="#e6c477" font-size="11" font-family="sans-serif"'
DIA = {
    "fue": head('<g fill="#e6c477">' + "".join('<circle cx="%d" cy="%d" r="3.2"/>' % p for p in [(110,140),(122,148),(134,152),(116,128),(128,136),(140,140),(104,118),(150,148)]) + '</g>'
                + strands([(176,56),(186,52),(196,50),(206,52),(181,66),(191,62),(201,62)]) + '<path d="M140 128C150 90 160 70 172 62" stroke="#fff" stroke-width="2" fill="none" stroke-dasharray="3 4"/>'
                '<text x="104" y="172" %s>donor</text><text x="170" y="40" %s>recipient</text>' % (T, T)),
    "dhi": head('<g transform="translate(176 52) rotate(-30)"><rect x="0" y="0" width="70" height="14" rx="7" fill="url(#gg)"/><path d="M-2 7h-14" stroke="#e6c477" stroke-width="3" stroke-linecap="round"/></g>'
                + strands([(160,76),(170,80),(150,84)], 4, -11) + '<text x="196" y="32" %s>implanter pen</text>' % T),
    "fut": head('<rect x="104" y="132" width="76" height="12" rx="3" fill="none" stroke="#e6c477" stroke-width="2.5" stroke-dasharray="5 4"/><text x="104" y="166" %s>donor strip</text>' % T
                + strands([(186,56),(196,52),(206,50),(216,52),(191,66),(201,62),(211,62)]) + '<path d="M140 128C150 90 170 70 184 62" stroke="#fff" stroke-width="2" fill="none" stroke-dasharray="3 4"/>'),
    "beard": head('<path d="M118 126q24 40 56 0" fill="none" stroke="#e6c477" stroke-width="3"/>' + strands([(126,130),(136,138),(146,142),(156,142),(166,138),(176,130)], -3, 8)),
    "brow": head('<path d="M110 90q18-14 44-6" fill="none" stroke="#e6c477" stroke-width="5" stroke-linecap="round"/><path d="M178 84q22-8 40 6" fill="none" stroke="#e6c477" stroke-width="5" stroke-linecap="round"/>'),
    "female": head('<path d="M92 120c-20 20-22 50-6 70M232 120c20 20 22 50 6 70" fill="none" stroke="#e6c477" stroke-width="5" stroke-linecap="round"/><path d="M164 44v36" stroke="#e6c477" stroke-width="2.4" stroke-dasharray="3 4"/>'),
    "repair": head('<path d="M120 76q40-36 90 0" fill="none" stroke="#e6c477" stroke-width="3" stroke-dasharray="4 4"/><path d="M118 82q42-26 94 0" fill="none" stroke="#fff" stroke-width="2.4"/><text x="124" y="108" %s>redesign</text>' % T),
}

CSS = r"""
:root{--bg:#fffdf8;--bg2:#f6efe0;--pn:#ffffff;--line:#e6d9ba;--gold:#875f17;--gold2:#c9a24b;--cream:#f6efe0;--tx:#231808;--mut:#6b5d44;--wa:#25d366;--r:22px}
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}
body{font-family:var(--bf);background:var(--bg);color:var(--tx);line-height:1.6;overflow-x:hidden;-webkit-font-smoothing:antialiased}
img,video,svg{max-width:100%;display:block}a{color:inherit;text-decoration:none}h1,h2,h3{font-family:var(--hf);line-height:1.15}
.wrap{max-width:1180px;margin:0 auto;padding:0 20px}section{padding:80px 0;position:relative}
.tag{display:inline-block;color:var(--gold);border:1px solid var(--line);background:rgba(201,162,75,.14);font-weight:600;font-size:12.5px;letter-spacing:.8px;text-transform:uppercase;padding:6px 14px;border-radius:99px;margin-bottom:14px}
.sh{text-align:center;max-width:740px;margin:0 auto 42px}.sh h2{font-size:clamp(28px,4.2vw,44px)}.sh p{color:var(--mut);margin-top:12px;font-size:17px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:9px;font:700 16px var(--bf);padding:15px 26px;border-radius:99px;border:0;cursor:pointer;position:relative;overflow:hidden;transition:transform .2s,box-shadow .2s}
.btn:hover{transform:translateY(-2px)}.btn svg{width:20px;height:20px;flex:none}
.b-gold{background:linear-gradient(135deg,#f3d98f,#c9a24b);color:#231808;box-shadow:0 10px 30px rgba(230,196,119,.28)}
.b-wa{background:var(--wa);color:#04210f;box-shadow:0 10px 30px rgba(37,211,102,.3)}.b-line{border:1.5px solid var(--gold2);color:var(--gold);background:transparent}
.b-gold::after,.b-wa::after{content:"";position:absolute;top:0;left:-80%;width:50%;height:100%;background:linear-gradient(100deg,transparent,rgba(255,255,255,.6),transparent);transform:skewX(-20deg);animation:shine 3.4s infinite}
@keyframes shine{0%,55%{left:-80%}100%{left:140%}}
.pulse{animation:pulse 2s infinite}@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(230,196,119,.55)}70%{box-shadow:0 0 0 16px rgba(230,196,119,0)}100%{box-shadow:0 0 0 0 rgba(230,196,119,0)}}
.top{position:sticky;top:0;z-index:50;background:rgba(255,253,248,.92);backdrop-filter:blur(14px);border-bottom:1px solid var(--line)}
.top .wrap{display:flex;align-items:center;justify-content:space-between;height:66px;gap:10px}.top img{height:40px;width:auto}
.top .ac{display:flex;gap:10px;align-items:center}.top .btn{padding:10px 18px;font-size:14px}.lang{font-size:13.5px;font-weight:700;color:var(--gold);border:1px solid var(--line);padding:8px 13px;border-radius:99px}
.hero{padding:40px 0 70px;overflow:hidden;background:radial-gradient(900px 500px at 10% -10%,rgba(201,162,75,.28),transparent 60%),radial-gradient(700px 500px at 100% 100%,rgba(201,162,75,.16),transparent 60%),var(--bg)}
.hero .g{display:grid;grid-template-columns:1.05fr .95fr;grid-template-areas:"a q" "b q";gap:0 44px;align-items:start}.hc1{grid-area:a}.hc2{grid-area:b}.hero .quiz{grid-area:q}
.eyebrow{display:inline-flex;align-items:center;gap:9px;font-size:13.5px;font-weight:600;color:var(--gold);background:#fff;border:1px solid var(--line);padding:7px 15px;border-radius:99px}
.eyebrow i{width:8px;height:8px;border-radius:50%;background:#2fe38a;animation:blink 1.4s infinite}@keyframes blink{50%{opacity:.25}}
.hero h1{font-size:clamp(34px,5vw,58px);margin:20px 0 16px;letter-spacing:-.5px}.hero h1 .a{display:block;color:var(--tx)}
.hero h1 em{font-style:italic;background:linear-gradient(90deg,#875f17,#c9a24b,#875f17);background-size:200%;-webkit-background-clip:text;background-clip:text;color:transparent;animation:grad 5s linear infinite}
@keyframes grad{to{background-position:200% 0}}
.hero .sub{font-size:18px;color:#5b4a2a;max-width:560px}.hero .sub b{color:#231808}
.ul{list-style:none;margin:22px 0}.ul li{display:flex;gap:11px;margin:10px 0;font-weight:500}.ul li::before{content:"✓";flex:none;width:24px;height:24px;border-radius:50%;background:linear-gradient(135deg,#f3d98f,#c9a24b);color:#231808;display:grid;place-items:center;font-size:13px;font-weight:800;margin-top:2px}
.proof{display:flex;gap:22px;flex-wrap:wrap;margin-top:6px}.proof div{display:flex;flex-direction:column}.proof b{font:800 30px var(--hf);color:var(--gold);line-height:1}.proof span{font-size:13px;color:var(--mut)}
.collage{position:relative;height:210px;margin-top:30px;max-width:520px}
.collage img{position:absolute;border-radius:16px;object-fit:cover;border:3px solid #fff;box-shadow:0 18px 40px rgba(0,0,0,.55);transition:transform .4s}
.collage img:nth-child(1){left:0;top:20px;width:160px;height:170px;transform:rotate(-6deg)}.collage img:nth-child(2){left:150px;top:0;width:190px;height:200px;z-index:2;transform:rotate(2deg)}.collage img:nth-child(3){left:330px;top:24px;width:160px;height:170px;transform:rotate(7deg)}
.collage:hover img{transform:rotate(0) scale(1.04)}
.quiz{background:linear-gradient(180deg,#fffaf0,#f6efe0);color:#231808;border-radius:26px;padding:26px;box-shadow:0 30px 70px rgba(135,95,23,.28),0 0 0 1px rgba(201,162,75,.55);position:relative;scroll-margin-top:90px}
.quiz .hd{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;font-weight:700}.quiz .hd small{color:#7a6a4c;font-weight:600}
.pbar{height:7px;background:#e8dcc0;border-radius:9px;overflow:hidden;margin-bottom:20px}.pbar i{display:block;height:100%;width:25%;background:linear-gradient(90deg,#c9a24b,#875f17);border-radius:9px;transition:width .4s}
.quiz h3{font-size:22px;margin-bottom:14px;font-family:var(--bf);font-weight:800}.quiz h4{font-size:14.5px;margin:14px 0 8px;color:#5b4a2a;font-weight:700}
.step{display:none;animation:in .35s}.step.on{display:block}@keyframes in{from{opacity:0;transform:translateX(18px)}}
.opts{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.op{border:2px solid #e3d4b1;background:#fff;border-radius:16px;overflow:hidden;cursor:pointer;text-align:left;font:600 14px var(--bf);color:#231808;transition:.2s;padding:0}
.op:hover{border-color:#c9a24b;transform:translateY(-2px);box-shadow:0 10px 22px rgba(135,95,23,.18)}.op.sel{border-color:#875f17;background:#fff6dc;box-shadow:0 0 0 3px rgba(201,162,75,.35)}
.op img{width:100%;height:92px;object-fit:cover}.op .e{height:92px;display:grid;place-items:center;background:#f3e6c4;color:#875f17}.op .e svg{width:44px;height:44px}.op span{display:block;padding:9px 11px;line-height:1.3}
.chips{display:flex;flex-wrap:wrap;gap:8px}.chip{padding:10px 16px;border-radius:99px;border:2px solid #e3d4b1;background:#fff;font:600 14px var(--bf);color:#231808;cursor:pointer;transition:.2s}.chip:hover{border-color:#c9a24b}.chip.sel{background:#875f17;border-color:#875f17;color:#fff}
.big{display:grid;gap:10px}.big .op{display:flex;align-items:center;gap:14px;padding:15px 16px}.big .op b{width:44px;height:44px;border-radius:12px;background:#f3e6c4;color:#875f17;display:grid;place-items:center}.big .op b svg{width:24px;height:24px}.big .op span{padding:0;font-size:16px}
.fld{margin-bottom:11px}.fld input,.fld select{width:100%;padding:14px 16px;border:2px solid #e3d4b1;border-radius:13px;font:500 15.5px var(--bf);background:#fff;outline:0;color:#231808}.fld input:focus,.fld select:focus{border-color:#c9a24b;box-shadow:0 0 0 4px rgba(201,162,75,.2)}
.row2{display:grid;grid-template-columns:1fr 1fr;gap:10px}.err{display:none;color:#c0392b;font-size:13px;margin:-3px 0 9px}
.nav{display:flex;gap:10px;margin-top:16px}.nav .btn{flex:1;padding:14px}.nav .back{flex:0 0 auto;background:transparent;color:#7a6a4c;border:2px solid #e3d4b1}
.quiz .b-gold{color:#231808}.quiz .note{font-size:11.5px;color:#7a6a4c;margin-top:10px}
.done{display:none;text-align:center}.done h3{font-size:24px}.done p{color:#5b4a2a;margin:8px 0 16px}.done .btn{width:100%;margin-top:10px}.done small{display:block;color:#7a6a4c;margin-top:4px}
.done .ck{width:68px;height:68px;border-radius:50%;background:linear-gradient(135deg,#2fe38a,#12a85e);color:#fff;display:grid;place-items:center;font-size:34px;margin:0 auto 12px;animation:pop .5s}@keyframes pop{from{transform:scale(.2)}}
.mq{background:linear-gradient(90deg,#c9a24b,#f3d98f,#c9a24b);color:#231808;padding:13px 0;overflow:hidden;white-space:nowrap;font-weight:700}.mq div{display:inline-block;animation:mq 36s linear infinite}.mq span{margin:0 22px}.mq span::before{content:"✦";margin-right:22px}
@keyframes mq{to{transform:translateX(-33.33%)}}
.kg{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.kc{position:relative;border-radius:var(--r);overflow:hidden;aspect-ratio:4/4.4;cursor:pointer;border:1px solid var(--line);background:#000;transform-style:preserve-3d}
.kc img{width:100%;height:100%;object-fit:cover;transition:transform .6s}.kc:hover img{transform:scale(1.08)}
.kc::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 45%,rgba(0,0,0,.88))}
.kc .t{position:absolute;left:0;right:0;bottom:0;z-index:2;padding:18px}.kc{color:#fff}.kc b{display:block;font-size:19px;font-family:var(--bf)}.kc span{color:#f3d98f!important}.kc span{color:var(--gold);font-weight:700;font-size:14px}
.types{background:var(--bg2)}.tt{display:flex;gap:8px;padding-bottom:8px;margin-bottom:24px;justify-content:center;flex-wrap:wrap}
.tt button{padding:11px 20px;border-radius:99px;border:1.5px solid var(--line);background:transparent;color:var(--mut);font:700 15px var(--bf);cursor:pointer;transition:.2s}.tt button.on{background:linear-gradient(135deg,#f3d98f,#c9a24b);color:#231808;border-color:transparent}
.tp{display:none;grid-template-columns:1fr 1fr;gap:30px;align-items:center;background:var(--pn);border:1px solid var(--line);border-radius:28px;padding:28px;animation:in .4s}.tp.on{display:grid}
.tp .vis{position:relative;border-radius:20px;overflow:hidden;background:radial-gradient(circle at 50% 40%,#2a1f0e,#0f0b06);min-height:320px;height:100%;display:grid;place-items:center}
.tp .vis img.ph{width:100%;height:100%;object-fit:cover;position:absolute;inset:0}.tp .vis .dia{position:relative;width:78%;filter:drop-shadow(0 10px 20px rgba(0,0,0,.6))}.tp .vis.has .dia{position:absolute;right:10px;bottom:10px;width:46%;background:rgba(12,9,5,.78);border-radius:14px;padding:6px;border:1px solid var(--line)}
.tp h3{font-size:30px}.tp .full{color:var(--gold);font-weight:600;margin:4px 0 12px}.tp p{color:#5b4a2a}
.tp ol{margin:10px 0 16px;padding-left:0;list-style:none;counter-reset:s}.tp ol li{counter-increment:s;display:flex;gap:12px;margin:9px 0;color:#3b2c12}.tp ol li::before{content:counter(s);flex:none;width:26px;height:26px;border-radius:50%;background:var(--gold);color:#fff;font-weight:800;display:grid;place-items:center;font-size:13px}
.meta{display:grid;gap:8px;margin:14px 0 18px}.meta div{background:#fbf5e6;border:1px solid var(--line);border-radius:12px;padding:10px 14px;font-size:14.5px}.meta b{color:var(--gold);display:block;font-size:12px;letter-spacing:.6px;text-transform:uppercase}
.rj{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.rj figure{position:relative;border-radius:var(--r);overflow:hidden;border:1px solid var(--line);aspect-ratio:1/1.05}.rj img{width:100%;height:100%;object-fit:cover}
.rj figcaption{position:absolute;left:0;right:0;bottom:0;padding:34px 14px 14px;background:linear-gradient(transparent,rgba(0,0,0,.85));font-weight:700;color:#fff}.rj figure:nth-child(3) figcaption{color:#f3d98f}
.rj figure::before{content:attr(data-n);position:absolute;top:12px;left:12px;z-index:2;width:34px;height:34px;border-radius:50%;background:#f3d98f;color:#231808;display:grid;place-items:center;font-weight:800}
.ba-tabs{display:flex;justify-content:center;gap:8px;margin:40px 0 18px}.ba-tabs button{width:42px;height:42px;border-radius:50%;border:1.5px solid var(--line);background:transparent;color:var(--gold);font:700 15px var(--bf);cursor:pointer}.ba-tabs button.on{background:var(--gold);color:#fff}
.ba{position:relative;max-width:520px;margin:0 auto;aspect-ratio:1/1;border-radius:24px;overflow:hidden;box-shadow:0 24px 54px rgba(0,0,0,.6);user-select:none;touch-action:pan-y;cursor:ew-resize;background:#222}
.ba img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}.ba .af{clip-path:inset(0 0 0 50%)}.ba .hd2{position:absolute;top:0;bottom:0;left:50%;width:4px;background:#fff;transform:translateX(-50%)}
.ba .hd2::after{content:"⇄";position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:48px;height:48px;border-radius:50%;background:#fff;color:#875f17;display:grid;place-items:center;font-size:22px;box-shadow:0 6px 18px rgba(0,0,0,.4)}
.ba .lb{position:absolute;top:14px;padding:5px 13px;border-radius:99px;background:rgba(0,0,0,.65);color:#fff;font-size:13px;font-weight:700}.ba .l1{left:14px}.ba .l2{right:14px;background:#c9a24b;color:#231808}
.disc{max-width:660px;margin:20px auto 0;text-align:center;font-size:13px;color:var(--mut)}
.celeb{background:var(--bg2)}.cg{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;max-width:900px;margin:0 auto}.cg img{border-radius:var(--r);aspect-ratio:3/4;object-fit:cover;width:100%;border:1px solid var(--line)}
.yt{position:relative;border-radius:var(--r);overflow:hidden;aspect-ratio:16/9;background:#000;cursor:pointer;border:1px solid var(--line);box-shadow:0 14px 34px rgba(60,40,5,.2)}.yt img,.yt iframe{width:100%;height:100%;object-fit:cover;border:0;display:block}
.yt .pl{position:absolute;inset:0;display:grid;place-items:center;background:linear-gradient(180deg,transparent 40%,rgba(0,0,0,.7))}.yt .pl i{width:66px;height:66px;border-radius:50%;background:#fff;display:grid;place-items:center;color:#875f17;font-size:24px;padding-left:4px;font-style:normal;animation:pulse 2s infinite}.yt .cap{position:absolute;left:14px;bottom:10px;color:#fff;font-weight:600;font-size:14px;z-index:2}
.yg{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.gd{background:linear-gradient(135deg,#c9a24b,#7a5410);color:#fff}.gd .g{display:grid;grid-template-columns:.8fr 1.2fr;gap:44px;align-items:center}
.book{width:min(300px,80%);aspect-ratio:3/4.1;margin:0 auto;border-radius:10px 20px 20px 10px;background:linear-gradient(160deg,#fffaf0,#efe0b8);color:#231808;padding:26px 22px;box-shadow:-14px 18px 40px rgba(0,0,0,.5),inset 6px 0 0 rgba(0,0,0,.1);transform:perspective(900px) rotateY(-14deg);transition:transform .5s;display:flex;flex-direction:column;position:relative;overflow:hidden}
.book:hover{transform:perspective(900px) rotateY(0)}.book img{border-radius:12px;height:44%;object-fit:cover;margin-bottom:14px}.book small{font-weight:700;letter-spacing:1px;color:#875f17;font-size:11px;text-transform:uppercase}.book b{font:800 27px/1.1 var(--hf);margin:4px 0 6px}.book em{font-size:12px;color:#5b4a2a;font-style:normal;margin-top:auto}
.gd h2{font-size:clamp(28px,4vw,42px);margin-bottom:12px}.gd .ul li::before{background:#fff;color:#7a5410}.gd .b-gold{background:#fff;color:#7a5410}.gd .tag{color:#fff;border-color:rgba(255,255,255,.4);background:rgba(255,255,255,.12)}
.doc .g{display:grid;grid-template-columns:.8fr 1.2fr;gap:44px;align-items:center}.doc .ph{border-radius:28px;overflow:hidden;position:relative;box-shadow:0 30px 60px rgba(135,95,23,.3);border:1px solid var(--line);background:linear-gradient(160deg,#e6c477,#7a5410);min-height:320px}
.doc h2{font-size:clamp(28px,4vw,42px);margin-bottom:12px}.doc p{color:#5b4a2a;font-size:17px}
.rs{display:flex;gap:16px;overflow-x:auto;scroll-snap-type:x mandatory;padding:6px 20px 24px;margin:36px -20px 0;scrollbar-width:thin}
.rc{flex:none;width:230px;scroll-snap-align:center;position:relative;border-radius:22px;overflow:hidden;background:#000;aspect-ratio:9/16;box-shadow:0 18px 40px rgba(0,0,0,.6);cursor:pointer;border:1px solid var(--line)}
.rc video,.rc img.p{width:100%;height:100%;object-fit:cover}.rc .pl{position:absolute;inset:0;display:grid;place-items:center;background:linear-gradient(180deg,transparent 45%,rgba(0,0,0,.8));transition:opacity .3s}
.rc .pl i{width:60px;height:60px;border-radius:50%;background:rgba(255,255,255,.93);display:grid;place-items:center;color:#875f17;font-size:22px;padding-left:4px;font-style:normal;animation:pulse 2s infinite}.rc .cap{position:absolute;left:0;right:0;bottom:0;padding:14px;color:#fff;font-weight:600;font-size:13.5px;line-height:1.35}.rc.on .pl{opacity:0;pointer-events:none}
.sg{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;counter-reset:s}.sc{background:var(--pn);border:1px solid var(--line);border-radius:var(--r);padding:30px 22px 22px;position:relative}
.sc::before{counter-increment:s;content:counter(s);position:absolute;top:-19px;left:22px;width:40px;height:40px;border-radius:50%;background:linear-gradient(135deg,#c9a24b,#875f17);color:#fff;font:800 18px var(--bf);display:grid;place-items:center}
.sc h3{font:700 18px var(--bf);margin-bottom:6px}.sc p{color:var(--mut);font-size:15px}
.tl{margin-top:54px;display:grid;grid-template-columns:repeat(4,1fr);position:relative}.tl::before{content:"";position:absolute;top:18px;left:6%;right:6%;height:3px;background:linear-gradient(90deg,transparent,var(--gold2),transparent)}
.tl div{text-align:center;padding:0 10px;position:relative}.tl div::before{content:"";display:block;width:16px;height:16px;border-radius:50%;background:var(--gold);margin:11px auto 14px;box-shadow:0 0 0 6px rgba(201,162,75,.25)}.tl b{display:block;color:var(--gold);font-size:17px}.tl span{color:var(--mut);font-size:14.5px}
.tlh{text-align:center;margin-top:56px;font-size:26px;font-family:var(--bf);font-weight:800}
.rvg{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.rv{background:var(--pn);border:1px solid var(--line);border-radius:var(--r);padding:26px;position:relative}.rv::before{content:"“";position:absolute;top:4px;right:20px;font:700 80px Georgia;color:rgba(201,162,75,.3);line-height:1}
.rv .st{color:#f4b400;letter-spacing:2px;margin-bottom:10px}.rv p{color:#5b4a2a;font-size:15px;font-style:italic}.rv b{display:block;margin-top:14px}.rv small{color:var(--gold);font-weight:600}
.lg{display:grid;grid-template-columns:1fr 1fr;gap:18px}.lc{background:var(--pn);border:1px solid var(--line);border-radius:var(--r);padding:28px}.lc h3{font-size:24px;color:var(--gold);display:flex;align-items:center;gap:8px}.lc h3 svg{width:22px;height:22px}.lc .h{display:flex;align-items:center;gap:8px}.lc .h svg{width:18px;height:18px;color:var(--gold)}.lc p{color:var(--mut);margin:8px 0}.lc .h{color:var(--tx);font-weight:600}.lc .r{display:flex;gap:10px;flex-wrap:wrap;margin-top:14px}.lc .btn{padding:12px 20px;font-size:15px}
.fq{max-width:820px;margin:0 auto}details{background:var(--pn);border:1px solid var(--line);border-radius:16px;margin-bottom:12px}summary{list-style:none;cursor:pointer;padding:19px 56px 19px 22px;font-weight:600;position:relative}summary::-webkit-details-marker{display:none}
summary::after{content:"+";position:absolute;right:22px;top:50%;transform:translateY(-50%);font-size:26px;color:var(--gold);transition:transform .25s}details[open] summary::after{transform:translateY(-50%) rotate(45deg)}details[open]{border-color:var(--gold2)}details p{padding:0 22px 20px;color:var(--mut)}
.end{text-align:center;background:radial-gradient(700px 400px at 50% 0,rgba(201,162,75,.35),transparent 70%),var(--bg2)}.end h2{font-size:clamp(30px,5vw,54px);max-width:800px;margin:0 auto 14px}.end p{color:var(--mut);font-size:18px;margin-bottom:28px}.end .r{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}
footer{padding:34px 0 110px;text-align:center;font-size:13px;color:var(--mut);border-top:1px solid var(--line)}footer a{color:var(--gold);text-decoration:underline}
.sb{display:none;position:fixed;left:0;right:0;bottom:0;z-index:60;background:#fff;border-top:1px solid var(--line);box-shadow:0 -8px 24px rgba(0,0,0,.1);padding:9px 10px calc(9px + env(safe-area-inset-bottom));gap:8px}
.sb a,.sb button{flex:1;display:flex;flex-direction:column;align-items:center;gap:2px;padding:9px 4px;border-radius:14px;border:0;font:700 13px var(--bf);cursor:pointer}.sb svg{width:20px;height:20px}
.sb .c{background:#f6efe0;color:#875f17}.sb .w{background:var(--wa);color:#04210f}.sb .b{background:linear-gradient(135deg,#f3d98f,#c9a24b);color:#231808}
.fab{position:fixed;right:18px;bottom:22px;z-index:55;width:60px;height:60px;border-radius:50%;background:var(--wa);display:grid;place-items:center;animation:p2 2s infinite}@keyframes p2{0%{box-shadow:0 0 0 0 rgba(37,211,102,.55)}70%{box-shadow:0 0 0 18px rgba(37,211,102,0)}100%{box-shadow:0 0 0 0 rgba(37,211,102,0)}}.fab svg{width:32px;height:32px;fill:#fff}
.md{position:fixed;inset:0;background:rgba(0,0,0,.7);z-index:90;display:none;place-items:center;padding:20px;backdrop-filter:blur(5px)}.md.on{display:grid}
.md .bx{background:var(--cream);color:#231808;border-radius:24px;padding:30px;max-width:420px;text-align:center;position:relative;animation:pop .35s}.md h3{font:800 24px var(--bf);margin-bottom:8px}.md p{color:#5b4a2a;margin-bottom:18px}.md .x{position:absolute;right:14px;top:8px;border:0;background:0;font-size:28px;cursor:pointer;color:#7a6a4c}
.rv-up{opacity:0;transform:translateY(34px);transition:opacity .8s,transform .8s}.rv-up.in{opacity:1;transform:none}
.glow{position:fixed;width:340px;height:340px;border-radius:50%;background:radial-gradient(circle,rgba(230,196,119,.12),transparent 65%);pointer-events:none;z-index:0;transform:translate(-50%,-50%)}
@media(max-width:900px){.hero .g{grid-template-areas:"a" "q" "b";gap:22px 0;grid-template-columns:1fr}section{padding:56px 0}.hero{padding-top:26px}.tp.on,.gd .g,.doc .g,.lg{grid-template-columns:1fr}.kg,.rj,.cg{grid-template-columns:1fr 1fr}.yg{grid-template-columns:1fr 1fr}.sg,.tl{grid-template-columns:1fr 1fr;row-gap:34px}.tl::before{display:none}.sb{display:flex}.fab,.glow{display:none}.top .btn.hide-m{display:none}.collage{display:none}.tp{padding:18px}.tp .vis{min-height:240px}.rvg{grid-template-columns:1fr}}
@media(max-width:520px){.top img{height:34px}.kg{gap:10px}.kc b{font-size:15px}.kc .t{padding:12px}.rj{grid-template-columns:1fr}.yg{grid-template-columns:1fr}.sg{grid-template-columns:1fr}.opts{gap:8px}.rc{width:210px}.row2{grid-template-columns:1fr}.quiz{padding:20px 16px}.hero .sub{font-size:16px}}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}.rv-up{opacity:1;transform:none}}
"""

WA = '<svg viewBox="0 0 32 32" fill="currentColor"><path d="M16 3C9 3 3.4 8.6 3.4 15.5c0 2.3.6 4.4 1.7 6.3L3 29l7.4-2c1.8 1 3.8 1.5 5.6 1.5 7 0 12.6-5.6 12.6-12.5S23 3 16 3zm0 22.8c-1.8 0-3.5-.5-5-1.4l-.4-.2-4.4 1.2 1.2-4.3-.3-.4a10 10 0 0 1-1.5-5.3C5.6 9.9 10.3 5.3 16 5.3s10.4 4.6 10.4 10.2S21.7 25.8 16 25.8zm5.7-7.5c-.3-.2-1.8-.9-2.100-1s-.5-.2-.7.2-.8 1-1 1.200-.4.200-.7.1a8.500 8.500 0 0 1-4.200-3.700c-.3-.6.3-.5.9-1.700.1-.2 0-.4 0-.5l-1-2.300c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4s-1 1-1 2.500 1.100 2.900 1.200 3.100c.2.2 2.200 3.400 5.300 4.700 2 .8 2.700.9 3.700.7.6-.1 1.800-.7 2.100-1.400s.3-1.300.2-1.400-.3-.2-.6-.4z"/></svg>'
PH = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M6.6 10.8a15 15 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.400 11.400 0 0 0 3.600.6 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.500a1 1 0 0 1 1 1c0 1.300.2 2.500.6 3.600a1 1 0 0 1-.25 1z"/></svg>'
AS = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.4 6.600L21 9l-5.200 4.300L17.500 20 12 16.300 6.500 20l1.700-6.700L3 9l6.600-.4z"/></svg>'

JS = r"""
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
const track=(e,x={})=>{try{(window.dataLayer=window.dataLayer||[]).push({event:'lp_'+e,lang:CFG.lang,...x});if(window.gtag)gtag('event','lp_'+e,x);if(window.fbq&&e==='lead')fbq('track','Lead')}catch(_){}};
$$('[data-ev]').forEach(a=>a.addEventListener('click',()=>track(a.dataset.ev)));
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.1});
$$('.rv-up').forEach((el,i)=>{el.style.transitionDelay=(i%4)*70+'ms';io.observe(el)});
if(matchMedia('(hover:hover)').matches){const g=$('#glow');addEventListener('mousemove',e=>{g.style.left=e.clientX+'px';g.style.top=e.clientY+'px'});
$$('.tilt').forEach(c=>{c.addEventListener('mousemove',e=>{const r=c.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;c.style.transform=`perspective(800px) rotateY(${x*8}deg) rotateX(${-y*8}deg) translateY(-5px)`});c.addEventListener('mouseleave',()=>c.style.transform='')})}
const Q=$('#quiz'),steps=$$('.step',Q),md=$('#md'),A={concern:'',since:'',age:'',timing:'',prev:CFG.prevDefault};let cur=0;
const show=n=>{cur=n;steps.forEach((s,i)=>s.classList.toggle('on',i===n));$('.pbar i',Q).style.width=((n+1)*25)+'%';$('.hd small',Q).textContent=CFG.stepLabel.replace('{n}',n+1)};
const pick=(el,key,group)=>{$$(group).forEach(x=>x.classList.remove('sel'));el.classList.add('sel');A[key]=el.dataset.v};
$$('[data-q1]',Q).forEach(b=>b.addEventListener('click',()=>{pick(b,'concern','[data-q1]');track('step1',{concern:A.concern});setTimeout(()=>show(1),180)}));
$$('[data-since]',Q).forEach(b=>b.addEventListener('click',()=>pick(b,'since','[data-since]')));
$$('[data-age]',Q).forEach(b=>b.addEventListener('click',()=>pick(b,'age','[data-age]')));
$$('[data-timing]',Q).forEach(b=>b.addEventListener('click',()=>{pick(b,'timing','[data-timing]');track('step3',{timing:A.timing});setTimeout(()=>show(3),180)}));
$$('[data-prev]',Q).forEach(b=>b.addEventListener('click',()=>pick(b,'prev','[data-prev]')));
$('[data-next2]',Q).addEventListener('click',()=>{if(!A.since)A.since=$('[data-since]',Q).dataset.v;if(!A.age)A.age=$('[data-age]',Q).dataset.v;show(2)});
$$('[data-back]',Q).forEach(b=>b.addEventListener('click',()=>show(Math.max(0,cur-1))));
const goQuiz=c=>{if(c){const b=$$('[data-q1]',Q).find(x=>x.dataset.v===c);if(b){pick(b,'concern','[data-q1]');show(1)}}Q.scrollIntoView({behavior:'smooth',block:'center'})};
$$('[data-concern]').forEach(c=>c.addEventListener('click',()=>{track('concern',{concern:c.dataset.concern});goQuiz(c.dataset.concern)}));
$$('[data-go]').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();md.classList.remove('on');goQuiz(a.dataset.goConcern||'')}));
$('#qform').addEventListener('submit',async e=>{e.preventDefault();const f=e.target,phone=f.phone.value.replace(/\D/g,'').replace(/^(91|0)(?=\d{10}$)/,''),err=$('.err',f);
 if(!/^[6-9]\d{9}$/.test(phone)){err.style.display='block';f.phone.focus();return}err.style.display='none';
 const name=f.name.value.trim()||'-',clinic=f.clinic.value,time=f.time.value,p=new URLSearchParams(location.search);
 const data={name,phone,clinic,time,...A,lang:CFG.lang,page:location.href,utm_source:p.get('utm_source')||'',utm_medium:p.get('utm_medium')||'',utm_campaign:p.get('utm_campaign')||'',utm_term:p.get('utm_term')||'',gclid:p.get('gclid')||''};
 track('lead',{concern:A.concern,timing:A.timing});
 const msg=CFG.waMsg.replace('{name}',name).replace('{phone}',phone).replace('{concern}',A.concern).replace('{since}',A.since).replace('{age}',A.age).replace('{timing}',A.timing).replace('{prev}',A.prev).replace('{clinic}',clinic).replace('{time}',time);
 $('#done-wa').href='https://wa.me/'+CFG.waNumber+'?text='+encodeURIComponent(msg);
 $('#done-title').innerHTML=CFG.doneTitle.replace('{name}',name==='-'?'':name);$('#done-sub').innerHTML=CFG.doneSub.replace('{phone}',phone).replace('{time}',time).replace('{clinic}',clinic);
 if(CFG.endpoint){try{await fetch(CFG.endpoint,{method:'POST',mode:'no-cors',headers:{'Content-Type':'text/plain'},body:JSON.stringify(data)})}catch(_){}}
 steps.forEach(s=>s.classList.remove('on'));$('.pbar i',Q).style.width='100%';$('.done',Q).style.display='block';$('.hd small',Q).textContent='✓';Q.scrollIntoView({behavior:'smooth',block:'center'})});
$$('.tt button').forEach(b=>b.addEventListener('click',()=>{$$('.tt button').forEach(x=>x.classList.toggle('on',x===b));$$('.tp').forEach(p=>p.classList.toggle('on',p.id==='tp-'+b.dataset.k))}));
$$('.rc').forEach(c=>c.addEventListener('click',()=>{let v=$('video',c);
 if(!v){$$('.rc video').forEach(o=>{o.pause();o.parentElement.classList.remove('on')});v=document.createElement('video');v.src=c.dataset.v;v.playsInline=true;v.controls=true;v.preload='auto';c.prepend(v);c.classList.add('on');v.play();track('reel',{src:c.dataset.v});v.addEventListener('ended',()=>c.classList.remove('on'));return}
 if(v.paused){$$('.rc video').forEach(o=>{if(o!==v){o.pause();o.parentElement.classList.remove('on')}});c.classList.add('on');v.play()}}));
const ba=$('#ba'),af=$('#ba-a');let drag=false;const setPos=x=>{const r=ba.getBoundingClientRect(),p=Math.max(0,Math.min(1,(x-r.left)/r.width))*100;af.style.clipPath=`inset(0 0 0 ${p}%)`;$('.hd2',ba).style.left=p+'%'};
ba.addEventListener('pointerdown',e=>{drag=true;ba.setPointerCapture(e.pointerId);setPos(e.clientX)});ba.addEventListener('pointermove',e=>{if(drag)setPos(e.clientX)});ba.addEventListener('pointerup',()=>drag=false);
$$('.ba-tabs button').forEach(b=>b.addEventListener('click',()=>{$$('.ba-tabs button').forEach(x=>x.classList.remove('on'));b.classList.add('on');const p=CFG.ba[+b.dataset.i];$('#ba-b').src=p[0];af.src=p[1];setPos(ba.getBoundingClientRect().left+ba.offsetWidth/2)}));
$$('.yt').forEach(y=>y.addEventListener('click',()=>{if(y.dataset.on)return;y.dataset.on=1;y.innerHTML='<iframe src="https://www.youtube-nocookie.com/embed/'+y.dataset.id+'?autoplay=1&rel=0" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen title="Patient story"></iframe>';track('youtube',{id:y.dataset.id})}));
$('.x',md).onclick=()=>md.classList.remove('on');md.addEventListener('click',e=>{if(e.target===md)md.classList.remove('on')});
let shown=0;try{shown=sessionStorage.getItem('xi')}catch(_){}
document.addEventListener('mouseout',e=>{if(!shown&&e.clientY<=0&&innerWidth>900&&$('.done',Q).style.display!=='block'){shown=1;try{sessionStorage.setItem('xi',1)}catch(_){}md.classList.add('on')}});
"""


ICON = {
 "repair": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a4 4 0 0 0-5.4 5.2L3 17.800 6.200 21l6.300-6.300a4 4 0 0 0 5.200-5.400l-2.600 2.600-2.400-.6-.6-2.400z"/></svg>',
 "female": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="9" r="5"/><path d="M12 14v7M9 18h6"/></svg>',
 "now": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 4 14h7l-1 8 9-12h-7z"/></svg>',
 "soon": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>',
 "explore": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.300-4.300"/></svg>',
 "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s7-6.100 7-11a7 7 0 1 0-14 0c0 4.900 7 11 7 11z"/><circle cx="12" cy="10" r="2.500"/></svg>',
 "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
}
def ai(name):
    """Optional AI-generated image slot: assets/ai/<name>.jpg"""
    return "assets/ai/%s.jpg" % name if (HERE / "assets" / "ai" / ("%s.jpg" % name)).exists() else ""


def esc(s):
    return s.replace('"', "&quot;")


def build(t):
    wa_hello = "https://wa.me/%s?text=%s" % (PHONE_WA, urllib.parse.quote(t["wa_hello"]))
    IM = lambda n: "assets/img/%s.jpg" % n
    h = []
    A = h.append
    A('<!doctype html><html lang="%s"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' % t["html_lang"])
    A('<title>%s</title><meta name="description" content="%s"><meta name="robots" content="noindex,follow">' % (t["title"], esc(t["meta"])))
    A('<link rel="alternate" hreflang="en-IN" href="index.html"><link rel="alternate" hreflang="mr-IN" href="mr.html"><meta property="og:title" content="%s"><meta property="og:image" content="assets/img/top2.jpg">' % esc(t["title"]))
    A('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?%s&display=swap" rel="stylesheet">' % t["fonts"])
    A('<style>:root{--bf:%s;--hf:%s}%s</style><!-- Paste GTM / Google Ads / Meta Pixel snippets here --></head><body><div class="glow" id="glow"></div>' % (t["bf"], t["hf"], CSS))
    A('<header class="top"><div class="wrap"><a href="%s"><img src="%s" alt="Bloom Hair Transplant &amp; Skin Care" width="150" height="40"></a><div class="ac"><a class="lang" href="%s">%s</a><a class="btn b-wa hide-m" href="%s" target="_blank" rel="noopener" data-ev="whatsapp">%s WhatsApp</a><a class="btn b-gold" href="tel:%s" data-ev="call">%s %s</a></div></div></header>' % (t["file"], LOGO, t["other_file"], t["lang_label"], wa_hello, WA, PHONE_TEL, PH, t["nav_call"]))
    A('<section class="hero"><div class="wrap g"><div class="hc1"><span class="eyebrow"><i></i>%s</span><h1><span class="a">%s</span> %s</h1><p class="sub">%s</p></div>' % (t["eyebrow"], t["h1a"], t["h1b"], t["sub"]))
    HC2 = ['<div class="hc2"><ul class="ul">']
    for b in t["bullets"]:
        HC2.append("<li>%s</li>" % b)
    HC2.append('</ul><div class="proof"><div><b>%s</b><span>%s</span></div><div><b>%s</b><span>%s</span></div><div><b>%s</b><span>%s</span></div></div>' % (t["trust1"], t["trust1l"], t["trust2"], t["trust2l"], t["trust3"], t["trust3l"]))
    HC2.append('<div class="collage"><img src="%s" alt="Receding hairline before transplant"><img src="%s" alt="Hairline marking at Bloom Hair Transplant"><img src="%s" alt="Crown thinning"></div></div>' % (IM("rec1"), ai("hero") or IM("ba_mark"), IM("crown")))
    A('<div class="quiz" id="quiz"><div class="hd"><span>%s</span><small>%s</small></div><div class="pbar"><i></i></div>' % (t["q_title"], t["q_sub"].replace("{n}", "1")))
    A('<div class="step on"><h3>%s</h3><div class="opts">' % t["q1"])
    for val, lab, img in t["q1opts"]:
        vis = ('<img src="%s" alt="%s">' % (ai(img), esc(lab)) if ai(img) else '<div class="e">%s</div>' % ICON[img]) if img in ("repair", "female") else '<img src="%s" alt="%s">' % (IM(img), esc(lab))
        A('<button type="button" class="op" data-q1 data-v="%s">%s<span>%s</span></button>' % (esc(val), vis, lab))
    A('</div></div><div class="step"><h3>%s</h3><h4>%s</h4><div class="chips">' % (t["q2"], t["q2a"]))
    for o in t["q2aopts"]:
        A('<button type="button" class="chip" data-since data-v="%s">%s</button>' % (esc(o), o))
    A('</div><h4>%s</h4><div class="chips">' % t["q2b"])
    for o in t["q2bopts"]:
        A('<button type="button" class="chip" data-age data-v="%s">%s</button>' % (esc(o), o))
    A('</div><div class="nav"><button type="button" class="btn back" data-back>←</button><button type="button" class="btn b-gold" data-next2>%s →</button></div></div>' % t["q_next"])
    A('<div class="step"><h3>%s</h3><div class="big">' % t["q3"])
    for o, e in t["q3opts"]:
        A('<button type="button" class="op" data-timing data-v="%s"><b>%s</b><span>%s</span></button>' % (esc(o), ICON[e], o))
    A('</div><h4>%s</h4><div class="chips">' % t["q3b"])
    for i, o in enumerate(t["q3bopts"]):
        A('<button type="button" class="chip%s" data-prev data-v="%s">%s</button>' % (" sel" if i == 0 else "", esc(o), o))
    A('</div><div class="nav"><button type="button" class="btn back" data-back>←</button></div></div>')
    A('<div class="step"><h3>%s</h3><p style="font-size:13.5px;color:#7a6a4c;margin:-6px 0 12px">%s</p><form id="qform" novalidate>' % (t["q4"], t["q4sub"]))
    A('<div class="fld"><input name="name" placeholder="%s" autocomplete="name"></div><div class="fld"><input name="phone" type="tel" inputmode="numeric" maxlength="14" placeholder="%s" autocomplete="tel" required></div><div class="err">%s</div>' % (t["f_name"], t["f_phone"], t["f_err"]))
    A('<div class="row2"><div class="fld"><select name="clinic" aria-label="%s">%s</select></div><div class="fld"><select name="time" aria-label="%s">%s</select></div></div>' % (t["f_clinic"], "".join("<option>%s</option>" % c for c in t["clinics_short"]), t["f_time"], "".join("<option>%s</option>" % c for c in t["times"])))
    A('<button class="btn b-gold pulse" style="width:100%%" type="submit">%s</button><p class="note">%s</p><div class="nav"><button type="button" class="btn back" data-back>←</button></div></form></div>' % (t["f_btn"], t["f_consent"]))
    A('<div class="done"><div class="ck">✓</div><h3 id="done-title"></h3><p id="done-sub"></p><a class="btn b-wa" id="done-wa" target="_blank" rel="noopener" data-ev="whatsapp">%s %s</a><small>%s</small><a class="btn b-gold" href="%s" download data-ev="guide">%s</a><a class="btn b-line" style="color:#875f17;border-color:#c9a24b" href="tel:%s" data-ev="call">%s</a></div></div>' % (WA, t["done_wa"], t["done_wa_sub"], t["guide"], t["done_guide"], PHONE_TEL, t["done_call"]))
    A("".join(HC2) + "</div></div></section>")
    m = "".join("<span>%s</span>" % x for x in t["mq"])
    A('<div class="mq" aria-hidden="true"><div>%s%s%s</div></div>' % (m, m, m))
    A('<section><div class="wrap"><div class="sh rv-up"><span class="tag">%s</span><h2>%s</h2><p>%s</p></div><div class="kg">' % (t["k_tag"], t["k_title"], t["k_sub"]))
    for img, ttl, val in t["k_cards"]:
        A('<div class="kc rv-up tilt" data-concern="%s"><img src="%s" alt="%s"><div class="t"><b>%s</b><span>%s →</span></div></div>' % (esc(val), IM(img), esc(ttl), ttl, t["k_cta"]))
    A('</div></div></section><section class="types"><div class="wrap"><div class="sh rv-up"><span class="tag">%s</span><h2>%s</h2><p>%s</p></div><div class="tt">' % (t["t_tag"], t["t_title"], t["t_sub"]))
    for i, ty in enumerate(t["types"]):
        A('<button data-k="%s"%s>%s</button>' % (ty["k"], ' class="on"' if i == 0 else "", ty["name"]))
    A("</div>")
    for i, ty in enumerate(t["types"]):
        src = ai(ty["k"].lower()) or (IM(ty["img"]) if ty["img"] else "")
        has = bool(src)
        photo = '<img class="ph" src="%s" alt="%s">' % (src, esc(ty["full"])) if has else ""
        A('<div class="tp%s" id="tp-%s"><div class="vis%s">%s%s</div><div><h3>%s</h3><div class="full">%s</div><p>%s</p><div class="meta"><div><b>%s</b>%s</div><div><b>%s</b>%s</div></div><b style="color:var(--gold);font-size:12px;letter-spacing:.6px;text-transform:uppercase">%s</b><ol>%s</ol><a class="btn b-gold" href="#quiz" data-go>%s</a></div></div>' % (
            " on" if i == 0 else "", ty["k"], " has" if has else "", photo, DIA[ty["dia"]], ty["name"], ty["full"], ty["d"], t["t_best"], ty["best"], t["t_scar"], ty["scar"], t["t_how"], "".join("<li>%s</li>" % s for s in ty["steps"]), t["t_cta"]))
    A('</div></section><section><div class="wrap"><div class="sh rv-up"><span class="tag">%s</span><h2>%s</h2><p>%s</p></div><div class="rj">' % (t["r_tag"], t["r_title"], t["r_sub"]))
    for i, (img, cap) in enumerate(t["r_steps"]):
        A('<figure class="rv-up" data-n="%d"><img src="%s" alt="%s"><figcaption>%s</figcaption></figure>' % (i + 1, IM(img), cap, cap))
    A('</div><div class="ba-tabs">')
    for i in range(len(BA)):
        A('<button data-i="%d"%s>%d</button>' % (i, ' class="on"' if i == 0 else "", i + 1))
    A('</div><div class="ba" id="ba"><img src="%s" id="ba-b" alt="Before"><img class="af" src="%s" id="ba-a" alt="After"><span class="lb l1">%s</span><span class="lb l2">%s</span><div class="hd2"></div></div><p class="disc">%s</p></div></section>' % (BA[0][0], BA[0][1], t["b_before"], t["b_after"], t["r_disc"]))
    cel = list(CELEB_URLS)
    cd = HERE / "assets" / "celeb"
    if cd.exists():
        cel += ["assets/celeb/" + p.name for p in sorted(cd.iterdir()) if p.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp")]
    if cel:
        A('<section class="celeb"><div class="wrap"><div class="sh rv-up"><span class="tag">%s</span><h2>%s</h2><p>%s</p></div><div class="cg">' % (t["c_tag"], t["c_title"], t["c_sub"]))
        for u in cel:
            A('<img class="rv-up" src="%s" alt="Celebrity hair transplant at Bloom">' % u)
        A('</div><p style="text-align:center;margin-top:26px"><a class="btn b-line" href="%s/services/celebrity-hair-transplant-mumbai/" target="_blank" rel="noopener">%s</a></p></div></section>' % (SITE, t["c_cta"]))
    A('<section class="gd"><div class="wrap g"><div class="rv-up"><div class="book"><img src="%s" alt=""><small>Bloom Hair Transplant</small><b>%s<br>%s</b><em>%s</em></div></div><div class="rv-up"><span class="tag">%s</span><h2>%s</h2><ul class="ul">' % (IM("top2"), t["g_cover1"], t["g_cover2"], t["g_cover3"], t["g_tag"], t["g_title"]))
    for p in t["g_pts"]:
        A("<li>%s</li>" % p)
    A('</ul><a class="btn b-gold pulse" href="#quiz" data-go>%s</a></div></div></section>' % t["g_cta"])
    A('<section class="doc"><div class="wrap"><div class="g"><div class="ph rv-up"><img src="%s" alt="Dr. Vinod Sonawane" width="670" height="838"></div><div class="rv-up"><span class="tag">%s</span><h2>%s</h2><p>%s</p><ul class="ul">' % (DOCTOR, t["d_tag"], t["d_title"], t["d_text"]))
    for p in t["d_pts"]:
        A("<li>%s</li>" % p)
    A('</ul><a class="btn b-gold" href="#quiz" data-go>%s</a></div></div>' % t["d_cta"])
    A('<div class="sh rv-up" style="margin-top:70px;margin-bottom:0"><span class="tag">%s</span><h2>%s</h2><p>%s</p></div><div class="rs">' % (t["v_tag"], t["v_title"], t["v_sub"]))
    for key, cap in t["reels"]:
        A('<div class="rc" data-v="assets/reels/%s.mp4"><img class="p" src="assets/reels/%s.jpg" alt="%s" width="270" height="480"><div class="pl"><i>▶</i></div><div class="cap">%s</div></div>' % (key, key, esc(cap), cap))
    A('</div></div></section><section class="types"><div class="wrap"><div class="sh rv-up"><span class="tag">%s</span><h2>%s</h2></div><div class="sg">' % (t["s_tag"], t["s_title"]))
    for a, b in t["steps"]:
        A('<div class="sc rv-up"><h3>%s</h3><p>%s</p></div>' % (a, b))
    A('</div><div class="tlh rv-up">%s</div><div class="tl" style="margin-top:34px">' % t["tl_title"])
    for a, b in t["timeline"]:
        A('<div class="rv-up"><b>%s</b><span>%s</span></div>' % (a, b))
    A('</div></div></section><section><div class="wrap"><div class="sh rv-up"><span class="tag">%s</span><h2>%s</h2></div><div class="rvg">' % (t["rv_tag"], t["rv_title"]))
    for n, tx in t["reviews"]:
        A('<div class="rv rv-up"><div class="st">★★★★★</div><p>%s</p><b>%s</b><small>Google review</small></div>' % (tx, n))
    A('</div></div></section><section class="types"><div class="wrap"><div class="sh rv-up"><span class="tag">%s</span><h2>%s</h2><p>%s</p></div><div class="yg">' % (t["y_tag"], t["y_title"], t["y_sub"]))
    for i, vid in enumerate(YT):
        A('<div class="yt rv-up" data-id="%s"><img src="https://i.ytimg.com/vi/%s/hqdefault.jpg" alt="%s %d"><div class="pl"><i>▶</i></div><div class="cap">%s %d</div></div>' % (vid, vid, t["y_cap"], i + 1, t["y_cap"], i + 1))
    A('</div></div></section><section><div class="wrap"><div class="sh rv-up"><span class="tag">%s</span><h2>%s</h2></div><div class="lg">' % (t["l_tag"], t["l_title"]))
    for n, addr, mp in t["clinics"]:
        A('<div class="lc rv-up"><h3>%s %s</h3><p>%s</p><p class="h">%s %s</p><div class="r"><a class="btn b-gold" href="tel:%s" data-ev="call">%s %s</a><a class="btn b-line" href="%s" target="_blank" rel="noopener" data-ev="directions">%s</a></div></div>' % (ICON["pin"], n, addr, ICON["clock"], t["hours"], PHONE_TEL, PH, PHONE_DISPLAY, mp, t["directions"]))
    A('</div></div></section><section><div class="wrap"><div class="sh rv-up"><span class="tag">%s</span><h2>%s</h2></div><div class="fq">' % (t["f_tag"], t["f_title"]))
    for q, a in t["faqs"]:
        A('<details class="rv-up"><summary>%s</summary><p>%s</p></details>' % (q, a))
    A('</div></div></section><section class="end"><div class="wrap"><h2 class="rv-up">%s</h2><p class="rv-up">%s</p><div class="r rv-up"><a class="btn b-gold pulse" href="#quiz" data-go>%s</a><a class="btn b-wa" href="%s" target="_blank" rel="noopener" data-ev="whatsapp">%s %s</a><a class="btn b-line" href="tel:%s" data-ev="call">%s %s</a></div></div></section>' % (t["e_title"], t["e_sub"], t["e_start"], wa_hello, WA, t["e_wa"], PHONE_TEL, PH, t["e_call"]))
    A('<footer><div class="wrap"><p>%s</p><p style="margin-top:10px"><a href="%s/privacy-policy/" target="_blank" rel="noopener">%s</a> · <a href="%s" target="_blank" rel="noopener">bloomhairtransplant.com</a></p></div></footer>' % (t["foot"], SITE, t["privacy"], SITE))
    A('<nav class="sb"><a class="c" href="tel:%s" data-ev="call">%s%s</a><a class="w" href="%s" target="_blank" rel="noopener" data-ev="whatsapp">%s%s</a><button class="b" data-go>%s%s</button></nav>' % (PHONE_TEL, PH, t["sb_call"], wa_hello, WA, t["sb_wa"], AS, t["sb_go"]))
    A('<a class="fab" href="%s" target="_blank" rel="noopener" aria-label="WhatsApp" data-ev="whatsapp">%s</a>' % (wa_hello, WA))
    A('<div class="md" id="md"><div class="bx"><button class="x" aria-label="Close">×</button><h3>%s</h3><p>%s</p><a class="btn b-gold" style="width:100%%" href="#quiz" data-go>%s</a></div></div>' % (t["x_title"], t["x_sub"], t["x_cta"]))
    cfg = dict(endpoint=FORM_ENDPOINT, waNumber=PHONE_WA, waMsg=t["wa_msg"], ba=BA, lang=t["lang"], stepLabel=t["q_sub"], doneTitle=t["done_title"], doneSub=t["done_sub"], prevDefault=t["q3bopts"][0])
    A("<script>const CFG=%s;%s</script></body></html>" % (json.dumps(cfg, ensure_ascii=False), JS))
    return "".join(h)


if __name__ == "__main__":
    for t in (EN, MR):
        (HERE / t["file"]).write_text(build(t), encoding="utf-8")
        print("wrote", t["file"])
