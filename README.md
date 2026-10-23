# Chris' Teaching Tools — kreyzkai.github.io

Static GitHub Pages site: browser-only classroom game and worksheet generators.
No build step, no framework, no server. Every tool is a standalone HTML file.

## Layout

```
index.html                              ← launcher / index page (the tiles)
001 … 030 *.html                        ← one numbered file per live index tile
031 COMET Basic Note Hub.html           ← password-gated hub for the COMET packs
999 Under construction.html             ← placeholder tile
028 IELTS Academic Quest/               ← project 028, self-contained
   028 IELTS Academic Quest.html        ←   the app (audio + PDFs link relatively)
   028-script-*.mp3                    ←   11 audio tracks
   IELTS Quest *.pdf                   ←   5 printable A4 packs
   028 IELTS Quest Print Pack.zip      ←   rebuilt by build-packs.sh
   028 IELTS Offline Study Pack.zip
   build-packs.sh, README-028.txt, README-OFFLINE.txt
028 IELTS Listening Speaking Reviewer.html  ← REDIRECT STUB — do not delete (see below)
comets/                                 ← the 5 gated textbook packs (031–035)
_archive/                               ← unlaunched / superseded HTML (never published)
tools/check-links.py                    ← link checker
```

`_archive/` is skipped by Jekyll (leading underscore), so nothing in it is published.
`comets/` *is* published but intentionally not linked from the index — it is only
reachable through the gated hub.

## Naming convention

Every live tile is `NNN Title Case Name.html`, where `NNN` is the number shown on
its card in `index.html`. No underscores, no `(1)`, no `test` / `standalone`,
no extension-case drift. The card badge and the filename number must agree.

Adding a project: create `NNN Title Case Name.html`, add the tile to `index.html`
with the same number, then run `python3 tools/check-links.py`.

## ⚠ The 028 redirect stub

`028 IELTS Listening Speaking Reviewer.html` at the repository root is **not** the
IELTS app. It is a redirect page kept for one reason: **21 QR codes already printed
in the IELTS PDFs** point at that exact URL, e.g.

```
https://kreyzkai.github.io/028%20IELTS%20Listening%20Speaking%20Reviewer.html#mission1
```

14 in `IELTS Quest Mission Sheets.pdf`, 6 on the `Mini Workbook` cover, 1 in
`Test Day Journey.pdf`. The stub forwards the path *and* the `#hash` to the new
folder. The PDFs are prebuilt ReportLab output with no generator script in this
repo, so the QR URLs cannot be reissued here. Keep the stub until every printed
handout is out of circulation.

## Scripts

```bash
python3 tools/check-links.py                 # every local href/src must resolve
bash "028 IELTS Academic Quest/build-packs.sh"   # rebuild both download ZIPs
```

## Credits

Built by CMarasigan for Tokyo Metropolitan Kasai-Minami High School. Educational
material only; the IELTS packs are unofficial and not affiliated with IELTS,
British Council, IDP or Cambridge.
