---
name: seo-audit
description: Three-phase SEO audit — Phase 1 audits local code, Phase 2 audits the live site via Google Search Console, Phase 3 runs a PageSpeed Insights performance audit via curl (no install needed)
---

# SEO Audit

## ⚡ Start here — always show this first

**Before doing anything else**, present the following menu to the user:

---

> **SEO Audit — pick your phase:**
>
> **Phase 1 — Code audit** *(no domain needed)*
> Reads your local source files. Checks metadata, alt tags, sitemap generator, heading structure, URL slugs, indexable content, and more. Scored out of 20. Run this before deploying or in a PR review.
>
> **Phase 2 — GSC audit** *(requires your domain + Google Search Console)*
> Checks the live site. Indexing status, sitemap health, clicks/impressions/CTR per page, quick-win pages (pos 8–20), content gaps, Core Web Vitals field data, and GEO/AI-search visibility.
>
> **Phase 3 — PageSpeed audit** *(requires your domain)*
> Hits the Google PageSpeed Insights API (same as pagespeed.web.dev). Returns mobile + desktop performance scores (0–100), Core Web Vitals lab data, and a prioritised list of opportunities with estimated time savings. No install, no API key needed.
>
> **Reply with:** `1`, `2`, `3`, `1+2`, `1+3`, `2+3`, or `all` — or just describe what you want.

---

Wait for the user's reply before proceeding. Then run only the selected phase(s), in order.

- Phase 1 needs no domain — start immediately.
- Phase 2 and 3 need the domain — if not already provided, ask: *"What's your site's domain? (e.g. `https://example.com`)"*

---

# SEO Audit (Three Phases)

---

## Phase 1 — Local Code Audit

Audits the codebase directly. No domain or live site needed. Run this before deploying or as part of a PR review.

### How to run
- Read the local source files (pages, components, sitemap generator, robots.txt, SEO component).
- Check each of the 10 areas below.
- Score and produce the deliverables.

### Scoring
- 2 = Pass
- 1 = Needs work
- 0 = Fail

**Total: 0–20**

---

### 1) Mobile-friendliness
**What to check in code:**
- Responsive CSS used (Tailwind breakpoints, flex/grid) — no fixed-width layouts.
- No horizontal overflow on small screens.
- Tap targets adequately sized (min 44×44px).
- Key content not hidden on mobile via CSS `hidden` / `display:none` without a mobile equivalent.

**Fix guidance:**
- Prefer Tailwind responsive prefixes (`sm:`, `md:`, `lg:`) over hardcoded pixel widths.
- Don't gate indexable content behind hover-only interactions.

---

### 2) Website speed
**What to check in code:**
- Images use modern formats (`.webp`, `.avif`) and have explicit `width`/`height`.
- No render-blocking scripts loaded synchronously in `<head>`.
- Large JS bundles — check `vite.config.js` for code-splitting / dynamic imports.
- Fonts loaded with `font-display: swap` or preloaded.
- Third-party scripts deferred.

**Fix guidance:**
- Add `loading="lazy"` to below-fold images; add `fetchpriority="high"` + `preload` to LCP image.
- Use `import()` / `React.lazy` for heavy page components.
- Self-host fonts when possible; add `<link rel="preload">` for critical font files.

---

### 3) Sitemaps
**What to check in code:**
- Sitemap generator script exists and covers all page templates.
- `lastmod` dates are dynamic (not hardcoded).
- Sitemap excludes low-value URLs (utility pages, parameterised duplicates).
- `robots.txt` references the sitemap URL.

**Fix guidance:**
- Run the sitemap generator locally and spot-check the output.
- Ensure new page types (blog posts, case studies) are added to the generator.

---

### 4) Readability
**What to check in code:**
- One `<h1>` per page — verify in page components.
- Logical heading hierarchy (`h1` → `h2` → `h3`, no skips).
- No heading typos in static copy strings.
- Body font ≥ 16px; line-height ≥ 1.5.

**Fix guidance:**
- Search for hardcoded heading strings — grep for `<h1` across `src/pages/`.
- Fix any heading level skips.

---

### 5) Image file names
**What to check in code:**
- Image files in `public/images/` use descriptive, hyphenated names (not hashes).
- Names reflect content/topic, not generic (`img1.jpg`, `DSC_4821.jpg`).

**Fix guidance:**
- Rename files to `[topic]-[descriptor].webp` pattern.
- Update all `src` references after rename.

---

### 6) Alt tags
**What to check in code:**
- Every `<img>` that carries information has a non-empty `alt`.
- Purely decorative images have `alt=""`.
- Alt text is descriptive — not keyword-stuffed, not filename echoes.

**Fix guidance:**
- `grep -rn 'alt=""' src/` and review — confirm each is truly decorative.
- `grep -rn '<img' src/ | grep -v 'alt='` to find images with no alt attribute at all.

---

### 7) Website navigation
**What to check in code:**
- Nav links cover all key page types.
- Internal links exist from content pages (blog posts) to money pages (home, services).
- No orphan pages — every page reachable within 2–3 clicks.
- Nav markup is semantic (`<nav>`, `<ul>/<li>` or ARIA roles).

**Fix guidance:**
- Add a "Related posts" or CTA section at the bottom of blog posts linking to the home page or a relevant service.
- Ensure footer includes links to all top-level pages.

---

### 8) URL structure
**What to check in code:**
- Route definitions use lowercase, hyphenated slugs.
- No unnecessary URL parameters.
- Consistent trailing-slash behaviour (check `vite.config.js` / router config).
- No duplicate routes for the same content.

**Fix guidance:**
- Enforce trailing-slash consistency via a redirect rule in `vercel.json`.
- Ensure blog post slugs are set in content files, not auto-generated from titles.

---

### 9) Metadata
**What to check in code:**
- Every page component renders a unique `<title>` tag (50–60 chars).
- Every page has a unique `<meta name="description">` (120–160 chars).
- OG tags present: `og:title`, `og:description`, `og:image`, `og:url`.
- Canonical `<link rel="canonical">` on every page.
- SEO component / head injection works at pre-render time (not JS-only).

**Fix guidance:**
- Read the SEO component (`src/components/SEO.jsx` or equivalent) — verify it writes tags into `<head>` during pre-render.
- Check `prerender.mjs` output HTML — confirm `<meta>` tags are in the static HTML, not injected post-load.
- Audit each page's `<SEO>` call for missing or duplicate descriptions.

---

### 10) Indexable content
**What to check in code:**
- Main content is in HTML source (check pre-render output), not only in JS bundles.
- `robots.txt` doesn't accidentally block any page types.
- No `<meta name="robots" content="noindex">` on rankable pages.
- Canonical tags don't point to wrong URLs.
- Pre-render / SSG script covers all dynamic routes.

**Fix guidance:**
- Run `npm run build` and inspect the generated HTML files — confirm body content is present in source.
- Check `prerender.mjs` — ensure it hits all routes defined in `src/routes` or the router config.

---

### Phase 1 deliverables

#### A) Scorecard (0–20)
- Mobile-friendliness: __/2
- Website speed: __/2
- Sitemaps: __/2
- Readability: __/2
- Image file names: __/2
- Alt tags: __/2
- Website navigation: __/2
- URL structure: __/2
- Metadata: __/2
- Indexable content: __/2

#### B) Top findings (prioritized)
For each: Impact (High/Med/Low) · Affected file/URL · What to change · How to verify.

#### C) Action plan
1. Do-now (1–3 days)
2. Next (1–2 weeks)
3. Later (1–2 months)

---
---

## Phase 2 — GSC Live Site Audit

Audits the **deployed site** using Google Search Console data. Run this after deployment, or periodically (weekly/monthly) to track progress.

**Requires:** the site's domain.

> If the domain hasn't been provided, ask:
> "What's your site's domain? (e.g. `https://example.com`)"

This phase is **not scored** — it produces a structured report of raw GSC data, indexing status, and actionable opportunities.

---

### Step 0 — Check `gsc` CLI availability

```bash
gsc --version 2>/dev/null || echo "NOT_INSTALLED"
```

If not installed:
> "`gsc` CLI isn't installed. Run `npm install -g @nicholasgasior/gsc` to enable it. Without it I'll fall back to `site:` searches and manual GSC steps for each check."

---

### 2a) Indexing check

**What to check:**
- Which sitemap URLs are actually indexed by Google.
- Which pages are missing from the index and why.

**With `gsc`:**
```bash
gsc inspect --url "https://example.com/page" --site "https://example.com"
gsc coverage --site "https://example.com"
```

**Without `gsc` (fallback):**
Use `WebSearch` with `site:example.com` and `site:example.com/blog` to spot-check indexed pages.

**Output — index status table:**

| URL | Status | Last crawled | Notes |
|---|---|---|---|
| /  | INDEXED | YYYY-MM-DD | — |
| /blog/post | NOT_INDEXED | — | Too new / not submitted |

**Submitting unindexed pages:**
```bash
gsc request-indexing --url "https://example.com/page" --site "https://example.com"
```
Without `gsc`: GSC web UI → URL Inspection → Request Indexing.

---

### 2b) Sitemap health

```bash
gsc sitemaps list --site "https://example.com"
gsc sitemaps get --site "https://example.com" --url "https://example.com/sitemap.xml"
```

**Output:**

| Sitemap | Submitted | Last read | URLs submitted | URLs indexed | Errors |
|---|---|---|---|---|---|
| /sitemap.xml | YYYY-MM-DD | YYYY-MM-DD | N | N | N |

**Flags:**
- Last read > 14 days → resubmit.
- Submitted ≠ indexed by large margin → coverage issue.

**Manual fallback:** GSC → Sitemaps.

---

### 2c) Coverage report

```bash
gsc coverage --site "https://example.com"
gsc coverage --site "https://example.com" --type ERROR
gsc coverage --site "https://example.com" --type EXCLUDED
```

**Output:**

| Status | Count | Top reason |
|---|---|---|
| Valid | N | — |
| Valid with warning | N | e.g. "Indexed, not in sitemap" |
| Error | N | e.g. "404", "redirect error" |
| Excluded | N | e.g. "noindex", "duplicate" |

**Manual fallback:** GSC → Pages.

---

### 2d) Search performance — clicks, impressions, CTR, position

```bash
# Site-wide totals
gsc performance --site "https://example.com" --days 28
gsc performance --site "https://example.com" --days 90

# Per page (top 25 by impressions)
gsc performance --site "https://example.com" --days 28 --dimension page --limit 25

# Per query (top 25 by impressions)
gsc performance --site "https://example.com" --days 28 --dimension query --limit 25

# Quick-win pages: pos 8–20
gsc performance --site "https://example.com" --days 28 --dimension page --min-position 8 --max-position 20
```

**Auto-flags:**
- Impressions > 500 + CTR < 2% → rewrite title/meta description.
- Avg position 8–20 → content or internal link opportunity.
- Query impressions > 200 + no matching optimised page → content gap.
- Avg position worsening > 3 positions vs prior period → regression.

**Manual fallback:** GSC → Search results → export CSV.

---

### 2e) Core Web Vitals (field data)

```bash
gsc cwv --site "https://example.com"
gsc cwv --site "https://example.com" --device mobile
gsc cwv --site "https://example.com" --device desktop
```

**Output:**

| Device | Good | Needs improvement | Poor | Top poor URL |
|---|---|---|---|---|
| Mobile | N | N | N | /page |
| Desktop | N | N | N | /page |

Any `Poor` URLs → High-impact fix (direct ranking signal).

**Manual fallback:** GSC → Core Web Vitals.

---

### 2f) GEO / AI-search visibility

Run 3–5 buyer queries via `WebSearch` relevant to the site's niche. Record whether the domain surfaces vs. competitors.

---

### Phase 2 report format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GSC REPORT — example.com
Last 28 days · YYYY-MM-DD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

INDEXING
  Checked: N pages · Indexed: N · Not indexed: N
  Unindexed: /page-a, /page-b
  Submitted for indexing: /page-a

SITEMAPS
  /sitemap.xml · Last read: YYYY-MM-DD
  Submitted: N · Indexed: N · Errors: N

COVERAGE
  ✅ Valid: N  ⚠️ Warning: N  ❌ Error: N  ⬜ Excluded: N
  Top error: "..."

PERFORMANCE (28d)
  Clicks: N · Impressions: N · CTR: N% · Avg pos: N.N

TOP PAGES BY IMPRESSIONS
  1. /page — N imp / N clicks / N% CTR / pos N.N  [⚠️ low CTR]
  2. /page — N imp / N clicks / N% CTR / pos N.N  [🎯 pos 8–20]

QUICK WIN PAGES (pos 8–20)
  /page · pos N.N · N impressions

CONTENT GAPS
  "query" · N impressions · pos N.N

CORE WEB VITALS
  Mobile  — Good: N · Needs work: N · Poor: N
  Desktop — Good: N · Needs work: N · Poor: N

GEO VISIBILITY
  "query 1" — not visible (competitor.com ranks)
  "query 2" — not visible (competitor.com ranks)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---
---

## Phase 3 — PageSpeed Insights Performance Audit

Audits the **live deployed site** using the Google PageSpeed Insights API — the exact same engine and scores as pagespeed.web.dev. No browser extension, no install, no API key needed for occasional use.

**Requires:** the site's domain.

> If not provided, ask: "What's your site's domain? (e.g. `https://example.com`)"

---

### How it works

The PSI API wraps Lighthouse and returns:
- **Performance score** (0–100) for mobile and desktop separately
- **Core Web Vitals** — LCP, INP, CLS, FCP, TTFB (both lab data and real-world field data where available)
- **Opportunities** — specific improvements with estimated time savings
- **Diagnostics** — additional detail on potential issues
- **Passed audits** — what's already good

---

### Step 1 — Run PSI for mobile and desktop

```bash
# Mobile
curl -s "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://example.com&strategy=mobile" -o psi-mobile.json

# Desktop
curl -s "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://example.com&strategy=desktop" -o psi-desktop.json
```

No API key needed for occasional runs. If you hit rate limits, add `&key=YOUR_API_KEY`.

Run for multiple pages if needed (home, key landing page, a blog post):
```bash
curl -s "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://example.com/blog/post-slug&strategy=mobile" -o psi-blog-mobile.json
```

---

### Step 2 — Extract the scores and metrics

```bash
# Performance score (0–100)
cat psi-mobile.json | python3 -c "import json,sys; d=json.load(sys.stdin); print('Mobile score:', d['lighthouseResult']['categories']['performance']['score']*100)"
cat psi-desktop.json | python3 -c "import json,sys; d=json.load(sys.stdin); print('Desktop score:', d['lighthouseResult']['categories']['performance']['score']*100)"

# Core Web Vitals — lab data
cat psi-mobile.json | python3 -c "
import json,sys
d=json.load(sys.stdin)['lighthouseResult']['audits']
print('LCP:', d['largest-contentful-paint']['displayValue'])
print('INP:', d.get('interaction-to-next-paint', {}).get('displayValue', 'n/a'))
print('CLS:', d['cumulative-layout-shift']['displayValue'])
print('FCP:', d['first-contentful-paint']['displayValue'])
print('TTFB:', d['server-response-time']['displayValue'])
"

# Top opportunities (with estimated savings)
cat psi-mobile.json | python3 -c "
import json,sys
audits = json.load(sys.stdin)['lighthouseResult']['audits']
opps = [(k,v) for k,v in audits.items() if v.get('details',{}).get('type')=='opportunity' and v.get('score',1)<1]
for k,v in sorted(opps, key=lambda x: x[1].get('details',{}).get('overallSavingsMs',0), reverse=True):
    print(f\"  [{v['score']}] {v['title']} — {v['displayValue']}\")
"

# Diagnostics (failed audits that aren't opportunities)
cat psi-mobile.json | python3 -c "
import json,sys
audits = json.load(sys.stdin)['lighthouseResult']['audits']
diags = [(k,v) for k,v in audits.items() if v.get('score') is not None and v['score']<1 and v.get('details',{}).get('type')!='opportunity']
for k,v in diags[:10]:
    print(f\"  {v['title']} — {v['displayValue']}\")
"
```

Or read the JSON files directly and extract the key fields manually.

---

### Step 3 — Check real-world field data (CrUX)

The API also returns Chrome User Experience Report data if available:

```bash
cat psi-mobile.json | python3 -c "
import json,sys
crux = json.load(sys.stdin).get('loadingExperience', {})
metrics = crux.get('metrics', {})
for k,v in metrics.items():
    print(f\"{k}: {v.get('category')} (p75: {v.get('percentile')})\")
print('Overall:', crux.get('overall_category'))
"
```

If field data is unavailable (not enough real users), it will say `NONE` — lab data from Lighthouse is the fallback.

---

### Output to capture

**Scores table:**

| Page | Mobile score | Desktop score |
|---|---|---|
| / (home) | N/100 | N/100 |
| /blog/post | N/100 | N/100 |

**Core Web Vitals — mobile:**

| Metric | Lab value | Field value | Status |
|---|---|---|---|
| LCP | Xs | Xs | Good / Needs work / Poor |
| INP | Xms | Xms | Good / Needs work / Poor |
| CLS | X.XX | X.XX | Good / Needs work / Poor |
| FCP | Xs | Xs | — |
| TTFB | Xms | — | — |

**Top opportunities (mobile, by time saving):**

| Opportunity | Est. saving |
|---|---|
| Eliminate render-blocking resources | X.Xs |
| Properly size images | X.Xs |
| Reduce unused JavaScript | X.Xs |
| ... | ... |

**Diagnostics:**
- List any failed diagnostic audits (e.g. "Image elements do not have explicit width and height", "Avoid large layout shifts")

---

### Scoring guide (for Phase 3 findings)

| Score | Meaning |
|---|---|
| 90–100 | Good |
| 50–89 | Needs improvement |
| 0–49 | Poor |

Flag any mobile score < 50 as **High impact** — it directly affects mobile search ranking.

---

### Phase 3 report format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PAGESPEED REPORT — example.com
YYYY-MM-DD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SCORES
  Mobile:  N/100  [Good / Needs improvement / Poor]
  Desktop: N/100  [Good / Needs improvement / Poor]

CORE WEB VITALS (mobile)
  LCP:  Xs     [Good / Needs work / Poor]
  INP:  Xms    [Good / Needs work / Poor]
  CLS:  X.XX   [Good / Needs work / Poor]
  FCP:  Xs
  TTFB: Xms

FIELD DATA (real users)
  Overall: Good / Needs improvement / Poor / UNAVAILABLE

TOP OPPORTUNITIES
  1. Eliminate render-blocking resources     — save ~X.Xs
  2. Properly size images                    — save ~X.Xs
  3. Reduce unused JavaScript                — save ~X.Xs

DIAGNOSTICS
  - Image elements missing explicit dimensions
  - Avoid large layout shifts (CLS sources: ...)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Live dashboard (every run)

After each phase, append to `.claude/skills/seo-audit/history.jsonl` and regenerate the dashboard:

```json
{
  "date": "YYYY-MM-DD",
  "phase": "code|gsc|pagespeed|all",
  "total": 0,
  "scores": {
    "mobile": 0, "speed": 0, "sitemaps": 0, "readability": 0,
    "imageNames": 0, "altTags": 0, "navigation": 0,
    "urlStructure": 0, "metadata": 0, "indexable": 0
  },
  "gsc": {
    "sitemapLastRead": "YYYY-MM-DD",
    "sitemapUrlsSubmitted": 0, "sitemapUrlsIndexed": 0,
    "coverageValid": 0, "coverageErrors": 0, "coverageExcluded": 0,
    "clicks28d": 0, "impressions28d": 0, "ctr28d": 0.0, "avgPosition28d": 0.0,
    "quickWinPages": [], "contentGaps": [],
    "cwvMobilePoor": 0, "cwvDesktopPoor": 0
  },
  "indexing": {
    "checked": 0, "indexed": 0,
    "notIndexed": [], "submitted": [],
    "tool": "gsc|site-search|manual"
  },
  "findings": [{ "title": "...", "impact": "High|Med|Low", "status": "open|fixed|pending-deploy" }],
  "nextSteps": [],
  "geoChecked": 0, "geoHits": 0,
  "geo": [{ "query": "...", "visible": false, "competitors": "..." }],
  "notes": ""
}
```

```bash
node .claude/skills/seo-audit/generate-dashboard.mjs
open .claude/skills/seo-audit/dashboard.html
```

Dashboard tabs: **Scorecard** (Phase 1, /20 + trend), **Findings**, **Action Plan**, **GSC Report** (Phase 2), **GEO Visibility**, **Live Report**.
