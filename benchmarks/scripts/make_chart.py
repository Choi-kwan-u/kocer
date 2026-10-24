"""results/scores2.json → docs/breakdown-{light,dark}.svg : raw 오류를 종류별로 나눈 100% 누적 가로 막대."""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = json.load(open(os.path.join(ROOT, "results", "scores2.json"), encoding="utf-8"))["scores"]
NAMES = {"buzzasr-korean": "BuzzASR/korean", "qwen3-asr-1.7b-ko-univa": "TeamUNIVA ko", "whisper-large-v3": "whisper-large-v3",
         "qwen3-asr-1.7b": "Qwen3-ASR-1.7B", "sensevoice-small-itn": "SenseVoice (itn on)", "sensevoice-small-noitn": "SenseVoice (itn off)"}
rows = []
for tag, name in NAMES.items():
    E = S[tag]["overall"]["E"]
    rows.append((name, [E[0] - E[1], E[1] - E[2], E[2] - E[3], E[3]], S[tag]["overall"]["cer"]))
rows.sort(key=lambda r: r[2]["kocer"])
LEGEND = ["띄어쓰기 차이", "문장부호 차이", "숫자·영문 표기 차이", "진짜 오류 (kocer CER)"]
THEMES = {"light": dict(bg="#fcfcfb", fg="#0b0b0b", muted="#52514e", series=["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]),
          "dark": dict(bg="#1a1a19", fg="#f0efec", muted="#c3c2b7", series=["#3987e5", "#d95926", "#199e70", "#c98500"])}
W, LABEL, RIGHT, BAR, GAP, TOP = 760, 150, 120, 22, 12, 108
for mode, t in THEMES.items():
    H = TOP + len(rows) * (BAR + GAP) + 16
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="-apple-system,Apple SD Gothic Neo,Malgun Gothic,Noto Sans KR,Segoe UI,Helvetica,Arial,sans-serif">',
         f'<rect width="{W}" height="{H}" fill="{t["bg"]}"/>',
         f'<text x="16" y="26" font-size="15" font-weight="600" fill="{t["fg"]}">CER가 센 오류의 절반은 모델이 틀린 게 아니라 적는 방식 차이입니다</text>',
         f'<text x="16" y="46" font-size="12" fill="{t["muted"]}">공개 한국어 STT 모델 6개, 테스트 1,418발화. 막대 전체가 보통 CER(jiwer)이 센 오류이고, kocer는 노란 부분만 셉니다.</text>']
    x = 16
    for c, lab in zip(t["series"], LEGEND):
        o.append(f'<rect x="{x}" y="56" width="10" height="10" rx="2" fill="{c}"/><text x="{x + 15}" y="65" font-size="11" fill="{t["muted"]}">{lab}</text>')
        x += 15 + 11 * len(lab) + 22
    span = W - LABEL - RIGHT
    # 막대 위 안내: 왼쪽 ~60%는 표기 차이, 오른쪽은 진짜 오류 (합산 평균 기준 위치)
    cut = LABEL + span * 0.60
    o.append(f'<text x="{(LABEL + cut) / 2:.0f}" y="{TOP - 12}" font-size="11" text-anchor="middle" fill="{t["muted"]}">← 표기만 다름: kocer는 오류로 안 셈 →</text>')
    o.append(f'<text x="{(cut + LABEL + span) / 2:.0f}" y="{TOP - 12}" font-size="11" text-anchor="middle" fill="{t["fg"]}">← 진짜 오류 →</text>')
    o.append(f'<text x="{LABEL + span + 10}" y="{TOP - 12}" font-size="11" fill="{t["muted"]}">보통 CER → kocer</text>')
    for i, (name, parts, cer) in enumerate(rows):
        y = TOP + i * (BAR + GAP); total = sum(parts); x = LABEL
        o.append(f'<text x="{LABEL - 10}" y="{y + 15}" font-size="12" text-anchor="end" fill="{t["fg"]}">{name}</text>')
        for c, v in zip(t["series"], parts):
            w = span * v / total - 2
            o.append(f'<rect x="{x:.1f}" y="{y}" width="{max(w, 0):.1f}" height="{BAR}" rx="2" fill="{c}"/>')
            if v / total >= 0.06:
                o.append(f'<text x="{x + w / 2:.1f}" y="{y + 15}" font-size="11" text-anchor="middle" fill="#0b0b0b">{v / total:.0%}</text>')
            x += span * v / total
        o.append(f'<text x="{LABEL + span + 10}" y="{y + 15}" font-size="11" fill="{t["muted"]}">{cer["raw"]:.2%} → {cer["kocer"]:.2%}</text>')
    o.append("</svg>")
    out = os.path.join(os.path.dirname(ROOT), "docs", f"breakdown-{mode}.svg")
    open(out, "w", encoding="utf-8").write("\n".join(o)); print(out)
