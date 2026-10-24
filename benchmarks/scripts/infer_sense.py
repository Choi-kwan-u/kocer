"""SenseVoiceSmall (funasr). usage: infer_sense.py <tag> <dataset> <use_itn: 0|1> [batch]"""
import sys, os, torch, funasr
from tqdm import tqdm
sys.path.insert(0, os.path.dirname(__file__)); from common import load_data, Writer
from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess

tag, ds, itn = sys.argv[1], sys.argv[2], bool(int(sys.argv[3])); bs = int(sys.argv[4]) if len(sys.argv) > 4 else 16
model = AutoModel(model="FunAudioLLM/SenseVoiceSmall", device="cuda:0", hub="hf", disable_update=True)
rows = load_data(ds); w = Writer(tag, ds)
todo = [r for r in rows if r["id"] not in w.done]
for i in tqdm(range(0, len(todo), bs)):
    chunk = todo[i:i+bs]
    try:
        res = model.generate(input=[r["audio_path"] for r in chunk], cache={}, language="ko", use_itn=itn, batch_size=bs)
        for r, o in zip(chunk, res):
            w.write({"id": r["id"], "ref": r["ref"], "hyp": rich_transcription_postprocess(o["text"]), "hyp_raw": o["text"]})
    except Exception as e:
        torch.cuda.empty_cache()
        for r in chunk: w.error(ds, r["id"], repr(e)[:300])
w.meta(ds, dict(model="FunAudioLLM/SenseVoiceSmall", use_itn=itn, language="ko", postprocess="rich_transcription_postprocess",
               batch=bs, torch=torch.__version__, cuda=torch.version.cuda, funasr=funasr.__version__))
print("done", tag, ds)
