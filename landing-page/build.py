#!/usr/bin/env python3
"""Generates index.html (English) and mr.html (Marathi) from one template.
Run:  python3 build.py
Edit the CONFIG block and the EN / MR dictionaries, then re-run."""
import json, pathlib

# ---------------------------------------------------------------- CONFIG
PHONE_DISPLAY = "+91 80970 00044"
PHONE_TEL = "+918097000044"
PHONE_WA = "918097000044"
FORM_ENDPOINT = ""   # e.g. a Zoho/Formspree/Apps Script URL. Empty = quick form opens WhatsApp with the details prefilled.
ZOHO_FORM = "https://forms.zohopublic.in/bloomhairtransplant1/form/BookYourConsultation/formperma/oGIl60Cie5njgdi2Z-ryDX5HqUU9ZcPz86OTdnu6OfY"
SITE = "https://bloomhairtransplant.com"
UP = SITE + "/wp-content/uploads/"
MAP_ANDHERI = "https://www.google.com/maps/search/?api=1&query=Bloom+Hair+Transplant+Andheri+West+Mumbai"
MAP_GHATKOPAR = "https://www.google.com/maps/search/?api=1&query=Bloom+Hair+Transplant+Ghatkopar+East+Mumbai"

IMG = {
    "logo": UP + "2025/08/bloom-logo-h.png.webp",
    "hero": UP + "2025/08/carousel-4.png.webp",
    "doctor": UP + "2025/08/Dr.-Vinod-Sonawane.png.webp",
    "ba": [(UP + "2025/08/Before-1.jpg.webp", UP + "2025/08/after-1.jpg.webp"),
           (UP + "2025/08/Before-2.jpg.webp", UP + "2025/08/after-2.jpg.webp"),
           (UP + "2025/08/Before-4.jpg.webp", UP + "2025/08/after-4.jpg.webp"),
           (UP + "2025/08/Before-5.jpg.webp", UP + "2025/08/after-5.jpg.webp")],
}

# ---------------------------------------------------------------- COPY
EN = dict(
    lang="en", html_lang="en-IN", file="index.html", other_file="mr.html", other_label="मराठी",
    fonts="family=Poppins:wght@400;500;600;700&family=Playfair+Display:wght@600;700;800",
    body_font="'Poppins',sans-serif", head_font="'Playfair Display',serif",
    title="Hair Transplant in Mumbai | Dr. Vinod Sonawane | Bloom Hair Transplant",
    meta="Doctor-led hair transplant in Andheri West & Ghatkopar East, Mumbai. FUE, beard, eyebrow, female and repair procedures. Call or WhatsApp Bloom Hair Transplant for a consultation.",
    nav_call="Call Now", nav_wa="WhatsApp",
    badge="Andheri West &amp; Ghatkopar East, Mumbai",
    h1="Hair Transplant in Mumbai", h1em="that looks like your own hair.",
    sub="Planned and led by <b>Dr. Vinod Sonawane</b>. A personalised hairline, honest advice on how many grafts you really need, and a clear estimate at your consultation.",
    rating="4.9 Google rating", reviews="407 reviews",
    cta_call="Call " + PHONE_DISPLAY, cta_wa="WhatsApp Us",
    form_title="Get a Call Back", form_sub="Tell us a little. Our team will call you during clinic hours.",
    f_name="Your name", f_phone="Mobile number", f_concern="What is your concern?",
    concerns=["Receding hairline / baldness", "Crown thinning", "Unhappy with a previous transplant", "Beard / moustache / eyebrow", "Female hair thinning", "Not sure, need advice"],
    f_btn="Request Callback", f_note="Clinic hours: Mon–Sat, 10 AM – 8 PM. Your details are used only to contact you about your enquiry.",
    f_err="Please enter a valid 10-digit mobile number.",
    f_ok_title="Thank you!", f_ok_text="We have your request. For a faster reply, call or message us now.",
    wa_msg="Hello Bloom Hair Transplant, I would like a consultation.\nName: {name}\nPhone: {phone}\nConcern: {concern}",
    marquee=["FUE Hair Transplant", "Beard Transplant", "Eyebrow Reconstruction", "Female Hair Transplant", "Hair Transplant Repair", "Crown & Hairline", "Moustache Transplant", "Body Hair Transplant"],
    s_counts=[("4.9", "Google rating", 1), ("407", "Google reviews", 0), ("2", "Clinics in Mumbai", 0), ("15", "Specialised treatments", 0)],
    p_tag="Is this you?", p_title="Which of these sounds familiar?", p_sub="Tap your concern. We will pre-fill it in your request.",
    p_cards=[("📉", "Receding hairline", "Receding hairline / baldness", "A hairline designed for your face, not a template."),
             ("🌀", "Thinning at the crown", "Crown thinning", "Realistic planning for crown coverage and density."),
             ("🛠️", "Unhappy with a past transplant", "Unhappy with a previous transplant", "Unnatural hairline, low density or scars? Repair is a speciality here."),
             ("🧔", "Beard, moustache or eyebrow", "Beard / moustache / eyebrow", "Fuller facial hair with natural direction and angle."),
             ("👩", "Female hair thinning", "Female hair thinning", "Gentle, density-focused planning for women."),
             ("🤔", "Low donor hair?", "Not sure, need advice", "Beard or body hair can sometimes help. We assess before we promise.")],
    p_cta="Check my options",
    links_title="Explore treatments",
    links=[("Male Hair Transplant", "male-hair-transplant-in-mumbai"), ("Female Hair Transplant", "female-hair-transplant"), ("FUE Hair Transplant", "fue-hair-transplant-in-mumbai"),
           ("Beard Transplant", "beard-hair-transplant-in-mumbai"), ("Eyebrow Reconstruction", "eyebrow-reconstruction-in-mumbai"), ("Hair Transplant Repair", "hair-transplant-repair-in-mumbai")],
    d_tag="Your surgeon", d_title="Meet Dr. Vinod Sonawane",
    d_text="Dr. Sonawane leads every case at Bloom, from hairline design to graft planning. He is recognised as an &ldquo;Iconic Hair Transplant Surgeon&rdquo; by Mid-Day and is known for natural-looking results and for correcting failed transplants.",
    d_pts=["Doctor-led planning, not a sales counter", "Custom hairline for your face and age", "Honest graft numbers and realistic expectations", "Specialist in repairing previous transplants"],
    d_cta="Talk to Dr. Sonawane&rsquo;s team",
    r_tag="Watch &amp; learn", r_title="Straight answers from the doctor", r_sub="Short reels from Bloom. Tap to play.",
    reels=[("reel5", "A real result, start to finish"), ("reel1", "Dr. Sonawane: what makes a transplant look natural"), ("reel6", "Can grey hair be transplanted?"), ("reel3", "Not enough scalp donor hair? Beard hair may help"), ("reel2", "Donor hair and planning (in Marathi)")],
    b_tag="Real patients", b_title="Before &amp; after", b_sub="Drag the handle to compare.", b_before="Before", b_after="After",
    b_disc="Results shown are from individual patients. Outcomes vary with hair type, donor supply, age and aftercare. A consultation is needed to know what is realistic for you.",
    rp_tag="Repair specialists", rp_title="Unhappy with a previous hair transplant?",
    rp_text="A poorly planned transplant can leave an unnatural hairline, low density, visible scars or a &ldquo;pluggy&rdquo; look. Bloom assesses your donor area, scars and graft placement, then plans a correction that restores balance.",
    rp_pts=["Unnatural, straight hairline", "Thin or uneven density", "Visible scarring", "Over-harvested donor area", "Poor or failed growth"], rp_cta="Get my repair assessed",
    st_tag="How it works", st_title="Four simple steps",
    steps=[("Call or WhatsApp", "Tell us your concern. We book a time at Andheri West or Ghatkopar East."), ("Scalp assessment", "Dr. Sonawane&rsquo;s team studies your hair loss pattern and donor area."), ("Personal plan", "Hairline design, graft estimate and a clear cost discussion. No pressure."), ("Procedure &amp; follow-up", "Done under local anaesthesia, with guidance for recovery and follow-ups.")],
    t_tag="What to expect", t_title="Your hair growth timeline",
    timeline=[("2–3 weeks", "Temporary shedding. This is normal."), ("3–4 months", "New hair growth begins."), ("6 months", "Noticeable improvement."), ("9–12 months", "Full, natural-looking result.")],
    rv_tag="Google reviews", rv_title="What patients say",
    reviews_list=[("Deepak Chandramohan", "I had done my hair transplant 10 months back and have got amazing natural results. Nobody can guess I have got a hair transplant. I would highly recommend to visit the clinic and speak with Dr Sonawane."),
                  ("Rajan Pillai", "The consultation provided by the Doctor was genuine and realistic. Doctor and their experienced technician took good care during the surgery. Now I am satisfied with my result."),
                  ("Ajit Pal", "From the start, the consultation, to the hair transplant procedure I was very comfortable and satisfied. I will definitely recommend Dr Vinod Sonawane to all my family and friends.")],
    l_tag="Visit us", l_title="Two clinics in Mumbai",
    clinics=[("Andheri West", "Ground Floor, Panchavati, Versova Marg, opp. Apna Bazar Road, next to D.N. Nagar Metro Station, Andheri West, Mumbai 400058", MAP_ANDHERI),
             ("Ghatkopar East", "1st Floor, Nand Ashish, 102, R.B. Mehta Marg, above Natural Ice Cream, Ghatkopar East, Mumbai 400077", MAP_GHATKOPAR)],
    hours="Mon–Sat, 10:00 AM – 8:00 PM", directions="Get Directions", call_clinic="Call",
    q_tag="FAQ", q_title="Questions we hear every day",
    faqs=[("How much does a hair transplant cost in Mumbai?", "It usually ranges from about ₹30,000 to ₹1,50,000 or more, depending on the number of grafts, the technique and the surgeon. After assessing your scalp, we give you a personalised estimate at your consultation."),
          ("Is a hair transplant painful?", "It is done under local anaesthesia. You may feel mild discomfort during the injection, and some swelling or tenderness for a few days afterwards."),
          ("Is the result permanent?", "Transplanted follicles come from the donor area, which is genetically resistant to hair loss, so they keep growing. Existing non-transplanted hair may still thin over time."),
          ("When will I see results?", "Shedding in 2–3 weeks, new growth from 3–4 months, noticeable improvement at 6 months and the full result at 9–12 months."),
          ("Who can get a hair transplant?", "Usually people with stable pattern hair loss, a healthy donor area and good general health, generally above 21. Only an assessment can confirm suitability."),
          ("Can a failed or unnatural transplant be corrected?", "Often, yes. Repair can include redesigning the hairline, redistributing grafts and adding density. It depends on your donor reserve and scarring, which we assess first.")],
    fc_title="Ready to talk?", fc_sub="Book your consultation. Call, message or fill the form.",
    wa_btn="Chat on WhatsApp", call_btn="Call Now", book_btn="Book",
    exit_title="Wait. Want a quick call back?", exit_sub="Leave your number and our team will reach out.",
    foot="&copy; Bloom Hair Transplant. Results vary from person to person. Information on this page is general and not a substitute for medical advice. A consultation and examination are required before any procedure.",
    privacy="Privacy Policy", sticky_call="Call", sticky_wa="WhatsApp", sticky_book="Callback", read_more="Read more",
)

MR = dict(
    lang="mr", html_lang="mr-IN", file="mr.html", other_file="index.html", other_label="English",
    fonts="family=Noto+Sans+Devanagari:wght@400;500;600;700;800&family=Poppins:wght@500;600",
    body_font="'Noto Sans Devanagari','Poppins',sans-serif", head_font="'Noto Sans Devanagari','Poppins',sans-serif",
    title="मुंबईतील हेअर ट्रान्सप्लांट | डॉ. विनोद सोनावणे | ब्लूम हेअर ट्रान्सप्लांट",
    meta="अंधेरी वेस्ट आणि घाटकोपर ईस्ट, मुंबई येथे डॉक्टरांच्या देखरेखीखाली हेअर ट्रान्सप्लांट. FUE, दाढी, भुवया, महिलांसाठी आणि रिपेअर उपचार. सल्ल्यासाठी ब्लूम हेअर ट्रान्सप्लांटला कॉल किंवा व्हॉट्सॲप करा.",
    nav_call="कॉल करा", nav_wa="व्हॉट्सॲप",
    badge="अंधेरी वेस्ट &amp; घाटकोपर ईस्ट, मुंबई",
    h1="मुंबईतील हेअर ट्रान्सप्लांट", h1em="जे दिसेल तुमच्याच केसांसारखे.",
    sub="<b>डॉ. विनोद सोनावणे</b> यांच्या नेतृत्वाखाली नियोजन. तुमच्या चेहऱ्याला साजेशी हेअरलाइन, खरंच किती ग्राफ्ट्स लागतील याचा प्रामाणिक सल्ला आणि सल्ला भेटीत स्पष्ट खर्चाचा अंदाज.",
    rating="४.९ गुगल रेटिंग", reviews="४०७ रिव्ह्यूज",
    cta_call="कॉल करा " + PHONE_DISPLAY, cta_wa="व्हॉट्सॲप करा",
    form_title="आम्ही तुम्हाला कॉल करू", form_sub="थोडी माहिती द्या. क्लिनिकच्या वेळेत आमची टीम तुम्हाला फोन करेल.",
    f_name="तुमचे नाव", f_phone="मोबाईल नंबर", f_concern="तुमची समस्या कोणती?",
    concerns=["कपाळावरचे केस कमी होणे / टक्कल", "डोक्याच्या मध्यभागी केस विरळ होणे", "आधीच्या ट्रान्सप्लांटने समाधान नाही", "दाढी / मिशी / भुवया", "महिलांचे केस विरळ होणे", "खात्री नाही, सल्ला हवा आहे"],
    f_btn="कॉलबॅक मागवा", f_note="क्लिनिकच्या वेळा: सोम–शनि, सकाळी १० ते रात्री ८. तुमची माहिती फक्त तुमच्या चौकशीसाठी संपर्क करण्यास वापरली जाईल.",
    f_err="कृपया १० अंकी योग्य मोबाईल नंबर टाका.",
    f_ok_title="धन्यवाद!", f_ok_text="तुमची विनंती मिळाली आहे. लवकर उत्तरासाठी आत्ताच कॉल किंवा मेसेज करा.",
    wa_msg="नमस्कार ब्लूम हेअर ट्रान्सप्लांट, मला सल्ला भेट हवी आहे.\nनाव: {name}\nफोन: {phone}\nसमस्या: {concern}",
    marquee=["FUE हेअर ट्रान्सप्लांट", "दाढी ट्रान्सप्लांट", "भुवया पुनर्रचना", "महिलांसाठी हेअर ट्रान्सप्लांट", "हेअर ट्रान्सप्लांट रिपेअर", "क्राउन आणि हेअरलाइन", "मिशी ट्रान्सप्लांट", "बॉडी हेअर ट्रान्सप्लांट"],
    s_counts=[("4.9", "गुगल रेटिंग", 1), ("407", "गुगल रिव्ह्यूज", 0), ("2", "मुंबईत क्लिनिक्स", 0), ("15", "विशेष उपचार", 0)],
    p_tag="हे तुमच्यासाठी आहे का?", p_title="यापैकी कोणती समस्या तुम्हाला भेडसावते?", p_sub="तुमची समस्या निवडा. ती आम्ही फॉर्ममध्ये आपोआप भरू.",
    p_cards=[("📉", "कपाळावरचे केस कमी होणे", "कपाळावरचे केस कमी होणे / टक्कल", "साच्यातली नाही, तुमच्या चेहऱ्याला साजेशी हेअरलाइन."),
             ("🌀", "डोक्याच्या मध्यभागी विरळपणा", "डोक्याच्या मध्यभागी केस विरळ होणे", "क्राउन भागातील दाटपणासाठी वास्तववादी नियोजन."),
             ("🛠️", "आधीच्या ट्रान्सप्लांटने समाधान नाही", "आधीच्या ट्रान्सप्लांटने समाधान नाही", "अनैसर्गिक हेअरलाइन, कमी दाटपणा किंवा व्रण? रिपेअर ही आमची खासियत आहे."),
             ("🧔", "दाढी, मिशी किंवा भुवया", "दाढी / मिशी / भुवया", "नैसर्गिक दिशा आणि कोनासह दाट चेहऱ्यावरील केस."),
             ("👩", "महिलांचे केस विरळ होणे", "महिलांचे केस विरळ होणे", "महिलांसाठी सौम्य, दाटपणावर भर देणारे नियोजन."),
             ("🤔", "डोनर केस कमी आहेत?", "खात्री नाही, सल्ला हवा आहे", "कधीकधी दाढी किंवा शरीरावरील केस उपयोगी ठरतात. आम्ही तपासूनच सांगतो.")],
    p_cta="माझे पर्याय तपासा",
    links_title="उपचार पहा",
    links=[("पुरुषांसाठी हेअर ट्रान्सप्लांट", "male-hair-transplant-in-mumbai"), ("महिलांसाठी हेअर ट्रान्सप्लांट", "female-hair-transplant"), ("FUE हेअर ट्रान्सप्लांट", "fue-hair-transplant-in-mumbai"),
           ("दाढी ट्रान्सप्लांट", "beard-hair-transplant-in-mumbai"), ("भुवया पुनर्रचना", "eyebrow-reconstruction-in-mumbai"), ("हेअर ट्रान्सप्लांट रिपेअर", "hair-transplant-repair-in-mumbai")],
    d_tag="तुमचे सर्जन", d_title="डॉ. विनोद सोनावणे यांना भेटा",
    d_text="ब्लूममधील प्रत्येक केसमध्ये हेअरलाइन डिझाइनपासून ग्राफ्ट नियोजनापर्यंत डॉ. सोनावणे स्वतः लक्ष घालतात. मिड-डे तर्फे त्यांना &ldquo;Iconic Hair Transplant Surgeon&rdquo; म्हणून गौरवण्यात आले आहे. नैसर्गिक दिसणारे निकाल आणि अयशस्वी ट्रान्सप्लांट सुधारण्यासाठी ते ओळखले जातात.",
    d_pts=["विक्री काउंटर नाही, डॉक्टरांनी केलेले नियोजन", "तुमच्या चेहऱ्याला आणि वयाला साजेशी हेअरलाइन", "ग्राफ्ट्सची प्रामाणिक संख्या आणि वास्तववादी अपेक्षा", "आधीचे ट्रान्सप्लांट दुरुस्त करण्यात तज्ज्ञ"],
    d_cta="डॉ. सोनावणे यांच्या टीमशी बोला",
    r_tag="पाहा आणि जाणून घ्या", r_title="डॉक्टरांकडून थेट उत्तरे", r_sub="ब्लूमचे छोटे रील्स. पाहण्यासाठी टॅप करा.",
    reels=[("reel2", "डोनर केस आणि नियोजन (मराठीत)"), ("reel5", "खऱ्या रुग्णाचा निकाल, सुरुवातीपासून शेवटपर्यंत"), ("reel1", "डॉ. सोनावणे: ट्रान्सप्लांट नैसर्गिक कसे दिसते?"), ("reel3", "डोक्यावर डोनर केस कमी? दाढीचे केस उपयोगी ठरू शकतात"), ("reel6", "पांढरे केस ट्रान्सप्लांट करता येतात का?")],
    b_tag="खरे रुग्ण", b_title="आधी आणि नंतर", b_sub="तुलना करण्यासाठी हँडल ओढा.", b_before="आधी", b_after="नंतर",
    b_disc="येथे दाखवलेले निकाल वैयक्तिक रुग्णांचे आहेत. केसांचा प्रकार, डोनर केस, वय आणि काळजी यावर निकाल वेगवेगळे असतात. तुमच्यासाठी काय वास्तववादी आहे हे सल्ला भेटीतच कळेल.",
    rp_tag="रिपेअर तज्ज्ञ", rp_title="आधीच्या हेअर ट्रान्सप्लांटने समाधान नाही?",
    rp_text="चुकीच्या नियोजनामुळे अनैसर्गिक हेअरलाइन, कमी दाटपणा, दिसणारे व्रण किंवा &ldquo;प्लग्ड&rdquo; लुक येऊ शकतो. ब्लूममध्ये तुमचा डोनर भाग, व्रण आणि ग्राफ्ट्सची जागा तपासून संतुलन परत आणणारी दुरुस्ती आखली जाते.",
    rp_pts=["अनैसर्गिक, सरळ रेषेतील हेअरलाइन", "विरळ किंवा असमान दाटपणा", "दिसणारे व्रण", "डोनर भागातून जास्त ग्राफ्ट्स काढले गेले", "केस नीट न उगवणे"], rp_cta="माझे रिपेअर तपासून घ्या",
    st_tag="प्रक्रिया कशी चालते", st_title="चार सोप्या पायऱ्या",
    steps=[("कॉल किंवा व्हॉट्सॲप", "तुमची समस्या सांगा. आम्ही अंधेरी वेस्ट किंवा घाटकोपर ईस्टमध्ये वेळ ठरवू."), ("स्कॅल्प तपासणी", "डॉ. सोनावणे यांची टीम तुमच्या केस गळतीचा प्रकार आणि डोनर भाग तपासते."), ("वैयक्तिक योजना", "हेअरलाइन डिझाइन, ग्राफ्ट्सचा अंदाज आणि खर्चावर स्पष्ट चर्चा. कसलाही दबाव नाही."), ("प्रक्रिया आणि फॉलो-अप", "लोकल ॲनेस्थेशियाखाली प्रक्रिया, तसेच रिकव्हरी आणि फॉलो-अपसाठी मार्गदर्शन.")],
    t_tag="काय अपेक्षित आहे", t_title="केस वाढीचा कालावधी",
    timeline=[("२–३ आठवडे", "केस तात्पुरते गळतात. हे सामान्य आहे."), ("३–४ महिने", "नवीन केस उगवायला सुरुवात होते."), ("६ महिने", "लक्षात येण्याइतका फरक."), ("९–१२ महिने", "पूर्ण, नैसर्गिक निकाल.")],
    rv_tag="गुगल रिव्ह्यूज", rv_title="रुग्ण काय म्हणतात",
    reviews_list=[("Deepak Chandramohan", "I had done my hair transplant 10 months back and have got amazing natural results. Nobody can guess I have got a hair transplant. I would highly recommend to visit the clinic and speak with Dr Sonawane."),
                  ("Rajan Pillai", "The consultation provided by the Doctor was genuine and realistic. Doctor and their experienced technician took good care during the surgery. Now I am satisfied with my result."),
                  ("Ajit Pal", "From the start, the consultation, to the hair transplant procedure I was very comfortable and satisfied. I will definitely recommend Dr Vinod Sonawane to all my family and friends.")],
    l_tag="आम्हाला भेटा", l_title="मुंबईत दोन क्लिनिक्स",
    clinics=[("अंधेरी वेस्ट", "ग्राउंड फ्लोअर, पंचवटी, वर्सोवा मार्ग, अपना बाजार रोडसमोर, डी.एन. नगर मेट्रो स्टेशनजवळ, अंधेरी वेस्ट, मुंबई ४०००५८", MAP_ANDHERI),
             ("घाटकोपर ईस्ट", "पहिला मजला, नंद आशिष, १०२, आर.बी. मेहता मार्ग, नॅचरल आईस्क्रीमच्या वर, घाटकोपर ईस्ट, मुंबई ४०००७७", MAP_GHATKOPAR)],
    hours="सोम–शनि, सकाळी १०:०० ते रात्री ८:००", directions="रस्ता दाखवा", call_clinic="कॉल",
    q_tag="प्रश्नोत्तरे", q_title="आम्हाला रोज विचारले जाणारे प्रश्न",
    faqs=[("मुंबईत हेअर ट्रान्सप्लांटचा खर्च किती येतो?", "ग्राफ्ट्सची संख्या, तंत्र आणि सर्जन यावर अवलंबून साधारणपणे ₹३०,००० ते ₹१,५०,००० किंवा त्याहून जास्त. तुमचा स्कॅल्प तपासल्यानंतर सल्ला भेटीत आम्ही वैयक्तिक अंदाज देतो."),
          ("हेअर ट्रान्सप्लांट वेदनादायक असते का?", "ही प्रक्रिया लोकल ॲनेस्थेशियाखाली होते. इंजेक्शन देताना थोडा त्रास जाणवू शकतो, आणि नंतर काही दिवस सूज किंवा हलकी वेदना असू शकते."),
          ("निकाल कायमस्वरूपी असतो का?", "ट्रान्सप्लांट केलेले फॉलिकल्स डोनर भागातून घेतले जातात, जो भाग केस गळतीला जनुकीयदृष्ट्या प्रतिरोधक असतो, म्हणून ते वाढत राहतात. मात्र ट्रान्सप्लांट न केलेले आधीचे केस पुढे विरळ होऊ शकतात."),
          ("निकाल कधी दिसतो?", "२–३ आठवड्यांत केस गळतात, ३–४ महिन्यांपासून नवीन केस उगवतात, ६ महिन्यांत लक्षात येण्याजोगा फरक आणि ९–१२ महिन्यांत पूर्ण निकाल."),
          ("हेअर ट्रान्सप्लांट कोण करू शकतो?", "साधारणपणे स्थिर पॅटर्न केस गळती, निरोगी डोनर भाग आणि चांगले सर्वसाधारण आरोग्य असलेल्या, साधारण २१ वर्षांवरील व्यक्ती. योग्यता फक्त तपासणीनंतरच ठरते."),
          ("अयशस्वी किंवा अनैसर्गिक ट्रान्सप्लांट दुरुस्त करता येतो का?", "बऱ्याचदा हो. हेअरलाइन पुन्हा डिझाइन करणे, ग्राफ्ट्स नव्याने लावणे आणि दाटपणा वाढवणे असे उपाय असू शकतात. हे तुमचा डोनर साठा आणि व्रणांवर अवलंबून असते, जे आम्ही आधी तपासतो.")],
    fc_title="बोलायला तयार आहात?", fc_sub="सल्ला भेट बुक करा. कॉल करा, मेसेज करा किंवा फॉर्म भरा.",
    wa_btn="व्हॉट्सॲपवर चॅट करा", call_btn="कॉल करा", book_btn="बुक करा",
    exit_title="थांबा! कॉलबॅक हवा आहे का?", exit_sub="तुमचा नंबर द्या, आमची टीम तुम्हाला संपर्क करेल.",
    foot="&copy; ब्लूम हेअर ट्रान्सप्लांट. निकाल प्रत्येक व्यक्तीनुसार वेगळे असतात. या पानावरील माहिती सर्वसाधारण असून वैद्यकीय सल्ल्याला पर्याय नाही. कोणतीही प्रक्रिया करण्यापूर्वी सल्ला आणि तपासणी आवश्यक आहे.",
    privacy="गोपनीयता धोरण", sticky_call="कॉल", sticky_wa="व्हॉट्सॲप", sticky_book="कॉलबॅक", read_more="अधिक वाचा",
)

# ---------------------------------------------------------------- TEMPLATE
CSS = r"""
:root{--gold:#875f17;--gold2:#ad8946;--gold3:#f8e6c0;--cream:#faf6ee;--ink:#231a0c;--mut:#6b5f4c;--wa:#25d366;--r:20px}
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}
body{font-family:var(--bf);color:var(--ink);background:#fff;line-height:1.6;overflow-x:hidden;-webkit-font-smoothing:antialiased}
img,video{max-width:100%;display:block}a{color:inherit;text-decoration:none}
h1,h2,h3{font-family:var(--hf);line-height:1.18}
.wrap{max-width:1160px;margin:0 auto;padding:0 20px}
section{padding:72px 0;position:relative}
.tag{display:inline-block;background:var(--gold3);color:var(--gold);font-weight:600;font-size:13px;padding:6px 14px;border-radius:99px;letter-spacing:.3px;margin-bottom:14px}
.sec-h{text-align:center;max-width:720px;margin:0 auto 40px}
.sec-h h2{font-size:clamp(28px,4vw,40px);color:var(--ink)}.sec-h p{color:var(--mut);margin-top:10px}
/* buttons */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:9px;font:600 16px var(--bf);padding:15px 26px;border-radius:99px;border:0;cursor:pointer;transition:transform .2s,box-shadow .2s;position:relative;overflow:hidden}
.btn:hover{transform:translateY(-2px)}
.btn-gold{background:linear-gradient(135deg,var(--gold),var(--gold2));color:#fff;box-shadow:0 10px 26px rgba(135,95,23,.35)}
.btn-wa{background:var(--wa);color:#fff;box-shadow:0 10px 26px rgba(37,211,102,.32)}
.btn-line{background:#fff;color:var(--gold);border:2px solid var(--gold)}
.btn-gold::after,.btn-wa::after{content:"";position:absolute;top:0;left:-80%;width:50%;height:100%;background:linear-gradient(100deg,transparent,rgba(255,255,255,.55),transparent);transform:skewX(-20deg);animation:shine 3.2s infinite}
@keyframes shine{0%,60%{left:-80%}100%{left:140%}}
.pulse{animation:pulse 2s infinite}@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(135,95,23,.5)}70%{box-shadow:0 0 0 16px rgba(135,95,23,0)}100%{box-shadow:0 0 0 0 rgba(135,95,23,0)}}
/* top bar */
.top{position:sticky;top:0;z-index:50;background:rgba(255,255,255,.92);backdrop-filter:blur(12px);border-bottom:1px solid #eee4d0}
.top .wrap{display:flex;align-items:center;justify-content:space-between;height:68px;gap:12px}
.top img{height:44px;width:auto}.top .acts{display:flex;gap:10px;align-items:center}
.top .btn{padding:10px 18px;font-size:14px}.lang{font-size:14px;font-weight:600;color:var(--gold);border:1.5px solid var(--gold3);padding:7px 12px;border-radius:99px}
/* hero */
.hero{padding:44px 0 70px;background:radial-gradient(circle at 85% 10%,#f8e6c0 0,transparent 45%),linear-gradient(180deg,#fffdf8,#faf3e3);overflow:hidden}
.blob{position:absolute;border-radius:50%;filter:blur(70px);opacity:.45;z-index:0;animation:float 12s ease-in-out infinite}
.b1{width:340px;height:340px;background:#ecd08f;top:-80px;left:-100px}.b2{width:300px;height:300px;background:#f6dcc0;bottom:-60px;right:30%;animation-delay:-5s}
@keyframes float{50%{transform:translate(40px,30px) scale(1.1)}}
.hero .grid{display:grid;grid-template-columns:1.1fr .9fr;gap:40px;align-items:center;position:relative;z-index:1}
.badge{display:inline-flex;align-items:center;gap:8px;background:#fff;border:1px solid #eadfc6;border-radius:99px;padding:7px 15px;font-size:13.5px;font-weight:600;color:var(--gold);box-shadow:0 4px 14px rgba(0,0,0,.05)}
.badge i{width:8px;height:8px;border-radius:50%;background:#2fbf71;animation:blink 1.4s infinite}@keyframes blink{50%{opacity:.3}}
.hero h1{font-size:clamp(34px,5.4vw,58px);margin:18px 0 16px;color:var(--ink)}
.hero h1 em{font-style:normal;background:linear-gradient(90deg,var(--gold),#c79a3f,var(--gold));background-size:200%;-webkit-background-clip:text;background-clip:text;color:transparent;animation:grad 5s linear infinite;display:block}
@keyframes grad{to{background-position:200% 0}}
.hero .sub{font-size:18px;color:var(--mut);max-width:560px}
.chips{display:flex;flex-wrap:wrap;gap:10px;margin:22px 0}
.chip{background:#fff;border:1px solid #eadfc6;border-radius:12px;padding:9px 14px;font-size:14px;font-weight:600;display:flex;gap:7px;align-items:center}.chip b{color:#f4b400}
.cta-row{display:flex;flex-wrap:wrap;gap:12px}
.hero-img{position:relative;justify-self:center;max-width:430px;width:100%}
.hero-img .frame{border-radius:28px;padding:8px;background:linear-gradient(135deg,var(--gold3),var(--gold2));box-shadow:0 30px 60px rgba(135,95,23,.28);transform:rotate(2deg);transition:transform .4s}
.hero-img:hover .frame{transform:rotate(0)}
.hero-img img{border-radius:22px;width:100%}
.float-card{position:absolute;background:#fff;border-radius:16px;padding:11px 15px;box-shadow:0 14px 30px rgba(0,0,0,.14);font-size:13.5px;font-weight:600;display:flex;gap:9px;align-items:center;animation:bob 4s ease-in-out infinite}
.fc1{left:-22px;bottom:34px}.fc2{right:-14px;top:30px;animation-delay:-2s}@keyframes bob{50%{transform:translateY(-9px)}}
/* form */
.card{background:#fff;border-radius:var(--r);box-shadow:0 24px 60px rgba(60,40,5,.16);padding:26px;border:1px solid #f0e6d0}
.hero .card{margin-top:26px;max-width:520px}
.card h3{font-size:22px}.card .s{color:var(--mut);font-size:14px;margin:4px 0 16px}
.fld{margin-bottom:12px}.fld input,.fld select{width:100%;padding:14px 16px;border:1.5px solid #e5d9bf;border-radius:12px;font:500 15px var(--bf);background:#fffdf9;outline:0;transition:border .2s,box-shadow .2s}
.fld input:focus,.fld select:focus{border-color:var(--gold2);box-shadow:0 0 0 4px rgba(173,137,70,.18)}
.card .btn{width:100%}.note{font-size:12px;color:var(--mut);margin-top:10px}.err{color:#c0392b;font-size:13px;margin:-4px 0 10px;display:none}
.ok{display:none;text-align:center;padding:10px 0}.ok h3{color:var(--gold)}.ok .cta-row{justify-content:center;margin-top:14px}
/* marquee */
.mq{background:var(--gold);color:#fff;padding:14px 0;overflow:hidden;white-space:nowrap}
.mq div{display:inline-block;animation:mq 32s linear infinite}.mq span{margin:0 26px;font-weight:600;font-size:15px}.mq span::before{content:"✦";margin-right:26px;color:var(--gold3)}
@keyframes mq{to{transform:translateX(-50%)}}
/* stats */
.stats{padding:46px 0;background:var(--cream)}.stats .g{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;text-align:center}
.stat b{font:800 clamp(34px,5vw,50px) var(--hf);color:var(--gold);display:block}.stat span{color:var(--mut);font-weight:500;font-size:15px}
/* concerns */
.cg{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.cc{background:#fff;border:1px solid #efe4cb;border-radius:var(--r);padding:26px;transition:transform .25s,box-shadow .25s,border-color .25s;cursor:pointer;transform-style:preserve-3d}
.cc:hover{box-shadow:0 20px 44px rgba(135,95,23,.18);border-color:var(--gold2)}
.cc .i{font-size:34px;width:62px;height:62px;display:grid;place-items:center;background:var(--gold3);border-radius:18px;margin-bottom:14px}
.cc h3{font-size:20px;margin-bottom:6px}.cc p{color:var(--mut);font-size:15px}.cc .go{display:inline-block;margin-top:14px;color:var(--gold);font-weight:700;font-size:15px}
.cc:hover .go{letter-spacing:.4px}
.links{text-align:center;margin-top:34px}.links h4{font-size:15px;color:var(--mut);font-weight:600;margin-bottom:12px}
.links a{display:inline-block;margin:5px;padding:9px 16px;border-radius:99px;border:1.5px solid #e5d9bf;font-size:14px;font-weight:600;color:var(--gold);background:#fff;transition:.2s}.links a:hover{background:var(--gold);color:#fff}
/* doctor */
.doc{background:linear-gradient(180deg,#fff,var(--cream))}.doc .g{display:grid;grid-template-columns:.85fr 1.15fr;gap:46px;align-items:center}
.doc .ph{border-radius:28px;overflow:hidden;box-shadow:0 26px 54px rgba(60,40,5,.22);position:relative}
.doc .ph::after{content:"";position:absolute;inset:0;border:6px solid rgba(255,255,255,.55);border-radius:28px;pointer-events:none}
.doc h2{font-size:clamp(28px,4vw,40px);margin-bottom:14px}.doc p{color:var(--mut);font-size:17px}
.ul{list-style:none;margin:20px 0 26px}.ul li{display:flex;gap:11px;margin:11px 0;font-weight:500}.ul li::before{content:"✓";flex:none;width:24px;height:24px;border-radius:50%;background:var(--gold);color:#fff;display:grid;place-items:center;font-size:13px;margin-top:2px}
/* reels */
.reels{background:#1b1308;color:#fff}.reels .sec-h h2{color:#fff}.reels .sec-h p{color:#d8c9a8}.reels .tag{background:rgba(248,230,192,.15);color:var(--gold3)}
.rs{display:flex;gap:18px;overflow-x:auto;scroll-snap-type:x mandatory;padding:6px 20px 24px;margin:0 -20px;scrollbar-width:thin}
.rc{flex:none;width:250px;scroll-snap-align:center;position:relative;border-radius:22px;overflow:hidden;background:#000;aspect-ratio:9/16;box-shadow:0 18px 40px rgba(0,0,0,.5);cursor:pointer}
.rc video,.rc img.p{width:100%;height:100%;object-fit:cover}
.rc .pl{position:absolute;inset:0;display:grid;place-items:center;background:linear-gradient(180deg,transparent 45%,rgba(0,0,0,.78));transition:opacity .3s}
.rc .pl i{width:62px;height:62px;border-radius:50%;background:rgba(255,255,255,.92);display:grid;place-items:center;color:var(--gold);font-size:24px;padding-left:4px;animation:pulse 2s infinite}
.rc .cap{position:absolute;left:0;right:0;bottom:0;padding:16px;font-weight:600;font-size:14px;line-height:1.35}
.rc.on .pl{opacity:0;pointer-events:none}
/* before-after */
.ba-tabs{display:flex;justify-content:center;gap:8px;margin-bottom:20px;flex-wrap:wrap}
.ba-tabs button{padding:9px 18px;border-radius:99px;border:1.5px solid #e5d9bf;background:#fff;font:600 14px var(--bf);cursor:pointer;color:var(--gold)}
.ba-tabs button.on{background:var(--gold);color:#fff;border-color:var(--gold)}
.ba{position:relative;max-width:520px;margin:0 auto;aspect-ratio:1/1;border-radius:24px;overflow:hidden;box-shadow:0 24px 54px rgba(60,40,5,.22);user-select:none;touch-action:pan-y;cursor:ew-resize}
.ba img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}.ba .af{clip-path:inset(0 0 0 50%)}
.ba .hd{position:absolute;top:0;bottom:0;left:50%;width:4px;background:#fff;transform:translateX(-50%);box-shadow:0 0 12px rgba(0,0,0,.4)}
.ba .hd::after{content:"⇄";position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:48px;height:48px;border-radius:50%;background:#fff;color:var(--gold);display:grid;place-items:center;font-size:22px;box-shadow:0 6px 18px rgba(0,0,0,.3)}
.ba .lb{position:absolute;top:14px;padding:5px 13px;border-radius:99px;background:rgba(0,0,0,.6);color:#fff;font-size:13px;font-weight:600}.ba .l1{left:14px}.ba .l2{right:14px;background:var(--gold)}
.disc{max-width:640px;margin:18px auto 0;text-align:center;font-size:13px;color:var(--mut)}
/* repair */
.rep{background:linear-gradient(135deg,var(--gold),#6b4a10);color:#fff}.rep .g{display:grid;grid-template-columns:1.1fr .9fr;gap:40px;align-items:center}
.rep h2{font-size:clamp(28px,4vw,40px)}.rep p{color:#f3e6c9;margin:14px 0;font-size:17px}.rep .tag{background:rgba(255,255,255,.18);color:#fff}
.rep .pts{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);border-radius:var(--r);padding:26px}.rep .ul li::before{background:#fff;color:var(--gold)}
.rep .btn-gold{background:#fff;color:var(--gold)}
/* steps */
.sg{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;counter-reset:s}
.sc{background:#fff;border:1px solid #efe4cb;border-radius:var(--r);padding:26px 22px;position:relative}
.sc::before{counter-increment:s;content:counter(s);position:absolute;top:-18px;left:22px;width:38px;height:38px;border-radius:50%;background:linear-gradient(135deg,var(--gold),var(--gold2));color:#fff;font:700 17px var(--bf);display:grid;place-items:center;box-shadow:0 8px 18px rgba(135,95,23,.35)}
.sc h3{font-size:18px;margin:8px 0 6px}.sc p{color:var(--mut);font-size:15px}
.tl{margin-top:54px;display:grid;grid-template-columns:repeat(4,1fr);gap:0;position:relative}
.tl::before{content:"";position:absolute;top:18px;left:6%;right:6%;height:3px;background:linear-gradient(90deg,var(--gold3),var(--gold),var(--gold3))}
.tp{text-align:center;padding:0 10px;position:relative}.tp::before{content:"";display:block;width:16px;height:16px;border-radius:50%;background:var(--gold);margin:11px auto 14px;box-shadow:0 0 0 6px var(--gold3)}
.tp b{display:block;color:var(--gold);font-size:17px}.tp span{color:var(--mut);font-size:14.5px}
.tlh{text-align:center;margin-top:50px}.tlh h3{font-size:24px}
/* reviews */
.rvw{background:var(--cream)}.rvg{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.rv{background:#fff;border-radius:var(--r);padding:26px;border:1px solid #efe4cb;position:relative}
.rv::before{content:"“";position:absolute;top:6px;right:20px;font:700 80px Georgia;color:var(--gold3);line-height:1}
.rv .st{color:#f4b400;letter-spacing:2px;margin-bottom:10px}.rv p{color:var(--mut);font-size:15px;font-style:italic}.rv b{display:block;margin-top:14px;font-size:15px}.rv small{color:var(--gold);font-weight:600}
/* locations */
.lg{display:grid;grid-template-columns:1fr 1fr;gap:20px}.lc{background:#fff;border:1px solid #efe4cb;border-radius:var(--r);padding:28px;box-shadow:0 12px 30px rgba(60,40,5,.07)}
.lc h3{font-size:22px;color:var(--gold);margin-bottom:8px}.lc p{color:var(--mut);margin-bottom:8px;font-size:15px}.lc .h{font-weight:600;color:var(--ink)}.lc .cta-row{margin-top:16px}.lc .btn{padding:12px 20px;font-size:15px}
/* faq */
.fq{max-width:800px;margin:0 auto}details{background:#fff;border:1px solid #efe4cb;border-radius:16px;margin-bottom:12px;overflow:hidden}
summary{list-style:none;cursor:pointer;padding:19px 56px 19px 22px;font-weight:600;position:relative;font-size:16.5px}summary::-webkit-details-marker{display:none}
summary::after{content:"+";position:absolute;right:22px;top:50%;transform:translateY(-50%);font-size:26px;color:var(--gold);transition:transform .25s}
details[open] summary::after{transform:translateY(-50%) rotate(45deg)}details[open]{border-color:var(--gold2);box-shadow:0 10px 26px rgba(135,95,23,.12)}
details p{padding:0 22px 20px;color:var(--mut)}
/* final */
.fin{background:linear-gradient(180deg,var(--cream),#f3e7cb)}.fin .g{display:grid;grid-template-columns:.9fr 1.1fr;gap:34px;align-items:start}
.fin h2{font-size:clamp(28px,4vw,42px);margin-bottom:10px}.fin p{color:var(--mut);font-size:17px;margin-bottom:22px}
.fin .stack{display:flex;flex-direction:column;gap:12px;max-width:340px}
.zf{border-radius:var(--r);overflow:hidden;background:#fff;box-shadow:0 24px 60px rgba(60,40,5,.16);border:1px solid #f0e6d0}.zf iframe{width:100%;height:640px;border:0;display:block}
footer{background:#1b1308;color:#cdbf9f;padding:34px 0 110px;font-size:13px;text-align:center}footer a{color:var(--gold3);text-decoration:underline}
/* sticky mobile */
.sb{display:none;position:fixed;left:0;right:0;bottom:0;z-index:60;background:#fff;box-shadow:0 -8px 24px rgba(0,0,0,.14);padding:9px 10px calc(9px + env(safe-area-inset-bottom));gap:8px}
.sb a,.sb button{flex:1;display:flex;flex-direction:column;align-items:center;gap:2px;padding:9px 4px;border-radius:14px;border:0;font:600 13px var(--bf);color:#fff;cursor:pointer}
.sb .c{background:var(--gold)}.sb .w{background:var(--wa)}.sb .b{background:var(--ink)}.sb svg{width:20px;height:20px}
.fab{position:fixed;right:18px;bottom:22px;z-index:55;width:60px;height:60px;border-radius:50%;background:var(--wa);display:grid;place-items:center;box-shadow:0 10px 26px rgba(37,211,102,.5);animation:pulse2 2s infinite}
@keyframes pulse2{0%{box-shadow:0 0 0 0 rgba(37,211,102,.55)}70%{box-shadow:0 0 0 18px rgba(37,211,102,0)}100%{box-shadow:0 0 0 0 rgba(37,211,102,0)}}
.fab svg{width:32px;height:32px;fill:#fff}
/* modal */
.md{position:fixed;inset:0;background:rgba(20,12,2,.62);z-index:90;display:none;place-items:center;padding:20px;backdrop-filter:blur(4px)}.md.on{display:grid}
.md .card{max-width:430px;width:100%;position:relative;animation:pop .35s}@keyframes pop{from{transform:scale(.9);opacity:0}}
.md .x{position:absolute;right:14px;top:10px;background:0;border:0;font-size:28px;cursor:pointer;color:var(--mut)}
/* reveal */
.rv-up{opacity:0;transform:translateY(34px);transition:opacity .8s,transform .8s}.rv-up.in{opacity:1;transform:none}
.glow{position:fixed;width:300px;height:300px;border-radius:50%;background:radial-gradient(circle,rgba(173,137,70,.16),transparent 65%);pointer-events:none;z-index:0;transform:translate(-50%,-50%)}
@media(max-width:900px){
 section{padding:54px 0}.hero .grid,.doc .g,.rep .g,.fin .g,.lg{grid-template-columns:1fr}.hero-img{max-width:300px}
 .cg,.rvg{grid-template-columns:1fr}.sg{grid-template-columns:1fr 1fr;row-gap:34px}.stats .g{grid-template-columns:1fr 1fr;row-gap:22px}
 .tl{grid-template-columns:1fr 1fr;row-gap:24px}.tl::before{display:none}.sb{display:flex}.fab{display:none}.top .btn.hide-m{display:none}.fc1{left:-8px}.fc2{right:-4px}
 .glow{display:none}.zf iframe{height:700px}
}
@media(max-width:520px){.top img{height:36px}.sg{grid-template-columns:1fr}.rc{width:220px}.hero .sub{font-size:16px}.cta-row .btn{width:100%}}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}.rv-up{opacity:1;transform:none}}
"""

WA_SVG = '<svg viewBox="0 0 32 32"><path d="M16 3C9 3 3.4 8.6 3.4 15.5c0 2.3.6 4.4 1.7 6.3L3 29l7.4-2c1.8 1 3.800 1.500 5.600 1.500 7 0 12.600-5.600 12.600-12.500S23 3 16 3zm0 22.800c-1.800 0-3.500-.5-5-1.400l-.4-.2-4.400 1.200 1.200-4.300-.3-.4a10 10 0 0 1-1.500-5.300C5.600 9.900 10.300 5.300 16 5.300s10.400 4.600 10.400 10.200S21.700 25.800 16 25.800zm5.700-7.500c-.3-.2-1.800-.9-2.100-1s-.5-.2-.7.200-.8 1-1 1.200-.4.200-.7.100a8.500 8.500 0 0 1-4.200-3.700c-.3-.6.300-.5.900-1.700.1-.2 0-.4 0-.5l-1-2.300c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.5.100-.8.400s-1 1-1 2.500 1.100 2.900 1.200 3.100c.2.200 2.200 3.400 5.300 4.700 2 .8 2.700.9 3.700.7.600-.1 1.800-.7 2.100-1.400s.3-1.300.2-1.400-.3-.2-.6-.4z"/></svg>'
PH_SVG = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M6.6 10.800a15 15 0 0 0 6.600 6.600l2.200-2.200a1 1 0 0 1 1-.25 11.400 11.400 0 0 0 3.600.6 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.500a1 1 0 0 1 1 1c0 1.300.2 2.500.6 3.600a1 1 0 0 1-.25 1z"/></svg>'
FORM_HTML = """<form class="lead" novalidate>
<div class="fld"><input type="text" name="name" placeholder="{f_name}" autocomplete="name" required></div>
<div class="fld"><input type="tel" name="phone" placeholder="{f_phone}" inputmode="numeric" autocomplete="tel" maxlength="14" required></div>
<div class="fld"><select name="concern" aria-label="{f_concern}">{opts}</select></div>
<div class="err">{f_err}</div>
<button class="btn btn-gold pulse" type="submit">{f_btn}</button>
<p class="note">{f_note}</p></form>
<div class="ok"><h3>{f_ok_title}</h3><p>{f_ok_text}</p><div class="cta-row"><a class="btn btn-gold" href="tel:{tel}" data-ev="call">{call_btn}</a><a class="btn btn-wa" href="{wa}" target="_blank" rel="noopener" data-ev="whatsapp">{wa_btn}</a></div></div>"""


def build(t):
    wa_link = "https://wa.me/%s?text=%s" % (PHONE_WA, __import__("urllib.parse").parse.quote(t["wa_msg"].split("\n")[0]))
    opts = "".join('<option value="%s">%s</option>' % (c, c) for c in t["concerns"])

    def form():
        return FORM_HTML.format(opts=opts, tel=PHONE_TEL, wa=wa_link, **{k: t[k] for k in ("f_name", "f_phone", "f_concern", "f_err", "f_btn", "f_note", "f_ok_title", "f_ok_text", "call_btn", "wa_btn")})

    h = []
    A = h.append
    A('<!doctype html><html lang="%s"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' % t["html_lang"])
    A("<title>%s</title><meta name=\"description\" content=\"%s\">" % (t["title"], t["meta"]))
    A('<meta name="robots" content="noindex,follow"><link rel="alternate" hreflang="en-IN" href="index.html"><link rel="alternate" hreflang="mr-IN" href="mr.html">')
    A('<meta property="og:title" content="%s"><meta property="og:image" content="%s">' % (t["title"], IMG["hero"]))
    A('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?%s&display=swap" rel="stylesheet">' % t["fonts"])
    A('<link rel="preload" as="image" href="%s">' % IMG["hero"])
    A("<style>:root{--bf:%s;--hf:%s}%s</style>" % (t["body_font"], t["head_font"], CSS))
    A("<!-- Paste GTM / Google Ads / Meta Pixel snippets here -->")
    A("</head><body><div class=\"glow\" id=\"glow\"></div>")
    # top bar
    A('<header class="top"><div class="wrap"><a href="%s"><img src="%s" alt="Bloom Hair Transplant &amp; Skin Care logo" width="168" height="44"></a><div class="acts"><a class="lang" href="%s" hreflang="%s">%s</a>' % (t["file"], IMG["logo"], t["other_file"], "en" if t["lang"] == "mr" else "mr", t["other_label"]))
    A('<a class="btn btn-wa hide-m" href="%s" target="_blank" rel="noopener" data-ev="whatsapp">%s</a><a class="btn btn-gold" href="tel:%s" data-ev="call">%s %s</a></div></div></header>' % (wa_link, WA_SVG.replace("<svg", '<svg width="18" height="18" fill="#fff"'), PHONE_TEL, PH_SVG.replace("<svg", '<svg width="18" height="18"'), t["nav_call"]))
    # hero
    A('<section class="hero"><span class="blob b1"></span><span class="blob b2"></span><div class="wrap grid"><div>')
    A('<span class="badge"><i></i>%s</span><h1>%s <em>%s</em></h1><p class="sub">%s</p>' % (t["badge"], t["h1"], t["h1em"], t["sub"]))
    A('<div class="chips"><span class="chip"><b>★★★★★</b>%s</span><span class="chip">%s</span></div>' % (t["rating"], t["reviews"]))
    A('<div class="cta-row"><a class="btn btn-gold pulse" href="tel:%s" data-ev="call">%s %s</a><a class="btn btn-wa" href="%s" target="_blank" rel="noopener" data-ev="whatsapp">%s %s</a></div>' % (PHONE_TEL, PH_SVG.replace("<svg", '<svg width="20" height="20"'), t["cta_call"], wa_link, WA_SVG.replace("<svg", '<svg width="20" height="20" fill="#fff"'), t["cta_wa"]))
    A('<div class="card" id="lead"><h3>%s</h3><p class="s">%s</p>%s</div></div>' % (t["form_title"], t["form_sub"], form()))
    A('<div class="hero-img"><div class="frame"><img src="%s" alt="Dr. Vinod Sonawane, hair transplant surgeon at Bloom Hair Transplant, Mumbai" width="800" height="1000" fetchpriority="high"></div>' % IMG["hero"])
    A('<div class="float-card fc1">⭐ %s</div><div class="float-card fc2">📍 %s</div></div></div></section>' % (t["rating"], t["clinics"][0][0] + " &amp; " + t["clinics"][1][0]))
    # marquee
    items = "".join("<span>%s</span>" % m for m in t["marquee"])
    A('<div class="mq" aria-hidden="true"><div>%s%s</div></div>' % (items, items))
    # stats
    A('<div class="stats"><div class="wrap g">')
    for n, l, dec in t["s_counts"]:
        A('<div class="stat rv-up"><b data-n="%s" data-d="%d">%s</b><span>%s</span></div>' % (n, dec, n, l))
    A("</div></div>")
    # concerns
    A('<section><div class="wrap"><div class="sec-h rv-up"><span class="tag">%s</span><h2>%s</h2><p>%s</p></div><div class="cg">' % (t["p_tag"], t["p_title"], t["p_sub"]))
    for ico, ttl, val, txt in t["p_cards"]:
        A('<div class="cc rv-up tilt" data-concern="%s"><div class="i">%s</div><h3>%s</h3><p>%s</p><span class="go">%s →</span></div>' % (val, ico, ttl, txt, t["p_cta"]))
    A('</div><div class="links rv-up"><h4>%s</h4>' % t["links_title"])
    for lbl, slug in t["links"]:
        A('<a href="%s/services/%s/" target="_blank" rel="noopener">%s</a>' % (SITE, slug, lbl))
    A("</div></div></section>")
    # doctor
    A('<section class="doc"><div class="wrap g"><div class="ph rv-up"><img src="%s" alt="Dr. Vinod Sonawane" loading="lazy" width="670" height="838"></div><div class="rv-up"><span class="tag">%s</span><h2>%s</h2><p>%s</p><ul class="ul">' % (IMG["doctor"], t["d_tag"], t["d_title"], t["d_text"]))
    for p in t["d_pts"]:
        A("<li>%s</li>" % p)
    A('</ul><a class="btn btn-gold" href="tel:%s" data-ev="call">%s %s</a></div></div></section>' % (PHONE_TEL, PH_SVG.replace("<svg", '<svg width="18" height="18"'), t["d_cta"]))
    # reels
    A('<section class="reels"><div class="wrap"><div class="sec-h rv-up"><span class="tag">%s</span><h2>%s</h2><p>%s</p></div><div class="rs">' % (t["r_tag"], t["r_title"], t["r_sub"]))
    for key, cap in t["reels"]:
        A('<div class="rc" data-v="assets/reels/%s.mp4"><img class="p" src="assets/reels/%s.jpg" alt="%s" loading="lazy" width="270" height="480"><div class="pl"><i>▶</i></div><div class="cap">%s</div></div>' % (key, key, cap, cap))
    A("</div></div></section>")
    # before/after
    A('<section><div class="wrap"><div class="sec-h rv-up"><span class="tag">%s</span><h2>%s</h2><p>%s</p></div><div class="ba-tabs">' % (t["b_tag"], t["b_title"], t["b_sub"]))
    for i in range(len(IMG["ba"])):
        A('<button data-i="%d"%s>%d</button>' % (i, ' class="on"' if i == 0 else "", i + 1))
    A('</div><div class="ba" id="ba"><img src="%s" alt="Patient before hair transplant at Bloom" id="ba-b" loading="lazy"><img class="af" src="%s" alt="Same patient after hair transplant at Bloom" id="ba-a" loading="lazy"><span class="lb l1">%s</span><span class="lb l2">%s</span><div class="hd"></div></div><p class="disc">%s</p></div></section>' % (IMG["ba"][0][0], IMG["ba"][0][1], t["b_before"], t["b_after"], t["b_disc"]))
    # repair
    A('<section class="rep"><div class="wrap g"><div class="rv-up"><span class="tag">%s</span><h2>%s</h2><p>%s</p><a class="btn btn-gold" href="#lead" data-concern-go="%s">%s</a></div><div class="pts rv-up"><ul class="ul">' % (t["rp_tag"], t["rp_title"], t["rp_text"], t["concerns"][2], t["rp_cta"]))
    for p in t["rp_pts"]:
        A("<li>%s</li>" % p)
    A("</ul></div></div></section>")
    # steps + timeline
    A('<section><div class="wrap"><div class="sec-h rv-up"><span class="tag">%s</span><h2>%s</h2></div><div class="sg">' % (t["st_tag"], t["st_title"]))
    for a, b in t["steps"]:
        A('<div class="sc rv-up"><h3>%s</h3><p>%s</p></div>' % (a, b))
    A('</div><div class="tlh rv-up"><span class="tag">%s</span><h3>%s</h3></div><div class="tl">' % (t["t_tag"], t["t_title"]))
    for a, b in t["timeline"]:
        A('<div class="tp rv-up"><b>%s</b><span>%s</span></div>' % (a, b))
    A("</div></div></section>")
    # reviews
    A('<section class="rvw"><div class="wrap"><div class="sec-h rv-up"><span class="tag">%s</span><h2>%s</h2><p>%s · %s</p></div><div class="rvg">' % (t["rv_tag"], t["rv_title"], t["rating"], t["reviews"]))
    for n, tx in t["reviews_list"]:
        A('<div class="rv rv-up"><div class="st">★★★★★</div><p>%s</p><b>%s</b><small>Google review</small></div>' % (tx, n))
    A("</div></div></section>")
    # locations
    A('<section><div class="wrap"><div class="sec-h rv-up"><span class="tag">%s</span><h2>%s</h2></div><div class="lg">' % (t["l_tag"], t["l_title"]))
    for n, addr, mp in t["clinics"]:
        A('<div class="lc rv-up"><h3>📍 %s</h3><p>%s</p><p class="h">🕘 %s</p><div class="cta-row"><a class="btn btn-gold" href="tel:%s" data-ev="call">%s</a><a class="btn btn-line" href="%s" target="_blank" rel="noopener" data-ev="directions">%s</a></div></div>' % (n, addr, t["hours"], PHONE_TEL, t["call_clinic"] + " " + PHONE_DISPLAY, mp, t["directions"]))
    A("</div></div></section>")
    # faq
    A('<section style="background:var(--cream)"><div class="wrap"><div class="sec-h rv-up"><span class="tag">%s</span><h2>%s</h2></div><div class="fq">' % (t["q_tag"], t["q_title"]))
    for q, a in t["faqs"]:
        A("<details class=\"rv-up\"><summary>%s</summary><p>%s</p></details>" % (q, a))
    A("</div></div></section>")
    # final cta
    A('<section class="fin" id="book"><div class="wrap g"><div class="rv-up"><h2>%s</h2><p>%s</p><div class="stack"><a class="btn btn-gold pulse" href="tel:%s" data-ev="call">%s %s</a><a class="btn btn-wa" href="%s" target="_blank" rel="noopener" data-ev="whatsapp">%s %s</a></div></div>' % (t["fc_title"], t["fc_sub"], PHONE_TEL, PH_SVG.replace("<svg", '<svg width="20" height="20"'), t["cta_call"], wa_link, WA_SVG.replace("<svg", '<svg width="20" height="20" fill="#fff"'), t["wa_btn"]))
    A('<div class="zf rv-up"><iframe title="%s" loading="lazy" src="%s"></iframe></div></div></section>' % (t["form_title"], ZOHO_FORM))
    A('<footer><div class="wrap"><p>%s</p><p style="margin-top:10px"><a href="%s/privacy-policy/" target="_blank" rel="noopener">%s</a></p></div></footer>' % (t["foot"], SITE, t["privacy"]))
    # sticky + fab + modal
    A('<nav class="sb"><a class="c" href="tel:%s" data-ev="call">%s%s</a><a class="w" href="%s" target="_blank" rel="noopener" data-ev="whatsapp">%s%s</a><button class="b" data-open>%s%s</button></nav>' % (PHONE_TEL, PH_SVG, t["sticky_call"], wa_link, WA_SVG.replace("<svg", '<svg fill="#fff"'), t["sticky_wa"], '<svg viewBox="0 0 24 24" fill="#fff"><path d="M4 4h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2zm8 7 8-5H4l8 5zm0 2L4 8v10h16V8l-8 5z"/></svg>', t["sticky_book"]))
    A('<a class="fab" href="%s" target="_blank" rel="noopener" aria-label="WhatsApp" data-ev="whatsapp">%s</a>' % (wa_link, WA_SVG))
    A('<div class="md" id="md"><div class="card"><button class="x" aria-label="Close">×</button><h3>%s</h3><p class="s">%s</p>%s</div></div>' % (t["exit_title"], t["exit_sub"], form()))
    cfg = dict(endpoint=FORM_ENDPOINT, waNumber=PHONE_WA, waMsg=t["wa_msg"], ba=IMG["ba"], lang=t["lang"])
    A("<script>const CFG=%s;" % json.dumps(cfg, ensure_ascii=False))
    A(JS)
    A("</script></body></html>")
    return "".join(h)


JS = r"""
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
const track=(e,x={})=>{try{(window.dataLayer=window.dataLayer||[]).push({event:'lp_'+e,lang:CFG.lang,...x});if(window.gtag)gtag('event','lp_'+e,x);if(window.fbq&&e==='lead')fbq('track','Lead')}catch(_){}};
$$('[data-ev]').forEach(a=>a.addEventListener('click',()=>track(a.dataset.ev)));
/* reveal */
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.12});
$$('.rv-up').forEach((el,i)=>{el.style.transitionDelay=(i%4)*70+'ms';io.observe(el)});
/* counters */
const co=new IntersectionObserver(es=>es.forEach(e=>{if(!e.isIntersecting)return;co.unobserve(e.target);const el=e.target,n=parseFloat(el.dataset.n),d=+el.dataset.d,t0=performance.now();
const f=t=>{const p=Math.min((t-t0)/1400,1),v=n*(1-Math.pow(1-p,3));el.textContent=v.toFixed(d);if(p<1)requestAnimationFrame(f)};requestAnimationFrame(f)}),{threshold:.6});
$$('[data-n]').forEach(el=>co.observe(el));
/* cursor glow + tilt (desktop) */
if(matchMedia('(hover:hover)').matches){const g=$('#glow');addEventListener('mousemove',e=>{g.style.left=e.clientX+'px';g.style.top=e.clientY+'px'});
$$('.tilt').forEach(c=>{c.addEventListener('mousemove',e=>{const r=c.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;c.style.transform=`perspective(700px) rotateY(${x*8}deg) rotateX(${-y*8}deg) translateY(-6px)`});c.addEventListener('mouseleave',()=>c.style.transform='')})}
/* concern cards -> form */
const goForm=v=>{const s=$('#lead select');if(s&&v)s.value=v;$('#lead').scrollIntoView({behavior:'smooth',block:'center'});setTimeout(()=>$('#lead input')?.focus({preventScroll:true}),600)};
$$('[data-concern]').forEach(c=>c.addEventListener('click',()=>{track('concern',{concern:c.dataset.concern});goForm(c.dataset.concern)}));
$$('[data-concern-go]').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();goForm(a.dataset.concernGo)}));
/* reels */
$$('.rc').forEach(c=>c.addEventListener('click',()=>{
 let v=$('video',c);
 if(!v){$$('.rc video').forEach(o=>{o.pause();o.parentElement.classList.remove('on')});v=document.createElement('video');v.src=c.dataset.v;v.playsInline=true;v.controls=true;v.preload='auto';c.prepend(v);c.classList.add('on');v.play();track('reel',{src:c.dataset.v});v.addEventListener('ended',()=>c.classList.remove('on'));return}
 if(v.paused){$$('.rc video').forEach(o=>{if(o!==v){o.pause();o.parentElement.classList.remove('on')}});c.classList.add('on');v.play()}}));
/* before/after */
const ba=$('#ba'),af=$('#ba-a');let drag=false;
const setPos=x=>{const r=ba.getBoundingClientRect();let p=Math.max(0,Math.min(1,(x-r.left)/r.width))*100;af.style.clipPath=`inset(0 0 0 ${p}%)`;$('.hd',ba).style.left=p+'%'};
ba.addEventListener('pointerdown',e=>{drag=true;ba.setPointerCapture(e.pointerId);setPos(e.clientX)});ba.addEventListener('pointermove',e=>{if(drag)setPos(e.clientX)});ba.addEventListener('pointerup',()=>drag=false);
$$('.ba-tabs button').forEach(b=>b.addEventListener('click',()=>{$$('.ba-tabs button').forEach(x=>x.classList.remove('on'));b.classList.add('on');const p=CFG.ba[+b.dataset.i];$('#ba-b').src=p[0];af.src=p[1];setPos(ba.getBoundingClientRect().left+ba.offsetWidth/2)}));
/* forms */
const modal=$('#md');const closeM=()=>modal.classList.remove('on');
$('.x',modal).onclick=closeM;modal.addEventListener('click',e=>{if(e.target===modal)closeM()});
$$('[data-open]').forEach(b=>b.addEventListener('click',()=>modal.classList.add('on')));
$$('form.lead').forEach(f=>f.addEventListener('submit',async e=>{e.preventDefault();
 const name=f.name.value.trim(),phone=f.phone.value.replace(/[^\d]/g,'').replace(/^(91|0)(?=\d{10}$)/,''),concern=f.concern.value,err=$('.err',f.parentElement);
 if(!/^[6-9]\d{9}$/.test(phone)){err.style.display='block';f.phone.focus();return}err.style.display='none';
 const params=new URLSearchParams(location.search),data={name,phone,concern,lang:CFG.lang,page:location.href,utm_source:params.get('utm_source')||'',utm_campaign:params.get('utm_campaign')||'',utm_term:params.get('utm_term')||''};
 track('lead',{concern});
 const msg=CFG.waMsg.replace('{name}',name||'-').replace('{phone}',phone).replace('{concern}',concern);
 if(CFG.endpoint){try{await fetch(CFG.endpoint,{method:'POST',mode:'no-cors',headers:{'Content-Type':'text/plain'},body:JSON.stringify(data)})}catch(_){}
  f.style.display='none';$('.ok',f.parentElement).style.display='block'}
 else{window.open('https://wa.me/'+CFG.waNumber+'?text='+encodeURIComponent(msg),'_blank');f.style.display='none';$('.ok',f.parentElement).style.display='block'}}));
/* exit intent (desktop, once) */
let shown=sessionStorage.getItem('xi');
document.addEventListener('mouseout',e=>{if(!shown&&e.clientY<=0&&innerWidth>900){shown=1;try{sessionStorage.setItem('xi',1)}catch(_){}modal.classList.add('on')}});
"""

if __name__ == "__main__":
    here = pathlib.Path(__file__).parent
    for t in (EN, MR):
        (here / t["file"]).write_text(build(t), encoding="utf-8")
        print("wrote", t["file"])
