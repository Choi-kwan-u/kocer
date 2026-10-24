"""Download Common Voice Scripted Speech 27.0 Korean from Mozilla Data Collective and build data/commonvoice/.
Key from env MDC_API_KEY (never written to disk). Terms must be accepted once in the browser:
https://mozilladatacollective.com/datasets/cmu5rwtaf003dnq07e7n3q6tf
Output rows match the other datasets: {"id","ref","audio_path", ...}; ref = test.tsv `sentence` as-is."""
import csv, io, json, os, sys, tarfile, time
import numpy as np, requests, soundfile as sf, librosa

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DID = "cmu5rwtaf003dnq07e7n3q6tf"
RAW = os.path.join(ROOT, "data", "_cv_raw")
OUT = os.path.join(ROOT, "data", "commonvoice")

def download():
    os.makedirs(RAW, exist_ok=True)
    have = [f for f in os.listdir(RAW) if f.endswith((".tar.gz", ".tgz", ".tar"))]
    if have:
        return os.path.join(RAW, have[0])
    H = {"Authorization": "Bearer " + os.environ["MDC_API_KEY"]}
    r = requests.post(f"https://mozilladatacollective.com/api/datasets/{DID}/download", headers=H, timeout=60)
    j = r.json()
    if r.status_code != 200 or "error" in j:
        sys.exit(f"MDC refused ({r.status_code}): {j.get('error', j)}")
    url = j.get("downloadUrl") or j.get("url")
    fn = os.path.basename(j.get("filename") or "cv27_ko.tar.gz")
    out = os.path.join(RAW, fn + ".part"); t = time.time()
    with requests.get(url, stream=True, timeout=900) as s:
        s.raise_for_status()
        with open(out, "wb") as f:
            for c in s.iter_content(1 << 20): f.write(c)
    os.replace(out, out[:-5])
    print(f"downloaded {fn} {os.path.getsize(out[:-5])//1_000_000} MB in {time.time()-t:.0f}s")
    return out[:-5]

def to16k(y, sr):
    if y.ndim > 1: y = y.mean(axis=1)
    if sr != 16000: y = librosa.resample(y.astype(np.float32), orig_sr=sr, target_sr=16000)
    return y.astype(np.float32)

def build(tar_path):
    wav = os.path.join(OUT, "wav"); os.makedirs(wav, exist_ok=True)
    with tarfile.open(tar_path) as tf:
        members = {m.name: m for m in tf.getmembers() if m.isfile()}
        test_tsv = [n for n in members if n.endswith("/test.tsv") or n == "test.tsv"]
        assert test_tsv, "test.tsv not found in archive: " + str(list(members)[:10])
        prefix = test_tsv[0][: -len("test.tsv")]
        txt = tf.extractfile(members[test_tsv[0]]).read().decode("utf-8")
        rdr = csv.DictReader(io.StringIO(txt), delimiter="\t", quoting=csv.QUOTE_NONE)
        rows = []
        for r in rdr:
            clip = prefix + "clips/" + r["path"]
            if clip not in members:
                print("missing clip", r["path"]); continue
            data = tf.extractfile(members[clip]).read()
            try:
                y, sr = sf.read(io.BytesIO(data))
            except Exception:
                y, sr = librosa.load(io.BytesIO(data), sr=None, mono=True)
            cid = os.path.splitext(r["path"])[0]
            out = os.path.join(wav, cid + ".wav"); sf.write(out, to16k(np.asarray(y), sr), 16000)
            rows.append({"id": cid, "ref": r["sentence"], "audio_path": out, "client_id": r.get("client_id", "")[:12],
                         "source": "Common Voice Scripted Speech 27.0 Korean (MDC " + DID + ")"})
    with open(os.path.join(OUT, "test.jsonl"), "w", encoding="utf-8") as f:
        for r in rows: f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"[commonvoice] {len(rows)} rows -> {OUT}/test.jsonl  (archive prefix: {prefix})")

if __name__ == "__main__":
    build(download())
