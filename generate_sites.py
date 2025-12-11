import csv
import json
import re
import unicodedata
from pathlib import Path

SOURCE_CSV = Path("從-google.com.tw-抓取細節--6--2025-12-11.csv")
OUTPUT_DIR = Path("docs")
ASSETS_DIR = OUTPUT_DIR / "assets"
STORE_DIR = OUTPUT_DIR / "stores"
DATA_DIR = OUTPUT_DIR / "data"

FIELD_NAMES = [
    "map_url",
    "name",
    "rating",
    "category",
    "address",
    "status",
    "phone_primary",
    "phone_primary_link",
    "phone_alt",
    "phone_alt_link",
    "phone_display",
    "image_url",
]

def slugify(name: str, index: int) -> str:
    normalized = unicodedata.normalize("NFKD", name)
    ascii_name = normalized.encode("ascii", "ignore").decode().lower()
    ascii_name = re.sub(r"[^a-z0-9]+", "-", ascii_name).strip("-")
    if not ascii_name:
        ascii_name = f"store-{index+1}"
    return ascii_name

def collect_phones(row):
    phones = []
    seen = set()
    for value in row[6:11]:
        clean = value.strip()
        if clean.startswith("tel:"):
            clean = clean[4:]
        if clean and clean not in seen:
            phones.append(clean)
            seen.add(clean)
    return phones

def load_businesses():
    if not SOURCE_CSV.exists():
        raise FileNotFoundError(f"Source CSV not found: {SOURCE_CSV}")

    businesses = []
    with SOURCE_CSV.open(encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for index, row in enumerate(reader):
            data = dict(zip(FIELD_NAMES, row))
            phones = collect_phones(row)
            business = {
                "id": index + 1,
                "slug": slugify(data["name"], index),
                "map_url": data["map_url"],
                "name": data["name"],
                "rating": data.get("rating"),
                "category": data.get("category"),
                "address": data.get("address"),
                "status": data.get("status"),
                "phones": phones,
                "image_url": data.get("image_url"),
            }
            businesses.append(business)
    return businesses

def write_json(businesses):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "businesses.json").write_text(
        json.dumps(businesses, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

def build_assets():
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    (ASSETS_DIR / "style.css").write_text(
        """
:root {
  --bg: #0b0c10;
  --card: #12141b;
  --accent: #3fd0c9;
  --text: #e5e7eb;
  --muted: #a0aec0;
  --danger: #ff6b6b;
  --success: #45d483;
  --shadow: 0 10px 30px rgba(0,0,0,0.35);
  --radius: 14px;
  --max-width: 1200px;
}

* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: radial-gradient(circle at 20% 20%, rgba(63,208,201,0.08), transparent 25%),
              radial-gradient(circle at 80% 0%, rgba(255,255,255,0.04), transparent 30%),
              var(--bg);
  color: var(--text);
  min-height: 100vh;
  padding: 40px 16px 80px;
}

main {
  max-width: var(--max-width);
  margin: 0 auto;
}

.header {
  display: flex;
  gap: 16px;
  align-items: center;
  margin-bottom: 32px;
}

.badge {
  background: rgba(63,208,201,0.1);
  color: var(--accent);
  padding: 6px 12px;
  border-radius: 999px;
  font-size: 13px;
  letter-spacing: 0.02em;
  border: 1px solid rgba(63,208,201,0.25);
}

h1 {
  margin: 0;
  font-size: 32px;
  letter-spacing: -0.02em;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 18px;
}

.card {
  background: var(--card);
  border-radius: var(--radius);
  padding: 18px;
  box-shadow: var(--shadow);
  border: 1px solid rgba(255,255,255,0.05);
  display: flex;
  flex-direction: column;
  gap: 12px;
  position: relative;
  overflow: hidden;
}

.card::after {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: linear-gradient(135deg, rgba(63,208,201,0.08), transparent 35%);
}

.card h2 {
  margin: 0;
  font-size: 20px;
}

.meta, .contact {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  color: var(--muted);
  font-size: 14px;
}

.status {
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 13px;
  border: 1px solid rgba(255,255,255,0.1);
}

.status.open { color: var(--success); border-color: rgba(69,212,131,0.3); }
.status.closed { color: var(--danger); border-color: rgba(255,107,107,0.25); }

.buttons {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-top: auto;
}

button, .btn {
  appearance: none;
  border: none;
  background: var(--accent);
  color: #0b0c10;
  padding: 10px 14px;
  border-radius: 10px;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
  transition: transform 120ms ease, box-shadow 120ms ease;
  box-shadow: 0 10px 25px rgba(63,208,201,0.25);
}

.btn.secondary {
  background: transparent;
  color: var(--text);
  border: 1px solid rgba(255,255,255,0.08);
  box-shadow: none;
}

button:hover, .btn:hover { transform: translateY(-1px); }

.hero {
  background: linear-gradient(135deg, rgba(63,208,201,0.16), rgba(63,208,201,0.08));
  padding: 18px;
  border-radius: var(--radius);
  border: 1px solid rgba(63,208,201,0.25);
  margin-bottom: 18px;
  box-shadow: var(--shadow);
}

.hero img {
  width: 100%;
  border-radius: 12px;
  border: 1px solid rgba(255,255,255,0.05);
  margin-top: 12px;
}

.details {
  background: var(--card);
  padding: 18px;
  border-radius: var(--radius);
  border: 1px solid rgba(255,255,255,0.06);
  box-shadow: var(--shadow);
}

a { color: var(--accent); }

footer {
  margin-top: 36px;
  color: var(--muted);
  text-align: center;
  font-size: 13px;
}

@media (max-width: 600px) {
  body { padding: 24px 14px; }
  .header { flex-direction: column; align-items: flex-start; }
}
""",
        encoding="utf-8",
    )

def render_index(businesses):
    OUTPUT_DIR.mkdir(exist_ok=True)
    cards = []
    for b in businesses:
        status_class = "open" if b.get("status", "").startswith("營業") else "closed"
        phone = b["phones"][0] if b["phones"] else None
        call_button = (
            f'<a class="btn" href="tel:{phone}" aria-label="撥打 {phone}">立即致電</a>'
            if phone else ""
        )
        cards.append(
            f"""
            <article class=\"card\">
              <div class=\"meta\">{b.get('category','')}</div>
              <h2>{b['name']}</h2>
              <div class=\"meta\">⭐ {b.get('rating','--')} / 5</div>
              <div class=\"meta\">{b.get('address','')}</div>
              <div class=\"status {status_class}\">{b.get('status','')}</div>
              <div class=\"contact\">{', '.join(b['phones']) if b['phones'] else '未提供電話'}</div>
              <div class=\"buttons\">
                <a class=\"btn\" href=\"stores/{b['slug']}/\" aria-label=\"查看 {b['name']} 詳情\">查看店家頁面</a>
                {call_button}
              </div>
            </article>
            """
        )

    content = f"""
<!doctype html>
<html lang=\"zh-Hant\">
  <head>
    <meta charset=\"UTF-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
    <title>高雄水電行地圖｜GitHub Pages</title>
    <link rel=\"stylesheet\" href=\"assets/style.css\" />
  </head>
  <body>
    <main>
      <div class=\"header\">
        <span class=\"badge\">共 {len(businesses)} 間店家</span>
        <h1>高雄水電行專屬網站</h1>
      </div>
      <section class=\"hero\">
        <p>資料來源於 Google 地圖抓取，已為每間水電行生成專屬單頁，並可直接掛載於 GitHub Pages。</p>
        <p>點選卡片可查看專屬網站，也可以直接點擊電話按鈕立即撥打。</p>
      </section>
      <section class=\"grid\">
        {''.join(cards)}
      </section>
      <footer>以 CSV 自動生成，更新資料後執行 <code>python generate_sites.py</code> 重新發布。</footer>
    </main>
  </body>
</html>
"""
    (OUTPUT_DIR / "index.html").write_text(content, encoding="utf-8")

def render_store_page(business):
    store_path = STORE_DIR / business["slug"]
    store_path.mkdir(parents=True, exist_ok=True)
    status_class = "open" if business.get("status", "").startswith("營業") else "closed"
    phone_links = "".join(
        f'<li><a href="tel:{p}" aria-label="撥打 {p}">{p}</a></li>' for p in business["phones"]
    ) or "<li>未提供電話</li>"
    image_url = business.get("image_url")
    image_html = (
        f'<img src="{image_url}" alt="{business["name"]}" loading="lazy" />'
        if image_url
        else ""
    )
    primary_phone = business["phones"][0] if business["phones"] else ""
    call_button = (
        f'<a class="btn" href="tel:{primary_phone}">立即致電</a>' if primary_phone else ""
    )
    content = f"""
<!doctype html>
<html lang=\"zh-Hant\">
  <head>
    <meta charset=\"UTF-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
    <title>{business['name']}｜高雄水電行專屬網站</title>
    <link rel=\"stylesheet\" href=\"../../assets/style.css\" />
  </head>
  <body>
    <main>
      <div class=\"header\">
        <span class=\"badge\">專屬頁面</span>
        <h1>{business['name']}</h1>
      </div>
      <section class=\"hero\">
        <p>⭐ 評分：{business.get('rating','--')} · {business.get('category','')}</p>
        <p class=\"meta\">地址：{business.get('address','')}</p>
        <p class=\"status {status_class}\">{business.get('status','')}</p>
        {image_html}
      </section>
      <section class=\"details\">
        <h3>聯絡資訊</h3>
        <ul>{phone_links}</ul>
        <p><a href=\"{business.get('map_url','')}\" target=\"_blank\" rel=\"noopener\">在 Google 地圖查看</a></p>
      </section>
      <div class=\"buttons\">
        <a class=\"btn secondary\" href=\"../../\">返回總覽</a>
        {call_button}
      </div>
      <footer>此頁面由 CSV 自動生成，更新資料後重新執行產生腳本即可同步。</footer>
    </main>
  </body>
</html>
"""
    (store_path / "index.html").write_text(content, encoding="utf-8")

def main():
    businesses = load_businesses()
    build_assets()
    write_json(businesses)
    render_index(businesses)
    for business in businesses:
        render_store_page(business)
    print(f"Generated {len(businesses)} store pages in {STORE_DIR}")

if __name__ == "__main__":
    main()
