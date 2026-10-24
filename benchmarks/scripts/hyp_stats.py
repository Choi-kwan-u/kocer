"""Output-style profile per model/dataset: share of hyps with digits / Latin / punctuation, empties."""
import json, re, os, sys
sys.path.insert(0, os.path.dirname(__file__)); from common import ROOT
tags = sorted(d for d in os.listdir(os.path.join(ROOT, "results")) if os.path.isdir(os.path.join(ROOT, "results", d)))
print("| model | dataset | hyp has digit | hyp has Latin | hyp has punct | empty |"); print("|---|---|---|---|---|---|")
for t in tags:
    for ds in ["zeroth", "fleurs", "commonvoice"]:
        p = os.path.join(ROOT, "results", t, f"{ds}.jsonl")
        if not os.path.exists(p): continue
        rows = [json.loads(l) for l in open(p, encoding="utf-8")]; N = len(rows)
        if N == 0: continue
        f = lambda rx: 100 * sum(bool(re.search(rx, r["hyp"])) for r in rows) / N
        d, a, pu = f(r"\d"), f(r"[A-Za-z]"), f(r"[.,?!]"); e = sum(not r["hyp"].strip() for r in rows)
        print(f"| {t} | {ds} | {d:.1f}% | {a:.1f}% | {pu:.1f}% | {e} |")
