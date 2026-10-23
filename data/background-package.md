# MiniBrick.mk — Website / Codex integration package

Contains 110 authentic client-supplied backgrounds from Archive.zip with the six name-removal edits already applied. BG014 is excluded (editor screenshot).

## Actual ZIP layout
- `backgrounds/BG001.jpg` ... `backgrounds/BG111.jpg` (except BG014): 110 complete-resolution JPGs.
- `backgrounds/thumbnails/BG001.jpg` ...: 110 smaller JPG thumbnails generated directly from those same photographs, not AI-generated.
- `manifest.json`: 111 catalog entries (110 with real `src` and `thumbnail`; BG014 excluded), nine category definitions, per-item flags and statuses.
- `inventory.csv`: original-to-background mapping and audit information.

## Installation
1. In existing Next.js repo, copy `backgrounds/` directly under `public/`, resulting in `public/backgrounds/BG001.jpg` and `public/backgrounds/thumbnails/BG001.jpg`.
2. Copy `manifest.json` to a suitable project data directory (for example `src/data/minibrick-backgrounds.json`) and load it from local source code.
3. Filter only entries with non-null `src`/`thumbnail`; exclude `status: excluded` / BG014. The owner has reviewed and approved the provided selections for the demo, including `status: review`; preserve warnings for production QA rather than removing assets silently.
4. Keep `id`, category, `src`, `thumbnail` exactly as in the manifest and show all nine category filters. Do not generate replacement backgrounds or fabricate missing artwork.
5. Important: some JPGs include fixed pre-printed calendar dates; interactive calendars are a separate feature. A few designs contain visible third-party brand text or a small creator signature; confirm rights/branding before public production release.

All public website-facing text should be Macedonian. Preserve existing character customization and frame live preview.
