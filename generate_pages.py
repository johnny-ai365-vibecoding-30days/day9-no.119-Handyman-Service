import csv
import html
import pathlib
import re
from typing import Dict, List

DATA_PATH = pathlib.Path("從-google.com.tw-抓取細節--6--2025-12-11.csv")
DOCS_DIR = pathlib.Path("docs")
STORE_DIR = DOCS_DIR / "stores"
ASSETS_DIR = DOCS_DIR / "assets"


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", name).strip("-").lower()
    return slug or "store"


def parse_rows(path: pathlib.Path) -> List[Dict[str, str]]:
    stores: List[Dict[str, str]] = []
    with path.open(encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)  # skip header row
        slugs = set()
        for idx, row in enumerate(reader):
            if not row:
                continue
            data = {
                "map_url": row[0].strip(),
                "name": row[1].strip(),
                "rating": row[2].strip(),
                "category": row[3].strip(),
                "address": row[4].strip(),
                "status": row[5].strip(),
                "contact_primary": row[6].strip(),
                "contact_link": row[7].strip(),
                "website_1": row[8].strip(),
                "website_2": row[9].strip(),
                "contact_secondary": row[10].strip(),
                "image_url": row[11].strip(),
            }
            base_slug = slugify(data["name"] or f"store-{idx+1}")
            slug = base_slug
            counter = 2
            while slug in slugs:
                slug = f"{base_slug}-{counter}"
                counter += 1
            data["slug"] = slug
            slugs.add(slug)
            stores.append(data)
    return stores


def build_assets():
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    css = """
    :root {
        --bg: #0f172a;
        --panel: #111827;
        --card: #1f2937;
        --text: #e5e7eb;
        --muted: #9ca3af;
        --accent: #38bdf8;
        --accent-2: #a855f7;
        --shadow: 0 10px 40px rgba(0,0,0,0.25);
    }

    * { box-sizing: border-box; }

    body {
        font-family: 'Inter', 'Noto Sans TC', system-ui, -apple-system, sans-serif;
        margin: 0;
        background: radial-gradient(circle at 20% 20%, rgba(56,189,248,0.08), transparent 25%),
                    radial-gradient(circle at 80% 0%, rgba(168,85,247,0.08), transparent 25%),
                    var(--bg);
        color: var(--text);
        min-height: 100vh;
    }

    a { color: inherit; text-decoration: none; }

    header {
        padding: 32px 24px 8px;
        text-align: center;
    }

    header h1 { margin: 0; font-size: 32px; letter-spacing: 0.4px; }
    header p { margin: 8px 0 0; color: var(--muted); }

    main { padding: 16px 24px 40px; }

    .grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
        gap: 18px;
        max-width: 1200px;
        margin: 0 auto;
    }

    .card {
        background: linear-gradient(145deg, rgba(31,41,55,0.97), rgba(17,24,39,0.95));
        border: 1px solid rgba(255,255,255,0.04);
        border-radius: 16px;
        padding: 18px;
        box-shadow: var(--shadow);
        transition: transform 160ms ease, border-color 160ms ease, box-shadow 160ms ease;
    }

    .card:hover {
        transform: translateY(-4px);
        border-color: rgba(56,189,248,0.3);
        box-shadow: 0 20px 50px rgba(0,0,0,0.32);
    }

    .card h2 { margin: 0 0 8px; font-size: 20px; }
    .meta { color: var(--muted); font-size: 14px; }

    .badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 10px;
        border-radius: 999px;
        background: rgba(56,189,248,0.12);
        color: #7dd3fc;
        font-size: 13px;
        margin-right: 8px;
    }

    .status-open { color: #4ade80; }
    .status-closed { color: #f87171; }

    .hero {
        position: relative;
        border-radius: 18px;
        overflow: hidden;
        margin: 24px auto;
        max-width: 960px;
        box-shadow: var(--shadow);
    }

    .hero img {
        width: 100%;
        height: 320px;
        object-fit: cover;
        display: block;
    }

    .hero .overlay {
        position: absolute;
        inset: 0;
        background: linear-gradient(180deg, rgba(0,0,0,0.1), rgba(0,0,0,0.35));
    }

    .content {
        max-width: 960px;
        margin: 0 auto;
        background: rgba(17,24,39,0.8);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 20px;
        padding: 24px;
        box-shadow: var(--shadow);
    }

    .section { margin-bottom: 18px; }
    .section h3 { margin: 0 0 8px; font-size: 16px; color: #bfdbfe; letter-spacing: 0.5px; }

    .info-row { display: flex; flex-wrap: wrap; gap: 10px; color: var(--muted); }

    .links a {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 10px 12px;
        margin-right: 8px;
        margin-bottom: 8px;
        border-radius: 12px;
        background: rgba(56,189,248,0.1);
        color: #7dd3fc;
        font-weight: 600;
    }

    .footer { text-align: center; color: var(--muted); margin: 24px 0 12px; font-size: 14px; }

    .back-link { color: #c084fc; }
    """
    (ASSETS_DIR / "style.css").write_text(css, encoding="utf-8")


def render_index(stores: List[Dict[str, str]]):
    cards = []
    for store in stores:
        status_class = "status-open" if "營業中" in store["status"] else "status-closed"
        image_style = f"background-image:url('{store['image_url']}');" if store["image_url"] else ""
        cards.append(f"""
        <a class=\"card\" href=\"stores/{store['slug']}.html\" aria-label=\"前往 {html.escape(store['name'])}\">
            <h2>{html.escape(store['name'])}</h2>
            <div class=\"meta\">{html.escape(store['category'])}</div>
            <div class=\"meta\">{html.escape(store['address'])}</div>
            <div class=\"meta\"><span class=\"badge\">⭐ {html.escape(store['rating'] or 'N/A')}</span><span class=\"{status_class}\">{html.escape(store['status'] or '營業狀態未知')}</span></div>
        </a>
        """)

    html_doc = f"""
    <!doctype html>
    <html lang=\"zh-Hant\">
    <head>
        <meta charset=\"utf-8\">
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
        <title>水電行資料彙整 | GitHub Pages</title>
        <link rel=\"stylesheet\" href=\"assets/style.css\">
    </head>
    <body>
        <header>
            <h1>高雄三民區水電行彙整</h1>
            <p>共 {len(stores)} 間店家，點擊卡片即可進入各自的介紹頁。</p>
        </header>
        <main>
            <div class=\"grid\">{''.join(cards)}</div>
        </main>
        <div class=\"footer\">資料來源：Google 地圖，最後更新：2025-12-11</div>
    </body>
    </html>
    """
    (DOCS_DIR / "index.html").write_text(html_doc.strip(), encoding="utf-8")


def render_store(store: Dict[str, str]):
    DOCS_DIR.mkdir(exist_ok=True)
    STORE_DIR.mkdir(parents=True, exist_ok=True)

    contact_numbers = [c for c in [store["contact_primary"], store["contact_secondary"]] if c]
    contacts = "<br>".join(html.escape(c) for c in dict.fromkeys(contact_numbers)) or "無資料"

    links = []
    for label, url in [
        ("Google 地圖", store["map_url"]),
        ("撥打電話", store["contact_link"] or ("tel:" + store["contact_primary"] if store["contact_primary"] else "")),
        ("網站", store["website_1"]),
        ("其他連結", store["website_2"]),
    ]:
        if url:
            links.append(f"<a href=\"{html.escape(url)}\" target=\"_blank\" rel=\"noopener\">{label}</a>")

    status_class = "status-open" if "營業中" in store["status"] else "status-closed"
    hero = f"<div class=\"hero\"><img src=\"{html.escape(store['image_url'])}\" alt=\"{html.escape(store['name'])}\"><div class=\"overlay\"></div></div>" if store["image_url"] else ""

    page = f"""
    <!doctype html>
    <html lang=\"zh-Hant\">
    <head>
        <meta charset=\"utf-8\">
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
        <title>{html.escape(store['name'])} | 水電行介紹</title>
        <link rel=\"stylesheet\" href=\"../assets/style.css\">
    </head>
    <body>
        <header>
            <h1>{html.escape(store['name'])}</h1>
            <p>{html.escape(store['category'])}</p>
        </header>
        {hero}
        <main class=\"content\">
            <div class=\"section\">
                <h3>評分與營業狀態</h3>
                <div class=\"info-row\">
                    <span class=\"badge\">⭐ {html.escape(store['rating'] or 'N/A')}</span>
                    <span class=\"{status_class}\">{html.escape(store['status'] or '營業狀態未知')}</span>
                </div>
            </div>
            <div class=\"section\">
                <h3>地址</h3>
                <div class=\"info-row\">{html.escape(store['address'])}</div>
            </div>
            <div class=\"section\">
                <h3>聯絡方式</h3>
                <div class=\"info-row\">{contacts}</div>
            </div>
            <div class=\"section links\">
                <h3>相關連結</h3>
                {''.join(links) or '<span class="meta">無連結</span>'}
            </div>
            <div class=\"section\">
                <a class=\"back-link\" href=\"../index.html\">← 返回店家列表</a>
            </div>
        </main>
        <div class=\"footer\">資料來源：Google 地圖，最後更新：2025-12-11</div>
    </body>
    </html>
    """
    (STORE_DIR / f"{store['slug']}.html").write_text(page.strip(), encoding="utf-8")


def main():
    stores = parse_rows(DATA_PATH)
    build_assets()
    render_index(stores)
    for store in stores:
        render_store(store)


if __name__ == "__main__":
    main()
