"""0.5.0 check (#7): kocer must never count more errors than the same text scored with numbers and letters off.
Every scored pair of the benchmark (7 settings; public sets; KsponSpeech and telephone with both references).
Numbers only. Output: results/never_worse.md"""
import json, os, sys
import kocer
sys.path.insert(0, os.path.dirname(__file__)); from common import ROOT

TAGS = ["qwen3-asr-1.7b-ko-univa-release", "qwen3-asr-1.7b-ko-univa", "qwen3-asr-1.7b", "buzzasr-korean",
        "whisper-large-v3", "sensevoice-small-itn", "sensevoice-small-noitn"]


def jl(p): return [json.loads(l) for l in open(p, encoding="utf-8")]


def pairs():
    ids = json.load(open(os.path.join(ROOT, "results", "common_ids.json"), encoding="utf-8"))
    for ds in ["zeroth", "fleurs", "commonvoice"]:
        keep = set(ids[ds])
        for t in TAGS:
            for r in jl(os.path.join(ROOT, "results", t, f"{ds}.jsonl")):
                if r["id"] in keep:
                    yield ds, t, r["id"], r["ref"], r["hyp"]
    for ds in ["kspon_clean", "kspon_other", "tel_hr"]:
        data = {r["id"]: r for r in jl(os.path.join(ROOT, "data", ds, "test.jsonl"))}
        for t in TAGS:
            for r in jl(os.path.join(ROOT, "results", t, f"{ds}.jsonl")):
                for side in ("ref", "ref_pron"):
                    yield f"{ds} {side}", t, r["id"], data[r["id"]][side], r["hyp"]


n = 0; worse = []
for ds, t, i, ref, hyp in pairs():
    n += 1
    k = kocer.measure(ref, hyp).errors; o = kocer.measure(ref, hyp, numbers=False, letters=False).errors
    if k > o:
        worse.append((ds, t, i, k, o))
out = [f"# kocer {kocer.__version__}: pairs where kocer counts more errors than with numbers and letters off\n",
       f"{n:,} scored pairs checked; {len(worse)} worse."]
out += [f"- {ds} / {t} / {i}: kocer {k} vs off {o}" for ds, t, i, k, o in worse[:20]]
txt = "\n".join(out)
open(os.path.join(ROOT, "results", "never_worse.md"), "w", encoding="utf-8").write(txt + "\n")
print(txt)
