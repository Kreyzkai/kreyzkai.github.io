#!/usr/bin/env python3
"""
Repository link checker for kreyzkai.github.io

Verifies that every local (non-http, non-data, non-mailto) href/src in the site's
HTML actually resolves on disk, and that every numbered project referenced by
index.html exists with a matching number.

Usage:  python3 tools/check-links.py
Exit code 0 = clean, 1 = broken links found.
"""
import os
import re
import sys
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", "_archive", "tools"}

ATTR = re.compile(r'(?:href|src)="([^"]+)"', re.I)


def walk_html():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in filenames:
            if f.lower().endswith((".html", ".htm")):
                yield os.path.join(dirpath, f)


def is_local(url):
    u = url.strip()
    # Skip template-literal fragments that only look like paths, e.g. inside a
    # generated string: src="' + card.image + '"  or  src="\${item.img}"
    if u.startswith("\\'") or "' +" in u or '" +' in u:
        return False
    return not (u.startswith(("http://", "https://", "//", "data:", "mailto:",
                              "javascript:", "#", "tel:")) or "${" in u
                or u.startswith("'") or u.startswith("/_sdk"))


def main():
    broken, checked = [], 0
    for path in walk_html():
        rel = os.path.relpath(path, ROOT)
        with open(path, encoding="utf-8", errors="ignore") as fh:
            html = fh.read()
        for raw in ATTR.findall(html):
            if not is_local(raw):
                continue
            target = urllib.parse.unquote(raw.split("#")[0].split("?")[0]).strip()
            if not target:
                continue
            checked += 1
            resolved = os.path.normpath(os.path.join(os.path.dirname(path), target))
            if not os.path.exists(resolved):
                broken.append((rel, raw))

    print(f"Checked {checked} local links across {len(list(walk_html()))} HTML files.")

    # index.html must reference exactly the numbered projects, and each number
    # must be a real file at the repository root.
    index = os.path.join(ROOT, "index.html")
    with open(index, encoding="utf-8") as fh:
        ih = fh.read()
    tiles = re.findall(r'<a href="([^"]+)">.*?<div class="number">([^<]*)</div>',
                       ih, re.S)
    print(f"index.html: {len(tiles)} tiles")
    for href, num in tiles:
        if href.startswith("http"):
            continue
        base = os.path.basename(href)
        if num.strip().isdigit() and num.strip() != "999":
            if not base.startswith(num.strip()):
                print(f"  NUMBER MISMATCH: tile {num} -> {base}")

    if broken:
        print("\nBROKEN LOCAL LINKS:")
        for src, target in broken:
            print(f"  {src}  ->  {target}")
        return 1
    print("\nAll local links resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
