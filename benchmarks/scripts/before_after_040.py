"""kocer 0.3.x → 0.4.0 재채점 비교표. results/_before_040/ (0.3.0으로 채점) vs results/ (현재 설치본). 숫자만.
Output: results/before_after_040.md"""
import json, os, re, sys
import kocer
sys.path.insert(0, os.path.dirname(__file__)); from common import ROOT

R = os.path.join(ROOT, "results"); B = os.path.join(R, "_before_040")
NAMES = {"qwen3-asr-1.7b-ko-univa-release": "TeamUNIVA ko", "qwen3-asr-1.7b-ko-univa": "TeamUNIVA ko beta", "qwen3-asr-1.7b": "Qwen3-ASR base",
         "buzzasr-korean": "BuzzASR", "whisper-large-v3": "whisper-large-v3", "sensevoice-small-itn": "SenseVoice itn", "sensevoice-small-noitn": "SenseVoice noitn"}
out = [f"# Re-scoring the same outputs: kocer 0.3.0 → {kocer.__version__}\n",
       "Nothing was re-run; only the scorer changed. Rule changes: fixed denominator (reference-only), raw CER strips outer whitespace (= jiwer), "
       "unit symbols / time / currency / temperature / minus as candidates, Latin case-folding and letter variants, digit-wise reading restricted, NFKC, "
       "more AI-Hub tags, WER without number normalization.\n"]

def load(p): return json.load(open(p, encoding="utf-8"))
b, a = load(os.path.join(B, "scores2.json"))["scores"], load(os.path.join(R, "scores2.json"))["scores"]

out.append("## Public sets: CER % per level (before → after)\n")
out.append("| model | set | raw | nospace | nospace+punct | kocer | notation share of raw |"); out.append("|---|---|---|---|---|---|---|")
for t in NAMES:
    for ds in ["zeroth", "fleurs", "commonvoice", "overall"]:
        x, y = b[t][ds], a[t][ds]
        cells = [f"{x['cer'][L]*100:.2f} → {y['cer'][L]*100:.2f}" for L in ["raw", "nospace", "nopunct", "kocer"]]
        sh = lambda d: 1 - d["E"][3] / d["E"][0]
        out.append(f"| {NAMES[t]} | {ds} | " + " | ".join(cells) + f" | {sh(x):.0%} → {sh(y):.0%} |")

def rank_str(scores, ds, L):
    return " < ".join(NAMES[t] for t in sorted(NAMES, key=lambda t: scores[t][ds]["cer"][L]))
out.append("\n## Ranks at the kocer level (before / after)\n")
for ds in ["zeroth", "fleurs", "commonvoice", "overall"]:
    rb, ra = rank_str(b, ds, "kocer"), rank_str(a, ds, "kocer")
    out.append(f"- {ds}: {rb}" + ("" if rb == ra else f"\n  → after: {ra}"))
shares = [1 - a[t]["overall"]["E"][3] / a[t]["overall"]["E"][0] for t in NAMES]
shares_b = [1 - b[t]["overall"]["E"][3] / b[t]["overall"]["E"][0] for t in NAMES]
out.append(f"\nNotation share of raw errors, pooled public sets: {min(shares_b):.0%}–{max(shares_b):.0%} → **{min(shares):.0%}–{max(shares):.0%}**")

def table_block(path, heading, rows_re):
    """Lines of the first table after `heading` whose first cell matches rows_re."""
    txt = open(path, encoding="utf-8").read()
    i = txt.find(heading)
    if i < 0:
        return {}
    block = txt[i:].split("\n## ", 1)[0]
    rows = {}
    for line in block.splitlines():
        if line.startswith("|") and not line.startswith("|---") and not line.startswith("| model"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            rows[cells[0] + ("|" + cells[1] if rows_re == "split" else "")] = cells[1 if rows_re != "split" else 2:]
    return rows

for title, fname, heading, mode, cols in [
        ("KsponSpeech (spelling reference), CER % raw / nospace / nopunct / kocer / kocer+fillers", "kspon_tables.md", "## Reference = spelling side", "split", 5),
        ("KsponSpeech (pronunciation reference)", "kspon_tables.md", "## Reference = pronunciation side", "split", 5),
        ("Telephone HR: spelling raw / nospace+punct / kocer, pronunciation raw / nospace+punct / kocer, raw transcript kocer", "tel_hr_tables.md", "# tel_hr", "", 7)]:
    rb, ra = table_block(os.path.join(B, fname), heading, mode), table_block(os.path.join(R, fname), heading, mode)
    out.append(f"\n## {title}\n")
    for k in ra:
        if k in rb:
            out.append(f"- {k}: " + " | ".join(f"{x} → {y}" for x, y in zip(rb[k][:cols], ra[k][:cols])))

for fname in ["number_subset.md", "decoding_check.md", "univa_compare.md"]:
    out.append(f"\n## {fname}: lines that changed\n")
    lb = open(os.path.join(B, fname), encoding="utf-8").read().splitlines()
    la = open(os.path.join(R, fname), encoding="utf-8").read().splitlines()
    n = 0
    for x, y in zip(lb, la):
        if x != y and ("|" in y or re.search(r"\d", y)):
            out.append(f"- before: {x.strip()[:160]}\n  after:  {y.strip()[:160]}"); n += 1
            if n >= 25:
                out.append("- ..."); break
    if n == 0:
        out.append("- (identical)")
txt = "\n".join(out)
open(os.path.join(R, "before_after_040.md"), "w", encoding="utf-8").write(txt + "\n")
print(txt)
