# Blockchain Study

블록체인 기술과 응용 학습 기록 (Alchemy University Ethereum Bootcamp). 주차별 폴더(`week1/` …) 안에 문제 단계마다 폴더를 만들고, 각 폴더의 `README.md`에 풀이와 배운 점을 정리합니다.

## 실행 방법

```bash
npm install
npx mocha week1/find-favorite-color/test.js   # 문제 폴더 이름만 바꿔서 실행
```

## 실행 도구

- [tools/make_diagram.py](./tools/make_diagram.py): 각 README의 코드 흐름 다이어그램을 만드는 스크립트. 설정 파일은 [tools/specs/](./tools/specs/)에 있다.

## 문제 목록

### Week 1

| # | 과제 | 단계 | 핵심 개념 |
|---|------|------|-----------|
| 1 | Cryptographic Hashes | [Find Favorite Color](./week1/find-favorite-color) | SHA256 해시, 브루트포스, 바이트 ↔ 16진수 |
| 2 | Public Key Exercise | [Hash Message](./week1/hash-message) | keccak256 해시, 서명 전 단계, keccak256 vs SHA-256 |
| 3 | Public Key Exercise | [Sign Message](./week1/sign-message) | secp256k1 서명, 복구 비트, async/await |
| 4 | Public Key Exercise | [Recover Key](./week1/recover-key) | recoverPublicKey, 서명에서 공개키 복구, Uint8Array 비교 |
| 5 | Public Key Exercise | [Key to Address](./week1/key-to-address) | 공개키 → 이더리움 주소, slice, 체크섬 주소 |
| 6 | Proof of Work Miner | [Add Transaction](./week1/add-transaction) | mempool, push |
| 7 | Proof of Work Miner | [Mine Block](./week1/mine-block) | 블록 높이, 객체 리터럴 |
| 8 | Proof of Work Miner | [Block Hash](./week1/block-hash) | JSON.stringify, SHA256 블록 해시 |
| 9 | Proof of Work Miner | [Mine Transactions](./week1/mine-transactions) | 블록 크기 제한, pop, while |
| 10 | Proof of Work Miner | [Target Difficulty](./week1/target-difficulty) | 작업 증명, nonce, BigInt |
| 11 | Blockchain Data Structure | [Blocks and Hashes](./week1/blocks-and-hashes) | class, toHash, 정규식 |
| 12 | Blockchain Data Structure | [What's in a Hash?](./week1/whats-in-a-hash) | constructor, this.data, faker |
| 13 | Blockchain Data Structure | [The Genesis Block](./week1/genesis-block) | 제네시스 블록, instanceof |
| 14 | Blockchain Data Structure | [Adding Blocks](./week1/adding-blocks) | addBlock, some, 화살표 함수 |
| 15 | Blockchain Data Structure | [Linking The Blocks](./week1/linking-blocks) | previousHash, 블록 연결 |
| 16 | Blockchain Data Structure | [Validating the Chain](./week1/validating-chain) | isValid, 위조 검출 |
