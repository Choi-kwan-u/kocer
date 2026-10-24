"""4.4: sample 100 sentences with raw>0 and kocer==0 from results/fake_error_pool.jsonl -> results/fake_review.tsv
Columns: idx, model, dataset, id, ref, hyp, verdict (fill: 1=표기차이만 2=실제오류숨김 3=애매), note"""
import json, random, os, sys
sys.path.insert(0, os.path.dirname(__file__)); from common import ROOT
SEED = 20261024
pool = [json.loads(l) for l in open(os.path.join(ROOT, "results", "fake_error_pool.jsonl"), encoding="utf-8")]
# dedupe identical (ref,hyp) pairs so the same sentence from two models is not reviewed twice
seen = set(); uniq = []
for r in pool:
    k = (r["ref"], r["hyp"].strip())
    if k in seen: continue
    seen.add(k); uniq.append(r)
random.Random(SEED).shuffle(uniq)
sample = uniq[:100]
with open(os.path.join(ROOT, "results", "fake_review.tsv"), "w", encoding="utf-8") as f:
    f.write("idx\tmodel\tdataset\tid\tref\thyp\tverdict\tnote\n")
    for i, r in enumerate(sample, 1):
        f.write(f"{i}\t{r['model']}\t{r['dataset']}\t{r['id']}\t{r['ref']}\t{r['hyp'].strip()}\t\t\n")
print(f"pool={len(pool)} unique={len(uniq)} sampled={len(sample)} seed={SEED}")
