# 01. Hash Message

## 문제

문자열 메시지를 받아서 **keccak256 해시**로 바꿔 돌려주는 `hashMessage` 함수를 완성하기.
(과제 번역에는 "해시태그로 변환"이라고 되어 있지만, 원문 "Hash a Message"는 **메시지를 해시하기**라는 뜻이다.)

## 한 줄 요약

문자열을 **바이트로 바꾸고 → keccak256으로 해시**해서 32바이트를 그대로 돌려준다. 이더리움에서 서명하기 전의 첫 단계다.

![hashMessage 한눈에 보기](./hashMessage_diagram.png)

---

## 0. 이 과제가 말하려는 것

> **서명은 메시지에 바로 하지 않는다. 먼저 32바이트 지문(해시)을 만들고, 그 지문에 서명한다.**

```
메시지 ──→ [해시하기] ──→ 서명하기 ──→ 검증하기
           ★ 이 과제      개인키로       서명에서 공개키·주소를 찾아
           32바이트 지문   도장 찍기      "누가 썼나" 확인
```

왜 메시지를 바로 서명하지 않고 해시부터 할까?

| 이유 | 설명 |
|------|------|
| 길이가 항상 같다 | 메시지가 한 글자든 책 한 권이든 해시는 항상 32바이트다. 서명 계산은 정해진 크기의 숫자를 다루기 때문에 크기가 고정되면 편하다. |
| 빠르다 | 긴 메시지 전체에 서명 계산을 하는 것보다, 해시를 한 번 구하고 32바이트에만 서명하는 게 훨씬 빠르다. |
| 조금만 바꿔도 들킨다 | 메시지가 한 글자만 바뀌어도 해시가 완전히 달라진다. 그래서 해시에 서명해도 메시지 전체에 서명한 것과 같은 효과가 있다. |

이 과제에서 함께 익히는 것:
1. **이더리움의 해시 함수는 keccak256**이다. 비트코인의 SHA-256과 다르다.
2. **데이터 형식의 흐름**: 문자열 → 바이트 → 해시(바이트) → 16진수 문자열. 각 단계에서 무엇을 다루는지 구분해야 한다.

---

## 1. 정답 코드

```js
const { keccak256 } = require("ethereum-cryptography/keccak");
const { utf8ToBytes } = require("ethereum-cryptography/utils");

function hashMessage(message) {
    return keccak256(utf8ToBytes(message));
}

module.exports = hashMessage;
```

### 안쪽부터 읽기

```
return keccak256( utf8ToBytes(message) );
          ②            ①
```

| 순서 | 코드 | 하는 일 | `'hello world'`일 때 |
|------|------|---------|----------------------|
| ① | `utf8ToBytes(message)` | 문자열 → 바이트 | `68 65 6c 6c 6f 20 77 6f 72 6c 64` (11개) |
| ② | `keccak256(...)` | 바이트 → 32바이트 해시 | `47 17 32 85 a8 d7 ... ad` (32개) |
| | `return` | 해시를 **바이트 그대로** 반환 | `Uint8Array(32)` |

같은 동작을 Python으로 쓰면 (pycryptodome 라이브러리 사용):

```python
from Crypto.Hash import keccak

def hash_message(message):
    return keccak.new(digest_bits=256, data=message.encode("utf-8")).digest()
```

### 지난 문제와 비교

지난 문제의 `toHex(sha256(utf8ToBytes(color)))`에서 **`sha256` → `keccak256`으로 바꾸고 `toHex`를 빼면** 이번 정답이다.

| | 01-find-favorite-color | 01-hash-message |
|---|---|---|
| 해시 함수 | `sha256` | `keccak256` |
| 함수가 받는 것 | 해시 | 문자열 |
| 함수가 돌려주는 것 | 색 이름 (문자열) | 해시 (바이트) |
| 방향 | 해시 → 원래 값 찾기 | 원래 값 → 해시 만들기 |

---

## 2. test.js 한 줄씩

```js
const hashMessage = require('./hashMessage');                       // 1
const { assert } = require('chai');                                 // 2
const { toHex } = require("ethereum-cryptography/utils");           // 3

const helloWorldHex = '47173285a8d7341e5e972fc677286384f802f8ef42a5ec5f03bbfa254cb01fad'; // 5

describe('Hash Message', () => {                                    // 7
    it('should return the keccak256 hash of hello world', () => {   // 8
        const messageHash = hashMessage('hello world');             // 9
        assert.equal(toHex(messageHash), helloWorldHex);            // 11
    });
});
```

| 줄 | 하는 일 |
|----|---------|
| 1 | 내가 완성할 함수를 가져옴. 원래 강의 코드는 `'../hashMessage'`였는데, test.js와 같은 폴더에 있으므로 `'./hashMessage'`로 고쳐야 한다. |
| 2 | 채점 도구 `assert` |
| 3 | 바이트 → 16진수 문자열 변환 도구. 11줄에서 쓴다. |
| 5 | **정답지**: `'hello world'`의 keccak256 해시 (16진수 64글자 = 32바이트) |
| 7~8 | 테스트 묶음과 테스트 1개. 테스트 이름이 곧 요구사항이다. |
| 9 | 내 함수에 **문자열**을 넣고 결과를 받음 |
| 11 | 결과를 `toHex`로 바꿔서 정답지와 비교 |

**11줄에서 알 수 있는 점**: test.js가 직접 `toHex`를 하므로, `hashMessage`는 16진수 문자열이 아니라 **바이트(`Uint8Array`) 그대로** 돌려줘야 한다.

---

## 3. 문자열은 왜 꼭 바이트로 바꿔야 하나?

해시 함수는 글자가 아니라 숫자(바이트)를 섞는 계산이라 문자열을 바로 넣을 수 없다.

```js
keccak256("hello world")   // ERROR: Uint8Array expected
```

```python
hashlib.sha256("hello world")   # TypeError: Strings must be encoded before hashing
```

같은 글자도 바꾸는 규칙(인코딩)에 따라 바이트가 달라진다. 그래서 **UTF-8로 바꾼다고 명시**한다.
파일 내용, 다른 해시, 키처럼 **이미 바이트인 데이터**는 변환 없이 바로 넣으면 된다.

---

## 4. keccak256과 SHA-256의 차이

같은 `"hello world"`를 넣어도 결과가 완전히 다르다.

```
sha256     b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9
keccak256  47173285a8d7341e5e972fc677286384f802f8ef42a5ec5f03bbfa254cb01fad
sha3-256   644bcc7e564373040999aac89e7622f3ca71fba1d972fd94a31c3bfbf24e3938
```

| | SHA-256 | keccak256 |
|---|---|---|
| 출력 길이 | 32바이트 | 32바이트 |
| 소속 | SHA-2 계열 (NSA, 2001) | SHA-3 대회 우승작 Keccak (2012) |
| 섞는 방식 | 데이터를 조각내서 차례로 압축 (반죽 기계) | 흡수했다가 짜내는 "스펀지" 방식 |
| 주로 쓰는 곳 | **비트코인**, HTTPS, 파일 무결성 확인 | **이더리움** |

### keccak256 ≠ SHA3-256

keccak이 대회에서 우승한 뒤, 미국 표준기관(NIST)이 설정을 살짝 바꿔 **SHA3-256**이라는 이름으로 표준을 만들었다. 이더리움은 표준이 확정되기 **전에** 원래 keccak을 채택했다.
그래서 Python 기본 `hashlib.sha3_256()`으로는 이더리움 해시가 나오지 않는다. 이더리움 코드에서 `sha3`라는 이름이 keccak256을 뜻하는 경우도 있어서 헷갈리기 쉽다.

### 그 밖의 차이

SHA-256에는 해시 값만 알아도 원본 뒤에 데이터를 덧붙인 것의 해시를 계산할 수 있는 **길이 확장 공격**이라는 약점이 있다. keccak은 스펀지 구조라 이 약점이 없다.

---

## 5. 배경: 공개키와 개인키

다음 문제(서명)로 이어지는 개념. 두 키는 한 쌍이고, **한쪽으로 잠근 건 다른 쪽으로만 열린다.**

| 키 | 누가 가짐 | 비유 |
|---|---|---|
| 공개키 | 모두에게 공개 | 이름표, 전화번호부의 번호 |
| 개인키 | 나만 가짐 | 도장, 비밀번호 |

| 사용법 | 잠그는 키 | 여는 키 | 목적 | 비유 |
|---|---|---|---|---|
| 서명 | 내 **개인키** | 내 **공개키** | 누가 썼는지 증명 | 도장 |
| 암호화 | 받는 사람의 **공개키** | 받는 사람의 **개인키** | 그 사람만 읽게 함 | 우편함 |

### 서명에서 "개인키로 잠근다"는 게 무슨 뜻?

여기서 "잠금"은 숨기는 게 아니라 **나만 할 수 있는 방식으로 도장을 찍는다**는 뜻이다.

```
밥이 공개하는 것:  원본 "앨리스에게 1 ETH 보냄"  +  서명 (원본을 개인키로 변형한 값)
누구나 확인:      서명을 밥의 공개키로 되돌림 → 원본과 같으면 밥이 쓴 게 맞음
```

- 원본만 바꾸면: 서명을 되돌린 값과 원본이 달라서 들킨다.
- 서명을 지어내면: 밥의 개인키가 없어서 맞는 값을 만들 수 없다.

작은 숫자로 원리 확인하기 (실제로는 수백 자리 숫자를 쓴다):

```python
n, private_key, public_key = 33, 7, 3
message = 4

signature = pow(message, private_key, n)   # 밥: 4^7 % 33 = 16
pow(signature, public_key, n)              # 누구나: 16^3 % 33 = 4 → 원본과 같음 ✓
pow(10, public_key, n)                     # 지어낸 서명: 10 → 4가 아님 ✗
```

실제 이더리움 서명(ECDSA)은 메시지를 "암호화"하는 방식은 아니지만, **개인키로만 만들 수 있고 공개키로 누구나 확인할 수 있다**는 성질은 같다. 그리고 이때 서명하는 대상이 바로 이 과제에서 만든 **메시지의 해시**다.

---

## 6. 실행 방법

```bash
# 테스트로 채점하기 (바깥 폴더 기준)
npx mocha 01-hash-message/test.js
```

```
  Hash Message
    ✔ should return the keccak256 hash of hello world

  1 passing
```

해시값을 직접 보고 싶을 때:

```bash
node -e 'const h = require("./01-hash-message/hashMessage"); const { toHex } = require("ethereum-cryptography/utils"); console.log(toHex(h("hello world")))'
```

`"hello world"`를 다른 문자열로 바꾸면 해시가 완전히 달라진다.

---

## 7. Git에 올리기

```bash
git add 01-hash-message
git commit -m "01-hash-message 풀이"
git push
```

| 단계 | 하는 일 | 비유 |
|------|---------|------|
| `git add` | 기록할 파일 고르기 | 택배 상자에 담기 |
| `git commit` | 내 컴퓨터에 기록 | 상자 봉하고 송장 붙이기 |
| `git push` | GitHub로 보내기 | 택배 보내기 |

VS Code에서 초록색 글자와 **U**(Untracked) 표시는 아직 Git에 한 번도 올라가지 않은 새 파일이라는 뜻이다. 커밋하면 흰색으로 돌아간다.

## 헷갈렸던 점

- "해시태그로 변환"은 번역 실수다. **메시지를 해시하기**라는 뜻이다.
- `hashMessage`가 16진수 문자열을 돌려줘야 한다고 생각하기 쉽다. test.js가 `toHex`를 해 주니까 **바이트 그대로** 돌려줘야 한다.
- keccak256과 SHA3-256은 같은 거라고 생각하기 쉽지만 결과가 다르다.
- 서명의 "개인키로 잠근다"는 숨기는 게 아니라 **나만 찍을 수 있는 도장**을 찍는 것이다.
