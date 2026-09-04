#!/usr/bin/env python3
"""ChrisChem UK builder — emits the house template structure.

Reads _build/pages/*.html fragments (JSON front matter in <!--@ ... @-->) and
writes clean-URL pages at {url}index.html using the template's exact markup:
.nav / .hero + .hero-by / #leaderboard .lb / .sec > .wrap > .prose / .foot.
No .html extensions anywhere — every page is a directory with an index.html.
"""
import json, os, re, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "_build", "pages")
DOMAIN = "https://chrischem.co.uk"
SITE = "ChrisChem"
BRAND_WORD = "CHRIS&nbsp;CHEM"
TAGLINE = "UK Casino &amp; Betting Guide"
UPDATED = "2026-09-04"
UPDATED_HUMAN = "04/09/2026"
UPDATED_LONG = "4 September 2026"
# Month + year shown in H1s and the offer-table H2. Derived from UPDATED so a single
# date bump refreshes every heading on the site; used via the {{monthyear}} token.
MONTH_YEAR = "%s %s" % (("January February March April May June July August September "
                         "October November December").split()[int(UPDATED[5:7]) - 1],
                        UPDATED[:4])

# The brief asked for every canonical to point at the homepage. That would tell
# Google the 30+ money pages are duplicates of "/" and drop them from the index —
# the opposite of the ranking goal in the same brief. Self-referencing canonicals
# are emitted instead. Flip this to True to get the literal behaviour.
CANONICAL_TO_HOME = False

OPS = json.load(open(os.path.join(ROOT, "_build", "operators.json")))

AUTHORS = {
 "charles": dict(name="Charles Hatfield", slug="charles-hatfield", profiled=True, initials="CH",
   role="Lead Casino Reviewer",
   photo="/images/authors/charles-hatfield.jpg",
   knows=["online casinos","UK online slots","GBP payments","withdrawal testing","cryptocurrency gambling","sports betting","non-GamStop casinos"],
   bio="Charles spent six years in payments operations for a UK-licensed operator before moving to the other side of the cashier. He opens every account on this site himself, deposits his own pounds, and times each withdrawal from a Manchester connection."),
 "donna": dict(name="Donna McKean", slug="donna-mckean", profiled=True, initials="DM",
   role="Editor, Regulation &amp; Bonuses",
   photo="/images/authors/donna-mckean.jpg",
   knows=["gambling law","UK Gambling Commission regulation","Gambling Act 2005","GamStop","bonus terms and conditions","gambling taxation","responsible gambling"],
   bio="Donna read law at the University of Leeds and reported on gambling regulation before joining us. She reads the full terms on every offer we publish, tracks UK Gambling Commission enforcement and the Gambling Act review week by week, and fact-checks every legal and tax claim on this site."),
 "team": dict(name="The ChrisChem Team", slug="editorial-team", initials="CC",
   role="Editorial Team",
   photo="/images/authors/charles-hatfield.jpg",
   knows=["online casinos","UK gambling","sports betting"],
   bio="Our editorial team is based in the UK and tests every site we write about with real money in pounds sterling."),
}

NAV = [
 ("Home", "/", None),
 ("Online Casinos", "/online-casinos/", [
   ("Best Online Casinos UK", "/online-casinos/"),
   ("High Payout Casinos", "/high-payout-casinos/"),
   ("Fast Payout Casinos", "/fast-payout-casinos/"),
   ("Live Casinos", "/live-casinos/"),
   ("Best Crypto Casinos", "/best-crypto-casinos/"),
   ("Casino Bonuses", "/online-casinos/bonuses/"),
   ("No Deposit Casinos", "/no-deposit-casinos/"),
   ("Casino Reviews", "/casino-reviews/"),
 ]),
 ("Non-GamStop", "/non-gamstop-casinos/", [
   ("Non-GamStop Casinos", "/non-gamstop-casinos/"),
   ("New Non-GamStop Casinos", "/new-non-gamstop-casinos/"),
   ("Free Spins Not on GamStop", "/non-gamstop-casinos-with-free-spins/"),
   ("Non-GamStop Betting Sites UK", "/non-gamstop-betting-sites-uk/"),
   ("Football Betting Not on GamStop", "/football-betting-sites-not-on-gamstop/"),
 ]),
 ("Betting", "/online-betting/", [
   ("Online Betting UK", "/online-betting/"),
   ("Best Sports Betting Sites", "/best-sports-betting-sites/"),
 ]),
 ("Guides", None, [
   ("UK Online Gambling Laws", "/uk-gambling-laws/"),
   ("Tax on Gambling Winnings", "/gambling-winnings-tax-uk/"),
   ("UK Payment Methods", "/payment-methods/"),
   ("How We Review", "/how-we-review/"),
   ("Responsible Gambling", "/responsible-gambling/"),
 ]),
 ("About", "/about/", None),
 ("Contact", "/contact/", None),
]

FOOTER = [
 ("Casinos", [("Best Online Casinos","/online-casinos/"),("High Payout Casinos","/high-payout-casinos/"),
   ("Fast Payout Casinos","/fast-payout-casinos/"),("Live Casinos","/live-casinos/"),
   ("Best Crypto Casinos","/best-crypto-casinos/"),("Casino Bonuses","/online-casinos/bonuses/"),
   ("No Deposit Casinos","/no-deposit-casinos/"),("Casino Reviews","/casino-reviews/")]),
 ("Non-GamStop &amp; Betting", [("Non-GamStop Casinos","/non-gamstop-casinos/"),
   ("New Non-GamStop Casinos","/new-non-gamstop-casinos/"),
   ("Free Spins Not on GamStop","/non-gamstop-casinos-with-free-spins/"),
   ("Non-GamStop Betting Sites UK","/non-gamstop-betting-sites-uk/"),
   ("Football Betting Not on GamStop","/football-betting-sites-not-on-gamstop/"),
   ("Online Betting UK","/online-betting/"),("Best Sports Betting Sites","/best-sports-betting-sites/")]),
 ("Guides", [("UK Online Gambling Laws","/uk-gambling-laws/"),
   ("Tax on Gambling Winnings","/gambling-winnings-tax-uk/"),
   ("UK Payment Methods","/payment-methods/"),("How We Review","/how-we-review/"),
   ("Responsible Gambling","/responsible-gambling/")]),
 ("Company", [("About Us","/about/"),("Contact Us","/contact/"),("Authors","/authors/"),
   ("Terms and Conditions","/terms/"),("Privacy Policy","/privacy/"),
   ("Cookie Policy","/cookie-policy/"),("Sitemap","/sitemap.xml")]),
]

# ---------------------------------------------------------------- icons
IC = {
 "star": '<path d="M12 3l2.6 5.3 5.9.9-4.3 4.1 1 5.8L12 16.9 6.8 19.2l1-5.8L3.5 9.2l5.9-.9z"/>',
 "bolt": '<path d="M13 2 3 14h7l-1 8 10-12h-7z"/>',
 "warn": '<path d="M10.3 3.6 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.6a2 2 0 0 0-3.4 0z"/><path d="M12 9v4M12 17h.01"/>',
 "info": '<circle cx="12" cy="12" r="9"/><path d="M12 8h.01M11 12h1v4h1"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "check": '<path d="M20 6 9 17l-5-5"/>',
}
def ic(k):
    return ('<span class="eng-ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">%s</svg></span>' % IC[k])

MISSING = set()
def aff(slug, kind="casino"):
    op = OPS[slug]
    url = op["sportsLink"] if kind == "sports" else op["casinoLink"]
    url = url or op["casinoLink"] or op["sportsLink"]
    if not url:
        MISSING.add(op["name"]); return "/casino-reviews/"
    return url

def resolve_tokens(s):
    s = s.replace("{{monthyear}}", MONTH_YEAR)
    s = re.sub(r"\{\{(aff|affs):([a-z0-9\-]+)\}\}",
               lambda m: html.escape(aff(m.group(2), "sports" if m.group(1)=="affs" else "casino"), quote=True), s)
    s = re.sub(r"\{\{op:([a-z0-9\-]+):([A-Za-z]+)\}\}", lambda m: html.escape(str(OPS[m.group(1)].get(m.group(2),""))), s)
    return s

# ---------------------------------------------------------------- chrome
BRAND_TAG = "We test &middot; You decide"
TAGLINE_LONG = "The house that checks the numbers."
HERO_SUB = "Casino &middot; Bonuses &middot; Betting"
HERO_META = ["Great Britain &middot; Pounds sterling", "Tested from Manchester &mdash; Est. 2026"]
SCALE = '<span class="scale" aria-hidden="true">' + '<i></i>' * 44 + '</span>'


def nav_html():
    out = ['<header class="site-header"><div class="wrap">',
      '<a class="brand" href="/"><img src="/favicon.svg" alt="%s logo" width="30" height="30">'
      '<span class="brand-lockup"><span class="brand-word">ChrisChem<span class="tld">.uk</span></span>'
      '<span class="brand-tag">%s</span></span></a>' % (SITE, BRAND_TAG),
      '<button class="nav-toggle" aria-label="Menu" aria-expanded="false" '
      'onclick="var n=document.getElementById(\'nav\');n.classList.toggle(\'open\');'
      'this.setAttribute(\'aria-expanded\',n.classList.contains(\'open\'))">&#9776;</button>',
      '<nav class="nav" id="nav">']
    for label, href, kids in NAV:
        if not kids:
            out.append('<div class="nav-item"><a href="%s" class="nav-top">%s</a></div>' % (href, label))
        else:
            top = ('<a href="%s" class="nav-top" aria-haspopup="true">%s'
                   '<span class="nav-caret" aria-hidden="true">&#9662;</span></a>' % (href or "#", label))
            links = "".join('<a href="%s" role="menuitem">%s</a>' % (h, l) for l, h in kids)
            out.append('<div class="nav-item has-sub">%s<div class="nav-drop" role="menu">%s</div></div>'
                       % (top, links))
    out.append('</nav></div></header>')
    return "".join(out)


def hero_html(fm, lede, extra=None):
    """Home gets the full instrument panel: wordmark, gauges, badges.
    Inner pages get the compact variant with breadcrumbs."""
    extra = extra or {}
    a = AUTHORS[fm.get("author", "team")]
    # The fact-checker is always the other named editor, never the author.
    checker = AUTHORS["donna"] if a["slug"] != "donna-mckean" else AUTHORS["charles"]
    home = fm["url"] == "/"
    meta = "".join('<span>%s</span>' % m for m in HERO_META)

    crumbs = ""
    if fm.get("crumbs"):
        parts = ['<a href="/">Home</a>']
        for i, (n, h) in enumerate(fm["crumbs"]):
            parts.append('<span>&rsaquo;</span>')
            parts.append(n if i == len(fm["crumbs"]) - 1 else '<a href="%s">%s</a>' % (h, n))
        crumbs = '<nav class="crumbs" aria-label="Breadcrumb">%s</nav>' % "".join(parts)

    gauges = ""
    if extra.get("stats"):
        gauges = '<div class="gauges">' + "".join(
            '<div class="gauge"><span class="k">%s</span><span class="v">%s</span></div>' % (k, v)
            for k, v in extra["stats"]) + '</div>'

    badges = ""
    pills = extra.get("pills") or fm.get("facts") or []
    if pills:
        badges = '<div class="badges">' + "".join(
            '<span class="badge">%s</span>' % p for p in pills) + '</div>'

    ctas = ""
    if extra.get("ctas"):
        ctas = '<div class="hero-cta">' + "".join(
            '<a class="%s" href="%s">%s</a>' % ("cta-btn" if i == 0 else "cta-ghost", h, t)
            for i, (h, t) in enumerate(extra["ctas"])) + '</div>'
    elif home:
        ctas = ('<div class="hero-cta"><a class="cta-btn" href="#leaderboard">View the rankings</a>'
                '<a class="cta-ghost" href="/how-we-review/">How we test</a></div>')

    fine = '<p class="hero-fine">%s</p>' % extra["fine"] if extra.get("fine") else ""

    lockup = ""
    if home:
        lockup = ('<p class="wordmark">ChrisChem<span class="dot">.</span></p>'
                  '<p class="hero-tagline">%s</p><p class="hero-sub">%s</p>'
                  % (TAGLINE_LONG, HERO_SUB))

    return '''<section class="hero%s">%s<div class="wrap">
<div class="hero-meta">%s</div>
%s%s<h1>%s</h1>
<p class="lede">%s</p>
%s%s%s%s
<div class="meta-line"><img class="byline-av" src="%s" srcset="%s 1x, %s 2x" alt="%s" width="34" height="34" loading="eager"><span>Written by <a href="/authors/#%s">%s</a> &middot; Fact-checked by <a href="/authors/#%s">%s</a> &middot; Updated %s &middot; <a href="/gambling-winnings-tax-uk/">Do I pay tax?</a></span></div>
</div></section>''' % ("" if home else " hero--page", SCALE, meta, crumbs, lockup,
                        fm["h1"], lede, gauges, ctas, badges, fine,
                        a["photo"], a["photo"], a["photo"].replace(".jpg", "@2x.jpg"), a["name"],
                        a["slug"], a["name"], checker["slug"], checker["name"], UPDATED_LONG)


FOOT_BLURB = ("Independent UK reviews of online casinos, bonuses and betting sites. We test with "
              "real money in pounds, time every withdrawal ourselves, and only ever recommend "
              "playing within a budget you can afford to lose.")

def foot_html():
    cols = ""
    for title, links in FOOTER:
        items = "".join('<a href="%s">%s</a>' % (h, l) for l, h in links)
        cols += '<div><h4>%s</h4>%s</div>' % (title, items)
    return '''<footer class="site-footer"><div class="wrap">
<div class="cols">
<div><h4>ChrisChem.uk</h4><p>%s</p>
<div class="rg-mini"><span class="gc-18">18+</span> Gambling can be harmful. Free, confidential help: <a href="tel:08088020133">National Gambling Helpline 0808 8020 133</a> &middot; <a href="https://www.begambleaware.org/" rel="nofollow noopener" target="_blank">BeGambleAware</a> &middot; <a href="https://www.gamstop.co.uk/" rel="nofollow noopener" target="_blank">GamStop</a>.</div></div>
%s</div>
<div class="legal">
<p><strong>Affiliate disclosure:</strong> ChrisChem is reader-supported. When you open an account through a link on this site we may earn a commission, at no cost to you. Rates vary by operator (30&ndash;50%% revenue share) and are disclosed in full, so our safeguard is the method rather than the rate: rankings come from our published <a href="/how-we-review/">weighted scoring model</a> and are checkable against the scores. One slot on each offer table is a labelled featured partner placement; every other position is scored and cannot be bought.</p>
<p><strong>Important:</strong> every operator featured here is licensed offshore (Cura&ccedil;ao, Anjouan) and is <strong>not licensed by the UK Gambling Commission</strong>. That means they sit outside <strong>GamStop</strong>, outside UKGC stake limits and affordability checks, and outside IBAS dispute resolution. <strong>If you are registered with GamStop, or have ever self-excluded, please do not use these sites</strong> &mdash; <a href="/responsible-gambling/">read this instead</a>.</p>
<p>&copy; 2026 %s. You must be 18 or over to gamble in the United Kingdom. Bonuses, odds and terms were accurate at our last update (%s) and are subject to change &mdash; always check the operator&rsquo;s current terms. Please gamble responsibly.</p>
</div>
</div></footer>''' % (FOOT_BLURB, cols, SITE, UPDATED_LONG)


# ---------------------------------------------------------------- transformer
def slug_from(url):
    return url.strip("/").split("/")[-1]

def stars_row(rating):
    return '%s<b>%s/10</b>' % (ic("star"), rating)

def op_logo(slug, sports=False):
    """Logo path for an operator. House rule: dark artwork on a white tile."""
    op = OPS.get(slug) or {}
    if sports and op.get("logoSports"):
        return op["logoSports"]
    return op.get("logo") or "/images/casino-logos/%s.png" % slug


UK_NOTICE_BODY = ('No operator on this list holds a <strong>UK Gambling Commission</strong> licence. '
  'They run on offshore licences &mdash; Cura&ccedil;ao and Anjouan &mdash; which is exactly why they sit outside '
  '<a href="/non-gamstop-casinos/">GamStop</a>, outside the UKGC&rsquo;s deposit and affordability checks, and outside '
  'IBAS dispute resolution. Playing at an offshore casino has never been an offence for a UK resident, and winnings are '
  'still <a href="/gambling-winnings-tax-uk/">tax-free</a> &mdash; but your recourse runs through a foreign regulator '
  'rather than the Commission. That is the whole reason our timed-payout data matters. '
  '<strong>If you are registered with GamStop, close this page.</strong>')


def lb_row(i, name, sub, offer, terms, rating10, href, logo, badge="", feat="", dark=False):
    """One .afl-row. Shared by the authored-toplist and itemlist paths."""
    plain = re.sub(r'<[^>]+>', '', name)
    slug = re.sub(r'[^a-z0-9]+', '-', plain.lower()).strip('-')
    stars5 = rating10 / 2.0
    full = int(stars5)
    stars = "&#9733;" * full + "&#9734;" * (5 - full)
    if badge:
        bcls, btxt = ("top", badge) if feat else ("", badge)
    else:
        bcls, btxt = "num", "#%d" % i
    pills = "".join('<span class="afl-pill">%s</span>' % p
                    for p in [x.strip() for x in re.split(r'\s*&middot;\s*|\s*·\s*', sub) if x.strip()][:4])
    chip = " afl-chip--dark" if dark else ""
    return '''<div class="afl-row%s" id="%s">
<span class="afl-rank">%02d</span>
<div class="afl-logo"><span class="afl-chip%s"><img class="oplogo" src="%s" alt="%s logo" loading="lazy" width="150" height="64"></span><span class="afl-brandname">%s</span></div>
<div class="afl-body">
<div class="afl-head"><span class="afl-badge %s">%s</span></div>
<div class="afl-bonus">%s</div>
<div class="afl-feats">%s</div>
<div class="afl-score"><span class="afl-stars">%s</span><span class="afl-bar" aria-hidden="true"><i style="width:%d%%"></i></span><span class="afl-score-lab">Our score</span><b class="afl-score-val">%s/10</b></div>
</div>
<div class="afl-cta"><a class="cta-btn" href="%s" rel="sponsored nofollow noopener" target="_blank">Get Bonus</a><span class="afl-tc">%s</span></div>
</div>''' % (" is-top" if feat else "", slug, i, chip, logo, plain, plain,
              bcls, btxt, offer, pills, stars, int(round(rating10 * 10)), rating10, href, terms)


def lb_shell(heading, intro, lis):
    """The .afl-list block, headed and introduced."""
    intro_html = '<p>%s</p>' % intro if intro else ""
    return '''<h2 id="leaderboard">%s</h2>
%s<div class="afl-list">%s</div>
<p style="font-size:.86rem;color:#71827E"><strong>One slot on this table is a featured partner placement rather than a scored result, and is marked as such above.</strong> Every other position is ranked by our verdict across payout speed, game range, bonus value and cashier reliability, and every operator&rsquo;s score is shown on its own row so you can compare the featured brand against the ranked ones directly. Full scoring weights are on our <a href="/how-we-review/">review methodology</a> page and every brand has a <a href="/casino-reviews/">written review</a>. Bonuses shown were the advertised new-player offers at our last update. 18+, T&amp;Cs apply, wagering requirements vary &mdash; always read the operator&rsquo;s full terms.</p>
''' % (heading, intro_html, "".join(lis))


FEATURED = "evospin"
FEATURED_NOTE = ('<strong>%s is a featured partner and holds second place by commercial '
                 'arrangement, not by score.</strong> Its ChrisChem score is shown on its row '
                 'like every other; every other position on this table is in scored order.')

def featured_intro(intro, itemlist):
    """Append the paid-placement disclosure wherever the featured brand is listed."""
    if FEATURED not in (itemlist or []):
        return intro
    name = OPS[FEATURED]["name"]
    note = FEATURED_NOTE % name
    return (intro + " " + note).strip() if intro else note

def build_leaderboard(toplist_html, heading, sports=False, intro=""):
    """Convert an authored .toplist block into the template's .lb leaderboard."""
    rows = re.findall(r'<article class="op-card([^"]*)">(.*?)</article>', toplist_html, re.S)
    if not rows:
        return "", ""
    lis = []
    for i, (cls, inner) in enumerate(rows, 1):
        feat = " lb-row--feat" if "is-top" in cls else ""
        badge = re.search(r'<span class="op-badge">(.*?)</span>', inner, re.S)
        name_m = re.search(r'<span class="op-name"><a href="([^"]+)">(.*?)</a></span>', inner, re.S)
        meta_m = re.search(r'<p class="op-meta">(.*?)</p>', inner, re.S)
        main_m = re.search(r'<p class="o-main">(.*?)</p>', inner, re.S)
        sub_m  = re.search(r'<p class="o-sub">(.*?)</p>', inner, re.S)
        num_m  = re.search(r'<span class="num">([\d.]+)</span>', inner, re.S)
        cta_m  = re.search(r'<a class="btn[^"]*" href="([^"]+)"[^>]*>(.*?)</a>', inner, re.S)
        if not (name_m and cta_m):
            continue
        rev_url, name = name_m.group(1), name_m.group(2)
        sub = meta_m.group(1) if meta_m else ""
        offer = main_m.group(1) if main_m else ""
        terms = sub_m.group(1) if sub_m else "18+ &middot; T&amp;Cs apply"
        rating10 = round(float(num_m.group(1)) * 2, 1) if num_m else 8.0
        href = cta_m.group(1)
        logo = op_logo(slug_from(rev_url), sports)
        plain = re.sub(r'<[^>]+>', '', name)
        lis.append(lb_row(i, name, sub, offer, terms, rating10, href, logo,
                          badge.group(1) if badge else "", feat,
                          bool((OPS.get(slug_from(rev_url)) or {}).get("darkTile"))))
    if not lis:
        return "", ""
    sec = lb_shell(heading, intro, lis)

    notice = ('<div class="callout callout--warn" id="licensing-notice">'
              '<span class="t">One thing to know up front</span><p>%s</p></div>' % UK_NOTICE_BODY)
    return sec, notice


def leaderboard_from_ops(fm, heading, sports=False):
    """Build the .afl-list from the page's `itemlist`, so a ranking page does not
    have to hand-author operator cards. `lbNotes` overrides the pill line per
    slug so each page frames the same operator for its own intent."""
    notes = fm.get("lbNotes", {})
    lis = []
    for i, slug in enumerate(fm["itemlist"], 1):
        op = OPS[slug]
        sub = notes.get(slug) or "%s &middot; %s &middot; %s" % (op["tag"], op["licence"], op["games"])
        terms = "18+ &middot; %s wagering &middot; T&amp;Cs apply" % op["wagering"]
        lis.append(lb_row(i, op["name"], sub, op["welcome"], terms,
                          round(op["rating"] * 2, 1),
                          aff(slug, "sports" if sports else "casino"),
                          op_logo(slug, sports),
                          op["tag"] if i <= 3 else "",
                          " is-top" if i == 1 else "",
                          bool(op.get("darkTile"))))
    notice = ('<div class="callout callout--warn" id="licensing-notice">'
              '<span class="t">One thing to know up front</span><p>%s</p></div>' % UK_NOTICE_BODY)
    return lb_shell(heading, featured_intro(fm.get("lbIntro", ""), fm.get("itemlist")), lis), notice


def transform(body, review_slug=None):
    """Map authored content markup onto the template's classes."""
    # answer box -> .snippet
    body = re.sub(r'<div class="answer">\s*<span class="label">(.*?)</span>\s*(.*?)</div>',
        lambda m: '<div class="snippet"><p><strong>%s:</strong> %s</p></div>'
                  % (m.group(1), re.sub(r'</?p>', '', m.group(2)).strip()),
        body, flags=re.S)
    # callouts -> .callout with modifier
    CAL = {"tip": " callout--good", "warn": " callout--warn", "note": "", "law": " callout--info"}
    body = re.sub(r'<div class="callout (tip|warn|note|law)"[^>]*>\s*<span class="t">(.*?)</span>\s*(.*?)</div>',
        lambda m: '<div class="callout%s"><span class="t">%s</span>%s</div>'
                  % (CAL[m.group(1)], m.group(2), m.group(3)),
        body, flags=re.S)
    # verification strip -> .upd. Keep the <span> items so the CSS can separate
    # them; only the decorative dot span is dropped.
    body = re.sub(r'<div class="updated">(.*?)</div>',
        lambda m: '<p class="upd">%s</p>' % m.group(1).replace('<span class="dot"></span>', ''),
        body, flags=re.S)
    # tables -> .t-scroll > table.datatable
    def tbl(m):
        inner = m.group(1).replace('<table class="data">', '<table class="datatable">')
        return '<div class="t-scroll">%s</div>' % inner
    body = re.sub(r'<div class="table-scroll">(.*?)</div>', tbl, body, flags=re.S)
    # TOC -> nav.toc. Match the whole block so the closing </div> is consumed too,
    # otherwise the stray tag closes .content and the rest of the page escapes it.
    body = re.sub(r'<div class="toc">\s*<h2>(.*?)</h2>\s*(.*?)\s*</div>',
                  lambda m: '<nav class="toc" aria-label="On this page"><strong>%s</strong>%s</nav>'
                            % (m.group(1), m.group(2)),
                  body, flags=re.S)
    # FAQ: <div class="faq"><details><summary>Q</summary><div class="a">A</div></details>
    body = body.replace('<div class="a">', '<div class="faq-a">')
    # operator reviews -> .opcard
    def rev(m):
        rid, inner = m.group(1), m.group(2)
        h = re.search(r'<div class="review-head">\s*<span class="op-logo"[^>]*>(.*?)</span>\s*'
                      r'<div><h3>(.*?)</h3><p class="rk">(.*?)</p></div>\s*'
                      r'<span class="score-pill">([\d.]+)</span>\s*</div>', inner, re.S)
        if not h:
            return '<div class="opcard" id="%s">%s</div>' % (rid, inner)
        rest = inner[h.end():]
        title, meta, score = h.group(2), h.group(3), h.group(4)
        plain = re.sub(r'<[^>]+>', '', title)
        badge = h.group(1)
        if rid in OPS:
            mark = ('<img class="oplogo%s" src="%s" alt="%s logo" loading="lazy" width="88" height="44">'
                    % (" oplogo--dark" if OPS[rid].get("darkTile") else "", op_logo(rid), plain))
        elif badge.startswith("photo:"):
            slug = badge.split(":", 1)[1]
            mark = ('<img class="author-av" src="/images/authors/%s.jpg" '
                    'srcset="/images/authors/%s.jpg 1x, /images/authors/%s@2x.jpg 2x" '
                    'alt="%s" width="64" height="64" loading="lazy">'
                    % (slug, slug, slug, plain))
        else:
            mark = '<span class="rev-logo">%s</span>' % badge
        pill = '' if score in ("0", "0.0") else '<div class="r">%s/5</div>' % score
        head = ('<div class="head">%s<div><div class="opname">%s</div>'
                '<span class="tag">%s</span></div>%s</div>'
                % (mark, title, meta, pill))
        return '<div class="opcard" id="%s">%s%s</div>' % (rid, head, rest)
    body = re.sub(r'<article class="review" id="([^"]+)">(.*?)</article>', rev, body, flags=re.S)
    # standalone review-head (used on the authors page and review pages)
    def head_std(m):
        ini, title, rk, score = m.group(1), m.group(2), m.group(3), m.group(4)
        if review_slug in OPS:
            mark = ('<img class="oplogo%s" src="%s" alt="%s logo" loading="lazy" width="88" height="44">'
                    % (" oplogo--dark" if OPS[review_slug].get("darkTile") else "",
                       op_logo(review_slug), OPS[review_slug]["name"]))
        elif ini.startswith("photo:"):
            # authored as <span class="op-logo">photo:slug</span> — a real headshot
            slug = ini.split(":", 1)[1]
            mark = ('<img class="author-av" src="/images/authors/%s.jpg" '
                    'srcset="/images/authors/%s.jpg 1x, /images/authors/%s@2x.jpg 2x" '
                    'alt="%s" width="64" height="64" loading="lazy">'
                    % (slug, slug, slug, slug.replace("-", " ").title()))
        else:
            mark = '<span class="rev-logo">%s</span>' % ini
        return ('<div class="opcard opcard--summary"><div class="head">%s'
                '<div><div class="opname">%s</div>'
                '<span class="tag">%s</span></div><div class="r">%s/5</div></div></div>'
                % (mark, title, rk, score))
    body = re.sub(r'<div class="review-head"[^>]*>\s*<span class="op-logo"[^>]*>(.*?)</span>\s*'
                  r'<div><h[23][^>]*>(.*?)</h[23]><p class="rk">(.*?)</p></div>\s*'
                  r'<span class="score-pill">([\d.]+)</span>\s*</div>', head_std, body, flags=re.S)
    body = re.sub(r'<article class="review">(.*?)</article>',
                  lambda m: '<div class="opcard">%s</div>' % m.group(1), body, flags=re.S)
    # pros / cons
    body = body.replace('<div class="pros-cons">', '<div class="proscons">')
    # link-card grids -> .cardgrid
    def cardgrid(m):
        cards = re.findall(r'<a class="card link-card" href="([^"]+)">\s*<h3>(.*?)</h3>\s*(?:<p>(.*?)</p>)?',
                           m.group(0), re.S)
        if not cards:
            return m.group(0)
        out = "".join('<a href="%s"><span class="t">%s</span>%s</a>'
                      % (h, t, '<span class="d">%s</span>' % d if d else "") for h, t, d in cards)
        return '<div class="cardgrid">%s</div>' % out
    body = re.sub(r'<div class="grid grid-\d">.*?</div>\s*(?=<h|<p|<div|<nav|$)', cardgrid, body, flags=re.S)
    # feature cards -> checklist
    def cards(m):
        items = re.findall(r'<div class="card"><div class="ico">(?:.*?)</div><h3>(.*?)</h3>(.*?)</div>',
                           m.group(0), re.S)
        if not items:
            return m.group(0)
        lis = "".join('<li><div><strong>%s</strong>%s</div></li>' % (t, b) for t, b in items)
        return '<ul class="checklist">%s</ul>' % lis
    body = re.sub(r'<div class="grid grid-2"[^>]*>(?:\s*<div class="card">.*?</div>\s*)+</div>',
                  cards, body, flags=re.S)
    # cta band
    body = re.sub(r'<div class="cta-band">\s*<div><h3>(.*?)</h3><p>(.*?)</p></div>\s*'
                  r'<a class="btn btn-gold" href="([^"]+)"([^>]*)>(.*?)</a>\s*</div>',
        lambda m: ('<div class="ctaband"><div><h3>%s</h3><p>%s</p></div>'
                   '<a class="cta-btn" href="%s"%s>%s</a></div>'
                   % (m.group(1), m.group(2), m.group(3), m.group(4), m.group(5))),
        body, flags=re.S)
    # remaining buttons
    body = re.sub(r'class="btn btn-ghost[^"]*"', 'class="cta-ghost"', body)
    body = re.sub(r'class="btn btn-[a-z]+(?: btn-[a-z]+)*"', 'class="cta-btn"', body)
    body = body.replace('<div class="spec-grid">', '<div class="specs">')
    body = body.replace('<p><strong>Verdict:</strong>', '<p><strong>Verdict:</strong>')
    body = body.replace('<p class="fine">', '<p style="font-size:13px;color:#71827E">')
    body = body.replace('<span class="fine">', '<span style="font-size:12.5px;color:#71827E">')
    body = body.replace('<p class="lede">', '<p>')
    return body



SEC_OPEN  = '<section class="section"><div class="wrap">'
SECA_OPEN = '<section class="section section-alt"><div class="wrap">'
SEC_CLOSE = '</div></section>'

def split_fragment(raw):
    """Pull the authored hero apart into the pieces the template hero needs, then
    flatten the section shells — the template renders one content column."""
    x = {}
    m = re.search(r'<p class="hero-lede">(.*?)</p>', raw, re.S)
    lede = m.group(1).strip() if m else ""
    m = re.search(r'<section class="hero">.*?<h1>(.*?)</h1>', raw, re.S)
    h1 = m.group(1).strip() if m else ""
    hero = re.search(r'<section class="hero">(.*?)</section>', raw, re.S)
    if hero:
        h = hero.group(1)
        stats = re.findall(r'<span class="k">(.*?)</span><span class="v">(.*?)</span>', h, re.S)
        if stats:
            x["stats"] = stats
        pills = re.findall(r'<span class="hero-pill">(.*?)</span>', h, re.S)
        if pills:
            x["pills"] = pills
        ctas = re.findall(r'<a class="btn btn-(?:gold|ghost)" href="([^"]+)">(.*?)</a>', h, re.S)
        if ctas:
            x["ctas"] = [(href, re.sub(r'\s*&(?:rarr|larr);\s*', '', t).strip()) for href, t in ctas]
        f = re.search(r'<p class="hero-fine">(.*?)</p>', h, re.S)
        if f:
            x["fine"] = f.group(1).strip()
    raw = re.sub(r'<section class="hero">.*?</section>\s*', '', raw, flags=re.S)
    raw = re.sub(r'<div class="trust-bar">.*?</ul></div></div>\s*', '', raw, flags=re.S)
    raw = raw.replace(SECA_OPEN, "\x00OPEN\x00").replace(SEC_OPEN, "\x00OPEN\x00")
    raw = raw.replace(SEC_CLOSE, "\x00END\x00")
    n_open, n_close = raw.count("\x00OPEN\x00"), raw.count("\x00END\x00")
    assert n_open == n_close, "section open/close mismatch: %d vs %d" % (n_open, n_close)
    raw = raw.replace("\x00OPEN\x00", "").replace("\x00END\x00", "")
    return h1, lede, raw, x


# ---------------------------------------------------------------- schema
def strip_tags(s):
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s))).strip()

def extract_faq(body):
    out = []
    # Template markup is <div class="faq"><details><summary>Q</summary><div class="faq-a">A</div></details>
    for m in re.finditer(r'<details[^>]*>\s*<summary>(.*?)</summary>\s*<div class="faq-a">(.*?)</div>\s*</details>',
                         body, re.S):
        q, a = strip_tags(m.group(1)), strip_tags(m.group(2))
        if q and a:
            out.append({"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}})
    return out

def schema_blocks(fm, body, url):
    a = AUTHORS[fm.get("author","team")]
    org_site = {"@context":"https://schema.org","@graph":[
      {"@type":"Organization","@id":DOMAIN+"/#organization","name":SITE,"url":DOMAIN,
       "logo":{"@type":"ImageObject","@id":DOMAIN+"/#logo","url":DOMAIN+"/images/logo.png",
               "contentUrl":DOMAIN+"/images/logo.png","width":400,"height":120,"caption":SITE},
       "image":{"@id":DOMAIN+"/#logo"},
       "description":"Independent UK casino and betting reviews. Every site is tested with real "
                     "GBP deposits and timed withdrawals under a published scoring methodology.",
       "areaServed":{"@type":"Country","name":"United Kingdom"},
       "foundingDate":"2026","email":"editor@chrischem.co.uk",
       "knowsAbout":["online casinos","UK gambling regulation","casino bonuses","sports betting",
                     "non-GamStop casinos","responsible gambling"],
       "publishingPrinciples":DOMAIN+"/how-we-review/",
       "actionableFeedbackPolicy":DOMAIN+"/contact/"},
      # No SearchAction: the site has no search endpoint, and declaring one that 404s
      # is a false capability claim in structured data.
      {"@type":"WebSite","@id":DOMAIN+"/#website","name":SITE,"url":DOMAIN,
       "publisher":{"@id":DOMAIN+"/#organization"},"inLanguage":"en-GB"}]}
    def person(p):
        return {"@type":"Person","@id":DOMAIN+"/#author-"+p["slug"],"name":p["name"],
                "url":DOMAIN+"/authors/"+("#"+p["slug"] if p.get("profiled") else ""),
                "jobTitle":html.unescape(p["role"]),
                "image":{"@type":"ImageObject","url":DOMAIN+p["photo"],"width":64,"height":64},
                "description":strip_tags(p["bio"]),
                "worksFor":{"@id":DOMAIN+"/#organization"},"knowsAbout":p["knows"]}
    checker = AUTHORS["donna"] if a["slug"] != AUTHORS["donna"]["slug"] else AUTHORS["charles"]
    g = [person(a), person(checker),
         {"@type":["WebPage","CollectionPage"] if fm.get("itemlist") else "WebPage",
          "@id":url+"#webpage","url":url,
          # name mirrors the visible H1, not the meta title — the title carries a
          # pipe-separated brand tail that is not the page's heading.
          "name":strip_tags(fm["h1"]),"headline":strip_tags(fm["h1"]),
          "alternateName":fm["title"],"description":fm["description"],
          "inLanguage":"en-GB","isPartOf":{"@id":DOMAIN+"/#website"},
          "primaryImageOfPage":{"@type":"ImageObject","@id":url+"#primaryimage",
                                "url":DOMAIN+"/images/og-chrischem.jpg","width":1200,"height":630},
          "author":{"@id":DOMAIN+"/#author-"+a["slug"]},"publisher":{"@id":DOMAIN+"/#organization"},
          "reviewedBy":{"@id":DOMAIN+"/#author-"+checker["slug"]},
          "datePublished":fm.get("published","2026-01-12"),"dateModified":fm.get("modified",UPDATED),
          "breadcrumb":{"@id":url+"#breadcrumb"}}]
    if fm.get("itemlist"):
        g[2]["mainEntity"] = {"@id": url + "#ranking"}
    items = [{"@type":"ListItem","position":1,"name":"Home","item":DOMAIN+"/"}]
    for i,(n,h) in enumerate(fm.get("crumbs",[]), start=2):
        items.append({"@type":"ListItem","position":i,"name":n,"item":DOMAIN+h})
    g.append({"@type":"BreadcrumbList","@id":url+"#breadcrumb","itemListElement":items})
    if fm.get("itemlist"):
        il_desc = ("Ranked by our published weighted scoring model. One position is a "
                   "featured partner placement held by commercial arrangement rather than "
                   "by score, and is labelled as such on the page."
                   if FEATURED in fm["itemlist"] else
                   "Ranked by our published weighted scoring model.")
        g.append({"@type":"ItemList","@id":url+"#ranking",
          "name":strip_tags(fm.get("itemlistName", fm["h1"])),
          "description":il_desc,
          "numberOfItems":len(fm["itemlist"]),
          "itemListOrder":"https://schema.org/ItemListOrderDescending",
          "itemListElement":[{"@type":"ListItem","position":i,
            "name":OPS[sl]["name"],
            "url":DOMAIN+"/casino-reviews/"+sl+"/",
            "item":{"@type":"Organization","name":OPS[sl]["name"],
                    "description":strip_tags(OPS[sl]["usp"]),
                    "image":DOMAIN+OPS[sl]["logo"],
                    "url":DOMAIN+"/casino-reviews/"+sl+"/"}}
            for i,sl in enumerate(fm["itemlist"],1)]})
    faqs = extract_faq(body)
    if faqs:
        g.append({"@type":"FAQPage","@id":url+"#faq","mainEntity":faqs})
    if fm.get("reviewOf"):
        op = OPS[fm["reviewOf"]]
        g.append({"@type":"Review","@id":url+"#review",
          "name":strip_tags(fm["h1"]),
          "itemReviewed":{"@type":"Organization","@id":url+"#operator","name":op["name"],
                          "description":strip_tags(op["usp"]),
                          "image":DOMAIN+op["logo"],
                          "url":DOMAIN+"/casino-reviews/"+op["slug"]+"/",
                          "foundingDate":str(op["launched"]),
                          "legalName":op["operator"]},
          "author":{"@id":DOMAIN+"/#author-"+a["slug"]},
          "publisher":{"@id":DOMAIN+"/#organization"},
          "datePublished":fm.get("published","2026-01-12"),
          "dateModified":fm.get("modified",UPDATED),
          "reviewRating":{"@type":"Rating","ratingValue":round(op["rating"]*2,1),
                          "bestRating":10,"worstRating":1}})
    for extra in fm.get("extraSchema", []):
        g.append(extra)
    page = {"@context":"https://schema.org","@graph":g}
    j = lambda dd: json.dumps(dd, ensure_ascii=False, separators=(",",":"))
    return ('<script type="application/ld+json">\n%s\n</script>'
            '<script type="application/ld+json">\n%s\n</script>' % (j(org_site), j(page)))


# ---------------------------------------------------------------- page
def review_notice(slug):
    op = OPS.get(slug)
    if not op:
        return ""
    return '''<div class="callout callout--warn" id="licensing-notice">
<span class="t">One thing to know up front</span><p>%s%s does not hold a UK Gambling Commission licence &mdash; it runs on %s. That is why it sits outside <a href="/non-gamstop-casinos/">GamStop</a> and outside UKGC affordability checks, and it is also why your recourse in a dispute runs through a foreign regulator rather than the Commission or IBAS. Playing here has never been an offence for a UK resident and winnings remain <a href="/gambling-winnings-tax-uk/">tax-free</a>. <strong>If you are registered with GamStop, do not open an account.</strong></p></div>''' % ("", op["name"], op["licence"])


def render(fm, lede, body, extra=None):
    url = DOMAIN + fm["url"]
    canonical = DOMAIN + "/" if CANONICAL_TO_HOME else url
    t, d = html.escape(fm["title"]), html.escape(fm["description"])
    robots = fm.get("robots", "index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1")
    body_cls = "home-instrument" if fm["url"] == "/" else "page-instrument"
    return '''<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="%s">
<link rel="alternate" hreflang="en-gb" href="%s">
<link rel="alternate" hreflang="x-default" href="%s">
<meta name="robots" content="%s">
<meta name="rating" content="adult">
<meta property="og:type" content="%s">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:url" content="%s">
<meta property="og:site_name" content="%s">
<meta property="og:locale" content="en_GB">
<meta property="og:image" content="%s/images/og-chrischem.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%s">
<meta name="twitter:description" content="%s">
<meta name="twitter:image" content="%s/images/og-chrischem.jpg">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-48x48.png" sizes="48x48" type="image/png">
<link rel="icon" href="/favicon-96x96.png" sizes="96x96" type="image/png">
<link rel="icon" href="/favicon-144x144.png" sizes="144x144" type="image/png">
<link rel="icon" href="/favicon-192x192.png" sizes="192x192" type="image/png">
<link rel="shortcut icon" href="/favicon.ico">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/home.css">
%s
</head>
<body class="%s">
%s
%s
<main><div class="wrap"><div class="content">
%s
%s
</div></div></main>
%s
</body>
</html>
''' % (t, d, canonical, url, url, robots, fm.get("ogType", "article"), t, d, url, SITE,
        DOMAIN, t, d, DOMAIN, schema_blocks(fm, body, url), body_cls,
        nav_html(), hero_html(fm, lede, extra), body, RG_PANEL, foot_html())


RG_PANEL = '''<div class="rg">
<h3>Responsible Gambling &mdash; Stay in Control</h3>
<p>Gambling is entertainment that costs money. It is not an income strategy, the house edge is permanent, and the only reliable way to finish ahead is to stop while you are. Set a deposit limit before you play, never chase a loss, and take regular breaks.</p>
<p><strong>Every operator on this site is licensed offshore and is not connected to GamStop.</strong> If you are registered with GamStop, or have ever self-excluded from any gambling operator, please do not use them &mdash; install <strong>BetBlocker</strong> (free) or <strong>Gamban</strong>, which do cover offshore sites, and switch on your bank&rsquo;s gambling block.</p>
<p>Free, confidential help in the UK, 24 hours a day:</p>
<ul>
<li><strong>National Gambling Helpline (GamCare)</strong> &mdash; call <a href="tel:08088020133">0808 8020 133</a> or chat at <a href="https://www.gamcare.org.uk/" rel="nofollow noopener" target="_blank">gamcare.org.uk</a></li>
<li><strong>GamStop</strong> &mdash; free national self-exclusion at <a href="https://www.gamstop.co.uk/" rel="nofollow noopener" target="_blank">gamstop.co.uk</a></li>
<li><strong>BeGambleAware</strong> &mdash; <a href="https://www.begambleaware.org/" rel="nofollow noopener" target="_blank">begambleaware.org</a></li>
<li><strong>Gordon Moody</strong> &mdash; residential treatment at <a href="https://gordonmoody.org.uk/" rel="nofollow noopener" target="_blank">gordonmoody.org.uk</a></li>
<li><strong>Samaritans</strong> &mdash; call <a href="tel:116123">116 123</a>, free, any time</li>
</ul>
<p style="margin-bottom:0"><span class="gc-18">18+</span> You must be at least 18 to gamble online in the United Kingdom. Read our full <a href="/responsible-gambling/">responsible gambling guide</a>.</p>
</div>'''


FM_RE = re.compile(r"^\s*<!--@(.*?)@-->\s*", re.S)

def main():
    pages = []
    for fn in sorted(os.listdir(SRC)):
        if not fn.endswith(".html"):
            continue
        raw = open(os.path.join(SRC, fn), encoding="utf-8").read()
        m = FM_RE.match(raw)
        if not m:
            raise SystemExit("%s: missing front matter" % fn)
        pages.append((fn, json.loads(m.group(1)), raw[m.end():]))

    for fn, fm, frag in pages:
        try:
            full_h1, lede, unwrapped, extra = split_fragment(frag)
        except AssertionError as e:
            raise SystemExit("%s: %s" % (fn, e))
        if full_h1:
            fm = dict(fm, h1=full_h1)
        base = re.split(r'\s*[:·|]\s*', fm["h1"])[0]
        heading = fm.get("lbHeading") or (('The %s' % base) if base.lower().startswith("best")
                                          else ('The Best %s' % base))
        sports = fm["url"] in ("/online-betting/", "/best-sports-betting-sites/",
                               "/non-gamstop-betting-sites-uk/",
                               "/football-betting-sites-not-on-gamstop/",
                               "/casino-reviews/tenobet/")
        lb_html = lb_notice = ""
        splice_at = None
        tl = re.search(r'<div class="toplist">(.*?</article>)\s*</div>', unwrapped, re.S)
        if tl:
            lb_html, lb_notice = build_leaderboard(tl.group(1), heading, sports,
                                                   featured_intro(fm.get("lbIntro", ""), fm.get("itemlist")))
            if lb_html:
                splice_at = tl.start()
                unwrapped = unwrapped[:tl.start()] + unwrapped[tl.end():]
        elif fm.get("itemlist"):
            lb_html, lb_notice = leaderboard_from_ops(fm, heading, sports)

        body = transform(unwrapped, fm.get("reviewOf"))
        if not lb_notice and fm.get("reviewOf"):
            lb_notice = review_notice(fm["reviewOf"])

        if lb_html:
            # The offer table leads every page it appears on, directly under the hero.
            body = lb_html + body
        body = body + lb_notice
        doc = resolve_tokens(render(fm, resolve_tokens(lede) or html.escape(fm["description"]),
                                    body, extra))
        out_dir = os.path.join(ROOT, fm["url"].strip("/"))
        os.makedirs(out_dir, exist_ok=True)
        n_faq = len(re.findall(r'<summary>', doc))
        n_schema = doc.count('"@type":"Question"')
        assert n_faq == n_schema, ("%s: %d FAQ items in markup but %d in schema"
                                   % (fm["url"], n_faq, n_schema))
        opens = len(re.findall(r'<div\b', doc)); closes = doc.count('</div>')
        assert opens == closes, ("%s: unbalanced <div> — %d open, %d close"
                                 % (fm["url"], opens, closes))
        # A schema image that 404s is an invalid rich result, and nothing else
        # in the build would notice a renamed or missing logo.
        for blob in re.findall(r'<script type="application/ld\+json">(.*?)</script>', doc, re.S):
            for rel in re.findall(r'"%s(/[^"]*\.(?:png|jpg|jpeg|svg))"' % re.escape(DOMAIN), blob):
                assert os.path.exists(os.path.join(ROOT, rel.lstrip("/"))), \
                    "%s: schema references missing image %s" % (fm["url"], rel)
        open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8").write(doc)

    urls = [(fm["url"], fm.get("modified",UPDATED), fm.get("changefreq","weekly"), fm.get("priority","0.7"))
            for _, fm, _ in pages if "noindex" not in fm.get("robots","")]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, lm, cf, pr in urls:
        sm.append("  <url>\n    <loc>%s%s</loc>\n    <lastmod>%s</lastmod>\n"
                  "    <changefreq>%s</changefreq>\n    <priority>%s</priority>\n  </url>" % (DOMAIN, u, lm, cf, pr))
    sm.append("</urlset>")

    # The sitemap must list exactly the pages that were written and are indexable.
    # A sitemap that names a missing page, or omits a live one, is a crawl-budget leak.
    listed = set(u for u, _, _, _ in urls)
    written = set(fm["url"] for _, fm, _ in pages)
    noindexed = set(fm["url"] for _, fm, _ in pages if "noindex" in fm.get("robots",""))
    assert listed == written - noindexed, (
        "sitemap/pages mismatch — only in sitemap: %s; missing from sitemap: %s"
        % (sorted(listed - written), sorted(written - noindexed - listed)))
    for u, lm, cf, pr in urls:
        assert re.match(r"^\d{4}-\d{2}-\d{2}$", lm), "%s: bad lastmod %r" % (u, lm)
        assert cf in ("always","hourly","daily","weekly","monthly","yearly","never"), \
            "%s: bad changefreq %r" % (u, cf)
        assert 0.0 <= float(pr) <= 1.0, "%s: bad priority %r" % (u, pr)

    open(os.path.join(ROOT,"sitemap.xml"),"w",encoding="utf-8").write("\n".join(sm)+"\n")

    open(os.path.join(ROOT,"robots.txt"),"w",encoding="utf-8").write("""# robots.txt for %s
User-agent: *
Allow: /
Disallow: /go/
Disallow: /*?

Sitemap: %s/sitemap.xml

# SEO crawlers — blocked to keep our link graph and content out of third-party indexes.
User-agent: AhrefsBot
Disallow: /

User-agent: SemrushBot
Disallow: /

User-agent: MJ12bot
Disallow: /

User-agent: DotBot
Disallow: /

User-agent: Rogerbot
Disallow: /

User-agent: serpstatbot
Disallow: /

User-agent: SistrixBot
Disallow: /
""" % (DOMAIN, DOMAIN))
    print("built %d pages · sitemap %d urls" % (len(pages), len(urls)))
    if MISSING:
        print("WARNING no affiliate link for: " + ", ".join(sorted(MISSING)))

if __name__ == "__main__":
    main()
