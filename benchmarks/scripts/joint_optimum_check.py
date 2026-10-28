"""Issue #3: how often does kocer's sequential candidate choice miss the joint optimum?
kocer picks hypothesis candidates against the raw reference first, then reference candidates against the chosen
hypothesis (and, past 64 combinations, one span at a time). Here every combination of reference candidates x
hypothesis candidates is tried, when there are at most CAP of them, and the minimum error count is compared with
kocer's. Numbers only (AI-Hub sets included). Output: results/joint_optimum.md"""
import json, os, sys
from itertools import product
import kocer
from kocer import numbers as N
from kocer.normalize import ALIASES, normalize as norm
from kocer.align import distance
sys.path.insert(0, os.path.dirname(__file__)); from common import ROOT

CAP = 20000
TAGS = ["qwen3-asr-1.7b-ko-univa-release", "qwen3-asr-1.7b-ko-univa", "qwen3-asr-1.7b", "buzzasr-korean",
        "whisper-large-v3", "sensevoice-small-itn", "sensevoice-small-noitn"]
TABLE = dict(ALIASES)


def jl(p): return [json.loads(l) for l in open(p, encoding="utf-8")]


def expansions(text):
    spans = N._spans(text, True, TABLE)
    total = 1
    for _, _, o in spans:
        total *= len(o)
    return spans, total


def joint_min(ref, hyp):
    r, h = norm(ref), norm(hyp)
    rs, rt = expansions(r); hs, ht = expansions(h)
    if rt == 1 and ht == 1:
        return None, 1  # nothing to choose
    if rt * ht > CAP:
        return None, rt * ht
    rc = [list(N._build(r, rs, c).replace(" ", "")) for c in product(*(o for _, _, o in rs))]
    hc = [list(N._build(h, hs, c).replace(" ", "")) for c in product(*(o for _, _, o in hs))]
    return min(distance(a, b) for a in rc for b in hc), rt * ht


def pairs():
    ids = json.load(open(os.path.join(ROOT, "results", "common_ids.json"), encoding="utf-8"))
    for ds in ["zeroth", "fleurs", "commonvoice"]:
        keep = set(ids[ds])
        for t in TAGS:
            for r in jl(os.path.join(ROOT, "results", t, f"{ds}.jsonl")):
                if r["id"] in keep:
                    yield ds, t, r["ref"], r["hyp"]
    for ds in ["kspon_clean", "kspon_other", "tel_hr"]:
        data = {r["id"]: r for r in jl(os.path.join(ROOT, "data", ds, "test.jsonl"))}
        for t in TAGS:
            for r in jl(os.path.join(ROOT, "results", t, f"{ds}.jsonl")):
                for side in ("ref", "ref_pron"):
                    yield f"{ds} ({'spelling' if side == 'ref' else 'pronunciation'})", t, data[r["id"]][side], r["hyp"]


stats = {}
for ds, t, ref, hyp in pairs():
    s = stats.setdefault(ds, dict(pairs=0, choice=0, checked=0, over_cap=0, missed=0, excess=0, max_excess=0, ref_len=0, per={}))
    s["pairs"] += 1
    m = kocer.measure(ref, hyp)
    s["ref_len"] += m.ref_len
    pm = s["per"].setdefault(t, [0, 0]); pm[1] += m.ref_len
    jm, combos = joint_min(ref, hyp)
    if combos == 1:
        continue
    s["choice"] += 1
    if jm is None:
        s["over_cap"] += 1
        continue
    s["checked"] += 1
    if m.errors > jm:
        s["missed"] += 1; s["excess"] += m.errors - jm; s["max_excess"] = max(s["max_excess"], m.errors - jm); pm[0] += m.errors - jm

out = [f"# Sequential candidate choice vs joint optimum (kocer {kocer.__version__}, issue #3)\n",
       f"Joint optimum = minimum error count over every reference-candidate x hypothesis-candidate combination, "
       f"checked when there are at most {CAP:,} combinations. Seven settings, every scored pair (KsponSpeech and telephone: both references).\n",
       "| set | scored pairs | with a choice to make | checked | too many combinations | kocer above optimum | extra errors (total / max per sentence) | corpus CER overstated by (largest setting) |",
       "|---|---|---|---|---|---|---|---|"]
T = dict(pairs=0, choice=0, checked=0, over_cap=0, missed=0, excess=0, max_excess=0)
for ds, s in stats.items():
    out.append(f"| {ds} | {s['pairs']:,} | {s['choice']:,} | {s['checked']:,} | {s['over_cap']:,} | {s['missed']:,} | "
               f"{s['excess']} / {s['max_excess']} | {max(e / n for e, n in s['per'].values()) * 100:.3f} pt |")
    for k in T:
        T[k] = max(T[k], s[k]) if k == "max_excess" else T[k] + s[k]
out.append(f"| **all** | {T['pairs']:,} | {T['choice']:,} | {T['checked']:,} | {T['over_cap']:,} | {T['missed']:,} | {T['excess']} / {T['max_excess']} | |")
txt = "\n".join(out)
open(os.path.join(ROOT, "results", "joint_optimum.md"), "w", encoding="utf-8").write(txt + "\n")
print(txt)
