/**
 * Google Apps Script: receives the landing-page leads, stores them in a Google Sheet and e-mails the guide PDF.
 *
 * Setup (5 minutes):
 * 1. Create a Google Sheet with two tabs named "Guide" and "Assessment". Copy the sheet ID from its URL.
 * 2. Open script.google.com > New project > paste this file > set SHEET_ID below.
 * 3. Deploy > New deployment > type "Web app" > Execute as: Me > Who has access: Anyone > Deploy. Copy the /exec URL.
 * 4. In build.py set FORM_ENDPOINT (and/or GUIDE_ENDPOINT) to that URL, set BASE_URL to the public folder URL
 *    (the PDF must be reachable by Google at BASE_URL + guide-en.pdf), then run: python3 build.py && python3 share.py
 *
 * Note: MailApp has a daily limit (about 100 recipients/day on a free Gmail account, 1500 on Google Workspace).
 */
const SHEET_ID = 'PASTE_SHEET_ID_HERE';
const NOTIFY = 'info@bloomhairtransplant.com'; // gets a copy of every lead

function doPost(e) {
  const d = JSON.parse(e.postData.contents);
  const ss = SpreadsheetApp.openById(SHEET_ID);
  const now = new Date();
  if (d.type === 'guide') {
    ss.getSheetByName('Guide').appendRow([now, d.name, d.email, d.phone, d.lang, d.utm_source, d.utm_campaign, d.utm_term, d.gclid, d.page]);
    try {
      const mr = d.lang === 'mr';
      const blob = UrlFetchApp.fetch(d.guide_url).getBlob().setName(mr ? 'Bloom-Hair-Transplant-Guide-Marathi.pdf' : 'Bloom-Hair-Transplant-Guide.pdf');
      MailApp.sendEmail({
        to: d.email,
        subject: mr ? 'तुमचं मुंबई हेअर ट्रान्सप्लांट गाईड' : 'Your Mumbai Hair Transplant Guide',
        htmlBody: (mr ? 'नमस्कार ' : 'Hello ') + (d.name || '') + ',<br><br>' +
          (mr ? 'तुम्ही मागितलेलं गाईड सोबत जोडलं आहे. प्रश्न असल्यास +91 80970 00044 वर कॉल किंवा व्हॉट्सअॅप करा.' : 'Your guide is attached. For any question, call or WhatsApp us on +91 80970 00044.') +
          '<br><br>Bloom Hair Transplant<br>Andheri West &amp; Ghatkopar East, Mumbai',
        attachments: [blob],
        name: 'Bloom Hair Transplant'
      });
    } catch (err) {
      MailApp.sendEmail(NOTIFY, 'Guide e-mail failed for ' + d.email, String(err));
    }
    MailApp.sendEmail(NOTIFY, 'New guide download: ' + (d.name || d.email), JSON.stringify(d, null, 2));
  } else {
    ss.getSheetByName('Assessment').appendRow([now, d.name, d.phone, d.clinic, d.time, d.concern, d.since, d.age, d.timing, d.prev, d.lang, d.utm_source, d.utm_campaign, d.utm_term, d.gclid, d.page]);
    MailApp.sendEmail(NOTIFY, 'New assessment lead: ' + (d.name || d.phone), JSON.stringify(d, null, 2));
  }
  return ContentService.createTextOutput('ok');
}
