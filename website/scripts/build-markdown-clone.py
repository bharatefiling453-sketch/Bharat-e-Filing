"""
Builds a Markdown file that renders as an EXACT clone of a page (for the Discord → parallel-site blog pipeline).

Line 1 is "# <Title>" as the pipeline requires; everything after it is the page's own HTML (styles, fonts, scripts,
schema, body) as ONE raw-HTML block, so a CommonMark renderer (marked, markdown-it with html:true, remark/rehype-raw,
Python-Markdown) passes it through untouched:
  - every line is dedented (4+ leading spaces would otherwise become a code block) — HTML/CSS/JS ignore the indent;
  - blank lines are removed (a blank line ends a raw-HTML block);
  - the block is wrapped in one <div>, and the Markdown "# Title" heading is hidden by CSS so the page shows the
    designed H1 only (no extra space, no duplicate heading).
<head>-only tags (title, meta, canonical, Open Graph) cannot live in Markdown; they are printed for the Discord message.

Usage: python3 scripts/build-markdown-clone.py <dist-html> <out-md>
"""
import html as H
import re
import sys

src, out = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
head, body = s.split("<body", 1)
body_attrs, body = body.split(">", 1)
body = body.rsplit("</body>", 1)[0]

h1 = re.search(r'<h1 id="page-title"[^>]*>(.*?)</h1>', body, re.S).group(1)
title_text = H.unescape(re.sub(r"<[^>]+>", "", h1)).strip()

keep = [m.group(0) for m in re.finditer(r"<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>", head, re.S)]
service = re.search(r'data-service="([^"]*)"', body_attrs)
hide_md_h1 = '<style>h1:not(#page-title){display:none!important}</style>'
set_service = f'<script>document.body.dataset.service="{service.group(1)}";</script>' if service else ""

block = "\n".join([f'<div class="bef-md-clone">', hide_md_h1, set_service, *keep, body, "</div>"])
lines = [ln.strip() for ln in block.splitlines()]
block = "\n".join(ln for ln in lines if ln)
assert "\n\n" not in block

open(out, "w", encoding="utf-8").write(f"# {title_text}\n\n{block}\n")

meta = {
    "title": re.search(r"<title>(.*?)</title>", head, re.S).group(1).strip(),
    "description": re.search(r'name="description"\s+content="([^"]*)"', head).group(1),
    "canonical": re.search(r'rel="canonical" href="([^"]*)"', head).group(1),
    "og:image": re.search(r'property="og:image" content="([^"]*)"', head).group(1),
}
print(f"wrote {out} ({len(open(out, encoding='utf-8').read()) // 1024} KB), first line: # {title_text}")
for k, v in meta.items():
    print(f"{k}: {H.unescape(v)}")
