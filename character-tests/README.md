# Character builder verification

`/dev/characters` is available only in development. It displays all 9 heads, 27 faces, 12 torsos, 12 legs, and 12 provisional newborn body variants, with optional alignment guides. Production requests return 404.

## Browser tests

Install Python Playwright in a virtual environment. These scripts launch a separate headless Google Chrome at its standard macOS application path; they do not control an existing user browser session.

Run the app on port 3010, then:

```bash
python character-tests/test_builder.py
python character-tests/final_visual_check.py
```

`test_builder.py` also accepts `CHARACTER_TEST_URL` for another server. It verifies 207 non-baby face/head combinations, all torso/leg colors, all newborn faces/body colors, native keyboard activation, four independent figures, count decrease/readdition, frame preview synchronization, unchanged frame text/background defaults, asset availability, and layout at 1024, 768, 390 and 320 pixels. Browser page errors and unexpected HTTP failures fail the test.

`final_visual_check.py` captures stabilized desktop/mobile views and verifies that the live character never overlaps the option-code caption. Reports and screenshots are written to `artifacts/characters/`.

For a built production server, run `production_smoke.py` (default URL: `http://localhost:3004`). It checks interactive controls, independent figures, mobile widths, all 81 PNG endpoints, and that the development gallery returns 404.
