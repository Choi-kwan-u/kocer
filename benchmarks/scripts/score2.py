"""Fair re-scoring. Four normalization levels, each applied identically to ref and hyp:
  L0 raw          : nothing (jiwer-style; spaces count as characters)
  L1 nospace      : whitespace removed
  L2 nospace+punct: whitespace + punctuation removed (NFC)   [= kocer with numbers/letters off; nlptutti standard as cross-check]
  L3 kocer        : + number candidate sets + Latin letters/acronyms
Per sentence we keep error count E = S+D+I and reference length N = hits+S+D at each level.
Corpus CER_L = sum(E_L)/sum(N_L). Fake-error decomposition uses COUNTS (denominator-free):
  spacing = E0-E1, punctuation = E1-E2, numbers/letters = E2-E3, each as share of E0.
Pairwise paired bootstrap over sentences (both datasets pooled) tests model-vs-model differences."""
import json, os, sys, re
import numpy as np, kocer
from nlptutti import compare_systems
sys.path.insert(0, os.path.dirname(__file__)); from common import ROOT

LEVELS = ["raw", "nospace", "nopunct", "kocer"]
DATASETS = [d for d in ["zeroth", "fleurs", "commonvoice"] if os.path.exists(os.path.join(ROOT, "data", d, "test.jsonl"))]
_ws = re.compile(r"\s+")

def en(m): return sum(m.ops.values()), m.ref_len  # kocer >= 0.4.0: 분모는 정답만으로 정해짐
def sent(ref, hyp):
    r1, h1 = _ws.sub("", ref), _ws.sub("", hyp)
    return [en(kocer.measure(ref, hyp, normalize=False)),
            en(kocer.measure(r1, h1, normalize=False)),
            en(kocer.measure(ref, hyp, numbers=False, letters=False)),
            en(kocer.measure(ref, hyp))]

def load(p): return {r["id"]: r for r in (json.loads(l) for l in open(p, encoding="utf-8"))}

tags = sorted(d for d in os.listdir(os.path.join(ROOT, "results")) if os.path.isdir(os.path.join(ROOT, "results", d)) and not d.startswith("_"))  # "_" = auxiliary runs
per = {}      # per[tag][ds] = np.array shape (n, 4, 2)  [E, N]
nlpt = {}     # nlptutti micro cross-check
common_ids = {}
fake_pool = []
for ds in DATASETS:
    files = {t: os.path.join(ROOT, "results", t, f"{ds}.jsonl") for t in tags}
    data = {t: load(p) for t, p in files.items() if os.path.exists(p) and os.path.getsize(p) > 0}
    if not data: continue
    ids = sorted(set.intersection(*(set(d) for d in data.values())))
    ids = [i for i in ids if all(data[t][i]["hyp"].strip() for t in data)]
    common_ids[ds] = ids
    print(f"[{ds}] models={len(data)} common={len(ids)}")
    for t in data:
        refs = [data[t][i]["ref"] for i in ids]; hyps = [data[t][i]["hyp"] for i in ids]
        arr = np.array([sent(r, h) for r, h in zip(refs, hyps)], dtype=np.int64)
        per.setdefault(t, {})[ds] = arr
        nlpt.setdefault(t, {})[ds] = compare_systems(refs, {"m": hyps, "_": hyps}, rate_mode="standard")["systems"][0]["metrics"]["cer"]["micro"]
        for i, row in zip(ids, arr):
            if row[0][0] > 0 and row[3][0] == 0:
                fake_pool.append(dict(model=t, dataset=ds, id=i, ref=data[t][i]["ref"], hyp=data[t][i]["hyp"]))
models = sorted(per)

def cer(arr, L): return arr[:, L, 0].sum() / arr[:, L, 1].sum()
def pooled(t): return np.concatenate([per[t][d] for d in DATASETS if d in per[t]])

out = []
scores = {}
# ---- Table A: ladder per dataset ----
for ds in DATASETS + ["overall"]:
    out.append(f"\n## {ds}: CER (%) at each normalization level\n")
    out.append("| model | raw | nospace | nospace+punct | kocer | nlptutti std (check) | ref chars raw / kocer |")
    out.append("|---|---|---|---|---|---|---|")
    for t in models:
        arr = pooled(t) if ds == "overall" else per[t].get(ds)
        if arr is None: continue
        c = [cer(arr, L) for L in range(4)]
        nt = "-" if ds == "overall" else f"{nlpt[t][ds]*100:.2f}"
        out.append(f"| {t} | {c[0]*100:.2f} | {c[1]*100:.2f} | {c[2]*100:.2f} | {c[3]*100:.2f} | {nt} | {arr[:,0,1].sum()} / {arr[:,3,1].sum()} |")
        scores.setdefault(t, {})[ds] = dict(cer=dict(zip(LEVELS, [float(x) for x in c])), E=[int(arr[:, L, 0].sum()) for L in range(4)], N=[int(arr[:, L, 1].sum()) for L in range(4)], n=int(len(arr)))
# ---- Table B: error-count decomposition ----
for ds in DATASETS + ["overall"]:
    out.append(f"\n## {ds}: where the raw errors go (counts; share of raw error count)\n")
    out.append("| model | raw errors | spacing | punctuation | numbers/letters (kocer only) | remaining (kocer errors) | fake share (count) |")
    out.append("|---|---|---|---|---|---|---|")
    for t in models:
        arr = pooled(t) if ds == "overall" else per[t].get(ds)
        if arr is None: continue
        E = [int(arr[:, L, 0].sum()) for L in range(4)]
        sp, pu, nu = E[0]-E[1], E[1]-E[2], E[2]-E[3]
        def f(x): return f"{x} ({x/E[0]*100:.0f}%)"
        out.append(f"| {t} | {E[0]} | {f(sp)} | {f(pu)} | {f(nu)} | {f(E[3])} | {(E[0]-E[3])/E[0]*100:.0f}% |")
# ---- Table C: ranks at each level ----
out.append("\n## Overall rank at each level (pooled Zeroth+FLEURS)\n")
out.append("| model | " + " | ".join(LEVELS) + " |"); out.append("|---|" + "---|"*4)
rank_by_level = {}
for L, name in enumerate(LEVELS):
    vals = {t: cer(pooled(t), L) for t in models}
    order = sorted(vals, key=vals.get); rank_by_level[name] = {t: order.index(t)+1 for t in models}
for t in models:
    out.append(f"| {t} | " + " | ".join(f"{cer(pooled(t),L)*100:.2f} ({rank_by_level[n][t]})" for L, n in enumerate(LEVELS)) + " |")
# ---- Pairwise paired bootstrap ----
B, rng = 2000, np.random.default_rng(0)
n_all = len(pooled(models[0])); idx = rng.integers(0, n_all, (B, n_all))
boot = {}
for L, name in enumerate(LEVELS):
    boot[name] = {}
    for t in models:
        arr = pooled(t); E, N = arr[:, L, 0], arr[:, L, 1]
        boot[name][t] = E[idx].sum(1) / N[idx].sum(1)
pair_stats = {}
for name in ["raw", "nopunct", "kocer"]:
    out.append(f"\n## Pairwise paired bootstrap, level = {name} (overall; {B} resamples, seed 0). Cell = CER(row) - CER(col) in %p, 95% CI; * = CI excludes 0\n")
    out.append("| | " + " | ".join(m[:14] for m in models) + " |"); out.append("|---|" + "---|"*len(models))
    Li = LEVELS.index(name)
    for a in models:
        cells = []
        for b in models:
            if a == b: cells.append("."); continue
            d = boot[name][a] - boot[name][b]; lo, hi = np.percentile(d, [2.5, 97.5]); pt = cer(pooled(a), Li) - cer(pooled(b), Li)
            sig = "*" if (lo > 0 or hi < 0) else ""
            cells.append(f"{pt*100:+.2f} [{lo*100:+.2f},{hi*100:+.2f}]{sig}")
            pair_stats.setdefault(name, {})[f"{a} vs {b}"] = dict(diff=float(pt), lo=float(lo), hi=float(hi), sig=bool(sig))
        out.append(f"| {a[:14]} | " + " | ".join(cells) + " |")
    mat = np.stack([boot[name][t] for t in models], 1)
    ranks = mat.argsort(1).argsort(1) + 1
    out.append(f"\nRank distribution at level {name}: P(rank 1), median rank, 95% rank interval")
    for j, t in enumerate(models):
        r = ranks[:, j]; out.append(f"- {t}: P(1st)={np.mean(r==1):.2f}, median={int(np.median(r))}, 95% [{int(np.percentile(r,2.5))}, {int(np.percentile(r,97.5))}]")
        pair_stats.setdefault("rank_"+name, {})[t] = dict(p1=float(np.mean(r==1)), med=int(np.median(r)), lo=int(np.percentile(r,2.5)), hi=int(np.percentile(r,97.5)))

txt = "\n".join(out)
open(os.path.join(ROOT, "results", "tables2.md"), "w", encoding="utf-8").write(txt + "\n")
json.dump(dict(scores=scores, pairs=pair_stats, levels=LEVELS, kocer_version=kocer.__version__), open(os.path.join(ROOT, "results", "scores2.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(common_ids, open(os.path.join(ROOT, "results", "common_ids.json"), "w", encoding="utf-8"))
with open(os.path.join(ROOT, "results", "fake_error_pool.jsonl"), "w", encoding="utf-8") as f:
    for r in fake_pool: f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(txt); print("\nfake pool:", len(fake_pool))
