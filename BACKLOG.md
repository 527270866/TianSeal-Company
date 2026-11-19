# Current decision: free GitHub Pages

The owner clarified that tsseal.com may never have been registered, then authorized
switching to https://527270866.github.io/TianSeal-Company/. This supersedes the
prior domain-retention plan below. Remove CNAME and the Pages custom-domain setting;
retain the exact Google verification file. Canonical/hreflang/sitemap URLs now
include /TianSeal-Company/. A project-path robots.txt does not control crawlers:
robots rules are read at https://527270866.github.io/robots.txt. Submit the sitemap
directly in the matching Search Console and Bing properties after deployment.

Current code validation: all 219 pages pass; live deployment/settings verification pending.
Next task: clear the Pages custom-domain setting, deploy, then verify HTTPS and submit
https://527270866.github.io/TianSeal-Company/sitemap.xml in the existing matching
Search Console property if it is still verified. No paid domain is required.

## Historical audit and earlier plan (superseded where conflicting)

# Backlog

## Completed first increment
- [x] Recover full source with history into this project workspace.
- [x] Confirm current CNAME, verification file, catalog and latest successful Pages run.
- [x] Independently confirm tsseal.com NXDOMAIN and old project URL redirect.
- [x] Generate and test search discovery files and annotations for 219 pages.
- [x] Preserve existing style, product content, sourcing disclaimers and identity files.

## Required account decisions/actions — before publication
1. Confirm whether tsseal.com is still owned and intended. If yes, sign in to the
   existing registrar and inspect registration status and authoritative nameservers.
   NXDOMAIN does not distinguish expired registration from absent delegation.
   Do not buy a domain or authorize a renewal charge through this task.
2. Once registration/delegation works, inspect existing DNS before editing anything.
   For a retained tsseal.com apex on GitHub Pages, official A-record targets are
   185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153.
   Optional www CNAME targets 527270866.github.io (no repository path).
   Preserve unrelated email/TXT records; do not apply changes until owner/domain
   authority is established. Consult linked GitHub documentation for IPv6 or ALIAS.
3. Inspect repository Settings → Pages: source branch/directory, tsseal.com custom
   domain, DNS check, certificate status, then Enforce HTTPS when available.
4. Review/merge the prepared increment only for the confirmed canonical domain.
   Verify deployment, homepage, one product in each language, robots, sitemap and
   the unchanged Google verification file over HTTPS with 200 responses. Check
   redirects from HTTP, www (if configured) and the old project URL.
5. In the owner's Google Search Console, select or add https://tsseal.com/ as a
   URL-prefix property (or use DNS-verified Domain property tsseal.com). The old
   github.io URL-prefix property does not cover the custom domain. If verification
   is requested, use the exact file/token Google supplies for this account/property;
   never overwrite or remove the existing file without checking its purpose.
6. Submit https://tsseal.com/sitemap.xml in that property. Inspect the homepage and
   representative products using URL Inspection → Test Live URL; request indexing
   when eligible. Record actual indexing/canonical results and dates, not assumptions.
7. Add/verify the same site in free Bing Webmaster Tools (import from Search Console
   if available) and submit the same sitemap. Record processing errors/results.

## Subsequent free improvements
- Consider IndexNow only after working host ownership and deployment are verified.
  It requires a real key file accessible on that host; no key or submission was
  invented here. Receipt is not indexing. It can notify participating engines;
  Google Search Console remains a separate workflow.
- Review actual Search Console coverage/exclusions and Bing crawl errors, then fix
  demonstrated issues. Track impressions/clicks and branded queries over time.
- Audit product metadata and factual specifications individually; do not invent
  certifications, reviews, manufacturing claims or commercial guarantees.
- Replace legacy build_catalog.py only in a separate catalog-preservation increment.
- Add visual QA of the new expandable directory on desktop/mobile before merging.

## Next daily task (small, user-initiated)
Resolve the intended-domain decision and inspect registrar + GitHub Pages settings.
Then retest DNS/HTTPS and record the actual result. If account access is unavailable,
review the prepared changes and directory layout locally. No daily automation exists.
