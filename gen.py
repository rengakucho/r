#!/usr/bin/env python3
"""slugs.json から、スラグごとのリダイレクトページ（記事別OGP付き）を生成する。

使い方: python3 gen.py → <slug>/index.html を一括生成 → git commit & push
スラグ追加は slugs.json に1エントリ足して再実行するだけ。
ルートの index.html（?s= 形式の互換ルーター）はこのスクリプトでは触らない。
"""
import json
import os
import html

BASE = os.path.dirname(os.path.abspath(__file__))
LOG = "https://script.google.com/macros/s/AKfycbwRRC_LUTQJ8X_sw4cDqqjqYS88YEhU6AcC351CY-6fjAj1M8zlYc07wqxIEePdvxHBRQ/exec"
SITE = "https://rengakucho.github.io/r"

TEMPLATE = """<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex">
<title>{title}</title>
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="article">
<meta property="og:url" content="{site}/{slug}/">
<meta property="og:image" content="{site}/{image}">
<meta name="twitter:card" content="summary_large_image">
</head>
<body>
<p style="font-family:sans-serif;color:#666;">記事へ移動しています…</p>
<script>
(function () {{
  var dest = {dest_js};
  try {{ new Image().src = "{log}?s=" + encodeURIComponent("{slug}"); }} catch (e) {{}}
  setTimeout(function () {{ location.replace(dest); }}, 150);
  document.addEventListener("DOMContentLoaded", function () {{
    var a = document.createElement("a");
    a.href = dest;
    a.textContent = "自動で移動しない場合はこちら";
    document.body.appendChild(a);
  }});
}})();
</script>
<noscript><a href="{dest_attr}">続きはこちら</a></noscript>
</body>
</html>
"""


def main():
    slugs = json.load(open(os.path.join(BASE, "slugs.json")))
    for slug, meta in slugs.items():
        outdir = os.path.join(BASE, slug)
        os.makedirs(outdir, exist_ok=True)
        page = TEMPLATE.format(
            title=html.escape(meta["title"], quote=True),
            description=html.escape(meta.get("description", ""), quote=True),
            image=meta["image"],
            slug=slug,
            site=SITE,
            log=LOG,
            dest_js=json.dumps(meta["url"]),
            dest_attr=html.escape(meta["url"], quote=True),
        )
        with open(os.path.join(outdir, "index.html"), "w") as f:
            f.write(page)
        print(f"generated {slug}/index.html -> {meta['url']}")


if __name__ == "__main__":
    main()
