from pathlib import Path
from urllib.parse import quote
import json, re, html

ROOT = Path(__file__).resolve().parent
IMGDIR = ROOT / 'images' / 'products'
PRODUCTDIR = ROOT / 'products'
PRODUCTDIR.mkdir(exist_ok=True)

# Factory image filenames are the source of truth for product/model names.
# Image notes such as 合成 (composite), 所有颜色 (all colors), and copy suffixes are removed from the displayed model.
def clean_model(filename: str) -> str:
    stem = Path(filename).stem
    stem = re.sub(r'\s*合成$', '', stem)
    stem = re.sub(r'\s+所有颜色$', '', stem)
    stem = re.sub(r'\s+\(\d+\)$', '', stem)
    stem = re.sub(r'^SKL\s+', '', stem, flags=re.I)
    return stem.strip()

def slugify(model: str) -> str:
    s = model.lower().strip()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    s = s.strip('-')
    return s or 'product'

def series_for(model: str) -> str:
    u = model.upper()
    if u.startswith('H') and re.match(r'^H\d', u): return 'H Series'
    if u.startswith('FP') and re.match(r'^FP\d', u): return 'FP Series'
    if u.startswith('P') and re.match(r'^P\d', u): return 'P Series'
    return 'Other Models'

def category_for(model: str) -> str:
    u = model.upper()
    if u.startswith('H') and re.match(r'^H\d', u): return 'Bolt Seal Series'
    if u.startswith('FP') and re.match(r'^FP\d', u): return 'Plastic Seal Series'
    if u.startswith('P') and re.match(r'^P\d', u): return 'Security Seal Series'
    if u.startswith('RF'): return 'Meter Seal Series'
    if u.startswith('M'): return 'Metal Seal Series'
    return 'Security Seal Series'

def sort_key(model: str):
    series_order = {'H Series':0,'FP Series':1,'P Series':2,'Other Models':3}
    return (series_order[series_for(model)], model.upper())

jpgs = [p for p in IMGDIR.iterdir() if p.is_file() and p.suffix.lower() in {'.jpg','.jpeg'}]
# Group multiple factory photographs of the same model (e.g. H002) into one product page/gallery.
groups = {}
for p in jpgs:
    model = clean_model(p.name)
    groups.setdefault(model, []).append(p.name)

products = []
for model, image_names in sorted(groups.items(), key=lambda kv: sort_key(kv[0])):
    slug = slugify(model)
    title = f'SKL {model}' if not model.upper().startswith('SKL ') else model
    series = series_for(model)
    category = category_for(model)
    primary = image_names[0]
    # Prefer the plain model image over annotated/copy variants when available.
    for name in image_names:
        if clean_model(name) == Path(name).stem.replace('SKL ', ''):
            primary = name
            break
    # H002 plain image is especially clean for the card; its extra references remain in gallery.
    if model.upper() == 'H002' and 'H002.jpg' in image_names:
        primary = 'H002.jpg'
    desc = (
        f'Factory model {model} from the SKL security seal catalog. '
        'Open the product page to view the supplied factory image and request current verified specifications.'
    )
    products.append({
        'id': slug,
        'model': model,
        'title': title,
        'series': series,
        'category': category,
        'description': desc,
        'image': f'images/products/{quote(primary)}',
        'images': [f'images/products/{quote(n)}' for n in image_names],
        'sourceNames': image_names,
        'detailPage': f'products/{slug}.html',
    })

# Write products.js
with open(ROOT/'products.js','w',encoding='utf-8') as f:
    f.write('// Auto-generated from the JPG filenames in images/products.\n')
    f.write('// The image filename is treated as the factory model source of truth.\n')
    f.write('const products = ')
    json.dump(products, f, ensure_ascii=False, indent=2)
    f.write(';\n')

# Related products: same series first, then neighboring catalog entries.
def related_for(i):
    p = products[i]
    same = [x for j,x in enumerate(products) if j != i and x['series'] == p['series']]
    others = [x for j,x in enumerate(products) if j != i and x['series'] != p['series']]
    return (same + others)[:3]

for i,p in enumerate(products):
    imgs = p['images']
    source_names = p['sourceNames']
    hero_img = '../' + imgs[0]
    thumb_html = ''
    if len(imgs) > 1:
        thumb_html = '<div class="detail-thumbnails" aria-label="Product image gallery">' + ''.join(
            f'<button class="detail-thumb{" active" if j==0 else ""}" type="button" data-image="../{src}" data-full="../{src}" aria-label="View image {j+1}"><img src="../{src}" alt="{html.escape(p["title"])} factory view {j+1}"></button>'
            for j,src in enumerate(imgs)
        ) + '</div>'
    source_rows = ''.join(
        f'<li><code>{html.escape(n)}</code></li>' for n in source_names
    )
    related_cards = ''.join(
        f'''<a class="related-product-card" href="../{r['detailPage']}">
          <div class="related-product-image"><img src="../{r['image']}" alt="{html.escape(r['title'])}"></div>
          <span>{html.escape(r['series'])}</span>
          <strong>{html.escape(r['title'])}</strong>
        </a>'''
        for r in related_for(i)
    )
    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{html.escape(p['title'])} factory product page from SKL Security Seals.">
  <title>{html.escape(p['title'])} | SKL Security Seals</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../styles.css">
</head>
<body class="product-detail-page">
  <header class="site-header detail-header">
    <div class="container nav-wrap">
      <a class="brand" href="../index.html#top" aria-label="SKL home">
        <span class="brand-mark">SKL</span>
        <span class="brand-text"><strong>Security Seals</strong><small>Factory product catalog</small></span>
      </a>
      <nav class="main-nav detail-nav" aria-label="Product navigation">
        <a href="../index.html#products">All Products</a>
        <a href="../index.html#about">About</a>
        <a class="nav-cta" href="../index.html?product={quote(p['id'])}#contact">Request a Quote</a>
      </nav>
    </div>
  </header>

  <main>
    <section class="product-detail-hero">
      <div class="container">
        <div class="product-breadcrumb"><a href="../index.html">Home</a><span>→</span><a href="../index.html#products">Products</a><span>→</span><strong>{html.escape(p['model'])}</strong></div>
        <div class="product-detail-grid">
          <div class="detail-media-wrap">
            <div class="detail-product-visual">
              <img id="mainProductImage" class="detail-main-image" src="{hero_img}" alt="{html.escape(p['title'])} factory product image">
            </div>
            {thumb_html}
            <a id="fullImageLink" class="view-full-image" href="{hero_img}" target="_blank" rel="noopener">Open full factory image ↗</a>
          </div>
          <div class="detail-product-copy">
            <span class="detail-category">{html.escape(p['series'])}</span>
            <h1>{html.escape(p['model'])}</h1>
            <p class="detail-model">Factory model · {html.escape(p['title'])}</p>
            <p class="detail-intro">This page uses the actual factory JPG supplied for model <strong>{html.escape(p['model'])}</strong>. Contact SKL for the current verified dimensions, material, color availability, marking options, MOQ, packing details and pricing before ordering.</p>
            <div class="detail-actions">
              <a class="button button-primary" href="../index.html?product={quote(p['id'])}#contact">Request a Quote</a>
              <a class="button detail-back-button" href="../index.html#products">Back to Products</a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="product-detail-body">
      <div class="container detail-content-stack">
        <section class="detail-section product-info-section">
          <div class="detail-section-heading"><span>PRODUCT INFORMATION</span><h2>Factory catalog reference</h2></div>
          <div class="product-info-grid">
            <div><span>Model</span><strong>{html.escape(p['model'])}</strong></div>
            <div><span>Catalog group</span><strong>{html.escape(p['series'])}</strong></div>
            <div><span>Product family</span><strong>{html.escape(p['category'])}</strong></div>
            <div><span>Factory images</span><strong>{len(imgs)} supplied</strong></div>
          </div>
        </section>

        <section class="detail-section source-image-section">
          <div class="detail-section-heading"><span>FACTORY SOURCE</span><h2>Original image file reference</h2></div>
          <div class="source-file-content">
            <p>The product name on this page is derived from the supplied factory image filename. Image notes such as “composite”, “all colors”, or duplicate-copy numbers are kept in the source filename but removed from the displayed model code.</p>
            <ul>{source_rows}</ul>
          </div>
        </section>

        <section class="quick-details-card">
          <span class="quick-label">BEFORE QUOTING</span>
          <h2>Confirm the production specification with SKL.</h2>
          <p>Some supplied images include dimensional drawings or visual variants, but this website does not invent missing technical specifications. Use the quote form to confirm the exact current specification for this model.</p>
          <a class="button button-dark" href="../index.html?product={quote(p['id'])}#contact">Ask about {html.escape(p['model'])}</a>
        </section>

        <section class="related-products-section">
          <div class="detail-section-heading related-heading"><span>CONTINUE BROWSING</span><h2>Related factory models</h2></div>
          <div class="related-products-grid">{related_cards}</div>
        </section>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="container footer-grid">
      <div><a class="brand footer-brand" href="../index.html#top"><span class="brand-mark">SKL</span><span class="brand-text"><strong>Security Seals</strong><small>Factory product catalog</small></span></a></div>
      <div class="footer-links"><a href="../index.html#products">Products</a><a href="../index.html#about">About</a><a href="../index.html#contact">Contact</a></div>
      <p class="copyright">© <span class="detail-year"></span> SKL Security Seals.</p>
    </div>
  </footer>
  <script>
    document.querySelectorAll('.detail-year').forEach(el => el.textContent = new Date().getFullYear());
    const mainImage = document.getElementById('mainProductImage');
    const fullImageLink = document.getElementById('fullImageLink');
    document.querySelectorAll('.detail-thumb').forEach(btn => btn.addEventListener('click', () => {{
      document.querySelectorAll('.detail-thumb').forEach(x => x.classList.remove('active'));
      btn.classList.add('active');
      mainImage.src = btn.dataset.image;
      fullImageLink.href = btn.dataset.full;
    }}));
  </script>
</body>
</html>'''
    (PRODUCTDIR/f"{p['id']}.html").write_text(page,encoding='utf-8')

# Remove old numeric placeholder pages that no longer represent factory models.
for old in PRODUCTDIR.glob('product-*.html'):
    old.unlink()

# README
readme=f'''# SKL Security Seals — Factory Product Catalog\n\nThis build uses the JPG filenames in `images/products/` as the source of truth for factory product/model names.\n\n- **{len(products)} individual product pages** are generated in `products/`.\n- Every product card on `index.html` uses a real factory image.\n- Clicking **View product** opens that model's dedicated detail page.\n- Multiple photos of the same model are grouped into one gallery (for example, H002).\n- The non-JPG file `未标题-2.png` is intentionally not treated as a factory-named product because the request specified JPG product names and that filename is not a model code.\n- Missing technical specifications are **not invented**. The detail pages ask the buyer to confirm current specifications with SKL.\n\n## Add a new product later\n1. Put a correctly named `.jpg` or `.JPG` in `images/products/`.\n2. Run `python3 build_catalog.py`.\n3. The catalog data and individual product page will be regenerated.\n\nOpen `index.html` with VS Code Live Server for local preview.\n'''
(ROOT/'README.md').write_text(readme,encoding='utf-8')
print(f'Generated {len(products)} product pages from {len(jpgs)} JPG files.')
