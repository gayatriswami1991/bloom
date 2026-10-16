#!/usr/bin/env python3
"""Builds guide-en.pdf and guide-mr.pdf (lead magnet) with headless Chromium. Run: python3 guide.py"""
import pathlib, subprocess, sys, tempfile
HERE = pathlib.Path(__file__).parent.resolve()
CSS = """
@page{size:A4;margin:0}*{box-sizing:border-box;margin:0;padding:0}
body{font-family:%(f)s;color:#231808;font-size:12.5px;line-height:1.55}
.pg{width:210mm;height:297mm;padding:16mm 15mm;position:relative;overflow:hidden;page-break-after:always;background:#fffaf0}
.cover{background:linear-gradient(160deg,#0c0905,#2a1f0e);color:#f4ecdc;padding:0}.cover .in{padding:20mm 16mm}
.cover img.h{width:100%%;height:120mm;object-fit:cover}.cover small{color:#e6c477;letter-spacing:2px;text-transform:uppercase;font-weight:700}
.cover h1{font-family:%(h)s;font-size:44px;line-height:1.1;margin:8px 0 10px;color:#fff}.cover h1 em{color:#e6c477}.cover p{color:#d9cdb2;font-size:14px}
.cover .ft{position:absolute;left:16mm;right:16mm;bottom:14mm;border-top:1px solid #5a4624;padding-top:8px;color:#e6c477;font-weight:600}
h2{font-family:%(h)s;font-size:25px;color:#875f17;margin-bottom:8px}h3{font-size:14px;color:#875f17;margin:12px 0 4px}
.tag{display:inline-block;background:#f8e6c0;color:#875f17;font-weight:700;font-size:10px;letter-spacing:1px;text-transform:uppercase;padding:3px 10px;border-radius:9px;margin-bottom:8px}
table{width:100%%;border-collapse:collapse;margin:8px 0}th{background:#875f17;color:#fff;text-align:left;padding:7px 8px;font-size:11px}td{border-bottom:1px solid #e3d4b1;padding:7px 8px;vertical-align:top;font-size:11.5px}td:first-child{font-weight:700;color:#875f17}
ul{margin:4px 0 6px 16px}li{margin:3px 0}.box{background:#f6efe0;border:1px solid #e3d4b1;border-radius:10px;padding:10px 13px;margin:8px 0}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:12px}.imgs{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin:8px 0}.imgs img{width:100%%;height:85px;object-fit:cover;border-radius:8px}
.foot{position:absolute;left:15mm;right:15mm;bottom:10mm;font-size:9.5px;color:#7a6a4c;border-top:1px solid #e3d4b1;padding-top:5px}
.cl{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:8px}.cl div{background:#fff;border:1px solid #e3d4b1;border-radius:10px;padding:9px 11px;font-size:11px}
"""
L = {
"en": dict(f="Poppins,sans-serif", h="'Playfair Display',serif", file="guide-en.pdf", lang="en",
  c1="The Mumbai", c2="Hair Transplant <em>Guide</em>", c3="Types, candidacy and what affects cost, explained simply.", cs="Bloom Hair Transplant &amp; Skin Care", by="By the team of Dr. Vinod Sonawane · Andheri West &amp; Ghatkopar East, Mumbai",
  p1_t="Types of hair transplant at a glance", p1_s="Which method is used depends on your hair loss, donor supply and goals. Your surgeon decides after examining you.",
  th=["Method", "How it works", "Marks left", "Often considered when"],
  rows=[["FUE", "Follicles are extracted one at a time with a micro-punch and implanted.", "Tiny dot marks in the donor area", "Most men and women, shorter hairstyles, beard and eyebrow work"],
        ["DHI", "Follicles are extracted as in FUE and placed with an implanter pen that sets depth and angle.", "Tiny dot marks in the donor area", "Fine hairline detail and controlled density"],
        ["FUT (strip)", "A thin donor strip is removed, divided into grafts under magnification and implanted.", "A fine linear scar", "Cases needing many grafts where hair is worn longer; suitability decided on examination"]],
  sp="Special areas", sp_l=["<b>Beard &amp; moustache:</b> fills patches and gaps along the natural direction of growth.", "<b>Eyebrow:</b> fine grafts placed at a low angle to rebuild shape and density.", "<b>Female:</b> density-focused planning that respects your natural pattern and parting.", "<b>Repair:</b> corrects an unnatural hairline, poor density, scars or misplaced grafts from an earlier procedure."],
  note="This guide is general information, not medical advice.",
  p2_t="Are you a candidate?", p2_s="A simple checklist. Only an examination can confirm suitability.",
  chk=["Your hair loss pattern is stable or has been assessed by a doctor", "You have a healthy donor area (usually back and sides of the scalp)", "You are generally above 21 years of age", "You are in good general health", "Your expectations are realistic about density and coverage", "You can follow aftercare instructions for the first weeks"],
  cost_t="What affects the cost", cost=["Number of grafts needed", "Technique used (FUE, DHI, FUT)", "Surgeon&rsquo;s expertise and who performs each step", "Complexity, e.g. repair or scar correction", "Clinic location"],
  cost_n="At Bloom, transplant costs are commonly quoted in the range of about ₹30,000 to ₹1,50,000 or more. You receive a personalised estimate after your scalp assessment.",
  tl_t="Typical growth timeline", tl=[("2–3 weeks", "Temporary shedding (normal)"), ("3–4 months", "New growth begins"), ("6 months", "Noticeable improvement"), ("9–12 months", "Full natural result")],
  p3_t="10 questions to ask any clinic", qs=["Who designs my hairline: the doctor or a technician?", "Who performs extraction and implantation?", "How many grafts do I realistically need, and why?", "Which technique suits me, and what are the alternatives?", "How much donor hair is available, and what is the safe limit?", "What will the total cost include, and are there extra charges?", "What marks will the donor area have?", "What does recovery look like week by week?", "What is the follow-up plan, and who do I contact with concerns?", "Can I see before-and-after cases similar to mine, with the dates?"],
  vis="Visit us", clin=[("Andheri West", "Ground Floor, Panchavati, Versova Marg, opp. Apna Bazar Road, next to D.N. Nagar Metro Station, Andheri West, Mumbai 400058"), ("Ghatkopar East", "1st Floor, Nand Ashish, 102, R.B. Mehta Marg, above Natural Ice Cream, Ghatkopar East, Mumbai 400077")],
  call="Call +91 80970 00044 · Mon–Sat, 10 AM – 8 PM · bloomhairtransplant.com", disc="Results vary from person to person. A consultation and examination are required before any procedure."),
"mr": dict(f="'Noto Sans Devanagari',sans-serif", h="'Noto Sans Devanagari',sans-serif", file="guide-mr.pdf", lang="mr",
  c1="मुंबई", c2="हेअर ट्रान्सप्लांट <em>गाईड</em>", c3="प्रकार, पात्रता आणि खर्चावर परिणाम करणाऱ्या गोष्टी, सोप्या भाषेत.", cs="ब्लूम हेअर ट्रान्सप्लांट &amp; स्किन केअर", by="डॉ. विनोद सोनावणे यांच्या टीमकडून · अंधेरी वेस्ट &amp; घाटकोपर ईस्ट, मुंबई",
  p1_t="हेअर ट्रान्सप्लांटचे प्रकार, एका नजरेत", p1_s="कोणती पद्धत वापरायची हे तुमची केस गळती, डोनर साठा आणि अपेक्षा यावर अवलंबून असते. तपासणीनंतर सर्जन ते ठरवतात.",
  th=["पद्धत", "कसे चालते", "खुणा", "केव्हा विचारात घेतली जाते"],
  rows=[["FUE", "मायक्रो-पंचने एकेक फॉलिकल काढून लावले जातात.", "डोनर भागात बारीक ठिपक्यासारख्या खुणा", "बहुतेक पुरुष आणि महिला, छोटे केस, दाढी आणि भुवयांसाठी"],
        ["DHI", "FUE प्रमाणे फॉलिकल्स काढले जातात आणि इम्प्लांटर पेनने खोली व कोन ठरवून लावले जातात.", "डोनर भागात बारीक ठिपक्यासारख्या खुणा", "सूक्ष्म हेअरलाइन आणि नियंत्रित दाटपणा"],
        ["FUT (पट्टी)", "डोनर भागातून पातळ पट्टी काढून भिंगाखाली ग्राफ्ट्समध्ये विभागून लावली जाते.", "बारीक रेषेसारखी खूण", "जास्त ग्राफ्ट्स लागणारे आणि केस मोठे ठेवणारे रुग्ण; योग्यता तपासणीनंतर"]],
  sp="विशेष भाग", sp_l=["<b>दाढी &amp; मिशी:</b> नैसर्गिक दिशेने रिकाम्या जागा भरल्या जातात.", "<b>भुवया:</b> आकार आणि दाटपणा परत आणण्यासाठी कमी कोनात बारीक ग्राफ्ट्स लावले जातात.", "<b>महिला:</b> तुमचा नैसर्गिक पॅटर्न आणि भांग जपून दाटपणावर भर देणारे नियोजन.", "<b>रिपेअर:</b> आधीच्या प्रक्रियेतील अनैसर्गिक हेअरलाइन, कमी दाटपणा, व्रण किंवा चुकीच्या जागी लावलेले ग्राफ्ट्स दुरुस्त केले जातात."],
  note="हे गाईड सर्वसाधारण माहिती आहे, वैद्यकीय सल्ला नाही.",
  p2_t="तुम्ही पात्र आहात का?", p2_s="सोपी चेकलिस्ट. योग्यता फक्त तपासणीनंतरच ठरते.",
  chk=["तुमची केस गळती स्थिर आहे किंवा डॉक्टरांनी तपासली आहे", "निरोगी डोनर भाग आहे (साधारणपणे डोक्याचा मागचा आणि बाजूचा भाग)", "साधारण २१ वर्षांवरील वय", "सर्वसाधारण आरोग्य चांगले आहे", "दाटपणा आणि कव्हरेजबद्दल अपेक्षा वास्तववादी आहेत", "पहिल्या आठवड्यांत काळजीच्या सूचना पाळता येतील"],
  cost_t="खर्चावर काय परिणाम करते", cost=["लागणाऱ्या ग्राफ्ट्सची संख्या", "वापरलेले तंत्र (FUE, DHI, FUT)", "सर्जनचा अनुभव आणि प्रत्येक टप्पा कोण करतो", "गुंतागुंत, उदा. रिपेअर किंवा व्रण सुधारणा", "क्लिनिकचे ठिकाण"],
  cost_n="ब्लूममध्ये ट्रान्सप्लांटचा खर्च साधारणपणे ₹३०,००० ते ₹१,५०,००० किंवा त्याहून जास्त सांगितला जातो. स्कॅल्प तपासल्यानंतर तुम्हाला वैयक्तिक अंदाज मिळतो.",
  tl_t="केस वाढीचा सर्वसाधारण कालावधी", tl=[("२–३ आठवडे", "तात्पुरती गळती (सामान्य)"), ("३–४ महिने", "नवीन केस उगवू लागतात"), ("६ महिने", "लक्षात येणारा फरक"), ("९–१२ महिने", "पूर्ण नैसर्गिक निकाल")],
  p3_t="कोणत्याही क्लिनिकला विचारायचे १० प्रश्न", qs=["माझी हेअरलाइन कोण डिझाइन करणार: डॉक्टर की टेक्निशियन?", "फॉलिकल्स काढण्याचे आणि लावण्याचे काम कोण करणार?", "मला खरंच किती ग्राफ्ट्स लागतील आणि का?", "माझ्यासाठी कोणते तंत्र योग्य आणि पर्याय कोणते?", "किती डोनर केस उपलब्ध आहेत आणि सुरक्षित मर्यादा काय?", "एकूण खर्चात काय समाविष्ट आहे आणि जादा शुल्क आहे का?", "डोनर भागात कोणत्या खुणा राहतील?", "आठवड्या-आठवड्याने रिकव्हरी कशी असते?", "फॉलो-अप योजना काय आणि शंका असल्यास कुणाशी संपर्क करायचा?", "माझ्यासारख्या केसचे आधी-नंतरचे निकाल (तारखांसह) पाहता येतील का?"],
  vis="आम्हाला भेटा", clin=[("अंधेरी वेस्ट", "ग्राउंड फ्लोअर, पंचवटी, वर्सोवा मार्ग, अपना बाजार रोडसमोर, डी.एन. नगर मेट्रो स्टेशनजवळ, अंधेरी वेस्ट, मुंबई ४०००५८"), ("घाटकोपर ईस्ट", "पहिला मजला, नंद आशिष, १०२, आर.बी. मेहता मार्ग, नॅचरल आईस्क्रीमच्या वर, घाटकोपर ईस्ट, मुंबई ४०००७७")],
  call="कॉल करा +91 80970 00044 · सोम–शनि, सकाळी १० ते रात्री ८ · bloomhairtransplant.com", disc="निकाल प्रत्येक व्यक्तीनुसार वेगळे असतात. कोणतीही प्रक्रिया करण्यापूर्वी सल्ला आणि तपासणी आवश्यक आहे."),
}
def page(t):
    im = "assets/img/"
    rows = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in r) for r in t["rows"])
    return """<!doctype html><html lang="%(lang)s"><head><meta charset="utf-8"><style>%(css)s</style></head><body>
<div class="pg cover"><img class="h" src="%(im)stop2.jpg"><div class="in"><small>%(cs)s</small><h1>%(c1)s<br>%(c2)s</h1><p>%(c3)s</p></div><div class="ft">%(by)s</div></div>
<div class="pg"><span class="tag">1</span><h2>%(p1_t)s</h2><p>%(p1_s)s</p><table><tr>%(th)s</tr>%(rows)s</table>
<div class="imgs"><img src="%(im)sdonor.jpg"><img src="%(im)sstrand.jpg"><img src="%(im)sbeard1.jpg"></div><h3>%(sp)s</h3><ul>%(sp_l)s</ul><div class="box">%(note)s</div><div class="foot">%(disc)s</div></div>
<div class="pg"><span class="tag">2</span><h2>%(p2_t)s</h2><p>%(p2_s)s</p><ul style="margin-top:8px">%(chk)s</ul>
<div class="g2"><div><h3>%(cost_t)s</h3><ul>%(cost)s</ul></div><div class="box">%(cost_n)s</div></div>
<h3>%(tl_t)s</h3><div class="cl" style="grid-template-columns:repeat(4,1fr)">%(tl)s</div>
<div class="imgs" style="margin-top:12px"><img src="%(im)scase-before.jpg"><img src="%(im)scase-design.jpg"><img src="%(im)scase-result.jpg"></div><div class="foot">%(disc)s</div></div>
<div class="pg"><span class="tag">3</span><h2>%(p3_t)s</h2><ol style="margin:8px 0 0 18px">%(qs)s</ol>
<h3 style="margin-top:16px">%(vis)s</h3><div class="cl">%(clin)s</div><div class="box" style="margin-top:14px;font-weight:700;color:#875f17">%(call)s</div><div class="foot">%(disc)s</div></div>
</body></html>""" % dict(t, css=CSS % t, im=im, rows=rows, th="".join("<th>%s</th>" % c for c in t["th"]), sp_l="".join("<li>%s</li>" % x for x in t["sp_l"]),
        chk="".join("<li>☐ %s</li>" % x for x in t["chk"]), cost="".join("<li>%s</li>" % x for x in t["cost"]),
        tl="".join("<div><b style='color:#875f17'>%s</b><br>%s</div>" % x for x in t["tl"]), qs="".join("<li style='margin:6px 0'>%s</li>" % x for x in t["qs"]),
        clin="".join("<div><b style='color:#875f17'>%s</b><br>%s</div>" % x for x in t["clin"]))
def find_chrome():
    import glob, shutil
    for c in ["chromium", "chromium-browser", "google-chrome"]:
        if shutil.which(c): return shutil.which(c)
    g = glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome")
    if g: return g[0]
    sys.exit("Chrome/Chromium not found")
def main():
    chrome = find_chrome()
    for k, t in L.items():
        f = HERE / ("_guide_%s.html" % k); f.write_text(page(t), encoding="utf-8")
        subprocess.run([chrome, "--headless=new", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=4000",
                        "--print-to-pdf=" + str(HERE / t["file"]), f.as_uri()], check=True, capture_output=True)
        f.unlink(); print("wrote", t["file"])
if __name__ == "__main__":
    main()
