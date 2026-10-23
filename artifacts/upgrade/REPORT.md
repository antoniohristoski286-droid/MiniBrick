# MiniBrick.mk configurator upgrade — 2026-10-23

## Delivered features

All three implementation phases extend the existing five-step configurator. The approved Character Builder source and character artwork are unchanged, as are the 110 supplier backgrounds, thumbnails, IDs, categories and warnings. No dependency, backend, payment flow, authentication or deployment was introduced. Existing modified/untracked files and the project handoff were preserved.

### 1. Frames and calendar

- White and black choices in Фигури update the existing CSS shadow-box exterior immediately. Selection persists through all steps and appears in the review and exported request; interior artwork is unchanged by frame color.
- Figure count now supports 1–8, retaining the original 1–4 buttons and adding a compact count selector. Stable hidden character/accessory slots are retained. Larger groups use two rows; extra builder tabs wrap without modifying the approved builder component.
- Календар is a third mode beside the authentic catalog and local photograph. Its SVG uses a generated Monday-first grid, Macedonian month/year/weekdays, correct month lengths and leap years, and a single thin red circle around the selected day. The reference image's fixed month/circle is not used as a raster layer. Month/year/day changes regenerate the design; invalid month transitions clamp to the last available day. Supported years: 1900–2100.
- Calendar date, catalog choice and uploaded photo retain their separate state across mode changes. Existing static calendar-themed catalog images remain untouched. Calendar figures occupy a reserved lower area; positioning controls remain available. Calendar and final review use the same renderer/state.
- Size mapping is centralized: 1–2 figures = 15 × 20 cm; 4–5 = 20 × 25 cm; 6–8 = A4. Three figures explicitly require confirmation because the supplied rules overlap. No size/color surcharge is applied. CSS remains an approximate preview, not a physical-size proof.

### 2. Accessories and prices

- An accessory panel sits alongside the approved Стил builder. Heart, money and pistol each cost 70 ден.; pet costs 150 ден. Each supported item is toggled once per stable figure. Pet choices include three dogs and four cats shown in the supplied references. Switching variants does not add another pet charge.
- Missing heart/money/pistol images use generated transparent illustrations, authorized by the user's direct request. Pet cutouts were prepared with image assistance from the supplied product screenshots. All new accessory visuals are approximate previews; exact fulfillment appearance is subject to confirmation. Original screenshots and asset provenance are retained.
- Accessory overlays are separate from the character SVG compositor. The large character preview measures the actual character viewport to keep overlays aligned during resizing. Hidden figure selections are retained but excluded from the active total.
- One centralized utility computes base price, accessory lines/subtotal, delivery and total. Delivery is included exactly once at 170 ден. Backgrounds, photos, calendars, frame color and text add no surcharge. The estimate is labeled 2–3 business days, not a guaranteed date.

| Figures | Base | Total with delivery, no accessories |
|---|---:|---:|
| 1 | 1,290 | 1,460 |
| 2 | 1,690 | 1,860 |
| 3 | 2,090 | 2,260 |
| 4 | 2,490 | 2,660 |
| 5 | 2,840 | 3,010 |
| 6 | 3,190 | 3,360 |
| 7 | 3,540 | 3,710 |
| 8 | 3,890 | 4,060 |

Other verified totals: two figures + heart + pet + delivery = **2,080 ден.**; two figures + all four accessory types + delivery = **2,220 ден.** Price grouping is deterministic across server/browser rendering.

### 3. Order requests

- The review includes product/frame/design, personalization, readable per-character choices, accessories and complete pricing. Newborn details include face and baby-body color only; unsupported adult appearance fields are omitted from structured requests.
- Required name, phone, address and city are validated locally; an optional note is available. Phone handling permits Macedonian/international formatting, spaces, parentheses, slash and hyphens. Errors identify and focus the affected field. Contact state persists across steps; no personal information is logged or sent.
- A valid request can be prepared, copied as complete readable text or downloaded as structured JSON. Editing contact information invalidates the prepared state. Clipboard denial has a manual text-selection fallback.
- No verified business destination exists. The UI and request explicitly state **prepared, not submitted**; there is no invented submission confirmation.
- For local photographs, exports include filename, crop/position/zoom and `attached: false`. Browser object URLs are excluded. The UI explains that the original photo must be delivered separately. Selecting custom mode without a photo blocks preparation.
- The exact required product disclaimer is displayed in review without changing its wording.

## State and files

`Configurator.tsx` remains the owner of product configuration. New optional `frameColor` and per-character `accessories` fields extend `FrameConfiguration`. Calendar date lives in `backgroundSettings`; transient customer information is separate configurator-level state. Pricing, reviews and requests are derived from that configuration rather than maintained as duplicate totals or product snapshots. Background/text changes retain the memoized character subtree.

New implementation files in `components/product/`:

- `catalog.ts`, `calendar.ts`, `pricing.ts`: typed options, isolated size rules, calendar logic and pricing.
- `CalendarDesign.tsx`: date controls and dynamic SVG.
- `ProductOptions.tsx`: frame/accessory controls, independent overlays and price presentation.
- `order.ts`, `OrderReview.tsx`: validation, sanitized structured/text requests, review and copy/download UI.
- `product.module.css`: styles matching the existing design tokens.

Integration changes: `components/Configurator.tsx`, `components/FramePreview.tsx`, `components/config.ts`, `components/backgrounds/{catalog.ts,BackgroundCustomizer.tsx,BackgroundCustomizer.module.css,FrameBackground.tsx}`, `app/globals.css`, and `README.md`. The old audit test's obsolete white-only report note was corrected in `background-tests/test_background_audit.py`.

New assets/documentation: `public/accessories/` (10 active transparent images plus two retained prototypes and provenance notes), five original reference screenshots in `artifacts/upgrade/references/`, and this report. New tests: `upgrade-tests/product.test.cjs` and `upgrade-tests/test_upgrade.py`. No package dependency or npm-script changes were needed for this upgrade.

## Verification executed

- `npm run typecheck`: passed.
- `npm run lint`: passed with the same three pre-existing warnings: two raw homepage images and the anonymous PostCSS default export. No new warnings/errors.
- `npm run build`: passed; production preview restarted on port 3004.
- `node upgrade-tests/product.test.cjs`: **7,352 assertions**, including all base counts 1–8, all 16 accessory subsets, seven pet variants, hidden-selection exclusion, 2,412 calendar months across 1900–2100, century/leap rules, contact validation, photo URL sanitization and newborn fields.
- `upgrade-tests/test_upgrade.py`: white/black persistence, counts 1–8, seven pet variants and image decodes, automatic date clamping, month/year/circle synchronization, catalog/photo/calendar continuity, customer validation, actual clipboard contents, downloaded JSON and photo sanitization. Twenty calendar/figure bounds cases cover counts 1/2/4/8 at 1440/1024/768/390/320 px. Narrow pet-button labels are additionally checked. No runtime exceptions in the passing report.
- `background-tests/test_backgrounds.py`: all 110 selections/originals/thumbnails, nine categories, keyboard access, uploads/validation, photo positioning, URL cleanup, error/retry and five responsive widths passed.
- `background-tests/test_background_audit.py`: 30 text/composition cases passed.
- `background-tests/test_figure_placement.py`: 72 bounds cases passed.
- `background-tests/test_text_placement.py`: 12 bounds cases and optional-text/state checks passed.
- `character-tests/test_builder.py` with production flag: 207 face/hair combinations, 12 torso and 12 leg colors, four newborn faces, 12 baby colors, independent character retention, keyboard and responsive layouts passed. No runtime errors or failed requests.
- `npm run test:character-assets`: all 81 approved RGBA layers/masks passed.
- `background-tests/verify_assets.py` against the supplied ZIP: all 220 background images match byte for byte, decode and retain expected metadata/categories.
- `background-tests/test_gallery_loading.py`: passed; 110 options retain lazy loading. Request counts are viewport-dependent; see the raw loading report.
- Checksums for **335** existing Character Builder/character/background files: **zero changes**. All 12 new PNGs decode with alpha; see `preservation-report.json` and `accessory-assets.json`.

Browser evidence uses headless Google Chrome on macOS with responsive viewport sizes. It does not claim physical iOS/Android or cross-engine testing. Initial verification exposed and resolved currency hydration differences, narrow mode-button overflow, calendar SVG intrinsic sizing and narrow pet-label overflow. The final passing results supersede those intermediate failures.

Relevant evidence: `unit-report.json`, `browser-report.json`, `preservation-report.json`, `accessory-assets.json`, `calendar-desktop.png`, `accessories-mobile.png`, and `review-{1440,390,320}.png`. Existing regression reports remain in their original character/background artifact directories.

## Unresolved business details and limits

1. Confirm the frame size for exactly three figures. The UI/export explicitly leave it unresolved.
2. Supply a verified ordering destination before real transmission can be connected. Current copy/download behavior is intentionally local.
3. Confirm fulfillment availability and permitted accessory combinations/quantities. The demo provides at most one of each listed accessory per figure; no unlimited quantities or additional prices are invented.
4. Confirm exact missing accessory artwork when available. Generated illustrations and reference-derived cutouts are approximate; the newborn body remains the earlier provisional asset.
5. Uploads/configuration/contact details are temporary in-memory data. Photos are not attached to exported requests. Reloading clears changes. No print/export-production pipeline or automatic semantic collision detection was added.

Skills used: find-skills to select from the installed catalog, Vercel React Best Practices for state/render integration, imagegen for the authorized assets, and webapp-testing for browser verification. No additional skill installation was required.

## Follow-up notice review

The design hook flagged the notice's 2 px colored left border. It was removed; the warm notice background and padding remain. No detector suppression was added. The targeted detector returned no findings, the production rebuild passed, and desktop/mobile checks confirmed a 0 px border and no notice overflow. Evidence: `notice-review.json`, `notice-1440.png`, `notice-320.png`. The production preview was restarted.

The Impeccable context loader separately reported an older `.impeccable/design.json` schema. That unrelated metadata was left unchanged; the `document` command owns its optional refresh.
