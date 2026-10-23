# MiniBrick.mk

A Macedonian personalized-gift frontend with a five-step live frame configurator. The site is being developed as the actual business website; the user has deferred backend implementation. Order requests are currently prepared locally and are not submitted to the business.

## Run locally

```bash
npm install
npm run dev
```

Open the URL printed by Next.js (normally http://localhost:3000).

## Production check

```bash
npm run build
npm run start
```

The supplied logo and product reference are in `public/`. The frame artwork and brick-style figures are rendered with reusable React and CSS components so every control updates the preview immediately.

## Modular character builder

The existing **Стил** step uses `components/characters/MiniBrickCharacter.tsx` and a typed asset catalog. It supports 9 heads, 27 facial expressions across four character types, 12 upper-body colors, and 12 lower-body colors. Each figure retains its own settings when switching figures, types, or figure counts. The existing frame preview renders the same character configurations.

Newborns use the owner-supplied hat-and-tapered-body reference, with four existing faces and twelve matching hat/body colors. Child artwork is rendered at 88% of adult size about the shared foot anchor; adult assets are unchanged.

```bash
npm run lint
npm run typecheck
npm run test:character-assets
npm run build
```

See `scripts/character-assets/README.md` for asset provenance and shared coordinates, and `character-tests/README.md` for the development-only testing gallery and browser verification.

## Background customization

The existing **Позадина** step now offers the supplied 110 backgrounds, 110 lazy-loaded thumbnails and nine category filters. Artwork is copied unchanged into `public/backgrounds/`. `data/backgrounds.json` preserves the complete supplier manifest, including the excluded BG014 entry and warnings on seven approved demo designs. Only entries with usable image paths appear in the gallery. `data/background-inventory.csv` retains the original filename mapping.

`FrameConfiguration.backgroundSettings` is the source of truth for the configurator's active catalog ID, photo URL, mode, fit, position and zoom. The old `background` presets remain compatible with the unchanged homepage examples and occasion headings. Both live and final previews consume the same settings. The memoized figure subtree keeps the approved artwork and character state intact during background changes.

Personal photos support JPEG, PNG and WebP up to 10 MB, with type, size and decode validation. They remain local to the mounted configurator; refreshing the page clears them. Switching modes keeps the uploaded photo and its adjustments. Replacing, removing or resetting it revokes the unused object URL; unmount also cleans up. Catalog artwork uses centered `cover` to fill the entire frame interior without distortion; edges may crop. Custom photos default to full-frame `cover`, with positioning and zoom controls. The whole-photo option retains the complete image over a soft full-frame backdrop from the same photograph. No backend, storage service or new application dependency was added.

### Background verification

With the application running, install Playwright and Pillow in a separate Python environment, then run:

```bash
python background-tests/verify_assets.py /path/to/MiniBrick_Backgrounds_Codex_Ready.zip
BACKGROUND_TEST_URL=http://localhost:3004 python background-tests/test_backgrounds.py
```

The browser script uses Google Chrome on macOS. It checks all 110 gallery selections and image decodes, nine category counts, keyboard activation, independent figures, upload formats and validation, crop/position behavior, final-preview synchronization, object URL cleanup, image errors/retry, and five desktop/mobile widths. Reports and screenshots are written to `artifacts/backgrounds/`.

### Demo limitations

Uploads are intentionally temporary and never sent to a server. Supplied calendar designs are static images. Some artwork has existing printed text, so it may overlap the preserved personal text or figures; no artwork is edited or removed. The supplier's seven `review` warnings remain in the manifest for production review (including branding/signatures and fixed printed details). BG014 still requires a clean source. The former provisional newborn files remain preserved; the active model now uses the owner-supplied reference.

### Figure placement

The frame preview on the **Позадина**, **Текст** and **Преглед** steps includes **Положба на фигурите** controls for moving the entire figure group vertically and widening its spacing. Placement lives in `FrameConfiguration.figureLayout`, independently of the selected background/photo and each character's appearance. Changing figure count retains placement; spacing is disabled for a single figure. The reset button resets placement only. Movement uses relative scene coordinates and count-dependent spacing limits, retaining character scale across desktop/mobile and final previews.

Run `python background-tests/test_figure_placement.py` with the application running to verify actual transparent-asset bounds, movement, spacing, keyboard use, state preservation and final-preview synchronization for one to four figures.

### Optional text and placement

**Положба на текстот** below the frame moves the names, message and date together, independently of figure placement. `FrameConfiguration.textLayout` preserves this position across background changes and the final preview. Name, message and date fields may be empty; no fallback copy is printed in their place. Empty rows retain their layout height so removing text does not shift the figures. Partial names are joined without extra separators.

Run `python background-tests/test_text_placement.py` against the running application to check optional fields, independent movement, reset, keyboard controls, final-preview state and frame bounds at desktop/mobile sizes.

### Background composition audit

The refinement audit found three reproducible issues: long names were truncated with ellipses; dark personalized text lost contrast on dark photos; and long unbroken values in the final summary could widen the grid and change the preview scale.

The configurator now wraps full text, gently reduces name typography for very long groups, and measures/clamps the text within the frame interior. A fixed text slot retains the approved figure geometry even when rows wrap or fields become empty. The optional **Подлога за читливост** setting adds a small translucent backing behind the figures and personalized text, without changing any source artwork. Grid tracks and summary wrapping keep preview size consistent between steps. Homepage examples retain their original rendering.

Run `python background-tests/test_background_audit.py` for long-copy bounds, readable backing, stable loading geometry, filters, state continuity and uploaded-photo final review. `test_backgrounds.py` separately verifies the complete collection and upload behavior; its photo slider selectors are scoped to the photo fieldset so the figure/text controls remain independent.

Only a white frame option exists in this demo; a black frame could not be verified. Printed text/illustrations are part of the supplied raster artwork, and automatic detection or repositioning of those elements is not implemented. Use the existing figure/text sliders to choose the composition; the backing is opt-in and does not alter background files.

## Coordinated configurator upgrade — 2026-10-23

The existing five steps now support 1–8 figures, white/black CSS frames, an additional interactive calendar background mode, per-figure optional accessories, centralized MKD pricing and a local order-request preparation form. The approved Character Builder, its 81 PNGs and compositor, and all 110 original backgrounds/thumbnails are retained. Extra figures use stable slots and a compact two-row frame composition; their builder tabs wrap into a four-column grid.

- `components/product/calendar.ts` generates a Monday-first grid with UTC calculations, Gregorian leap years and clamped dates from 1900–2100. `CalendarDesign.tsx` renders Macedonian month/year/weekdays and exactly one selected-day red circle as SVG. It follows the supplied reference style without using its fixed October/26 raster. The original static calendar catalog images remain unchanged. Switching background modes retains the selected date, photo and catalog ID.
- `components/product/catalog.ts` owns frame labels, accessory/pet IDs and isolated size mapping. Current sizes are 15 × 20 cm for 1–3 figures, vertical 20 × 25 cm for exactly four, and horizontal A4 for more than four. The numeric 4+ team field supports 5–24 figures in the browser preview. The selected size appears in the review and exported request. No size/color surcharge is applied.
- `components/product/pricing.ts` calculates the base figure price, accessory lines/subtotal, 170 ден. delivery and total. Hidden figure accessories do not contribute. Each accessory can be toggled once per visible stable figure; a pet variant counts as one pet. The UI supports 1–8 figures; the pricing formula supports additional figures after four at 350 ден. each.
- Accessory controls sit alongside the unchanged builder. `AccessoryArtwork` renders separate preview overlays without changing approved character geometry, masks or layers. Newborn summaries include face/body only. Preview art is approximate: heart/money/pistol are generated illustrations; pet cutouts are derived with image assistance from the supplied screenshots. Original screenshots are preserved in `artifacts/upgrade/references/`. See `public/accessories/PROVENANCE.md`.
- `OrderReview.tsx` derives the visible review, pricing and request from the same current configuration. Contact fields are kept in memory across steps, validated locally and never logged or transmitted. Copy and JSON download require valid contact details. Editing contact details invalidates the prepared state. The exact required product disclaimer is displayed in review.
- No verified ordering address/phone/endpoint was supplied. Requests explicitly remain **prepared, not submitted**. Custom-photo requests include filename and crop settings with `attached: false`; they exclude local object URLs and require separate photo delivery. No backend, payment, auth, remote upload or persistence was added.

Additional checks:

```bash
node upgrade-tests/product.test.cjs
BACKGROUND_TEST_URL=http://localhost:3004 /tmp/minibrick-character-qa/bin/python upgrade-tests/test_upgrade.py
```

The Node tests use the already installed TypeScript compiler and a small CommonJS test loader; no dependency was added. Integration tests use the existing separate Python Playwright environment and synthetic contact information. Results and delivery notes are in `artifacts/upgrade/`.


## Frontend readiness pass — 2026-10-23

Backend development is explicitly deferred by the user. The public frontend now replaces fictional testimonials with factual FAQs, uses the supplied real-work photograph, removes the unverified generic Instagram destination, and links to `/privacy` for an accurate explanation of current local data handling. The footer no longer claims that personal data is never processed. This factual page is not a substitute for the final business privacy policy once orders are received.

Keyboard improvements include a skip link, Escape dismissal/focus return in the mobile menu, focus movement to the selected configurator step, and focus on prepared request output. Native controls and customer text inputs retain responsive layouts; phone-sized editable fields use at least 16 px type. The supplied product image, logo and accessory thumbnails use Next Image optimization without changing source assets.

Next.js and its ESLint configuration are patched within version 15, with narrowly scoped transitive security overrides. See the runtime and full dependency audit reports in `artifacts/frontend-readiness/`. Standard response headers protect against framing, MIME sniffing and unnecessary device access; the CSP only contains compatible framing/base/object/form directives and is not claimed to be a complete script policy.

Search indexing is disabled in metadata during frontend development. Enable it only as part of a future verified public release, alongside canonical URLs/sitemap based on the actual deployment and completed business policies. No fake order receipt, database record or uploaded-photo delivery is implemented.

Detailed feature classification, verification and remaining launch blockers are in `artifacts/frontend-readiness/REPORT.md`.

## Story, gallery and preview refinement

`/#about` uses the complete business story transcribed from the user-supplied Instagram screenshot. `/gallery` uses all 50 original client photographs supplied in `Archive 2.zip`, referenced through `data/gallery.ts`. The responsive grid shows complete photographs, with accessible native-dialog enlargement and a configurator CTA. The homepage gallery preview also uses this collection. Files in `public/projects/client/` are byte-identical to the ZIP; previous project assets remain preserved. Client-supplied images have no inferred Instagram attribution links. The hero displays the original birthday-frame photograph with an exterior-only CSS mask; its product pixels are unchanged. No customer identities or projects are invented.

Configurator frame width, figure region and accessory coordinates now share the same geometry across catalog, calendar, custom-photo, text and review modes. Calendar paper and image layers fill the complete usable frame interior. Original artwork and approved character assembly remain unchanged. Accessory SVG view boxes crop transparent padding for legibility; previews retain approximate-art notices.

See `artifacts/visual-refinement/REPORT.md` for scope, validation, files and content still needed.

### Higher-resolution product photos and larger teams

The earlier four Instagram project images remain preserved as larger public-post originals (`public/projects/*-hq.jpg`); the hero still uses the birthday photo. The gallery and homepage showcase now use the 50 client-supplied originals described above, with quality-90 responsive delivery and full-photo enlargement. Smaller original files remain untouched. Landscape A4 previews use more of the available pane, and team SVGs scale uniformly without changing source artwork. Measured team figures are approximately 28–61% larger across tested desktop/mobile counts. See `artifacts/photo-quality/REPORT.md` and `frontend-tests/test_photo_quality.py`.

Client gallery intake and verification: `artifacts/client-gallery/REPORT.md`, `manifest.json`, and `browser-report.json`.

### New Year occasion and model availability

The twelve seasonal backgrounds are labelled **Новогодишни** and have a dedicated **Нова година** occasion. Selecting it starts with BG015; the ordinary initial/reset background remains BG018. Original background artwork and IDs are unchanged. Model availability is explained in the character builder and final review; the exact product disclaimer is introduced by **Напомена:**. See artifacts/new-year-models/REPORT.md and frontend-tests/test_new_year_models.py.
