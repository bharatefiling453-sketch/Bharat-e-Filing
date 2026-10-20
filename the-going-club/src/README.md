# The Going Club — website

- `../index.html` — the finished, self-contained site (open in any browser).
- `index.src.html` — editable source: trips (`PLANS`), contact (`CONTACT`), photos, copy.
- `build.js` — inlines GSAP 3 (ScrollTrigger, SplitText) + Lenis into `index.html`.

Rebuild after editing:

    npm i gsap@3 lenis@1
    node build.js

## Photos
All photos are free Unsplash photos (Unsplash License), loaded from images.unsplash.com. The
direct links come from the official Unsplash open dataset (PHOTO_URL map in index.src.html).
colour gradient shows. Before launch, download them and host them on thegoingclub.com
(faster loading, and no dependency on Unsplash's download links).

## Trip data format
Each day: `[title, place, "photoId,backupId", [activities], stay, meals]`.
