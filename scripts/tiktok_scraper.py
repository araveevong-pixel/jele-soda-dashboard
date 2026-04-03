#!/usr/bin/env python3
"""
JELE SODA 2026 — TikTok Scraper (yt-dlp)
Scrape views, likes, shares, comments, saves, followers from TikTok video links.
Uses yt-dlp for reliable JSON metadata extraction.
Usage: python3 scripts/tiktok_scraper.py [output_json]
"""

import json
import sys
import subprocess
import time
import random

# ============================================================
#  KOL LINKS — เพิ่มลิงก์ใหม่เมื่อ KOL โพสต์
# ============================================================
KOL_LINKS = {
    # Main (5)
    'biw_songkran': 'https://vt.tiktok.com/ZSm7UqSxm/',
    'fasin22052545': 'https://vt.tiktok.com/ZSmcaAb2h/',
    'ovapachannel': 'https://vt.tiktok.com/ZSmcm17pD/',
    'nophuwanet': 'https://vt.tiktok.com/ZSHdU6PSb/',
    'tkpst2': 'https://vt.tiktok.com/ZSuG2hcdu/',
    # Micro - ภาคกลาง (15)
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
    # Micro - ภาคเหนือ (4)
    'gotarm65': 'https://vt.tiktok.com/ZSm7MXU59/',
    'tikbadai': 'https://vt.tiktok.com/ZSmcW2HWK/',
    'patpaladmuang': 'https://vt.tiktok.com/ZSmcaqqea/',
    'coochamp': 'https://vt.tiktok.com/ZSuY8vRRb/',
    # Micro - ภาคอีสาน (6)
    'aodbom2': 'https://vt.tiktok.com/ZSuYMrAnR/',
    'wootza5555': 'https://vt.tiktok.com/ZSuYhbTuQ/',
    'bookteerapat': 'https://vt.tiktok.com/ZSunNhY3V/',
    'juno55555': 'https://vt.tiktok.com/ZSubjckjm/',
    'biggesttha': 'https://vt.tiktok.com/ZSuasTfRG/',
    'apirak2539ice': 'https://vt.tiktok.com/ZSuGpLFHg/',
    # Micro - ภาคใต้ (3)
    'royver_th': 'https://vt.tiktok.com/ZSuY89A6a/',
    'bunyaporn_2009': 'https://vt.tiktok.com/ZSumseLjA/',
    'thebellchanel': 'https://vt.tiktok.com/ZSumN9avE/',
    # Mixology (14)
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


def scrape_tiktok_video(url, timeout=60):
    """Extract TikTok video metadata using yt-dlp --dump-json."""
    try:
        result = subprocess.run(
            ['yt-dlp', '--dump-json', '--no-download', '--no-warnings', url],
            capture_output=True, text=True, timeout=timeout
        )

        if result.returncode != 0:
            print(f"    yt-dlp error: {result.stderr.strip()[:200]}")
            return None

        info = json.loads(result.stdout)

        # Debug: dump all keys containing 'count', 'save', 'collect', 'favorite', 'bookmark'
        debug_keys = {k: v for k, v in info.items()
                      if any(word in k.lower() for word in ['count', 'save', 'collect', 'favorite', 'bookmark'])}
        if debug_keys:
            print(f"    [DEBUG] Available count fields: {debug_keys}")

        data = {
            'url': info.get('webpage_url', url),
            'views': info.get('view_count', 0) or 0,
            'likes': info.get('like_count', 0) or 0,
            'shares': info.get('repost_count', 0) or 0,
            'comments': info.get('comment_count', 0) or 0,
            'saves': (info.get('collect_count', 0)
                      or info.get('favorite_count', 0)
                      or info.get('bookmark_count', 0)
                      or info.get('save_count', 0)
                      or 0),
            'followers': info.get('channel_follower_count', 0) or 0,
        }

        return data

    except subprocess.TimeoutExpired:
        print(f"    Timeout scraping {url}")
        return None
    except json.JSONDecodeError as e:
        print(f"    JSON parse error: {e}")
        return None
    except Exception as e:
        print(f"    Error scraping {url}: {e}")
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

    print(f"Scraping {len(active_kols)} KOL(s) using yt-dlp...")

    for username, link in active_kols.items():
        print(f"  Scraping @{username}...")
        data = scrape_tiktok_video(link)
        if data:
            results[username] = data
            print(f"    Views: {data['views']:,} | Likes: {data['likes']:,} | "
                  f"Shares: {data['shares']:,} | Saves: {data['saves']:,} | "
                  f"Comments: {data['comments']:,}")
        else:
            print(f"    Failed to scrape @{username}")

        # Rate limiting — yt-dlp ไม่ต้อง delay มากเท่า requests
        time.sleep(random.uniform(0.5, 1.5))

    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\nResults saved to {output_file}")
    print(f"Successfully scraped: {len(results)}/{len(active_kols)}")


if __name__ == '__main__':
    main()
