#!/usr/bin/env python3
"""Refresh search files without rebuilding or deleting catalog content. No dependencies."""
from pathlib import Path
import argparse
import html
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
LANGS = {'en': '', 'zh-CN': 'zh/', 'es': 'es/'}
DESCRIPTIONS = {
    'en': 'Explore Tianseal International Inc security seals: bolt seals, cable seals, plastic seals and meter seals. View product details and request a quote.',
    'zh-CN': '浏览 Tianseal International Inc 安全封条目录：高保封、钢丝封条、塑料封条和电表封条。查看产品详情并咨询报价。',
    'es': 'Explore los sellos de seguridad de Tianseal International Inc: sellos de perno, cable, plástico y medidor. Consulte los productos y solicite una cotización.',
}
LABELS = {'en': 'Browse all product models', 'zh-CN': '浏览全部产品型号', 'es': 'Ver todos los modelos de productos'}

def generate():
    host = (ROOT / 'CNAME').read_text().strip()
    if not re.fullmatch(r'[a-zA-Z0-9.-]+', host):
        raise ValueError('CNAME must contain a single domain')
    origin = 'https://' + host
    pages = sorted([ROOT / (p + 'index.html') for p in LANGS.values()] +
                   [f for p in LANGS.values() for f in (ROOT / p / 'products').glob('*.html')])
    paths = {p.relative_to(ROOT).as_posix() for p in pages}
    def url(path):
        return origin + '/' + (path[:-10] if path.endswith('index.html') else path)
    outputs = {}
    for page in pages:
        path = page.relative_to(ROOT).as_posix()
        lang, prefix = next(((l, p) for l, p in LANGS.items() if p and path.startswith(p)), ('en', ''))
        equivalent = path[len(prefix):]
        source = page.read_text(encoding='utf-8')
        # Replace only metadata we own, preserving body, title, and product descriptions.
        source = re.sub(r'  <!-- search metadata -->\n.*?  <!-- /search metadata -->\n', '', source, flags=re.S)
        source = re.sub(r'^[ \t]*<link\b[^>]*\brel=["\'](?:alternate|canonical)["\'][^>]*>\s*\n', '', source, flags=re.M)
        links = [f'  <link rel="canonical" href="{url(path)}">']
        for other, pre in LANGS.items():
            if pre + equivalent in paths:
                links.append(f'  <link rel="alternate" hreflang="{other}" href="{url(pre + equivalent)}">')
        if equivalent in paths:
            links.append(f'  <link rel="alternate" hreflang="x-default" href="{url(equivalent)}">')
        source = source.replace('</head>', '  <!-- search metadata -->\n' + '\n'.join(links) + '\n  <!-- /search metadata -->\n</head>')
        if equivalent == 'index.html':
            source = re.sub(r'<meta name="description" content="[^"]*"\s*/?>',
                            '<meta name="description" content="' + html.escape(DESCRIPTIONS[lang], quote=True) + '" />', source)
            # Native details keeps a compact UI and real links available without JavaScript.
            source = re.sub(r'\n        <!-- product directory -->.*?<!-- /product directory -->', '', source, flags=re.S)
            items = []
            for product in sorted((ROOT / prefix / 'products').glob('*.html')):
                text = product.read_text(encoding='utf-8')
                model = re.search(r'<h1[^>]*>(.*?)</h1>', text, re.S)
                name = re.sub('<[^>]+>', '', model.group(1)) if model else product.stem
                items.append(f'            <li><a href="products/{product.name}">{html.escape(html.unescape(name))}</a></li>')
            directory = '\n        <!-- product directory -->\n        <details class="product-directory">\n          <summary>' + LABELS[lang] + '</summary>\n          <ul>\n' + '\n'.join(items) + '\n          </ul>\n        </details>\n        <!-- /product directory -->'
            marker = '<div class="product-grid" id="productGrid" aria-live="polite"></div>'
            if marker not in source:
                raise ValueError(f'Product grid missing in {path}')
            source = source.replace(marker, marker + directory)
        outputs[path] = source
    ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    ns = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
    sitemap = ET.Element(ns + 'urlset')
    for path in sorted(paths):
        ET.SubElement(ET.SubElement(sitemap, ns + 'url'), ns + 'loc').text = url(path)
    ET.indent(sitemap, space='  ')
    outputs['sitemap.xml'] = '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(sitemap, encoding='unicode') + '\n'
    outputs['robots.txt'] = f'User-agent: *\nAllow: /\n\nSitemap: {origin}/sitemap.xml\n'
    return outputs

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if generated files are stale; write nothing')
    args = parser.parse_args()
    outputs = generate()
    changed = [p for p, text in outputs.items() if not (ROOT / p).exists() or (ROOT / p).read_text(encoding='utf-8') != text]
    if args.check and changed:
        raise SystemExit('Stale search files: ' + ', '.join(changed))
    if not args.check:
        for path in changed:
            (ROOT / path).write_text(outputs[path], encoding='utf-8')
    print(f'{len(outputs) - 2} pages; {len(changed)} files ' + ('stale' if args.check else 'updated'))

if __name__ == '__main__':
    main()
