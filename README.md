# Blockchain Study

블록체인 기술과 응용 학습 기록. 문제마다 폴더를 만들고, 각 폴더의 `README.md`에 풀이와 배운 점을 정리합니다.

## 실행 방법

```bash
npm install
npx mocha 01-find-favorite-color/test.js   # 문제 폴더 이름만 바꿔서 실행
```

## 문제 목록

| # | 문제 | 핵심 개념 |
|---|------|-----------|
| 01 | [Find Favorite Color](./01-find-favorite-color) | SHA256 해시, 브루트포스, 바이트 ↔ 16진수 |
| 01 | [Hash Message](./01-hash-message) | keccak256 해시, 서명 전 단계, keccak256 vs SHA-256 |
| 02 | [Sign Message](./02-sign-message) | secp256k1 서명, 복구 비트, 공개키 복구, async/await |
| 03 | [Recover Key](./03-recover-key) | recoverPublicKey, 서명에서 공개키 복구, Uint8Array 비교 |
