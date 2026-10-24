"""results/scores.json -> results/tables.md (4.3 ranking table + fake-error ratio + paired bootstrap CI)."""
import json, os, sys, random
import numpy as np, kocer
sys.path.insert(0, os.path.dirname(__file__)); from common import ROOT

scores = json.load(open(os.path.join(ROOT, "results", "scores.json"), encoding="utf-8"))
datasets = [d for d in ["zeroth", "fleurs", "commonvoice"] if any(d in v for v in scores.values())]
models = sorted(scores)

def overall(t, key):  # pooled across datasets: total errors / total ref chars
    e = sum(scores[t][d][f"{'raw' if key=='raw' else 'ko'}_err"] for d in datasets if d in scores[t])
    n = sum(scores[t][d][f"{'raw' if key=='raw' else 'ko'}_n"] for d in datasets if d in scores[t])
    return e / n

def ranks(vals):
    order = sorted(vals, key=vals.get); return {m: i + 1 for i, m in enumerate(order)}

out = []
out.append("## Per-dataset CER (%) — raw / nlptutti(standard) / kocer\n")
out.append("| model | " + " | ".join(f"{d} raw | {d} nlptutti | {d} kocer | {d} fake%" for d in datasets) + " |")
out.append("|---|" + "---|" * (4 * len(datasets)))
for t in models:
    cells = []
    for d in datasets:
        s = scores[t].get(d)
        if not s: cells += ["-"] * 4; continue
        cells += [f"{s['raw']*100:.2f}", f"{s['nlptutti']*100:.2f}", f"{s['kocer']*100:.2f}", f"{(s['raw']-s['kocer'])/s['raw']*100:.0f}%"]
    out.append(f"| {t} | " + " | ".join(cells) + " |")

out.append("\n## Ranking (overall = pooled over datasets)\n")
r_raw = ranks({m: overall(m, "raw") for m in models}); r_ko = ranks({m: overall(m, "kocer") for m in models})
hdr = "| model | " + " | ".join(f"{d} raw | {d} kocer" for d in datasets) + " | overall raw (rank) | overall kocer (rank) |"
out.append(hdr); out.append("|---|" + "---|" * (2 * len(datasets) + 2))
per_ds_rank = {d: (ranks({m: scores[m][d]["raw"] for m in models if d in scores[m]}),
                   ranks({m: scores[m][d]["kocer"] for m in models if d in scores[m]})) for d in datasets}
for t in models:
    cells = []
    for d in datasets:
        s = scores[t].get(d)
        if not s: cells += ["-", "-"]; continue
        rr, rk = per_ds_rank[d][0][t], per_ds_rank[d][1][t]
        b = "**" if rr != rk else ""
        cells += [f"{b}{s['raw']*100:.2f} ({rr}){b}", f"{b}{s['kocer']*100:.2f} ({rk}){b}"]
    b = "**" if r_raw[t] != r_ko[t] else ""
    cells += [f"{b}{overall(t,'raw')*100:.2f} ({r_raw[t]}){b}", f"{b}{overall(t,'kocer')*100:.2f} ({r_ko[t]}){b}"]
    out.append(f"| {t} | " + " | ".join(cells) + " |")
out.append("\n굵게 = raw와 kocer에서 순위가 다른 칸.")

# paired bootstrap on sentence-level error counts: CI of (raw - kocer) per model/dataset
out.append("\n## Paired bootstrap 95% CI of raw − kocer (%p), 1000 resamples, seed 0\n")
out.append("| model | " + " | ".join(datasets) + " |"); out.append("|---|" + "---|" * len(datasets))
rng = np.random.default_rng(0)
for t in models:
    cells = []
    for d in datasets:
        p = os.path.join(ROOT, "results", t, f"{d}.jsonl")
        if not os.path.exists(p): cells.append("-"); continue
        rows = [json.loads(l) for l in open(p, encoding="utf-8")]
        ids = set(json.load(open(os.path.join(ROOT, "results", "common_ids.json"), encoding="utf-8"))[d])
        rows = [r for r in rows if r["id"] in ids]
        re_, rn, ke, kn = [], [], [], []
        for r in rows:
            a = kocer.measure(r["ref"], r["hyp"], normalize=False); b = kocer.measure(r["ref"], r["hyp"])
            re_.append(sum(a.ops.values())); rn.append(a.hits + a.ops["S"] + a.ops["D"])
            ke.append(sum(b.ops.values())); kn.append(b.hits + b.ops["S"] + b.ops["D"])
        re_, rn, ke, kn = map(np.array, (re_, rn, ke, kn)); N = len(rows)
        diffs = []
        for _ in range(1000):
            idx = rng.integers(0, N, N)
            diffs.append(re_[idx].sum() / rn[idx].sum() - ke[idx].sum() / kn[idx].sum())
        lo, hi = np.percentile(diffs, [2.5, 97.5])
        cells.append(f"{(re_.sum()/rn.sum()-ke.sum()/kn.sum())*100:.2f} [{lo*100:.2f}, {hi*100:.2f}]")
    out.append(f"| {t} | " + " | ".join(cells) + " |")

open(os.path.join(ROOT, "results", "tables.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
print("\n".join(out))
