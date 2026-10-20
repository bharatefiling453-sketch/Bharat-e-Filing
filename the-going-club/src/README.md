# The Going Club — website

- `../index.html` — the finished, self-contained site (open it in any browser; no install needed).
- `index.src.html` — editable source (trips, prices, photos, copy).
- `build.js` — inlines GSAP 3 (ScrollTrigger, SplitText) and Lenis smooth-scroll into `index.html`.

Rebuild after editing:

    npm i gsap@3 lenis@1
    node build.js

Edit `WHATSAPP`, `IMG` (photo IDs), `PLANS` (itineraries/prices) near the top of the script in `index.src.html`.
