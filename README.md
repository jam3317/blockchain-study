# Blockchain Study

블록체인 기술과 응용 학습 기록 (Alchemy University Ethereum Bootcamp). 주차별 폴더(`week1/` …) 안에 문제 단계마다 폴더를 만들고, 각 폴더의 `README.md`에 풀이와 배운 점을 정리합니다.

## 실행 방법

```bash
npm install
npx mocha week1/find-favorite-color/test.js   # 문제 폴더 이름만 바꿔서 실행
npx mocha week3/block-number/test.js --exit   # ganache를 쓰는 week3부터는 --exit를 붙인다
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

### Week 3

| # | 과제 | 단계 | 핵심 개념 |
|---|------|------|-----------|
| 37 | Activity: Query Ethereum | [JSON-RPC Read Requests](./week3/json-rpc-read-activity) | 공개 노드에 실제 읽기 요청, fetch |
| 38 | JSON-RPC Requests | [Current Block Number](./week3/block-number) | JSON-RPC 형식, eth_blockNumber, ganache |
| 39 | JSON-RPC Requests | [Get Balance](./week3/get-balance) | eth_getBalance, 블록 태그, wei |
| 40 | JSON-RPC Requests | [Transaction Nonce](./week3/get-nonce) | eth_getTransactionCount, 재전송 공격 |
| 41 | JSON-RPC Requests | [Block Transactions](./week3/total-transactions) | 블록 번호 16진수, 가스 한도 |
| 42 | JSON-RPC Requests | [Batch Transactions](./week3/batch-balance) | 묶음 요청, id, parseInt |
| 43 | Code a Transaction | [Send a Signed Transaction (직접 실행)](./week3/sign-tx-activity) | Sepolia, Type 2 거래, .env |
| 44 | Intro to Ethers.js | [Making Wallets](./week3/ethers-wallets) | Wallet, 니모닉 |
| 45 | Intro to Ethers.js | [Sign a Transaction](./week3/ethers-sign) | signTransaction, parseEther, 가스 |
| 46 | Intro to Ethers.js | [Connect to Ethereum](./week3/ethers-connect) | Web3Provider, 전송 |
| 47 | Intro to Ethers.js | [Account Nonce](./week3/ethers-nonce) | wallet.sendTransaction, nonce 자동 |
| 48 | Intro to Ethers.js | [Retrieve the Balance](./week3/ethers-balance) | getBalance, BigNumber |
| 49 | Intro to Ethers.js | [Donating to Charities](./week3/ethers-donate) | for…of + await, tx.wait |
| 50 | Where is the Ether? | [Where is the Ether?](./week3/where-is-the-ether) | getBlockWithTransactions, 거래 추적 |

### Week 4

Solidity 문제는 `sh tools/sol-test.sh week4/<폴더>`로 실행한다 (Hardhat).

| # | 과제 | 단계 | 핵심 개념 |
|---|------|------|-----------|
| 51 | Data Types | [Booleans](./week4/booleans) | 상태 변수, public getter |
| 52 | Data Types | [Unsigned Integers](./week4/unsigned-integers) | uint8/16/256, 범위 |
| 53 | Data Types | [Signed Integers](./week4/signed-integers) | int, 형 변환 |
| 54 | Data Types | [String Literals](./week4/string-literals) | bytes32 vs string |
| 55 | Data Types | [Enum Type](./week4/enum-type) | enum |
| 56 | Functions | [Arguments](./week4/constructor-arguments) | constructor 인자, shadowing |
| 57 | Functions | [Increment](./week4/increment) | external, 거래 |
| 58 | Functions | [View Addition](./week4/view-addition) | view, returns |
| 59 | Functions | [Pure Double](./week4/pure-double) | pure |
| 60 | Functions | [Overloading Functions](./week4/overload-double) | 오버로딩, 튜플 |
| 61 | Contracts with ethers.js | [Contracts](./week4/contract-get-value) | ABI, Contract 객체 |
| 62 | Contracts with ethers.js | [Transactions](./week4/contract-set-value) | Signer, 쓰기 거래 |
| 63 | Contracts with ethers.js | [Multiple Arguments](./week4/contract-transfer) | mapping, msg.sender, require |
| 64 | Contracts with ethers.js | [Signer](./week4/contract-signer) | connect |
| 65 | Contracts with ethers.js | [Value Transfer](./week4/contract-deposit) | payable, overrides { value } |
| 66 | Sending Ether | [Storing Owner](./week4/storing-owner) | address, msg.sender |
| 67 | Sending Ether | [Receive Ether](./week4/receive-ether) | receive() |
| 68 | Sending Ether | [Transferring Funds](./week4/transfer-tips) | call{value} |
| 69 | Sending Ether | [Charity](./week4/charity) | address(this).balance |
| 70 | Sending Ether | [Self Destruct](./week4/self-destruct) | selfdestruct, Cancun |
| 71 | Learning Revert | [Constructor Revert](./week4/constructor-revert) | require, revert |
| 72 | Learning Revert | [Only Owner](./week4/owner-withdrawal) | 접근 제어 |
| 73 | Learning Revert | [Function Modifiers](./week4/only-owner-modifier) | modifier, _ |
| 74 | Sending Data | [Interfaces](./week4/interface-alert) | interface |
| 75 | Sending Data | [Function Signature](./week4/function-signature) | 함수 선택자 |
| 76 | Sending Data | [With Signature](./week4/encode-with-signature) | abi.encodeWithSignature |
| 77 | Sending Data | [Taking Calldata](./week4/pass-calldata) | calldata 전달 |
| 78 | Sending Data | [Fallback](./week4/fallback) | fallback() |
| 79 | Sum and Average | [Sum and Average](./week4/sum-and-average) | 정수 나눗셈, 이름 붙은 반환값 |
| 80 | Countdown | [Countdown](./week4/countdown) | 카운터 + selfdestruct |

### Week 5

| # | 과제 | 단계 | 핵심 개념 |
|---|------|------|-----------|
| 81 | Mappings | [Members Mapping](./week5/members-mapping) | mapping, 기본값 |
| 82 | Mappings | [Is Member](./week5/is-member) | O(1) 조회 |
| 83 | Mappings | [Remove Member](./week5/remove-member) | mapping 삭제 |
| 84 | Mappings | [Mapping to Struct](./week5/mapping-structs) | mapping → struct, isActive |
| 85 | Mappings | [Types of Balances](./week5/transfer-amount) | 토큰 잔액, storage vs memory |
| 86 | Mappings | [Nested Mappings](./week5/nested-mappings) | 중첩 mapping |
| 87 | Events | [Deployed](./week5/event-deployed) | event, emit, 로그 |
| 88 | Events | [Transfer](./week5/event-transfer) | 인자 2개 이벤트 |
| 89 | Events | [Mark the Price](./week5/event-for-sale) | block.timestamp |
| 90 | Events | [Make a Purchase](./week5/event-purchase) | Checks-Effects-Interactions |
| 91 | Events | [Indexed](./week5/event-indexed) | indexed, topics |
| 92 | Build an Escrow | [State Variables](./week5/escrow-addresses) | 에스크로 3역할 |
| 93 | Build an Escrow | [Constructor Storage](./week5/escrow-constructor) | constructor |
| 94 | Build an Escrow | [Funding](./week5/escrow-funding) | payable constructor |
| 95 | Build an Escrow | [Approval](./week5/escrow-approve) | 송금 |
| 96 | Build an Escrow | [Lock it Down](./week5/escrow-security) | arbiter 권한 |
| 97 | Build an Escrow | [Events](./week5/escrow-event) | Approved 이벤트 |
| 98 | Build an Escrow | [Deploy Escrow](./week5/escrow-deploy) | ContractFactory |
| 99 | Build an Escrow | [Approve](./week5/escrow-approve-js) | connect(signer) |
| 100 | Arrays | [Fixed Sum](./week5/fixed-sum) | uint[5], calldata |
| 101 | Arrays | [Dynamic Sum](./week5/dynamic-sum) | uint[] |
| 102 | Arrays | [Filter Even](./week5/filter-even) | storage push |
| 103 | Arrays | [Filter to Memory](./week5/filter-to-memory) | new uint[](n) |
| 104 | Arrays | [Stack Club](./week5/stack-club-add) | 주소 배열 검색 |
| 105 | Arrays | [Pop](./week5/stack-club-pop) | pop, onlyMember |
| 106 | Structs | [Vote Storage](./week5/vote-storage) | struct |
| 107 | Structs | [Vote Memory](./week5/vote-memory) | struct 반환 |
| 108 | Structs | [Vote Array](./week5/vote-array) | struct 배열 |
| 109 | Structs | [Choice Lookup](./week5/choice-lookup) | internal 도우미, 튜플 |
| 110 | Structs | [Vote Once](./week5/vote-once) | public vs external |
| 111 | Structs | [Change Vote](./week5/change-vote) | storage 원소 수정 |
