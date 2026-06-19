#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
import shutil
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "docs" / "policybase-source"
PUBLIC = ROOT / "public"
POLICY_PUBLIC = PUBLIC / "politik"
ASSET_DIR = PUBLIC / "assets" / "blog"

CATEGORY_LABELS = {
    "arbetsmarknad": ("Arbetsmarknad", "Labour market"),
    "bostad-bygg": ("Bostad & bygg", "Housing & construction"),
    "brott-ratt": ("Brott & rätt", "Crime & justice"),
    "demokrati": ("Demokrati", "Democracy"),
    "digitalisering": ("Digitalisering", "Digitalisation"),
    "energi-klimat": ("Energi & klimat", "Energy & climate"),
    "familj": ("Familj", "Family policy"),
    "forsvar": ("Försvar", "Defence"),
    "infrastruktur": ("Infrastruktur", "Infrastructure"),
    "migration-integration": ("Migration & integration", "Migration & integration"),
    "naringsliv": ("Näringsliv", "Business"),
    "pension": ("Pension", "Pensions"),
    "skatt": ("Skatt", "Tax"),
    "utbildning": ("Utbildning", "Education"),
    "vard-omsorg": ("Vård & omsorg", "Healthcare & care"),
}

NAV = '''<a href="/"><span data-lang="sv">Start</span><span data-lang="en">Start</span></a><a href="/constitutional-core/"><span data-lang="sv">Konstitutionell kärna</span><span data-lang="en">Constitutional core</span></a><a href="/politik/"><span data-lang="sv">Politik & policy</span><span data-lang="en">Politics & policy</span></a><a href="/research/"><span data-lang="sv">Forskning</span><span data-lang="en">Research</span></a><a href="/blog/"><span data-lang="sv">Blogg</span><span data-lang="en">Blog</span></a><a href="/about/"><span data-lang="sv">Om oss</span><span data-lang="en">About us</span></a><span class="od-lang-switch lang-switch"><button type="button" data-set-lang="en" onclick="odSetLang('en')">EN</button><button type="button" data-set-lang="sv" onclick="odSetLang('sv')">SV</button></span>'''

SHARED_HEAD = '''<meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <link rel="icon" href="/favicon.ico" sizes="any"/>
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png"/>
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png"/>
  <link rel="apple-touch-icon" href="/apple-touch-icon.png"/>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
  <link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet"/>
  <link rel="stylesheet" href="/assets/site-shared.css"/>'''

BASE_CSS = ''':root{--navy:#132845;--navy-dark:#0d1e35;--stone:#F7F4ED;--stone-mid:#EDE9E0;--dim:#D9D7D1;--forest:#31584D;--sky:#21B6F5;--leaf:#37C96B;--sun:#F2C318;--ember:#F39A1E;--text:#1a2e45;--text-mid:#4a5568;--text-light:#7a8a9a}*{box-sizing:border-box}body{margin:0;background:var(--stone);color:var(--text);font-family:Inter,system-ui,sans-serif;line-height:1.68}.hidden-lang{display:none!important}.container{max-width:1120px;margin:0 auto;padding:0 2rem}.hero{background:var(--navy);color:var(--stone);padding:5.5rem 0}.eyebrow{display:block;text-transform:uppercase;letter-spacing:.16em;font-size:.72rem;font-weight:800;color:rgba(247,244,237,.55);margin-bottom:1rem}h1,h2,h3{font-family:'Source Serif 4',Georgia,serif;line-height:1.1;letter-spacing:-.025em}h1{font-size:clamp(2.6rem,6vw,4.8rem);margin:0 0 1.2rem}.hero p{font-size:1.08rem;color:rgba(247,244,237,.76);max-width:820px}.section{padding:4rem 0}.notice{border:1px solid rgba(242,195,24,.55);background:#fff8d8;border-left:6px solid var(--sun);border-radius:10px;padding:1.25rem 1.4rem;margin:0 0 2rem}.notice strong{color:var(--navy)}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1rem}.card{display:block;background:#fff;border:1px solid var(--dim);border-radius:12px;padding:1.25rem;text-decoration:none;color:inherit}.card:hover h3{text-decoration:underline;text-underline-offset:.18em}.card h3{font-size:1.45rem;margin:.25rem 0 .5rem;color:var(--navy)}.tag{font-size:.72rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--forest)}.muted{color:var(--text-mid)}.policy-list{display:grid;gap:.65rem;margin-top:1rem}.policy-link{display:flex;justify-content:space-between;gap:1rem;align-items:center;background:#fff;border:1px solid var(--dim);border-radius:9px;padding:.85rem 1rem;text-decoration:none;color:inherit}.policy-link:hover strong{text-decoration:underline}.policy-id{font-size:.75rem;font-weight:800;color:var(--forest);white-space:nowrap}.article{background:#fff;border:1px solid var(--dim);border-radius:12px;padding:2rem}.article h2{font-size:2rem;margin:2rem 0 .7rem}.article h3{font-size:1.45rem;margin:1.4rem 0 .5rem}.article p,.article li{color:var(--text-mid)}.article table{width:100%;border-collapse:collapse;margin:1rem 0;display:block;overflow-x:auto}.article th,.article td{border:1px solid var(--dim);padding:.55rem;text-align:left;vertical-align:top}.article th{background:var(--stone-mid);color:var(--navy)}.article blockquote{border-left:4px solid var(--forest);margin:1.2rem 0;padding:.4rem 1rem;color:var(--text-mid);background:var(--stone)}.breadcrumbs{font-size:.84rem;margin-bottom:1rem;color:var(--text-mid)}.breadcrumbs a{color:var(--navy);font-weight:800;text-decoration:none}.post-image img{display:block;width:100%;height:auto;border-radius:10px;border:1px solid var(--dim);box-shadow:0 16px 50px rgba(19,40,69,.15);background:#fff}.post-content{font-family:'Source Serif 4',Georgia,serif;font-size:clamp(1.18rem,2vw,1.42rem);line-height:1.78;color:var(--text)}.post-content p{margin:0 0 1.45rem}.back-link{display:inline-block;margin-top:2rem;color:var(--navy);font-weight:800;text-decoration:none}.back-link:hover{text-decoration:underline}@media(max-width:760px){.container{padding:0 1.2rem}.hero{padding:4.5rem 0}.policy-link{display:block}.article{padding:1.2rem}}'''


def slugify(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s.lower()).strip("-")
    return s or "policy"


def title_from_md(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip().replace("Policyanalys: ", "")
    return path.stem


def metadata_from_md(path: Path) -> dict[str, str]:
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"- \*\*(.+?):\*\*\s*(.+)", line)
        if m:
            out[m.group(1)] = m.group(2)
    return out


def inline_md(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    return text


def md_to_html(md: str) -> str:
    lines = md.splitlines()
    out = []
    in_ul = False
    i = 0
    def close_ul():
        nonlocal in_ul
        if in_ul:
            out.append("</ul>")
            in_ul = False
    while i < len(lines):
        line = lines[i].rstrip()
        if not line:
            close_ul(); i += 1; continue
        if line.strip() == "---":
            close_ul(); out.append("<hr/>"); i += 1; continue
        if line.startswith("#### "):
            close_ul(); out.append(f"<h4>{inline_md(line[5:].strip())}</h4>"); i += 1; continue
        if line.startswith("### "):
            close_ul(); out.append(f"<h3>{inline_md(line[4:].strip())}</h3>"); i += 1; continue
        if line.startswith("## "):
            close_ul(); out.append(f"<h2>{inline_md(line[3:].strip())}</h2>"); i += 1; continue
        if line.startswith("# "):
            close_ul(); out.append(f"<h2>{inline_md(line[2:].strip())}</h2>"); i += 1; continue
        if line.startswith("> "):
            close_ul(); out.append(f"<blockquote>{inline_md(line[2:].strip())}</blockquote>"); i += 1; continue
        if line.startswith("|") and i + 1 < len(lines) and lines[i+1].lstrip().startswith("|") and "---" in lines[i+1]:
            close_ul()
            headers = [c.strip() for c in line.strip("|").split("|")]
            i += 2
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip("|").split("|")])
                i += 1
            out.append("<table><thead><tr>" + "".join(f"<th>{inline_md(h)}</th>" for h in headers) + "</tr></thead><tbody>" + "".join("<tr>" + "".join(f"<td>{inline_md(c)}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table>")
            continue
        if line.startswith("- "):
            if not in_ul:
                out.append("<ul>"); in_ul = True
            out.append(f"<li>{inline_md(line[2:].strip())}</li>"); i += 1; continue
        close_ul(); out.append(f"<p>{inline_md(line)}</p>"); i += 1
    close_ul()
    return "\n".join(out)


def page(title: str, description: str, body: str, lang="sv") -> str:
    return f'''<!doctype html>
<html lang="{lang}">
<head>
  <title>{html.escape(title)} — Oberoende Digital</title>
  <meta name="description" content="{html.escape(description)}"/>
  {SHARED_HEAD}
  <style>{BASE_CSS}</style>
</head>
<body>
<header class="od-site-header">
  <div class="od-ai-disclosure" role="note" aria-label="AI-generated content disclosure"><div class="od-ai-disclosure-inner"><span aria-hidden="true">&#9888;&#65039;</span><img class="od-ai-icon" src="https://oberoendedigital.se/assets/eu-ai-label/fully-ai-generated.svg" alt="EU fully AI-generated content label"/><span>This entire page was generated by artificial intelligence.</span></div></div>
  <div class="od-nav-inner"><a class="od-brand" href="/"><img src="/od.png" alt="OD"/><span>Oberoende Digital</span></a><button class="od-menu-toggle" type="button" aria-controls="od-site-menu" aria-expanded="false" aria-label="Open navigation menu"><span class="od-menu-toggle-lines" aria-hidden="true"></span></button><div class="od-site-menu" id="od-site-menu" role="navigation" aria-label="Primary navigation">{NAV}</div></div>
</header>
{body}
<footer class="od-site-footer"><div class="od-footer-top"><div class="od-footer-brand"><div class="od-footer-logo"><img src="/od.png" alt="OD"/><span class="od-footer-name">Oberoende Digital</span></div><p class="od-footer-tagline"><span data-lang="sv">Världens första säkra autonoma partilabb.<br/>AI hjälper. Människor legitimerar.</span><span data-lang="en">The world’s first Safe Autonomous Party Lab.<br/>AI assists. Humans legitimize.</span></p></div><div class="od-footer-col"><h4>Site</h4><ul><li><a href="/">Start</a></li><li><a href="/constitutional-core/">Constitutional core</a></li><li><a href="/politik/">Politics & policy</a></li><li><a href="/research/">Research agenda</a></li><li><a href="/blog/">Blog</a></li><li><a href="/about/">About us</a></li></ul></div><div class="od-footer-col"><h4>Legal</h4><ul><li><a href="/gdpr/">GDPR / privacy</a></li><li><a href="/impressum/">Impressum</a></li><li><a href="mailto:admin@oberoendedigital.se">admin@oberoendedigital.se</a></li></ul></div></div><div class="od-footer-bottom"><span>© 2026 Oberoende Digital · <a href="https://oberoendedigital.se">oberoendedigital.se</a></span><span>EU AI label icon source: European Commission.</span></div></footer>
<script>(function(){{function setLang(lang){{document.documentElement.lang=lang;document.querySelectorAll('[data-lang]').forEach(function(el){{el.classList.toggle('hidden-lang',el.getAttribute('data-lang')!==lang)}});document.querySelectorAll('.lang-switch button').forEach(function(b){{b.classList.toggle('active',b.dataset.setLang===lang)}});try{{localStorage.setItem('od_lang',lang)}}catch(e){{}}}}window.odSetLang=setLang;var saved;try{{saved=localStorage.getItem('od_lang')}}catch(e){{}}var guess=(navigator.language||'').toLowerCase().startsWith('sv')?'sv':'en';setLang(saved||guess)}})();</script><script src="/assets/site-shared.js"></script>
</body>
</html>
'''


def copy_source_clean():
    for p in SRC.rglob(".DS_Store"):
        p.unlink()


def generate_policy_pages():
    copy_source_clean()
    data = json.loads((SRC / "index.json").read_text(encoding="utf-8"))
    POLICY_PUBLIC.mkdir(parents=True, exist_ok=True)
    categories_html = []
    total_docs = 0
    for cat, info in sorted(data["categories"].items()):
        sv, en = CATEGORY_LABELS.get(cat, (cat.replace('-', ' ').title(), cat))
        cat_dir = POLICY_PUBLIC / cat
        cat_dir.mkdir(parents=True, exist_ok=True)
        policies = []
        for md_path in sorted((SRC / info["path"]).glob("*.md")):
            total_docs += 1
            title = title_from_md(md_path)
            meta = metadata_from_md(md_path)
            stem_slug = slugify(md_path.stem)
            out_dir = cat_dir / stem_slug
            out_dir.mkdir(parents=True, exist_ok=True)
            doc_body = f'''<main><section class="hero"><div class="container"><span class="eyebrow">{html.escape(sv)} · {html.escape(meta.get('Fråge-ID', md_path.stem))}</span><h1>{html.escape(title)}</h1><p>Policyanalys från OD:s policybas. Detta är ett underlag för granskning, argumentation och mänsklig dialog — inte en låst partilinje.</p></div></section><section class="section"><div class="container"><div class="notice"><strong>Under granskning:</strong> Denna position är preliminär och kan ändras när bättre argument, källor, kritik och mänsklig deliberation tillkommer.</div><div class="breadcrumbs"><a href="/politik/">Politik & policy</a> / <a href="/politik/{cat}/">{html.escape(sv)}</a></div><article class="article">{md_to_html(md_path.read_text(encoding='utf-8'))}</article><a class="back-link" href="/politik/{cat}/">← Till {html.escape(sv)}</a></div></section></main>'''
            (out_dir / "index.html").write_text(page(title, f"OD policyanalys: {title}", doc_body), encoding="utf-8")
            policies.append((title, meta.get("Fråge-ID", md_path.stem), f"/politik/{cat}/{stem_slug}/"))
        links = "\n".join(f'<a class="policy-link" href="{href}"><strong>{html.escape(title)}</strong><span class="policy-id">{html.escape(pid)}</span></a>' for title, pid, href in policies)
        cat_body = f'''<main><section class="hero"><div class="container"><span class="eyebrow">Policy Lab · {html.escape(sv)}</span><h1>{html.escape(sv)}</h1><p>{len(policies)} analyser i Green Book-format. Alla positioner är preliminära och ska prövas i dialog.</p></div></section><section class="section"><div class="container"><div class="notice"><strong>Under granskning:</strong> Dessa policyunderlag är startpunkter för samtal, inte slutpunkter. OD kommer att ändra dem när bättre argument, evidens och mänsklig deliberation kräver det.</div><div class="policy-list">{links}</div><a class="back-link" href="/politik/">← Politik & policy</a></div></section></main>'''
        (cat_dir / "index.html").write_text(page(f"{sv} — Politik & policy", f"OD policybas inom {sv}", cat_body), encoding="utf-8")
        categories_html.append(f'<a class="card" href="/politik/{cat}/"><span class="tag">{info["count"]} analyser</span><h3><span data-lang="sv">{html.escape(sv)}</span><span data-lang="en">{html.escape(en)}</span></h3><p class="muted"><span data-lang="sv">Öppna underlag för granskning och dialog.</span><span data-lang="en">Open policy material for review and dialogue.</span></p></a>')
    index_body = f'''<main><section class="hero"><div class="container"><span class="eyebrow">Oberoende Digital Policy Lab</span><h1><span data-lang="sv">Politik & policy</span><span data-lang="en">Politics & policy</span></h1><p><span data-lang="sv">{total_docs} preliminära policyanalyser från Quberon 1, publicerade för granskning, argumentation och dialog med människor.</span><span data-lang="en">{total_docs} preliminary policy analyses from Quberon 1, published for review, argumentation and human dialogue.</span></p></div></section><section class="section"><div class="container"><div class="notice"><strong><span data-lang="sv">Under granskning:</span><span data-lang="en">Under review:</span></strong> <span data-lang="sv">Det här är inte ett låst partiprogram. Policyerna är maskinellt strukturerade beslutsunderlag och kommer att ändras när bättre argument, källor, kritik och mänsklig deliberation tillkommer.</span><span data-lang="en">This is not a locked party platform. These policies are machine-structured decision materials and will change when better arguments, sources, criticism and human deliberation are added.</span></div><div class="grid">{''.join(categories_html)}</div><p class="muted" style="margin-top:2rem;"><span data-lang="sv">Källfilerna ligger även i GitHub under <code>docs/policybase-source/</code> för spårbarhet och vidare RAG-indexering.</span><span data-lang="en">The source files are also in GitHub under <code>docs/policybase-source/</code> for traceability and future RAG indexing.</span></p></div></section></main>'''
    (POLICY_PUBLIC / "index.html").write_text(page("Politik & policy", "OD:s preliminära policybas med evidensbaserade underlag", index_body), encoding="utf-8")


def update_existing_nav_and_footer():
    menu_re = re.compile(r'(<div class="od-site-menu" id="od-site-menu" role="navigation" aria-label="Primary navigation">)(.*?)(</div></div>)')
    for p in PUBLIC.rglob("*.html"):
        text = p.read_text(encoding="utf-8")
        new = menu_re.sub(r"\1" + NAV + r"\3", text, count=1)
        # Add Politics & policy to simple footer site lists when absent, and
        # normalize repeated links from earlier generator runs.
        footer_link = '<li><a href="/politik/">Politics & policy</a></li>'
        if footer_link not in new:
            new = new.replace(
                '<li><a href="/research/">Research agenda</a></li><li><a href="/blog/">Blog</a></li>',
                footer_link + '<li><a href="/research/">Research agenda</a></li><li><a href="/blog/">Blog</a></li>',
            )
        while footer_link + footer_link in new:
            new = new.replace(footer_link + footer_link, footer_link)
        if new != text:
            p.write_text(new, encoding="utf-8")


def add_homepage_policy_callout():
    p = PUBLIC / "index.html"
    text = p.read_text(encoding="utf-8")
    if 'href="/politik/" class="btn btn-outline-light"' not in text:
        text = text.replace('''<a href="/research/" class="btn btn-outline-light"><span data-lang="sv">Se forskningsagendan</span><span data-lang="en">See research agenda</span></a>''', '''<a href="/research/" class="btn btn-outline-light"><span data-lang="sv">Se forskningsagendan</span><span data-lang="en">See research agenda</span></a>
        <a href="/politik/" class="btn btn-outline-light"><span data-lang="sv">Utforska politik & policy</span><span data-lang="en">Explore politics & policy</span></a>''')
    if 'homepage-policy-review-notice' not in text:
        insert = '''\n<section class="section" id="homepage-policy-review-notice" style="background:var(--stone-mid)">\n  <div class="container">\n    <span class="eyebrow"><span data-lang="sv">Ny policybas · Under granskning</span><span data-lang="en">New policy base · Under review</span></span>\n    <h2 class="display"><span data-lang="sv">Politiken är publicerad för att prövas — inte för att stelna.</span><span data-lang="en">The policies are published to be tested — not to harden.</span></h2>\n    <p class="lead"><span data-lang="sv">OD:s första policybas innehåller preliminära analyser över svenska politikområden. De är maskinellt strukturerade beslutsunderlag som ska ändras när människor kommer med bättre argument, källor, kritik och erfarenheter.</span><span data-lang="en">OD’s first policy base contains preliminary analyses across Swedish policy areas. They are machine-structured decision materials meant to change when humans bring better arguments, sources, criticism and lived experience.</span></p>\n    <p class="lead" style="margin-top:1rem;"><a href="/politik/" class="btn btn-outline"><span data-lang="sv">Öppna Politik & policy</span><span data-lang="en">Open Politics & policy</span></a></p>\n  </div>\n</section>\n'''
        text = text.replace('<section id="focus" class="section">', insert + '\n<section id="focus" class="section">')
    p.write_text(text, encoding="utf-8")


def add_blog_post():
    img_src = Path('/Users/Apple/Downloads/IMG_4388.jpeg')
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    img_dest = ASSET_DIR / 'can-politics-be-machined-2026-06-16.jpg'
    shutil.copyfile(img_src, img_dest)
    post_dir = PUBLIC / 'blog' / '2026-06-16-can-politics-be-machined'
    post_dir.mkdir(parents=True, exist_ok=True)
    body = '''<main><section class="hero"><div class="container"><span class="eyebrow">Build log · 2026-06-16</span><h1>Can politics be machined?</h1><p>OD’s first policy base is now published for people to inspect, challenge and improve.</p></div></section><article class="section"><div class="container"><div class="post-meta">Published 2026-06-16 · Oberoende Digital</div><figure class="post-image"><img src="/assets/blog/can-politics-be-machined-2026-06-16.jpg?v=20260616" alt="Workshop machinery and laptops during Oberoende Digital policy-platform work."/><figcaption>A machine room for political prototypes: not a metaphor for replacing people, but for building tools humans can inspect.</figcaption></figure><div class="post-content"><p><strong>Can politics be machined?</strong></p><p>Not in the sense that a machine should rule. That is the wrong question, and a dangerous one.</p><p>The better question is whether parts of political work can be made more structured, inspectable and corrigible: gathering evidence, comparing options, naming trade-offs, preserving minority views, tracking uncertainty and showing where a proposed position came from.</p><p>Today we are publishing OD’s first policy base on the homepage under <a href="/politik/">Politics & policy</a>. It contains preliminary analyses across Swedish policy areas in a Green Book-inspired format. They are not a locked party programme. They are working material — deliberately exposed to argumentation, critique and human dialogue.</p><p>If a policy cannot survive questions from citizens, researchers, opponents and affected people, it should change. That is the point of publishing it now.</p><p>Machines can help us make political reasoning more legible. Humans must still decide what is legitimate.</p></div><a class="back-link" href="/blog/">← Back to Blog</a></div></article></main>'''
    (post_dir / 'index.html').write_text(page('Can politics be machined?', 'Oberoende Digital publishes its first policy base for exploration, critique and human dialogue.', body, lang='en'), encoding='utf-8')
    blog = PUBLIC / 'blog' / 'index.html'
    text = blog.read_text(encoding='utf-8')
    if '/blog/2026-06-16-can-politics-be-machined/' not in text:
        card = '''<a class="post-card" href="/blog/2026-06-16-can-politics-be-machined/"><div class="post-body"><span class="post-date">2026-06-16</span><h2>Can politics be machined?</h2><p>OD’s first policy base is now published for people to inspect, challenge and improve on the homepage.</p></div><img src="/assets/blog/can-politics-be-machined-2026-06-16.jpg?v=20260616" alt="Workshop machinery and laptops during Oberoende Digital policy-platform work."/></a>'''
        text = text.replace('<div class="post-list">', '<div class="post-list">' + card, 1)
        blog.write_text(text, encoding='utf-8')


def main():
    generate_policy_pages()
    add_blog_post()
    add_homepage_policy_callout()
    update_existing_nav_and_footer()
    print('Generated policy pages, blog post, homepage callout, and nav/footer updates.')

if __name__ == '__main__':
    main()
