# Eightinity Skills

![License](https://img.shields.io/github/license/eightinity/skills)
![Version](https://img.shields.io/github/v/release/eightinity/skills?label=version)
![Skills](https://img.shields.io/badge/skills-1-7C3AED)
![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-black)

Claude Code skills published by [Eightinity](https://eightinity.in).

## Install

```bash
npx skills add eightinity/skills
```

Or install a specific skill:

```bash
npx skills add eightinity/skills/seo-audit
```

## Available skills

| Skill | Description |
|---|---|
| [seo-audit](./seo-audit/) | Three-phase SEO audit — local code, GSC live site, and PageSpeed Insights |

---

## seo-audit

A three-phase SEO audit skill for Claude Code.

**Phase 1 — Local code audit** *(no domain needed)*
Reads your source files. Checks metadata, alt tags, sitemap generator, heading structure, URL slugs, image formats, navigation, and indexable content. Scored out of 20.

**Phase 2 — GSC live site audit** *(requires domain + Google Search Console)*
Indexing status, sitemap health, clicks/impressions/CTR per page, quick-win pages (pos 8–20), content gaps, Core Web Vitals field data, GEO/AI-search visibility.

**Phase 3 — PageSpeed audit** *(requires domain, uses `curl` — no install needed)*
Hits the Google PageSpeed Insights API directly. Returns mobile + desktop scores (0–100), Core Web Vitals lab data, top opportunities with estimated savings, and diagnostics. Same data as pagespeed.web.dev.

When you run `/seo-audit`, Claude shows a menu so you pick which phase(s) to run.

---

## License

[MIT](./LICENSE) © [Eightinity Technologies](https://eightinity.in)
