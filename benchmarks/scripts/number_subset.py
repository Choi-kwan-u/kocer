"""How big is the kocer effect on utterances that actually contain numbers? (numbers only printed)
Subsets, chosen from references where possible:
  FLEURS        : reference contains a digit
  KsponSpeech   : spelling reference contains a digit (the dual-notation number cases)
  Zeroth        : references never contain digits (numbers are spelled in Hangul), so we use
                  "at least one of the 7 systems wrote a digit" as a proxy for a spoken number
Common Voice has almost no numbers and is skipped."""
import json, os, re, sys
import numpy as np, kocer
sys.path.insert(0, os.path.dirname(__file__)); from common import ROOT

TAGS = ["qwen3-asr-1.7b-ko-univa-release", "qwen3-asr-1.7b-ko-univa", "qwen3-asr-1.7b", "buzzasr-korean",
        "whisper-large-v3", "sensevoice-small-itn", "sensevoice-small-noitn"]
def jl(p): return [json.loads(l) for l in open(p, encoding="utf-8")]
def en(m): return sum(m.ops.values()), m.hits + m.ops["S"] + m.ops["D"]
digit = re.compile(r"\d")

sets = {}
ids = json.load(open(os.path.join(ROOT, "results", "common_ids.json"), encoding="utf-8"))
for ds in ["zeroth", "fleurs"]:
    hyp = {t: {r["id"]: r for r in jl(os.path.join(ROOT, "results", t, f"{ds}.jsonl"))} for t in TAGS}
    keep = []
    for i in ids[ds]:
        ref = hyp[TAGS[0]][i]["ref"]
        if ds == "fleurs" and digit.search(ref): keep.append(i)
        if ds == "zeroth" and any(digit.search(hyp[t][i]["hyp"]) for t in TAGS): keep.append(i)
    sets[ds] = [(hyp[TAGS[0]][i]["ref"], {t: hyp[t][i]["hyp"] for t in TAGS}) for i in keep]
for refkind, field in [("kspon (spelling ref)", "ref"), ("kspon (pronunciation ref)", "ref_pron")]:
    rows = []
    for s in ["kspon_clean", "kspon_other"]:
        data = {r["id"]: r for r in jl(os.path.join(ROOT, "data", s, "test.jsonl"))}
        hyp = {t: {r["id"]: r["hyp"] for r in jl(os.path.join(ROOT, "results", t, f"{s}.jsonl"))} for t in TAGS}
        for i, d in data.items():
            if digit.search(d["ref"]):
                rows.append((d[field], {t: hyp[t][i] for t in TAGS}))
    sets[refkind] = rows

out = []
for name, rows in sets.items():
    A = {t: np.array([[en(kocer.measure(r, h[t], numbers=False, letters=False)), en(kocer.measure(r, h[t]))] for r, h in rows]) for t in TAGS}
    out.append(f"\n## {name}: {len(rows)} utterances with numbers\n")
    out.append("| model | nospace+punct CER | kocer CER | drop | rank nopunct -> kocer |"); out.append("|---|---|---|---|---|")
    c = {t: [A[t][:, L, 0].sum() / A[t][:, L, 1].sum() * 100 for L in (0, 1)] for t in TAGS}
    r0 = sorted(TAGS, key=lambda t: c[t][0]); r1 = sorted(TAGS, key=lambda t: c[t][1])
    for t in r1:
        out.append(f"| {t} | {c[t][0]:.2f} | {c[t][1]:.2f} | {c[t][0]-c[t][1]:.2f} | {r0.index(t)+1} -> {r1.index(t)+1} |")
    rng = np.random.default_rng(0); n = len(rows); idx = rng.integers(0, n, (2000, n))
    def boot(a, b, L):
        d = A[a][:, L, 0][idx].sum(1) / A[a][:, L, 1][idx].sum(1) - A[b][:, L, 0][idx].sum(1) / A[b][:, L, 1][idx].sum(1)
        lo, hi = np.percentile(d, [2.5, 97.5]); pt = c[a][L] - c[b][L]
        return f"{pt:+.2f} [{lo*100:+.2f},{hi*100:+.2f}]{'*' if lo > 0 or hi < 0 else ''}"
    out.append(f"\nversion check, fine-tune minus base (negative = fine-tune better): "
               f"beta-base nopunct {boot('qwen3-asr-1.7b-ko-univa','qwen3-asr-1.7b',0)} | kocer {boot('qwen3-asr-1.7b-ko-univa','qwen3-asr-1.7b',1)}; "
               f"release-base nopunct {boot('qwen3-asr-1.7b-ko-univa-release','qwen3-asr-1.7b',0)} | kocer {boot('qwen3-asr-1.7b-ko-univa-release','qwen3-asr-1.7b',1)}")
txt = "\n".join(out)
open(os.path.join(ROOT, "results", "number_subset.md"), "w", encoding="utf-8").write(txt + "\n")
print(txt)
