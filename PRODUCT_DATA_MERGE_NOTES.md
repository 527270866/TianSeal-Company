# Product Information Merge Notes

Source: `product information -all.xlsx` supplied by the user.

Only exact model-code matches were merged. Existing website values were preserved when the spreadsheet was missing the model or when a value conflicted with an existing website value. Spreadsheet-only technical fields were added as additional specification cards.

- Website product models: 32
- Exact spreadsheet matches merged: 18
- Website models left unchanged because no exact spreadsheet model was found: 14

## Exact matches merged
DP001, FP004, FP005, FP006, FP006-1, FP007, FP008, H002, H002-1, H003, H004, H008, L004, M001, MS004-1, P001, P015-1, YP001

## Website models left unchanged
CS005, FP001, FP002, FP003, FP010, FP011, H002-6, H009, H010, P006, P014, P015, RF001, YP001-1

## Preserved conflicts
- FP006-1 — Packing/Carton Size: website kept `350 × 230 × 255 mm`; spreadsheet value `560 × 400 × 360mm` was not used to overwrite it.
- H004 — Min. Order: website kept `5,000 PCS`; spreadsheet value `50,000 PCS` was not used to overwrite it.
- H004 — Packing/Carton Size: website kept `435 × 327 × 163 mm (250 PCS)`; spreadsheet value `345 × 300 × 275 mm` was not used to overwrite it.
- YP001 — Packing/Carton Size: website kept `590 × 415 × 420 mm`; spreadsheet value `570 × 280 × 250 mm` was not used to overwrite it.

## 2026 special-sourcing catalog expansion

The supplied `product information -all.numbers` workbook was reviewed again against the current website catalog.

- Unique workbook models: 58
- Existing website models matched: 18
- Workbook-only models added as Special Sourcing: 40
- New total catalog size: 72

Workbook-only products are intentionally not described as Tianseal factory-manufactured models. They are labeled as special-sourcing items, and their pages state that manufacturing source, availability, MOQ, lead time, packing, and final specifications must be confirmed before quotation.

See `SPECIAL_SOURCING_PRODUCTS.md` for the complete added-model list.
