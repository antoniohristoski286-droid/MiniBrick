# MiniBrick background configurator audit — 2026-10-23

## Confirmed findings and fixes

1. Four long names produced 548 px of text in a 210 px row. The preview hid the remaining names behind an ellipsis. Configurator copy now wraps fully; long groups use slightly smaller name typography. The fixed text slot preserves figure placement and scale. Measured offsets keep the entire text block within the printable interior at desktop and mobile sizes.
2. Dark text lost contrast on a dark uploaded photo. The optional **Подлога за читливост** setting provides a translucent backing. It sits behind the figures, while customer text stays in the foreground. It never changes the original image file and is hidden when all text fields are empty.
3. An unbroken review message increased frame interior width from 238.56 px to 243.13 px on the same viewport. Explicitly shrinkable grid tracks and wrapping review values now keep the frame and figures at the same size across Background, Text and Review.
4. A photo-upload test still used a broad vertical-slider locator after figure/text sliders were introduced. Its selector now targets the photo fieldset. Geometry tests now wait for entrance animations to settle before comparing scale.

## Verified functionality

- 110 original images and 110 thumbnails decode and match the supplied ZIP byte for byte. The full supplier manifest, original filename mappings, categories and warnings remain unchanged. BG014 stays excluded; seven approved review entries remain selectable.
- All 110 selections, nine category counts, Сите, selected indicators and keyboard activation passed in production Chrome.
- Filtering does not replace the selected background. Thumbnail/full-resolution mapping is verified for every entry.
- Opening the gallery requested one full-resolution image and 36 lazy-loaded thumbnails, rather than 110 full-resolution files. Frame geometry remained stable while a background request was deliberately delayed.
- Backgrounds remain clipped to the frame interior with `contain`; uploaded images support contain/cover, position and zoom without distortion.
- JPG, PNG and WebP uploads, landscape/portrait/square sources, the 10 MB limit, invalid/corrupt/empty files, replacement, removal, mode switching, final review and temporary URL cleanup passed.
- Four independent figures, text, figure placement and custom-photo placement survive step navigation. Background edits preserve the existing figure DOM nodes.
- 207 face/hair combinations, twelve torso colors, twelve leg colors, four newborn faces and twelve provisional newborn body colors passed the existing character regression. Count reduction/restoration preserved independent configurations.
- Thirty long-copy/backing/bounds cases passed at widths 1440, 1024, 768, 390 and 320. Twelve existing text-position cases passed, including optional empty fields. No horizontal overflow or runtime exceptions were observed.
- Homepage examples and approved character artwork were not changed.

## Checks

- `npm run lint`: exit 0; only the three existing warnings remain (two raw-image warnings in `app/page.tsx`, one anonymous default export in `postcss.config.mjs`). No new lint warnings or errors.
- `npm run build`: exit 0.
- `npm run typecheck`: exit 0.
- Production browser reports: `../test-report.json`, `audit-report.json`, `loading-report.json`, `../text-placement-report.json`, `../../characters/browser-test-report.json`.
- Figure-position regression: see `../figure-placement-report.json`.
- Asset checksums: `../asset-report.json`.
- Visual evidence: `before-long-text.png`, `after-long-text.png`, `before-dark-photo.png`, `after-dark-photo.png`, `after-mobile-390.png`, `after-mobile-320.png`.

## Files changed

- `components/FrameText.tsx` — new configurator text renderer, measurement and bounds handling.
- `components/FramePreview.tsx` — uses the focused text renderer for configured backgrounds; homepage examples retain their existing rendering.
- `components/TextPlacement.tsx` — optional readability backing, preserved independently of vertical-position reset.
- `components/config.ts` — optional backing flag on the existing text-layout state.
- `components/FigurePlacement.module.css` — styling for the readability checkbox.
- `app/globals.css` — wrapped text, fixed slot, backing layer, constrained grid and summary wrapping.
- `background-tests/test_background_audit.py` — focused composition and state-continuity checks.
- `background-tests/test_gallery_loading.py` — observed image loading behavior.
- `background-tests/test_backgrounds.py` — scoped photo slider selector.
- `background-tests/test_figure_placement.py` — waits for completed entrance animation before measuring geometry.
- `README.md` — audit behavior, verification and limitations.

No source backgrounds, thumbnails, IDs, metadata, category assignments, character assets or Character Builder components were modified. No application dependency was added.

## Limits of verification

Only the existing white frame is implemented. There is no black-frame option to verify; none was added.

Printed text and illustrations belong to the supplied raster images. Their meaning and location are not automatically detected. Customers can use the existing figure/text sliders and optional backing to choose a composition; arbitrary manual positions can still overlap printed details. No source artwork was removed or rewritten.

Responsive testing used headless desktop Google Chrome at mobile/tablet viewport sizes; physical iOS/Android devices and other browser engines were not tested. Uploads intentionally remain local and temporary while the configurator is mounted; no server persistence was added.
