import csv
import html
import os
import re
from pathlib import Path

DATA_FILE = Path('從-google.com.tw-抓取細節--6--2025-12-11.csv')
DOCS_DIR = Path('docs')
STYLE_PATH = DOCS_DIR / 'style.css'


def slugify(name: str, index: int) -> str:
    base = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return base if base else f"business-{index + 1}"


def first_non_empty(*values):
    for value in values:
        if value and value.strip():
            return value.strip()
    return ""


def clean_phone(value: str) -> str:
    cleaned = value.replace("tel:", "").replace(" ", "").strip()
    return cleaned


def collect_phone_numbers(row):
    phones = []
    for idx in (6, 10, 7, 8, 9):
        if idx < len(row):
            raw = row[idx].strip()
            if raw:
                phone = clean_phone(raw)
                if phone and phone not in phones:
                    phones.append(phone)
    return phones


def ensure_style():
    DOCS_DIR.mkdir(exist_ok=True)
    if STYLE_PATH.exists():
        return
    STYLE_PATH.write_text(
        """
:root {
  --bg: #f8fafc;
  --surface: #ffffff;
  --primary: #0f766e;
  --text: #0f172a;
  --muted: #475569;
  --border: #e2e8f0;
  --shadow: 0 8px 24px rgba(15, 23, 42, 0.12);
  font-family: 'Noto Sans TC', 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
}

* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--text); }
header { background: linear-gradient(135deg, #14b8a6, #0f766e); color: #fff; padding: 48px 24px; text-align: center; }
main { max-width: 1080px; margin: -40px auto 48px; padding: 0 24px; }
.card-grid { display: grid; gap: 20px; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); }
.card, .page { background: var(--surface); border-radius: 14px; box-shadow: var(--shadow); padding: 20px; border: 1px solid var(--border); }
.card h2 { margin-top: 0; font-size: 20px; }
.badge { display: inline-flex; align-items: center; gap: 6px; padding: 6px 10px; background: #ecfeff; color: #0f766e; border-radius: 999px; font-weight: 700; }
.status { font-weight: 600; }
.status.open { color: #16a34a; }
.status.closed { color: #dc2626; }
.meta { color: var(--muted); margin: 4px 0; }
button, .button { background: var(--primary); color: #fff; border: none; padding: 12px 16px; border-radius: 10px; font-weight: 700; cursor: pointer; text-decoration: none; display: inline-flex; align-items: center; gap: 8px; box-shadow: 0 10px 30px rgba(20, 184, 166, 0.35); }
.actions { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 12px; }
.hero { width: 100%; border-radius: 12px; margin: 16px 0; object-fit: cover; max-height: 340px; border: 1px solid var(--border); }
nav { margin-bottom: 16px; }
nav a { color: var(--primary); text-decoration: none; font-weight: 700; }
.footer { text-align: center; color: var(--muted); margin-top: 32px; }
section { margin-top: 12px; }
ul { padding-left: 18px; margin: 6px 0; }
@media (max-width: 640px) { header { padding: 32px 18px; } main { padding: 0 14px; } }
""",
        encoding="utf-8",
    )


def write_index(businesses):
    cards = []
    for biz in businesses:
        phones = "、".join(biz['phones']) if biz['phones'] else "未提供聯絡電話"
        status_class = "open" if "營業" in biz['status'] else "closed"
        cards.append(
            f"<article class='card'>"
            f"<div class='badge'>⭐ {html.escape(biz['rating'] or 'N/A')}</div>"
            f"<h2><a href='{biz['slug']}/'>{html.escape(biz['name'])}</a></h2>"
            f"<div class='meta'>{html.escape(biz['category'])}</div>"
            f"<div class='meta'>{html.escape(biz['address'])}</div>"
            f"<div class='meta status {status_class}'>{html.escape(biz['status'] or '狀態未知')}</div>"
            f"<div class='meta'>☎️ {html.escape(phones)}</div>"
            f"<div class='actions'><a class='button' href='{biz['slug']}/'>查看網站</a>"
            f"<a class='button' href='{html.escape(biz['map_link'])}' target='_blank' rel='noopener'>Google 地圖</a></div>"
            f"</article>"
        )

    DOCS_DIR.mkdir(exist_ok=True)
    (DOCS_DIR / 'index.html').write_text(
        """
<!doctype html>
<html lang='zh-TW'>
<head>
  <meta charset='utf-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1'>
  <title>水電行名錄｜GitHub Pages</title>
  <link rel='stylesheet' href='style.css'>
</head>
<body>
  <header>
    <p style='letter-spacing: 0.12em; text-transform: uppercase; opacity: 0.85;'>Handyman Directory</p>
    <h1 style='margin: 8px 0 0;'>水電行 GitHub Pages 集合</h1>
    <p style='opacity: 0.9;'>每一家水電行都有專屬的單頁網站，點擊卡片即可進入。</p>
  </header>
  <main>
    <div class='card-grid'>
"""
        + "\n".join(cards)
        + """
    </div>
    <p class='footer'>資料來源：從 Google Maps 匯出，生成時間由 build_sites.py 控制。</p>
  </main>
</body>
</html>
""",
        encoding="utf-8",
    )


def write_business_page(biz):
    folder = DOCS_DIR / biz['slug']
    folder.mkdir(parents=True, exist_ok=True)
    phones = biz['phones']
    phone_list = "".join(f"<li>{html.escape(p)}</li>" for p in phones) if phones else "<li>未提供</li>"
    phone_actions = "".join(
        f"<a class='button' href='tel:{html.escape(p)}'>立即撥打 {html.escape(p)}</a>" for p in phones
    ) or "<span class='meta'>沒有提供電話號碼</span>"
    status_class = "open" if "營業" in biz['status'] else "closed"

    (folder / 'index.html').write_text(
        f"""
<!doctype html>
<html lang='zh-TW'>
<head>
  <meta charset='utf-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1'>
  <title>{html.escape(biz['name'])}｜水電行專頁</title>
  <link rel='stylesheet' href='../style.css'>
</head>
<body>
  <header>
    <p style='letter-spacing: 0.12em; text-transform: uppercase; opacity: 0.85;'>Handyman Profile</p>
    <h1 style='margin: 8px 0 0;'>{html.escape(biz['name'])}</h1>
    <p style='opacity: 0.9;'>{html.escape(biz['category'] or '')}</p>
  </header>
  <main>
    <nav><a href='../index.html'>← 返回名錄</a></nav>
    <article class='page'>
      <div class='badge'>⭐ {html.escape(biz['rating'] or '尚未評分')}</div>
      <p class='meta status {status_class}'>{html.escape(biz['status'] or '營業狀態未知')}</p>
      <p class='meta'>📍 {html.escape(biz['address'])}</p>
      <div class='actions'>
        <a class='button' href='{html.escape(biz['map_link'])}' target='_blank' rel='noopener'>在 Google 地圖查看</a>
        {phone_actions}
      </div>
      {f"<img class='hero' src='{html.escape(biz['image'])}' alt='{html.escape(biz['name'])}'>" if biz['image'] else ''}
      <section>
        <h3>聯絡電話</h3>
        <ul>{phone_list}</ul>
      </section>
      <section>
        <h3>關於本店</h3>
        <p>這個頁面是從原始資料自動生成的，方便在 GitHub Pages 上為每一間水電行建立獨立的介紹頁。</p>
      </section>
    </article>
    <p class='footer'>資料來源：{html.escape(DATA_FILE.name)}</p>
  </main>
</body>
</html>
""",
        encoding="utf-8",
    )


def load_businesses():
    with DATA_FILE.open(encoding='utf-8') as f:
        rows = list(csv.reader(f))
    header, data_rows = rows[0], rows[1:]
    businesses = []
    for idx, row in enumerate(data_rows):
        map_link = row[0].strip()
        name = row[1].strip()
        rating = row[2].strip()
        category = row[3].strip()
        address = row[4].strip()
        status = row[5].strip()
        phones = collect_phone_numbers(row)
        image = row[11].strip() if len(row) > 11 else ""
        businesses.append({
            'slug': slugify(name, idx),
            'map_link': map_link,
            'name': name,
            'rating': rating,
            'category': category,
            'address': address,
            'status': status,
            'phones': phones,
            'image': image,
        })
    return businesses


def main():
    ensure_style()
    businesses = load_businesses()
    write_index(businesses)
    for biz in businesses:
        write_business_page(biz)
    print(f"Generated {len(businesses)} business pages in {DOCS_DIR}/")


if __name__ == '__main__':
    main()
