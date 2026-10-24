"""Qwen3-ASR family (qwen-asr). usage: infer_qwen.py <hf_model_id> <tag> <dataset> [batch]"""
import sys, os, torch
from tqdm import tqdm
sys.path.insert(0, os.path.dirname(__file__)); from common import load_data, Writer
from qwen_asr import Qwen3ASRModel
import qwen_asr, transformers

model_id, tag, ds = sys.argv[1:4]; bs = int(sys.argv[4]) if len(sys.argv) > 4 else 1
model = Qwen3ASRModel.from_pretrained(model_id, dtype=torch.bfloat16, device_map="cuda:0",
                                      max_inference_batch_size=bs, max_new_tokens=256)
gc = getattr(getattr(model, "model", None), "generation_config", None)
if gc is not None: gc.do_sample = False; gc.num_beams = 1; gc.temperature = None; gc.top_p = None; gc.top_k = None  # force greedy
rows = load_data(ds); w = Writer(tag, ds)
todo = [r for r in rows if r["id"] not in w.done]
for i in tqdm(range(0, len(todo), bs)):
    chunk = todo[i:i+bs]
    try:
        res = model.transcribe(audio=[r["audio_path"] for r in chunk], language=["Korean"] * len(chunk))
        for r, o in zip(chunk, res):
            w.write({"id": r["id"], "ref": r["ref"], "hyp": o.text, "lang_detected": getattr(o, "language", None)})
    except Exception as e:
        torch.cuda.empty_cache()
        for r in chunk:  # retry one by one
            try:
                o = model.transcribe(audio=r["audio_path"], language="Korean")[0]
                w.write({"id": r["id"], "ref": r["ref"], "hyp": o.text, "lang_detected": getattr(o, "language", None)})
            except Exception as e2:
                torch.cuda.empty_cache(); w.error(ds, r["id"], repr(e2)[:300])
w.meta(ds, dict(model=model_id, decoding="qwen-asr default (greedy per package)", language="Korean", dtype="bf16",
               batch=bs, max_new_tokens=256, torch=torch.__version__, cuda=torch.version.cuda,
               transformers=transformers.__version__, qwen_asr=getattr(qwen_asr, "__version__", "?")))
print("done", tag, ds)
