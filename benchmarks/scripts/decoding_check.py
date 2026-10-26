"""BuzzASR greedy (no repetition penalty) vs BuzzASR with its model-card settings
(no_repeat_ngram_size=3, repetition_penalty=1.2). Numbers only (KsponSpeech text never printed).

Runaway criterion A (used in the README): sentence kocer CER > 1 (errors exceed reference length).
Runaway criterion B (sensitivity check): hypothesis has >= 2x the characters of the reference (spaces removed).
"""
import json, os, re, sys
import numpy as np, kocer
sys.path.insert(0, os.path.dirname(__file__)); from common import ROOT

GREEDY, CARD = "buzzasr-korean", "_buzzasr-korean-cardgen"
OTHERS = ["qwen3-asr-1.7b-ko-univa-release", "qwen3-asr-1.7b-ko-univa", "qwen3-asr-1.7b", "whisper-large-v3",
          "sensevoice-small-itn", "sensevoice-small-noitn"]
PUBLIC = ["zeroth", "fleurs", "commonvoice"]; KSPON = ["kspon_clean", "kspon_other"]
_ws = re.compile(r"\s+")
def jl(p): return [json.loads(l) for l in open(p, encoding="utf-8")]
def en(m): return sum(m.ops.values()), m.ref_len  # kocer >= 0.4.0: 분모는 정답만으로 정해짐

ids = json.load(open(os.path.join(ROOT, "results", "common_ids.json"), encoding="utf-8"))
def pairs(ds):
    """[(ref, hyp_by_tag)] for a dataset, refs from data (spelling side for Kspon)."""
    if ds in KSPON + ["tel_hr"]:
        data = {r["id"]: r for r in jl(os.path.join(ROOT, "data", ds, "test.jsonl"))}; keys = sorted(data)
        ref = {k: data[k]["ref"] for k in keys}
    else:
        keys = ids[ds]; first = {r["id"]: r for r in jl(os.path.join(ROOT, "results", GREEDY, f"{ds}.jsonl"))}
        ref = {k: first[k]["ref"] for k in keys}
    hyp = {t: {r["id"]: r["hyp"] for r in jl(os.path.join(ROOT, "results", t, f"{ds}.jsonl"))} for t in [GREEDY, CARD] + OTHERS}
    return [(ref[k], {t: hyp[t][k] for t in hyp}) for k in keys]

def stats(rows, tag):
    a = []
    for r, h in rows:
        nP = en(kocer.measure(r, h[tag], numbers=False, letters=False)); k = en(kocer.measure(r, h[tag]))
        lr, lh = len(_ws.sub("", r)), len(_ws.sub("", h[tag]))
        a.append([nP[0], nP[1], k[0], k[1], int(k[1] > 0 and k[0] > k[1]), int(lr > 0 and lh >= 2 * lr)])
    return np.array(a, dtype=np.int64)

out = []; cache = {}
groups = {"KsponSpeech (clean+other, spelling ref)": KSPON, "Zeroth": ["zeroth"], "FLEURS": ["fleurs"], "Common Voice 27": ["commonvoice"], "AI-Hub telephone HR (spelling ref)": ["tel_hr"]}
for gname, dss in groups.items():
    rows = sum((pairs(d) for d in dss), [])
    S = {t: stats(rows, t) for t in [GREEDY, CARD] + OTHERS}; cache[gname] = S
    def cer(a, L): return a[:, L].sum() / a[:, L + 1].sum() * 100
    g, c = S[GREEDY], S[CARD]
    out.append(f"\n## {gname} ({len(rows)} utt.)\n")
    out.append("| BuzzASR decoding | nospace+punct CER | kocer CER | runaway A (CER>1) | runaway B (len>=2x) | kocer CER without A |")
    out.append("|---|---|---|---|---|---|")
    for name, a in [("greedy, no repetition penalty (published)", g), ("model-card settings", c)]:
        m = a[:, 4] == 0
        out.append(f"| {name} | {cer(a,0):.2f} | {cer(a,2):.2f} | {a[:,4].sum()} | {a[:,5].sum()} | {a[m,2].sum()/a[m,3].sum()*100:.2f} |")
    rng = np.random.default_rng(0); n = len(rows); idx = rng.integers(0, n, (2000, n))
    d = c[:, 2][idx].sum(1) / c[:, 3][idx].sum(1) - g[:, 2][idx].sum(1) / g[:, 3][idx].sum(1)
    lo, hi = np.percentile(d, [2.5, 97.5])
    out.append(f"\ncard - greedy, kocer: {cer(c,2)-cer(g,2):+.2f} pt [{lo*100:+.2f}, {hi*100:+.2f}]{' *' if lo > 0 or hi < 0 else ''}")
    ranked = sorted([(cer(S[t], 2), t) for t in OTHERS] + [(cer(g, 2), "BuzzASR greedy"), (cer(c, 2), "BuzzASR card settings")])
    out.append("kocer ranking with both BuzzASR runs: " + "; ".join(f"{i+1}. {t} {v:.2f}" for i, (v, t) in enumerate(ranked)))
    wh = S["whisper-large-v3"]; out.append(f"(whisper-large-v3 greedy runaway A/B: {wh[:,4].sum()}/{wh[:,5].sum()})")

txt = "\n".join(out)
open(os.path.join(ROOT, "results", "decoding_check.md"), "w", encoding="utf-8").write(txt + "\n")
print(txt)
