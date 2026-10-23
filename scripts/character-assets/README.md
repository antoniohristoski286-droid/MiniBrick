# MiniBrick character assets

The source catalogs are stored in `references/` for reproducible processing. The application never displays or loads a complete catalog as a character layer.

## Preparation and provenance

- **H01–H09:** extracted from the supplied opaque head catalog. Border-connected background flood filling preserves enclosed artwork and dark outlines; the largest connected silhouette removes disconnected catalog labels. The background predicate is applied only to the exterior flood, never as a global RGB color key. Each head is uniformly scaled using its exposed face width and bottom connection. No independent hair recoloring is offered. The original silhouette alpha is retained exactly; `head_style.py` normalizes existing color regions into flat family palettes and draws a three-unit interior ink contour. Exposed skin and all C-shaped hands use the same peach `#ffc78e`.
- **F01–F13, M01–M06, C01–C04, B01–B04:** retained from the supplied RGBA sheet. Its actual alpha range is 0–254. Controlled per-expression bounds exclude labels; alpha values below 16 are suppressed to remove faint source residue. Expressions are positioned around a common eye-line anchor without changing their aspect ratios. White eyes and printed dark details are retained.
- **T01–T12 and L01–L12:** carefully reconstructed as flat SVG tracings of the supplied silhouettes, with the twelve source colors sampled from the torso sheet. PNGs are exported from those SVGs. Every color shares exactly the same geometry and alpha silhouette. Sleeves inherit the selected torso color; the two existing hand paths explicitly use the common skin fill, independent of the torso. No gradients, patterns, neck studs, or leg connectors are added.
- **BC01–BC12:** current newborn hat/body variants in public/characters/baby-reference/, based on references/baby-client-reference.png supplied by the owner. The crown, brim and tapered body share the selected palette color; B01–B04 remain independent face decals. Run node scripts/character-assets/render-reference-baby.mjs to regenerate only these twelve variants. The former provisional baby/ files remain preserved.

The source catalogs have raster edges, so head silhouettes and decals retain the original edge alpha. Head color gradients are flattened into solid color regions without moving those edges. Torsos/legs are flat reconstructions rather than pixel-identical crops. All requested IDs are present; no catalog labels or rectangular catalog backgrounds are part of the exported layers.

## Shared coordinates

All body/head PNGs use a transparent **512 × 768** canvas. Faces use a transparent **240 × 180** source canvas and are placed using typed head metadata.

- Head/body connection: `(256, 280)`.
- Torso/waist connection: `(256, 466)`; silhouettes overlap by two logical units to prevent antialias gaps.
- Head exposed width: approximately 140 logical units.
- Face source eye-line anchor: `(120, 70)`.
- Per-head face placements and exposed-skin masks follow the supplied fringe contours. A unique SVG alpha mask clips every face decal to the exposed head; no facial mark can print over hair.
- The complete SVG scales uniformly. Thumbnails use alternate SVG viewBoxes, not independent CSS offsets for individual pieces.

`components/characters/catalog.ts` is the typed manifest for IDs, categories, display names, paths, canvas dimensions, bounds, and anchors. `state.ts` handles selection changes separately from `MiniBrickCharacter.tsx` rendering.

## Reproduce

Python asset tooling requires Pillow and NumPy. The application itself does not require Python.

```bash
python3 scripts/character-assets/prepare.py
node scripts/character-assets/render-vectors.mjs
npm run test:character-assets
```

The vector exporter uses the Sharp installation already supplied with Next.js. Asset checks verify all 81 PNGs, transparent corners, exact canvas sizes, preserved white regions, identical body silhouettes across colors, absence of top studs, and continuous body connections. Contact sheets and source-channel inspection metadata are saved under `artifacts/characters/`.

Targeted visual regression checks: `python3 scripts/character-assets/validate-refinements.py`. This compares the preserved pre-refinement silhouettes, confirms both hands share the head skin color for every torso, and checks unchanged UI/state files and newborn assets.

The five fuller/longer hairstyles H01–H05 use display scales of 0.75–0.82 from `public/characters/head-display.json` to balance their volume with short hair. The renderer scales the head, face, and mask together about `(256, 280)`. Source assets and silhouettes are unmodified, and the neck remains fixed.

Child figures use a shared SVG assembly transform of 0.88 about (256, 714) so their feet stay aligned. All layers scale together, and held accessory positioning follows the assembly matrix. Original head/torso/leg PNGs remain unchanged. The newborn face placement is defined by CHARACTER_COORDINATES.babyFace.
