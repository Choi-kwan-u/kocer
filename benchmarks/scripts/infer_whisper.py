"""Whisper-family (transformers). usage: infer_whisper.py <hf_model_id> <tag> <dataset> [batch] [extra_gen_kwargs_json]
extra_gen_kwargs_json, e.g. '{"no_repeat_ngram_size": 3, "repetition_penalty": 1.2}', is merged into the greedy defaults."""
import sys, os, torch, soundfile as sf, transformers
from transformers import WhisperForConditionalGeneration, WhisperProcessor
from tqdm import tqdm
sys.path.insert(0, os.path.dirname(__file__)); from common import load_data, Writer

model_id, tag, ds = sys.argv[1:4]; bs = int(sys.argv[4]) if len(sys.argv) > 4 else 8
proc = WhisperProcessor.from_pretrained(model_id)
model = WhisperForConditionalGeneration.from_pretrained(model_id, torch_dtype=torch.float16).cuda().eval()
gen_kwargs = dict(num_beams=1, do_sample=False, language="ko", task="transcribe", max_new_tokens=440)
if len(sys.argv) > 5:
    import json as _json
    gen_kwargs.update(_json.loads(sys.argv[5]))
rows = load_data(ds); w = Writer(tag, ds)
todo = [r for r in rows if r["id"] not in w.done]
for i in tqdm(range(0, len(todo), bs)):
    chunk = todo[i:i+bs]
    try:
        audios = [sf.read(r["audio_path"])[0] for r in chunk]
        feats = proc(audios, sampling_rate=16000, return_tensors="pt").input_features.to("cuda", torch.float16)
        with torch.inference_mode():
            out = model.generate(feats, **gen_kwargs)
        texts = proc.batch_decode(out, skip_special_tokens=True)
        for r, t in zip(chunk, texts):
            w.write({"id": r["id"], "ref": r["ref"], "hyp": t})
    except Exception as e:
        torch.cuda.empty_cache()
        for r in chunk: w.error(ds, r["id"], repr(e)[:300])
w.meta(ds, dict(model=model_id, decoding=gen_kwargs, dtype="fp16", batch=bs,
               torch=torch.__version__, cuda=torch.version.cuda, transformers=transformers.__version__))
print("done", tag, ds)
