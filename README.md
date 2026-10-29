# Wax Point — website

Static website for Wax Point, waxing & laser specialists in West Ealing. No build server or database: plain HTML/CSS/JS, hosted free on Cloudflare Pages.

## Change links (booking, WhatsApp, Instagram, form, Klarna)
Edit `config.js`. Any empty value hides its button automatically.

- `treatwellWidget` – your Treatwell **website booking widget** link (0% commission). Find it in Treatwell Connect.
- `instagram` – full Instagram profile URL.
- `consultationForm` – Tally form link.
- `payLinks` – Stripe Payment Links per course, e.g. `"L1-6": "https://buy.stripe.com/..."` (Ladies package 1, 6 sessions). IDs: `L1`–`L7`, `G1`–`G6`; sizes `6`, `8`, `10`.

## Change prices
Edit `data/laser-prices.json`, then run `python3 tools/build.py` and commit.
Page text lives in `tools/build.py`; don't edit the generated `.html` files directly.

## Deploy (Cloudflare Pages)
Cloudflare dashboard → Workers & Pages → Create → Pages → Connect to Git → pick this repo.
Build command: *(leave empty)* · Output directory: `/`. Every push to `main` goes live.
After buying the domain, update `site` in `tools/build.py` and rebuild.
