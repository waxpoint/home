#!/usr/bin/env python3
"""Builds the Wax Point static site:  python3 tools/build.py
Edit data/laser-prices.json (prices), data/photos.json (photos) or the page text below, then run this script.
"""
import json
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "data" / "laser-prices.json").read_text())
PHOTOS = json.loads((ROOT / "data" / "photos.json").read_text())

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


# ---------- helpers ----------

def money(n):
    return f"£{n:,}"


def fmt_time(t):
    h, m = map(int, t.split(":"))
    suffix = "am" if h < 12 else "pm"
    h12 = h if 1 <= h <= 12 else (h - 12 if h > 12 else 12)
    return f"{h12}{'' if m == 0 else ':%02d' % m}{suffix}"


_ICON_CACHE = {}


def icon(name, cls="ico"):
    """Inline a Phosphor (light) icon from assets/icons so it inherits text colour."""
    if name not in _ICON_CACHE:
        svg = (ROOT / "assets" / "icons" / f"{name}.svg").read_text().strip()
        _ICON_CACHE[name] = re.sub(r"^<svg ", '<svg aria-hidden="true" focusable="false" class="{cls}" ', svg)
    return _ICON_CACHE[name].replace("{cls}", cls)


def photo(key, w, h, cls="", eager=False):
    p = PHOTOS[key]
    alt = e(p["alt"])
    if p.get("local"):
        full = p["local"]
        small = full.replace(".jpg", "-sm.jpg")
        has_small = (ROOT / small).exists()
        src = small if (has_small and w <= 450) else full
        srcset = f' srcset="{small} 700w, {full} 1400w" sizes="(max-width: 980px) 90vw, {w}px"' if has_small else ""
    else:
        base = f"https://images.unsplash.com/photo-{p['id']}?auto=format&fit=crop&crop=entropy&q=78"
        src = f"{base}&w={w}&h={h}"
        srcset = f' srcset="{base}&w={w}&h={h} 1x, {base}&w={w*2}&h={h*2} 2x"'
    pos = f' style="object-position:{p["pos"]}"' if p.get("pos") else ""
    loading = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return f'<div class="frame {cls}"><img src="{src}"{srcset} alt="{alt}" width="{w}" height="{h}" {loading}{pos}></div>'


def stars():
    return '<span class="stars" aria-label="5 out of 5 stars">' + icon("star-fill") * 5 + "</span>"


# ---------- layout ----------

def layout(page_id, title, description, body, path):
    left = [("laser", "laser.html", "Laser"), ("consultation", "consultation.html", "Consultation"), ("aftercare", "aftercare.html", "Aftercare")]
    right = [("visit", "index.html#visit", "Visit")]

    def links(items):
        return "".join(
            f'<a href="{href}"{" aria-current=\"page\"" if pid == page_id else ""}>{label}</a>' for pid, href, label in items
        )

    sheet_links = "".join(f'<a href="{href}">{label}</a>' for _, href, label in [("home", "index.html", "Home")] + left + right)
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
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:image" content="{SALON['site']}/assets/og-image.jpg">
<meta property="og:type" content="website">
<meta name="theme-color" content="#fbf9f7">
<link rel="icon" href="assets/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="preconnect" href="https://images.unsplash.com">
<link rel="preload" href="assets/fonts/cormorant-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/styles.css">
<script>document.documentElement.classList.add("js")</script>
<script type="application/ld+json">{json.dumps(ld)}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <button class="menu-btn" aria-label="Menu" aria-expanded="false" aria-controls="sheet"><span class="i-open">{icon("list")}</span><span class="i-close" style="display:none">{icon("x")}</span></button>
    <nav class="nav" aria-label="Main">{links(left)}</nav>
    <a class="brand" href="index.html" aria-label="Wax Point — home"><img src="assets/logo-header.png" alt="Wax Point — beauty, waxing, laser" width="188" height="34"></a>
    <nav class="nav nav-right" aria-label="Secondary">{links(right)}<a class="btn sm" data-link="book" href="#">Book now</a></nav>
    <a class="btn sm header-book-sm" data-link="book" href="#">Book</a>
  </div>
</header>
<div class="scrim"></div>
<nav class="sheet" id="sheet" aria-label="Menu">{sheet_links}<a class="btn" data-link="book" href="#">Book an appointment</a></nav>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div>
      <div class="footer-name">Wax Point</div>
      <p>Beauty, waxing &amp; laser in West Ealing since 2019.</p>
      <p>{e(SALON['street'])}<br>{e(SALON['area'])}, {e(SALON['city'])} {e(SALON['postcode'])}</p>
    </div>
    <div>
      <h4>Get in touch</h4>
      <ul>
        <li><a data-link="whatsapp" href="#">WhatsApp</a></li>
        <li><a data-link="phone" href="#">{SALON['phone_display']}</a></li>
        <li><a data-link="instagram" href="#">Instagram</a></li>
        <li><a data-link="treatwell" href="#">Treatwell</a></li>
      </ul>
    </div>
    <div>
      <h4>Clients</h4>
      <ul>
        <li><a href="laser.html">Laser prices &amp; packages</a></li>
        <li><a href="consultation.html">Laser consultation</a></li>
        <li><a href="aftercare.html">Before &amp; aftercare</a></li>
        <li><a href="privacy.html">Privacy &amp; credits</a></li>
      </ul>
    </div>
    <p class="legal">&copy; <span id="year">2026</span> Wax Point. Prices in GBP. Laser courses are sold only after a free consultation and patch test.</p>
  </div>
</footer>
<a class="wa-float" data-link="whatsapp" href="#" aria-label="Message us on WhatsApp">{icon("whatsapp-logo")}<span>WhatsApp</span></a>
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
        items.append(f'<li{" class=\"closed\"" if not o else ""}><span>{d}</span><span>{val}</span></li>')
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
            f'<thead><tr><th scope="col">Area <span class="hide-sm">· per session</span></th>{head}</tr></thead>'
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
                f'<li><span>{p} sessions<span class="total">{money(v * p)} course</span></span>'
                f'<span class="per">{money(v)}<span class="total">per session</span></span>'
                f'<a class="btn soft sm" data-pay="{key}" href="#">Pay for course</a></li>'
            )
        cards.append(
            f'<article class="pkg"><span class="tag">{i}</span><h4>{e(r["name"])}</h4>{detail}'
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


def page_hero(eyebrow, title, script, lead, buttons, photo_key):
    return f"""
<section class="page-hero">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">{eyebrow}</span>
      <h1>{title}<span class="script">{script}</span></h1>
      <p class="lead">{lead}</p>
      <div class="btn-row">{buttons}</div>
    </div>
    <div class="reveal">{photo(photo_key, 560, 640, "wide")}</div>
  </div>
</section>"""


# ---------- pages ----------

def page_index():
    wax = "".join(
        f'<li><span>{e(r["name"])}<span class="dur">{e(r["duration"])}</span></span><span class="price">{e(r["price"])}</span></li>'
        for r in DATA["waxing_highlights"]["rows"]
    )
    lowest = min(min(r["prices"]) for s in DATA["sections"] for r in s["rows"])
    n_pkgs = sum(len(s["rows"]) for s in DATA["sections"] if s["kind"] == "packages")
    map_src = "https://maps.google.com/maps?q=Wax%20Point%2C%2036-38%20Broadway%2C%20London%20W13%200SU&z=16&output=embed"
    body = f"""
<section class="hero">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">West Ealing · Since 2019</span>
      <h1 class="display">Smooth skin,<span class="script">the gentle way</span></h1>
      <p class="lead">Over 15 years of experience, techniques designed to keep waxing as pain-free as possible, and a spotless, calm studio five minutes from West Ealing station.</p>
      <div class="btn-row">
        <a class="btn" data-link="book" href="#">Book an appointment</a>
        <a class="btn ghost" href="laser.html">Laser prices</a>
      </div>
      <div class="rating">{stars()} <span><strong>5.0</strong> from 1,000+ Treatwell reviews</span></div>
    </div>
    <div class="reveal">
      {photo("hero", 600, 750, "tall", eager=True)}
    </div>
  </div>
</section>

<div class="values">
  <div>{icon("seal-check")}<span><strong>15+ years</strong>of expert hands</span></div>
  <div>{icon("hand-heart")}<span><strong>Gentle technique</strong>as pain-free as possible</span></div>
  <div>{icon("shield-check")}<span><strong>Spotless studio</strong>hygiene first, always</span></div>
  <div>{icon("star")}<span><strong>5.0 rating</strong>from 1,000+ reviews</span></div>
</div>

<section id="treatments">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">What we do</span>
      <h2>Explore our<span class="script">treatments</span></h2>
    </div>
    <div class="cards">
      <article class="card-t reveal">
        {photo("waxing", 420, 420, "square")}
        <span class="meta">{icon("drop")} Hot &amp; strip wax</span>
        <h3>Waxing</h3>
        <p>Face and body waxing for ladies and gents, from brows to Hollywood, with techniques refined over 15 years.</p>
        <a class="link" href="#waxing-menu">See prices {icon("arrow-right")}</a>
      </article>
      <article class="card-t reveal">
        {photo("laser", 420, 420, "square")}
        <span class="meta">{icon("lightning")} Courses of 6, 8 or 10</span>
        <h3>Laser</h3>
        <p>Long-term hair reduction from {money(lowest)} per session, with {n_pkgs} money-saving packages and a free consultation first.</p>
        <a class="link" href="laser.html">Laser prices {icon("arrow-right")}</a>
      </article>
      <article class="card-t reveal">
        {photo("brows", 420, 420, "square")}
        <span class="meta">{icon("eye")} Brows &amp; lashes</span>
        <h3>Brows</h3>
        <p>Brow shaping, tints and the eye trio — brow wax with brow and lash tint — for a polished, low-maintenance look.</p>
        <a class="link" data-link="book" href="#">Book on Treatwell {icon("arrow-right")}</a>
      </article>
    </div>
  </div>
</section>

<section class="tint">
  <div class="wrap split">
    <div class="reveal">
      {photo("studio", 560, 700, "tall")}
    </div>
    <div class="reveal">
      <span class="eyebrow">Your therapist</span>
      <h2>Meet Emilia</h2>
      <p class="lead">Wax Point is run by Emilia, a waxing specialist with over 15 years of experience. Her own techniques keep treatments quick, thorough and as comfortable as possible — which is why so many clients have stayed with her for years.</p>
      <ul class="ico-list" style="margin:28px 0 34px">
        <li>{icon("check-circle")}<span>Hot wax for sensitive and intimate areas</span></li>
        <li>{icon("check-circle")}<span>Free patch test before your first treatment</span></li>
        <li>{icon("check-circle")}<span>Ladies and gents welcome</span></li>
      </ul>
      <a class="link" data-link="treatwell" href="#">Read 1,000+ reviews {icon("arrow-right")}</a>
    </div>
  </div>
</section>

<section class="white" id="waxing-menu">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">Waxing menu</span>
      <h2>Popular<span class="script">treatments</span></h2>
      <p class="muted">A few favourites. Every area and waxing package is on our Treatwell menu, where you can book instantly.</p>
      <div class="btn-row" style="margin-top:28px"><a class="btn" data-link="book" href="#">Full menu &amp; booking</a></div>
    </div>
    <ul class="menu-list reveal">{wax}</ul>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Laser hair removal</span>
      <h2>Your laser<span class="script">journey</span></h2>
    </div>
    <div class="steps">
      <div class="step reveal"><span class="num">1</span><div class="ico-badge">{icon("clipboard-text")}</div><h3>Consultation</h3><p>A short health questionnaire and a chat about your skin, hair and goals. Always free.</p></div>
      <div class="step reveal"><span class="num">2</span><div class="ico-badge">{icon("drop-half-bottom")}</div><h3>Patch test</h3><p>A quick test on a small area to check how your skin responds, at no cost.</p></div>
      <div class="step reveal"><span class="num">3</span><div class="ico-badge">{icon("calendar-check")}</div><h3>Your course</h3><p>Choose 6, 8 or 10 sessions. Pay by card in the salon, or online with card or Klarna.</p></div>
    </div>
    <div class="btn-row center" style="margin-top:48px;justify-content:center"><a class="btn" data-link="whatsapp" data-wa-text="Hi Wax Point, I'd like to book a free laser consultation." href="#">{icon("whatsapp-logo")} WhatsApp us</a><a class="btn ghost" data-link="phone" href="#">{icon("phone")} Call</a><a class="btn ghost" href="laser.html">See laser prices</a></div>
  </div>
</section>

<section class="white">
  <div class="wrap split reverse">
    <div class="reveal">{photo("good_to_know", 560, 700, "tall")}</div>
    <div class="reveal">
      <span class="eyebrow">Good to know</span>
      <div class="info"><h4>{icon("calendar-blank")} Appointments</h4><p>Book online any time through Treatwell, or message us on WhatsApp. If you need to cancel or reschedule, please let us know as early as you can so we can offer your slot to someone else.</p></div>
      <div class="info"><h4>{icon("credit-card")} Paying for laser</h4><p>Pay for your course by card in the salon, or online by card, Apple Pay, Google Pay or Klarna — always after your free patch test.</p></div>
      <div class="info"><h4>{icon("hourglass-medium")} Course validity</h4><p>{e(DATA['validity'])}</p></div>
      <a class="link" href="aftercare.html">Before &amp; aftercare {icon("arrow-right")}</a>
    </div>
  </div>
</section>

<section class="ig-band" data-needs="instagram">
  <div class="wrap reveal">
    <div class="ico-badge">{icon("instagram-logo")}</div>
    <span class="eyebrow">Follow along</span>
    <h2>@waxpoint.london</h2>
    <p class="lead center" style="margin:0 auto 30px">Studio news, offers and last-minute appointments.</p>
    <a class="btn ghost" data-link="instagram" href="#">Follow on Instagram</a>
  </div>
</section>

<section class="tint" id="visit">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">Visit us</span>
      <h2>West Ealing<span class="script">studio</span></h2>
      <div class="contact-line">{icon("map-pin")}<span>{e(SALON['street'])}<br>{e(SALON['area'])}, {e(SALON['city'])} {e(SALON['postcode'])}</span></div>
      <div class="contact-line">{icon("train-simple")}<span>5 minutes' walk from West Ealing station</span></div>
      <div class="contact-line">{icon("clock")}<span>Opening hours</span></div>
      {hours_list()}
      <div class="btn-row">
        <a class="btn" data-link="book" href="#">Book now</a>
        <a class="btn ghost" data-link="whatsapp" href="#">{icon("whatsapp-logo")} WhatsApp</a>
        <a class="btn ghost" data-link="phone" href="#">{icon("phone")} Call</a>
      </div>
    </div>
    <iframe class="map reveal" title="Map to Wax Point, West Ealing" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="{map_src}"></iframe>
  </div>
</section>
"""
    return layout("index", "Wax Point — Waxing & Laser Hair Removal in West Ealing",
                  "Beauty, waxing and laser hair removal in West Ealing, London W13. Free laser consultation and patch test, 5.0 rating from 1,000+ Treatwell reviews.",
                  body, "index.html")


def page_laser():
    hero = page_hero(
        "Laser hair removal",
        "Laser prices", "per session",
        "All prices are per session when you book a course of 6, 8 or 10. The longer the course, the lower the price per session.",
        f'<a class="btn" data-link="whatsapp" data-wa-text="Hi Wax Point, I\'d like to book a free laser consultation." href="#">{icon("whatsapp-logo")} WhatsApp us</a>'
        f'<a class="btn ghost" data-link="phone" href="#">{icon("phone")} Call</a>',
        "laser_page",
    )
    body = hero + f"""
<section class="white" style="padding-top:72px">
  <div class="wrap">
    <div class="note">{icon("first-aid")}<span><strong>Consultation first.</strong> Every laser course starts with a free consultation and patch test, so we can make sure treatment is safe and right for you. Please only pay for a course after your patch test.</span></div>
    <div class="note" data-pay-note>{icon("credit-card")}<span><strong>Paying online.</strong> “Pay for course” opens a secure checkout where you can pay by card, Apple Pay, Google Pay or Klarna. Klarna options depend on eligibility and are explained by Klarna at checkout.</span></div>

    <div data-tabs style="margin-top:48px">
      <div class="tabs" role="tablist" aria-label="Choose prices" data-active="0">
        <span class="pill" aria-hidden="true"></span>
        <button role="tab" id="tab-ladies" aria-controls="panel-ladies" aria-selected="true">{icon("gender-female")} Ladies</button>
        <button role="tab" id="tab-gents" aria-controls="panel-gents" aria-selected="false">{icon("gender-male")} Gents</button>
      </div>
      <div id="panel-ladies" role="tabpanel" aria-labelledby="tab-ladies">{group_panel('ladies')}</div>
      <div id="panel-gents" role="tabpanel" aria-labelledby="tab-gents" hidden>{group_panel('gents')}</div>
    </div>

    <div class="note" style="margin-top:40px">{icon("hourglass-medium")}<span><strong>Validity.</strong> {e(DATA['validity'])} Package prices are per session when you book the whole package.</span></div>
  </div>
</section>

<section>
  <div class="wrap" style="max-width:820px">
    <div class="section-head reveal"><span class="eyebrow">Questions</span><h2>Laser<span class="script">FAQ</span></h2></div>
    <details><summary>How many sessions will I need? {icon("x")}</summary><p>Most people need a course of 6–10 sessions, spaced several weeks apart, because hair grows in cycles. We'll recommend a course at your consultation.</p></details>
    <details><summary>Does it hurt? {icon("x")}</summary><p>Most clients describe a quick snapping or warm sensation. Sensitivity varies by area and we adjust settings to keep you comfortable.</p></details>
    <details><summary>Can I shave between sessions? {icon("x")}</summary><p>Yes, shaving is fine. Please don't wax, pluck, thread or epilate during your course, as laser needs the hair root in place.</p></details>
    <details><summary>Is laser suitable for everyone? {icon("x")}</summary><p>Not always. Some medications, skin conditions, pregnancy and recent sun exposure can mean we need to wait or adjust treatment. That's what the consultation and patch test are for.</p></details>
    <details><summary>How long is my course valid? {icon("x")}</summary><p>{e(DATA['validity'])}</p></details>
  </div>
</section>
"""
    return layout("laser", "Laser Hair Removal Prices — Wax Point, West Ealing",
                  "Laser hair removal prices for ladies and gents in West Ealing. Courses of 6, 8 or 10 sessions, money-saving packages, free consultation and patch test.",
                  body, "laser.html")


def page_consultation():
    hero = page_hero(
        "Free · about 20 minutes",
        "Laser consultation", "your first step",
        "Your consultation and patch test are free. Filling in the questionnaire before your visit saves time and lets us check that laser is safe for you.",
        f'<a class="btn" data-link="whatsapp" data-wa-text="Hi Wax Point, I\'d like to book a free laser consultation." href="#">{icon("whatsapp-logo")} WhatsApp us</a>'
        f'<a class="btn ghost" data-link="phone" href="#">{icon("phone")} Call</a>'
        '<a class="btn ghost" data-link="form" href="#">Fill in the form</a>',
        "consult_page",
    )
    body = hero + f"""
<section class="white">
  <div class="wrap">
    <div class="steps">
      <div class="step reveal"><span class="num">1</span><div class="ico-badge">{icon("clipboard-text")}</div><h3>Questionnaire</h3><p>About 5 minutes: your skin, medication, health and recent sun exposure.</p></div>
      <div class="step reveal"><span class="num">2</span><div class="ico-badge">{icon("drop-half-bottom")}</div><h3>Patch test</h3><p>We talk through your goals, check your skin and hair, and test a small area.</p></div>
      <div class="step reveal"><span class="num">3</span><div class="ico-badge">{icon("calendar-check")}</div><h3>Your plan</h3><p>We recommend the right course and you choose how to pay.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap care-grid">
    <div class="care reveal">
      <h3>{icon("heartbeat")} What we ask</h3>
      <ul class="ico-list">
        <li>{icon("check-circle")}<span>Your skin type and how it reacts to sun</span></li>
        <li>{icon("check-circle")}<span>Medication, including antibiotics, acne treatments and anything that makes skin light-sensitive</span></li>
        <li>{icon("check-circle")}<span>Skin conditions, recent tattoos, scars or cold sores in the area</span></li>
        <li>{icon("check-circle")}<span>Pregnancy or breastfeeding</span></li>
        <li>{icon("check-circle")}<span>Recent tanning, sunbeds or fake tan</span></li>
      </ul>
    </div>
    <div class="care reveal">
      <h3>{icon("sparkle")} Before your test</h3>
      <ul class="ico-list">
        <li>{icon("check-circle")}<span>Shave the area 24 hours before. No waxing, plucking or epilating for 4–6 weeks.</span></li>
        <li>{icon("sun")}<span>Avoid sun, sunbeds and fake tan on the area for 2–4 weeks.</span></li>
        <li>{icon("drop")}<span>Come with clean skin: no creams, deodorant or make-up on the area.</span></li>
        <li>{icon("first-aid")}<span>Tell us about any new medication, even if you've had laser before.</span></li>
      </ul>
    </div>
  </div>
</section>

<section class="white">
  <div class="wrap" style="max-width:820px">
    <div class="note" style="background:var(--paper)">{icon("shield-check")}<span><strong>Your information.</strong> Your answers include health information, so we treat them with extra care. They are used only to decide whether laser treatment is safe for you, stored securely by our form provider, seen only by your therapist and never used for marketing. You can ask us to see or delete them at any time. See our <a href="privacy.html">privacy notice</a>.</span></div>
  </div>
</section>
"""
    return layout("consultation", "Free Laser Consultation — Wax Point, West Ealing",
                  "Book a free laser hair removal consultation and patch test at Wax Point, West Ealing. Fill in the questionnaire online before your visit.",
                  body, "consultation.html")


def care_list(items):
    return '<ul class="ico-list">' + "".join(f"<li>{icon(i)}<span>{t}</span></li>" for i, t in items) + "</ul>"


def page_aftercare():
    hero = page_hero(
        "Before &amp; aftercare",
        "Care guide", "for smooth results",
        "A few simple steps make your results smoother and longer-lasting, and keep your skin calm.",
        '<a class="btn" href="#waxing">Waxing</a><a class="btn ghost" href="#laser">Laser</a><a class="btn ghost" href="#help">When to contact us</a>',
        "care_page",
    )
    body = hero + f"""
<section class="white" id="waxing">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Waxing</span><h2>Before &amp;<span class="script">after your wax</span></h2></div>
    <div class="care-grid">
      <div class="care reveal" style="background:var(--paper)"><h3>{icon("calendar-blank")} Before</h3>{care_list([
        ("hourglass-medium", "Let hair grow to about 5 mm, roughly 2–3 weeks after shaving."),
        ("sparkle", "Gently exfoliate the day before, not on the day."),
        ("drop", "Skip creams, oils and fake tan on the area on the day."),
        ("sun", "Avoid sunbathing or sunbeds for 24 hours before."),
        ("first-aid", "Using retinoids or acne medication? Tell us before we start."),
      ])}</div>
      <div class="care reveal" style="background:var(--paper)"><h3>{icon("clock")} First 24–48 hours</h3>{care_list([
        ("thermometer-simple", "No hot baths, saunas, steam rooms or swimming."),
        ("barbell", "Skip the gym and heavy sweating."),
        ("sun", "No sunbathing, sunbeds or fake tan."),
        ("leaf", "Wear loose, breathable clothing over the area."),
        ("drop", "Avoid perfumed products, deodorant (underarms) and make-up (face)."),
      ])}</div>
      <div class="care reveal" style="background:var(--paper)"><h3>{icon("sparkle")} After 48 hours</h3>{care_list([
        ("shower", "Exfoliate gently 2–3 times a week to prevent ingrown hairs."),
        ("drop", "Moisturise daily with an unperfumed lotion."),
        ("hand-heart", "Avoid shaving between waxes so hair grows back finer."),
        ("calendar-check", "Book your next wax in 4–6 weeks."),
      ])}</div>
      <div class="care reveal" style="background:var(--paper)"><h3>{icon("snowflake")} Is this normal?</h3><p class="muted">Some redness and small bumps are normal and usually settle within a few hours to a day. A cool compress helps. If redness, swelling or spots get worse after 48 hours, contact us.</p></div>
    </div>
  </div>
</section>

<section id="laser">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Laser</span><h2>Laser<span class="script">aftercare</span></h2></div>
    <div class="care-grid">
      <div class="care reveal"><h3>{icon("calendar-blank")} Before each session</h3>{care_list([
        ("check-circle", "Shave the area 24 hours before. Don't wax, pluck, thread or epilate during your course."),
        ("sun", "No sun, sunbeds or fake tan on the area for 2–4 weeks before."),
        ("drop", "Come with clean skin: no creams, deodorant or make-up."),
        ("first-aid", "Tell us about any new medication or health changes."),
      ])}</div>
      <div class="care reveal"><h3>{icon("clock")} First 48 hours</h3>{care_list([
        ("snowflake", "Skin may look pink and feel warm, like mild sunburn. A cool compress or aloe vera gel soothes it."),
        ("thermometer-simple", "No hot baths, saunas, steam rooms, swimming or intense exercise."),
        ("drop", "Avoid perfumed products, deodorant (underarms) and make-up (face)."),
        ("hand-heart", "Don't scrub or exfoliate the area."),
      ])}</div>
      <div class="care reveal"><h3>{icon("sun")} During your course</h3>{care_list([
        ("sun", "Use SPF 30+ on treated areas exposed to the sun, and avoid sunbeds completely."),
        ("waves", "Shaving is fine. Treated hairs may shed for 1–3 weeks; this is normal."),
        ("shower", "Exfoliate gently after the first week to help shedding hairs come out."),
        ("calendar-check", "Keep to your session schedule for the best results."),
      ])}</div>
      <div class="care reveal"><h3>{icon("eye")} Is this normal?</h3><p class="muted">Redness and small raised bumps around follicles are common and usually fade within 24–48 hours. Blistering, crusting or changes in skin colour are not expected — contact us straight away if you notice them.</p></div>
    </div>
  </div>
</section>

<section class="white" id="help">
  <div class="wrap center reveal" style="max-width:760px">
    <div class="ico-badge" style="margin:0 auto 20px">{icon("chat-circle-text")}</div>
    <h2>When to<span class="script">contact us</span></h2>
    <p class="lead">Message us if redness or swelling hasn't settled after 48 hours, or if you notice blisters, crusting, spots that look infected or any change in skin colour. For a severe reaction, contact your GP or NHS 111.</p>
    <div class="btn-row" style="justify-content:center;margin-top:26px"><a class="btn" data-link="whatsapp" data-wa-text="Hi Wax Point, I have a question about my aftercare." href="#">{icon("whatsapp-logo")} WhatsApp us</a><a class="btn ghost" data-link="phone" href="#">{icon("phone")} Call</a></div>
  </div>
</section>
"""
    return layout("aftercare", "Waxing & Laser Aftercare — Wax Point",
                  "Before and aftercare advice for waxing and laser hair removal from Wax Point, West Ealing.",
                  body, "aftercare.html")


def page_privacy():
    credits = "".join(
        f"<li>{e(v['alt'])} — photo by {e(v['credit'])} on Unsplash</li>"
        for k, v in PHOTOS.items() if not k.startswith("_") and not v.get("local")
    )
    body = f"""
<section>
  <div class="wrap" style="max-width:820px">
    <span class="eyebrow">Legal</span>
    <h1>Privacy</h1>
    <p class="muted small">Draft — to be reviewed by the salon owner before going live.</p>
    <h3>Who we are</h3>
    <p>Wax Point, Unit 5, 36-38 Broadway, West Ealing, London W13 0SU. Contact us via WhatsApp or on 07702 014136 about anything in this notice.</p>
    <h3>What we collect and why</h3>
    <ul class="ico-list" style="margin-bottom:24px">
      <li>{icon("calendar-check")}<span><strong>Bookings</strong> are handled by Treatwell under their own privacy policy.</span></li>
      <li>{icon("clipboard-text")}<span><strong>Laser consultation form:</strong> your contact details and health information, used only to assess whether treatment is safe for you (legal basis: your explicit consent).</span></li>
      <li>{icon("credit-card")}<span><strong>Payments</strong> are processed by our payment providers (Stripe, Klarna, SumUp). We never see or store your full card details.</span></li>
      <li>{icon("chat-circle-text")}<span><strong>WhatsApp messages</strong> are kept only as long as needed to answer you.</span></li>
    </ul>
    <h3>How long we keep it</h3>
    <p>Consultation and treatment records are kept while you are a client and for a limited period afterwards to meet insurance requirements, then deleted.</p>
    <h3>Your rights</h3>
    <p>You can ask to see, correct or delete your information, or withdraw consent, at any time. You can also complain to the Information Commissioner's Office (ico.org.uk).</p>
    <h3>Cookies</h3>
    <p>This website doesn't set its own tracking cookies. Photos load from Unsplash, and the embedded Google map and links to Treatwell, Instagram, Stripe and Klarna are subject to those services' own policies.</p>
    <h3>Credits</h3>
    <p class="muted small">Photos from Unsplash under the Unsplash License. Icons: Phosphor Icons (MIT). Fonts: Cormorant Garamond, Montserrat, Mrs Saint Delafield (SIL Open Font License).</p>
    <ul class="small muted">{credits}</ul>
  </div>
</section>
"""
    return layout("privacy", "Privacy — Wax Point", "Privacy notice and credits for Wax Point, West Ealing.", body, "privacy.html")


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
