"""AI-Hub 저음질 전화망 음성인식 데이터(dataSetSn=571) 검증셋 → data/tel_<domain>/test.jsonl (로컬 전용, 공개 금지).

usage: prepare_tel.py <VL_xxx.zip 라벨 압축> <VS_xxx.zip 음성 압축> <name, 예: tel_hr>

AI-Hub 약관: 재배포·국외 반출 금지, NIA 출처 표기. 개수만 출력하고 전사 텍스트는 출력하지 않는다.
정답 세 가지를 저장한다:
  ref      = 이중 표기 (A)/(B)의 철자 쪽(A) + 태그 정리   (KsponSpeech와 같은 규칙)
  ref_pron = 발음 쪽(B) + 태그 정리
  ref_raw  = 원본 전사 그대로 (kocer aihub=True로 채점)
"""
import io, json, os, re, sys, zipfile
import numpy as np, soundfile as sf, librosa

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUAL = re.compile(r"\(([^()]*)\)/\(([^()]*)\)")
TAG = re.compile(r"(?<![A-Za-z])[a-z]/")


def clean(s):
    s = TAG.sub("", s)
    s = s.replace("*", "").replace("+", "").replace("/", "")
    return re.sub(r"\s+", " ", s).strip()


def main(label_zip, audio_zip, name):
    lz, az = zipfile.ZipFile(label_zip), zipfile.ZipFile(audio_zip)
    wavs = {n.replace("\\", "/").lower(): n for n in az.namelist() if n.lower().endswith(".wav")}
    out_dir = os.path.join(ROOT, "data", name); wav_dir = os.path.join(out_dir, "wav"); os.makedirs(wav_dir, exist_ok=True)
    rows, missing, too_long, srs = [], 0, 0, {}
    for jn in sorted(n for n in lz.namelist() if n.lower().endswith(".json")):
        d = json.loads(lz.read(jn).decode("utf-8-sig"))
        for u in d["dataSet"]["dialogs"]:
            ap = u["audioPath"].replace("\\", "/")
            key = next((k for k in (ap.lower(), ap.lower().split("/", 1)[-1]) if k in wavs), None)
            if key is None:
                missing += 1; continue
            y, sr = sf.read(io.BytesIO(az.read(wavs[key])), dtype="float32")
            srs[sr] = srs.get(sr, 0) + 1
            if y.ndim > 1: y = y.mean(axis=1)
            if sr != 16000: y = librosa.resample(y, orig_sr=sr, target_sr=16000)
            dur = len(y) / 16000
            if dur > 30:
                too_long += 1; continue
            uid = ap.rsplit(".", 1)[0].replace("/", "_")
            wav = os.path.join(wav_dir, uid + ".wav"); sf.write(wav, y.astype(np.float32), 16000)
            t = u["text"]
            rows.append({"id": uid, "ref": clean(DUAL.sub(r"\1", t)), "ref_pron": clean(DUAL.sub(r"\2", t)), "ref_raw": t,
                         "audio_path": wav, "dur": round(dur, 2)})
    with open(os.path.join(out_dir, "test.jsonl"), "w", encoding="utf-8") as f:
        for r in rows: f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"[{name}] rows={len(rows)} missing_audio={missing} over_30s={too_long} hours={sum(r['dur'] for r in rows)/3600:.2f} "
          f"source_sample_rates={srs} empty_refs={sum(not r['ref'] for r in rows)} spelling!=pron={sum(r['ref'] != r['ref_pron'] for r in rows)}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])
