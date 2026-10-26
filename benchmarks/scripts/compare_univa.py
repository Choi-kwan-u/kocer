"""Beta vs release (and base) of TeamUNIVA Qwen3-ASR: scores at several normalization levels,
the model card's own normalization, number-writing habits, and a paired bootstrap release - beta."""
import json, os, re, sys, unicodedata
import numpy as np, kocer
sys.path.insert(0, os.path.dirname(__file__)); from common import ROOT

TAGS = {"base": "qwen3-asr-1.7b", "beta": "qwen3-asr-1.7b-ko-univa", "release": "qwen3-asr-1.7b-ko-univa-release"}
DS = ["zeroth", "fleurs", "commonvoice"]
ids = json.load(open(os.path.join(ROOT, "results", "common_ids.json"), encoding="utf-8"))
_ws = re.compile(r"\s+")
_punct = re.compile(r"[^\w\s]", re.UNICODE)

def card_norm(s, keep_space):
    # model card: "punctuation removed and case-folded"; spacing handling unstated -> both variants
    s = unicodedata.normalize("NFC", s).lower()
    s = _punct.sub("", s)
    s = _ws.sub(" " if keep_space else "", s).strip()
    return s

def en(m): return sum(m.ops.values()), m.ref_len  # kocer >= 0.4.0: 분모는 정답만으로 정해짐

LEVELS = ["raw", "card (punct+case, spaces kept)", "card + spaces removed", "kocer"]
def levels(ref, hyp):
    return [en(kocer.measure(ref, hyp, normalize=False)),
            en(kocer.measure(card_norm(ref, True), card_norm(hyp, True), normalize=False)),
            en(kocer.measure(card_norm(ref, False), card_norm(hyp, False), normalize=False)),
            en(kocer.measure(ref, hyp))]

def load(tag, ds):
    p = os.path.join(ROOT, "results", tag, f"{ds}.jsonl")
    rows = {json.loads(l)["id"]: json.loads(l) for l in open(p, encoding="utf-8")}
    return [rows[i] for i in ids[ds]]

arr, style = {}, {}
for name, tag in TAGS.items():
    for ds in DS:
        rows = load(tag, ds)
        arr[(name, ds)] = np.array([levels(r["ref"], r["hyp"]) for r in rows], dtype=np.int64)
        style[(name, ds)] = dict(digit=np.mean([bool(re.search(r"\d", r["hyp"])) for r in rows]),
                                 punct=np.mean([bool(re.search(r"[.,?!]", r["hyp"])) for r in rows]),
                                 empty=sum(not r["hyp"].strip() for r in rows))

def cer(a, L): return a[:, L, 0].sum() / a[:, L, 1].sum()
out = []
for L, lv in enumerate(LEVELS):
    out.append(f"\n## CER (%) — {lv}\n")
    out.append("| model | " + " | ".join(DS) + " | pooled |"); out.append("|---|" + "---|" * (len(DS) + 1))
    for name in TAGS:
        pooled = np.concatenate([arr[(name, d)] for d in DS])
        out.append(f"| {name} | " + " | ".join(f"{cer(arr[(name, d)], L)*100:.2f}" for d in DS) + f" | {cer(pooled, L)*100:.2f} |")

out.append("\n## Where raw errors go (pooled counts, share of raw)\n")
out.append("| model | raw errors | spacing+punct (card+space level) | numbers/letters (kocer only) | remaining |"); out.append("|---|---|---|---|---|")
for name in TAGS:
    p = np.concatenate([arr[(name, d)] for d in DS]); E = [int(p[:, L, 0].sum()) for L in range(4)]
    out.append(f"| {name} | {E[0]} | {E[0]-E[2]} ({(E[0]-E[2])/E[0]*100:.0f}%) | {E[2]-E[3]} ({(E[2]-E[3])/E[0]*100:.0f}%) | {E[3]} ({E[3]/E[0]*100:.0f}%) |")

out.append("\n## Number-writing habit: share of hypotheses containing a digit / punctuation\n")
out.append("| model | " + " | ".join(f"{d} digit | {d} punct" for d in DS) + " |"); out.append("|---|" + "---|" * (2 * len(DS)))
for name in TAGS:
    out.append(f"| {name} | " + " | ".join(f"{style[(name,d)]['digit']*100:.1f}% | {style[(name,d)]['punct']*100:.1f}%" for d in DS) + " |")

out.append("\n## Paired bootstrap, release - beta and release - base (2,000 resamples, seed 0, sentence level)\n")
out.append("| comparison | level | " + " | ".join(DS) + " | pooled |"); out.append("|---|---|" + "---|" * (len(DS) + 1))
rng = np.random.default_rng(0)
def boot(a, b, L):
    n = len(a); idx = rng.integers(0, n, (2000, n))
    d = a[:, L, 0][idx].sum(1) / a[:, L, 1][idx].sum(1) - b[:, L, 0][idx].sum(1) / b[:, L, 1][idx].sum(1)
    lo, hi = np.percentile(d, [2.5, 97.5]); pt = cer(a, L) - cer(b, L)
    return f"{pt*100:+.2f} [{lo*100:+.2f},{hi*100:+.2f}]{'*' if lo > 0 or hi < 0 else ''}"
for other in ["beta", "base"]:
    for L in [0, 2, 3]:
        cells = [boot(arr[("release", d)], arr[(other, d)], L) for d in DS]
        pa = np.concatenate([arr[("release", d)] for d in DS]); pb = np.concatenate([arr[(other, d)] for d in DS])
        cells.append(boot(pa, pb, L))
        out.append(f"| release - {other} | {LEVELS[L]} | " + " | ".join(cells) + " |")

txt = "\n".join(out)
open(os.path.join(ROOT, "results", "univa_compare.md"), "w", encoding="utf-8").write(txt + "\n")
print(txt)
