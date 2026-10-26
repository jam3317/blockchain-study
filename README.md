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

### Week 2

| # | 과제 | 단계 | 핵심 개념 |
|---|------|------|-----------|
| 17 | Coding the UTXO Model | [TXO Class](./week2/txo-class) | UTXO 모델 vs 계정 모델, spent |
| 18 | Coding the UTXO Model | [Ensure Inputs are UTXOs](./week2/utxo-inputs) | 이중 지불 방지, some, throw |
| 19 | Coding the UTXO Model | [Ensure Sufficient Input](./week2/sufficient-input) | reduce로 합계, 금액 검사 |
| 20 | Coding the UTXO Model | [Successful Transaction](./week2/mark-spent) | 검사 후 spend, 거스름돈 |
| 21 | Coding the UTXO Model | [Miner's Fee](./week2/miners-fee) | 수수료 = 입력 − 출력 |
| 22 | Build a Binary Search Tree | [Creating a Node](./week2/bst-node) | 노드, null |
| 23 | Build a Binary Search Tree | [Storing the Root](./week2/bst-root) | root |
| 24 | Build a Binary Search Tree | [Adding a Root](./week2/bst-add-root) | addNode |
| 25 | Build a Binary Search Tree | [First Layer](./week2/bst-first-layer) | 작으면 왼쪽, 크면 오른쪽 |
| 26 | Build a Binary Search Tree | [Many Layers](./week2/bst-many-layers) | 재귀 |
| 27 | Build a Binary Search Tree | [Search Tree](./week2/bst-search) | hasNode, 삼항 연산자 |
| 28 | Merkle Trees | [Combine Two Leaves](./week2/merkle-two-leaves) | 머클 루트, concat 함수 |
| 29 | Merkle Trees | [Multiple Layers](./week2/merkle-multiple-layers) | 층 단위로 합치기 |
| 30 | Merkle Trees | [Odd Leaves](./week2/merkle-odd-leaves) | 짝 없는 원소 올리기 |
| 31 | Merkle Trees | [Build the Proof](./week2/merkle-proof) | 머클 증명, 짝꿍과 방향 |
| 32 | Merkle Trees | [Verify your Proof](./week2/merkle-verify) | 증명 검증, for…of |
| 33 | Learn Tries | [Trie & Trie Node](./week2/trie-node) | 트라이, children 객체 |
| 34 | Learn Tries | [Simple Trie Insert](./week2/trie-insert) | insert, isWord |
| 35 | Learn Tries | [Branching](./week2/trie-branching) | 접두사 공유 |
| 36 | Learn Tries | [Does it Contain the Word?](./week2/trie-contains) | contains |
