"""Score KsponSpeech eval (clean + other) for all settings, against BOTH references:
  spelling side  "(3시)/(세 시)" -> "3시"   and   pronunciation side -> "세 시".
Prints/writes numbers only (AI-Hub terms: no transcript text leaves this machine).
Outputs:
  results/kspon_tables.md          numbers only, safe to publish
  data/kspon_review/pool.jsonl     raw>0 & kocer==0 sentences (contains text, LOCAL ONLY)
"""
import json, os, re, sys
import numpy as np, kocer
sys.path.insert(0, os.path.dirname(__file__)); from common import ROOT

SPLITS = ["kspon_clean", "kspon_other"]
PUBLIC = ["zeroth", "fleurs", "commonvoice"]
REFS = {"spelling": "ref", "pronunciation": "ref_pron"}
LEVELS = ["raw", "nospace", "nopunct", "kocer", "kocer+fillers"]
_ws = re.compile(r"\s+")

def en(m): return sum(m.ops.values()), m.hits + m.ops["S"] + m.ops["D"]
def levels(ref, hyp):
    return [en(kocer.measure(ref, hyp, normalize=False)),
            en(kocer.measure(_ws.sub("", ref), _ws.sub("", hyp), normalize=False)),
            en(kocer.measure(ref, hyp, numbers=False, letters=False)),
            en(kocer.measure(ref, hyp)),
            en(kocer.measure(ref, hyp, fillers=True))]

def jl(p): return [json.loads(l) for l in open(p, encoding="utf-8")]
tags = sorted(t for t in os.listdir(os.path.join(ROOT, "results")) if not t.startswith("_")  # "_" = auxiliary runs
              if all(os.path.exists(os.path.join(ROOT, "results", t, f"{s}.jsonl")) for s in SPLITS))
if not tags:
    sys.exit("no model has results for both kspon splits yet")
print("models:", tags)

arr = {}          # (tag, split, refkind) -> (n, levels, 2)
pool = []
for s in SPLITS:
    data = {r["id"]: r for r in jl(os.path.join(ROOT, "data", s, "test.jsonl"))}
    hyps = {t: {r["id"]: r["hyp"] for r in jl(os.path.join(ROOT, "results", t, f"{s}.jsonl"))} for t in tags}
    ids = sorted(set(data).intersection(*[set(h) for h in hyps.values()]))
    ids = [i for i in ids if all(hyps[t][i].strip() for t in tags) and data[i]["ref"].strip()]
    print(f"[{s}] usable={len(ids)} of {len(data)}")
    for t in tags:
        for rk, field in REFS.items():
            a = np.array([levels(data[i][field], hyps[t][i]) for i in ids], dtype=np.int64)
            arr[(t, s, rk)] = a
            if rk == "spelling":
                for i, row in zip(ids, a):
                    if row[0][0] > 0 and row[3][0] == 0:
                        pool.append({"model": t, "dataset": s, "id": i, "ref": data[i]["ref"], "ref_pron": data[i]["ref_pron"], "hyp": hyps[t][i]})

def cer(a, L): return a[:, L, 0].sum() / a[:, L, 1].sum()
def both(t, rk): return np.concatenate([arr[(t, s, rk)] for s in SPLITS])
out = [f"# KsponSpeech eval (clean + other), {sum(len(arr[(tags[0], s, 'spelling')]) for s in SPLITS)} utterances. Numbers only.\n"]

for rk in REFS:
    out.append(f"\n## Reference = {rk} side. CER (%) per level\n")
    out.append("| model | split | " + " | ".join(LEVELS) + " |"); out.append("|---|---|" + "---|" * len(LEVELS))
    for t in sorted(tags, key=lambda t: cer(both(t, rk), 3)):
        for s in SPLITS + ["both"]:
            a = both(t, rk) if s == "both" else arr[(t, s, rk)]
            out.append(f"| {t} | {s} | " + " | ".join(f"{cer(a, L)*100:.2f}" for L in range(len(LEVELS))) + " |")

out.append("\n## Reference choice sensitivity (clean+other): spelling vs pronunciation reference\n")
out.append("| model | raw spelling | raw pron | gap | nopunct spelling | nopunct pron | gap | kocer spelling | kocer pron | gap |")
out.append("|---|---|---|---|---|---|---|---|---|---|")
for t in sorted(tags, key=lambda t: cer(both(t, "spelling"), 3)):
    c = {(rk, L): cer(both(t, rk), L) * 100 for rk in REFS for L in (0, 2, 3)}
    out.append(f"| {t} | " + " | ".join(f"{c[('spelling', L)]:.2f} | {c[('pronunciation', L)]:.2f} | {c[('pronunciation', L)] - c[('spelling', L)]:+.2f}" for L in (0, 2, 3)) + " |")

out.append("\n## Ranks (clean+other) by reference and level\n")
out.append("| model | " + " | ".join(f"{rk[:5]} {LEVELS[L]}" for rk in REFS for L in (0, 2, 3)) + " |"); out.append("|---|" + "---|" * 6)
rank = {}
for rk in REFS:
    for L in (0, 2, 3):
        v = {t: cer(both(t, rk), L) for t in tags}; o = sorted(v, key=v.get)
        for t in tags: rank[(t, rk, L)] = o.index(t) + 1
for t in sorted(tags, key=lambda t: rank[(t, "spelling", 3)]):
    out.append(f"| {t} | " + " | ".join(str(rank[(t, rk, L)]) for rk in REFS for L in (0, 2, 3)) + " |")

out.append("\n## Where raw errors go (clean+other, spelling reference; counts, share of raw)\n")
out.append("| model | raw errors | spacing | punctuation | numbers/letters (kocer only) | fillers (extra) | remaining |"); out.append("|---|---|---|---|---|---|---|")
for t in sorted(tags, key=lambda t: cer(both(t, "spelling"), 3)):
    a = both(t, "spelling"); E = [int(a[:, L, 0].sum()) for L in range(len(LEVELS))]
    f = lambda x: f"{x} ({x / E[0] * 100:.0f}%)"
    out.append(f"| {t} | {E[0]} | {f(E[0]-E[1])} | {f(E[1]-E[2])} | {f(E[2]-E[3])} | {f(E[3]-E[4])} | {f(E[4])} |")

# pairwise paired bootstrap at kocer level: (a) Kspon only, (b) Kspon + the three public sets
def public_arr(t):
    ids = json.load(open(os.path.join(ROOT, "results", "common_ids.json"), encoding="utf-8"))
    rows = []
    for d in PUBLIC:
        p = os.path.join(ROOT, "results", t, f"{d}.jsonl")
        if not os.path.exists(p): return None
        r = {x["id"]: x for x in jl(p)}
        rows += [levels(r[i]["ref"], r[i]["hyp"]) for i in ids[d]]
    return np.array(rows, dtype=np.int64)
pub = {t: public_arr(t) for t in tags}
rng = np.random.default_rng(0)
for label, getter in [("KsponSpeech only (spelling ref)", lambda t: both(t, "spelling")),
                      ("Kspon + Zeroth + FLEURS + CV27 (spelling ref for Kspon)", lambda t: np.concatenate([both(t, "spelling"), pub[t]]) if pub[t] is not None else None)]:
    A = {t: getter(t) for t in tags}
    if any(v is None for v in A.values()):
        continue
    n = len(next(iter(A.values()))); idx = rng.integers(0, n, (2000, n))
    B = {t: A[t][:, 3, 0][idx].sum(1) / A[t][:, 3, 1][idx].sum(1) for t in tags}
    order = sorted(tags, key=lambda t: cer(A[t], 3))
    out.append(f"\n## Pairwise paired bootstrap, kocer level — {label}, n={n}. CER(row) - CER(col), %p, 95% CI, * = excludes 0\n")
    out.append("| | " + " | ".join(t[:16] for t in order) + " |"); out.append("|---|" + "---|" * len(order))
    for a in order:
        cells = []
        for b in order:
            if a == b: cells.append("."); continue
            d = B[a] - B[b]; lo, hi = np.percentile(d, [2.5, 97.5]); pt = cer(A[a], 3) - cer(A[b], 3)
            cells.append(f"{pt*100:+.2f} [{lo*100:+.2f},{hi*100:+.2f}]{'*' if lo > 0 or hi < 0 else ''}")
        out.append(f"| {a[:16]} | " + " | ".join(cells) + " |")
    M = np.stack([B[t] for t in order], 1); R = M.argsort(1).argsort(1) + 1
    out.append("\nRank intervals: " + "; ".join(f"{t} [{int(np.percentile(R[:, j], 2.5))}, {int(np.percentile(R[:, j], 97.5))}] P(1st)={np.mean(R[:, j] == 1):.2f}" for j, t in enumerate(order)))

txt = "\n".join(out)
open(os.path.join(ROOT, "results", "kspon_tables.md"), "w", encoding="utf-8").write(txt + "\n")
os.makedirs(os.path.join(ROOT, "data", "kspon_review"), exist_ok=True)
with open(os.path.join(ROOT, "data", "kspon_review", "pool.jsonl"), "w", encoding="utf-8") as f:
    for r in pool: f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(txt)
print(f"\nreview pool (local only): {len(pool)} rows -> data/kspon_review/pool.jsonl")
