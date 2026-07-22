---
name: eval-failure-triage
description: Triage failures from an LLM or ML eval run — cluster them by error type and flag rows where the gold label itself looks wrong rather than the model. Use when eval accuracy drops and you need to know if it's a real regression or bad labels, when curating a golden/eval dataset and want to sanity-check gold labels before trusting them, or when the user asks to triage, cluster, or debug eval failures, or find mislabeled eval rows.
---

# Eval Failure Triage

A failing eval row means one of two very different things: the model got it wrong, or the gold label is wrong and the model didn't. Conflating them wastes fix effort on the model when the fix is really a label correction, and vice versa. Triage separates the two before anyone touches a prompt.

## Steps

1. **Normalize the eval file.** Run the bundled script against the eval output (accepts JSONL, JSON, or CSV):
   ```bash
   python3 scripts/normalize_eval.py <eval_file> -o failures.jsonl
   ```
   It auto-detects input/prediction/gold/pass/score columns from common names. If it reports it couldn't find a pass or score field, ask the user which field marks a row as failing, then re-run with `--pass-field NAME` or `--score-field NAME --score-threshold N`. Completion criterion: `failures.jsonl` exists and its row count is plausible against the `N/total failed` line it prints — a real regression reporting 0 failures means a field was misdetected; fix that before moving on.

2. **Read the failures in batches of ~15-20 rows** — hundreds of rows won't fit a useful single analysis pass. For each row, form a judgment on two independent questions:
   - **Error type**: what kind of mistake is this? Don't force rows into a fixed taxonomy — let categories emerge from what you actually see (e.g. "wrong classification direction," "missing required field," "off-by-one attribution," "hallucinated detail not in input," "format/schema violation"). Reuse a category name across batches when a new row matches one already established — categories must stay comparable across the whole set, not batch-local.
   - **Label trust**: independent of category, does the *gold* label actually hold up given the input? If the model's answer looks at least as defensible as the gold label, mark this row a **gold-label suspect**, not a model bug — this is the highest-leverage judgment in the whole triage, since a "regression" that's really bad labels needs a dataset fix, not a model fix.

3. **Track a running tally** as you go: per category, a count, the model-bug vs gold-label-suspect split, and 1-2 representative row IDs. Keep going until every failing row is categorized — reporting "top categories so far" from a partial pass is worse than useless, since the uncategorized tail is exactly where the next surprise hides.

4. **Write the triage report** (markdown), ranked by count:
   - A summary table: category, count, model-bug / gold-label-suspect split
   - The full list of gold-label-suspect rows — id, input, prediction, gold label, and why the gold label looks wrong — the exact list a human should review before touching the model at all
   - 2-3 representative examples per top model-bug category, since a category name alone rarely tells someone what to go fix

## Completion criterion

Every row in `failures.jsonl` is accounted for in the report — either in a category or explicitly flagged as unclear. Don't present partial coverage as if it were the whole picture.
