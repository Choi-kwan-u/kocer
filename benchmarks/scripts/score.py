"""Score results/*/{dataset}.jsonl -> results/scores.json + markdown tables.
Corpus CER = total errors / total reference chars (pooled), same for all three columns.
Sample set = ids present (non-error) in ALL model files for that dataset."""
import json, os, sys, glob, random
import kocer, nlptutti
from nlptutti import compare_systems
sys.path.insert(0, os.path.dirname(__file__)); from common import ROOT

def load(p): return {r["id"]: r for r in (json.loads(l) for l in open(p, encoding="utf-8"))}

def pooled_raw_and_kocer(refs, hyps):
    raw_e = raw_n = ko_e = ko_n = 0
    per = []
    for r, h in zip(refs, hyps):
        m_raw = kocer.measure(r, h, normalize=False); m_ko = kocer.measure(r, h)
        e_raw = sum(m_raw.ops.values()); n_raw = m_raw.hits + m_raw.ops["S"] + m_raw.ops["D"]
        e_ko = sum(m_ko.ops.values()); n_ko = m_ko.hits + m_ko.ops["S"] + m_ko.ops["D"]
        raw_e += e_raw; raw_n += n_raw; ko_e += e_ko; ko_n += n_ko
        per.append(dict(raw=m_raw.cer, kocer=m_ko.cer, raw_err=e_raw, raw_n=n_raw, ko_err=e_ko, ko_n=n_ko))
    return raw_e / raw_n, ko_e / ko_n, per

def nlptutti_micro(refs, hyps):
    rep = compare_systems(refs, {"m": hyps, "_dup": hyps}, rate_mode="standard")  # needs >=2 systems
    return rep["systems"][0]["metrics"]["cer"]["micro"]

if __name__ == "__main__":
    datasets = sys.argv[1:] or ["zeroth", "fleurs", "commonvoice"]
    tags = sorted(d for d in os.listdir(os.path.join(ROOT, "results")) if os.path.isdir(os.path.join(ROOT, "results", d)))
    scores = {}; fake_pool = []; common_ids = {}
    for ds in datasets:
        files = {t: os.path.join(ROOT, "results", t, f"{ds}.jsonl") for t in tags}
        files = {t: p for t, p in files.items() if os.path.exists(p)}
        if not files: continue
        data = {t: load(p) for t, p in files.items()}
        common = set.intersection(*(set(d) for d in data.values()))
        common = {i for i in common if all(data[t][i]["hyp"].strip() for t in data)}
        ids = sorted(common); common_ids[ds] = ids
        print(f"[{ds}] models={len(data)} common ids={len(ids)}")
        for t in data:
            refs = [data[t][i]["ref"] for i in ids]; hyps = [data[t][i]["hyp"] for i in ids]
            raw, ko, per = pooled_raw_and_kocer(refs, hyps)
            nt = nlptutti_micro(refs, hyps)
            scores.setdefault(t, {})[ds] = dict(raw=raw, nlptutti=nt, kocer=ko, n=len(ids),
                                                raw_err=sum(p["raw_err"] for p in per), raw_n=sum(p["raw_n"] for p in per),
                                                ko_err=sum(p["ko_err"] for p in per), ko_n=sum(p["ko_n"] for p in per))
            for i, p in zip(ids, per):
                if p["raw"] > 0 and p["kocer"] == 0:
                    fake_pool.append(dict(model=t, dataset=ds, id=i, ref=data[t][i]["ref"], hyp=data[t][i]["hyp"]))
            print(f"  {t:28s} raw={raw*100:6.2f}  nlptutti={nt*100:6.2f}  kocer={ko*100:6.2f}  fake%={(raw-ko)/raw*100:5.1f}")
    json.dump(scores, open(os.path.join(ROOT, "results", "scores.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(common_ids, open(os.path.join(ROOT, "results", "common_ids.json"), "w", encoding="utf-8"))
    with open(os.path.join(ROOT, "results", "fake_error_pool.jsonl"), "w", encoding="utf-8") as f:
        for r in fake_pool: f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("fake-error pool size:", len(fake_pool))
