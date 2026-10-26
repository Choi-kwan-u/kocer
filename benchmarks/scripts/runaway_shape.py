"""Shape of BuzzASR runaway outputs on KsponSpeech (numbers only; no transcript text is printed).
Criterion A: sentence kocer errors > normalized reference length.
usage: runaway_shape.py [tag=buzzasr-korean] [tag2=_buzzasr-korean-cardgen]"""
import json, os, re, sys, statistics as st
import kocer
sys.path.insert(0, os.path.dirname(__file__)); from common import ROOT

TAG = sys.argv[1] if len(sys.argv) > 1 else "buzzasr-korean"
TAG2 = sys.argv[2] if len(sys.argv) > 2 else "_buzzasr-korean-cardgen"
_ws = re.compile(r"\s+")
def jl(p): return [json.loads(l) for l in open(p, encoding="utf-8")]

# raw transcripts for tag statistics (never printed)
raw = {}
for name in ["eval_clean", "eval_other"]:
    for line in open(os.path.join(ROOT, "data", "_kspon_raw", "scripts", f"{name}.trn"), encoding="utf-8"):
        if " :: " in line:
            p, t = line.rstrip("\n").split(" :: ", 1)
            raw[os.path.basename(p).rsplit(".", 1)[0]] = t
TAGS = {"noise b/": r"(?<![A-Za-z])b/", "noise n/": r"(?<![A-Za-z])n/", "noise o/": r"(?<![A-Za-z])o/",
        "laugh l/": r"(?<![A-Za-z])l/", "unknown u/": r"(?<![A-Za-z])u/", "filler x/": r"(?<=[가-힣])/",
        "repeat +": r"\+", "unclear *": r"\*"}

def period(s):
    """Shortest unit u (len>=2) such that s ends with u repeated k>=3 times; returns (len(u), k, covered chars) best by coverage."""
    best = (0, 0, 0)
    n = len(s)
    for L in range(2, min(60, n // 3) + 1):
        u = s[-L:]; k = 1
        while k * L + L <= n and s[-(k + 1) * L:-k * L] == u:
            k += 1
        if k >= 3 and k * L > best[2]:
            best = (L, k, k * L)
    return best

def shape(ref, hyp):
    r, h = _ws.sub("", ref), _ws.sub("", hyp)
    L, k, cov = period(h)
    pre = h[:len(r)]
    pre_cer = kocer.cer(r, pre) if r else 1.0
    unit_in_ref = (h[-L:] in r) if L else False
    return dict(rlen=len(r), hlen=len(h), ratio=len(h) / max(len(r), 1), unit=L, reps=k, cover=cov / max(len(h), 1),
                prefix_cer=pre_cer, unit_in_ref=unit_in_ref)

rows_all = []
for ds in ["kspon_clean", "kspon_other"]:
    data = {x["id"]: x for x in jl(os.path.join(ROOT, "data", ds, "test.jsonl"))}
    hyp = {x["id"]: x["hyp"] for x in jl(os.path.join(ROOT, "results", TAG, f"{ds}.jsonl"))}
    hyp2 = {x["id"]: x["hyp"] for x in jl(os.path.join(ROOT, "results", TAG2, f"{ds}.jsonl"))} if os.path.exists(os.path.join(ROOT, "results", TAG2, f"{ds}.jsonl")) else {}
    for i, d in data.items():
        m = kocer.measure(d["ref"], hyp[i]); n = m.ref_len
        run = m.errors > n
        m2 = kocer.measure(d["ref"], hyp2[i]) if i in hyp2 else None
        run2 = (m2.errors > m2.ref_len) if m2 else None
        rows_all.append(dict(id=i, ds=ds, dur=d["dur"], run=run, run2=run2, errors=m.errors, n=n,
                             **shape(d["ref"], hyp[i]), tags={k: len(re.findall(v, raw.get(i, ""))) for k, v in TAGS.items()}))

R = [x for x in rows_all if x["run"]]
print(f"{TAG}: runaway A = {len(R)} / {len(rows_all)}  (clean {sum(x['ds']=='kspon_clean' for x in R)}, other {sum(x['ds']=='kspon_other' for x in R)})")
if any(x["run2"] is not None for x in rows_all):
    print(f"  card settings: runaway {sum(bool(x['run2']) for x in rows_all)}; overlap with greedy set {sum(bool(x['run2']) for x in R)}; new in card {sum(bool(x['run2']) and not x['run'] for x in rows_all)}")
rep = [x for x in R if x["reps"] >= 3 and x["cover"] >= 0.5]
tail = [x for x in R if x["prefix_cer"] <= 0.3]
print(f"  pattern: >=50% of output is one unit repeated >=3 times: {len(rep)}; unit length chars median {st.median([x['unit'] for x in rep]) if rep else '-'}, repeats median {st.median([x['reps'] for x in rep]) if rep else '-'}")
print(f"           unit also occurs in the reference: {sum(x['unit_in_ref'] for x in rep)} of {len(rep)}")
print(f"           prefix (first ref-length chars) CER <= 0.3, i.e. correct start then continues: {len(tail)}")
print(f"           neither (garbled throughout): {sum(1 for x in R if x not in rep and x not in tail)}")
print(f"  output / reference length ratio: mean {st.mean([x['ratio'] for x in R]):.1f}, median {st.median([x['ratio'] for x in R]):.1f}, min {min(x['ratio'] for x in R):.1f}, max {max(x['ratio'] for x in R):.1f}")
print(f"  reference length chars: median {st.median([x['rlen'] for x in R])}, min {min(x['rlen'] for x in R)}, max {max(x['rlen'] for x in R)}  (all 6000: median {st.median([x['rlen'] for x in rows_all])})")
print(f"  duration s: median {st.median([x['dur'] for x in R]):.1f}, min {min(x['dur'] for x in R):.1f}, max {max(x['dur'] for x in R):.1f}  (all 6000: median {st.median([x['dur'] for x in rows_all]):.1f}, >20 s share {sum(x['dur']>20 for x in rows_all)/len(rows_all):.0%})")
print(f"  duration buckets runaway: <5 s {sum(x['dur']<5 for x in R)}, 5-10 {sum(5<=x['dur']<10 for x in R)}, 10-20 {sum(10<=x['dur']<20 for x in R)}, >=20 {sum(x['dur']>=20 for x in R)}")
print(f"  hyp length chars: median {st.median([x['hlen'] for x in R])}, max {max(x['hlen'] for x in R)}")
print("  raw-transcript tags, share of utterances containing (runaway vs all 6000):")
for k in TAGS:
    a = sum(x["tags"][k] > 0 for x in R) / len(R); b = sum(x["tags"][k] > 0 for x in rows_all) / len(rows_all)
    print(f"    {k:12s} {a:5.0%}  vs {b:5.0%}")
print(f"  share of kocer errors from runaways: {sum(x['errors'] for x in R) / sum(x['errors'] for x in rows_all):.1%}")
