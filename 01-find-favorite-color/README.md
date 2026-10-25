# 01. Find Favorite Color

## 문제

누군가 좋아하는 색을 SHA-256으로 해시해서 **해시값만** 넘겨준다. 해시를 보고 원래 색이 무엇인지 맞히기.
후보는 `red`, `green`, `blue`, `yellow`, `pink`, `orange` 6개.

## 한 줄 요약

해시는 거꾸로 풀 수 없지만, 후보가 적으면 **후보를 전부 해시해서 비교**하는 방식(브루트포스)으로 원래 값을 알아낼 수 있다.

## 코드

```js
const { sha256 } = require("ethereum-cryptography/sha256");
const { toHex, utf8ToBytes } = require("ethereum-cryptography/utils");

const COLORS = ['red', 'green', 'blue', 'yellow', 'pink', 'orange'];

function findColor(hash) {
    const target = toHex(hash);
    return COLORS.find((color) => toHex(sha256(utf8ToBytes(color))) === target);
}

module.exports = findColor;
```

같은 동작을 Python으로 쓰면:

```python
from hashlib import sha256

COLORS = ['red', 'green', 'blue', 'yellow', 'pink', 'orange']

def find_color(hash):
    target = hash.hex()
    for color in COLORS:
        if sha256(color.encode('utf-8')).digest().hex() == target:
            return color
    return None
```

![findColor 로직 분석](./findColor_diagram.png)

---

## 1. 해시(hash)란?

데이터를 넣으면 그 데이터만의 **지문**을 만들어 주는 계산. 믹서기로 사과주스를 만드는 것과 비슷하다.

| 성질 | 예시 |
|------|------|
| 같은 입력이면 항상 같은 해시 | `'blue'`는 언제 해시해도 `16477688...` |
| 해시로 원래 입력을 되돌릴 수 없음 | `16477688...`만 보고 `'blue'`를 계산할 방법이 없음 |
| 입력이 조금만 달라도 해시는 완전히 다름 | `'blue'`와 `'Blue'`의 해시는 전혀 안 비슷함 |
| 입력 길이와 상관없이 해시 길이는 같음 | 3글자든 책 한 권이든 32바이트(16진수 64글자) |

### 같은 입력이면 같은 해시인데, 왜 해시로 원래 값을 못 알아낼까?

- **앞으로 가기**(`'blue'` → 해시)는 쉽지만, **거꾸로 가기**(해시 → `'blue'`)는 계산 방법이 없게 설계되어 있다.
- 비유: 17을 10으로 나눈 나머지는 7이지만, 7만 보고는 원래 수가 7인지 17인지 27인지 알 수 없다. 계산 중에 정보가 버려졌기 때문이다.
- 비유: 파랑과 노랑을 섞으면 초록이 되지만, 초록을 다시 파랑과 노랑으로 분리할 수는 없다.
- 입력이 한 글자만 달라도 해시가 완전히 바뀌므로, "b로 시작하겠네" 같은 단서도 얻을 수 없다.

### 그럼 findColor는 어떻게 맞혔나?

거꾸로 계산한 게 아니라 **앞으로 가는 계산만 반복**했다. 자물쇠를 분해하는 대신 열쇠 6개를 하나씩 꽂아 본 것이다.

| 방법 | 가능? |
|------|------|
| 해시를 거꾸로 계산해서 원래 값 구하기 | 불가능 |
| 후보를 하나씩 해시해서 비교하기 | 가능 (이 문제의 방법) |

---

## 2. 누가 해시를 넘겨주나? (test.js와 index.js의 관계)

`findColor`는 혼자 실행되지 않는다. 누군가 `findColor(값)`으로 불러야 실행되고, 그 값이 `hash`에 들어간다.
여기서는 **test.js가 출제자 겸 채점자** 역할을 한다.

```js
// test.js
assert.equal(findColor(sha256(utf8ToBytes(color))), color);
```

```
┌──────── test.js (출제자) ────────┐        ┌──────── index.js (우리) ────────┐
│ 'blue' (정답, 숨김)               │        │ findColor(hash)                 │
│    │ sha256                      │        │    │                            │
│    ▼                             │        │    ▼                            │
│ 16477688c0e0... (해시) ──────────┼───────▶│ 색 6개를 해시해 보며 비교          │
│                                  │        │    │                            │
│ 결과가 'blue'인지 채점 ◀──────────┼────────┤ 'blue' 반환                      │
└──────────────────────────────────┘        └─────────────────────────────────┘
```

- `index.js`에는 색 **이름** 6개만 있고, 해시값이 미리 저장되어 있지는 않다.
- `findColor`는 `'blue'`라는 글자를 보지 못하고 해시만 받는다.
- test.js는 이걸 6가지 색 모두에 대해 반복한다.

### test.js 한 줄씩

```js
const {assert} = require('chai');                                  // 1
const findColor = require('./index');                              // 2
const { sha256 } = require("ethereum-cryptography/sha256");        // 3
const { utf8ToBytes } = require("ethereum-cryptography/utils");    // 4

const COLORS = ['red', 'green', 'blue', 'yellow', 'pink', 'orange']; // 6

describe('findColor', () => {                                      // 8
    COLORS.forEach((color) => {                                    // 9
        it(`should work for ${color}`, () => {                     // 10
            assert.equal(findColor(sha256(utf8ToBytes(color))), color); // 11
        });
    });
});
```

| 줄 | 하는 일 | Python으로 치면 |
|----|---------|----------------|
| 1 | 테스트 라이브러리 chai에서 `assert`만 꺼냄 (`{ }`는 묶음에서 이름 하나만 꺼내는 문법) | `from chai import assert_` |
| 2 | index.js가 내보낸 함수를 통째로 가져옴 (묶음이 아니라 함수 하나라서 `{ }` 없음) | `from index import find_color` |
| 3~4 | 문제(해시)를 만들 도구. 해시를 바이트 그대로 넘기므로 `toHex`는 필요 없음 | `from hashlib import sha256` |
| 6 | 테스트할 색 목록 (index.js에 있어도 파일마다 따로 정의해야 함) | `COLORS = [...]` |
| 8 | `describe`: 테스트 묶음. mocha로 실행하면 자동으로 제공되어 require가 필요 없음 | `class TestFindColor:` |
| 9 | 색마다 반복 | `for color in COLORS:` |
| 10 | `it`: 테스트 하나. 반복문 안이라 6개 생성. `` `${color}` ``는 변수 값으로 바뀜 | f-string `f"... {color}"` |
| 11 | 안쪽부터: 바이트 변환 → 해시(**출제**) → `findColor`(**풀이**) → `assert.equal`(**채점**) | `assert find_color(...) == color` |
| 12~14 | 열었던 함수들을 안쪽부터 닫음 (JS는 들여쓰기 대신 `{ }`, `( )`로 블록 구분) | (들여쓰기) |

pytest로 옮기면:

```python
@pytest.mark.parametrize("color", COLORS)
def test_find_color(color):
    assert find_color(sha256(color.encode()).digest()) == color
```

---

## 3. 한 줄씩 따라가기 (`'blue'`의 해시가 들어왔을 때)

### 9줄: `const target = toHex(hash);`

받은 해시(바이트 32개)를 16진수 글자 64개로 바꿔서 `target`에 저장한다.

```
hash   = [22, 71, 118, 136, 192, 224, ...]   ← 숫자 32개
          16  47   76   88   c0   e0  ...    ← 숫자 하나를 16진수 두 글자로
target = "16477688c0e00699c6cfa4497a3612d7e83c532062b64b250fed8908128ed548"
```

- `toHex` = Python의 `bytes.hex()`
- 받은 해시는 바뀌지 않으므로 반복문 밖에서 **한 번만** 바꿔 둔다.

### 10줄: `COLORS.find((color) => toHex(sha256(utf8ToBytes(color))) === target)`

후보 색을 하나씩 꺼내 출제자와 **똑같은 순서**로 해시한 뒤 `target`과 비교한다. 함수가 겹쳐 있으면 가장 안쪽부터 실행된다.

```
toHex( sha256( utf8ToBytes( color ) ) )
  ③      ②         ①
```

| 순서 | 하는 일 | `'blue'`일 때 결과 |
|------|---------|--------------------|
| ① `utf8ToBytes` | 글자 → 바이트 | `[98, 108, 117, 101]` |
| ② `sha256` | 바이트 → 해시 | `[22, 71, 118, 136, ...]` (32개) |
| ③ `toHex` | 해시 → 16진수 글자 | `"16477688c0e0..."` |
| `=== target` | 받은 해시와 같은지 비교 | `true` |

```
red     b1f51a511f1da0cd... ✗ 다름
green   ba4788b226aa8dc2... ✗ 다름
blue    16477688c0e00699... ✔ 같음! → 'blue' 반환
(yellow, pink, orange는 검사하지 않음)
```

`find`는 조건이 처음 `true`가 되는 순간 멈추고 그 값을 돌려준다. 끝까지 없으면 `undefined`.

### 13줄: `module.exports = findColor;`

다른 파일(test.js)이 `require('./index')`로 이 함수를 가져갈 수 있게 내보낸다.

---

## 4. 글자 → 바이트 → 해시, 왜 이 순서인가?

### ① 글자 → 바이트 (`utf8ToBytes`)

컴퓨터는 숫자(0과 1)만 다룰 수 있어서, 글자를 정해진 규칙(UTF-8)으로 숫자로 바꿔야 한다.

| 글자 | UTF-8 바이트 |
|------|-------------|
| `'A'` | `[65]` |
| `'blue'` | `[98, 108, 117, 101]` |
| `'Blue'` | `[66, 108, 117, 101]` (대문자 B만 다름) |
| `'파랑'` | `[237, 140, 140, 235, 158, 145]` (한글은 글자당 3바이트) |

- 해시 함수는 숫자 계산이라 글자를 바로 넣을 수 없다. 실제로 `sha256("red")`처럼 문자열을 넣으면 `Uint8Array expected` 에러가 난다. Python도 `hashlib.sha256("red")`는 `TypeError: Strings must be encoded before hashing`이다.
- 파일 내용, 다른 해시값, 키처럼 **이미 바이트인 데이터**는 변환 없이 바로 넣으면 된다. 사람이 읽는 문자열일 때만 이 단계가 필요하다.
- 규칙이 다르면 바이트도 달라진다. 예를 들어 UTF-16으로 바꾼 `'blue'`는 `[98, 0, 108, 0, 117, 0, 101, 0]`이다. 그래서 출제자와 같은 규칙(UTF-8)을 써야 같은 해시가 나온다.
- Python의 `'blue'.encode('utf-8')`과 같다.

### ② 바이트 → 해시 (`sha256`)

아무 길이의 바이트를 넣으면 항상 32바이트(256비트) 결과를 만든다. 내부에서는 길이를 맞추고(padding), 비트를 더하고, 밀고, 뒤집는 과정을 64라운드 반복해서 입력을 철저히 섞는다.

---

## 5. JavaScript 문법 정리 (Python과 비교)

| 하는 일 | JavaScript | Python |
|---------|------------|--------|
| 불러오기 | `const { a } = require("x")` | `from x import a` |
| 변수 선언 | `const x = 1` (변경 불가) / `let x = 1` | `x = 1` |
| 주석 | `// 메모` | `# 메모` |
| 리스트 | `[1, 2, 3]` (배열) | `[1, 2, 3]` |
| 함수 정의 | `function f(x) { ... }` | `def f(x): ...` |
| 블록 구분 | `{ }` | 들여쓰기 |
| 이름 없는 함수 | `(x) => x * 2` | `lambda x: x * 2` |
| 같은지 비교 | `===` | `==` |
| 반복문 | `for (const x of arr) { }` | `for x in arr:` |
| 조건문 | `if (조건) { }` | `if 조건:` |
| 첫 번째로 맞는 값 찾기 | `arr.find((x) => 조건)` | `next((x for x in arr if 조건), None)` |
| 값 없음 | `undefined` / `null` | `None` |
| 출력 | `console.log(x)` | `print(x)` |
| 내보내기 | `module.exports = f` | (필요 없음) |

### 바이트 배열은 `===`로 비교하면 안 된다

```js
const a = new Uint8Array([1, 2, 3]);
const b = new Uint8Array([1, 2, 3]);

a === b                  // false: 내용이 아니라 "같은 객체인지"를 봄 (Python의 is처럼)
toHex(a) === toHex(b)    // true: "010203" === "010203"
```

Python은 `b'\x01\x02' == b'\x01\x02'`가 `True`라서 이런 변환이 필요 없다.

### `==` 대신 `===`를 쓰는 이유

`==`는 `1 == "1"`이 `true`가 되는 것처럼 타입을 바꿔서 비교한다. `===`가 Python의 `==`에 가깝다.

---

## 6. 개발 환경에서 배운 것

### 폴더 구조와 `node_modules`

```
블록체인기술과응용/
├── node_modules/        ← 설치된 라이브러리 (Python의 site-packages)
├── package.json         ← 필요한 라이브러리 목록 (장보기 목록)
├── package-lock.json    ← 설치된 정확한 버전 (영수증)
└── 01-find-favorite-color/
```

- `require`는 현재 폴더에 `node_modules`가 없으면 한 단계씩 위로 올라가며 찾는다. 그래서 바깥에 한 번만 설치하면 모든 문제 폴더에서 쓸 수 있다.
- `node_modules`는 직접 고치지 않는다. 지워도 `npm install`로 다시 만들 수 있어서 GitHub에는 올리지 않는다.

### `./`와 `../`

| 경로 | 뜻 |
|------|----|
| `./index` | 지금 파일이 있는 폴더의 `index.js` |
| `../index` | 한 단계 위 폴더의 `index.js` |

### 폴더 이름

`1: Find Favorite Color`처럼 띄어쓰기나 `:`가 있으면 터미널에서 매번 따옴표로 감싸야 한다. `01-find-favorite-color`처럼 쓰면 따옴표가 필요 없고, 앞에 두 자리 번호를 붙이면 10번이 넘어가도 순서대로 정렬된다.

### 실행 방법

```bash
# 테스트로 채점하기 (Python의 pytest)
npx mocha 01-find-favorite-color/test.js
```

`✔`만 나오면 정상이다. 테스트는 채점만 하고 과정은 보여 주지 않는다.
터미널 위치가 바깥 폴더인데 `npx mocha test.js`만 쓰면 `No test files found` 오류가 난다.

과정을 눈으로 보고 싶으면 문제 폴더에 `run.js`를 만들고 `node run.js`로 실행한다 (Python의 `python run.py`).

```js
const findColor = require("./index");
const { sha256 } = require("ethereum-cryptography/sha256");
const { toHex, utf8ToBytes } = require("ethereum-cryptography/utils");

const COLORS = ['red', 'green', 'blue', 'yellow', 'pink', 'orange'];

const secret = "blue";                      // 이 값을 바꿔 보기
const hash = sha256(utf8ToBytes(secret));
console.log("받은 해시:", toHex(hash));

const target = toHex(hash);
for (const color of COLORS) {
    const colorHash = toHex(sha256(utf8ToBytes(color)));
    const same = colorHash === target;
    console.log(color.padEnd(7), colorHash.slice(0, 16) + "...", same ? "✔ 같음!" : "✗ 다름");
    if (same) break;
}

console.log("findColor 결과:", findColor(hash));
```

목록에 없는 색(예: `"black"`)을 넣으면 6개 모두 ✗가 나오고 결과는 `undefined`다.

---

## 7. 보안 관점과 블록체인

| 상황 | 후보 수 | 하나씩 해 보면? |
|------|--------|----------------|
| 이 문제의 색깔 | 6개 | 순식간에 맞힘 |
| 4자리 숫자 비밀번호 | 1만 개 | 1초도 안 걸림 |
| 무작위 영문+숫자 20자리 | 약 10³⁵개 | 사실상 불가능 |

- 원본이 짐작하기 쉬우면 해시해도 들킨다. 그래서 비밀번호 저장에는 **salt**(무작위 값)를 섞고 느린 해시(bcrypt 등)를 쓴다.
- 블록체인은 블록마다 이전 블록의 해시를 담아 연결한다. 중간 데이터를 바꾸면 해시가 달라져서 바로 들통난다.
- 비트코인 채굴은 조건에 맞는 해시가 나올 때까지 숫자를 바꿔 가며 계속 해시하는 작업이다. 이 문제의 "하나씩 다 해 보기"를 엄청난 규모로 하는 셈이다.

## 헷갈렸던 점

- 처음에는 "blue를 프로그램에 입력한다"고 생각했다. 실제로는 test.js가 blue를 해시해서 **해시만** 넘기고, findColor는 그 해시로 원래 색을 맞힌다.
- 6개 색의 해시가 미리 준비되어 있다고 생각했다. 실제로는 색 **이름**만 있고, 해시는 10줄에서 그때그때 계산한다.
- `hash`는 처음부터 정해진 값이 아니라, 함수를 부를 때 들어오는 값의 **이름표**(매개변수)다.
