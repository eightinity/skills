# Eightinity Skills

![License](https://img.shields.io/badge/license-MIT-blue)
![Version](https://img.shields.io/github/v/release/eightinity/skills?label=version)
![Skills](https://img.shields.io/badge/skills-2-7C3AED)
![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-black)

Claude Code skills published by [Eightinity](https://eightinity.in).

## Install

```bash
npx skills add eightinity/skills
```

Or install a specific skill:

```bash
npx skills add eightinity/skills/seo-audit
npx skills add eightinity/skills/eval-failure-triage
```

## Available skills

| Skill | Description |
|---|---|
| [seo-audit](./seo-audit/) | Three-phase SEO audit — local code, GSC live site, and PageSpeed Insights |
| [eval-failure-triage](./eval-failure-triage/) | Triage LLM/ML eval failures — cluster by error type and flag rows where the gold label is wrong, not the model |

---

## eval-failure-triage

Triages failures from any LLM or ML eval run — JSONL, JSON, or CSV, with an input, prediction, gold/expected value, and a pass/fail flag or score.

A failing eval row means one of two very different things: the model got it wrong, or the gold label is wrong and the model didn't. Conflating them wastes fix effort on the model when the real fix is a dataset correction. This skill:

- Normalizes the eval file with a bundled, dependency-free script, auto-detecting common column names
- Reads through the failures and clusters them by error type — categories emerge from what's actually there, not a fixed taxonomy
- Independently judges, for every failure, whether the *gold label* holds up — flagging **gold-label suspects** separately from real model bugs
- Produces a markdown triage report: a summary table ranked by count, the full gold-label-suspect list ready for human review, and representative examples per top model-bug category

`examples/sample_eval.jsonl` includes a matched pair of failures that look identical on the surface (both "date extraction off by one") but have opposite root causes — one's a real model bug, the other's a bad gold label. That pair is the whole point of the skill.

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
