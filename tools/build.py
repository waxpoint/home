#!/usr/bin/env python3
"""Builds the Wax Point static site: python3 tools/build.py
Edit data/laser-prices.json or the page content below, then run this script.
"""
import json
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "data" / "laser-prices.json").read_text())

SALON = {
    "name": "Wax Point",
    "street": "Unit 5, 36-38 Broadway",
    "area": "West Ealing",
    "city": "London",
    "postcode": "W13 0SU",
    "phone_display": "07702 014136",
    "lat": 51.5106891,
    "lng": -0.321669,
    "site": "https://waxpoint.co.uk",  # change to the real domain once bought
    # Hours as listed on Treatwell (Oct 2026). Google shows different hours — keep both in sync.
    "hours": [
        ("Monday", None, None),
        ("Tuesday", "10:30", "19:00"),
        ("Wednesday", "11:00", "19:00"),
        ("Thursday", "10:30", "19:00"),
        ("Friday", "10:30", "19:00"),
        ("Saturday", "10:00", "17:00"),
        ("Sunday", None, None),
    ],
}

e = html.escape


def money(n):
    return f"£{n:,}"


def fmt_time(t):
    h, m = map(int, t.split(":"))
    suffix = "am" if h < 12 else "pm"
    h12 = h if 1 <= h <= 12 else (h - 12 if h > 12 else 12)
    return f"{h12}{'' if m == 0 else ':%02d' % m}{suffix}"


WA_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91S17.5 2 12.04 2zm5.8 14.03c-.24.68-1.42 1.3-1.95 1.34-.5.05-.97.23-3.27-.68-2.76-1.09-4.5-3.92-4.64-4.1-.13-.18-1.11-1.48-1.11-2.82s.7-2 .95-2.27c.25-.27.54-.34.72-.34h.52c.17 0 .39-.06.6.46.24.55.78 1.9.85 2.04.07.14.11.3.02.48-.09.18-.14.3-.27.46-.14.16-.29.36-.41.48-.14.14-.28.29-.12.56.16.27.71 1.17 1.52 1.9 1.05.93 1.93 1.22 2.2 1.36.27.14.43.11.59-.07.16-.18.68-.79.86-1.07.18-.27.36-.23.61-.14.25.09 1.59.75 1.86.89.27.14.45.2.52.32.07.11.07.66-.17 1.34z"/></svg>'


def layout(page_id, title, description, body, path):
    nav_items = [
        ("index", "index.html", "Home"),
        ("laser", "laser.html", "Laser prices"),
        ("consultation", "consultation.html", "Consultation"),
        ("aftercare", "aftercare.html", "Aftercare"),
        ("contact", "index.html#visit", "Visit us"),
    ]
    nav = "\n".join(
        f'<a href="{href}"{" aria-current=\"page\"" if pid == page_id else ""}>{label}</a>'
        for pid, href, label in nav_items
    )
    hours_ld = [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": d, "opens": o, "closes": c}
        for d, o, c in SALON["hours"] if o
    ]
    ld = {
        "@context": "https://schema.org",
        "@type": "BeautySalon",
        "name": SALON["name"],
        "description": "Beauty, waxing and laser hair removal in West Ealing, London.",
        "foundingDate": "2019",
        "sameAs": ["https://www.instagram.com/waxpoint.london/", "https://www.treatwell.co.uk/place/wax-point-1/"],
        "image": SALON["site"] + "/assets/og-image.jpg",
        "logo": SALON["site"] + "/assets/icon-512.png",
        "url": SALON["site"],
        "telephone": "+447702014136",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": SALON["street"],
            "addressLocality": SALON["city"],
            "postalCode": SALON["postcode"],
            "addressCountry": "GB",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": SALON["lat"], "longitude": SALON["lng"]},
        "openingHoursSpecification": hours_ld,
        "priceRange": "££",
    }
    canonical = SALON["site"] + ("/" if path == "index.html" else "/" + path)
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:image" content="{SALON['site']}/assets/og-image.jpg">
<meta property="og:type" content="website">
<meta name="theme-color" content="#e7dfd9">
<link rel="icon" href="assets/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="preload" href="assets/fonts/cormorant-500.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/styles.css">
<script type="application/ld+json">{json.dumps(ld)}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="Wax Point home"><img src="assets/logo-header.png" alt="Wax Point — beauty, waxing, laser" width="167" height="30"></a>
    <button class="menu-btn" aria-label="Menu" aria-expanded="false">&#9776;</button>
    <nav class="nav" aria-label="Main">
      {nav}
      <a class="btn sm" data-link="book" href="#">Book now</a>
    </nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div>
      <img class="footer-logo" src="assets/logo-light.png" alt="Wax Point" width="260" height="47">
      <p>Beauty, waxing &amp; laser in West Ealing. Est. 2019.</p>
      <p>{e(SALON['street'])}<br>{e(SALON['area'])}, {e(SALON['city'])} {e(SALON['postcode'])}</p>
    </div>
    <div>
      <h3>Get in touch</h3>
      <ul>
        <li><a data-link="whatsapp" href="#">WhatsApp</a></li>
        <li><a data-link="phone" href="#">{SALON['phone_display']}</a></li>
        <li><a data-link="instagram" href="#">Instagram</a></li>
        <li><a data-link="treatwell" href="#">Treatwell</a></li>
      </ul>
    </div>
    <div>
      <h3>Clients</h3>
      <ul>
        <li><a href="laser.html">Laser prices &amp; packages</a></li>
        <li><a href="consultation.html">Laser consultation</a></li>
        <li><a href="aftercare.html">Before &amp; aftercare</a></li>
        <li><a href="privacy.html">Privacy</a></li>
      </ul>
    </div>
    <p class="legal">&copy; <span id="year">2026</span> Wax Point. Prices shown in GBP. Laser courses are sold only after a free consultation and patch test.</p>
  </div>
</footer>
<a class="wa-float" data-link="whatsapp" href="#" aria-label="Message us on WhatsApp">{WA_ICON}<span>WhatsApp</span></a>
<script src="config.js"></script>
<script src="assets/site.js"></script>
</body>
</html>
"""


# ---------- shared fragments ----------

def hours_list():
    items = []
    for d, o, c in SALON["hours"]:
        val = f"{fmt_time(o)} – {fmt_time(c)}" if o else "Closed"
        items.append(f"<li><span>{d}</span><span>{val}</span></li>")
    return '<ul class="hours">' + "".join(items) + "</ul>"


def area_table(section):
    packs = DATA["packs"]
    head = "".join(f'<th class="num" scope="col">Pack<span class="hide-sm"> of</span> {p}</th>' for p in packs)
    rows = []
    for r in section["rows"]:
        detail = f'<span class="detail">{e(r["detail"])}</span>' if r.get("detail") else ""
        cells = "".join(f'<td class="num">{money(v)}</td>' for v in r["prices"])
        rows.append(f'<tr><th scope="row">{e(r["name"])}{detail}</th>{cells}</tr>')
    return (f'<div class="table-scroll"><table class="price-table"><caption class="skip">{e(section["title"])} — price per session</caption>'
            f'<thead><tr><th scope="col">Area <span class="small hide-sm">(price per session)</span></th>{head}</tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>')


def package_cards(section):
    packs = DATA["packs"]
    cards = []
    for i, r in enumerate(section["rows"], 1):
        detail = f'<p class="detail">{e(r["detail"])}</p>' if r.get("detail") else ""
        opts = []
        for p, v in zip(packs, r["prices"]):
            key = f'{r["id"]}-{p}'
            opts.append(
                f'<li><span>{p} sessions<span class="total">{money(v * p)} course total</span></span>'
                f'<span class="per">{money(v)}<span class="total">per session</span></span>'
                f'<a class="btn pink pay-link" data-pay="{key}" href="#">Pay for course</a></li>'
            )
        cards.append(
            f'<article class="pkg"><div class="tag">{i}</div><h3>{e(r["name"])}</h3>{detail}'
            f'<ul class="pkg-options">{"".join(opts)}</ul></article>'
        )
    return '<div class="pkg-grid">' + "".join(cards) + "</div>"


def group_panel(group):
    parts = []
    for s in DATA["sections"]:
        if s["group"] != group:
            continue
        parts.append(f'<h3 class="table-title" id="{s["id"]}">{e(s["title"])}</h3>')
        parts.append(area_table(s) if s["kind"] == "areas" else package_cards(s))
    return "".join(parts)


# ---------- pages ----------

def page_index():
    wax = "".join(
        f'<li><span>{e(r["name"])}<span class="dur">{e(r["duration"])}</span></span><span class="price">{e(r["price"])}</span></li>'
        for r in DATA["waxing_highlights"]["rows"]
    )
    featured = [r for s in DATA["sections"] if s["kind"] == "packages" for r in s["rows"]]
    lowest = min(min(r["prices"]) for s in DATA["sections"] for r in s["rows"])
    map_src = f"https://maps.google.com/maps?q=Wax%20Point%2C%2036-38%20Broadway%2C%20London%20W13%200SU&z=16&output=embed"
    body = f"""
<section class="hero">
  <div class="wrap hero-center" style="display:block">
    <img class="hero-logo" src="assets/logo-dark.png" alt="Wax Point — beauty, waxing, laser. Est. 2019" width="760" height="136">
    <h1>Smooth skin, <em>the gentle way.</em></h1>
    <p class="lead">Waxing &amp; laser hair removal in West Ealing. Over 15 years of experience, techniques designed to keep waxing as pain-free as possible, and a spotless, calm studio five minutes from West Ealing station.</p>
    <ul class="badges">
      <li>★ 5.0 · 1,000+ Treatwell reviews</li>
      <li>Free laser consultation</li>
      <li>Ladies &amp; gents</li>
    </ul>
    <div class="btn-row">
      <a class="btn" data-link="book" href="#">Book an appointment</a>
      <a class="btn alt" href="laser.html">Laser prices &amp; packages</a>
    </div>
  </div>
</section>

<section id="services">
  <div class="wrap">
    <div class="section-head">
      <h2>What we do</h2>
      <p class="muted">Two ways to smooth: instant results with waxing, or long-term reduction with a laser course.</p>
    </div>
    <div class="grid-2">
      <div class="card">
        <h3>Waxing</h3>
        <p class="muted">Hot and strip wax for face and body. Popular treatments:</p>
        <ul class="menu-list">{wax}</ul>
        <p class="small muted" style="margin-top:14px">Full waxing menu with every area and package is on Treatwell.</p>
        <div class="btn-row"><a class="btn" data-link="book" href="#">See full menu &amp; book</a></div>
      </div>
      <div class="card">
        <h3>Laser hair removal</h3>
        <p class="muted">Courses of 6, 8 or 10 sessions for single areas or money-saving packages, from <strong>{money(lowest)} per session</strong>.</p>
        <ul class="care-list">
          <li>Free consultation and patch test before every course</li>
          <li>{len(featured)} packages for ladies and gents</li>
          <li>Pay for your course by card or spread the cost with Klarna</li>
          <li>Packs of 6 &amp; 8 valid 12 months, packs of 10 valid 18 months</li>
        </ul>
        <div class="btn-row" style="margin-top:18px">
          <a class="btn" href="laser.html">Laser prices</a>
          <a class="btn alt" href="consultation.html">Book free consultation</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="tint">
  <div class="wrap">
    <div class="section-head">
      <h2>Your laser journey</h2>
    </div>
    <div class="grid-3">
      <div class="card"><div class="step-num">1</div><h3>Free consultation</h3><p class="muted">Fill in a short health questionnaire and we'll talk through your skin, hair and goals.</p></div>
      <div class="card"><div class="step-num">2</div><h3>Patch test</h3><p class="muted">A quick test on a small area to check how your skin responds, at no cost.</p></div>
      <div class="card"><div class="step-num">3</div><h3>Start your course</h3><p class="muted">Choose 6, 8 or 10 sessions. Pay by card in the salon or online, including Klarna.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap grid-2" style="align-items:center">
    <div class="card">
      <div class="stars" aria-hidden="true">★★★★★</div>
      <div class="stat">5.0</div>
      <p><strong>from 1,000+ verified reviews on Treatwell</strong></p>
      <p class="muted">Clients mention professionalism, attention to detail and how comfortable they feel. Many have been coming back for years.</p>
      <a class="btn alt" data-link="treatwell" href="#">Read the reviews</a>
    </div>
    <div class="card" data-needs="instagram">
      <span class="eyebrow">Instagram</span>
      <h3>@waxpoint.london</h3>
      <p class="muted">Results, studio life and offers. Follow along for the latest from the studio.</p>
      <div id="instagram-feed"></div>
      <a class="btn" data-link="instagram" href="#">Follow on Instagram</a>
    </div>
    <div class="card" data-missing="instagram">
      <h3>Questions before you book?</h3>
      <p class="muted">Send us a message on WhatsApp. We usually reply the same day.</p>
      <a class="btn" data-link="whatsapp" href="#">Message us</a>
    </div>
  </div>
</section>

<section class="tint" id="visit">
  <div class="wrap grid-2">
    <div>
      <h2>Visit us</h2>
      <p>{e(SALON['street'])}<br>{e(SALON['area'])}, {e(SALON['city'])} {e(SALON['postcode'])}<br><span class="muted small">5 minutes' walk from West Ealing station</span></p>
      {hours_list()}
      <div class="btn-row">
        <a class="btn" data-link="book" href="#">Book now</a>
        <a class="btn alt" data-link="whatsapp" href="#">WhatsApp us</a>
        <a class="btn alt" data-link="phone" href="#">Call</a>
      </div>
    </div>
    <iframe class="map" title="Map to Wax Point, West Ealing" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="{map_src}"></iframe>
  </div>
</section>
"""
    return layout("index", "Wax Point — Waxing & Laser Hair Removal in West Ealing",
                  "Waxing and laser hair removal specialists in West Ealing, London W13. Free laser consultation and patch test, 5.0 rating from 1,000+ Treatwell reviews.",
                  body, "index.html")


def page_laser():
    body = f"""
<section class="hero" style="padding-bottom:48px">
  <div class="wrap" style="display:block">
    <h1>Laser hair removal prices</h1>
    <p class="lead">All prices are <strong>per session</strong> when you book a course of 6, 8 or 10 sessions. The longer the course, the lower the price per session.</p>
    <ul class="badges"><li>Free consultation</li><li>Free patch test</li><li>Card or Klarna</li></ul>
    <div class="btn-row"><a class="btn" href="consultation.html">Book free consultation</a><a class="btn alt" data-link="whatsapp" data-wa-text="Hi Wax Point, I'd like to ask about laser hair removal." href="#">Ask on WhatsApp</a></div>
  </div>
</section>

<section style="padding-top:40px">
  <div class="wrap">
    <div class="note"><strong>Consultation first.</strong> Every laser course starts with a free consultation and patch test, so we can make sure treatment is safe and right for you. Please only pay for a course after your patch test.</div>
    <div class="note" data-pay-note><strong>Paying online:</strong> "Pay for course" takes you to a secure checkout where you can pay by card, Apple Pay, Google Pay or Klarna. Klarna options depend on eligibility and are offered and explained by Klarna at checkout.</div>

    <div data-tabs>
      <div class="tabs" role="tablist" aria-label="Choose prices">
        <button role="tab" id="tab-ladies" aria-controls="panel-ladies" aria-selected="true">Ladies</button>
        <button role="tab" id="tab-gents" aria-controls="panel-gents" aria-selected="false">Gents</button>
      </div>
      <div id="panel-ladies" role="tabpanel" aria-labelledby="tab-ladies">{group_panel('ladies')}</div>
      <div id="panel-gents" role="tabpanel" aria-labelledby="tab-gents" hidden>{group_panel('gents')}</div>
    </div>

    <p class="note"><strong>Validity:</strong> {e(DATA['validity'])} Package prices are per session when you book the whole package.</p>
  </div>
</section>

<section class="tint">
  <div class="wrap" style="max-width:820px">
    <h2>Laser FAQ</h2>
    <details><summary>How many sessions will I need?</summary><p>Most people need a course of 6–10 sessions, spaced several weeks apart, because hair grows in cycles. We'll recommend a course at your consultation.</p></details>
    <details><summary>Does it hurt?</summary><p>Most clients describe it as a quick snapping or warm sensation. Sensitivity varies by area and we adjust settings to keep you comfortable.</p></details>
    <details><summary>Can I shave between sessions?</summary><p>Yes, shaving is fine. Please don't wax, pluck, thread or use epilators during your course, as laser needs the hair root in place.</p></details>
    <details><summary>Is laser suitable for everyone?</summary><p>Not always. Some medications, skin conditions, pregnancy and recent sun exposure can mean we need to wait or adjust treatment. That's what the consultation and patch test are for.</p></details>
    <details><summary>How long is my course valid?</summary><p>{e(DATA['validity'])}</p></details>
  </div>
</section>
"""
    return layout("laser", "Laser Hair Removal Prices — Wax Point, West Ealing",
                  "Laser hair removal prices for ladies and gents in West Ealing. Courses of 6, 8 or 10 sessions, money-saving packages, free consultation and patch test.",
                  body, "laser.html")


def page_consultation():
    body = """
<section class="hero" style="padding-bottom:48px">
  <div class="wrap" style="display:block">
    <h1>Laser consultation</h1>
    <p class="lead">Your consultation and patch test are free. Filling in the questionnaire before your visit saves time and lets us check that laser is safe for you.</p>
    <div class="btn-row">
      <a class="btn" data-link="form" href="#">Fill in the consultation form</a>
      <a class="btn alt" data-link="book" href="#">Book consultation</a>
    </div>
    <p class="small muted" data-missing="form" style="margin-top:16px">Our online form is coming soon. Message us on WhatsApp to arrange your consultation and we'll go through the questions with you in the salon.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="grid-3">
      <div class="card"><div class="step-num">1</div><h3>Questionnaire</h3><p class="muted">About 5 minutes. We ask about your skin, medication, health and recent sun exposure.</p></div>
      <div class="card"><div class="step-num">2</div><h3>Consultation &amp; patch test</h3><p class="muted">We discuss your goals, check your skin and hair, and test a small area.</p></div>
      <div class="card"><div class="step-num">3</div><h3>Your course plan</h3><p class="muted">After the patch test we recommend the right course and you can choose how to pay.</p></div>
    </div>
  </div>
</section>

<section class="tint">
  <div class="wrap care-grid">
    <div class="card">
      <h3>What we'll ask about</h3>
      <ul class="care-list">
        <li>Your skin type and how it reacts to sun</li>
        <li>Current medication, including antibiotics, acne treatments and anything that makes skin sensitive to light</li>
        <li>Skin conditions, recent tattoos, scars or cold sores in the area</li>
        <li>Pregnancy or breastfeeding</li>
        <li>Recent tanning, sunbeds or fake tan</li>
        <li>How you've removed hair recently (waxing, threading, epilating)</li>
      </ul>
    </div>
    <div class="card">
      <h3>Before your patch test</h3>
      <ul class="care-list">
        <li>Shave the area 24 hours before. Don't wax, pluck or epilate for 4–6 weeks before.</li>
        <li>Avoid sun, sunbeds and fake tan on the area for 2–4 weeks.</li>
        <li>Come with clean skin: no creams, deodorant or make-up on the area.</li>
        <li>Tell us about any new medication, even if you've had laser before.</li>
      </ul>
    </div>
  </div>
</section>

<section>
  <div class="wrap" style="max-width:820px">
    <h2>Your information</h2>
    <p class="muted">Your answers include health information, so we treat them with extra care. They are used only to decide whether laser treatment is safe for you, are stored securely by our form provider in the EU/UK, are seen only by your therapist, and are never shared for marketing. You can ask us to see or delete your information at any time. See our <a href="privacy.html">privacy notice</a>.</p>
  </div>
</section>
"""
    return layout("consultation", "Free Laser Consultation — Wax Point, West Ealing",
                  "Book a free laser hair removal consultation and patch test at Wax Point, West Ealing. Fill in the questionnaire online before your visit.",
                  body, "consultation.html")


def page_aftercare():
    body = """
<section class="hero" style="padding-bottom:48px">
  <div class="wrap" style="display:block">
    <h1>Before &amp; aftercare</h1>
    <p class="lead">A few simple steps make your results smoother and longer-lasting, and keep your skin calm.</p>
    <div class="toc">
      <a class="btn pink sm" href="#waxing">Waxing</a>
      <a class="btn pink sm" href="#laser">Laser</a>
      <a class="btn pink sm" href="#help">When to contact us</a>
    </div>
  </div>
</section>

<section id="waxing">
  <div class="wrap">
    <h2>Waxing</h2>
    <div class="care-grid">
      <div class="card">
        <h3>Before your wax</h3>
        <ul class="care-list">
          <li>Let hair grow to about 5 mm, roughly 2–3 weeks after shaving.</li>
          <li>Gently exfoliate the day before, not on the day.</li>
          <li>Skip creams, oils and fake tan on the area on the day.</li>
          <li>Avoid sunbathing or sunbeds for 24 hours before.</li>
          <li>Retinoid creams or acne medication can make skin fragile. Please tell us before we start.</li>
        </ul>
      </div>
      <div class="card">
        <h3>For 24–48 hours after</h3>
        <ul class="care-list">
          <li>No hot baths, saunas, steam rooms, swimming or gym sessions.</li>
          <li>No sunbathing, sunbeds or fake tan.</li>
          <li>Wear loose, breathable clothing over the area.</li>
          <li>Avoid perfumed products, deodorant (underarms) and make-up (face).</li>
          <li>Try not to touch or scratch the area.</li>
        </ul>
      </div>
      <div class="card">
        <h3>After 48 hours</h3>
        <ul class="care-list">
          <li>Exfoliate gently 2–3 times a week to prevent ingrown hairs.</li>
          <li>Moisturise daily with an unperfumed lotion.</li>
          <li>Avoid shaving between waxes so hair grows back finer.</li>
          <li>Book your next wax in 4–6 weeks.</li>
        </ul>
      </div>
      <div class="card">
        <h3>Is this normal?</h3>
        <p class="muted">Some redness and small bumps are normal and usually settle within a few hours to a day. A cool compress helps. If redness, swelling or spots get worse after 48 hours, contact us.</p>
      </div>
    </div>
  </div>
</section>

<section class="tint" id="laser">
  <div class="wrap">
    <h2>Laser hair removal</h2>
    <div class="care-grid">
      <div class="card">
        <h3>Before each session</h3>
        <ul class="care-list">
          <li>Shave the area 24 hours before. Don't wax, pluck, thread or epilate during your course.</li>
          <li>No sun, sunbeds or fake tan on the area for 2–4 weeks before.</li>
          <li>Come with clean skin: no creams, deodorant or make-up on the area.</li>
          <li>Let us know about any new medication or health changes.</li>
        </ul>
      </div>
      <div class="card">
        <h3>For 48 hours after</h3>
        <ul class="care-list">
          <li>Skin may feel warm and look pink, like mild sunburn. A cool compress or aloe vera gel soothes it.</li>
          <li>No hot baths, saunas, steam rooms, swimming or intense exercise.</li>
          <li>Avoid perfumed products, deodorant (underarms) and make-up (face).</li>
          <li>Don't scrub or exfoliate the area.</li>
        </ul>
      </div>
      <div class="card">
        <h3>Throughout your course</h3>
        <ul class="care-list">
          <li>Use SPF 30+ on treated areas exposed to the sun, and avoid sunbeds completely.</li>
          <li>Shaving is fine. Treated hairs may "shed" for 1–3 weeks; this is normal.</li>
          <li>Exfoliate gently after the first week to help shedding hairs come out.</li>
          <li>Keep to your session schedule for the best results.</li>
        </ul>
      </div>
      <div class="card">
        <h3>Is this normal?</h3>
        <p class="muted">Redness and small raised bumps around follicles are common and usually fade within 24–48 hours. Blistering, crusting or changes in skin colour are not expected. Contact us straight away if you notice them.</p>
      </div>
    </div>
  </div>
</section>

<section id="help">
  <div class="wrap" style="max-width:820px">
    <h2>When to contact us</h2>
    <p>Message us if redness or swelling hasn't settled after 48 hours, if you notice blisters, crusting, spots that look infected or any change in skin colour. If you're worried about a severe reaction, contact your GP or NHS 111.</p>
    <div class="btn-row"><a class="btn" data-link="whatsapp" data-wa-text="Hi Wax Point, I have a question about my aftercare." href="#">WhatsApp us</a><a class="btn alt" data-link="phone" href="#">Call</a></div>
  </div>
</section>
"""
    return layout("aftercare", "Waxing & Laser Aftercare — Wax Point",
                  "Before and aftercare advice for waxing and laser hair removal from Wax Point, West Ealing.",
                  body, "aftercare.html")


def page_privacy():
    body = """
<section>
  <div class="wrap" style="max-width:820px">
    <h1>Privacy notice</h1>
    <p class="muted small">Draft — to be reviewed by the salon owner before going live.</p>
    <h3>Who we are</h3>
    <p>Wax Point, Unit 5, 36-38 Broadway, West Ealing, London W13 0SU. Contact us via WhatsApp or phone on 07702 014136 about anything in this notice.</p>
    <h3>What we collect and why</h3>
    <ul class="care-list">
      <li><strong>Bookings</strong> are handled by Treatwell under their own privacy policy.</li>
      <li><strong>Laser consultation form:</strong> your contact details and health information, used only to assess whether treatment is safe for you (legal basis: your explicit consent and our legitimate interest in providing safe treatment).</li>
      <li><strong>Payments</strong> are processed by our payment providers (Stripe, Klarna, SumUp). We never see or store your full card details.</li>
      <li><strong>WhatsApp messages</strong> you send us are kept only as long as needed to answer you.</li>
    </ul>
    <h3>How long we keep it</h3>
    <p>Consultation and treatment records are kept for as long as you are a client and for a limited period afterwards to meet insurance requirements, then deleted.</p>
    <h3>Your rights</h3>
    <p>You can ask to see, correct or delete your information, or withdraw consent, at any time. You can also complain to the Information Commissioner's Office (ico.org.uk).</p>
    <h3>Cookies</h3>
    <p>This website doesn't set its own tracking cookies. The embedded Google map and links to Treatwell, Instagram, Stripe and Klarna are subject to those services' own policies.</p>
  </div>
</section>
"""
    return layout("privacy", "Privacy — Wax Point", "Privacy notice for Wax Point, West Ealing.", body, "privacy.html")


PAGES = {
    "index.html": page_index,
    "laser.html": page_laser,
    "consultation.html": page_consultation,
    "aftercare.html": page_aftercare,
    "privacy.html": page_privacy,
}

if __name__ == "__main__":
    for name, fn in PAGES.items():
        (ROOT / name).write_text(fn())
        print("built", name)
    urls = "".join(f"<url><loc>{SALON['site']}/{'' if n == 'index.html' else n}</loc></url>" for n in PAGES)
    (ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SALON['site']}/sitemap.xml\n")
    print("built sitemap.xml, robots.txt")
