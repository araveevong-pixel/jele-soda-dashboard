#!/usr/bin/env python3
"""
JELE SODA 2026 — Update Dashboard
Read JSON from scraper → inject into KOL_DATA in index.html
Usage: python3 scripts/update_dashboard.py scrape_results.json index.html
"""

import json
import sys
import re

# ============================================================
#  KOL METADATA — fallback data for all KOLs
# ============================================================
KOL_METADATA = {
    # Main (5)
    'biw_songkran':   {'displayName': 'บิวบอง', 'tier': 'Main', 'category': 'ภาคอีสาน', 'gender': '-', 'followers': 1900000, 'budget': 110000},
    'fasin22052545':  {'displayName': 'พี่บังจับไมค์', 'tier': 'Main', 'category': 'ภาคใต้', 'gender': '-', 'followers': 297900, 'budget': 35000},
    'ovapachannel':   {'displayName': 'OVAPA CHANNEL', 'tier': 'Main', 'category': 'ภาคเหนือ', 'gender': '-', 'followers': 397200, 'budget': 50000},
    'nophuwanet':     {'displayName': 'เซียนหรั่ง', 'tier': 'Main', 'category': 'ภาคอีสาน', 'gender': '-', 'followers': 1700000, 'budget': 110000},
    'tkpst2':         {'displayName': 'บริษัทตั้งหวังเจ๊ง', 'tier': 'Main', 'category': 'ภาคอีสาน', 'gender': '-', 'followers': 5500000, 'budget': 35000},
    # Micro - ภาคกลาง (15)
    'plugsweden':     {'displayName': 'plugsweden', 'tier': 'Micro', 'category': 'ภาคกลาง', 'gender': '-', 'followers': 198800, 'budget': 16000},
    'pakkaput17':     {'displayName': 'pakkaput17', 'tier': 'Micro', 'category': 'ภาคกลาง', 'gender': '-', 'followers': 369700, 'budget': 25000},
    'kuanpuantiew':   {'displayName': 'กวนป่วนเที่ยว', 'tier': 'Micro', 'category': 'ภาคกลาง', 'gender': '-', 'followers': 1100000, 'budget': 25000},
    'pexjakkajee':    {'displayName': 'เป๊กจั๊กกะจี้', 'tier': 'Micro', 'category': 'ภาคกลาง', 'gender': '-', 'followers': 1400000, 'budget': 45000},
    'puwanaipison':   {'displayName': 'ไพซอล', 'tier': 'Micro', 'category': 'ภาคกลาง', 'gender': '-', 'followers': 335900, 'budget': 40000},
    'saokrungthep':   {'displayName': 'สาวกรุงเทพ', 'tier': 'Micro', 'category': 'ภาคกลาง', 'gender': '-', 'followers': 235200, 'budget': 35000},
    'll0499':         {'displayName': 'MY K ME KEN', 'tier': 'Micro', 'category': 'ภาคกลาง', 'gender': '-', 'followers': 248000, 'budget': 34000},
    'pooliepraew':    {'displayName': 'pooliepraew', 'tier': 'Micro', 'category': 'ภาคกลาง', 'gender': '-', 'followers': 1200000, 'budget': 45000},
    'f_u_i_':         {'displayName': 'f_u_i_', 'tier': 'Micro', 'category': 'ภาคกลาง', 'gender': '-', 'followers': 212200, 'budget': 55000},
    'tan_slaz19':     {'displayName': 'อินฟลูน้ำตาลตก', 'tier': 'Micro', 'category': 'ภาคกลาง', 'gender': '-', 'followers': 143800, 'budget': 25000},
    'armgoodsunday':  {'displayName': 'armgoodsunday', 'tier': 'Micro', 'category': 'ภาคกลาง', 'gender': '-', 'followers': 801800, 'budget': 35000},
    'pupemaipriaw':   {'displayName': 'ปูเป้ไม่เปรี้ยว', 'tier': 'Micro', 'category': 'ภาคกลาง', 'gender': '-', 'followers': 538700, 'budget': 40000},
    'jekkabot5555':   {'displayName': 'jekkabot5555', 'tier': 'Micro', 'category': 'ภาคกลาง', 'gender': '-', 'followers': 1500000, 'budget': 40000},
    'lenpaither':     {'displayName': 'เล่นไปเถอะ', 'tier': 'Micro', 'category': 'ภาคกลาง', 'gender': '-', 'followers': 27400, 'budget': 35000},
    'bosck999':       {'displayName': 'บอสซีเค', 'tier': 'Micro', 'category': 'ภาคกลาง', 'gender': '-', 'followers': 1500000, 'budget': 55000},
    # Micro - ภาคเหนือ (4)
    'gotarm65':       {'displayName': 'gotarm65', 'tier': 'Micro', 'category': 'ภาคเหนือ', 'gender': '-', 'followers': 563000, 'budget': 40000},
    'tikbadai':       {'displayName': 'อ้ายติ๊กบะดาย', 'tier': 'Micro', 'category': 'ภาคเหนือ', 'gender': '-', 'followers': 680800, 'budget': 28000},
    'patpaladmuang':  {'displayName': 'patpaladmuang', 'tier': 'Micro', 'category': 'ภาคเหนือ', 'gender': '-', 'followers': 243700, 'budget': 26000},
    'coochamp':       {'displayName': 'แช้มกับทีวีคู่ใจ', 'tier': 'Micro', 'category': 'ภาคเหนือ', 'gender': '-', 'followers': 639100, 'budget': 35000},
    # Micro - ภาคอีสาน (6)
    'aodbom2':        {'displayName': 'ปุณณภพ เฟรนลี่', 'tier': 'Micro', 'category': 'ภาคอีสาน', 'gender': '-', 'followers': 1700000, 'budget': 36000},
    'wootza5555':     {'displayName': 'wootza5555', 'tier': 'Micro', 'category': 'ภาคอีสาน', 'gender': '-', 'followers': 985100, 'budget': 33000},
    'bookteerapat':   {'displayName': 'บุ๊ค ธีร์', 'tier': 'Micro', 'category': 'ภาคอีสาน', 'gender': '-', 'followers': 694700, 'budget': 35000},
    'juno55555':      {'displayName': 'บักจูโน่', 'tier': 'Micro', 'category': 'ภาคอีสาน', 'gender': '-', 'followers': 2600000, 'budget': 29000},
    'biggesttha':     {'displayName': 'ครูใหญ่', 'tier': 'Micro', 'category': 'ภาคอีสาน', 'gender': '-', 'followers': 220900, 'budget': 25000},
    'apirak2539ice':  {'displayName': 'อิหล่าขาเลาะ', 'tier': 'Micro', 'category': 'ภาคอีสาน', 'gender': '-', 'followers': 5400000, 'budget': 32000},
    # Micro - ภาคใต้ (3)
    'royver_th':      {'displayName': 'royver_th', 'tier': 'Micro', 'category': 'ภาคใต้', 'gender': '-', 'followers': 793300, 'budget': 50000},
    'bunyaporn_2009': {'displayName': 'พาย คอนเฟลก', 'tier': 'Micro', 'category': 'ภาคใต้', 'gender': '-', 'followers': 5900000, 'budget': 29000},
    'thebellchanel':  {'displayName': 'The Bell channel', 'tier': 'Micro', 'category': 'ภาคใต้', 'gender': '-', 'followers': 331400, 'budget': 50000},
    # Mixology (14)
    'kayshomebar':    {'displayName': 'kayshomebar', 'tier': 'Mixology', 'category': 'Mixology', 'gender': '-', 'followers': 39100, 'budget': 15000},
    'raa_reun_core':  {'displayName': 'raa_reun_core', 'tier': 'Mixology', 'category': 'Mixology', 'gender': '-', 'followers': 424000, 'budget': 20000},
    'maxk_litt':      {'displayName': 'maxk_litt', 'tier': 'Mixology', 'category': 'Mixology', 'gender': '-', 'followers': 703600, 'budget': 10000},
    'maoaowfeel':     {'displayName': 'มาววเอาฟีลล', 'tier': 'Mixology', 'category': 'Mixology', 'gender': '-', 'followers': 12600, 'budget': 8000},
    'how.to.mao':     {'displayName': 'how.to.mao', 'tier': 'Mixology', 'category': 'Mixology', 'gender': '-', 'followers': 144700, 'budget': 9500},
    'arpo_story':     {'displayName': 'arpo_story', 'tier': 'Mixology', 'category': 'Mixology', 'gender': '-', 'followers': 149100, 'budget': 8000},
    'yod_121098':     {'displayName': 'yod_121098', 'tier': 'Mixology', 'category': 'Mixology', 'gender': '-', 'followers': 1200000, 'budget': 9000},
    'tatatomang':     {'displayName': 'tatatomang', 'tier': 'Mixology', 'category': 'Mixology', 'gender': '-', 'followers': 186900, 'budget': 9000},
    'taloncamp_sg':   {'displayName': 'ตะลอนแคมภ์', 'tier': 'Mixology', 'category': 'Mixology', 'gender': '-', 'followers': 257100, 'budget': 9000},
    'gowithgoldd':    {'displayName': 'ไปกับโกล์ด', 'tier': 'Mixology', 'category': 'Mixology', 'gender': '-', 'followers': 254000, 'budget': 9000},
    'maww_shabu':     {'displayName': 'มาวชาบู', 'tier': 'Mixology', 'category': 'Mixology', 'gender': '-', 'followers': 415500, 'budget': 10000},
    'tenitbrk':       {'displayName': 'โก้โกคนรักเมีย', 'tier': 'Mixology', 'category': 'Mixology', 'gender': '-', 'followers': 4099999, 'budget': 10000},
    'biibuaaastory':  {'displayName': 'biibuaaastory', 'tier': 'Mixology', 'category': 'Mixology', 'gender': '-', 'followers': 58900, 'budget': 9000},
    'snicker_nts':    {'displayName': 'snicker_nts', 'tier': 'Mixology', 'category': 'Mixology', 'gender': '-', 'followers': 114700, 'budget': 10000},
}

# ============================================================
#  KOL LINKS — same as scraper (for link injection)
# ============================================================
KOL_LINKS = {
    'biw_songkran': 'https://vt.tiktok.com/ZSm7UqSxm/',
    'fasin22052545': 'https://vt.tiktok.com/ZSmcaAb2h/',
    'ovapachannel': 'https://vt.tiktok.com/ZSmcm17pD/',
    'nophuwanet': 'https://vt.tiktok.com/ZSHdU6PSb/',
    'tkpst2': 'https://vt.tiktok.com/ZSuG2hcdu/',
    'plugsweden': 'https://vt.tiktok.com/ZSukQWcn8/',
    'pakkaput17': 'https://vt.tiktok.com/ZSmcaGQy3/',
    'kuanpuantiew': 'https://vt.tiktok.com/ZSmcato1w/',
    'pexjakkajee': 'https://vt.tiktok.com/ZSm7yUL5N/',
    'puwanaipison': 'https://vt.tiktok.com/ZSmcaTqdj/',
    'saokrungthep': 'https://vt.tiktok.com/ZSuYdxpWe/',
    'll0499': 'https://vt.tiktok.com/ZSuY6uqJd/',
    'pooliepraew': 'https://vt.tiktok.com/ZSuFppTeB/',
    'f_u_i_': 'https://vt.tiktok.com/ZSuYMC3Qs/',
    'tan_slaz19': 'https://vt.tiktok.com/ZSumNqjHt/',
    'armgoodsunday': 'https://vt.tiktok.com/ZSuaEAwaB/',
    'pupemaipriaw': 'https://vt.tiktok.com/ZSuWR3BAq/',
    'jekkabot5555': 'https://vt.tiktok.com/ZSuGTwRoY/',
    'lenpaither': 'https://vt.tiktok.com/ZSunRjn26/',
    'bosck999': 'https://vt.tiktok.com/ZSumpv8TU/',
    'gotarm65': 'https://vt.tiktok.com/ZSm7MXU59/',
    'tikbadai': 'https://vt.tiktok.com/ZSmcW2HWK/',
    'patpaladmuang': 'https://vt.tiktok.com/ZSmcaqqea/',
    'coochamp': 'https://vt.tiktok.com/ZSuY8vRRb/',
    'aodbom2': 'https://vt.tiktok.com/ZSuYMrAnR/',
    'wootza5555': 'https://vt.tiktok.com/ZSuYhbTuQ/',
    'bookteerapat': 'https://vt.tiktok.com/ZSunNhY3V/',
    'juno55555': 'https://vt.tiktok.com/ZSubjckjm/',
    'biggesttha': 'https://vt.tiktok.com/ZSuasTfRG/',
    'apirak2539ice': 'https://vt.tiktok.com/ZSuGpLFHg/',
    'royver_th': 'https://vt.tiktok.com/ZSuY89A6a/',
    'bunyaporn_2009': 'https://vt.tiktok.com/ZSumseLjA/',
    'thebellchanel': 'https://vt.tiktok.com/ZSumN9avE/',
    'kayshomebar': 'https://vt.tiktok.com/ZSuuWoyee/',
    'raa_reun_core': 'https://vt.tiktok.com/ZSum5tCCk/',
    'maxk_litt': 'https://vt.tiktok.com/ZSugeG1XM/',
    'maoaowfeel': 'https://vt.tiktok.com/ZSH8FKBrR/',
    'how.to.mao': 'https://vt.tiktok.com/ZSH22Lfm5/',
    'arpo_story': 'https://vt.tiktok.com/ZSHjVx76N/',
    'yod_121098': 'https://vt.tiktok.com/ZSHMfY2aq/',
    'tatatomang': 'https://vt.tiktok.com/ZSHeo6BDK/',
    'taloncamp_sg': 'https://vt.tiktok.com/ZSHReUSH1/',
    'gowithgoldd': 'https://vt.tiktok.com/ZSH6QyAGE/',
    'maww_shabu': 'https://vt.tiktok.com/ZSHdgHJDp/',
    'tenitbrk': 'https://vt.tiktok.com/ZSHd92dpE/',
    'biibuaaastory': 'https://vt.tiktok.com/ZSHj2v1y6/',
    'snicker_nts': 'https://vt.tiktok.com/ZSHFyNucR/',
}

# ============================================================
#  NOT POSTED KOLs — ลบชื่อออกเมื่อ KOL โพสต์แล้ว
# ============================================================
NOT_POSTED_KOLS = set([
    # เมื่อ KOL โพสต์แล้ว ให้ลบชื่อออกจาก set นี้
    # ตอนนี้ทุกคนโพสต์แล้ว — set ว่าง
])


def preserve_actual_use(html_content):
    """Extract current CAMPAIGN_ACTUAL_USE_DEFAULT value."""
    m = re.search(r'const\s+CAMPAIGN_ACTUAL_USE_DEFAULT\s*=\s*([\d.]+)', html_content)
    return float(m.group(1)) if m else 0


def parse_existing_kol_data(html_content):
    """Parse existing KOL_DATA from HTML to preserve stats for failed scrapes."""
    existing = {}
    pattern = r"\{\s*username:\s*'([^']+)'.*?views:\s*(\d+).*?likes:\s*(\d+).*?shares:\s*(\d+).*?comments:\s*(\d+).*?saves:\s*(\d+).*?followers:\s*(\d+)"
    for m in re.finditer(pattern, html_content):
        username = m.group(1)
        existing[username] = {
            'views': int(m.group(2)),
            'likes': int(m.group(3)),
            'shares': int(m.group(4)),
            'comments': int(m.group(5)),
            'saves': int(m.group(6)),
            'followers': int(m.group(7)),
        }
    return existing


def build_kol_entry(username, scrape_data, link='', existing_data=None):
    """Build a single KOL JavaScript object string.
    Falls back to existing_data (from HTML) when scrape fails."""
    meta = KOL_METADATA.get(username, {})
    sd = scrape_data.get(username, {})
    ex = (existing_data or {}).get(username, {})

    display_name = meta.get('displayName', username)
    tier = meta.get('tier', 'Micro')
    category = meta.get('category', 'ภาคกลาง')
    gender = meta.get('gender', '-')
    followers = sd.get('followers', 0) or meta.get('followers', 0)
    budget = meta.get('budget', 0)

    # Use scraped data; if missing, fall back to existing HTML data
    views = sd.get('views', 0) or ex.get('views', 0)
    likes = sd.get('likes', 0) or ex.get('likes', 0)
    shares = sd.get('shares', 0) or ex.get('shares', 0)
    comments = sd.get('comments', 0) or ex.get('comments', 0)
    saves = sd.get('saves', 0) or ex.get('saves', 0)

    posted = username not in NOT_POSTED_KOLS
    posts = 1 if posted else 0
    kpi_views = views

    return (
        f"  {{ username: '{username}', displayName: '{display_name}', "
        f"tier: '{tier}', platform: 'TikTok', category: '{category}', "
        f"gender: '{gender}', followers: {followers}, "
        f"views: {views}, likes: {likes}, shares: {shares}, "
        f"comments: {comments}, saves: {saves}, "
        f"posts: {posts}, kpi_views: {kpi_views}, "
        f"posted: {'true' if posted else 'false'}, "
        f"link: '{link}', budget: {budget} }}"
    )


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 scripts/update_dashboard.py scrape_results.json index.html")
        sys.exit(1)

    json_file = sys.argv[1]
    html_file = sys.argv[2]

    # Load scrape results
    try:
        with open(json_file, 'r') as f:
            scrape_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        scrape_data = {}

    # Read HTML
    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()

    # Preserve actual use
    actual_use = preserve_actual_use(html)

    # Parse existing KOL stats from HTML (fallback for failed scrapes)
    existing_data = parse_existing_kol_data(html)

    # Build new KOL_DATA array
    entries = []
    for username in KOL_METADATA.keys():
        link = KOL_LINKS.get(username, '')
        entry = build_kol_entry(username, scrape_data, link, existing_data)
        entries.append(entry)

    new_kol_data = "const KOL_DATA = [\n" + ",\n".join(entries) + "\n];"

    # Replace KOL_DATA in HTML
    pattern = r'const\s+KOL_DATA\s*=\s*\[[\s\S]*?\];'
    html = re.sub(pattern, new_kol_data, html, count=1)

    # Restore actual use
    html = re.sub(
        r'const\s+CAMPAIGN_ACTUAL_USE_DEFAULT\s*=\s*[\d.]+',
        f'const CAMPAIGN_ACTUAL_USE_DEFAULT = {actual_use}',
        html
    )

    # Write HTML
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Dashboard updated: {html_file}")
    print(f"KOLs updated: {len(entries)}")
    print(f"Scraped data injected: {len(scrape_data)} KOL(s)")
    print(f"Actual Use preserved: {actual_use:,.0f}")


if __name__ == '__main__':
    main()
