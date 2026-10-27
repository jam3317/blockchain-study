ENV = """강의 사이트는 브라우저 안에서 Hardhat으로 컴파일·테스트한다. 로컬에서는 루트의 Hardhat(ethers v5)으로 똑같이 돌린다: `sh tools/sol-test.sh <폴더>`.

이 과제는 한 컨트랙트를 13단계에 걸쳐 키워 가서, 단계마다 이전 단계 코드에 무엇을 더했는지 `tools/multisig_stage.py`로 만들었다."""
ENV_ABI = ENV + "\n\n강의 테스트는 `./artifacts/contracts/MultiSig.sol/MultiSig.json` 파일을 직접 읽는다. 로컬은 컴파일 결과 위치가 달라서 `hre.artifacts.readArtifact(\"MultiSig\")`로 같은 ABI를 읽도록 바꿨다."

FLOW = """```
constructor → 입력 검사 → Transaction 저장소 → addTransaction → confirmations → confirm
→ owner만 → submit → receive → isConfirmed → execute → 즉시 실행 → calldata
```"""

def st(**kw):
    kw.setdefault("env", ENV)
    kw.setdefault("img", "MultiSig_diagram.png")
    return kw

STAGES = [
st(dir="week6/multisig-constructor", title="Constructor (Multi-Signature Wallet 1단계)",
 problem="""
1. public `address[] owners`: 지갑 주인들.
2. public `uint256 required`: 거래 실행에 필요한 확인 수.
3. constructor: owner 주소 배열과 required를 받아 저장.
""",
 summary="`owners = _owners; required = _required;` — 예: 3명 중 2명이 확인해야 돈이 나가는 지갑 (2-of-3).",
 img_alt="constructor",
 intent=f"""
> **멀티시그 지갑 = 여러 명의 서명(확인)이 모여야 돈이 나가는 스마트 컨트랙트 지갑. 개인키 하나를 잃어버리거나 도둑맞아도 돈이 안전하다.**

- 일반 계정(EOA)은 개인키 하나가 곧 모든 권한이라 **단일 실패 지점**이다.
- 쓰임새: 회사 자금, 가족 공동 지출, DAO 금고. 실제 서비스로는 Gnosis Safe(Safe)가 있다.

{FLOW}
""",
 files=[("MultiSig.sol","**이번에 완성할 컨트랙트**"),("tests.js","출제 · 채점 (테스트 2개)")],
 solution="""
```solidity
address[] public owners;
uint256 public required;

constructor(address[] memory _owners, uint256 _required) {
    owners = _owners;
    required = _required;
}
```

- 배열 인자는 `memory`. memory 배열을 storage 상태 변수에 대입하면 **복사**된다.
""",
 tests="""
```js
contract = await MultiSig.deploy(accounts.slice(0, 3), 2);   // 계정 0, 1, 2가 owner
assert.equal(accounts[2], await contract.callStatic.owners(2));
```
""",
 remember=["멀티시그 = M-of-N 확인이 있어야 실행되는 지갑."]),

st(dir="week6/multisig-errors", title="Error Handling (Multi-Signature Wallet 2단계)",
 problem="배포할 때 다음 경우 revert: owner가 없음 / required가 0 / required가 owner 수보다 큼.",
 summary="constructor 맨 앞에 `require` 세 개.",
 img_alt="입력 검사",
 intent="""
> **잘못 배포된 멀티시그는 돈이 영원히 묶일 수 있다. (예: required가 owner 수보다 크면 절대 실행 불가)**

사용자 입력은 처음에 검사한다.
""",
 files=[("MultiSig.sol","constructor에 **require 3개**"),("tests.js","출제 · 채점 (테스트 5개)")],
 solution="""
```solidity
constructor(address[] memory _owners, uint256 _required) {
    require(_owners.length > 0, "No owners");
    require(_required > 0, "Required must be at least 1");
    require(_required <= _owners.length, "Required exceeds owner count");
    owners = _owners;
    required = _required;
}
```
""",
 tests="""
```js
await expectThrow(MultiSig.deploy([], 1));
await expectThrow(MultiSig.deploy(accounts.slice(0,3), 0));
await expectThrow(MultiSig.deploy(accounts.slice(0,3), 4));
```
""",
 remember=["입력 검사는 constructor 맨 앞에서."]),

st(dir="week6/multisig-transactions", title="Transaction Struct (Multi-Signature Wallet 3단계)",
 problem="""
1. struct `Transaction`: `address destination`, `uint256 value`, `bool executed` (이 순서).
2. 거래 저장소: public mapping(uint → Transaction) 또는 public 배열 `transactions`.
3. 저장된 거래 수를 돌려주는 public `transactionCount`.
""",
 summary="`mapping(uint256 => Transaction) public transactions;` + `uint256 public transactionCount;`",
 img_alt="저장소",
 intent="한 owner가 거래를 제안하면, 다른 owner들이 확인할 때까지 컨트랙트가 거래 정보를 보관해야 한다.\n\n" + FLOW,
 files=[("MultiSig.sol","**Transaction, transactions, transactionCount**"),("tests.js","출제 · 채점 (테스트 2개) — ABI만 확인")],
 solution="""
```solidity
uint256 public transactionCount;

struct Transaction {
    address destination;
    uint256 value;
    bool executed;
}

mapping(uint256 => Transaction) public transactions;
```

mapping을 고른 이유: 번호로 바로 찾고, 개수는 transactionCount가 따로 센다.
""",
 tests="""
```js
const transactions = abi.filter(x => x.name === 'transactions')[0];
assert.deepEqual(transactions.inputs.map(x => x.type), ['uint256']);
assert.deepEqual(transactions.outputs.map(x => x.type), ['address', 'uint256', 'bool']);   // struct 필드 순서대로
```
""",
 env=ENV_ABI,
 remember=["public struct mapping의 getter는 필드들을 순서대로 돌려준다."]),

st(dir="week6/multisig-add-transaction", title="Add Transaction (Multi-Signature Wallet 4단계)",
 problem="public `addTransaction(address destination, uint256 value)`: 새 거래를 저장하고 그 **거래 번호**(0부터)를 돌려준다. executed는 false로 시작.",
 summary="`id = transactionCount` → 저장 → `transactionCount += 1` → `return id`.",
 img_alt="addTransaction",
 intent="첫 거래는 #0이 되고 count는 1, 다음 거래는 #1이 되고 count는 2.",
 files=[("MultiSig.sol","**addTransaction**"),("tests.js","출제 · 채점 (테스트 3개)")],
 solution="""
```solidity
function addTransaction(address destination, uint256 value) public returns(uint256) {
    uint256 transactionId = transactionCount;
    transactions[transactionId] = Transaction(destination, value, false);
    transactionCount += 1;
    return transactionId;
}
```
""",
 tests="""
```js
await contract.addTransaction(accounts[1], 100);
let txId = await contract.callStatic.addTransaction(accounts[1], 100);   // 실행하면 무엇을 돌려줄지만 확인
assert.equal(txId.toNumber(), 1);
```

강의 원본의 첫 테스트는 `contract.callStatic.transactions;`(괄호 없이 함수 자체)를 받아 `tx[0]`이 항상 `undefined`라서 무조건 통과한다. 로컬에서는 `transactions(0)`으로 실제로 읽도록 고쳤다.
""",
 remember=["거래 번호는 0부터, 카운터는 저장 후 증가."]),

st(dir="week6/multisig-confirmations", title="Confirmations Storage (Multi-Signature Wallet 5단계)",
 problem="public 중첩 mapping `confirmations`: 거래 번호(uint) → owner 주소 → 확인 여부(bool).",
 summary="`mapping(uint256 => mapping(address => bool)) public confirmations;`",
 img_alt="confirmations",
 intent="거래마다 누가 확인했는지를 기록하는 표.",
 files=[("MultiSig.sol","**confirmations**"),("tests.js","출제 · 채점 (테스트 1개) — ABI만 확인")],
 solution="""
```solidity
mapping(uint256 => mapping(address => bool)) public confirmations;
```
""",
 tests="""
```js
assert.deepEqual(confirmations.inputs.map(x => x.type), ['uint256', 'address']);   // 중첩 mapping getter는 키 2개
assert.deepEqual(confirmations.outputs.map(x => x.type), ['bool']);
```
""",
 env=ENV_ABI,
 remember=["중첩 mapping getter = 키를 차례로 인자로."]),

st(dir="week6/multisig-confirm", title="Owner Confirmations (Multi-Signature Wallet 6단계)",
 problem="""
1. public `confirmTransaction(transactionId)`: msg.sender의 확인을 기록.
2. public view `getConfirmationsCount(transactionId)`: 확인 수를 돌려준다.
""",
 summary="확인은 `confirmations[id][msg.sender] = true`. 개수는 **owner 배열을 돌며** true인 사람을 센다.",
 img_alt="confirm",
 intent="mapping은 키 목록을 돌 수 없다. 그래서 \"누가 확인했나\"를 세려면 확인할 수 있는 사람(owners) 배열을 돌아야 한다.",
 files=[("MultiSig.sol","**confirmTransaction, getConfirmationsCount**"),("tests.js","출제 · 채점 (테스트 2개)")],
 solution="""
```solidity
function confirmTransaction(uint256 transactionId) public {
    confirmations[transactionId][msg.sender] = true;
}

function getConfirmationsCount(uint transactionId) public view returns(uint256) {
    uint256 count;
    for (uint i = 0; i < owners.length; i++) {
        if (confirmations[transactionId][owners[i]]) {
            count++;
        }
    }
    return count;
}
```
""",
 tests="""
```js
await contract.confirmTransaction(1);                                                   // 계정 0
await contract.connect(ethers.provider.getSigner(accounts[1])).confirmTransaction(1);  // 계정 1
assert.equal(await contract.callStatic.getConfirmationsCount(1), 2);
```
""",
 remember=["mapping은 순회 불가 → 확인 가능한 사람 배열을 돈다."]),

st(dir="week6/multisig-only-owners", title="Only Owners (Multi-Signature Wallet 7단계)",
 problem="owner가 아닌 사람이 `confirmTransaction`을 부르면 revert.",
 summary="private `isOwner` 도우미 + `require(isOwner(msg.sender))`.",
 img_alt="owner만",
 intent="아무나 확인할 수 있으면 멀티시그의 의미가 없다.",
 files=[("MultiSig.sol","**isOwner, 권한 확인**"),("tests.js","출제 · 채점 (테스트 2개)")],
 solution="""
```solidity
function isOwner(address addr) private view returns(bool) {
    for (uint i = 0; i < owners.length; i++) {
        if (owners[i] == addr) return true;
    }
    return false;
}

function confirmTransaction(uint256 transactionId) public {
    require(isOwner(msg.sender), "Only owners can confirm");
    confirmations[transactionId][msg.sender] = true;
}
```

`private`: 이 컨트랙트 안에서만 쓰는 도우미 (상속받은 컨트랙트도 못 씀).
""",
 tests="""
```js
await expectThrow(contract.connect(ethers.provider.getSigner(accounts[3])).confirmTransaction(0));   // 계정 3은 owner 아님
await contract.connect(ethers.provider.getSigner(accounts[2])).confirmTransaction(0);              // 성공
```
""",
 remember=["반복되는 검사는 도우미 함수로."]),

st(dir="week6/multisig-submit", title="Submit Transactions (Multi-Signature Wallet 8단계)",
 problem="""
1. external `submitTransaction(destination, value)`: 거래를 추가하고 **바로 확인**까지 한다.
2. `addTransaction`을 public → **internal**로 바꾼다.
""",
 summary="제출하는 owner는 당연히 찬성이니 두 번의 거래를 한 번으로 줄인다. 밖에서 부를 필요 없는 함수는 숨긴다.",
 img_alt="submit",
 intent="공개 함수가 적을수록 공격받을 수 있는 입구가 줄어든다 (보안 원칙: 최소 노출).",
 files=[("MultiSig.sol","**submitTransaction**, addTransaction internal"),("tests.js","출제 · 채점 (테스트 3개)")],
 solution="""
```solidity
function addTransaction(address destination, uint256 value) internal returns(uint256) { ... }

function submitTransaction(address destination, uint value) external {
    uint256 transactionId = addTransaction(destination, value);
    confirmTransaction(transactionId);
}
```
""",
 tests="""
```js
assert.equal(contract.addTransaction, undefined, "...");   // internal이라 ABI에 없음 → ethers 객체에도 없음
```
""",
 env=ENV + "\n\n화면에서 잘려 보이지 않은 assert 메시지 끝부분은 짐작으로 채웠다 (채점 결과와 무관).",
 remember=["internal = 밖에서 안 보임 (ABI에도 없음)."]),

st(dir="week6/multisig-receive", title="Receive (Multi-Signature Wallet 9단계)",
 problem="언제든 이더를 받을 수 있게 external payable `receive` 함수 정의.",
 summary="`receive() external payable { }`",
 img_alt="receive",
 intent="조직이 모든 입금을 멀티시그 주소로 받게 할 수 있다.",
 files=[("MultiSig.sol","**receive**"),("tests.js","출제 · 채점 (테스트 1개)")],
 solution="""
```solidity
receive() external payable { }
```
""",
 tests="""
```js
await ethers.provider.getSigner(accounts[1]).sendTransaction({ to: contract.address, value });
assert.equal((await ethers.provider.getBalance(contract.address)).toString(), value.toString());
```
""",
 remember=["그냥 송금을 받으려면 receive."]),

st(dir="week6/multisig-is-confirmed", title="Check if Confirmed (Multi-Signature Wallet 10단계)",
 problem="public view `isConfirmed(transactionId)`: 확인이 충분하면 true.",
 summary="`return getConfirmationsCount(transactionId) >= required;`",
 img_alt="isConfirmed",
 intent="실행 전에 쓸 판단 함수. 이미 만든 `getConfirmationsCount`를 재사용한다.",
 files=[("MultiSig.sol","**isConfirmed**"),("tests.js","출제 · 채점 (테스트 2개)")],
 solution="""
```solidity
function isConfirmed(uint transactionId) public view returns(bool) {
    return getConfirmationsCount(transactionId) >= required;
}
```
""",
 tests="""
```js
await contract.submitTransaction(accounts[1], 100);                                       // 확인 1 (계정 0)
await contract.connect(ethers.provider.getSigner(accounts[1])).confirmTransaction(0);    // 확인 2
assert.equal(await contract.callStatic.isConfirmed(0), true);
```
""",
 remember=["`>=` (정확히 required여도 충분)."]),

st(dir="week6/multisig-execute", title="Execute (Multi-Signature Wallet 11단계)",
 problem="""
public `executeTransaction(transactionId)`:
1. 거래의 value를 destination에 보낸다.
2. 보낸 뒤 executed를 true로.
3. 🔒 확인이 충분하지 않으면 revert.
""",
 summary="검사(owner, 확인 충분, 미실행) → `executed = true` → `call{ value }`.",
 img_alt="execute",
 intent="""
- 강의 조건은 "보낸 뒤 executed = true"지만, **상태를 먼저 바꾸고 보내는** 게 안전하다 (Checks-Effects-Interactions). 받는 쪽이 컨트랙트라면 송금 중에 다시 execute를 불러 두 번 받으려 할 수 있다(재진입). `require(!executed)`와 순서가 이걸 막는다.
- 테스트의 "owner만 실행" 조건도 만족하도록 owner 확인을 넣었다.
""",
 files=[("MultiSig.sol","**executeTransaction**"),("tests.js","출제 · 채점 (테스트 4개)")],
 solution="""
```solidity
function executeTransaction(uint transactionId) public {
    require(isOwner(msg.sender), "Only owners can execute");
    require(isConfirmed(transactionId), "Not enough confirmations");
    Transaction storage transaction = transactions[transactionId];
    require(!transaction.executed, "Already executed");

    transaction.executed = true;
    (bool success, ) = transaction.destination.call{ value: transaction.value }("");
    require(success, "Transfer failed");
}
```
""",
 tests="""
```js
await signer1.sendTransaction({ to: contract.address, value });       // 1 ETH 입금
await contract.submitTransaction(recipient, transferValue);            // 0.5 ETH 제안 (확인 1)
await contract.connect(signer1).confirmTransaction(0);                 // 확인 2
await contract.connect(signer1).executeTransaction(0);
assert.equal(balanceAfter.sub(balanceBefore).toString(), transferValue.toString());
```
""",
 remember=["검사 → 상태 변경 → 송금.","`Transaction storage tx = …`로 원본 수정."]),

st(dir="week6/multisig-immediate", title="Immediate Execution (Multi-Signature Wallet 12단계)",
 problem="`confirmTransaction` 안에서, 확인이 충분해지면 바로 `executeTransaction`을 부르기.",
 summary="`if (isConfirmed(id)) executeTransaction(id);`",
 img_alt="즉시 실행",
 intent="마지막 확인자가 실행을 위해 거래를 또 보낼 필요가 없다.",
 files=[("MultiSig.sol","confirmTransaction에 **자동 실행**"),("tests.js","출제 · 채점 (테스트 4개)")],
 solution="""
```solidity
function confirmTransaction(uint256 transactionId) public {
    require(isOwner(msg.sender), "Only owners can confirm");
    confirmations[transactionId][msg.sender] = true;
    if (isConfirmed(transactionId)) {
        executeTransaction(transactionId);
    }
}
```

- 이미 실행된 거래를 또 확인하면 `executeTransaction`의 `require(!executed)` 때문에 revert된다. 그래서 확인 수가 required를 넘는 경우는 생기지 않는다.
""",
 tests="""
```js
await signer1.sendTransaction({ to: contract.address, value: transferAmount.mul(2) });   // 1 ETH (화면에서 잘린 부분은 짐작)
await contract.submitTransaction(accounts[2], transferAmount);   // 확인 1 → 아직 실행 안 됨
await contract.connect(signer1).confirmTransaction(0);           // 확인 2 → 바로 실행
assert(txn.executed);
```
""",
 env=ENV + "\n\n화면에서 잘려 보이지 않은 입금액은 `transferAmount.mul(2)`로 짐작했다 (0.5 ETH 이상이면 결과는 같다).",
 remember=["조건이 충족되는 순간 자동 실행."]),

st(dir="week6/multisig-calldata", title="Sending Calldata (Multi-Signature Wallet 13단계)",
 problem="""
1. `Transaction`의 마지막 필드로 `bytes data` 추가.
2. `addTransaction`, `submitTransaction`이 bytes 인자를 받아 전달.
3. 실행할 때 `destination.call{ value: value }(data)`로 data를 보낸다.
""",
 summary="calldata까지 저장해 두면 **이더 송금뿐 아니라 어떤 함수 호출이든** 멀티시그 승인으로 실행할 수 있다.",
 img_alt="calldata",
 intent="""
> **ERC20 토큰을 멀티시그에서 보내려면 토큰 컨트랙트의 `transfer(to, amount)`를 \"멀티시그가\" 호출해야 한다. 그 호출 내용(calldata)을 거래에 저장해 두었다가 승인되면 실행한다.**

- 이더만 보낼 때는 data를 `"0x"`(빈 값)로.
- 4주차 pass-calldata 과제(calldata 전달)의 응용이다.
""",
 files=[("MultiSig.sol","**bytes data** 추가"),("EIP20.sol","테스트용 토큰 (사이트에서는 숨겨진 파일, 로컬에서 같은 모양으로 작성)"),("tests.js","출제 · 채점 (테스트 6개)")],
 solution="""
```solidity
struct Transaction {
    address destination;
    uint256 value;
    bool executed;
    bytes data;
}

function addTransaction(address destination, uint256 value, bytes memory data) internal returns(uint256) {
    ...
    transactions[transactionId] = Transaction(destination, value, false, data);
    ...
}

function submitTransaction(address destination, uint value, bytes memory data) external {
    uint256 transactionId = addTransaction(destination, value, data);
    confirmTransaction(transactionId);
}

// executeTransaction 안에서
(bool success, ) = transaction.destination.call{ value: transaction.value }(transaction.data);
```
""",
 tests="""
```js
contract = await MultiSig.deploy(accounts.slice(0, 3), 1);    // required 1 → submit하면 바로 실행
token = await EIP20.deploy(10000, 'My Token', 1, 'MT');
await token.transfer(contract.address, 10000);                 // 멀티시그에 토큰 입금
const data = token.interface.encodeFunctionData("transfer", [accounts[2], 10000]);
await contract.submitTransaction(token.address, 0, data);      // 멀티시그가 token.transfer 호출
assert.equal((await token.balanceOf(accounts[2])).toNumber(), 10000);
await contract.submitTransaction(accounts[1], oneEther, "0x"); // 이더 송금은 빈 data
```
""",
 env=ENV + "\n\n`EIP20`은 강의 사이트에서 숨겨진 테스트용 토큰이다. 로컬에서는 생성자(초기 수량, 이름, 소수점, 기호)와 `transfer`, `balanceOf`만 같은 모양으로 직접 만들었다.",
 remember=["거래 = 목적지 + 이더 + calldata.","calldata로 어떤 함수든 실행 가능 → 승인 대상이 '돈'에서 '행동'으로 넓어진다."]),
]
