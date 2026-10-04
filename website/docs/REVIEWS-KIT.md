# Getting 15+ real 5-star reviews (and showing them on every page)

Fake or self-written reviews are an unfair trade practice under the Consumer Protection Act, 2019 (CCPA guidelines and
BIS standard IS 19000:2022 on online reviews), break Google's review policy and can get the whole site penalised.
Real reviews, collected well, beat fake ones on trust and rankings. This kit gets you there in about two weeks.

## 1. Who to ask (this week)

Pick 25–30 clients whose work was completed smoothly in the last 6 months, across services (GST, ITR, company,
trademark). Expect roughly 50–60% to respond, so 25–30 asks gives about 15 reviews.

## 2. WhatsApp message (send right after a filing is completed)

> Namaste {Name} ji 🙏
> Your {GST return / ITR / registration} has been filed successfully. ARN: {ARN}.
> If you were happy with our service, could you spare 30 seconds to leave us a Google review? It really helps a small
> team like ours: {Google review link}
> Thank you for trusting Bharat e-Filing!

**Hindi version**

> नमस्ते {Name} जी 🙏
> आपका {GST रिटर्न / ITR / रजिस्ट्रेशन} सफलतापूर्वक फाइल हो गया है। ARN: {ARN}।
> अगर आप हमारी सेवा से संतुष्ट हैं, तो कृपया 30 सेकंड निकालकर Google पर हमारा रिव्यू दें: {Google review link}
> Bharat e-Filing पर भरोसा करने के लिए धन्यवाद!

Get the review link from Google Business Profile → "Ask for reviews" (format `https://g.page/r/…/review`).

## 3. Rules that keep reviews genuine

- Ask **every** eligible client the same way. Don't ask only happy ones and don't filter who gets the link.
- **No incentives** (discounts, freebies) in exchange for reviews.
- Never write, edit or suggest the wording; never post reviews on a client's behalf.
- Reply politely to every review, including critical ones, within 48 hours.

## 4. Putting them on the website

1. Copy each review **word for word** into `src/testimonials.json`:

```json
{
  "name": "Client name as shown on Google",
  "city": "Pune",
  "services": ["gst-registration"],
  "service_label": "GST Registration",
  "rating": 5,
  "text": "Exact review text from Google",
  "date": "2026-10-12",
  "source": "Google",
  "url": "https://maps.app.goo.gl/… (link to the review)"
}
```

2. Add the client's permission to show their name (a WhatsApp "yes" is enough; keep a screenshot).
3. Rebuild the pages: `python3 scripts/pagekit.py <page>`. Each service page shows only the reviews tagged with that
   service; an empty list shows nothing.
4. Do **not** add `AggregateRating` schema for your own business on your own site; Google ignores it for self-served reviews.
