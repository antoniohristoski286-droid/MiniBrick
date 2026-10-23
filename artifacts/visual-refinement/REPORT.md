# MiniBrick.mk — Story, gallery and configurator visual refinement

Frontend-only work completed in the three requested phases. No backend, API, database, upload service, payment flow or deployment was added. Existing modified/untracked work was retained.

## 1. Нашата приказна

Refined the existing `/#about` section rather than creating a duplicate navigation path. Cream surfaces, the supplied MiniBrick heart logo, existing dark/serif typography and red accents retain the site's visual language. The section offers customization and gallery links.

No verified business history, founding year, founder message or manufacturing account was available. The story explicitly says that the full story will be shared later. Its introduction and pending text are centralized in `data/gallery.ts` for replacement with client copy.

## 2. Галерија / Наши изработки

Added `/gallery`, with Macedonian metadata, a responsive image grid, enlargement on hover/click, native modal lightbox, Escape dismissal, close button and focus restoration, plus a clear configurator CTA. The homepage showcase and story link to it in a new tab so the existing configurator remains open.

The repository contains one supplied authentic product reference photograph, `public/minibrick-products.png`. This is the only gallery entry. It is labeled as a supplied reference photo, without invented customer names, dates, project titles or categories. No generated artwork or preview render is passed off as completed customer work. The simple typed gallery data array can accept additional authentic photos; the component also has a Macedonian empty state if that array is empty.

## 3. Accessory appearance

Retained every original accessory file. The existing heart, money and gun illustrations had substantial transparent canvas padding; rendering them inside another square SVG, with pixel height caps, made them tiny and uneven. Presentation-only SVG view boxes now frame the useful artwork consistently in both selection cards and previews. Selection cards have reserved image areas and clearer labels.

Each accessory uses a proportional slot, scaled against the rendered character canvas, with separate positions for heart, money and gun. Both editor and framed previews use the same SVG-coordinate measurement, excluding letterboxing and accounting for parent animation. Removed the previous stacked tiny thumbnails and absolute pixel caps. Approximate-art notices remain; no photorealistic replacement or misleading product art was invented. Pets, per-character selections and prices are retained.

## 4. Character customization UI

Refined spacing, group separators, rounded control corners, active choices, focus indicators and the standalone editor preview size. Tablet type/accessory grids adapt to two columns to prevent label overflow. All original face, hair, torso, legs, baby options, stable character IDs and assembly logic remain intact. The standalone editor deliberately stays larger than the framed group so facial and clothing choices can be inspected.

## 5. Figure scale and placement consistency

Removed calendar-specific frame-width and figure-row overrides. Catalog, photo and calendar now share the same frame width and the same interior-relative figure region. The region no longer depends on text height or background mode. A stable reserved text slot keeps default names below figures at small sizes, while text/figure movement controls remain independent. Tablet previews use a stacked layout for adequate space. Count-specific layouts retain one row through four figures and two rows for larger teams.

Maximum spacing is bounded for three/four figures in the expanded full-interior scene. This prevents outer SVGs crossing the frame at wide settings. Count changes and accessories do not replace the approved figure compositor.

## 6. Full frame coverage

Catalog layers render centered `cover` across the complete `.frame-art` interior, without distortion. Source aspect-ratio differences can crop edges; originals are untouched. Custom photos default/reset to `cover`, with existing x/y and zoom controls retained. The optional whole-photo mode keeps the entire foreground photo over a soft full-bleed backdrop from the same photo, so there are no uncovered bands.

Calendar mode has a full-interior paper layer, with its dynamically generated calendar placed in the upper area and the common figure scene beneath it. Month, year, days and selected-day circle still derive from the selected date. Frame borders, bevel and shadowbox remain visible. The same `FrameBackground` / `FramePreview` components serve background, text and review steps.

## 7. Files created or changed in this pass

Created:

- `app/gallery/page.tsx`
- `components/ProjectGallery.tsx`
- `data/gallery.ts`
- `frontend-tests/test_visual_refinement.py`
- `artifacts/visual-refinement/` plan, preservation manifest/report, browser report and screenshots.

Changed:

- `app/page.tsx` — story section and gallery entry links.
- `app/globals.css` — supporting content, consistent frame scene and accessory layout.
- `components/Configurator.tsx` — photo default/reset fit.
- `components/FramePreview.tsx` — bounded group spacing and shared accessory positioning.
- `components/backgrounds/FrameBackground.tsx` and `FrameBackground.module.css` — coverage/backdrop/calendar paper.
- `components/backgrounds/BackgroundCustomizer.tsx` and `catalog.ts` — fit default/reset and explanation.
- `components/characters/characters.module.css` — presentation only.
- `components/product/ProductOptions.tsx` and `product.module.css` — accessory view boxes, selectors and positioning.
- `background-tests/test_backgrounds.py` — expected cover behavior and foreground-image selector.
- `background-tests/test_figure_placement.py` — movement metrics relative to frame, avoiding page-scroll artifacts from the taller preview.
- `README.md` — current behavior and gallery/story documentation.

`git diff --stat` includes work from earlier sessions because much of this repository is already modified/untracked; it is not a list of changes introduced only by this pass.

## 8. Validation

Final results:

| Check | Result |
| --- | --- |
| `npm run typecheck` | Passed |
| `npm run lint` | Passed, no warnings |
| `npm run build` | Passed; `/gallery` statically generated |
| `git diff --check` | Passed |
| Product unit tests | Passed, 7,420 assertions |
| Character asset validator | Passed, 81 original RGBA assets |
| Character Builder browser tests (production flag) | Passed: 207 face/hair combinations, all 12 torso/leg/baby colors, four baby faces, independent state, keyboard and four widths |
| Background browser tests | Passed: all 110 originals/thumbnails/selections, nine categories, upload formats/validation/crop/cleanup/error-retry, five widths |
| Text placement browser tests | Passed, 12 responsive bounds cases |
| Frontend readiness browser tests | Passed: navigation, focus, validation, local photo, privacy, clipboard denial/download, no personal-data requests, no runtime/request errors |
| Confirmed frame-size browser test | Passed: eight counts, standard/A4, lower-count guard, review/export/reset and unchanged prices |
| New visual-refinement test | All assertions passed: 64 geometry comparisons, counts 1–8, widths 1440/768/390/320, full coverage including whole-photo backdrop, default text separation, final/text consistency, story/disclaimer and gallery lightbox |
| Figure placement browser test | All assertions passed, 72 extreme position/spacing cases with real artwork bounds |
| Product upgrade browser test | All assertions passed, including responsive calendar/figures, pets, pricing and request export |

The last three browser scripts saved their successful reports, then the local installed-Chrome/Playwright shutdown hung after the browser had exited. Those test processes were interrupted during teardown. They did **not** exit cleanly; this is recorded separately from the successful assertions and zero website runtime errors. Explicit page/context cleanup did not remove the tooling hang, so unnecessary teardown changes to existing scripts were reverted. The same Chrome teardown delay was observed before this task. No production dependency or browser installation was changed. Initial checks caught and corrected inherited story colors on the new cream surface, tablet button overflow, default names/feet overlap and maximum group-spacing overflow. The legacy background tests were updated for the intentionally requested cover default and optional whole-photo backdrop. Character tests use their existing production flag because `/dev/characters` correctly returns 404 in production.

## 9. Preservation and limits

SHA-256 verification covers 347 pre-existing files: public assets, approved character TSX source and background manifest. All are unchanged; none missing. The approved Character Builder logic and source assets remain intact. The exact supplied legal disclaimer remains in the homepage footer and gallery footer. The requested preview disclaimer, confirmed frame sizing/A4 choice, color options, prices, upload validation/cleanup, calendar behavior and local order preparation are preserved.

Business owner content still needed: the approved real story and additional authentic completed-work photographs/captions. No fabricated history or portfolio entries were added. Supplied reference-photo screenshot overlays remain part of the original photo. The frame remains an approximate visual composition, not print-ready output. Catalog cover may crop printed details; figure/text controls let customers adjust composition. Extreme user-selected text/figure positions can overlap intentionally.

Validation uses desktop Chrome with emulated tablet/mobile viewports, not physical devices or cross-browser certification. Existing backend and real order submission remain deferred. No warnings were suppressed and no ignores were added.

## Skills used

Used the explicitly requested find-skills workflow, then the already installed frontend-design and webapp-testing skills. The [skills.sh leaderboard](https://skills.sh/) and [official Anthropic skill repository](https://github.com/anthropics/skills) were checked before selection; no installation or dependency addition was necessary.
