"""단계 README를 공통 형식으로 만드는 도우미. 사용: python3 tools/write_readme.py <spec.py>
spec.py 안에 STAGES = [dict(...), ...] 를 정의한다."""
import runpy, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def render(s):
    out = [f"# {s['title']}\n", "## 문제\n", s['problem'].strip() + "\n",
           "## 한 줄 요약\n", s['summary'].strip() + "\n",
           f"![{s['img_alt']} 코드 흐름](./{s['img']})\n"]
    if s.get('diagram_table'):
        out += ["### 다이어그램 읽는 법\n", "| 구간 | 일어나는 일 |\n|------|-------------|"]
        out += [f"| {a} | {b} |" for a, b in s['diagram_table']]
        out.append("")
    out += ["---\n", "## 0. 이 과제가 말하려는 것\n", s['intent'].strip() + "\n",
            "---\n", "## 1. 파일 구성\n", "| 파일 | 역할 |\n|------|------|"]
    out += [f"| `{a}` | {b} |" for a, b in s['files']]
    out += ["", "---\n", "## 2. 정답 코드\n", s['solution'].strip() + "\n",
            "---\n", "## 3. 테스트 한 줄씩\n", s['tests'].strip() + "\n"]
    if s.get('wrong'):
        out += ["---\n", "## 4. 일부러 틀려 보면\n", "| 바꾼 것 | 결과 |\n|---------|------|"]
        out += [f"| {a} | {b} |" for a, b in s['wrong']]
        out.append("")
    out += ["---\n", "## 5. 실행 방법\n", f"```bash\n{s['run']}\n```\n"]
    if s.get('env'):
        out += ["## 로컬 실행 환경 메모\n", s['env'].strip() + "\n"]
    out += ["## 기억할 것\n"] + [f"{i}. {x}" for i, x in enumerate(s['remember'], 1)]
    if s.get('confusing'):
        out += ["", "## 헷갈렸던 점\n"] + [f"- {x}" for x in s['confusing']]
    return "\n".join(out) + "\n"

for s in runpy.run_path(sys.argv[1])['STAGES']:
    p = ROOT / s['dir'] / "README.md"
    p.write_text(render(s))
    print(p.relative_to(ROOT))
