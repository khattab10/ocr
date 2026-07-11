# GoVia

**One app. Every shipping company. Smart recommendations. Your choice.**
_We recommend. You decide._

GoVia is an AI-powered shipping marketplace for e-commerce sellers in Egypt and the
Middle East. Sellers compare multiple carriers, get intelligent recommendations,
choose the carrier they prefer, and manage every shipment from one platform.

## Repository layout

| Path | What it is |
|------|------------|
| `govia-brand/` | Brand & logo system — SVG/PNG assets + an HTML brand showcase (`index.html`). |
| `govia-app/` | Product MVP (POC). `auth.html` = login / register screen. More screens to come. |

## Quick start

Everything here is static HTML/CSS/JS — no build step. Open the files directly in a browser:

- Brand showcase: `govia-brand/index.html`
- Auth screen: `govia-app/auth.html` (add `?mode=login` or `?mode=signup`)

Or serve locally:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000/govia-app/auth.html
```

## Brand tokens

| Token | Hex |
|-------|-----|
| Deep Navy | `#0B1F3A` |
| Electric Green | `#22C55E` |
| Cloud (bg) | `#F8FAFC` |

Type: Plus Jakarta Sans (brand/headings) + Inter (UI) + Cairo/Tajawal (Arabic).

## Roadmap (MVP)

- [x] Brand & logo system
- [x] Auth — login / register (name, phone, email)
- [ ] OTP verification
- [ ] Connect store + shipping preferences
- [ ] Home / dashboard
- [ ] Create shipment
- [ ] Carrier comparison + recommendation details
- [ ] Checkout + tracking
