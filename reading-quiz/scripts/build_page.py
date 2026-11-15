"""把閱讀測驗資料檔 (JSON) 套進固定範本，產生單一 HTML。

用法：python build_page.py <資料.json> <輸出.html>
"""
import json
import sys
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "template.html"


def fail(msg):
    print(f"錯誤：{msg}")
    sys.exit(1)


def validate(d):
    for key in ("title", "paragraphs", "questions"):
        if key not in d:
            fail(f"資料檔缺少欄位 {key}")
    if not isinstance(d["paragraphs"], list) or not d["paragraphs"]:
        fail("paragraphs 必須是至少一段文字的陣列")
    for i, p in enumerate(d["paragraphs"], 1):
        if not isinstance(p, str) or not p.strip():
            fail(f"第 {i} 段是空的")
    if not d["questions"]:
        fail("questions 至少要有一題")
    for i, q in enumerate(d["questions"], 1):
        for key in ("question", "options", "correctAnswer", "explanation"):
            if key not in q:
                fail(f"第 {i} 題缺少 {key}")
        if q["correctAnswer"] not in q["options"]:
            fail(f"第 {i} 題的正確答案 {q['correctAnswer']} 不在選項裡")
        if len(q["options"]) < 2:
            fail(f"第 {i} 題選項少於 2 個")
        ev = q.get("evidence")
        if ev is None:
            print(f"提醒：第 {i} 題沒有 evidence，練習模式只能給「回到文章再讀一次」的一般提示")
            continue
        pn = ev.get("paragraph")
        if not isinstance(pn, int) or not 1 <= pn <= len(d["paragraphs"]):
            fail(f"第 {i} 題 evidence.paragraph 必須是 1～{len(d['paragraphs'])} 的整數")
        sent = ev.get("sentence", "")
        if sent:
            strip = lambda s: "".join(ch for ch in s if ch not in " ，。！？、；：「」『』,")
            if strip(sent) not in strip(d["paragraphs"][pn - 1]):
                fail(f"第 {i} 題 evidence.sentence 在第 {pn} 段找不到，請直接複製原文的句子")
    if d.get("mode", "practice") not in ("practice", "test"):
        fail('mode 只能是 "practice" 或 "test"')
    if d.get("theme", "minimal") not in ("minimal", "classic"):
        fail('theme 只能是 "minimal" 或 "classic"')
    ws = d.get("waitSeconds", 20)
    if not isinstance(ws, (int, float)) or ws < 0:
        fail("waitSeconds 必須是 0 以上的數字")


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    validate(data)
    data.setdefault("waitSeconds", 20)
    data.setdefault("source", "")
    data.setdefault("mode", "practice")
    data.setdefault("theme", "minimal")

    html = TEMPLATE.read_text(encoding="utf-8")
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    title = data["title"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    html = html.replace("/*__QUIZ_DATA__*/null", payload).replace("__PAGE_TITLE__", title).replace("__THEME__", data["theme"])

    out = Path(sys.argv[2])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"已產生 {out}（{len(data['paragraphs'])} 段、{len(data['questions'])} 題、每段等待 {data['waitSeconds']} 秒、預設{'練習' if data['mode'] == 'practice' else '測驗'}模式）")


if __name__ == "__main__":
    main()
