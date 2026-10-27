ENV = """강의 사이트는 브라우저 안에서 Hardhat으로 컴파일·테스트한다. 로컬에서는 루트의 Hardhat(ethers v5)과 `hardhat.config.js`로 똑같이 돌린다. `sh tools/sol-test.sh <폴더>`가 그 폴더의 `.sol`만 컴파일하고 테스트를 실행한다. 이 과제들은 `pragma solidity 0.8.4;`라서 설정에 0.8.4 컴파일러를 추가했다."""
ENV_CUT = ENV + "\n\n화면에서 잘려 보이지 않은 assert 메시지 끝부분은 짐작으로 채웠다 (채점 결과와 무관)."

ESCROW_FLOW = """```
[주소 3개] → constructor → payable → approve → arbiter만 → 이벤트 → JS로 배포 → JS로 승인
 escrow-addresses  escrow-constructor  escrow-funding  escrow-approve  escrow-security  escrow-event  escrow-deploy  escrow-approve-js
```"""

ESCROW_ROLES = """| 역할 | 하는 일 |
|------|---------|
| 🙂 **depositor** (맡기는 사람) | 돈을 맡긴다. 컨트랙트를 배포하는 사람 |
| 👨‍🔧 **beneficiary** (받는 사람) | 물건·서비스를 제공하고 돈을 받는다 |
| 👩‍⚖️ **arbiter** (승인자) | 거래가 끝났다고 판단하면 돈을 풀어 준다 |"""

def esc(**kw):
    kw.setdefault("env", ENV)
    return kw

STAGES = [
esc(dir="week5/escrow-addresses", title="State Variables (Build an Escrow 1단계)",
 problem="에스크로의 세 참여자 주소를 public 상태 변수로 만들기: `depositor`, `beneficiary`, `arbiter`.",
 summary="`address public depositor; address public beneficiary; address public arbiter;`",
 img="Escrow_diagram.png", img_alt="Escrow",
 intent=f"""
> **에스크로 = 믿을 만한 제3자가 돈을 맡아 두었다가, 조건이 충족되면 넘겨주는 거래. 컨트랙트가 그 "맡아 두는 곳"이 된다.**

{ESCROW_ROLES}

{ESCROW_FLOW}
""",
 files=[("Escrow.sol","**이번에 완성할 컨트랙트**"),("tests.js","출제 · 채점 (테스트 3개)")],
 solution="""
```solidity
contract Escrow {
    address public depositor;
    address public beneficiary;
    address public arbiter;
}
```
""",
 tests="""
```js
assert(contract.arbiter, "Did not find an arbiter!");   // getter 함수가 있는지만 확인 (값은 아직 0x000…)
```
""",
 run="sh tools/sol-test.sh week5/escrow-addresses",
 remember=["에스크로 = 조건부로 돈을 넘겨주는 중개.","세 역할: depositor, beneficiary, arbiter."]),

esc(dir="week5/escrow-constructor", title="Constructor Storage (Build an Escrow 2단계)",
 problem="arbiter 주소와 beneficiary 주소를 (이 순서로) 받는 constructor를 만들어 저장하기. depositor는 배포하는 사람(`msg.sender`).",
 summary="`arbiter = _arbiter; beneficiary = _beneficiary; depositor = msg.sender;`",
 img="Escrow_diagram.png", img_alt="constructor",
 intent="세 사람이 조건에 합의할 때마다 depositor가 새 Escrow를 배포한다. 다른 두 사람에게 주소를 받아 constructor 인자로 넣는다.\n\n" + ESCROW_FLOW,
 files=[("Escrow.sol","escrow-addresses + **constructor**"),("tests.js","출제 · 채점 (테스트 3개)")],
 solution="""
```solidity
constructor(address _arbiter, address _beneficiary) {
    arbiter = _arbiter;
    beneficiary = _beneficiary;
    depositor = msg.sender;
}
```
""",
 tests="""
```js
const roles = ['arbiter', 'beneficiary', 'depositor'];   // 계정 0, 1, 2
contract = await Contract.connect(accounts.depositor.signer).deploy(
    accounts.arbiter.address, accounts.beneficiary.address);
assert.equal(await contract.callStatic.depositor(), accounts.depositor.address);
```
""",
 wrong=[("인자 순서를 (beneficiary, arbiter)로","두 주소가 뒤바뀌어 실패")],
 run="sh tools/sol-test.sh week5/escrow-constructor",
 remember=["배포자 = msg.sender = depositor."]),

esc(dir="week5/escrow-funding", title="Funding (Build an Escrow 3단계)",
 problem="constructor를 **payable**로 바꿔서 배포할 때 이더를 맡길 수 있게 하기.",
 summary="`constructor(...) payable` — 배포 거래에 실린 이더가 그대로 컨트랙트 잔액이 된다.",
 img="Escrow_diagram.png", img_alt="payable constructor",
 intent="depositor가 이더를 맡기면, arbiter가 승인한 뒤 beneficiary에게 넘어간다.\n\n" + ESCROW_FLOW,
 files=[("Escrow.sol","escrow-constructor + **payable**"),("tests.js","출제 · 채점 (테스트 4개)")],
 solution="""
```solidity
constructor(address _arbiter, address _beneficiary) payable {
    arbiter = _arbiter;
    beneficiary = _beneficiary;
    depositor = msg.sender;
}
```
""",
 tests="""
```js
contract = await Contract.connect(depositor).deploy(arbiter, beneficiary, { value: deposit });   // 1 ETH
assert.equal((await ethers.provider.getBalance(contract.address)).toString(), deposit.toString());
```
""",
 wrong=[("payable 없음","이더를 실은 배포가 revert → 준비 단계에서 에러")],
 run="sh tools/sol-test.sh week5/escrow-funding",
 remember=["constructor도 payable이 될 수 있다."]),

esc(dir="week5/escrow-approve", title="Approval (Build an Escrow 4단계)",
 problem="""
1. external 함수 `approve`: 컨트랙트 잔액 전부를 beneficiary에게 보낸다.
2. public bool `isApproved`: 처음엔 false, 승인 후 true.
""",
 summary="`isApproved = true;` + `beneficiary.call{ value: address(this).balance }(\"\")`",
 img="Escrow_diagram.png", img_alt="approve",
 intent="beneficiary가 물건·서비스를 제공하면 arbiter가 승인해서 돈을 넘긴다. (이번 단계는 아직 아무나 approve를 부를 수 있다 → 다음 단계에서 막음)\n\n" + ESCROW_FLOW,
 files=[("Escrow.sol","escrow-funding + **isApproved, approve**"),("tests.js","출제 · 채점 (테스트 3개)")],
 solution="""
```solidity
bool public isApproved;

function approve() external {
    isApproved = true;
    (bool sent, ) = beneficiary.call{ value: address(this).balance }("");
    require(sent, "Failed to send ether");
}
```

상태(isApproved)를 먼저 바꾸고 외부 호출(송금)은 나중에 (Checks-Effects-Interactions).
""",
 tests="""
```js
beforeBalance = await ethers.provider.getBalance(accounts.beneficiary.address);
await contract.connect(accounts.arbiter.signer).approve();
assert.equal(after.sub(beforeBalance).toString(), deposit.toString());   // beneficiary는 가스를 안 내서 정확히 +1 ETH
assert(await contract.isApproved());
```
""",
 run="sh tools/sol-test.sh week5/escrow-approve",
 remember=["송금은 `.call{ value }` + 성공 확인.","상태 변경 → 외부 호출 순서."]),

esc(dir="week5/escrow-security", title="Lock it Down (Build an Escrow 5단계)",
 problem="arbiter가 아닌 사람이 `approve`를 부르면 revert하기.",
 summary="`require(msg.sender == arbiter, \"...\");`",
 img="Escrow_diagram.png", img_alt="arbiter only",
 intent="돈을 풀어 줄 권한은 arbiter에게만 있다. 이게 없으면 beneficiary가 일을 하기도 전에 스스로 돈을 가져갈 수 있다.\n\n" + ESCROW_FLOW,
 files=[("Escrow.sol","escrow-approve + **권한 확인**"),("tests.js","출제 · 채점 (테스트 3개)")],
 solution="""
```solidity
function approve() external {
    require(msg.sender == arbiter, "Only the arbiter can approve");
    isApproved = true;
    (bool sent, ) = beneficiary.call{ value: address(this).balance }("");
    require(sent, "Failed to send ether");
}
```
""",
 tests="""
```js
await contract.connect(accounts.beneficiary.signer).approve();   // 에러가 나야 통과
await contract.connect(accounts.arbiter.signer).approve();       // 성공 → beneficiary +1 ETH
```
""",
 run="sh tools/sol-test.sh week5/escrow-security", env=ENV_CUT,
 remember=["권한 확인은 함수 맨 앞에서 require."]),

esc(dir="week5/escrow-event", title="Events (Build an Escrow 6단계)",
 problem="beneficiary에게 보낸 금액(uint 하나)을 담는 이벤트 `Approved`를 만들고, `approve` 안에서 emit하기.",
 summary="보내기 **전에** 잔액을 변수에 담아 두고, 송금 후 `emit Approved(balance)`.",
 img="Escrow_diagram.png", img_alt="Approved",
 intent="프론트엔드는 이벤트를 구독해서 \"승인됨\"을 화면에 보여 줄 수 있다.\n\n" + ESCROW_FLOW,
 files=[("Escrow.sol","escrow-security + **Approved 이벤트**"),("tests.js","출제 · 채점 (테스트 5개)")],
 solution="""
```solidity
event Approved(uint balance);

function approve() external {
    require(msg.sender == arbiter, "Only the arbiter can approve");
    uint balance = address(this).balance;
    isApproved = true;
    (bool sent, ) = beneficiary.call{ value: balance }("");
    require(sent, "Failed to send ether");
    emit Approved(balance);
}
```
""",
 tests="""
```js
let tx = await contract.connect(accounts.arbiter.signer).approve();
receipt = await tx.wait();
const event = receipt.events.find(x => x.event === "Approved");
assert.equal(event.args[0].toString(), deposit.toString(), "...");
```
""",
 wrong=[("송금 후 `emit Approved(address(this).balance)`","이미 보내서 잔액이 0 → 이벤트 금액 테스트 실패")],
 run="sh tools/sol-test.sh week5/escrow-event",
 remember=["보내고 나면 잔액이 바뀐다 → 필요한 값은 먼저 저장."]),

esc(dir="week5/escrow-deploy", title="Deploy Escrow (Build an Escrow 7단계)",
 problem="`deploy.js`의 `deploy(abi, bytecode, signer, arbiterAddress, beneficiaryAddress)`를 완성하기. ContractFactory를 만들고, 생성자 인자와 1 ETH 예치금으로 배포한 뒤 그 Promise를 돌려준다.",
 summary="`new ethers.ContractFactory(abi, bytecode, signer).deploy(arbiter, beneficiary, { value: parseEther(\"1\") })`",
 img="deploy_diagram.png", img_alt="deploy",
 intent="""
> **Hardhat의 `getContractFactory`가 내부에서 하던 일을 직접 해 본다. 컴파일 결과(ABI + 바이트코드)와 서명자만 있으면 어디서든 배포할 수 있다.**

- 배포 거래 = 바이트코드 + ABI로 인코딩한 생성자 인자. `to` 주소가 없다.
- overrides 객체(`{ value, gasLimit, nonce … }`)는 항상 마지막 인자.
""" + "\n" + ESCROW_FLOW,
 files=[("deploy.js","**이번에 완성할 함수**"),("Escrow.sol","escrow-event 과제 그대로"),("tests.js","출제 · 채점 (테스트 5개)")],
 solution="""
```js
function deploy(abi, bytecode, signer, arbiterAddress, beneficiaryAddress) {
    const factory = new ethers.ContractFactory(abi, bytecode, signer);
    return factory.deploy(arbiterAddress, beneficiaryAddress, {
        value: ethers.utils.parseEther("1"),
    });
}
```
""",
 tests="""
```js
// 강의 원본: ./artifacts/contracts/Escrow.sol/Escrow.json 파일을 직접 읽음
const { abi, bytecode } = await hre.artifacts.readArtifact("Escrow");   // 로컬: 같은 내용을 Hardhat API로 읽음
contract = await deploy(abi, bytecode, accounts.depositor.signer, arbiter, beneficiary);
```
""",
 run="sh tools/sol-test.sh week5/escrow-deploy",
 env=ENV + "\n\n로컬은 컴파일 결과를 `.hardhat/artifacts/…`에 두기 때문에, 테스트가 아티팩트 파일 경로를 직접 읽는 대신 `hre.artifacts.readArtifact`로 같은 ABI·바이트코드를 읽도록 바꿨다.",
 remember=["배포 = ContractFactory(abi, bytecode, signer).deploy(인자…, overrides)."]),

esc(dir="week5/escrow-approve-js", title="Approve (Build an Escrow 8단계)",
 problem="`approve.js`의 `approve(contract, arbiterSigner)`: arbiter 서명자로 Escrow의 `approve`를 호출하고 거래 Promise를 돌려주기.",
 summary="`return contract.connect(arbiterSigner).approve();`",
 img="approve_diagram.png", img_alt="approve",
 intent="프론트엔드의 \"승인\" 버튼이 하는 일이 바로 이것이다. arbiter가 서명해야 컨트랙트의 `require(msg.sender == arbiter)`를 통과한다.\n\n" + ESCROW_FLOW,
 files=[("approve.js","**이번에 완성할 함수**"),("Escrow.sol","escrow-event 과제 그대로"),("tests.js","출제 · 채점 (테스트 2개)")],
 solution="""
```js
function approve(contract, arbiterSigner) {
    return contract.connect(arbiterSigner).approve();
}
```
""",
 tests="""
```js
await approve(contract, accounts.arbiter.signer);
assert.equal(after.sub(balanceBefore).toString(), deposit.toString());
```
""",
 wrong=[("`contract.approve()` (connect 없이)","컨트랙트가 배포자(depositor)에 연결된 채라 depositor가 서명 → `require(msg.sender == arbiter)` 실패 (직접 확인함)")],
 run="sh tools/sol-test.sh week5/escrow-approve-js",
 remember=["누가 서명하느냐 = connect(signer)."]),

esc(dir="week5/fixed-sum", title="Fixed Sum (Arrays 1단계)",
 problem="크기 5짜리 고정 배열 `uint[5]`를 받아 합을 돌려주는 pure, external 함수 `sum` 만들기.",
 summary="`for (uint i = 0; i < numbers.length; i++) total += numbers[i];`",
 img="contract_diagram.png", img_alt="sum",
 intent="""
> **고정 크기 배열은 컴파일할 때 크기가 정해져서 늘이거나 줄일 수 없다.**

```
[고정 배열 합] → 동적 배열 합 → storage에 push → memory 배열 → StackClub → pop
 ★ 이 단계      dynamic-sum   filter-even      filter-to-memory  stack-club-add  stack-club-pop
```

| 데이터 위치 | 뜻 |
|-------------|-----|
| `storage` | 체인에 영구 저장 (상태 변수) |
| `memory` | 함수 실행 중에만 있는 임시 공간 |
| `calldata` | 외부에서 받은 인자, 읽기 전용 (가장 쌈) |

함수 안의 배열·문자열·구조체에는 이 중 하나를 꼭 적어야 한다.
""",
 files=[("contract.sol","**이번에 완성할 컨트랙트**"),("tests.js","출제 · 채점 (테스트 1개)")],
 solution="""
```solidity
function sum(uint[5] calldata numbers) external pure returns(uint total) {
    for (uint i = 0; i < numbers.length; i++) {
        total += numbers[i];
    }
}
```

`for (uint i = 0; i < n; i++)`는 Python의 `for i in range(n):`. 이름 붙은 반환값 `total`은 0에서 시작한다.
""",
 tests="""
```js
assert.equal(await contract.sum([1, 1, 1, 1, 1]), 5);
assert.equal(await contract.sum([1, 2, 3, 4, 5]), 15);
```
""",
 wrong=[("4개짜리 배열로 호출","ABI 인코딩 단계에서 에러 (길이가 5여야 함)")],
 run="sh tools/sol-test.sh week5/fixed-sum",
 remember=["`uint[5]` = 고정 크기.","배열 인자에는 데이터 위치(calldata/memory)를 적는다."]),

esc(dir="week5/dynamic-sum", title="Dynamic Sum (Arrays 2단계)",
 problem="크기가 정해지지 않은 `uint[]`를 받아 합을 돌려주기.",
 summary="`uint[5]` → `uint[]`만 바꾸면 된다. 반복 횟수는 `numbers.length`.",
 img="contract_diagram.png", img_alt="sum",
 intent="동적 배열은 실행할 때 크기가 정해진다. 길이는 `.length`로 읽는다.",
 files=[("contract.sol","**sum (동적 배열)**"),("tests.js","출제 · 채점 (테스트 1개)")],
 solution="""
```solidity
function sum(uint[] calldata numbers) external pure returns(uint total) {
    for (uint i = 0; i < numbers.length; i++) {
        total += numbers[i];
    }
}
```
""",
 tests="""
```js
assert.equal(await contract.sum([5]), 5);
assert.equal(await contract.sum([1, 1, 1]), 3);
```
""",
 run="sh tools/sol-test.sh week5/dynamic-sum",
 remember=["`uint[]` = 동적 크기, `.length`로 길이."]),

esc(dir="week5/filter-even", title="Filter Even (Arrays 3단계)",
 problem="""
1. public 동적 배열 상태 변수 `evenNumbers`를 만든다.
2. external 함수 `filterEven(uint[])`: 짝수만 골라 `evenNumbers`에 push한다.
""",
 summary="`if (numbers[i] % 2 == 0) evenNumbers.push(numbers[i]);`",
 img="contract_diagram.png", img_alt="filterEven",
 intent="storage 배열에는 `push`(끝에 추가)와 `pop`(끝에서 제거)이 있다. Python 리스트의 `append`, `pop`과 같다.",
 files=[("contract.sol","**evenNumbers, filterEven**"),("tests.js","출제 · 채점 (테스트 2개)")],
 solution="""
```solidity
uint[] public evenNumbers;

function filterEven(uint[] calldata numbers) external {
    for (uint i = 0; i < numbers.length; i++) {
        if (numbers[i] % 2 == 0) {
            evenNumbers.push(numbers[i]);
        }
    }
}
```
""",
 tests="""
```js
await contract.filterEven([1, 2, 1, 4, 5]);
assert.sameMembers(await getArrayElements(contract.evenNumbers), [2, 4]);

// public 배열 getter는 인덱스 하나씩만 읽을 수 있어서, 범위를 벗어나 에러가 날 때까지 0, 1, 2… 를 읽는다
async function getArrayElements(getterFn) {
    let vals = [];
    try { for (i = 0; ; i++) vals.push(await getterFn(i)); } catch (ex) {}
    return vals.map(x => Number(x));
}
```
""",
 run="sh tools/sol-test.sh week5/filter-even",
 remember=["storage 배열: push / pop.","public 배열 getter는 인덱스 하나씩."]),

esc(dir="week5/filter-to-memory", title="Filter to Memory (Arrays 4단계)",
 problem="짝수만 골라 **memory**의 새 배열에 담아 돌려주는 pure, external 함수 `filterEven` 만들기.",
 summary="memory 배열엔 push가 없다 → **짝수 개수를 먼저 세고**, `new uint[](count)`로 만든 뒤 채운다.",
 img="contract_diagram.png", img_alt="filterEven",
 intent="""
> **memory 배열은 만들 때 크기를 정하고, 그 뒤로는 바꿀 수 없다.**

```solidity
address[] memory addresses = new address[](x);   // x 크기로 생성
```

그래서 "개수 세기 → 만들기 → 채우기" 두 번 도는 방식이 흔하다.
""",
 files=[("contract.sol","**filterEven (memory)**"),("tests.js","출제 · 채점 (테스트 1개)")],
 solution="""
```solidity
function filterEven(uint[] calldata numbers) external pure returns(uint[] memory) {
    uint count;
    for (uint i = 0; i < numbers.length; i++) {
        if (numbers[i] % 2 == 0) count++;
    }

    uint[] memory evens = new uint[](count);
    uint j;
    for (uint i = 0; i < numbers.length; i++) {
        if (numbers[i] % 2 == 0) {
            evens[j] = numbers[i];
            j++;
        }
    }
    return evens;
}
```

Python이라면 `[n for n in numbers if n % 2 == 0]` 한 줄이다.
""",
 tests="""
```js
const result = await contract.filterEven([1, 2, 1, 4, 1]);
assert.sameMembers(result.map(x => Number(x)), [2, 4]);
```
""",
 wrong=[("`new uint[](numbers.length)`로 크게 만들기","남는 칸이 0으로 채워져 [2, 4, 0, 0, 0] → 실패"),("memory 배열에 `.push`","컴파일 에러: memory 배열엔 push가 없다")],
 run="sh tools/sol-test.sh week5/filter-to-memory",
 remember=["memory 배열 = 크기 고정, `new T[](n)`.","개수 세기 → 만들기 → 채우기."]),

esc(dir="week5/stack-club-add", title="Stack Club (Arrays 5단계)",
 problem="""
1. 주소 동적 배열 `members`를 만든다.
2. external `addMember(address)`: 새 회원을 추가한다.
3. public view `isMember(address)`: 회원인지 bool로 돌려준다.
""",
 summary="`members.push(member)` + 배열을 처음부터 훑는 `isMember`.",
 img="StackClub_diagram.png", img_alt="StackClub",
 intent="회원을 위에 쌓고(push) 맨 위부터 꺼내는(pop) **스택**(LIFO, 후입선출) 구조의 클럽.\n\n(같은 일을 mapping으로 하면 조회가 더 싸다 — members-mapping 과제와 비교)",
 files=[("StackClub.sol","**이번에 완성할 컨트랙트**"),("tests.js","출제 · 채점 (테스트 2개)")],
 solution="""
```solidity
address[] members;

function addMember(address member) external {
    members.push(member);
}

function isMember(address member) public view returns(bool) {
    for (uint i = 0; i < members.length; i++) {
        if (members[i] == member) return true;
    }
    return false;
}
```
""",
 tests="""
```js
for (let i = 0; i < 3; i++) await contract.addMember(accounts[i]);
assert(await contract.isMember(accounts[i]));        // 0~2: true
assert(!(await contract.isMember(accounts[i])));     // 3~5: false
```
""",
 run="sh tools/sol-test.sh week5/stack-club-add",
 remember=["배열 검색 = 처음부터 끝까지 비교 (회원이 많을수록 가스↑)."]),

esc(dir="week5/stack-club-pop", title="Pop (Arrays 6단계)",
 problem="""
1. constructor에서 배포자를 첫 회원으로 추가한다.
2. `removeLastMember`: 가장 최근에 추가된 회원을 제거한다.
3. 🔒 `addMember`와 `removeLastMember`는 기존 회원만 부를 수 있다.
""",
 summary="`members.pop()` + 공통 권한 검사는 `onlyMember` modifier로.",
 img="StackClub_diagram.png", img_alt="StackClub pop",
 intent="`pop`은 storage 배열의 마지막 원소를 지우고 길이를 1 줄인다. 4주차에서 배운 modifier로 두 함수의 권한 검사를 한곳에 모은다.",
 files=[("StackClub.sol","stack-club-add + **constructor, pop, onlyMember**"),("tests.js","출제 · 채점 (테스트 6개)")],
 solution="""
```solidity
constructor() {
    members.push(msg.sender);
}

modifier onlyMember {
    require(isMember(msg.sender), "Only members can do this");
    _;
}

function addMember(address member) external onlyMember {
    members.push(member);
}

function removeLastMember() external onlyMember {
    members.pop();
}
```
""",
 tests="""
```js
accounts = (await ethers.provider.listAccounts()).slice(1);   // 배포자(계정0)를 뺀 나머지
await assertRevert(contract.connect(accounts[0]).addMember(accounts[0]), "...");   // 비회원 → 실패
for (…) await contract.connect(owner).addMember(accounts[i]);  // [owner, a0, a1, a2]
await contract.connect(signer_a1).removeLastMember();          // a2 제거
assert(!(await contract.isMember(accounts[2])));
```

- `contract.connect(주소 문자열)`도 ethers v5에서는 그 주소를 쓰는 읽기 전용 provider처럼 동작해서, 거래를 보내면 실패한다 → 비회원 테스트가 의도대로 revert.
""",
 run="sh tools/sol-test.sh week5/stack-club-pop", env=ENV_CUT,
 remember=["`pop()` = 마지막 원소 제거.","여러 함수의 같은 검사 → modifier."]),

esc(dir="week5/vote-storage", title="Vote Storage (Structs 1단계)",
 problem="""
1. `Choices choice`와 `address voter`를 가진 구조체 `Vote`를 만든다.
2. public 상태 변수 `vote` (Vote 타입).
3. `createVote(choice)`에서 `Vote(choice, msg.sender)`를 만들어 `vote`에 저장.
""",
 summary="`struct Vote { Choices choice; address voter; }` + `vote = Vote(choice, msg.sender);`",
 img="contract_diagram.png", img_alt="Vote",
 intent="""
> **struct = 여러 변수를 묶은 사용자 정의 타입 (Python의 dataclass, JS 객체와 비슷).**

```
[struct 저장] → struct 반환 → struct 배열 → 투표 찾기 → 한 번만 → 투표 바꾸기
 ★ 이 단계     vote-memory  vote-array  choice-lookup  vote-once  change-vote
```

- 만들 때 필드 **순서대로** 값을 넣거나, `Vote({ choice: c, voter: v })`처럼 이름을 붙인다.
- `.`으로 필드에 접근: `vote.choice`.
""",
 files=[("contract.sol","**Vote, vote, createVote**"),("tests.js","출제 · 채점 (테스트 2개)")],
 solution="""
```solidity
enum Choices { Yes, No }

struct Vote {
    Choices choice;
    address voter;
}

Vote public vote;

function createVote(Choices choice) external {
    vote = Vote(choice, msg.sender);
}
```
""",
 tests="""
```js
await contract.connect(accounts[0].signer).createVote(CHOICES.YES);
const vote = await contract.vote();          // public struct getter → { choice, voter }
assert.equal(vote.choice, CHOICES.YES);
assert.equal(vote.voter, accounts[0].address);
```
""",
 run="sh tools/sol-test.sh week5/vote-storage",
 remember=["struct = 묶음 타입, `.`으로 필드 접근."]),

esc(dir="week5/vote-memory", title="Vote Memory (Structs 2단계)",
 problem="Choices 값을 받아 `Vote`를 **돌려주는** external view 함수 `createVote` 만들기 (choice와 msg.sender 사용, 저장은 안 함).",
 summary="`returns(Vote memory)` + `return Vote(choice, msg.sender);`",
 img="contract_diagram.png", img_alt="Vote 반환",
 intent="""
> **ABI encoder v2 덕분에 struct를 외부 함수의 인자·반환값으로 쓸 수 있다. ABI에서는 튜플(`tuple`)로 표현된다.**

- `pragma experimental ABIEncoderV2;`는 0.8부터 기본이라 없어도 되지만, 강의 코드에 있어서 그대로 뒀다.
""",
 files=[("contract.sol","**createVote (view, Vote 반환)**"),("tests.js","출제 · 채점 (테스트 2개)")],
 solution="""
```solidity
function createVote(Choices choice) external view returns(Vote memory) {
    return Vote(choice, msg.sender);
}
```

`msg.sender`를 읽으므로 pure가 아니라 view다.
""",
 tests="""
```js
vote = await contract.connect(accounts[0].signer).callStatic.createVote(CHOICES.YES);   // 읽기 호출의 msg.sender도 connect한 계정
assert.equal(vote.voter, accounts[0].address);
```
""",
 run="sh tools/sol-test.sh week5/vote-memory",
 remember=["struct 반환 = `returns(T memory)`."]),

esc(dir="week5/vote-array", title="Vote Array (Structs 3단계)",
 problem="public `Vote[] votes`를 만들고, `createVote`가 새 Vote를 push하게 하기.",
 summary="`votes.push(Vote(choice, msg.sender));`",
 img="contract_diagram.png", img_alt="Vote 배열",
 intent="struct도 배열에 담을 수 있다. 여러 사람의 투표를 차례로 쌓는다.",
 files=[("contract.sol","**votes, createVote (push)**"),("tests.js","출제 · 채점 (테스트 2개)")],
 solution="""
```solidity
Vote[] public votes;

function createVote(Choices choice) external {
    votes.push(Vote(choice, msg.sender));
}
```
""",
 tests="""
```js
const vote = await contract.votes(0);   // public 배열 getter = 인덱스로 하나씩
assert.equal(vote.choice, CHOICES.YES);
```
""",
 run="sh tools/sol-test.sh week5/vote-array",
 remember=["struct 배열 = `T[]`, push로 추가."]),

esc(dir="week5/choice-lookup", title="Choice Lookup (Structs 4단계)",
 problem="""
1. external view `hasVoted(address)`: 그 주소가 투표했는지 bool.
2. external view `findChoice(address)`: 그 주소의 선택(Choices).
""",
 summary="두 함수가 공통 **internal 도우미** `findVote`(찾았는지, 투표)를 함께 쓴다.",
 img="contract_diagram.png", img_alt="lookup",
 intent="""
- 같은 반복문을 두 번 쓰지 않으려고 internal 함수로 뺐다.
- 여러 값 반환 받기: `(bool found, ) = findVote(v);`처럼 **필요 없는 값은 비워 둔다** (Python의 `found, _ = find_vote(v)`).
""",
 files=[("contract.sol","vote-array + **findVote, hasVoted, findChoice**"),("tests.js","출제 · 채점 (테스트 5개)")],
 solution="""
```solidity
function findVote(address voter) internal view returns(bool found, Vote memory vote) {
    for (uint i = 0; i < votes.length; i++) {
        if (votes[i].voter == voter) {
            return (true, votes[i]);
        }
    }
    // 못 찾으면 이름 붙은 반환값의 기본값 (false, 빈 Vote)
}

function hasVoted(address voter) external view returns(bool) {
    (bool found, ) = findVote(voter);
    return found;
}

function findChoice(address voter) external view returns(Choices) {
    (, Vote memory vote) = findVote(voter);
    return vote.choice;
}
```
""",
 tests="""
```js
assert(await contract.hasVoted(accounts[0].address));
assert.equal(await contract.findChoice(accounts[0].address), CHOICES.YES);
assert(!(await contract.hasVoted(accounts[1].address)));   // 아직 투표 안 함
```
""",
 run="sh tools/sol-test.sh week5/choice-lookup",
 remember=["공통 로직은 internal 함수로.","튜플에서 필요 없는 값은 빈칸."]),

esc(dir="week5/vote-once", title="Vote Once (Structs 5단계)",
 problem="같은 주소는 `createVote`를 **한 번만** 부를 수 있게 하기. 다시 부르면 revert.",
 summary="`require(!hasVoted(msg.sender));` — 안에서 쓰려고 hasVoted를 `external` → `public`.",
 img="contract_diagram.png", img_alt="vote once",
 intent="external 함수는 컨트랙트 안에서 이름으로 부를 수 없다. 안팎에서 다 쓰려면 public.",
 files=[("contract.sol","choice-lookup + **중복 투표 차단**"),("tests.js","출제 · 채점 (테스트 4개)")],
 solution="""
```solidity
function createVote(Choices choice) external {
    require(!hasVoted(msg.sender), "Already voted");
    votes.push(Vote(choice, msg.sender));
}

function hasVoted(address voter) public view returns(bool) { ... }
```
""",
 tests="""
```js
await contract.connect(accounts[0].signer).createVote(CHOICES.NO);   // 두 번째 → 에러가 나야 통과
```
""",
 wrong=[("hasVoted를 external로 둔 채 안에서 호출","컴파일 에러: Undeclared identifier (external은 내부 호출 불가)")],
 run="sh tools/sol-test.sh week5/vote-once",
 remember=["내부에서도 쓰려면 public."]),

esc(dir="week5/change-vote", title="Change Vote (Structs 6단계)",
 problem="external `changeVote(Choices)`: msg.sender의 기존 투표의 선택을 바꾸기. 기존 투표가 없으면 revert.",
 summary="배열을 훑어 내 투표를 찾고 `votes[i].choice = choice;` (storage 원소를 직접 수정). 끝까지 못 찾으면 `revert`.",
 img="contract_diagram.png", img_alt="changeVote",
 intent="""
- `votes[i].choice = …`는 storage 배열 원소를 직접 고친다.
- `findVote`가 돌려주는 건 **memory 복사본**이라, 그걸 고쳐도 저장된 투표는 그대로다. 그래서 여기선 인덱스로 직접 접근했다.
""",
 files=[("contract.sol","vote-once + **changeVote**"),("tests.js","출제 · 채점 (테스트 9개)")],
 solution="""
```solidity
function changeVote(Choices choice) external {
    for (uint i = 0; i < votes.length; i++) {
        if (votes[i].voter == msg.sender) {
            votes[i].choice = choice;
            return;
        }
    }
    revert("No existing vote");
}
```
""",
 tests="""
```js
await contract.changeVote(CHOICES.NO, { from: a1 });   // 강의 테스트 원본 그대로
...
await contract.connect(accounts[0].signer).changeVote(CHOICES.NO);
assert.equal(await contract.findChoice(accounts[0].address), CHOICES.NO);
```

- 첫 테스트의 `a1`은 어디에도 선언되지 않은 변수라서, 이 줄은 컨트랙트까지 가기 전에 JS `ReferenceError`로 실패한다. 그래서 "에러가 났다"는 조건은 항상 참이 된다 (강의 테스트의 실수). 실제로 revert되는지는 다른 단계 테스트들과 코드로 확인했다.
""",
 wrong=[("`(, Vote memory v) = findVote(msg.sender); v.choice = choice;`","memory 복사본만 바뀌어 저장된 투표는 그대로 → 변경 테스트 실패")],
 run="sh tools/sol-test.sh week5/change-vote",
 remember=["storage 원소를 고치려면 `arr[i].field = …` 또는 `storage` 참조.","찾지 못하면 `revert(\"…\")`."]),
]
