"""Multi-Sig 과제 단계별 컨트랙트를 만들고, 사이트에 붙여넣을 JSON 문자열을 출력한다.
사용: python3 tools/multisig_stage.py <단계폴더> <이전단계폴더> <패치파일.py>
패치파일에는 apply(s) -> s 함수를 정의한다."""
import json, runpy, sys
from pathlib import Path
stage, prev, patch = sys.argv[1:4]
s = Path(prev, "MultiSig.sol").read_text()
s = runpy.run_path(patch)["apply"](s)
Path(stage).mkdir(parents=True, exist_ok=True)
Path(stage, "MultiSig.sol").write_text(s)
Path("/private/tmp/claude-501/-Users-yj-Desktop----------/3da75e08-daf4-408f-96d7-361d82325fad/scratchpad/ms.json").write_text(json.dumps(s))
