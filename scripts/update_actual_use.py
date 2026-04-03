#!/usr/bin/env python3
"""
JELE SODA 2026 — Update Actual Use
Update CAMPAIGN_ACTUAL_USE_DEFAULT value in HTML dashboard.
Usage: python3 scripts/update_actual_use.py <amount> <html_file>
Example: python3 scripts/update_actual_use.py 250000 index.html
"""

import sys
import re


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 scripts/update_actual_use.py <amount> <html_file>")
        print("Example: python3 scripts/update_actual_use.py 250000 index.html")
        sys.exit(1)

    amount = float(sys.argv[1])
    html_file = sys.argv[2]

    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()

    old_match = re.search(r'const\s+CAMPAIGN_ACTUAL_USE_DEFAULT\s*=\s*([\d.]+)', html)
    old_value = float(old_match.group(1)) if old_match else 0

    html = re.sub(
        r'const\s+CAMPAIGN_ACTUAL_USE_DEFAULT\s*=\s*[\d.]+',
        f'const CAMPAIGN_ACTUAL_USE_DEFAULT = {amount}',
        html
    )

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Actual Use updated: {old_value:,.0f} → {amount:,.0f}")
    print(f"File: {html_file}")


if __name__ == '__main__':
    main()
