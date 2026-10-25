"""Score an AI-Hub telephone set (default tel_hr) for all settings. Numbers only (AI-Hub terms).
References: spelling side, pronunciation side, and the raw transcript (kocer aihub=True).
Uses kocer.compare() for the paired bootstrap.  Output: results/<name>_tables.md"""
import json, os, re, sys
import kocer
sys.path.insert(0, os.path.dirname(__file__)); from common import ROOT

NAME = sys.argv[1] if len(sys.argv) > 1 else "tel_hr"
TAGS = ["qwen3-asr-1.7b-ko-univa-release", "qwen3-asr-1.7b-ko-univa", "qwen3-asr-1.7b", "buzzasr-korean",
        "whisper-large-v3", "sensevoice-small-itn", "sensevoice-small-noitn"]
SHORT = {"qwen3-asr-1.7b-ko-univa-release": "TeamUNIVA ko", "qwen3-asr-1.7b-ko-univa": "TeamUNIVA ko beta",
         "qwen3-asr-1.7b": "Qwen3-ASR base", "buzzasr-korean": "BuzzASR", "whisper-large-v3": "whisper-large-v3",
         "sensevoice-small-itn": "SenseVoice itn", "sensevoice-small-noitn": "SenseVoice noitn"}
_ws = re.compile(r"\s+")

def jl(p): return [json.loads(l) for l in open(p, encoding="utf-8")]
data = {r["id"]: r for r in jl(os.path.join(ROOT, "data", NAME, "test.jsonl"))}
hyp = {t: {r["id"]: r["hyp"] for r in jl(os.path.join(ROOT, "results", t, f"{NAME}.jsonl"))} for t in TAGS}
ids = sorted(i for i in data if all(i in hyp[t] and hyp[t][i].strip() for t in TAGS))
refs = {k: [data[i][f] for i in ids] for k, f in [("spelling", "ref"), ("pronunciation", "ref_pron"), ("raw", "ref_raw")]}
H = {SHORT[t]: [hyp[t][i] for i in ids] for t in TAGS}

def corpus(rs, hs, **o):
    E = N = 0
    for r, h in zip(rs, hs):
        m = kocer.measure(r, h, **o); E += m.errors; N += m.hits + m.substitutions + m.deletions
    return E / max(N, 1) * 100

LEVELS = [("raw", dict(normalize=False)), ("nospace+punct", dict(numbers=False, letters=False, dual=False)), ("kocer", {})]
out = [f"# {NAME}: {len(ids)} utterances (AI-Hub 저음질 전화망 음성인식 데이터, validation). CER %, numbers only.\n"]
out.append("| model | " + " | ".join(f"{rk} {lv}" for rk in ["spelling", "pronunciation"] for lv, _ in LEVELS) + " | kocer, raw transcript (aihub=True) |")
out.append("|---|" + "---|" * 7)
table = {}
for s, hs in H.items():
    row = [corpus(refs[rk], hs, **o) for rk in ["spelling", "pronunciation"] for _, o in LEVELS]
    row.append(corpus(refs["raw"], hs, aihub=True)); table[s] = row
for s in sorted(table, key=lambda s: table[s][2]):
    out.append(f"| {s} | " + " | ".join(f"{v:.2f}" for v in table[s]) + " |")

out.append("\n## Reference-choice sensitivity (pronunciation − spelling, pt)\n")
out.append("| model | nospace+punct | kocer |"); out.append("|---|---|---|")
for s in sorted(table, key=lambda s: table[s][2]):
    out.append(f"| {s} | {table[s][4]-table[s][1]:+.2f} | {table[s][5]-table[s][2]:+.2f} |")

out.append("\n## Ranks\n")
for k, col in [("spelling nospace+punct", 1), ("pronunciation nospace+punct", 4), ("spelling kocer", 2), ("pronunciation kocer", 5), ("raw transcript kocer", 6)]:
    out.append(f"- {k}: " + " < ".join(sorted(table, key=lambda s: table[s][col])))

out.append("\n## Where raw errors go (spelling reference, counts)\n")
b_tab = {s: kocer.breakdown(refs["spelling"], hs) for s, hs in H.items()}
out.append("| model | raw errors | spacing | punctuation | numbers/letters | remaining |"); out.append("|---|---|---|---|---|---|")
for s in sorted(b_tab, key=lambda s: b_tab[s].cer["kocer"]):
    b = b_tab[s]; d = max(b.raw_errors, 1)
    out.append(f"| {s} | {b.raw_errors} | {b.spacing/d:.0%} | {b.punctuation/d:.0%} | {b.numbers_letters/d:.0%} | {b.remaining/d:.0%} |")

# paired bootstrap with kocer.compare
for label, rk, opts in [("spelling reference, kocer", "spelling", {}), ("raw transcript, kocer aihub=True", "raw", {"aihub": True})]:
    c = kocer.compare(refs[rk], H, **opts)
    out.append(f"\n## kocer.compare(): {label}\n\n```\n{c}\n```")

# number subset: utterances whose spelling reference contains a digit
num = [k for k, r in enumerate(refs["spelling"]) if re.search(r"\d", r)]
sub = lambda xs: [xs[k] for k in num]
out.append(f"\n## Utterances with a digit in the spelling reference: {len(num)}\n")
for rk in ["spelling", "pronunciation"]:
    for lv, o in [("nospace+punct", dict(numbers=False, letters=False, dual=False)), ("kocer", {})]:
        c = kocer.compare(sub(refs[rk]), {"TeamUNIVA ko": sub(H["TeamUNIVA ko"]), "Qwen3-ASR base": sub(H["Qwen3-ASR base"])}, **o)
        d, lo, hi = c.pairs.get(("TeamUNIVA ko", "Qwen3-ASR base")) or tuple(-x for x in reversed(c.pairs[("Qwen3-ASR base", "TeamUNIVA ko")]))
        out.append(f"- {rk} reference, {lv}: TeamUNIVA ko − Qwen3-ASR base = {d*100:+.2f} pt [{lo*100:+.2f}, {hi*100:+.2f}]{' *' if lo > 0 or hi < 0 else ''}")

# runaway outputs (criterion: sentence kocer errors > normalized reference length)
out.append("\n## Runaway outputs (sentence kocer CER > 1, spelling reference)\n")
for s, hs in H.items():
    n = sum(1 for r, h in zip(refs["spelling"], hs) if (lambda m: m.errors > m.hits + m.substitutions + m.deletions)(kocer.measure(r, h)))
    out.append(f"- {s}: {n}")

txt = "\n".join(out)
open(os.path.join(ROOT, "results", f"{NAME}_tables.md"), "w", encoding="utf-8").write(txt + "\n")
print(txt)
