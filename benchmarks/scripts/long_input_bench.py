"""Speed and memory of kocer on long inputs (issue #1). Public Zeroth references concatenated, ~5% character noise.
usage: long_input_bench.py [label]"""
import json, os, random, sys, time, tracemalloc
import kocer
sys.path.insert(0, os.path.dirname(__file__)); from common import ROOT

refs = [json.loads(l)["ref"] for l in open(os.path.join(ROOT, "results", "whisper-large-v3", "zeroth.jsonl"), encoding="utf-8")]
text = " ".join(refs)
rng = random.Random(0)


def noisy(s):
    out = []
    for c in s:
        r = rng.random()
        if r < 0.02: continue
        if r < 0.04: out.append("가"); continue
        out.append(c)
        if r > 0.99: out.append("나")
    return "".join(out)


label = sys.argv[1] if len(sys.argv) > 1 else kocer.__version__
for n in (2050, 8200):
    ref = text[:n]; hyp = noisy(ref)
    for name, fn in (("measure", lambda: kocer.measure(ref, hyp)), ("breakdown", lambda: kocer.breakdown([ref], [hyp]))):
        tracemalloc.start(); t = time.perf_counter(); r = fn(); dt = time.perf_counter() - t
        peak = tracemalloc.get_traced_memory()[1] / 2**20; tracemalloc.stop()
        err = r.errors if name == "measure" else r.remaining
        print(f"{label} {name:9s} {n:5d} chars: {dt:6.2f} s, peak {peak:7.1f} MB, errors {err}")
