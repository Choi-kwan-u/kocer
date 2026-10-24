"""KsponSpeech eval_clean / eval_other -> data/kspon_clean, data/kspon_other (local only, never publish).

usage: prepare_kspon.py <folder where the AI-Hub eval audio and scripts were extracted>

AI-Hub terms: no redistribution, no export, credit NIA. So this script
  - prints counts only, never transcript text (anything printed reaches the assistant's context),
  - writes refs only under data/ (not part of the public repo).

Transcript rules (ETRI KsponSpeech): dual notation "(spelling)/(pronunciation)", e.g. "(3시)/(세 시)";
noise tags b/ l/ o/ n/ u/ ; filler words marked "word/" ; repeats "+" ; unclear "*".
We keep BOTH references: ref = spelling side (lhotse default), ref_pron = pronunciation side.
"""
import os, re, sys, json, glob
import numpy as np, soundfile as sf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUAL = re.compile(r"\(([^()]*)\)/\(([^()]*)\)")
TAG = re.compile(r"(?<![A-Za-z])[a-z]/")

def clean(s):
    s = TAG.sub("", s)
    s = s.replace("*", "").replace("+", "").replace("/", "")
    return re.sub(r"\s+", " ", s).strip()

def read_trn(path):
    raw = open(path, "rb").read()
    for enc in ("utf-8", "cp949"):
        try:
            return raw.decode(enc).splitlines(), enc
        except UnicodeDecodeError:
            pass
    raise SystemExit(f"cannot decode {path}")

def main(src):
    trns = {os.path.basename(p)[:-4]: p for p in glob.glob(os.path.join(src, "**", "eval_*.trn"), recursive=True)}
    if not {"eval_clean", "eval_other"} <= set(trns):
        sys.exit(f"eval_clean.trn / eval_other.trn not found under {src} (found: {sorted(trns)})")
    pcm_index = {os.path.basename(p): p for p in glob.glob(os.path.join(src, "**", "*.pcm"), recursive=True)}
    print(f"found {len(pcm_index)} .pcm files")
    for split in ("eval_clean", "eval_other"):
        lines, enc = read_trn(trns[split])
        out_dir = os.path.join(ROOT, "data", "kspon_" + split.split("_")[1]); wav_dir = os.path.join(out_dir, "wav")
        os.makedirs(wav_dir, exist_ok=True)
        rows, missing, n_dual, n_digit, n_diff = [], 0, 0, 0, 0
        for line in lines:
            if " :: " not in line:
                continue
            rel, text = line.split(" :: ", 1)
            base = os.path.basename(rel.strip())
            pcm = pcm_index.get(base)
            if pcm is None:
                missing += 1; continue
            spell = clean(DUAL.sub(r"\1", text)); pron = clean(DUAL.sub(r"\2", text))
            n_dual += bool(DUAL.search(text)); n_digit += bool(re.search(r"\d", spell)); n_diff += spell != pron
            y = np.fromfile(pcm, dtype="<i2").astype(np.float32) / 32768.0
            uid = base[:-4]; wav = os.path.join(wav_dir, uid + ".wav")
            sf.write(wav, y, 16000)
            rows.append({"id": uid, "ref": spell, "ref_pron": pron, "audio_path": wav, "dur": round(len(y) / 16000, 2)})
        with open(os.path.join(out_dir, "test.jsonl"), "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        hours = sum(r["dur"] for r in rows) / 3600
        print(f"[{split}] encoding={enc} rows={len(rows)} missing_audio={missing} hours={hours:.2f} "
              f"max_dur={max(r['dur'] for r in rows):.1f}s dual_notation={n_dual} spelling_has_digit={n_digit} spelling!=pron={n_diff}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
