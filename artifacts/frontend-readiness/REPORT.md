# MiniBrick.mk — frontend readiness and production-gap report

Date: 2026-10-23, Europe/Skopje.

## 1. Scope and release status

The user explicitly clarified that backend development comes later and that the current work is the frontend. This pass therefore completes safe frontend improvements and audits the existing configurator. **The complete website is not ready to accept real orders.** No order API, database, durable image storage, payment provider, notification service, cloud project or production deployment was created.

The source handoff and earlier artifact reports describe historical checkpoints. This report and `SCOPE.md` record the current frontend-only direction. Existing modified/untracked files were preserved; no commit, push, cleanup or asset regeneration was performed.

## 2. Verified features and classification

“Production-ready frontend” below describes the inspected/tested UI behavior only; it is not approval to launch a commercial ordering service.

| Feature | Classification | Actual status |
|---|---|---|
| Modular Character Builder | Production-ready frontend behavior | Nine heads, 27 faces, twelve torso/leg colors, independent stable figures, hidden-count retention and keyboard controls verified. Approved source/artwork unchanged. |
| Newborn appearance | Incomplete product artwork | Existing baby face/body controls work; body remains explicitly provisional. No replacement was generated. |
| Catalog backgrounds | Production-ready frontend behavior; production artwork review outstanding | All 110 originals/thumbnails and nine categories verified. BG014 remains excluded; seven supplier review flags remain intact. |
| Custom photograph preview | Production-ready local frontend behavior | JPG/PNG/WebP validation, decode, crop/zoom, cancel/replace/remove, URL cleanup and state continuity verified. No upload is sent to storage. |
| Calendar | Production-ready frontend behavior | Correct Monday-first grids, leap rules, month/year/day controls, selected-day circle, persistence and final-preview consistency verified. Existing static calendar artwork unchanged. |
| White/black frames | Production-ready frontend behavior | Immediate CSS exterior change, state persistence and review/export values verified. |
| Frame-size selection rules | Confirmed and implemented | User confirmed 15 × 20 cm for 1–3 figures, 20 × 25 cm by default for 4+ figures, and optional A4 team frames from four figures. Review and exports use the selected effective size. |
| Accessories | Functional frontend; final artwork/fulfillment incomplete | Independent selections, seven pet variants, approximate overlays and charges verified. Existing generated/reference-derived images retained; no new product art. |
| Prices | Production-ready client calculation; server authority incomplete | Counts 1–8, accessory combinations, hidden selections and 170 MKD delivery verified. An eventual order endpoint must validate/calculate its own total. |
| Text/figure positioning | Production-ready frontend behavior | Optional fields, long text, readability backing, independent movement and responsive bounds verified. User-approved heading and expanded preview explanation preserved. |
| Order review/contact form | Production-ready local preparation behavior | Validation, focus, copy/download, per-character details and consistent totals verified. Copy denial recovers without losing data. |
| Actual order submission/records | Deferred by user | No receiver, durable record, server receipt, order ID/status or timestamp exists. No success message claims otherwise. |
| Durable private photo storage | Deferred by user | Browser URLs are temporary. Export includes name/crop and explicitly marks the photo as not attached; object URLs are excluded. |
| Public business content | Functional frontend; factual content incomplete | Supplied authentic product photo retained; unsupported reviews/contact link removed. No fabricated history or projects added. Official contact and further real gallery material remain missing. |
| Privacy/legal | Current behavior documented; production policy incomplete | Working `/privacy` page accurately explains local processing. Full business identity, rights/contact, retention and order-processing policies remain required before receipt of orders. |
| Search/distribution | Prepared for frontend development | Macedonian metadata, semantic routes and localized 404 exist. `noindex` is intentional until a verified public release. Deployment-specific canonical URLs/sitemap are not invented. |

## 3. Problems found and fixed

1. The footer claimed “Без обработка на лични податоци” although the form processes contact information in browser memory. Replaced this claim and added accurate local-data information, linked from the form and footer.
2. Instagram linked to the generic service homepage rather than a verified business profile. Removed the destination and state honestly that the official ordering contact is not yet published.
3. Three fictional testimonials were still present, albeit labeled as demo examples. Replaced that section with factual FAQs derived from existing functionality and confirmed delivery information.
4. Real-work navigation, FAQ and privacy links were unclear/misleading. Added meaningful gallery/story/FAQ anchors, retained the genuine supplied photograph, labeled the adjacent rendered example as illustrative, and added a real information route.
5. Keyboard users lacked a skip link, mobile-menu Escape/focus return, deliberate configurator step focus and prepared-output focus. These are now implemented with native semantics and preserved configuration.
6. Small mobile input typography could trigger unwanted keyboard zoom. Editable phone-sized input/select/textarea fields now use at least 16 px type.
7. The logo/product photo and small accessory thumbnails loaded large native PNGs. Next Image now serves responsive optimized versions without changing originals. Catalog thumbnails and modular SVG renderer retain their existing asset/loading paths.
8. The expanded desktop navigation overran the 768 px viewport by roughly one pixel. Tablet widths now use the existing collapsible menu; subsequent responsive checks pass.
9. A hidden line break joined heading words on phones. Added ordinary separating whitespace for the configurator and new FAQ heading.
10. The default missing-page UI was English. Added a Macedonian 404 page; updated the production QA assertions while retaining actual 404 behavior.
11. Existing lint warnings for two raw homepage images and anonymous PostCSS export were resolved through image optimization and a named config export.
12. Dependency auditing identified runtime advisories, including a critical Next.js advisory. Applied the same-major patch and narrow transitive fixes described below.

## 4. Architecture and data handling

The existing Next App Router, React local state, configurator ownership, immutable character helpers and memoized shared renderer remain. No duplicate product state or new state-management library was introduced.

`Configurator.tsx` adds a pending-focus target/ref for explicit step navigation. `OrderReview.tsx` adds prepared-heading focus and a copy-in-progress state; the same current configuration still derives visible and structured request details. Contact data remains at configurator level across steps. Clipboard failure selects the complete existing request for manual copying. Download uses a temporary browser URL with cleanup.

`CustomerInfo.tsx` supplies factual FAQs and the exact shared product disclaimer. `/privacy` is a factual explanation of current behavior, not a fabricated final business policy. Privacy opens in a separate tab to preserve the active frame/photo/contact state. No localStorage, analytics service, cookie consent claim, remote file upload or customer-data log was added.

## 5. Real ordering and image storage

There is no existing order API/service/database/storage/deployment integration or project environment configuration to reuse. The user has explicitly deferred implementing it. Consequently:

- Preparing, copying or downloading a request does not transmit it to MiniBrick.
- No durable order record or reliable business receipt exists.
- No successful real-order submission was simulated or claimed.
- Local photo preview remains temporary and is not attached to exported requests.
- No private customer-image URLs are made public or included as remote URLs.
- Server-side validation, authoritative pricing, authorization, distributed abuse controls, idempotency and partial-failure handling are future backend work, not completed security features.

Future isolated backend tests must cover actual storage/receipt, retries, duplicates, invalid files and failures before any live orders are accepted. Those tests were intentionally **not** run against a fake service in this frontend pass.

## 6. Security/dependencies

Installed Next.js and its ESLint config were updated from 15.5.26 to **15.5.28**, preserving major version 15. The resulting Next image dependency is **sharp 0.35.5**. The Next-specific PostCSS override resolves to **8.5.31**, and source-map-js to **1.2.2**. Lockfile changes are included. No service/backend SDK was added.

The maintainer identifies Next 15.5.28 as patched for the image-optimization advisory: [vercel/next.js advisory](https://github.com/vercel/next.js/security/advisories/GHSA-2464-fhr4-w9xw). Related audit evidence and advisory URLs are preserved in the raw audit JSON.

- Initial full `npm audit`: one critical and seven high findings.
- Final runtime `npm audit --omit=dev`: **zero known findings** in that audit.
- Final full `npm audit`: **five high development-toolchain findings remain**, rooted in the braces → micromatch → fast-glob → Next ESLint chain. npm's proposed automated resolution is a breaking downgrade to ESLint config 14.2.35; it was not applied. The registry's braces latest was 3.0.3, which is still in the reported affected range. These are documented, not falsely reported as resolved.

Response headers now include nosniff, DENY framing, strict-origin referrer policy, restricted camera/microphone/geolocation permissions, and compatible CSP directives for frame ancestors, base URI, objects and form action. This is a partial CSP, not a claim of a complete script policy. No application secrets or private server data are exposed to the frontend.

## 7. Prices tested

| Figures | Base MKD | With 170 MKD delivery and no accessories |
|---|---:|---:|
| 1 | 1290 | 1460 |
| 2 | 1690 | 1860 |
| 3 | 2090 | 2260 |
| 4 | 2490 | 2660 |
| 5 | 2840 | 3010 |
| 6 | 3190 | 3360 |
| 7 | 3540 | 3710 |
| 8 | 3890 | 4060 |

Two figures + heart + pet + delivery = 2080 MKD. Two figures + all four accessory kinds + delivery = 2220 MKD. All sixteen accessory subsets, seven pet variants and exclusion/restoration of hidden figure selections passed existing tests. These are client calculations, not authoritative order creation.

## 8. Performance, responsiveness and accessibility

- Desktop/tablet/mobile widths 1440, 1024, 768, 390 and 320 px were exercised in headless Google Chrome; no horizontal overflow in passing runs.
- Skip-link focus, explicit step-region focus, native FAQ keyboard activation, mobile/tablet menu Escape/focus return, contact-error focus, prepared-output focus and clipboard failure recovery passed.
- The privacy page was checked at desktop and 320 px. Opening it did not lose the existing local photo/configuration/contact data.
- The supplied product photo is 2,126,642 bytes. One measured 828 px WebP optimization response was **57,178 bytes**, approximately 97.3% smaller. This is a specific representation measurement, not a Web Vitals guarantee; other viewport/format/quality responses vary.
- Source images and approved art were not edited or regenerated. Optimized thumbnail responses successfully decoded.
- No physical iOS/Android, assistive-technology, cross-engine, production-network or field Core Web Vitals result is claimed. Large group/long-copy bounds are covered by existing browser regressions.

## 9. Verification executed in this pass

- `npm run typecheck`: passed.
- `npm run lint`: passed with zero errors and zero warnings.
- `npm run build`: passed using Next 15.5.28; intended production preview restarted on port 3004.
- `node upgrade-tests/product.test.cjs`: passed, 7,352 assertions, including 2,412 calendar months and pricing/order-sanitization checks.
- `frontend-tests/test_frontend.py`: passed. Covers navigation anchors, five viewports, keyboard/focus, FAQ, privacy/new-tab state, optimized images, real response headers/noindex, validation, copy-denial recovery, JSON download, local-photo handling and HTML-like notes rendered as text. No personal-data POSTs, runtime exceptions or unexpected failed requests were observed.
- `upgrade-tests/test_upgrade.py`: passed, including seven pet decodes, frame/calendar/accessory/count persistence, actual clipboard/download checks, sanitized photo metadata and twenty responsive calendar/figure cases.
- `background-tests/test_backgrounds.py`: passed all 110 originals/thumbnails/selections, nine category counts, upload formats/validation/crop/cleanup/error-retry and responsive checks.
- `character-tests/test_builder.py` with production flag: passed 207 face/hair combinations, twelve torso and leg colors, newborn variants, independent state/count retention and responsive checks.
- `character-tests/production_smoke.py`: passed homepage, character controls, 81 image endpoints, responsive widths and development-gallery 404 exclusion.
- `background-tests/test_background_audit.py`: passed thirty composition/long-copy cases.
- `background-tests/test_figure_placement.py`: passed seventy-two bounds cases.
- `background-tests/test_text_placement.py`: passed twelve bounds cases and optional-field/state checks.
- `npm run test:character-assets`: passed 81 RGBA layers/masks and geometry/transparency checks.
- `background-tests/verify_assets.py` against the original supplied ZIP: all 220 images decode and match byte for byte; mappings and warnings retained.
- Preservation comparison: **348 existing builder and asset files, zero changes**. Supplied logo/product PNGs also remain unchanged in Git.
- Dependency audits were executed and saved separately; the full audit remains nonzero for the development findings above.

The first responsive run exposed the tablet navigation issue; the passing rerun supersedes it. The 404 test assertion was localized to match the intentional new page. Viewport checks wait for resizing to settle before checking computed typography. Reports are actual current executions, not merely quotations from the handoff.

## 10. Files changed

New:

- `components/CustomerInfo.tsx`
- `app/privacy/page.tsx`
- `app/not-found.tsx`
- `next.config.ts` (frontend-serving headers)
- `frontend-tests/test_frontend.py`
- `artifacts/frontend-readiness/` evidence/report files

Modified:

- `app/page.tsx`: truthful public content, verified/illustrative distinctions, image optimization, navigation and menu keyboard behavior.
- `app/layout.tsx`: skip link and prelaunch noindex metadata.
- `app/globals.css`: FAQ/privacy styles, accessible navigation, tablet menu, input typography and numeric presentation.
- `components/Configurator.tsx`: deliberate step focus and normal heading whitespace.
- `components/product/ProductOptions.tsx`: optimized small images.
- `components/product/OrderReview.tsx` and `product.module.css`: output focus, copy state, privacy link and disclaimer reuse.
- `package.json` / `package-lock.json`: same-major security patch and scoped overrides.
- `postcss.config.mjs`: named export object, resolving its old lint warning.
- `character-tests/test_builder.py` / `production_smoke.py`: Macedonian missing-page expectations.
- `PRODUCT.md` / `README.md`: current frontend-first direction and verification/launch limits.

Approved `components/characters/`, background originals/thumbnails, character assets, accessory originals, supplier metadata and the handoff were preserved. There is no new order API or database file.

## 11. Information and decisions still required

- Verified official contact/profile, legal business identity and approved delivery/payment/privacy/retention information.
- Authentic additional completed-work images and any factual founder/story material before expanding those claims.
- Exact final missing accessory/newborn artwork and fulfillment/combination decisions.
- Backend architecture/hosting/storage decisions and credentials **when the user resumes backend work**, not during this frontend-only phase.

## 12. Before public launch

Complete and verify real order receipt/storage, private image persistence/access, authoritative validation/pricing, retry/idempotency/abuse controls and failure recovery. Publish approved business/policy/contact information, resolve the remaining development dependency findings, verify physical-device/accessibility behavior, and perform an isolated end-to-end real-order test. Only then activate search indexing/canonical/sitemap metadata for the actual production deployment and consider launch. No deployment or live business data was touched in this pass.

Evidence directory includes `audit-before.json`, `browser-report.json`, `preservation-report.json`, `image-optimization.json`, the three `npm-audit-*.json` reports, before/after screenshots, FAQ/footer captures and desktop/mobile privacy captures. Existing configurator regression reports remain in their original artifact directories.

## Confirmed frame-size follow-up

Applied the user-approved mapping: 1–3 figures use 15 × 20 cm; 4–8 default to 20 × 25 cm and can select an A4 team frame. A4 preference never changes the effective size below four figures, and reset restores the standard choice. Review, copied text and JSON use the effective size; existing prices remain unchanged.

Validation: production build (including lint/type checking), 7,420 product assertions, and `frontend-tests/test_frame_sizes.py` passed. Browser checks cover all eight counts, both choices, lower-count guarding, review/text/JSON export, reset, unchanged prices, and 390/320 px layouts with no runtime errors.
