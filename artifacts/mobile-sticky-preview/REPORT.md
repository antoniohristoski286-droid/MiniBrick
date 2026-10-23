# Compact mobile character preview

The existing character editor now has a compact preview at phone widths, pinned within the customization controls. It follows the active figure and existing accessory state, and can open a larger native-dialog preview. The full desktop character preview and all source artwork remain unchanged.

Warnings, price and gallery link remain outside the sticky area, in normal flow after the mobile controls. The preview ends at the editor boundary. The dialog supports Escape, close, keyboard focus containment, return focus, preserved scroll, and automatic closing when switching to desktop width.

Verification executed:

- Production build, TypeScript and ESLint passed.
- Focused mobile browser checks passed at 320x568, 360x640, 390x844, 430x932 and 667x375. Preview height ranged from 140 to 180 px.
- Face, hair, torso, leg and accessory controls were clicked normally, without forced clicks. Hit testing confirmed selected controls were unobscured. Live updates, independent figures and newborn choices were preserved.
- Enlargement, keyboard/close actions, focus and scroll restoration passed at every size. Desktop and other-step behavior were checked.

Evidence: report.json and editing-*.png. The actual browser test is frontend-tests/test_mobile_sticky_preview.py.
