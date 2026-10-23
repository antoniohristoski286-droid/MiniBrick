# MiniBrick.mk — Codex Project Handoff

**Checkpoint: 2026-10-23, Europe/Skopje.**

This document is for a fresh Codex conversation continuing the existing repository. It is a documentation handoff, not authorization to implement the roadmap. **Read this entire document, inspect the current files, and wait for the user's next specific development instruction before editing application code.**

## 1. Project overview and operating environment

MiniBrick.mk is a Macedonian personalized-gift business concept: framed keepsakes assembled with small brick-style human figures, authentic backgrounds, optional names, messages and dates. The website is a premium client demo intended to present the product and let customers configure an approximate live preview. It is an existing, working website, **not a project to restart or rebuild**.

### Repository and runtime

- Absolute repository root: `/Users/antoniohristoski/programiranje/MiniBrick`.
- Local environment: macOS, zsh. Customer timezone: `Europe/Skopje`.
- Package manager: npm; `package-lock.json` exists, lockfile version 3. Its root dependency declarations match `package.json` at handoff.
- Current Git branch: `main`; current HEAD: `0bc86c7` (`Initial commit`).
- Configured origin: `https://github.com/antoniohristoski286-droid/minibrickdemo.git`. This does **not** establish that recent working-tree changes have been pushed or deployed.
- Many completed implementation files are **untracked**, and several original files are modified. The Git checkpoint is much older than the implemented application. Preserve the working tree; never reset, clean, or recreate the checkout from HEAD to “restore” the project.
- Local production server was verified listening on port **3004**; `http://localhost:3004/` returned HTTP 200 during this handoff. Preview URL: `http://localhost:3004/#configurator`. `.next/BUILD_ID` exists.
- Server availability is transient: inspect `lsof -nP -iTCP:3004 -sTCP:LISTEN` before starting another server. The existing process is the production Next server from the last development task.
- No production hosting/deployment configuration, deployed URL, backend, database, payment system or authentication integration is established in the inspected application. Do not infer deployment from the Git remote.

### Verified installed toolchain

Versions below came from `node --version`, `npm --version` and `npm ls --depth=0` during this documentation task. Package ranges are not the same as installed versions.

| Tool/package | Installed | Declaration, if applicable |
|---|---:|---|
| Node.js | 24.21.0 | No engine pin in package.json |
| npm | 11.19.0 | npm lockfile present |
| Next.js | 15.5.26 | `^15.5.0` |
| React / React DOM | 19.3.0 | `^19.1.0` |
| TypeScript | 5.9.3 | `^5.9.2` |
| Tailwind CSS / PostCSS adapter | 4.3.3 | `^4.1.0` |
| Framer Motion | 12.43.0 | `^12.23.0` |
| Lucide React | 0.468.0 | `^0.468.0` |
| ESLint | 9.39.5 | `^9.35.0` |
| eslint-config-next | 15.5.26 | `^15.5.0` |
| @types/node | 22.20.4 | `^22.18.0` |
| @types/react / @types/react-dom | 19.3.0 | `^19.1.0` |

The application uses Next App Router, strict TypeScript, React local state, global CSS and CSS Modules. Tailwind v4 is imported in global CSS, but much of the actual styling is authored CSS rather than utility-heavy JSX. No global state library is used. There is no custom `next.config.ts` in the inspected root. `tsconfig.json` defines `@/*` as the repository root, enables `resolveJsonModule`, and includes `.next/types/**/*.ts`.

## 2. Repository map

All paths in this document are relative to the repository root unless explicitly absolute.

```text
app/
  page.tsx                         Client homepage and inline marketing sections
  layout.tsx                       Macedonian HTML language, metadata, global stylesheet
  globals.css                      Shared design, physical frame, configurator and composition CSS
  dev/characters/page.tsx           Development-only character QA route; production returns 404
components/
  Configurator.tsx                  Five steps, canonical config state and demo order modal
  config.ts                        FrameConfiguration, defaults and legacy background presets
  FramePreview.tsx                  Existing physical frame + background + memoized figure group + text
  FrameText.tsx                     Configurator text measurement, wrapping, bounds and backing layer
  FigurePlacement.tsx               Whole-group vertical position and spacing controls
  TextPlacement.tsx                 Text vertical position and optional readability backing
  FigurePlacement.module.css        Shared composition-control styles
  characters/
    catalog.ts                     Typed character asset metadata, palettes, anchors and IDs
    state.ts                       Immutable character creation/update/count helpers
    MiniBrickCharacter.tsx           Approved modular SVG compositor
    CharacterBuilder.tsx            Controls plus CharacterLivePreview export
    characters.module.css           Approved builder styling
    CharacterTestingView.tsx         Asset testing gallery and alignment guides
    testing.module.css
  backgrounds/
    catalog.ts                     Typed manifest adapter and BackgroundSettings defaults
    BackgroundCustomizer.tsx        Catalog filters/cards and custom-photo controls
    BackgroundCustomizer.module.css
    FrameBackground.tsx            Original image/object-URL rendering and loading/error/retry UI
    FrameBackground.module.css
    usePhotoUpload.ts              Validation, decoding, cancellation and object-URL lifecycle
public/
  minibrick-logo.png                Supplied brand image
  minibrick-products.png            Supplied real product reference photograph
  characters/                      Approved transparent sprites, masks, metadata and vectors
  backgrounds/BGxxx.jpg            110 authentic full-resolution backgrounds
  backgrounds/thumbnails/BGxxx.jpg  110 matching supplied thumbnails
data/
  backgrounds.json                 Complete supplier manifest, including excluded entry and warnings
  background-inventory.csv          Original filename mappings and audit metadata
  background-package.md             Supplier integration/provenance notes
scripts/character-assets/           Source references and preparation/validation tooling
character-tests/                   Existing Python Playwright regression scripts
background-tests/                  Asset, catalog, upload, composition and positioning checks
artifacts/characters/               Character screenshots, source inspection and test reports
artifacts/backgrounds/              Asset hashes, screenshots and browser reports
artifacts/backgrounds/audit/        Latest composition audit, before/after evidence and REPORT.md
PRODUCT.md / DESIGN.md              Initial product scope and visual direction
README.md                          Runtime instructions and implementation/QA documentation
CODEX_PROJECT_HANDOFF.md            This document
```

There is no `src/` application tree, separate API route, real order endpoint or component library dependency to migrate to. The homepage currently defines its header, hero, occasion cards, showcase, story section, testimonials and footer inline in `app/page.tsx`; do not assume those are separate component files.

## 3. Accurate implementation status

“Implemented/verified” describes source code and executed tests. The Character Builder has explicit prior user approval. Do not interpret completion of a later task as permission to redesign it.

### A. Implemented and working at the current checkpoint

| Feature | Actual state |
|---|---|
| Homepage | Premium Macedonian single-page demo, navigation anchors, mobile menu, supplied logo/photo, CTAs, occasion cards, how-it-works, promotional story content, explicitly demo testimonials and footer. |
| Five-step configurator | `Фигури`, `Стил`, `Позадина`, `Текст`, `Преглед`; back/forward navigation and clickable progress buttons; same mounted config throughout. |
| Figure count | One to four visible figures. Reducing and restoring count preserves hidden configurations. No pricing calculation is attached. |
| Approved modular 2D Character Builder | Nine heads, 27 facial expressions, twelve torso colors, twelve leg colors, four character categories; independent per-figure state. |
| Newborn interaction | Only baby face and baby-body color controls. Artwork is explicitly provisional; see section 5. |
| Live character preview | Dedicated large character preview during Стил; the frame uses the same renderer/configuration for visible figures. |
| Authentic background collection | All 110 usable originals and 110 thumbnails; nine manifest categories; Сите; stable BG IDs; BG014 excluded. |
| Background selection | Keyboard-accessible thumbnail buttons, selected borders/checks, filter controls, loading/failure UI, lazy thumbnails and original full-resolution preview. |
| Custom photo backgrounds | JPG/PNG/WebP, up to 10 MiB, client validation and decode checks, replace/remove, contain/cover, x/y positioning, 1–2× zoom, mode retention and local object URLs with cleanup. |
| Figure placement | Whole-group up/down and spacing sliders; reset; count-dependent safe spacing; disabled spacing for one figure. |
| Text personalization | Optional names, message and date; live updates; no fallback names/message/date when fields are empty. |
| Text placement | Whole text-group up/down slider, reset and optional readability backing. Long text wraps without ellipses and stays within the frame. |
| Final review | Same active background/photo, individual figures, positions and personal text as the live frame; summary values wrap. |
| Demo order interaction | Button opens a clearly identified demo modal. No data is submitted, no payment is taken. |
| Responsive behavior | Automated Chrome checks at desktop, tablet and phone-sized viewports. See tested widths and limits below. |

### B. Implemented but with specific verification/refinement limits

- Responsive layouts were tested in headless desktop Google Chrome with mobile/tablet viewport sizes, not on physical iOS/Android devices or every browser engine.
- Frame text wrapping/bounds and placement are tested, but the meaning/location of decorative content inside each raster background is not automatically understood. Users can deliberately create overlaps with the sliders. Do not claim semantic collision avoidance for all designs.
- The supplied background manifest contains seven approved-demo `review` entries. They remain selectable and retain their warnings for future production review. Do not remove them or edit their artwork silently.
- The CSS frame is an approximate product preview, not a production print/export pipeline or a physical-size proof.
- The demo order modal works as a demo. Its production accessibility/checkout behavior has not been validated as a real purchasing workflow.
- The homepage uses system fonts and CSS frame mockups plus one real supplied reference photograph. Its marketing polish is not a verified business history or complete real-work portfolio.

### C. Partially implemented/demo-only areas

- **Newborn artwork:** twelve working color variants of a provisional swaddled baby body, with a clear Macedonian note. No actual newborn-body product reference was supplied.
- **Frames:** a fixed white shadow-box visual exists. No configurable black frame, physical dimensions, size selector or frame-color field exists.
- **Story/gallery:** promotional homepage sections and a supplied real reference photo exist. There is no verified founder story, dedicated business-story page or organized catalog of authentic completed customer projects.
- **Contact/privacy/FAQ:** footer links exist. Instagram points to the generic `https://www.instagram.com/`, not a verified client profile. Contact is an on-page block; FAQ links to how-it-works; privacy links to a demo footer note, not a full production policy.
- **Ordering:** final summary and demo modal exist; organized order requests, server-side validation, persistence and transmission do not.

### D. Not implemented / potential future work, not authorized by this handoff

- Figure/base/additional-figure pricing, accessory prices, delivery charges and order totals.
- Accessories, pets, accessory selection or accessory rendering.
- Interactive calendars or interactive highlighted-date generation. Catalog calendar JPGs remain static artwork.
- Configurable physical frame dimensions or colors beyond the existing white mockup.
- Actual order-request submission, customer contact form tied to orders, order management or real checkout.
- Payments, authentication, admin dashboard, database, inventory or production backend.
- Full authentic-work gallery and verified business-story content.
- Durable saved configurations/uploads, shareable designs, print exports or production fulfillment integrations.

These items are a roadmap vocabulary, not a list of already completed features. The user has explicitly said not to implement the next feature automatically.

## 4. Configurator architecture and data flow

### State ownership

`components/Configurator.tsx` owns:

- `config: FrameConfiguration` — the single source of truth for selected product appearance.
- `step` — index 0–4.
- `activeCharacterId` — stable figure ID being edited.
- `modal` — demo-order dialog visibility.
- `usePhotoUpload(...)` — mounted at configurator level, so switching steps does not destroy its photo URL or validation lifecycle.

`update(patch)` performs a functional shallow merge into the previous configuration. `updateBackground(patch)` functionally merges the nested background settings. `updateCharacter(id, patch)` delegates to the immutable state helper and replaces only the relevant character entry.

Do not replace this with duplicate per-step product state or a global store merely for convenience. Preserve references to the `characters` array when changing backgrounds/text, so memoized frame figures do not rebuild unnecessarily.

### Core types (current contract)

```ts
type Background =
  | 'heart' | 'fingerprint' | 'minimal'
  | 'love' | 'birthday' | 'anniversary';

interface FigureLayout {
  vertical: number; // UI -30..30, scene-relative offset
  spacing: number;  // UI 0..100; converted to safe gap by visible count
}

interface TextLayout {
  vertical: number; // UI -70..5; renderer clamps actual text within frame
  backplate?: boolean;
}

interface BackgroundSettings {
  mode: 'catalog' | 'custom';
  catalogId: string;
  photo: { url: string; name: string } | null;
  fit: 'contain' | 'cover';
  x: number;    // 0..100
  y: number;    // 0..100
  zoom: number; // 1..2, UI step .1
}

interface FrameConfiguration {
  figureCount: number;
  characters: CharacterConfig[];
  background: Background;
  backgroundSettings?: BackgroundSettings;
  figureLayout?: FigureLayout;
  textLayout?: TextLayout;
  names: string[];
  message: string;
  date: string;
  occasion: string;
}
```

There is intentionally **no** price, frame-color, frame-size, accessory, calendar model or real order model in this interface.

### Legacy backgrounds versus the authentic catalog

The `background` string and six preset definitions in `components/config.ts` remain for unchanged homepage examples/legacy decorations and occasion headings. The real configurator initializes:

```ts
{ ...initialConfig, backgroundSettings: initialBackgroundSettings }
```

When `backgroundSettings` exists, `FrameBackground` is the actual background authority; legacy CSS hearts/confetti/rings are not rendered behind it. Do not replace the 110 real images with the old six CSS examples.

Occasion cards dispatch `choose-occasion` with the title string. The handler changes `occasion`, updates the legacy `background` preset, returns to step 0 and scrolls into view. It currently **does not** select a manifest catalog ID, reset characters, or set the configurator figure count to the count used in the card's illustrative preview. Preserve/understand this behavior before any future explicit occasion-preset task.

### Current defaults

- Two visible figures, with four initialized stable slots (`figure-1` through `figure-4`).
- Figure 1: female, F02, H03, T12, L10.
- Figure 2: male, M01, H07, T02, L04.
- Figure 3: child, C01, H08, T07, L08 (initially hidden).
- Figure 4: male, M05, H09, T05, L02 (initially hidden).
- Names: `['Бојана', 'Петар', '', '']`.
- Message: `Against all odds`; date: `14.02.2026`. These are seeded demo values, not real customer data or the current date.
- Legacy background `heart`; actual configurator catalog selection BG001.
- Background mode catalog, no photo, contain, x/y 50, zoom 1.
- Figure vertical/spacing 0; text vertical 0; backing defaults off.

### Step behavior and persistence

- Стил displays `CharacterLivePreview` rather than the entire frame. This is intentional; do not mistake it for a missing frame preview.
- Background, Text and Review show the same `FramePreview` and the figure/text positioning controls below it.
- Figure count uses `ensureCharacterCount`. The visible set is `characters.slice(0, figureCount)`; hidden characters are retained.
- Names have `maxLength=18` per figure, message 42, date 20. Date is a free text field, not an interactive calendar or date-generation engine.
- Empty fields stay empty in the printed preview. The summary may use `—` for an absent value. It is not printed into the frame as a replacement name.
- All config lives in memory while the configurator is mounted. Reloading loses edits and uploads. No localStorage, URL serialization, server storage or database persistence exists.
- Step navigation retains product state. The category filter is view-local state and may return to Сите on remount; it is not the selected background.
- Whole-config reset returns to the seeded defaults and cancels pending upload work. Figure reset only resets figure layout. Text reset only resets vertical text placement and retains backing preference. Photo-position reset only resets photo fit/x/y/zoom.

## 5. Approved Character Builder: preserve exactly

The user explicitly approved the working modular flat 2D system. Later tasks refined it; do not replace it with emojis, arbitrary drawings, generated complete characters, 3D rendering, unrelated stock art or a new builder UI.

### Files and state

Key files: `components/characters/CharacterBuilder.tsx`, `MiniBrickCharacter.tsx`, `catalog.ts`, `state.ts`, `characters.module.css`.

```ts
interface CharacterConfig {
  id: string;
  type: 'male' | 'female' | 'child' | 'baby';
  faceId: FaceId;
  hairId: HeadId;
  torsoColorId: TorsoId;
  legsColorId: LegsId;
  babyBodyColorId: BabyBodyId;
  facesByType: Partial<Record<CharacterType, FaceId>>;
}
```

The concrete ID unions are in `catalog.ts`; use them. `CharacterPatch` cannot replace `id` or directly override `facesByType`.

- `createCharacter()` initializes valid defaults.
- `changeCharacter()` validates the face category and remembers the previous category's face in `facesByType`.
- `updateCharacterById()` updates only the targeted stable character.
- `ensureCharacterCount()` returns the existing array if enough slots exist, otherwise initializes only new stable IDs. Never truncate the saved array when decreasing visible count.
- Adult/child hairstyles are not arbitrarily restricted by gender. Every compatible head H01–H09 remains selectable.
- Baby mode retains adult selections internally so switching back restores them; it exposes **only** B01–B04 and BC01–BC12 controls.

### Actual artwork inventory

```text
public/characters/
  hair-heads/H01.png ... H09.png
  hair-heads/H01-face-mask.png ... H09-face-mask.png
  faces/female/F01.png ... F13.png
  faces/male/M01.png ... M06.png
  faces/child/C01.png ... C04.png
  faces/baby/B01.png ... B04.png
  torsos/T01.png ... T12.png      (+ traced SVG sources)
  legs/L01.png ... L12.png        (+ traced SVG sources)
  baby/BC01.png ... BC12.png
  baby/body-placeholder.svg
  head-alignment.json
  head-display.json
```

There are **81 PNG files including the nine masks**: 9 heads + 9 masks + 27 face decals + 12 torsos + 12 legs + 12 provisional baby bodies. Do not call all 81 files complete characters.

Heads were extracted from the supplied opaque catalog with controlled exterior removal; facial decals were extracted from actual alpha-bearing source artwork. Torsos/legs were reconstructed as flat SVG tracings matching the supplied shapes/colors and exported as transparent PNGs. These are documented reconstructions, not claims of pixel-identical torso crops. Black outlines, dark hair/details, white eye areas and white clothing remain intact. No whole catalog screenshot is a render layer.

Source catalogs are preserved in `scripts/character-assets/references/{heads,faces,torsos,legs}.png`. Preparation provenance is in `scripts/character-assets/README.md`. Do not regenerate these approved outputs as part of an unrelated task.

### Shared geometry and layering

- Complete SVG logical coordinate space: **512 × 768**.
- Head and body PNGs/masks share that canvas; face PNG sources are **240 × 180**.
- Head-to-body anchor: `(256, 280)`.
- Torso-to-waist anchor: `(256, 466)`; controlled overlap prevents seam gaps.
- Adult layer order: legs → torso/arms/hands → head/hair → face decal.
- Face decals use per-head placement metadata and unique SVG alpha masks for the exposed skin region. Hair and facial details must remain registered; do not let decals print over the fringe.
- `MiniBrickCharacter` uses `useId()` to avoid mask-ID collisions when multiple figures/thumbnails coexist.
- All body parts scale together through the SVG viewBox; do not introduce independent CSS margins or per-layer percentage scaling.
- The frame reuses `MiniBrickCharacter`, not a second approximation. `FrameCharacters` is memoized in `FramePreview.tsx`; stable arrays/IDs preserve its DOM on background/text changes.

### Resolved visual issues that must not return

- Both C-shaped hands are consistent peach `#ffc78e`, matching the head. Arms retain the selected torso color for all twelve torso IDs.
- Flat head/hair colors and dark contours have been normalized; preserve silhouettes and subtle outlines. No shiny gradients or photorealistic lighting on figure parts.
- No colored neck stud protrudes above torsos. No studs/connectors protrude above legs. Waist/head connections remain continuous.
- Fuller hairstyles previously looked too large. `head-display.json` applies H01 `.82`, H02 `.82`, H03 `.76`, H04 `.75`, H05 `.80`; H06–H09 `1`.
- The renderer scales the entire head/face/mask assembly together around `(256, 280)` using the same transform. Do not shrink only the hair bitmap or independently reposition the face; that would break registration and the fixed neck anchor.
- The newborn body is a **separate provisional swaddled 2D asset**, never adult torso/legs disguised as a baby. Replace it only when an accurate reference is supplied and the user asks for that work.

### Color IDs (same twelve-item ordering for T, L and BC)

01 yellow, 02 dark blue, 03 light blue/cyan, 04 black, 05 lime, 06 gray, 07 hot pink, 08 dark green, 09 orange, 10 light pink, 11 red, 12 white. Exact palette values and Macedonian labels are in `catalog.ts`. Do not change IDs or invent clothing designs, logos, accessories or unavailable hair recolors.

### Safe future integration

Add future product settings alongside the existing state. Pass existing character objects to the renderer. Preserve independent IDs, `facesByType`, hidden slots, newborn UI restrictions, mask geometry, artwork files and shared anchors. Reuse the current preview. Test multiple figures and type switching after relevant changes. A background, price or text update must not rebuild the character array unnecessarily.

## 6. Authentic backgrounds and custom upload

### Provenance and exact inventory

Original package: `/Users/antoniohristoski/Downloads/MiniBrick_Backgrounds_Codex_Ready.zip`. The repository contains the actual images and metadata, so the new conversation does not need that external ZIP to render the site.

- `public/backgrounds/`: 110 usable JPG originals, IDs BG001–BG111 except BG014.
- `public/backgrounds/thumbnails/`: 110 corresponding supplied JPG thumbnails.
- `data/backgrounds.json`: complete manifest, 111 entries including the excluded BG014 metadata record.
- `data/background-inventory.csv`: original filenames and audit mapping.
- `data/background-package.md`: supplier notes.
- The supplied package already included six name-removal edits: **BG040, BG043, BG068, BG075, BG085, BG097**. These were imported as supplied, not edited again by the implementation.
- BG014 is an editor screenshot with no usable source/thumbnail; it remains excluded, not fabricated.
- Latest asset verification compared all 220 images and the manifest to the ZIP byte for byte and decoded every image successfully.

**Never generate AI replacements, recolor, recreate, substitute unrelated stock photographs, invent catalog entries, or silently edit/remove genuine supplied artwork.**

### Nine manifest categories

| Category | Count |
|---|---:|
| Љубов и годишнини | 43 |
| Родендени и прослави | 15 |
| Дом и семејство | 12 |
| Пријателство | 3 |
| Свадби и свршувачки | 3 |
| Божиќ и зима | 12 |
| Минималистички и дезени | 18 |
| Календари и датуми | 2 |
| Мотивација и достигнувања | 2 |
| **Total** | **110** |

`components/backgrounds/catalog.ts` filters entries only when `src` and `thumbnail` exist and status is not `excluded`. It retains approved `review` entries, stable IDs, category assignments and warning metadata. Its adapter exposes `catalogBackgrounds`, `backgroundCategories`, `backgroundById`, defaults and the summary label helper.

Each entry retains `id`, `category`, `src`, `thumbnail`, `status`, `edited`, `original_filename`, `warnings`. Example paths are `/backgrounds/BG001.jpg` and `/backgrounds/thumbnails/BG001.jpg`; do not construct new mappings from guesses.

### Approved-demo review entries

- BG003, BG029: decorative third-party brand-word references in original artwork.
- BG025: small creator handle/signature.
- BG032: baked-in calendar month/date.
- BG053: subtle supplied vertical artifact.
- BG085: baked-in August calendar/highlighted date.
- BG109: fixed printed date `01.07.2025`.

The user explicitly approved all 110 for this demo. Preserve flags for future production decisions. Do not falsely report these as new implementation bugs or remove them during “cleanup.”

### Gallery and loading

`BackgroundCustomizer.tsx` owns only the current filter and file-input ref; selected product settings come from Configurator. Сите is default. Native buttons carry Macedonian labels, `aria-pressed`, keyboard behavior and selected check/border styling. Gallery images are the thumbnails, with lazy loading and a reserved aspect ratio. The grid has a bounded scroll region and responsive columns.

The latest production loading observation requested **one full-resolution background and 36 thumbnails** on first gallery opening, rather than 110 full-resolution sources. Counts depend on viewport/loading distance; this is evidence, not a fixed product guarantee.

`FrameBackground.tsx` draws the actual image in an absolute layer clipped by `.frame-art`. Catalog images use `object-fit: contain` to preserve printed details without distortion; letterboxing can be intentional. Custom photos use the saved fit, x/y, zoom and transform origin. Foreground characters and text remain separate.

Loading/error handling includes image refs checking `complete`/`naturalWidth`, because SSR images can finish/fail before hydration handlers attach. A full-image retry button remains clickable above the visual content on error; figures do not swallow its pointer events. Do not regress these previously solved cases.

### Upload lifecycle

`usePhotoUpload.ts`:

1. Cancels any pending decode request and clears its temporary URL.
2. Accepts `image/jpeg`, `image/png`, `image/webp`; rejects files over `10 * 1024 * 1024` bytes and empty files with Macedonian errors.
3. Creates a local object URL and verifies that `Image.decode()` succeeds.
4. Uses request-generation tokens so cancellation/out-of-order completion cannot replace a newer choice.
5. Commits `{url, name}` only after successful decoding. An invalid replacement leaves the previous valid photo intact.
6. Revokes replaced/removed URLs and active URLs on unmount; whole-config reset/cancel handles pending work.

A successful new photo selects custom mode and resets photo fit/position/zoom. Switching between catalog and custom keeps the photo and adjustments while mounted. Switching to catalog cancels pending decode work. Removing the photo returns to the retained catalog ID and resets photo placement. No file is uploaded to a server.

## 7. Frame composition, text and latest refinements

### Rendering architecture

`FramePreview.tsx` retains the physical white frame, bevel and shadow-box structure. `.frame-art` is the clipped interior. The configurator composes:

1. Original background image (`z-index: 0`).
2. Optional text readability backing (`z-index: 1`).
3. Memoized figures (`z-index: 2`).
4. Foreground personal text (`z-index: 3`).
5. Physical frame surroundings outside the artwork interior.

The backing is deliberately behind the figures; a large text block must not cover approved character artwork with an opaque white rectangle. An error/retry overlay can temporarily use a higher interactive layer. The generic decorative `art-topline` heading still exists separately from the optional user-entered fields; do not confuse it with fallback names.

### Figure positioning

`FigurePlacement.tsx` exposes whole-group vertical `-30..30`, spacing `0..100`, and reset. The stored values survive background switches and all relevant steps. Figure size stays fixed while gap changes. `FrameCharacters` adjusts row top/bottom symmetrically and maps spacing to count-dependent maximum gaps: 28% for two, 14% for three, 8% for four. Default gaps preserve the prior composition (2%, 1%, 0% for counts two, three, four). One-figure spacing is disabled. This is group positioning, not per-character drag/drop.

Figure entrance/exit motion remains, but the former `layout` animation on frame figure wrappers was removed because it could compensate against slider motion and cause temporary displacement. Do not reintroduce it without checking live positioning and actual asset bounds.

### Personalized text

- Personal fields are optional; `.trim()` is used for preview text, and only nonempty names join with ` & `.
- Empty names/message/date have no replacement copy in the frame.
- `FrameText.tsx` is used for configured backgrounds; homepage example rendering retains its legacy path.
- A fixed `.configurable-copy` slot reserves the original text-row height, preventing edits, wrapped names and empty fields from changing the scene or figure scale.
- The real `.art-copy-content` sits at the slot bottom, wraps complete text and uses `overflow-wrap: anywhere` instead of ellipses. Long joined-name groups over 48 characters use slightly reduced name typography and tighter line spacing.
- `useLayoutEffect` and `ResizeObserver` measure the frame, slot and content. Requested vertical offset is converted to pixels and clamped to keep the content within a six-pixel frame inset. Resizing or wrapping recomputes it. The stored slider value remains the requested setting; the renderer can stop movement at the printable boundary.
- The optional **Подлога за читливост** checkbox defaults off. Its state lives in `textLayout.backplate`; it is retained across catalog/custom mode and step changes. Its backing is hidden if all personal fields are empty.
- Summary text wraps; `minmax(0, ...)` grid tracks and `min-width: 0` prevent long values from widening the configurator and changing frame size.

### Confirmed problems resolved by the last development task

The most recent implementation request was **Background Configurator Refinement & Quality Assurance**, covering gallery/state audit, composition consistency and uploads/performance. All three phases were completed; do not repeat this task as though it were pending.

Actual reproduced problems:

1. Four long names created 548 px of text in a 210 px row and were truncated with `…`.
2. Dark personal text was unreadable over a dark uploaded photo.
3. A long unbroken review value widened the frame interior from 238.56 px to 243.13 px on the same viewport, changing preview scale between steps.
4. A pre-existing test locator for “Вертикална положба” became ambiguous after figure/text sliders were added. Geometry tests also needed to await completed entrance animation before measuring.

Fixes: complete wrapping and bounded measured text, opt-in backing, stable slot/figure geometry, constrained grid/summary wrapping, scoped photo-slider selectors and deterministic animation-settling checks. No source backgrounds, metadata or approved character assets were changed.

Latest task files: `components/FrameText.tsx` (new), `components/FramePreview.tsx`, `components/TextPlacement.tsx`, `components/config.ts`, `components/FigurePlacement.module.css`, `app/globals.css`, `background-tests/test_background_audit.py` (new), `background-tests/test_gallery_loading.py` (new), `background-tests/test_backgrounds.py`, `background-tests/test_figure_placement.py`, `README.md`, plus audit reports/screenshots.

## 8. Design and localization requirements

The approved language is premium, warm, minimal and editorial: off-white/cream page backgrounds, white controls, black typography, restrained MiniBrick red, thin warm-gray borders, clean spacing and subtle motion. Emotional heading portions use italic Georgia/serif. System Avenir/Avenir Next/Inter/Arial fallbacks are used rather than a confirmed downloadable font integration. Monospace details echo frame inscriptions.

Actual tokens from `DESIGN.md`/global CSS:

| Token | Value |
|---|---|
| Red | `#e9232d` |
| Dark | `#171514` |
| Warm | `#fbf8f4` |
| Cream | `#f4eee7` |
| Muted | `#706964` |
| Line | `#e7dfd7` |
| White | `#ffffff` |

- Desktop configurator: controls left, sticky frame preview right. Mobile: preview above controls; the character-only preview uses its established sticky layout.
- Reuse existing button, field, frame and option styling. Character/background controls use their existing CSS Modules. Figure/text positioning share `FigurePlacement.module.css`.
- Preserve the supplied heart-style MiniBrick logo and real product photo. Do not distort or replace them.
- Respect native button/fieldset/input semantics, visible focus, selected states and reduced motion styles.
- **All new customer-facing copy must be natural Macedonian. Implementation plans and technical explanations should be in English.** Technical asset IDs can remain IDs; the seeded “Against all odds” is an existing user-specified demo inscription, not permission to introduce English UI labels.
- Do not redesign the homepage or approved Character Builder to accomplish an unrelated feature.

## 9. Business facts, unknowns and required disclaimer

### Confirmed requirements and evidence

The real supplied materials are the MiniBrick heart logo, the product-reference photo, four character catalogs, and the authentic background ZIP with metadata. Personalized names, messages, dates, independent figures, custom local photos and an approximate preview are confirmed requirements. The original goal is a polished client demo; testimonials must remain explicitly examples, not fabricated customer proof.

### Do not invent missing commercial data

| Item | Confirmed information at this checkpoint |
|---|---|
| Base/frame/figure price | **Not supplied; not implemented.** |
| Additional-figure charge | **Not supplied; not implemented.** |
| Accessory list/prices | **Not supplied; not implemented.** |
| Delivery cost/coverage | **Not supplied; not implemented.** |
| Production/delivery timeframe | **Not supplied; not implemented.** |
| Physical frame dimensions | **Not supplied; not implemented.** SVG dimensions and CSS aspect ratios are not product measurements. |
| Frame colors | White visual mockup exists. Black was mentioned only conditionally (“where supported”) in QA; it is not an implemented option or verified physical catalog specification. |
| Business founder/history/story | **Not supplied.** Current emotional copy is promotional demo copy, not factual history. |
| Authentic completed-work gallery | One supplied product-reference photograph exists; no organized client-project dataset or captions were provided. |
| Official contact/profile/legal details | No verified address, phone, legal entity or exact social profile was supplied. Do not infer them. |
| Quantity | UI supports one to four figures. A hint about larger groups is not a confirmed product limit or price rule. |

No prior requirement to “preserve pricing logic” means that actual prices exist in this application. They do not. Obtain explicit rates/specifications before implementing commercial calculations.

### Required exact disclaimer

Preserve this sentence exactly whenever it is added/displayed:

> Производите претставуваат самостојни, небрандирани коцки за составување и не се поврзани со ниту еден официјален бренд или производител.

**Verified current limitation:** this exact sentence is required by the user's briefs but was not found in the inspected application source/footer at handoff. Do not claim it is already displayed. This documentation task deliberately did not edit the application to add it. Carry the requirement forward for an explicitly authorized content/production-readiness task.

Existing preview notes are separate:

- `Прегледот е приближен – финалниот дизајн го изработуваме специјално за вас.`
- `Приказот е приближен и може малку да се разликува од финалниот производ.`

Do not substitute either of these for the required product disclaimer.

## 10. Development commands and test setup

Run commands from the repository root.

```bash
npm install
npm run dev -- -p 3004
# or production:
npm run build
npm run start -- -p 3004

npm run typecheck
npm run lint
npm run test:character-assets
```

The available npm scripts are exactly `dev`, `build`, `start`, `lint`, `typecheck`, `test:character-assets`. There is no npm `test` script, Jest, Vitest or newly added test framework. The main test scripts are Python Playwright plus local Pillow/NumPy asset tooling.

**Do not run `next build` against the same `.next` directory while `next dev` is actively using it.** This previously corrupted local development output. Inspect/stop only this project's server, build, then restart the production server. Do not kill unrelated Node processes. If using a production server, rebuilding changes its output; coordinate a stop/restart as done in prior tasks.

### Browser/asset tooling

The prior session used `/tmp/minibrick-character-qa/bin/python` with Playwright and Pillow; the directory is temporary and may not survive. Asset preparation also uses NumPy. The application does not need Python at runtime.

Recreate a separate venv when needed:

```bash
python3 -m venv /tmp/minibrick-character-qa
/tmp/minibrick-character-qa/bin/python -m pip install playwright Pillow numpy
```

Browser scripts launch independent headless Google Chrome at `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`; they do not require controlling the user's existing browser. Adapt executable paths on other hosts. Do not add a large JavaScript test framework solely to run these checks.

### Useful executed/regression commands

Against a running production server on port 3004:

```bash
/tmp/minibrick-character-qa/bin/python background-tests/verify_assets.py \
  /Users/antoniohristoski/Downloads/MiniBrick_Backgrounds_Codex_Ready.zip
/tmp/minibrick-character-qa/bin/python background-tests/test_backgrounds.py
/tmp/minibrick-character-qa/bin/python background-tests/test_background_audit.py
/tmp/minibrick-character-qa/bin/python background-tests/test_gallery_loading.py
/tmp/minibrick-character-qa/bin/python background-tests/test_text_placement.py
/tmp/minibrick-character-qa/bin/python background-tests/test_figure_placement.py

CHARACTER_TEST_URL=http://localhost:3004 CHARACTER_TEST_PRODUCTION=1 \
  /tmp/minibrick-character-qa/bin/python character-tests/test_builder.py
```

Most background scripts accept `BACKGROUND_TEST_URL`; `test_gallery_loading.py` currently hardcodes localhost:3004 and writes relative to the current working directory. Character scripts have varying defaults (the main builder script defaults to port 3010); set environment variables explicitly when supported. The production flag makes the builder regression expect a 404 for `/dev/characters`; without it, it expects the development gallery.

Additional existing scripts: `character-tests/production_smoke.py`, `final_visual_check.py`, `test_hair_scale.py`, `test_refinement_rendering.py`. Read their URL/env assumptions before running. `production_smoke.py` defaults to port 3004 and checks all 81 PNG endpoints and development-gallery exclusion.

`app/dev/characters/page.tsx` calls `notFound()` unless `NODE_ENV === 'development'`. The QA view contains 72 figure examples and optional alignment guides. It is not a production customer feature.

### Older validator caveat

`scripts/character-assets/validate-refinements.py` includes hashes asserting that UI/state files match a much earlier hand/style-refinement baseline. Later authorized background/configurator work changed some of those files. A hash mismatch in that historical scope guard is not proof of a current sprite regression. Inspect the baseline and changed file before interpreting it. Do not blindly roll back completed work or claim this historical validator currently passes. The general PNG asset validator and current browser regressions are separate.

Do not run sprite regeneration (`prepare.py`, `render-vectors.mjs`, `head_style.py`) just to verify the website; it can overwrite approved assets. The source references and derivation are already preserved.

## 11. Latest verification results and provenance

### Latest completed development run (before this documentation task)

The previous implementation task actually executed these checks after its final application changes:

| Check | Result |
|---|---|
| `npm run lint` | Exit 0; zero errors, only three existing warnings |
| `npm run build` | Exit 0; production build succeeded |
| `npm run typecheck` | Exit 0 |
| Background asset verification | 110 originals + 110 thumbnails decode; source ZIP byte comparison passed |
| Full catalog browser test | 110 selections, 110 original images, 110 thumbnails, nine category counts, Сите, selected states, keyboard, four independent figures |
| Upload regression | JPG/PNG/WebP; landscape/portrait/square; unsupported, empty, corrupt and oversized files; invalid replacement retention; mode switching; crop/position; final review; URL cleanup; error/retry |
| Composition audit | 30 long-copy/backing/bounds cases at 1440/1024/768/390/320; stable delayed loading and step-to-step frame geometry |
| Text-placement regression | 12 bounds cases at 1440/768/390/320; independent movement, reset, optional empty text, partial names and state continuity |
| Figure-placement regression | 72 bounds cases for counts 1–4 at 1440/390/320; movement, spacing, scale, reset and state preservation |
| Character regression | 207 face/hair combinations; 12 torso + 12 leg colors; 4 baby faces + 12 baby body colors; four independent configurations and count retention |
| Observed browser failures | No runtime exceptions or unexpected failed requests in the passing reports |
| Gallery loading observation | One full-resolution image and 36 lazy thumbnails on first opening |

Three known pre-existing ESLint warnings:

1. `app/page.tsx:17`: `@next/next/no-img-element` for the logo image.
2. `app/page.tsx:23`: `@next/next/no-img-element` for the supplied product-reference image.
3. `postcss.config.mjs:1`: `import/no-anonymous-default-export`.

Do not turn these into a claim of a failed build, and do not redesign unrelated sections merely to silence warnings.

### Evidence files

- `artifacts/backgrounds/audit/REPORT.md` — latest background audit findings, changes and limits.
- `artifacts/backgrounds/audit/audit-report.json` — 30 composition cases and synchronization.
- `artifacts/backgrounds/audit/loading-report.json` — actual initial request counts.
- `artifacts/backgrounds/asset-report.json` — image counts and checksums.
- `artifacts/backgrounds/test-report.json` — complete catalog/upload regression.
- `artifacts/backgrounds/figure-placement-report.json` — 72 positioning cases.
- `artifacts/backgrounds/text-placement-report.json` — optional text and positioning.
- `artifacts/characters/browser-test-report.json` — full character regression.
- `artifacts/backgrounds/audit/before-*.png`, `after-*.png` — visual evidence, including dark photos, long names and mobile sizes.
- Older `checks.json`, production-smoke and refinement reports also exist. Read their timestamps/scope; do not present every historic report as newly rerun.

### Checks performed in this documentation task

This handoff was verified by reading current code, original request material, metadata, existing test reports, Git status/diff, npm scripts, lockfile and installed dependency versions. A local HTTP request returned 200 and the production build ID was present. **No lint/build/browser regression was rerun solely for the handoff**, and no application feature was implemented in this task. The passing build/test statements above refer to the actually executed preceding development run and its reports.

## 12. Git state and exact development checkpoint

### Current checkpoint answers

1. **Most recent development request:** audit/refine/stabilize background gallery, composition, preview continuity, custom uploads and performance, without rebuilding approved functionality.
2. **Implemented?** Yes. All three phases and the final verification completed. Current request is documentation only.
3. **Files changed?** Listed in section 7 and the audit REPORT.md; this documentation task adds only `CODEX_PROJECT_HANDOFF.md`.
4. **Verified?** Build/type/lint, asset/source comparisons, full gallery/uploads, composition, figure/text placement, character regression and responsive Chrome layouts; details in section 11.
5. **Incomplete?** No unfinished implementation item from that refinement task. Provisional newborn artwork, static calendar designs, missing commercial facts, absent actual order submission and the other roadmap items remain separate known limitations/future work.
6. **Uncommitted changes?** Yes, extensive. See below; do not lose them.
7. **Errors/warnings?** No outstanding TypeScript/build/runtime errors in the last passing run; three existing lint warnings. Historical refinement hash checks have the caveat described above. Required product disclaimer is not yet present in rendered app source.
8. **What next?** Read/inspect this checkpoint and wait for a new specific instruction. Do not automatically start a calendar, checkout, pricing or homepage task.

### Working-tree snapshot before adding this handoff

Modified tracked files:

```text
README.md
app/globals.css
components/Configurator.tsx
components/FramePreview.tsx
components/config.ts
package.json
```

Untracked directories/files included:

```text
app/dev/
artifacts/
background-tests/
character-tests/
components/FigurePlacement.module.css
components/FigurePlacement.tsx
components/FrameText.tsx
components/TextPlacement.tsx
components/backgrounds/
components/characters/
data/
eslint.config.mjs
public/backgrounds/
public/characters/
scripts/
```

This handoff is also newly untracked until the user chooses to commit it. No commit, push, deployment, reset or cleanup was performed for this task. The remote repository/initial commit alone is **not** the complete implemented project. A future save/commit should include the necessary untracked assets and source files; do not blindly ignore the entire untracked tree or erase user changes.

## 13. Roadmap: established scope versus optional recommendations

The following are candidates for subsequent user-directed tasks, not work to begin now.

### First: preserve and clarify

1. Preserve the full working tree and this handoff. A Git checkpoint/backup is advisable when the user authorizes it; no commit is required merely to read the project.
2. Confirm actual business rates, physical frame catalog, delivery rules, official contact/profile, business story and real-project gallery material before building features dependent on those facts.
3. Carry the exact missing product-disclaimer requirement into a future authorized content/production-readiness task.

### Functional areas explicitly recognized for future development

- **Interactive calendar customization:** separate from the two static calendar-category images and other fixed-date raster designs. Define month/year/date/layout behavior with the user before implementation; preserve the background catalog.
- **Accessories:** require actual compatible reference assets, option IDs, placement requirements and commercial prices. No fabricated catalog or arbitrary add-ons.
- **Pricing:** implement only after confirmed base, figure/additional-figure, accessory, frame and delivery rules are supplied. Keep calculations separate from character rendering.
- **Organized order-request submission:** define the required contact/configuration payload, destination and consent/error behavior. A local `blob:` URL is not a transferable stored file; real upload persistence requires a separately authorized design. No real checkout is currently present.
- **Business story and authentic-work gallery:** replace/extend promotional demo material only using genuine supplied history/projects and authorized content.
- **Frame sizes/colors:** require confirmed physical catalog/options; white visual mockup is the current baseline, not an inferred product specification.

### Optional targeted recommendations, not agreed next tasks

- Further text controls/print-safe layout refinements only for reproduced problems or a specific new requirement. Do not repeat the completed background audit.
- Physical-device and additional-browser testing, accessibility review, real contact/privacy content and production asset rights/quality decisions before public production release.
- Future configuration export/persistence or print output only if requested. Do not add cloud infrastructure or an image service speculatively.

No payments, authentication, dashboards, database or complex backend should be introduced without explicit authorization. The new conversation must wait for the user's selected feature instead of treating this roadmap as a development command.

## 14. Permanent working rules for the next conversation

1. Inspect the actual repository and applicable instructions before editing. Read this handoff, `README.md`, `PRODUCT.md`, `DESIGN.md` and the relevant implementation, not just the desired feature list.
2. Preserve working functionality and the approved Character Builder/artwork. Make narrowly scoped changes; do not rebuild the site or redesign unrelated sections.
3. Keep customer-facing UI in Macedonian. Write implementation plans and technical explanations in English.
4. Never invent client assets, completed projects, customer reviews, business history, prices, contact details or product specifications. Distinguish examples from facts.
5. Use at most three implementation phases per task. Execute them consecutively without approval pauses unless genuinely blocked by missing required information/authorization.
6. Reuse current local functional state and rendering architecture; avoid duplicate sources of truth and unnecessary libraries.
7. Preserve independent character IDs/configurations, catalog IDs/category mappings, optional empty text, local upload lifetime and live/final-preview consistency.
8. Do not regenerate approved character assets or replace authentic background artwork for unrelated work.
9. Run relevant focused tests, TypeScript, lint and build for implementation changes. Report only commands actually executed, distinguish historic reports from current runs, and separate pre-existing warnings from new failures.
10. Stop the relevant local server before rebuilding its shared `.next` output; restart the intended preview afterward. Never kill unrelated project processes.
11. Preserve extensive modified/untracked work. Do not reset/clean, silently discard changes, commit, push, deploy or install infrastructure merely to make the tree look tidy.
12. Do not use the old character-refinement scope hashes as justification to revert subsequently authorized background/configurator changes.
13. Do not start a roadmap feature automatically. **After reading and inspecting, wait for the user's next specific development instruction before editing code.**

---

## Deliverable B — Ready-to-copy new Codex conversation starter

```text
Continue the existing MiniBrick.mk project at /Users/antoniohristoski/programiranje/MiniBrick.

Read the entire attached CODEX_PROJECT_HANDOFF.md, then inspect the current repository to understand the actual implementation and latest checkpoint. Preserve all completed functionality, the approved modular Character Builder and authentic client assets, including the extensive modified/untracked files. Do not rebuild the site or repeat the completed background refinement task.

Be ready to continue from this checkpoint, but wait for my next specific development instruction before editing code or implementing anything from the roadmap. Confirm briefly that you have read the handoff and inspected the project.
```
