# Client project gallery replacement

Source: `/Users/antoniohristoski/Downloads/Archive 2.zip`.

All 50 JPEG photos were copied byte-for-byte to `public/projects/client/` with their original filenames. Finder metadata was excluded. SHA-256 checks and byte comparisons against every ZIP entry passed. EXIF-oriented dimensions are recorded in `manifest.json`; originals were not resized, edited or regenerated.

The gallery now displays all 50 client photos, with a mix of individual, family, team and calendar examples first. Both homepage gallery preview photos use the same collection. Photos are shown in full, with quality-90 responsive image delivery and the existing keyboard-accessible enlargement. Former Instagram gallery entries and attribution links were replaced; previous assets remain on disk. The hero, story, approved character builder, 110 configurator backgrounds and team sizing were preserved.

Verification executed for this change:

- `npm run build`, `npm run typecheck`, `npm run lint`: passed.
- All 50 gallery thumbnails and all 50 enlarged images decoded successfully.
- Escape closed every enlargement and restored focus to its trigger.
- No horizontal overflow at 1440, 768, 390 or 320 px.
- Both homepage gallery photos decoded; the hero retained its original birthday photo; the five-step configurator remained present.
- No browser runtime exceptions or HTTP error responses.

Evidence: `browser-report.json`, `gallery-1440.png`, `gallery-390.png`, `homepage-gallery.png`. Contact sheets are inspection derivatives only. Source files remain unchanged.
