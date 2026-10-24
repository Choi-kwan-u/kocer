import json, os, sys, time, platform, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_data(ds):
    p = os.path.join(ROOT, "data", ds, "test.jsonl")
    return [json.loads(l) for l in open(p, encoding="utf-8")]

class Writer:
    """Append-only jsonl with resume; failures go to errors.log."""
    def __init__(self, tag, ds):
        d = os.path.join(ROOT, "results", tag); os.makedirs(d, exist_ok=True)
        self.path = os.path.join(d, f"{ds}.jsonl"); self.err = os.path.join(d, "errors.log")
        self.done = set()
        if os.path.exists(self.path):
            for l in open(self.path, encoding="utf-8"):
                self.done.add(json.loads(l)["id"])
        self.f = open(self.path, "a", encoding="utf-8")
    def write(self, row):
        self.f.write(json.dumps(row, ensure_ascii=False) + "\n"); self.f.flush()
    def error(self, ds, id_, reason):
        with open(self.err, "a", encoding="utf-8") as e: e.write(f"{ds}\t{id_}\t{reason}\n")
    def meta(self, ds, info):
        info = dict(info, dataset=ds, date=time.strftime("%Y-%m-%d"), python=platform.python_version(),
                    pip=subprocess.run([sys.executable, "-m", "pip", "freeze"], capture_output=True, text=True).stdout.split())
        with open(self.path.replace(".jsonl", ".meta.json"), "w", encoding="utf-8") as m: json.dump(info, m, ensure_ascii=False, indent=1)
