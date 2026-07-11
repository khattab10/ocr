# GoVia — Brand & Logo System

**AI-powered shipping marketplace for e-commerce sellers.**

> One app. Every shipping company. Smart recommendations. Your choice.
>
> **We recommend. You decide.**

GoVia is a smart logistics **platform** — not a courier. The identity deliberately avoids
trucks, vans, boxes and pins, and instead reads like a global technology company
(think Google Maps + Stripe + Shopify).

To preview the whole system, open [`index.html`](./index.html) in a browser.

---

## The mark — one symbol, three meanings

The GoVia symbol is a **route** that bends upward into a **checkmark**. A small open dot marks
the seller's **origin**; the solid node is the **recommended, chosen carrier**.

| Direction | How the mark expresses it |
|-----------|---------------------------|
| **1 · Smart Route** | The `V` is a navigation path that resolves into a check — the smartest path, and *your* choice. |
| **2 · Connected Network** | Origin node and destination hub, linked through a single line = a marketplace of carriers on one platform. |
| **3 · Forward Movement** | The stroke lifts up and to the right — motion, progress and growth built into the geometry. |

---

## Colour

| Token | Hex | Use |
|-------|-----|-----|
| Deep Navy | `#0B1F3A` | Trust · technology · business. Primary text & dark backgrounds. |
| Electric Green | `#22C55E` | Smart decisions · success · growth. The route & "Via". |
| Green (deep) | `#16A34A` | Gradient anchor on light backgrounds. |
| Green (light) | `#4ADE80` | Gradient anchor / accents on dark backgrounds. |
| White | `#FFFFFF` | Space & clarity. |
| Cloud | `#F8FAFC` | App background & surfaces. |
| Slate | `#64748B` | Secondary / muted text. |

---

## Typography

- **Brand & headings:** Plus Jakarta Sans (ExtraBold `800` for the logo, Bold `700` for headings).
- **Product UI & body:** Inter (`400`–`600`).
- Alternatives in the same spirit: Manrope, SF Pro.
- Wordmark: **Go** in Deep Navy, **Via** in Electric Green, letter-spacing `-0.03em`.

---

## Assets

All logos are vector **SVG** (infinitely scalable). Key raster **PNG** exports are in `assets/png/`.

| File | Purpose |
|------|---------|
| `assets/govia-logo-stacked-light.svg` | **Primary** lockup (light backgrounds) |
| `assets/govia-logo-stacked-dark.svg` | Primary lockup (dark backgrounds) |
| `assets/govia-logo-horizontal-light.svg` | Horizontal lockup — headers, docs |
| `assets/govia-logo-horizontal-dark.svg` | Horizontal lockup on dark |
| `assets/govia-wordmark.svg` | Wordmark only |
| `assets/govia-symbol.svg` | Symbol — full colour |
| `assets/govia-symbol-dark.svg` | Symbol for dark backgrounds |
| `assets/govia-symbol-mono-navy.svg` | Single-colour navy |
| `assets/govia-symbol-mono-white.svg` | Single-colour white |
| `assets/govia-app-icon.svg` | App icon (navy, with signal glow) |
| `assets/govia-app-icon-light.svg` | App icon (light variant) |
| `assets/favicon.svg` | Favicon |
| `assets/png/*` | 256–1024px raster exports for stores/home screens |

### Which logo to use where

- **Mobile app icon / home screen:** `govia-app-icon*` (PNG for stores).
- **Website & dashboard header:** horizontal lockup.
- **Marketing / hero / business documents:** stacked primary lockup.
- **Avatars, favicons, small spaces:** symbol only.

---

## Usage

**Do**
- Give the logo clear space of at least the height of the symbol on all sides.
- Prefer navy or white backgrounds for maximum contrast.
- Use the symbol alone when space is tight.
- Keep **Go** navy and **Via** green.

**Don't**
- Add trucks, vans, boxes or location pins.
- Stretch, rotate, or recolour the mark.
- Put low-contrast green text on navy.
- Add drop shadows or outlines to the wordmark.

---

## Notes

- Standalone SVGs embed **Plus Jakarta Sans** via Google Fonts `@import`, so they render with the
  brand font when opened directly in a browser. When embedded via `<img>` in an app that blocks
  external font loading, the wordmark gracefully falls back to a system sans-serif; for guaranteed
  fidelity in that case, use the PNG exports or convert the wordmark text to outlines.
- PNGs were rendered from the SVG sources at high resolution and can be regenerated at any size.
