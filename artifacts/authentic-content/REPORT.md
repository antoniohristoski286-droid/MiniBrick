# MiniBrick — authentic content, hero photo and landscape teams

## Content and photo sourcing

Replaced the temporary story text with all four paragraphs transcribed from the owner's supplied Instagram screenshot. Decorative emoji/hashtags and social interface text are omitted; no founding year, founder identity or additional history was invented. Story copy remains centralized in `data/gallery.ts`.

Read the public [MiniBrick Instagram profile](https://www.instagram.com/minibrick.mk/) through the browser after the web fetch was throttled. Public profile images were available; full post views required login. Saved four publicly available photographs showing completed frames, retaining stable post source links in gallery data and `sources.json`. Excluded the workbench and accessory-announcement images. Originals were copied unchanged into `public/projects/`; the site does not depend on expiring Instagram CDN URLs or load a tracking embed.

The gallery now contains those four photos plus the original supplied authentic product-reference photo. Each new image links to its Instagram post. Native dialog enlargement supports every image and keeps original image proportions. The homepage showcase also uses a real family frame instead of its illustrative example. Added the supplied official Instagram contact link in the footer; local request preparation still does not submit an order.

## Real photographic hero

Replaced the hero's CSS/SVG preview with the authentic birthday-frame photo at `public/projects/birthday-frame.jpg`, sourced from [this MiniBrick post](https://www.instagram.com/minibrick.mk/p/DeeqDHgK2Hx/). An exterior-only CSS polygon follows the physical frame outline, leaving the site background visible around it. The frame's original photographed pixels, figures, paper, hearts and lettering are unchanged. This produces the requested background-free website presentation without fabricating a new product render.

The image-editing skill/built-in image tool was tried for transparent extraction, with a prompt requiring unchanged frame, figures, hearts, text and perspective. Its output altered product details and was rejected. It is not referenced by the site. `hero-provenance.json` records the attempt and the final exact-photo approach; `hero-edit-prompt.txt` stores the exact built-in editing prompt. No generated image replaces an authentic gallery product.

## Frame/count behavior

- 1–3 figures: 15 × 20 cm, portrait.
- Exactly four: 20 × 25 cm, portrait.
- More than four: A4, landscape (297:210 aspect ratio).
- Dedicated **4+ / Тимска рамка** option opens a numeric count field, replacing the old fixed 1–8 dropdown and optional A4 toggle.
- The browser preview accepts 5–24 figures. This explicit frontend preview guard is not a confirmed manufacturing maximum. Invalid/empty/fractional input keeps the last valid configuration and blocks forward navigation until corrected.
- Teams expand stable character slots rather than replacing the approved builder. Above eight, a two-row landscape grid adds columns as needed. Each figure remains independently configurable.
- Both frame colors, calendar/date behavior, upload controls, accessories and existing prices are preserved. Base pricing continues the existing +350 MKD per figure above four; no new pricing rule was invented.
- Review, copied request and JSON export include effective size, count and Macedonian orientation. Exactly four cannot retain an A4 selection from prior team state.

## Files

Added `public/projects/{birthday-frame,family-frame,couple-frames,four-figure-frame}.jpg`, `frontend-tests/test_authentic_content.py`, and this artifact directory.

Updated `data/gallery.ts`, `components/ProjectGallery.tsx`, `app/gallery/page.tsx`, `app/page.tsx`, `app/globals.css`, `components/Configurator.tsx`, `components/FramePreview.tsx`, `components/product/catalog.ts`, `components/product/order.ts`, `components/product/ProductOptions.tsx`, `components/product/OrderReview.tsx`, `frontend-tests/test_frame_sizes.py`, count selectors in existing visual/upgrade browser tests, product unit expectations, `PRODUCT.md`, and `README.md`.

No backend, service credentials, dependencies, deployment or Git commits were introduced. Existing work is preserved. SHA-256 verification found no changes/missing files among 344 previously existing character/background/accessory assets and approved character TSX sources.

## Verification

- Production build, TypeScript and ESLint pass without warnings.
- Product unit suite: 7,448 assertions pass, including 9/12/24-figure pricing/count/orientation exports.
- Numeric team/size browser test passes cleanly: counts 1/2/3/4/5/8/12/24, actual landscape/portrait ratios, invalid-input handling, review/JSON/text export, pricing and reset.
- Authentic-content browser assertions pass: 40 count/mode/viewport cases at 1440/768/390/320 px; all figures in bounds; identical geometry between catalog and calendar; all five gallery images/lightboxes; twelve independently selectable builder figures; original photographic hero; supplied story paragraphs; no website runtime errors or failed requests.
- That test wrote its successful report, then hit the previously observed local installed-Chrome/Playwright shutdown hang after the browser exited. It was interrupted during teardown; this is not reported as a clean test-process exit.
- Screenshots include hero, story, gallery and landscape team/calendar at desktop, tablet and mobile widths.
- Existing full frontend readiness test passes cleanly on the final build: navigation/focus, local uploads/privacy, validation, clipboard-denial recovery, export and no personal-data POSTs.
- Existing product-upgrade browser test passes cleanly after updating its count selectors: all 7 pet variants, 1–8 totals, frame colors, calendar clamping, 20 responsive cases and request preparation/export, with zero runtime errors.
- Final hero/home-gallery smoke test passes: both display original project photos, with no illustrative frame in those locations.
- `git diff --check` passes.

Public Instagram files are profile-resolution images, not private/full-resolution originals. Higher-quality originals can replace the same local files later. Original background and character files remain unchanged. The CSS preview is approximate, especially for dense teams; the standalone Character Builder remains available to inspect each figure in detail. Backend/order submission remains deferred.
