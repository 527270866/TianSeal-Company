#!/usr/bin/env python3
"""Validate discoverability, metadata and local link targets without network access."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, urljoin, unquote
import xml.etree.ElementTree as ET
import subprocess
from build_search import ROOT, LANGS, SITE_URL, generate

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.canonical, self.alternates, self.anchors, self.descriptions = [], {}, [], []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'link' and a.get('rel') == 'canonical': self.canonical.append(a['href'])
        if tag == 'link' and a.get('rel') == 'alternate':
            assert a['hreflang'] not in self.alternates, 'Duplicate language'
            self.alternates[a['hreflang']] = a['href']
        if tag == 'a' and 'href' in a: self.anchors.append(a['href'])
        if tag == 'meta' and a.get('name') == 'description': self.descriptions.append(a.get('content'))

origin = SITE_URL
assert not (ROOT / 'CNAME').exists(), 'Custom domain must be removed'
outputs = generate()
for path, expected in outputs.items():
    assert (ROOT / path).read_text() == expected, f'Stale: {path}'
urls = [el.text for el in ET.parse(ROOT / 'sitemap.xml').findall('.//{*}loc')]
assert len(urls) == len(set(urls)), 'Duplicate sitemap URLs'
expected_pages = {p for p in outputs if p.endswith('.html')}
assert len(urls) == len(expected_pages)
pages = {}
for url in urls:
    assert url.startswith(origin + '/') and not urlsplit(url).query
    relative = unquote(url[len(origin) + 1:])
    if not relative or relative.endswith('/'): relative += 'index.html'
    assert relative in expected_pages, f'Unknown sitemap target: {relative}'
    page = Page((ROOT / relative).read_text())
    assert page.canonical == [url], f'Canonical mismatch: {relative}'
    assert len(page.descriptions) == 1 and page.descriptions[0], relative
    assert set(page.alternates) == {'en', 'es', 'zh-CN', 'x-default'}, relative
    pages[url] = page
for url, page in pages.items():
    for lang, alternate in page.alternates.items():
        assert alternate in pages, f'Missing alternate: {alternate}'
        assert pages[alternate].alternates == page.alternates, f'Nonreciprocal languages: {url}'
# Every page must be reachable by real anchors from the English homepage, without JS.
seen, queue = set(), [origin + '/']
while queue:
    url = queue.pop()
    if url in seen: continue
    seen.add(url)
    for href in pages[url].anchors:
        dest = urlsplit(urljoin(url, href))
        path = dest.path
        if path.endswith('/index.html'): path = path[:-10]
        target = dest.scheme + '://' + dest.netloc + path
        if target in pages and target not in seen: queue.append(target)
assert set(pages) == seen, f'Orphan pages: {set(pages) - seen}'
# Critical identity files must match the recovered source byte for byte.
for path in ['google8be39db8c6f5e728.html']:
    original = subprocess.check_output(['git', 'show', '93b8b5c29c31b3c0784d9fa73b85a086016dc7c7:' + path], cwd=ROOT)
    assert (ROOT / path).read_bytes() == original, f'Identity file changed: {path}'
print(f'PASS: {len(pages)} canonical pages, reciprocal languages, sitemap coverage, no orphan pages, preserved identity files')
