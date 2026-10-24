"""Run scripts/run_kspon.sh while keeping Windows from sleeping. Sleep prevention ends when this process ends.
Launched detached (WMI Win32_Process.Create) so closing the editor or the assistant session does not stop it.
Powering the PC off does stop it; re-running resumes (finished ids are skipped)."""
import ctypes, datetime, os, shutil, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # benchmark root
BASH = os.environ.get("BASH_EXE") or shutil.which("bash") or r"C:\Program Files\Git\bin\bash.exe"
LOG = os.path.join(ROOT, "logs", "infer_kspon.log")
ES_CONTINUOUS, ES_SYSTEM_REQUIRED = 0x80000000, 0x00000001

with open(os.path.join(ROOT, "logs", "kspon_runner.pid"), "w") as f:
    f.write(str(os.getpid()))
ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)
with open(LOG, "a", encoding="utf-8") as log:
    log.write(f"\n=== start {datetime.datetime.now():%Y-%m-%d %H:%M:%S} pid={os.getpid()} ===\n"); log.flush()
    rc = subprocess.call([BASH, "scripts/run_kspon.sh"], cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
    log.write(f"\n=== end {datetime.datetime.now():%Y-%m-%d %H:%M:%S} rc={rc} ===\n")
ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
