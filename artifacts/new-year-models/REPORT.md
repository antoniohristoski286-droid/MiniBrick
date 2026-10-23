# New Year occasion, model reference and availability notices

Owner-requested changes:

- Renamed the twelve seasonal backgrounds to New Year (Macedonian UI: Novogodishni) and replaced the generic special-moment occasion card with a dedicated New Year occasion. It selects BG015; the standard initial/reset background remains BG018. Original background files, IDs, warnings and source filename mappings remain unchanged. The source inventory CSV retains its archival category names.
- Added shared model-availability copy to the character builder and final review. The exact existing product disclaimer remains intact, with a bold Macedonian Note label in the review, homepage footer and gallery footer.
- Added a newborn hat-and-tapered-body illustration based on the owner-supplied photo, retaining four independently selectable faces and twelve matching hat/body colors. New assets and their SVG sources are in public/characters/baby-reference/. The supplied reference and a generator that touches only this new folder are preserved under scripts/character-assets/. Previous newborn and all approved adult/child PNGs are unchanged.
- Scaled the complete child assembly to 88% about the common foot anchor (256, 714). Held accessories follow the same assembly matrix and remeasure after type changes. Mobile character previews stay in normal page flow so notices cannot cover editing controls.

Executed verification:

- npm run build, npm run typecheck, npm run lint: passed.
- node upgrade-tests/product.test.cjs: 7,448 checks passed.
- Asset validation: all 93 transparent PNG layers/masks passed. The twelve new baby colors have identical alpha silhouettes.
- Existing character-builder regression: 207 face/hair combinations, twelve torso colors, twelve leg colors, four newborn faces and twelve newborn colors; independent figures, retained settings, keyboard interaction and mobile options passed. Its initial-background expectation was updated to the previously approved BG018 default.
- Focused new-feature browser test: all twelve New Year originals decode; the occasion/filter, notices, child scale/foot anchor, accessory alignment and 1440/768/390/320 px layouts passed. No runtime exceptions or HTTP errors.

Evidence: report.json, baby-*.png, child-*.png, and the updated artifacts/characters/browser-test-report.json.
