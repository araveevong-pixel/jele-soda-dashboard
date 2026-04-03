#!/usr/bin/env python3
"""
JELE SODA 2026 — TikTok Scraper
Scrape views, likes, shares, comments, saves, followers from TikTok video links.
Usage: python3 scripts/tiktok_scraper.py [output_json]
"""

import json
import sys
import re
import time
import random

try:
    import requests
except ImportError:
    print("Installing requests...")
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests', '-q'])
    import requests

# ============================================================
#  KOL LINKS — เพิ่มลิงก์ใหม่เมื่อ KOL โพสต์
# ============================================================
KOL_LINKS = {
    # Main (5)
    'biw_songkran': '',
    'fasin22052545': '',
    'ovapachannel': '',
    'nophuwanet': '',
    'tkpst2': '',
    # Micro - ภาคกลาง (15)
    'plugsweden': '',
    'pakkaput17': '',
    'kuanpuantiew': '',
    'pexjakkajee': '',
    'puwanaipison': '',
    'saokrungthep': '',
    'll0499': '',
    'pooliepraew': '',
    'f_u_i_': '',
    'tan_slaz19': '',
    'armgoodsunday': '',
    'pupemaipriaw': '',
    'jekkabot5555': '',
    'lenpaither': '',
    'bosck999': '',
    # Micro - ภาคเหนือ (4)
    'gotarm65': '',
    'tikbadai': '',
    'patpaladmuang': '',
    'coochamp': '',
    # Micro - ภาคอีสาน (6)
    'aodbom2': '',
    'wootza5555': '',
    'bookteerapat': '',
    'juno55555': '',
    'biggesttha': '',
    'apirak2539ice': '',
    # Micro - ภาคใต้ (3)
    'royver_th': '',
    'bunyaporn_2009': '',
    'thebellchanel': '',
    # Mixology (14)
    'kayshomebar': '',
    'raa_reun_core': '',
    'maxk_litt': '',
    'maoaowfeel': '',
    'how.to.mao': '',
    'arpo_story': '',
    'yod_121098': '',
    'tatatomang': '',
    'taloncamp_sg': '',
    'gowithgoldd': '',
    'maww_shabu': '',
    'tenitbrk': '',
    'biibuaaastory': '',
    'snicker_nts': '',
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9,th;q=0.8',
}


def resolve_short_url(short_url, timeout=10):
    """Resolve vt.tiktok.com short URLs to full URLs."""
    try:
        resp = requests.head(short_url, headers=HEADERS, allow_redirects=True, timeout=timeout)
        return resp.url
    except Exception:
        return short_url


def scrape_tiktok_video(url, timeout=15):
    """Scrape metrics from a TikTok video page."""
    try:
        if 'vt.tiktok.com' in url:
            url = resolve_short_url(url)

        resp = requests.get(url, headers=HEADERS, timeout=timeout)
        html = resp.text

        data = {
            'url': url,
            'views': 0,
            'likes': 0,
            'shares': 0,
            'comments': 0,
            'saves': 0,
            'followers': 0,
        }

        # Try JSON-LD / SIGI_STATE / UNIVERSAL_DATA
        json_patterns = [
            r'"playCount"\s*:\s*(\d+)',
            r'"diggCount"\s*:\s*(\d+)',
            r'"shareCount"\s*:\s*(\d+)',
            r'"commentCount"\s*:\s*(\d+)',
            r'"collectCount"\s*:\s*(\d+)',
            r'"followerCount"\s*:\s*(\d+)',
        ]
        keys = ['views', 'likes', 'shares', 'comments', 'saves', 'followers']

        for pattern, key in zip(json_patterns, keys):
            m = re.search(pattern, html)
            if m:
                data[key] = int(m.group(1))

        return data

    except Exception as e:
        print(f"  Error scraping {url}: {e}")
        return None


def main():
    output_file = sys.argv[1] if len(sys.argv) > 1 else 'scrape_results.json'

    results = {}
    active_kols = {k: v for k, v in KOL_LINKS.items() if v.strip()}

    if not active_kols:
        print("No KOL links to scrape. Output empty results.")
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        return

    print(f"Scraping {len(active_kols)} KOL(s)...")

    for username, link in active_kols.items():
        print(f"  Scraping @{username}...")
        data = scrape_tiktok_video(link)
        if data:
            results[username] = data
            print(f"    Views: {data['views']:,} | Likes: {data['likes']:,} | Shares: {data['shares']:,}")
        else:
            print(f"    Failed to scrape @{username}")

        # Rate limiting
        time.sleep(random.uniform(1, 3))

    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\nResults saved to {output_file}")
    print(f"Successfully scraped: {len(results)}/{len(active_kols)}")


if __name__ == '__main__':
    main()
