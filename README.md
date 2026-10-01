# Tianseal International Inc — Product Catalog Website

This build now combines the existing Tianseal factory catalog with the supplied `product information -all.numbers` product-information workbook.

- **72 product models** are shown in the shared catalog.
- **32 existing/regular website models** are preserved.
- **40 additional lower-trade models** from the supplied workbook are included as **Special Sourcing** items.
- Special-sourcing items use the supplied catalog images and reference specifications, but the website clearly states that current manufacturing source, availability, MOQ, packing, lead time, and final specifications must be confirmed before quotation.
- English, Simplified Chinese, and Spanish detail pages are included for all 40 new special-sourcing items.
- Existing product pages and manually preserved specification conflicts remain unchanged.

## Special-sourcing wording

Products that were not previously shown on the website are not presented as Tianseal factory-manufactured items. They are labeled **Special Sourcing / Available by Request**. This is intended to be commercially appropriate while accurately reflecting that these models may be procured through Tianseal's supply network and have had lower trading volume this year.

## Important maintenance note

`build_catalog.py` is the older factory-image generator. Running it by itself will rebuild `products.js` only from factory JPG filenames and can remove the special-sourcing catalog entries. Preserve the current `products.js`, special product pages, and `images/products/special/` directory when making future catalog changes.

Open `index.html` with VS Code Live Server for local preview.
