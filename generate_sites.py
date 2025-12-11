import csv
import re
from pathlib import Path
from urllib.parse import urlparse

DATA_FILE = Path('從-google.com.tw-抓取細節--6--2025-12-11.csv')
DOCS_DIR = Path('docs')
BUSINESS_DIR = DOCS_DIR / 'businesses'


def slugify(name: str) -> str:
    slug = re.sub(r"[^\w]+", "-", name.lower())
    slug = re.sub(r"-+", "-", slug).strip('-')
    # 避免檔名過長造成存檔失敗
    slug = slug[:60]
    return slug or 'business'


def load_rows():
    with DATA_FILE.open(encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield {k: v.strip() for k, v in row.items()}


def ensure_dirs():
    DOCS_DIR.mkdir(exist_ok=True)
    BUSINESS_DIR.mkdir(parents=True, exist_ok=True)


def build_contact_list(row):
    contacts = []
    if row.get('Io6YTe (4)'):
        contacts.append(row['Io6YTe (4)'])
    if row.get('Io6YTe (2)') and row['Io6YTe (2)'] not in contacts:
        contacts.append(row['Io6YTe (2)'])
    # CsEnBe href tends to be tel: URLs
    tel = row.get('CsEnBe href', '')
    if tel and tel.startswith('tel:'):
        number = tel.replace('tel:', '')
        if number not in contacts:
            contacts.append(number)
    return contacts


def render_tags(label, values):
    if not values:
        return ''
    items = ''.join(f'<li>{value}</li>' for value in values)
    return f"<div class='info-block'><h3>{label}</h3><ul>{items}</ul></div>"


def render_link(label, url):
    if not url:
        return ''
    return f"<div class='info-block'><h3>{label}</h3><p><a href='{url}' target='_blank' rel='noopener'>{url}</a></p></div>"


def render_business_page(row, slug):
    name = row.get('DUwDvf', '未命名水電行')
    image = row.get('aoRNLd src', '')
    map_url = row.get('hfpxzc href', '')
    rating = row.get('F7nice', '')
    category = row.get('DkEaL', '')
    address = row.get('Io6YTe', '')
    status = row.get('ZDu9vd', '')
    extras = [row.get('Io6YTe (2)', ''), row.get('Io6YTe (3)', '')]
    extras = [item for item in extras if item]
    website = row.get('CsEnBe href (2)', '')
    contacts = build_contact_list(row)

    parts = [
        "<html lang='zh-Hant'>",
        '<head>',
        "<meta charset='utf-8'>",
        f"<title>{name} | 高雄水電行</title>",
        "<link rel='stylesheet' href='../style.css'>",
        '</head>',
        '<body>',
        "<div class='page'>",
        "<header class='hero'>",
        f"<div class='hero-text'><p class='eyebrow'>水電行專頁</p><h1>{name}</h1>",
    ]

    subhead = []
    if category:
        subhead.append(category)
    if rating:
        subhead.append(f"評分 {rating} ★")
    if status:
        subhead.append(status)
    if subhead:
        parts.append(f"<p class='subhead'>{' · '.join(subhead)}</p>")
    parts.append("</div>")
    if image:
        parts.append(f"<div class='hero-image'><img src='{image}' alt='{name}' loading='lazy'></div>")
    parts.append("</header>")

    parts.append("<main class='content'>")
    if address:
        parts.append(f"<div class='info-block'><h3>地址</h3><p>{address}</p></div>")

    if contacts:
        parts.append(render_tags('聯絡方式', contacts))

    if extras:
        parts.append(render_tags('其他資訊', extras))

    if website:
        parts.append(render_link('官方網站 / 連結', website))

    parts.append(render_link('地圖', map_url))
    parts.append("</main>")

    parts.append("<footer class='page-footer'>")
    parts.append("<a class='button' href='../index.html'>返回所有水電行</a>")
    if map_url:
        parts.append(f"<a class='button primary' href='{map_url}' target='_blank' rel='noopener'>在地圖上開啟</a>")
    parts.append("</footer>")

    parts.append("</div>")
    parts.append("</body></html>")

    (BUSINESS_DIR / f"{slug}.html").write_text('\n'.join(parts), encoding='utf-8')


def render_index(rows_with_slugs):
    cards = []
    for row, slug in rows_with_slugs:
        name = row.get('DUwDvf', '未命名水電行')
        image = row.get('aoRNLd src', '')
        rating = row.get('F7nice', '')
        category = row.get('DkEaL', '')
        address = row.get('Io6YTe', '')
        status = row.get('ZDu9vd', '')

        meta = [category] if category else []
        if rating:
            meta.append(f"評分 {rating} ★")
        if status:
            meta.append(status)
        meta_text = ' · '.join(meta)

        card = f"""
        <article class='card'>
            <a class='card-link' href='businesses/{slug}.html'>
                {'<div class="thumb"><img src="'+image+'" alt="'+name+'" loading="lazy"></div>' if image else ''}
                <div class='card-body'>
                    <h2>{name}</h2>
                    {'<p class="meta">'+meta_text+'</p>' if meta_text else ''}
                    {'<p class="address">'+address+'</p>' if address else ''}
                </div>
            </a>
        </article>
        """
        cards.append(card)

    html = f"""
    <html lang='zh-Hant'>
    <head>
        <meta charset='utf-8'>
        <title>高雄水電行列表</title>
        <link rel='stylesheet' href='style.css'>
    </head>
    <body>
        <div class='page'>
            <header class='hero'>
                <div class='hero-text'>
                    <p class='eyebrow'>GitHub Pages</p>
                    <h1>高雄水電行專區</h1>
                    <p class='subhead'>為 30 間水電行建立獨立介紹頁面，方便透過 GitHub Pages 瀏覽。</p>
                </div>
            </header>
            <main class='grid'>
                {''.join(cards)}
            </main>
        </div>
    </body>
    </html>
    """
    (DOCS_DIR / 'index.html').write_text(html, encoding='utf-8')


def write_styles():
    style = """
    :root {
        --bg: #0b1021;
        --card: #121832;
        --accent: #4fe3c1;
        --text: #e9edf7;
        --muted: #a6b2d1;
    }
    * { box-sizing: border-box; }
    body {
        margin: 0;
        font-family: 'Noto Sans TC', 'Inter', system-ui, -apple-system, sans-serif;
        background: radial-gradient(circle at 10% 20%, #19254b, #0b1021 50%), #0b1021;
        color: var(--text);
        min-height: 100vh;
    }
    a { color: inherit; text-decoration: none; }
    .page { max-width: 1100px; margin: 0 auto; padding: 32px 24px 64px; }
    .hero { display: grid; grid-template-columns: 1fr 320px; align-items: center; gap: 24px; padding: 24px; background: linear-gradient(135deg, rgba(79,227,193,0.12), rgba(79,227,193,0)); border: 1px solid rgba(79,227,193,0.25); border-radius: 16px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); }
    .hero-image img { width: 100%; border-radius: 14px; object-fit: cover; border: 1px solid rgba(79,227,193,0.35); box-shadow: 0 12px 40px rgba(0,0,0,0.35); }
    .eyebrow { text-transform: uppercase; letter-spacing: 0.12em; font-size: 12px; color: var(--accent); margin: 0 0 8px; font-weight: 700; }
    h1 { margin: 0 0 8px; font-size: 32px; }
    .subhead { margin: 0; color: var(--muted); font-size: 16px; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 18px; margin-top: 28px; }
    .card { background: var(--card); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; overflow: hidden; transition: transform 160ms ease, border-color 160ms ease, box-shadow 160ms ease; }
    .card:hover { transform: translateY(-4px); border-color: rgba(79,227,193,0.6); box-shadow: 0 18px 40px rgba(0,0,0,0.35); }
    .thumb { height: 160px; background: #0f142a; display: flex; align-items: center; justify-content: center; overflow: hidden; }
    .thumb img { width: 100%; height: 100%; object-fit: cover; }
    .card-body { padding: 16px; }
    .card h2 { margin: 0 0 8px; font-size: 18px; }
    .meta { margin: 0 0 8px; color: var(--muted); }
    .address { margin: 0; color: var(--text); font-weight: 600; }
    .content { display: grid; gap: 16px; margin-top: 24px; }
    .info-block { background: var(--card); border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; padding: 16px; }
    .info-block h3 { margin: 0 0 6px; font-size: 16px; color: var(--accent); }
    .info-block p { margin: 0; line-height: 1.5; }
    .info-block ul { margin: 0; padding-left: 18px; color: var(--text); line-height: 1.6; }
    .page-footer { margin-top: 28px; display: flex; gap: 12px; flex-wrap: wrap; }
    .button { padding: 12px 16px; border-radius: 12px; border: 1px solid rgba(79,227,193,0.3); color: var(--text); font-weight: 700; background: rgba(255,255,255,0.03); transition: background 140ms ease, border-color 140ms ease, transform 140ms ease; }
    .button.primary { background: linear-gradient(135deg, #4fe3c1, #3bc0a3); color: #06121f; border-color: transparent; }
    .button:hover { transform: translateY(-1px); border-color: rgba(79,227,193,0.8); }
    @media (max-width: 768px) {
        .hero { grid-template-columns: 1fr; }
        .hero-image { order: -1; }
    }
    """
    (DOCS_DIR / 'style.css').write_text(style, encoding='utf-8')


def main():
    ensure_dirs()
    rows = list(load_rows())
    rows_with_slugs = []
    used = set()
    for row in rows:
        slug = slugify(row.get('DUwDvf', 'business'))
        # ensure unique
        base = slug or 'business'
        suffix = 1
        while slug in used:
            suffix += 1
            slug = f"{base}-{suffix}"
        used.add(slug)
        render_business_page(row, slug)
        rows_with_slugs.append((row, slug))

    render_index(rows_with_slugs)
    write_styles()


if __name__ == '__main__':
    main()
