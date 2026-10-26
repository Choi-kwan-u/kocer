"""KsponSpeech: kocer CER with spelling ref / pronunciation ref / raw .trn transcript (aihub=True), six systems. Numbers only.
Also checks that no utterance has more errors with the raw transcript than with the better of the two cleaned sides.
Output: results/kspon_raw_transcript.md"""
import json, os, sys
import kocer
sys.path.insert(0, os.path.dirname(__file__)); from common import ROOT

TAGS = [("TeamUNIVA/qwen3_asr_1.7b_ko", "qwen3-asr-1.7b-ko-univa-release"), ("TeamUNIVA/qwen3_asr_1.7b_ko_beta", "qwen3-asr-1.7b-ko-univa"),
        ("Qwen/Qwen3-ASR-1.7B", "qwen3-asr-1.7b"), ("BuzzASR/korean", "buzzasr-korean"), ("openai/whisper-large-v3", "whisper-large-v3"),
        ("SenseVoiceSmall (itn off)", "sensevoice-small-noitn")]
raw = {}
for name in ["eval_clean", "eval_other"]:
    for line in open(os.path.join(ROOT, "data", "_kspon_raw", "scripts", f"{name}.trn"), encoding="utf-8"):
        if " :: " in line:
            p, t = line.rstrip("\n").split(" :: ", 1)
            raw[os.path.basename(p).rsplit(".", 1)[0]] = t
def jl(p): return [json.loads(l) for l in open(p, encoding="utf-8")]
data = {}
for ds in ["kspon_clean", "kspon_other"]:
    data.update({x["id"]: x for x in jl(os.path.join(ROOT, "data", ds, "test.jsonl"))})
ids = sorted(data)
out = [f"# KsponSpeech, kocer {kocer.__version__}: spelling / pronunciation / raw transcript (aihub=True). {len(ids)} utterances, numbers only.\n",
       "| Model | kocer, spelling ref | kocer, pronunciation ref | kocer, raw transcript (`aihub=True`) | utterances where raw > min(spelling, pron) errors |", "|---|---|---|---|---|"]
for name, tag in TAGS:
    hyp = {}
    for ds in ["kspon_clean", "kspon_other"]:
        hyp.update({x["id"]: x["hyp"] for x in jl(os.path.join(ROOT, "results", tag, f"{ds}.jsonl"))})
    E = [0, 0, 0]; N = [0, 0, 0]; worse = 0
    for i in ids:
        ms = [kocer.measure(data[i]["ref"], hyp[i]), kocer.measure(data[i]["ref_pron"], hyp[i]), kocer.measure(raw[i], hyp[i], aihub=True)]
        for k, m in enumerate(ms):
            E[k] += m.errors; N[k] += m.ref_len
        worse += ms[2].errors > min(ms[0].errors, ms[1].errors)
    out.append(f"| {name} | " + " | ".join(f"{e / n * 100:.2f}" for e, n in zip(E, N)) + f" | {worse} |")
txt = "\n".join(out)
open(os.path.join(ROOT, "results", "kspon_raw_transcript.md"), "w", encoding="utf-8").write(txt + "\n")
print(txt)
