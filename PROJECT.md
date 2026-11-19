# Tianseal Website & Search Visibility

## Scope and constraints
Recover and incrementally improve https://github.com/527270866/TianSeal-Company.
Preserve the existing design, content, product sourcing qualifications, Google
verification file and intended domain. Use free services and existing GitHub Pages;
no ads, paid APIs, SEO subscriptions, new hosting, or scheduled automation.
The distributor/importer lead-discovery app is a separate project and is untouched.

## Historical context
The previous “Configure GitHub Pages Domain SEO” chat reported successful HTML-file
verification for https://527270866.github.io/TianSeal-Company/ but poor Google
visibility. Historical assistant claims about CNAME removal were not treated as
current evidence. The recovered main commit is
93b8b5c29c31b3c0784d9fa73b85a086016dc7c7 and currently contains CNAME = tsseal.com.
Source was cloned from the independently recovered Desktop checkout into this
chat's work/TianSeal-Company directory; origin points to the public GitHub repository.

## Observations — November 18, 2026 (America/Los_Angeles)
- 72 product models, each with English, Spanish and Simplified Chinese pages;
  3 homepages: 219 content pages total. Google verification HTML is separate.
- No sitemap.xml or robots.txt in the recovered source. Their absence alone does
  not prohibit crawling. Missing canonicals and relative hreflang annotations were
  concrete opportunities to improve discovery and URL consistency.
- Product grid is JavaScript-populated. Static homepage links did not expose the
  full catalog directly. New native details directories expose all 72 models per
  language without requiring JavaScript, while keeping the page compact.
- Google DNS over HTTPS returned Status 3 (NXDOMAIN) for tsseal.com A and NS.
  Cloudflare independently returned Status 3 for tsseal.com A. The local resolver
  also failed for tsseal.com and www.tsseal.com. Registration/ownership/expiry
  cause is NOT established by DNS alone.
- Direct HTTPS HEAD to the GitHub Pages project URL returned 301 with Location:
  http://tsseal.com/. Thus the old public URL currently leads to the failing domain.
- Latest Pages workflow, run 37580991831, completed successfully for the recovered
  main commit. This proves a successful build/deploy job, not domain reachability.
- TLS and content on the custom domain cannot be verified while DNS is absent.
  Administrative Pages settings, Enforce HTTPS status and Search Console account
  state have not been inspected. No search index or ranking status is claimed.

## First increment
Prepared on branch seo/search-discovery-foundation:
- Dependency-free scripts/build_search.py; discovers actual existing pages without
  invoking the destructive legacy build_catalog.py or removing special-sourcing products.
- Sitemap of all 219 canonical content URLs; excludes verification HTML.
- robots.txt allows crawling and advertises the absolute sitemap URL.
- Self-canonicals and reciprocal absolute en/es/zh-CN/x-default annotations.
- More descriptive homepage metadata using existing product categories.
- Native expandable catalog links on each homepage; existing design assets unchanged.
- scripts/check_search.py checks full sitemap coverage, reciprocal annotations,
  canonical uniqueness, descriptions, static reachability and identity-file preservation.

Validation: generation followed by --check reports zero stale files; all 219 pages
pass the independent parser/graph checks; git diff --check passes. No browser
visual review or live deployment of these changes is claimed.

## Availability, ownership, discovery, crawling, indexing, ranking
Availability must be repaired first. Owning a repository or possessing an HTML
verification file does not confer access to Search Console. Sitemap and links aid
discovery; robots permits crawling; search engines independently decide indexing
and ranking. None of these code changes guarantees inclusion or a position.

## Canonical domain and live status
Canonical URLs currently follow the existing CNAME (https://tsseal.com/). This is
a preserved configuration, not proof that the domain is owned or operational.
Changes are prepared for review, not merged or live. Do not deploy and submit the
sitemap until the owner confirms the domain and DNS/HTTPS are working. Do not
silently remove CNAME or change DNS. If free github.io hosting is chosen instead,
update domain/path handling and canonical URLs together before deployment.

## Official references checked
- Google sitemaps: https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- Google language annotations: https://developers.google.com/search/docs/specialty/international/localized-versions
- Search Console property scope: https://support.google.com/webmasters/answer/10432366
- GitHub custom domain DNS: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site
- GitHub HTTPS: https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https
- Bing sitemaps: https://www.bing.com/webmasters/help/sitemaps-3b5cf6ed
- IndexNow: https://www.indexnow.org/documentation
- Successful existing workflow: https://github.com/527270866/TianSeal-Company/actions/runs/37580991831
