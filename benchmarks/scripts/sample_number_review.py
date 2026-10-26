"""0.4.0 review: 100 sentences where the number/letter step is what made the sentence correct
(nospace+punct errors > 0 and kocer errors == 0), from the three public sets only (publishable text).
Writes results/number_review.tsv (verdict column to fill: 1=notation only, 2=hides a real error, 3=ambiguous)
and a local HTML page results/number_review.html for reading side by side."""
import html, json, os, random, sys
import kocer
sys.path.insert(0, os.path.dirname(__file__)); from common import ROOT

SEED = 20261026
ids = json.load(open(os.path.join(ROOT, "results", "common_ids.json"), encoding="utf-8"))
tags = sorted(d for d in os.listdir(os.path.join(ROOT, "results")) if os.path.isdir(os.path.join(ROOT, "results", d)) and not d.startswith("_"))
pool, seen = [], set()
for t in tags:
    for ds in ["zeroth", "fleurs", "commonvoice"]:
        p = os.path.join(ROOT, "results", t, f"{ds}.jsonl")
        if not os.path.exists(p):
            continue
        keep = set(ids[ds])
        for line in open(p, encoding="utf-8"):
            r = json.loads(line)
            if r["id"] not in keep:
                continue
            k = (r["ref"], r["hyp"].strip())
            if k in seen:
                continue
            m2 = kocer.measure(r["ref"], r["hyp"], numbers=False, letters=False)
            if m2.errors == 0:
                continue
            m3 = kocer.measure(r["ref"], r["hyp"])
            if m3.errors == 0:
                seen.add(k); pool.append(dict(model=t, dataset=ds, id=r["id"], ref=r["ref"], hyp=r["hyp"].strip(),
                                              chosen_ref=m3.chosen_ref, chosen_hyp=m3.chosen_hyp, nopunct_errors=m2.errors))
random.Random(SEED).shuffle(pool)
sample = pool[:100]
with open(os.path.join(ROOT, "results", "number_review.tsv"), "w", encoding="utf-8") as f:
    f.write("idx\tmodel\tdataset\tid\tref\thyp\tchosen_ref\tchosen_hyp\tverdict\tnote\n")
    for i, r in enumerate(sample, 1):
        f.write(f"{i}\t{r['model']}\t{r['dataset']}\t{r['id']}\t{r['ref']}\t{r['hyp']}\t{r['chosen_ref']}\t{r['chosen_hyp']}\t\t\n")
rows = "".join(f"<tr id=r{i}><td>{i}</td><td class=s>{r['dataset']}<br>{r['model']}</td><td>{html.escape(r['ref'])}<br><span class=c>{html.escape(r['chosen_ref'])}</span></td>"
               f"<td>{html.escape(r['hyp'])}<br><span class=c>{html.escape(r['chosen_hyp'])}</span></td><td class=s>{r['nopunct_errors']}</td>"
               f"<td class=v><button data-i={i} data-v=1>1 표기만</button><button data-i={i} data-v=2>2 오류 숨김</button><button data-i={i} data-v=3>3 애매</button></td></tr>"
               for i, r in enumerate(sample, 1))
page = f"""<!doctype html><meta charset="utf-8"><title>kocer {kocer.__version__} number-step review</title>
<style>body{{font-family:sans-serif;max-width:1200px;margin:20px auto;padding:0 16px}}table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #ccc;padding:6px;vertical-align:top;font-size:14px}}
.s{{color:#666;font-size:12px;white-space:nowrap}}.c{{color:#2a78d6;font-size:12px}}.v{{white-space:nowrap}}button{{margin:1px;padding:4px 6px;cursor:pointer}}
tr.v1 td{{background:#eef7ee}}tr.v2 td{{background:#fdecea}}tr.v3 td{{background:#fff6dc}}button.on{{outline:2px solid #333}}#bar{{position:sticky;top:0;background:#fff;padding:8px 0;border-bottom:1px solid #ccc}}</style>
<h1>kocer {kocer.__version__}: 숫자·영문 단계가 작동한 문장 100건</h1>
<p>조건: 띄어쓰기·문장부호를 빼면 오류가 남는데(부호 제거 후 오류 열) kocer로는 0인 문장. 공개 데이터셋 3개, 후보 풀 {len(pool)}건에서 seed {SEED}로 100건.
파란 줄은 kocer가 실제로 채택한 후보. 판정: <b>1</b> = 같은 말을 다르게 적었을 뿐, <b>2</b> = 실제 오류인데 kocer가 맞다고 봄, <b>3</b> = 애매. 판정은 이 브라우저에 자동 저장되고, 끝나면 아래 버튼으로 tsv를 내려받아 results/number_review.tsv를 덮어쓰면 됩니다.</p>
<div id=bar><span id=cnt></span> &nbsp; <button id=dl>판정 tsv 내려받기</button></div>
<table><tr><th>#</th><th>출처</th><th>정답 / 채택된 정답 후보</th><th>STT 출력 / 채택된 출력 후보</th><th>부호 제거 후 오류</th><th>판정</th></tr>{rows}</table>
<script>
const KEY="kocer_number_review_{SEED}"; let V={{}}; try{{V=JSON.parse(localStorage.getItem(KEY)||"{{}}")}}catch(e){{}}
const TSV={json.dumps([[i, r['model'], r['dataset'], r['id'], r['ref'], r['hyp'], r['chosen_ref'], r['chosen_hyp']] for i, r in enumerate(sample, 1)], ensure_ascii=False)};
function paint(){{for(const [i,v] of Object.entries(V)){{const tr=document.getElementById("r"+i);tr.className="v"+v;tr.querySelectorAll("button").forEach(b=>b.classList.toggle("on",b.dataset.v==v));}}
  document.getElementById("cnt").textContent=Object.keys(V).length+" / 100 판정됨";}}
document.querySelectorAll("td.v button").forEach(b=>b.onclick=()=>{{V[b.dataset.i]=b.dataset.v;try{{localStorage.setItem(KEY,JSON.stringify(V))}}catch(e){{}}paint();}});
document.getElementById("dl").onclick=()=>{{const H="idx\\tmodel\\tdataset\\tid\\tref\\thyp\\tchosen_ref\\tchosen_hyp\\tverdict\\tnote";const lines=[H].concat(TSV.map(r=>r.concat([V[r[0]]||"",""]).join("\\t")));
  const a=document.createElement("a");a.href=URL.createObjectURL(new Blob([lines.join("\\n")+"\\n"],{{type:"text/tab-separated-values"}}));a.download="number_review.tsv";a.click();}};
paint();
</script>"""
open(os.path.join(ROOT, "results", "number_review.html"), "w", encoding="utf-8").write(page)
print(f"pool={len(pool)} sampled={len(sample)} seed={SEED} per dataset: " + str({ds: sum(r['dataset'] == ds for r in sample) for ds in ['zeroth', 'fleurs', 'commonvoice']}))
