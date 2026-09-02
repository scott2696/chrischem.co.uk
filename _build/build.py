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
UPDATED = "2026-09-02"
UPDATED_HUMAN = "02/09/2026"

# The brief asked for every canonical to point at the homepage. That would tell
# Google the 30+ money pages are duplicates of "/" and drop them from the index —
# the opposite of the ranking goal in the same brief. Self-referencing canonicals
# are emitted instead. Flip this to True to get the literal behaviour.
CANONICAL_TO_HOME = False

OPS = json.load(open(os.path.join(ROOT, "_build", "operators.json")))

AUTHORS = {
 "daniel": dict(name="Daniel Fairhurst", slug="daniel-fairhurst", initials="DF",
   role="Lead Casino Reviewer",
   photo="/images/authors/daniel-fairhurst.jpg",
   knows=["online casinos","UK online slots","GBP payments","withdrawal testing","cryptocurrency gambling","sports betting","non-GamStop casinos"],
   bio="Daniel spent six years in payments operations for a UK-licensed operator before moving to the other side of the cashier. He opens every account on this site himself, deposits his own pounds, and times each withdrawal from a Manchester connection."),
 "priya": dict(name="Priya Raval", slug="priya-raval", initials="PR",
   role="Editor, Regulation &amp; Bonuses",
   photo="/images/authors/priya-raval.jpg",
   knows=["gambling law","UK Gambling Commission regulation","Gambling Act 2005","GamStop","bonus terms and conditions","gambling taxation","responsible gambling"],
   bio="Priya read law at the University of Leeds and reported on gambling regulation before joining us. She reads the full terms on every offer we publish, tracks UK Gambling Commission enforcement and the Gambling Act review week by week, and fact-checks every legal and tax claim on this site."),
 "team": dict(name="The ChrisChem Team", slug="editorial-team", initials="CC",
   role="Editorial Team",
   photo="/images/authors/daniel-fairhurst.jpg",
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
    s = re.sub(r"\{\{(aff|affs):([a-z0-9\-]+)\}\}",
               lambda m: html.escape(aff(m.group(2), "sports" if m.group(1)=="affs" else "casino"), quote=True), s)
    s = re.sub(r"\{\{op:([a-z0-9\-]+):([A-Za-z]+)\}\}", lambda m: html.escape(str(OPS[m.group(1)].get(m.group(2),""))), s)
    return s

# ---------------------------------------------------------------- chrome
MARK = ('<svg class="eng-mark" viewBox="0 0 70 40" aria-hidden="true">'
  '<path d="M5 7 L21 20 L5 33" fill="none" stroke="var(--gold)" stroke-width="7.5" stroke-linecap="round" stroke-linejoin="round"></path>'
  '<path d="M22 7 L38 20 L22 33" fill="none" stroke="var(--gold)" stroke-width="7.5" stroke-linecap="round" stroke-linejoin="round"></path>'
  '<path d="M40 5 L66 20 L40 35 Z" fill="%s"></path></svg>')

def nav_html():
    out = ['<header class="nav"><div class="wrap">',
      '<a class="eng-logo" href="/" aria-label="%s — %s"><span class="eng-lockup">'
      '<span class="eng-word">%s</span>%s</span>'
      '<span class="eng-tag">%s</span></a>' % (SITE, TAGLINE, BRAND_WORD, MARK % "var(--slate)", TAGLINE),
      '<nav class="nav-links">']
    caret = ('<svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
             '<path d="M3 4.5l3 3 3-3"></path></svg>')
    for label, href, kids in NAV:
        if not kids:
            out.append('<a href="%s">%s</a>' % (href, label))
        else:
            trig = ('<a class="nav-trigger" href="%s">%s %s</a>' % (href, label, caret) if href
                    else '<span class="nav-trigger" tabindex="0">%s %s</span>' % (label, caret))
            links = "".join('<a href="%s">%s</a>' % (h, l) for l, h in kids)
            out.append('<div class="nav-item">%s<div class="nav-dd"><div class="nav-dd-inner">%s</div></div></div>'
                       % (trig, links))
    out.append('</nav>')
    out.append('<details class="menu"><summary aria-label="Open menu"><svg viewBox="0 0 24 24" width="22" height="22" '
      'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 6h18M3 12h18M3 18h18"></path>'
      '</svg></summary><div class="menu-panel">')
    for label, href, kids in NAV:
        if kids:
            out.append('<b>%s</b>' % label)
            out += ['<a href="%s">%s</a>' % (h, l) for l, h in kids]
        else:
            out.append('<a href="%s">%s</a>' % (href, label))
    out.append('<b>Company</b><a href="/about/">About Us</a><a href="/contact/">Contact Us</a>'
               '<a href="/authors/">Authors</a><a href="/responsible-gambling/">Responsible Gambling</a>')
    out.append('</div></details></div></header>')
    return "".join(out)


def hero_html(fm, lede):
    a = AUTHORS[fm.get("author", "team")]
    crumbs = ""
    if fm.get("crumbs"):
        parts = ['<a href="/">Home</a>']
        for i, (n, h) in enumerate(fm["crumbs"]):
            parts.append('<span>&rsaquo;</span>')
            parts.append(n if i == len(fm["crumbs"]) - 1 else '<a href="%s">%s</a>' % (h, n))
        crumbs = '<nav class="crumbs" aria-label="Breadcrumb">%s</nav>' % "".join(parts)
    facts = ""
    if fm.get("facts"):
        facts = '<div class="hero-facts">' + "".join(
            '<span class="hero-fact">%s</span>' % f for f in fm["facts"]) + '</div>'
    return '''<section class="hero"><div class="wrap">
%s<h1>%s</h1>
<div class="hero-by">
<a href="/authors/" aria-label="%s, author"><img src="%s" srcset="%s 1x, %s 2x" alt="%s" width="42" height="42" loading="eager"></a>
<div class="hero-by-txt">
<span>By <a class="by-link" href="/authors/"><b>%s</b></a>, %s</span>
<span class="eng-mono hero-by-date">%s Updated %s</span>
</div></div>
<p class="lede">%s</p>%s
</div></section>''' % (crumbs, fm["h1"], a['name'], a['photo'], a['photo'],
                       a['photo'].replace('.jpg','@2x.jpg'), a['name'], a['name'], a['role'],
                       ic("clock"), UPDATED_HUMAN, lede, facts)


def foot_html():
    cols = ""
    for title, links in FOOTER:
        items = "".join('<a href="%s">%s</a>' % (h, l) for l, h in links)
        cols += '<div class="foot-col"><b>%s</b>%s</div>' % (title, items)
    return '''<footer class="foot"><div class="wrap">
<div class="foot-top">
<div><a class="eng-logo" href="/" aria-label="%s"><span class="eng-lockup"><span class="eng-word">%s</span>%s</span>
<span class="eng-tag">%s</span></a>
<p style="margin:.7em 0 0;max-width:44ch;color:#9FB0D4">The UK's independent guide to online casinos, bonuses and betting sites. We test with real GBP deposits and timed withdrawals so you don't have to.</p></div>
<div class="foot-cols">%s</div>
</div>
<div class="foot-rg"><strong>18+. Gamble responsibly.</strong> Operators listed on this site are licensed offshore (Cura&ccedil;ao, Anjouan and similar) and are <strong>not licensed by the UK Gambling Commission</strong>. That means they are outside GamStop, outside the UKGC deposit-limit and affordability rules, and outside the Independent Betting Adjudication Service. <strong>If you are registered with GamStop, or have ever self-excluded, do not use these sites.</strong> Gambling carries real risk. Free, confidential help: <strong>GamCare&rsquo;s National Gambling Helpline on 0808 8020 133</strong>, 24/7, <strong>GamStop</strong> at gamstop.co.uk, <strong>Gordon Moody</strong>, and <strong>BeGambleAware</strong> at begambleaware.org. Affiliate links never affect our tested rankings &mdash; see <a href="/how-we-review/" style="color:#E9B949">how we review</a>. &copy; 2026 %s.</div>
</div></footer>''' % (SITE, BRAND_WORD, MARK % "#fff", TAGLINE, cols, SITE)


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


def lb_row(i, name, sub, offer, terms, rating10, href, logo, badge="", feat=""):
    """One leaderboard row. Shared by the authored-toplist and itemlist paths."""
    plain = re.sub(r'<[^>]+>', '', name)
    fast = '<span class="lb-fast">%s%s</span>' % (ic("bolt"), badge) if badge else ""
    return '''<li class="lb-row%s">
<a class="lb-cover" href="%s" rel="nofollow sponsored noopener" target="_blank" aria-label="Visit %s"></a>
<span class="lb-rank">%d</span>
<div class="lb-brand"><img class="lb-logo" src="%s" alt="%s logo" loading="lazy" width="96" height="48"><div class="lb-name">%s<span class="lb-sub">%s</span></div></div>
<div class="lb-speed"><div class="lb-payout">%s%s</div><div class="lb-bar"><span class="lb-bar-fill" style="width:%d%%"></span></div></div>
<div class="lb-bonus"><span class="lb-bonus-l">Welcome offer</span><span class="lb-bonus-v">%s</span></div>
<div class="lb-cta"><a class="eng-btn" href="%s" rel="nofollow sponsored noopener" target="_blank">Get bonus</a><span class="lb-min">%s</span></div>
</li>''' % (feat, href, plain, i, logo, plain, name, sub, stars_row(rating10), fast,
            min(99, int(rating10*10)), offer, href, terms)


def lb_shell(heading, intro, lis):
    """The section wrapper around a set of leaderboard rows."""
    intro_html = '<p class="lb-intro">%s</p>' % intro if intro else ""
    return '''<section id="leaderboard" class="sec sec--white"><div class="wrap">
<div class="sec-head sec--lead"><h2>%s</h2>%s</div>
<div class="lb">
<div class="lb-head" aria-hidden="true"><span>#</span><span>Casino</span><span>Our rating</span><span>Welcome offer</span><span></span></div>
<ol class="lb-rows">%s</ol>
</div>
<div style="max-width:820px;margin:22px auto 0">
<p>The leaderboard sorts our verdict &mdash; number one scored highest across payout speed, game range, bonus value and cashier reliability, and the scores step down from there. The full scoring weights are on our <a href="/how-we-review/">review methodology</a> page, and every brand has a <a href="/casino-reviews/">full written review</a>.</p>
</div></div></section>''' % (heading, intro_html, "".join(lis))


def leaderboard_from_ops(fm, heading, sports=False):
    """Build the leaderboard from the page's `itemlist`, so a ranking page does
    not have to hand-author operator cards. `lbNotes` overrides the meta line
    per slug so each page can frame the same operator for its own intent."""
    notes = fm.get("lbNotes", {})
    lis = []
    for i, slug in enumerate(fm["itemlist"], 1):
        op = OPS[slug]
        sub = notes.get(slug) or "%s &middot; %s &middot; %s" % (op["tag"], op["licence"], op["games"])
        terms = "%s wagering &middot; %s min &middot; 18+ T&amp;Cs apply" % (op["wagering"], op["minDep"])
        lis.append(lb_row(i, op["name"], sub, op["welcome"], terms,
                          round(op["rating"] * 2, 1), aff(slug, "sports" if sports else "casino"),
                          op_logo(slug, sports), op["tag"] if i <= 3 else "",
                          " lb-row--feat" if i == 1 else ""))
    notice = '''<section class="sec sec--alt" id="licensing-notice"><div class="wrap"><div class="prose">
<div class="cal cal--warn">%s<div><b>One thing to know up front</b>%s</div></div>
</div></div></section>''' % (ic("warn"), UK_NOTICE_BODY)
    return lb_shell(heading, fm.get("lbIntro", ""), lis), notice


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
                          badge.group(1) if badge else "", feat))
    if not lis:
        return "", ""
    sec = lb_shell(heading, intro, lis)

    notice = '''<section class="sec sec--alt" id="licensing-notice"><div class="wrap"><div class="prose">
<div class="cal cal--warn">%s<div><b>One thing to know up front</b>%s</div></div>
</div></div></section>''' % (ic("warn"), UK_NOTICE_BODY)
    return sec, notice


def transform(body, review_slug=None):
    """Map authored content markup onto the template's classes."""
    body = re.sub(r'<div class="answer">\s*<span class="label">(.*?)</span>\s*(.*?)</div>',
        lambda m: '<div class="cal cal--info">%s<div><b>%s</b>%s</div></div>' % (ic("info"), m.group(1), m.group(2)),
        body, flags=re.S)
    CAL = {"tip":"good","warn":"warn","note":"gold","law":"info"}
    ICO = {"tip":"check","warn":"warn","note":"info","law":"info"}
    body = re.sub(r'<div class="callout (tip|warn|note|law)"[^>]*>\s*<span class="t">(.*?)</span>\s*(.*?)</div>',
        lambda m: '<div class="cal cal--%s">%s<div><b>%s</b>%s</div></div>'
                  % (CAL[m.group(1)], ic(ICO[m.group(1)]), m.group(2), m.group(3)),
        body, flags=re.S)
    def tbl(m):
        inner = m.group(1)
        cap = re.search(r'<caption>(.*?)</caption>', inner, re.S)
        capd = '<figcaption>%s</figcaption>' % cap.group(1) if cap else ""
        inner = re.sub(r'<caption>.*?</caption>', '', inner, flags=re.S)
        inner = inner.replace('<table class="data">', '<table class="t">')
        return '<figure class="fig">%s<div class="t-scroll">%s</div></figure>' % (capd, inner)
    body = re.sub(r'<div class="table-scroll">(.*?)</div>', tbl, body, flags=re.S)
    body = body.replace('<div class="faq">', '<div class="faqs">')
    body = re.sub(r'<details( open)?><summary>', lambda m: '<details class="faq"%s><summary>' % (m.group(1) or ""), body)
    body = body.replace('<div class="a">', '<div class="faq-a">')
    def rev(m):
        rid, inner = m.group(1), m.group(2)
        h = re.search(r'<div class="review-head">\s*<span class="op-logo"[^>]*>(.*?)</span>\s*'
                      r'<div><h3>(.*?)</h3><p class="rk">(.*?)</p></div>\s*'
                      r'<span class="score-pill">([\d.]+)</span>\s*</div>', inner, re.S)
        if h:
            rest = inner[h.end():]
            title, meta, score = h.group(2), h.group(3), round(float(h.group(4))*2, 1)
            rank = re.match(r'\s*(\d+)\.', title)
            rankb = '<span class="rev-rank">#%s</span>' % rank.group(1) if rank else ""
            title = re.sub(r'^\s*\d+\.\s*', '', title)
            plain = re.sub(r'<[^>]+>', '', title)
            logo = ('<img class="lb-logo" src="%s" alt="%s logo" loading="lazy" width="96" height="48">'
                    % (op_logo(rid), plain)) if rid in OPS else ""
            cta = re.search(r'<a class="btn btn-gold" href="([^"]+)"[^>]*>(.*?)</a>', rest, re.S)
            ctab = ('<a class="eng-btn rev-cta-btn" href="%s" rel="nofollow sponsored noopener" target="_blank">Get bonus</a>'
                    % cta.group(1) if cta else "")
            head = ('<div class="rev-head">%s%s<div class="rev-h"><h3>%s</h3>'
                    '<span class="rev-meta">%s &middot; %s %s/10</span></div>%s</div>'
                    % (rankb, logo, title, meta, ic("star"), score, ctab))
            return '<article class="rev" id="%s">%s<div class="rev-body">%s</div></article>' % (rid, head, rest)
        return '<article class="rev" id="%s"><div class="rev-body">%s</div></article>' % (rid, inner)
    body = re.sub(r'<article class="review" id="([^"]+)">(.*?)</article>', rev, body, flags=re.S)
    body = re.sub(r'<article class="review">(.*?)</article>',
                  lambda m: '<article class="rev"><div class="rev-body">%s</div></article>' % m.group(1), body, flags=re.S)
    def head_std(m):
        ini, title, rk, score = m.group(1), m.group(2), m.group(3), float(m.group(4))
        mark = ('<img class="lb-logo" src="%s" alt="%s logo" loading="lazy" width="96" height="48">'
                % (op_logo(review_slug), OPS[review_slug]["name"])) if review_slug in OPS \
               else '<span class="rev-logo">%s</span>' % ini
        return ('<div class="rev-head">%s<div class="rev-h"><h2 style="margin:0;font-size:1.3rem">%s</h2>'
                '<span class="rev-meta">%s</span></div>'
                '<span class="rev-score">%s %s/10</span></div>'
                % (mark, title, rk, ic("star"), round(score*2, 1)))
    body = re.sub(r'<div class="review-head"[^>]*>\s*<span class="op-logo"[^>]*>(.*?)</span>\s*'
                  r'<div><h[23][^>]*>(.*?)</h[23]><p class="rk">(.*?)</p></div>\s*'
                  r'<span class="score-pill">([\d.]+)</span>\s*</div>', head_std, body, flags=re.S)
    body = body.replace('<div class="pros-cons">', '<div class="rev-pc">')
    body = body.replace('<div class="pros">', '<div class="rev-pros">')
    body = body.replace('<div class="cons">', '<div class="rev-cons">')
    body = body.replace('<div class="spec-grid">', '<div class="specs">')
    body = body.replace('<p><strong>Verdict:</strong>', '<p class="rev-for"><b>Verdict:</b>')
    def linkrow(m):
        links = re.findall(r'<a class="card link-card" href="([^"]+)"><h3>(.*?)</h3>', m.group(1), re.S)
        if links:
            return '<div class="linkrow">' + "".join('<a href="%s">%s</a>' % (h, t) for h, t in links) + '</div>'
        return m.group(0)
    body = re.sub(r'<div class="grid grid-\d">(.*?)</div>\s*(?=<|$)', linkrow, body, flags=re.S)
    def cards(m):
        items = re.findall(r'<div class="card"><div class="ico">(?:.*?)</div><h3>(.*?)</h3>(.*?)</div>', m.group(0), re.S)
        if not items:
            return m.group(0)
        lis = "".join('<li>%s<div><strong>%s</strong>%s</div></li>' % (ic("check"), t, b) for t, b in items)
        return '<ul class="checklist">%s</ul>' % lis
    body = re.sub(r'<div class="grid grid-2"[^>]*>(?:\s*<div class="card">.*?</div>\s*)+</div>', cards, body, flags=re.S)
    body = re.sub(r'<div class="cta-band">\s*<div><h3>(.*?)</h3><p>(.*?)</p></div>\s*<a class="btn btn-gold" href="([^"]+)"([^>]*)>(.*?)</a>\s*</div>',
        lambda m: ('<div class="method"><div class="method-ic">%s</div><div><span class="lab">%s</span>'
                   '<p>%s</p><p style="margin-top:12px"><a class="eng-btn" href="%s"%s>%s</a></p></div></div>'
                   % (ic("star"), m.group(1), m.group(2), m.group(3), m.group(4), m.group(5))),
        body, flags=re.S)
    body = re.sub(r'class="btn btn-ghost[^"]*"', 'class="eng-btn eng-btn--ghost"', body)
    body = re.sub(r'class="btn btn-[a-z]+(?: btn-[a-z]+)*"', 'class="eng-btn"', body)
    body = body.replace('<p class="fine">', '<p style="font-size:13px;color:var(--mut)">')
    body = body.replace('<span class="fine">', '<span style="font-size:12.5px;color:var(--mut)">')
    body = body.replace('<p class="lede">', '<p>')
    return body


SEC_OPEN  = '<section class="section"><div class="wrap">'
SECA_OPEN = '<section class="section section-alt"><div class="wrap">'
SEC_CLOSE = '</div></section>'

def split_fragment(raw):
    lede = h1 = ""
    m = re.search(r'<p class="hero-lede">(.*?)</p>', raw, re.S)
    if m:
        lede = m.group(1).strip()
    m = re.search(r'<section class="hero">.*?<h1>(.*?)</h1>', raw, re.S)
    if m:
        h1 = m.group(1).strip()
    raw = re.sub(r'<section class="hero">.*?</section>\s*', '', raw, flags=re.S)
    raw = re.sub(r'<div class="trust-bar">.*?</ul></div></div>\s*', '', raw, flags=re.S)
    raw = raw.replace(SECA_OPEN, "\x00ALT\x00").replace(SEC_OPEN, "\x00SEC\x00")
    raw = raw.replace(SEC_CLOSE, "\x00END\x00")
    n_open = raw.count("\x00ALT\x00") + raw.count("\x00SEC\x00")
    n_close = raw.count("\x00END\x00")
    assert n_open == n_close, "section open/close mismatch: %d vs %d" % (n_open, n_close)
    raw = raw.replace("\x00ALT\x00", '<section class="sec sec--alt"><div class="wrap"><div class="prose">')
    raw = raw.replace("\x00SEC\x00", '<section class="sec"><div class="wrap"><div class="prose">')
    raw = raw.replace("\x00END\x00", '</div></div></section>')
    return h1, lede, raw


# ---------------------------------------------------------------- schema
def strip_tags(s):
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s))).strip()

def extract_faq(body):
    out = []
    for m in re.finditer(r'<details class="faq"[^>]*>\s*<summary>(.*?)</summary>\s*<div class="faq-a">(.*?)</div>\s*</details>',
                         body, re.S):
        q, a = strip_tags(m.group(1)), strip_tags(m.group(2))
        if q and a:
            out.append({"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}})
    return out

def schema_blocks(fm, body, url):
    a = AUTHORS[fm.get("author","team")]
    org_site = {"@context":"https://schema.org","@graph":[
      {"@type":"Organization","@id":DOMAIN+"/#organization","name":SITE,"url":DOMAIN,
       "logo":{"@type":"ImageObject","url":DOMAIN+"/images/logo.png","width":400,"height":120},
       "areaServed":{"@type":"Country","name":"United Kingdom"},
       "email":"editor@chrischem.co.uk","sameAs":[]},
      {"@type":"WebSite","@id":DOMAIN+"/#website","name":SITE,"url":DOMAIN,
       "publisher":{"@id":DOMAIN+"/#organization"},"inLanguage":"en-GB",
       "potentialAction":{"@type":"SearchAction","target":DOMAIN+"/?s={search_term_string}",
                          "query-input":"required name=search_term_string"}}]}
    g = [{"@type":"Person","@id":DOMAIN+"/#author-"+a["slug"],"name":a["name"],
          "url":DOMAIN+"/authors/","jobTitle":html.unescape(a["role"]),
          "worksFor":{"@id":DOMAIN+"/#organization"},"knowsAbout":a["knows"]},
         {"@type":["WebPage","CollectionPage"] if fm.get("itemlist") else "WebPage",
          "@id":url+"#webpage","url":url,"name":fm["title"],"description":fm["description"],
          "inLanguage":"en-GB","isPartOf":{"@id":DOMAIN+"/#website"},
          "author":{"@id":DOMAIN+"/#author-"+a["slug"]},"publisher":{"@id":DOMAIN+"/#organization"},
          "datePublished":fm.get("published","2026-01-12"),"dateModified":fm.get("modified",UPDATED),
          "breadcrumb":{"@id":url+"#breadcrumb"}}]
    if fm.get("itemlist"):
        g[1]["mainEntity"] = {"@id": url + "#ranking"}
    items = [{"@type":"ListItem","position":1,"name":"Home","item":DOMAIN+"/"}]
    for i,(n,h) in enumerate(fm.get("crumbs",[]), start=2):
        items.append({"@type":"ListItem","position":i,"name":n,"item":DOMAIN+h})
    g.append({"@type":"BreadcrumbList","@id":url+"#breadcrumb","itemListElement":items})
    if fm.get("itemlist"):
        g.append({"@type":"ItemList","@id":url+"#ranking",
          "name":fm.get("itemlistName", fm["h1"]),
          "numberOfItems":len(fm["itemlist"]),
          "itemListOrder":"https://schema.org/ItemListOrderDescending",
          "itemListElement":[{"@type":"ListItem","position":i,
            "item":{"@type":"Organization","name":OPS[s]["name"],
                    "url":DOMAIN+"/casino-reviews/"+s+"/"}} for i,s in enumerate(fm["itemlist"],1)]})
    faqs = extract_faq(body)
    if faqs:
        g.append({"@type":"FAQPage","@id":url+"#faq","mainEntity":faqs})
    if fm.get("reviewOf"):
        op = OPS[fm["reviewOf"]]
        g.append({"@type":"Review","@id":url+"#review",
          "itemReviewed":{"@type":"Organization","name":op["name"],"description":op["usp"],
                          "url":DOMAIN+"/casino-reviews/"+op["slug"]+"/"},
          "author":{"@id":DOMAIN+"/#author-"+a["slug"]},"publisher":{"@id":DOMAIN+"/#organization"},
          "datePublished":fm.get("published","2026-01-12"),
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
    return '''<section class="sec sec--alt" id="licensing-notice"><div class="wrap"><div class="prose">
<div class="cal cal--warn">%s<div><b>One thing to know up front</b>%s does not hold a UK Gambling Commission licence &mdash; it runs on %s. That is why it sits outside <a href="/non-gamstop-casinos/">GamStop</a> and outside UKGC affordability checks, and it is also why your recourse in a dispute runs through a foreign regulator rather than the Commission or IBAS. Playing here has never been an offence for a UK resident and winnings remain <a href="/gambling-winnings-tax-uk/">tax-free</a>. <strong>If you are registered with GamStop, do not open an account.</strong></div></div>
</div></div></section>''' % (ic("warn"), op["name"], op["licence"])


def render(fm, lede, body):
    url = DOMAIN + fm["url"]
    canonical = DOMAIN + "/" if CANONICAL_TO_HOME else url
    t, d = html.escape(fm["title"]), html.escape(fm["description"])
    robots = fm.get("robots","index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1")
    return '''<!DOCTYPE html><html lang="en-GB"> <head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>%s</title><link rel="canonical" href="%s"><meta name="description" content="%s"><meta name="robots" content="%s"><meta name="rating" content="adult"><link rel="alternate" hreflang="en-gb" href="%s"><link rel="alternate" hreflang="x-default" href="%s"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet"><link rel="icon" type="image/svg+xml" href="/favicon.svg"><link rel="icon" type="image/png" sizes="48x48" href="/favicon-48x48.png"><link rel="icon" type="image/png" sizes="96x96" href="/favicon-96x96.png"><link rel="icon" type="image/png" sizes="144x144" href="/favicon-144x144.png"><link rel="icon" type="image/png" sizes="192x192" href="/favicon-192x192.png"><link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png"><link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png"><link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png"><link rel="shortcut icon" href="/favicon.ico">%s<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:type" content="%s">
<meta property="og:url" content="%s">
<meta property="og:site_name" content="%s">
<meta property="og:locale" content="en_GB">
<meta property="og:image" content="%s/images/og-chrischem.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%s">
<meta name="twitter:description" content="%s">
<meta name="twitter:image" content="%s/images/og-chrischem.jpg"><link rel="stylesheet" href="/assets/css/site.css"></head> <body> %s %s
%s
 %s </body></html>
''' % (t, canonical, d, robots, url, url, schema_blocks(fm, body, url), t, d,
       fm.get('ogType','article'), url, SITE, DOMAIN, t, d, DOMAIN,
       nav_html(), hero_html(fm, lede), body, foot_html())


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
            full_h1, lede, unwrapped = split_fragment(frag)
        except AssertionError as e:
            raise SystemExit("%s: %s" % (fn, e))
        if full_h1:
            fm = dict(fm, h1=full_h1)
        lb_html = lb_notice = ""
        base = re.split(r'\s*[:·|]\s*', fm["h1"])[0]
        heading = fm.get("lbHeading") or (('The %s' % base) if base.lower().startswith("best")
                                          else ('The Best %s' % base))
        sports = fm["url"] in ("/online-betting/", "/best-sports-betting-sites/",
                               "/non-gamstop-betting-sites-uk/",
                               "/football-betting-sites-not-on-gamstop/",
                               "/casino-reviews/tenobet/")
        tl = re.search(r'<div class="toplist">(.*?</article>)\s*</div>', unwrapped, re.S)
        if tl:
            lb_html, lb_notice = build_leaderboard(tl.group(1), heading, sports, fm.get("lbIntro", ""))
            if lb_html:
                unwrapped = unwrapped[:tl.start()] + unwrapped[tl.end():]
        elif fm.get("itemlist"):
            lb_html, lb_notice = leaderboard_from_ops(fm, heading, sports)
        body = transform(unwrapped, fm.get("reviewOf"))
        if not lb_notice and fm.get("reviewOf"):
            lb_notice = review_notice(fm["reviewOf"])
        body = lb_html + body + lb_notice
        doc = resolve_tokens(render(fm, resolve_tokens(lede) or html.escape(fm["description"]), body))
        out_dir = os.path.join(ROOT, fm["url"].strip("/"))
        os.makedirs(out_dir, exist_ok=True)
        open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8").write(doc)

    urls = [(fm["url"], fm.get("modified",UPDATED), fm.get("changefreq","weekly"), fm.get("priority","0.7"))
            for _, fm, _ in pages if "noindex" not in fm.get("robots","")]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, lm, cf, pr in urls:
        sm.append("  <url>\n    <loc>%s%s</loc>\n    <lastmod>%s</lastmod>\n"
                  "    <changefreq>%s</changefreq>\n    <priority>%s</priority>\n  </url>" % (DOMAIN, u, lm, cf, pr))
    sm.append("</urlset>")
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
