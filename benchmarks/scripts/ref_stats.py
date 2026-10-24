"""Section 1 table: share of reference sentences containing digits / Latin letters / punctuation."""
import json, re, sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
names = sys.argv[1:] or ["zeroth", "fleurs", "commonvoice"]
print("| dataset | n | has digit | has Latin | has punct [.,?!] | avg ref chars |")
print("|---|---|---|---|---|---|")
for n in names:
    p = os.path.join(ROOT, "data", n, "test.jsonl")
    if not os.path.exists(p): print(f"| {n} | (missing) |"); continue
    refs = [json.loads(l)["ref"] for l in open(p, encoding="utf-8")]
    N = len(refs)
    def share(rx): return 100 * sum(bool(re.search(rx, t)) for t in refs) / N
    d, a, pu = share(r"\d"), share(r"[A-Za-z]"), share(r"[.,?!]")
    avg = sum(len(t) for t in refs) / N
    print(f"| {n} | {N} | {d:.1f}% | {a:.1f}% | {pu:.1f}% | {avg:.1f} |")
