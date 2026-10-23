# Product photo quality and larger team figures

Replaced all four low-resolution Instagram profile photos used by the site with the larger files served by their individual public posts. Original low-resolution files remain unchanged for recovery/provenance. New files use `-hq.jpg` names to avoid old optimized-image cache entries.

| Photo | Previous | New public-post file |
| --- | --- | --- |
| Birthday / hero | 530 × 640 | 1378 × 1663 |
| Family | 640 × 640 | 1248 × 1248 |
| Couple frames | 480 × 640 | 3024 × 4032 |
| Four-figure frame | 480 × 640 | 3072 × 4096 |

Files are copied directly from the public posts, without resizing, re-encoding, AI enhancement or alteration of photographed products. `sources.json` records source-post links and hashes. The hero keeps its original exterior-only CSS mask. Gallery metadata uses the correct larger dimensions, and hero/showcase/gallery/lightbox product photographs explicitly request Next image quality 90. Responsive image delivery and lazy loading remain in place; the site does not serve every image at its full size for every thumbnail.

The previously supplied 1078 × 1506 reference photograph was already a larger original and is retained, now also served at quality 90. Approved character layers, catalog backgrounds and intentionally small selection thumbnails were not artificially enlarged or replaced.

## Team previews

The landscape A4 preview can occupy the available pane width (up to 540 px, previously capped at 460 px). The assembled team SVGs receive a uniform 1.2 presentation scale, without changing parts, masks or Character Builder logic. Accessory anchoring continues to follow the SVG's actual coordinate transform.

Measured increases against the recorded pre-change baseline:

- Desktop 1440 px: 61% for 5/8/12 figures, 43% for 24.
- Mobile 390 px: 36% for 5/8/12 figures, 28% for 24.
- Mobile 320 px: 40% for 5/8/12 figures, 31% for 24.

Real nontransparent character artwork was checked in bounds, with no intersecting figure bounds, for all twelve count/viewport combinations. One-to-four portrait frames and the standalone editor retain their previous scale. Team count limits, pricing, frame colors, exports and orientation rules are unchanged.

## Verification

- TypeScript, ESLint and production build passed without warnings.
- 7,448 product unit assertions passed.
- `frontend-tests/test_photo_quality.py` passed cleanly: four larger sources, quality-90 retina delivery, twelve measured team cases, real artwork bounds/no overlaps, all gallery images and lightboxes; no runtime errors or failed requests.
- `frontend-tests/test_frame_sizes.py` passed cleanly: portrait four-figure rule, landscape teams, input validation, pricing/export/reset.
- Preservation hashes confirm the approved character/background/accessory assets and all four previous photo files remain unchanged.
- Existing authentic-content browser test passed cleanly: 40 desktop/tablet/mobile catalog/calendar cases, all five gallery lightboxes, supplied story, twelve-figure builder, no runtime errors or failed requests.
- The legacy product-upgrade bounds assertion now checks clipping against transformed nontransparent artwork, while retaining its minimum SVG viewport-size checks. This avoids treating empty SVG letterboxing as visible artwork. The suite passed cleanly: all seven pet variants, calendar dates/clamping, count pricing, 20 responsive cases and order validation/copy/export, with zero runtime errors.

Files changed: `app/page.tsx`, `app/globals.css`, `data/gallery.ts`, `components/ProjectGallery.tsx`, the authentic-content test's hero path assertion, the legacy upgrade test’s artwork bounds measurement, and README documentation. Added four `public/projects/*-hq.jpg` files, `frontend-tests/test_photo_quality.py`, and this artifact directory. No backend, dependencies, deployment or Git commits were added.
