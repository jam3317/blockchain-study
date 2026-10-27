ENV = """강의 사이트는 브라우저 안에서 Hardhat으로 컴파일·테스트한다. 로컬에서는 루트에 설치한 Hardhat(ethers v5)과 `hardhat.config.js`로 똑같이 돌린다. `sh tools/sol-test.sh <폴더>`가 그 폴더의 `.sol`만 컴파일하고 테스트를 실행한다."""

ENV_REVERT = ENV + """

강의 테스트의 `await expect(...).to.be.reverted`는 Hardhat 전용 chai 플러그인이 필요하다. 로컬에는 그 플러그인이 없어서 **같은 검사를 try/catch로 바꿨다** (거래가 실패해야 통과). 화면에서 잘려 보이지 않은 assert 메시지 끝부분은 짐작으로 채웠다 (채점 결과와 무관)."""

ENV_CUT = ENV + """

화면에서 잘려 보이지 않은 assert 메시지 끝부분은 짐작으로 채웠다 (채점 결과와 무관)."""

MAP_FLOW = "[{0}]"

STAGES = [
dict(dir="week5/members-mapping", title="Members Mapping (Mappings 1단계)",
 problem="""
1. 주소를 bool로 대응시키는 public mapping `members`를 만든다 (멤버인지 여부).
2. 주소를 받아 멤버로 등록하는 external 함수 `addMember`를 만든다.
""",
 summary="`mapping(address => bool) public members;` + `members[member] = true;` — mapping은 Solidity의 딕셔너리(해시 테이블)다.",
 img="contract_diagram.png", img_alt="members",
 diagram_table=[("addMember × 2","계정 0, 1의 칸에 true를 적음"),("채점","계정 0, 1은 true, 계정 2는 아무것도 안 적어서 기본값 false")],
 intent="""
> **mapping = 키로 값을 바로 찾는 표 (O(1)). 주소별 기록을 남길 때 가장 많이 쓰는 자료구조다.**

```
[members 만들기] → 멤버 확인 → 멤버 삭제 → 구조체 저장 → 잔액 송금 → 중첩 mapping
 ★ 이 단계        is-member   remove-member  mapping-structs  transfer-amount  nested-mappings
```

- ERC-20 토큰의 잔액도 `mapping(address => uint) public balanceOf;`로 관리한다 (DAI, USDC 등).
- Python의 `dict`와 다른 점: **모든 키가 이미 존재**하고 기본값(0, false…)을 가진다. 그래서 "키가 있나?"를 따로 물을 수 없고, 키 목록을 돌 수도 없다.
- 키는 값 타입(주소, 숫자, bool, bytes…)만 된다. 값은 struct, 배열, 다른 mapping도 된다.
""",
 files=[("contract.sol","**이번에 완성할 컨트랙트**"),("tests.js","출제 · 채점 (테스트 2개)")],
 solution="""
```solidity
contract Contract {
    mapping(address => bool) public members;

    function addMember(address member) external {
        members[member] = true;
    }
}
```

```python
members = defaultdict(bool)
def add_member(member):
    members[member] = True
```
""",
 tests="""
```js
const accounts = await ethers.provider.listAccounts();
members = accounts.slice(0, 2);      // 계정 0, 1
nonMember = accounts[2];             // 계정 2
await contract.addMember(members[i]);
assert(await contract.callStatic.members(members[i]));       // public mapping은 키를 인자로 받는 getter가 생김
assert(!(await contract.callStatic.members(nonMember)));
```
""",
 wrong=[("`public`을 빼먹음","`members()` getter가 없어서 테스트에서 `is not a function`")],
 run="sh tools/sol-test.sh week5/members-mapping", env=ENV,
 remember=["mapping = 딕셔너리, 모든 키의 기본값이 이미 있음.","public mapping → 키를 받는 getter 자동 생성."]),

dict(dir="week5/is-member", title="Is Member (Mappings 2단계)",
 problem="주소를 받아 멤버인지 `bool`로 돌려주는 external **view** 함수 `isMember` 만들기.",
 summary="`return members[member];` — mapping은 반복문 없이 한 번에 찾는다.",
 img="contract_diagram.png", img_alt="isMember",
 intent="""
> **같은 일을 배열로 하면 처음부터 끝까지 돌며 찾아야 한다. 자료구조를 잘 고르면 코드도 짧고 가스도 덜 든다.**

```solidity
// mapping: 바로 찾음
return students[addr];

// 배열: 하나씩 비교
for (uint i = 0; i < students.length; i++) {
    if (students[i] == addr) return true;
}
return false;
```

mapping 값의 저장 위치는 `keccak256(키 . mapping의 슬롯 번호)`로 계산된다. 그래서 키만 알면 위치가 바로 나온다.
""",
 files=[("contract.sol","members-mapping + **isMember**"),("tests.js","출제 · 채점 (테스트 2개)")],
 solution="""
```solidity
function isMember(address member) external view returns(bool) {
    return members[member];
}
```
""",
 tests="""
```js
assert(await contract.callStatic.isMember(members[i]));
assert(!(await contract.callStatic.isMember(nonMember)));
```
""",
 run="sh tools/sol-test.sh week5/is-member", env=ENV,
 remember=["mapping 조회 = O(1).","읽기만 하면 `view`."]),

dict(dir="week5/remove-member", title="Remove Member (Mappings 3단계)",
 problem="주소를 받아 `members`의 그 칸을 `false`로 바꾸는 external 함수 `removeMember` 만들기.",
 summary="`members[member] = false;` — mapping은 삭제도 칸 하나만 바꾸면 끝.",
 img="contract_diagram.png", img_alt="removeMember",
 intent="""
> **배열에서 중간 원소를 빼면 뒤를 전부 당겨야 해서(저장소 쓰기가 많아서) 비싸다. mapping은 그럴 필요가 없다.**

- `delete members[member];`도 같은 결과다 (기본값으로 되돌림).
""",
 files=[("contract.sol","is-member + **removeMember**"),("tests.js","출제 · 채점 (테스트 4개)")],
 solution="""
```solidity
function removeMember(address member) external {
    members[member] = false;
}
```
""",
 tests="""
```js
await contract.removeMember(members[0]);
assert(!(await contract.callStatic.isMember(members[0])));   // 지운 사람은 false
assert(await contract.callStatic.isMember(members[1]));      // 다른 사람은 그대로
```
""",
 run="sh tools/sol-test.sh week5/remove-member", env=ENV,
 remember=["mapping 삭제 = 기본값으로 되돌리기 (`= false` 또는 `delete`)."]),

dict(dir="week5/mapping-structs", title="Mapping to Struct (Mappings 4단계)",
 problem="""
새 토큰 만들기: 새 사용자는 100토큰을 받는다.

1. 주소를 `User` 구조체(`balance`, `isActive`)로 대응시키는 public mapping `users`를 만든다.
2. external 함수 `createUser`: `msg.sender`에게 잔액 100, `isActive = true`인 사용자를 만든다.
3. 🔒 이미 활성 사용자인 주소가 다시 부르면 revert.
""",
 summary="`require(!users[msg.sender].isActive); users[msg.sender] = User(100, true);`",
 img="contract_diagram.png", img_alt="users",
 diagram_table=[("처음 createUser","활성 사용자가 아니라서 통과 → User(100, true) 저장"),("두 번째 createUser","이미 활성 → require 실패 → revert"),("채점","잔액·활성 여부와 중복 생성 차단 확인")],
 intent="""
> **mapping의 값으로 구조체를 두면 주소마다 여러 정보를 묶어 저장할 수 있다.**

- `isActive` 같은 플래그를 두는 이유: mapping은 모든 키가 이미 있어서, 새로 만든 사용자인지 원래 없던 사용자인지 구분할 방법이 필요하다.
""",
 files=[("contract.sol","**users, createUser**"),("tests.js","출제 · 채점 (테스트 4개)")],
 solution="""
```solidity
struct User {
    uint balance;
    bool isActive;
}

mapping(address => User) public users;

function createUser() external {
    require(!users[msg.sender].isActive, "User already exists");
    users[msg.sender] = User(100, true);
}
```

- `User(100, true)`: 필드 순서대로 값을 넣어 구조체를 만든다. `User({ balance: 100, isActive: true })`처럼 이름을 붙여도 된다.
""",
 tests="""
```js
await contract.connect(a1).createUser();
const user = await contract.users(await a1.getAddress());   // 구조체 getter → { balance, isActive }
assert.equal(user.balance, 100);
assert(user.isActive, "...");
// 같은 주소로 다시 createUser → 에러가 나야 통과
```
""",
 wrong=[("require 없이 덮어쓰기","두 번 불러도 성공 → 중복 생성 테스트 실패 (잔액을 100으로 되돌리는 꼼수도 가능)")],
 run="sh tools/sol-test.sh week5/mapping-structs", env=ENV_CUT,
 remember=["mapping 값으로 struct를 저장할 수 있다.","\"존재하는지\"는 플래그(isActive)로 표시한다."]),

dict(dir="week5/transfer-amount", title="Types of Balances (Mappings 5단계)",
 problem="""
external 함수 `transfer(address recipient, uint amount)`: `msg.sender`의 잔액에서 `amount`를 빼서 받는 사람 잔액에 더하기.

🔒 두 주소 모두 활성 사용자여야 하고, 보내는 사람 잔액이 충분해야 한다. 아니면 revert.
""",
 summary="`User storage`로 두 사용자 구조체를 직접 가리킨 뒤 잔액을 옮긴다. 이더는 전혀 움직이지 않는다.",
 img="contract_diagram.png", img_alt="transfer",
 intent="""
> **잔액에는 두 종류가 있다. 이더 잔액은 이더리움 자체가 관리하고, 토큰 잔액은 컨트랙트가 자기 mapping으로 관리한다.**

이번 토큰은 컨트랙트 안의 숫자일 뿐이라 `.call{ value }`로 이더를 보낼 필요가 없다. 숫자만 바꾸면 된다.

| | 이더 | 토큰 |
|---|---|---|
| 누가 관리 | 이더리움 상태 | 컨트랙트의 mapping |
| 보내는 방법 | `addr.call{ value: x }("")` | `balances[a] -= x; balances[b] += x;` |
""",
 files=[("contract.sol","mapping-structs + **transfer**"),("tests.js","출제 · 채점 (테스트 7개)")],
 solution="""
```solidity
function transfer(address recipient, uint amount) external {
    User storage sender = users[msg.sender];
    User storage receiver = users[recipient];
    require(sender.isActive && receiver.isActive, "Both users must be active");
    require(sender.balance >= amount, "Not enough balance");

    sender.balance -= amount;
    receiver.balance += amount;
}
```

| 키워드 | 뜻 |
|--------|-----|
| `storage` | 저장소의 **원본을 가리키는** 참조. 고치면 바로 저장된다 (Python 객체 참조와 비슷) |
| `memory` | 함수 안에서만 쓰는 **복사본**. 고쳐도 저장소는 그대로 |
""",
 tests="""
```js
// 받는 사람이 아직 없음 → revert
await contract.connect(a1).transfer(await a2.getAddress(), 50);   // 에러가 나야 함
// a2 생성 후
await contract.connect(a1).transfer(await a2.getAddress(), 50);
assert.equal(user1.balance, 50);   assert.equal(user2.balance, 150);
// 150 보내기 (잔액 100) → revert
```
""",
 wrong=[("`User memory sender = users[msg.sender];`","복사본만 바뀌어 잔액이 그대로 → 송금 테스트 실패"),("잔액 확인 require 생략","0.8부터는 `100 - 150`이 underflow로 자동 revert되어 이 테스트는 통과하지만, 의도를 코드로 드러내는 게 좋다")],
 run="sh tools/sol-test.sh week5/transfer-amount", env=ENV_CUT,
 remember=["토큰 잔액 = 컨트랙트 장부의 숫자.","원본을 고치려면 `storage` 참조.","보내는 쪽 검사 → 상태 변경 순서."]),

dict(dir="week5/nested-mappings", title="Nested Mappings (Mappings 6단계)",
 problem="""
1. 주소 → (주소 → `ConnectionTypes` enum)으로 대응시키는 public 중첩 mapping `connections`를 만든다.
2. `connectWith(other, connectionType)`에서 `msg.sender` → `other` 방향의 관계를 저장한다.
""",
 summary="`connections[msg.sender][other] = connectionType;` — 칸을 두 번 골라 들어간다.",
 img="contract_diagram.png", img_alt="connections",
 intent="""
> **mapping 안에 mapping을 넣으면 "누가 누구에게"처럼 두 키로 찾는 표가 된다 (DAO 투표: 안건별·주소별 찬반 등).**

```solidity
mapping(uint => mapping(address => bool)) voteToAddressChoice;
voteToAddressChoice[212][msg.sender] = true;
```

Python으로는 `connections[me][other] = kind` (dict 안의 dict).
""",
 files=[("contract.sol","**connections, connectWith**"),("tests.js","출제 · 채점 (테스트 6개)")],
 solution="""
```solidity
enum ConnectionTypes { Unacquainted, Friend, Family }

mapping(address => mapping(address => ConnectionTypes)) public connections;

function connectWith(address other, ConnectionTypes connectionType) external {
    connections[msg.sender][other] = connectionType;
}
```
""",
 tests="""
```js
const getConnection = (x, y) => contract.connections(x, y).then(Number);   // 중첩 mapping getter는 키 2개
await contract.connect(s1).connectWith(a2, TYPES.Family);
assert.equal(await getConnection(a1, a2), TYPES.Family);         // 2
assert.equal(await getConnection(a2, a1), TYPES.Unacquainted);   // 0, 반대 방향은 그대로
```
""",
 wrong=[("`connections[other][msg.sender]`","방향이 뒤집혀 한쪽 연결 테스트 실패")],
 run="sh tools/sol-test.sh week5/nested-mappings", env=ENV,
 remember=["중첩 mapping = 키 두 개로 찾는 표.","방향이 있다: [a][b] ≠ [b][a]."]),

dict(dir="week5/event-deployed", title="Deployed (Events 1단계)",
 problem="""
1. 주소 하나를 받는 이벤트 `Deployed`를 만든다.
2. constructor에서 배포자 주소로 `Deployed`를 emit한다.
""",
 summary="`event Deployed(address owner);` 선언 + `emit Deployed(msg.sender);`",
 img="collectible_diagram.png", img_alt="Deployed",
 intent="""
> **이벤트는 거래 영수증에 남는 로그다. 컨트랙트는 못 읽지만, 밖(프론트엔드·인덱서)에서 싸게 기록을 읽을 수 있다.**

```
[Deployed] → Transfer → ForSale → Purchase → indexed
 ★ 이 단계   event-transfer  event-for-sale  event-purchase  event-indexed
```

- 이벤트 이름은 UpperCamelCase, 함수 이름은 lowerCamelCase가 관례.
- 저장소(상태 변수)보다 훨씬 싸서, "무슨 일이 있었는지" 알리는 데 쓴다.
""",
 files=[("collectible.sol","**이번에 완성할 컨트랙트**"),("tests.js","출제 · 채점 (테스트 1개)")],
 solution="""
```solidity
contract Collectible {
    event Deployed(address owner);

    constructor() {
        emit Deployed(msg.sender);
    }
}
```
""",
 tests="""
```js
const receipt = await collectible.deployTransaction.wait();       // 배포 거래의 영수증
const topic = collectible.interface.getEventTopic('Deployed');    // keccak256("Deployed(address)")
const log = receipt.logs.find(x => x.topics.indexOf(topic) >= 0); // 그 이벤트의 로그 찾기
deployedEvent = collectible.interface.parseLog(log);              // ABI로 해석
assert.equal(deployedEvent.args[0], owner);
```

- 로그의 첫 topic은 이벤트 시그니처의 해시다 (함수 선택자와 비슷한 원리, 단 32바이트 전체).
""",
 run="sh tools/sol-test.sh week5/event-deployed", env=ENV,
 remember=["`event 이름(타입)` 선언 + `emit 이름(값)`.","이벤트 = 영수증의 로그, 밖에서 읽는다."]),

dict(dir="week5/event-transfer", title="Transfer (Events 2단계)",
 problem="""
1. 주소 두 개(원래 주인, 새 주인)를 받는 이벤트 `Transfer`를 만든다.
2. external 함수 `transfer(recipient)`: 소유권을 넘기고 `Transfer(원래 주인, 새 주인)`을 emit한다.
3. 현재 주인이 아니면 revert. (constructor에서 배포자를 주인으로 저장)
""",
 summary="owner를 상태 변수로 저장 → `require(msg.sender == owner)` → 바꾸고 → emit.",
 img="collectible_diagram.png", img_alt="Transfer",
 intent="""
- 이벤트 인자 이름은 생략해도 되지만, 적어 두면 ABI에 이름이 들어가서 `event.args.newOwner`처럼 읽을 수 있다.
- 새 주인을 저장하기 **전에** 원래 주인을 지역 변수에 담아 둬야 이벤트에 넣을 수 있다.
""",
 files=[("collectible.sol","event-deployed + **owner, Transfer, transfer**"),("tests.js","출제 · 채점 (테스트 2개)")],
 solution="""
```solidity
address owner;

event Deployed(address owner);
event Transfer(address originalOwner, address newOwner);

constructor() {
    owner = msg.sender;
    emit Deployed(msg.sender);
}

function transfer(address recipient) external {
    require(msg.sender == owner, "Only the owner can transfer");
    address originalOwner = owner;
    owner = recipient;
    emit Transfer(originalOwner, recipient);
}
```
""",
 tests="""
```js
response = await collectible.transfer(a2);
// Transfer 로그를 찾아 parseLog
assert.equal(deployedEvent.args[0], owner);
assert.equal(deployedEvent.args[1], a2);
// 원래 주인이 다시 transfer → 이제 주인이 아니라서 revert
```
""",
 wrong=[("`owner = recipient;` 다음에 `emit Transfer(owner, recipient)`","원래 주인 자리에 새 주인이 들어감 → 첫 번째 값 검사 실패")],
 run="sh tools/sol-test.sh week5/event-transfer", env=ENV_REVERT,
 remember=["바꾸기 전 값은 지역 변수에 보관.","권한 확인 → 상태 변경 → 이벤트."]),

dict(dir="week5/event-for-sale", title="Mark the Price (Events 3단계)",
 problem="""
1. uint 두 개(가격, 현재 블록 시간)를 받는 이벤트 `ForSale`을 만든다.
2. external 함수 `markPrice(uint price)`: `ForSale(price, block.timestamp)`를 emit한다.
3. 🔒 현재 주인이 아니면 revert.
""",
 summary="`emit ForSale(price, block.timestamp);` — `block.timestamp`는 지금 블록의 시간(초).",
 img="collectible_diagram.png", img_alt="ForSale",
 intent="""
- `block.timestamp`, `block.number`, `msg.sender`, `msg.value` 같은 **전역 변수**는 어디서든 쓸 수 있다.
- 블록 시간은 검증자가 어느 정도 조정할 수 있어서, 몇 초 단위의 정확도가 필요한 곳에는 쓰지 않는다.
""",
 files=[("collectible.sol","event-transfer + **ForSale, markPrice**"),("tests.js","출제 · 채점 (테스트 2개)")],
 solution="""
```solidity
event ForSale(uint price, uint timestamp);

function markPrice(uint price) external {
    require(msg.sender == owner, "Only the owner can mark the price");
    emit ForSale(price, block.timestamp);
}
```

(다음 단계 purchase를 위해 event-purchase에서는 가격을 상태 변수에도 저장한다.)
""",
 tests="""
```js
response = await collectible.markPrice(oneEther);
let block = await ethers.provider.getBlock(response.blockNumber);   // 그 거래가 들어간 블록
assert.equal(deployedEvent.args[1].toNumber(), block.timestamp);
```
""",
 run="sh tools/sol-test.sh week5/event-for-sale", env=ENV_REVERT,
 remember=["`block.timestamp` = 블록 시간(초)."]),

dict(dir="week5/event-purchase", title="Make a Purchase (Events 4단계)",
 problem="""
1. 이벤트 `Purchase(uint 금액, address 구매자)`를 만든다.
2. external **payable** 함수 `purchase`: 요청 가격으로 수집품을 산다.
   - `msg.value`를 판매자에게 보낸다.
   - 소유권을 구매자에게 넘긴다.
   - 판매 중이 아님으로 표시한다.
   - `Purchase`를 emit한다.
3. 🔒 금액이 가격과 다르거나, 판매 중이 아니면 revert.
""",
 summary="가격을 상태 변수로 저장해 두고(0 = 판매 안 함), 구매 시 **상태를 먼저 바꾼 뒤** 판매자에게 이더를 보낸다.",
 img="collectible_diagram.png", img_alt="purchase",
 intent="""
> **돈을 보내는 외부 호출은 맨 마지막에.** 상태를 바꾸기 전에 외부로 이더를 보내면, 받는 쪽 컨트랙트가 되돌아와 다시 purchase를 부르는 **재진입(reentrancy) 공격**에 취약해질 수 있다.

순서: **검사(Checks) → 상태 변경(Effects) → 외부 호출(Interactions)**. 이 패턴을 CEI라고 부른다.
""",
 files=[("collectible.sol","event-for-sale + **price, Purchase, purchase**"),("tests.js","출제 · 채점 (테스트 6개)")],
 solution="""
```solidity
uint price;   // 0이면 판매 중이 아님

function markPrice(uint _price) external {
    require(msg.sender == owner, "Only the owner can mark the price");
    price = _price;
    emit ForSale(_price, block.timestamp);
}

function purchase() external payable {
    require(price > 0, "Not for sale");                 // Checks
    require(msg.value == price, "Wrong amount");

    address seller = owner;                             // Effects
    owner = msg.sender;
    price = 0;

    (bool success, ) = seller.call{ value: msg.value }("");   // Interactions
    require(success, "Payment failed");

    emit Purchase(msg.value, msg.sender);
}
```
""",
 tests="""
```js
// 판매 전 구매 → revert / 0.5 ETH로 구매 → revert
response = await collectible.connect(signer_a2).purchase({ value: oneEther });
purchaseEvent = receipt.events.find(x => x.event === "Purchase");   // ethers가 해석해 둔 이벤트 목록
assert.equal(balanceAfter.sub(initialBalance).toString(), parseEther("1").toString());   // 판매자 +1 ETH
// 같은 가격으로 a3가 또 구매 → price가 0이라 revert
// a2(새 주인)가 다시 가격을 걸면 a3가 살 수 있음
```
""",
 wrong=[("`price = 0` 빼먹음","판매 후에도 계속 살 수 있음 → 재구매 차단 테스트 실패"),("`msg.value >= price`","더 비싸게는 살 수 있지만 문제 조건(같아야 함)과 다름")],
 run="sh tools/sol-test.sh week5/event-purchase", env=ENV_REVERT,
 remember=["Checks → Effects → Interactions.","가격 0 = 판매 안 함 표시."]),

dict(dir="week5/event-indexed", title="Indexed (Events 5단계)",
 problem="이벤트들의 **주소** 인자에 모두 `indexed`를 붙이기.",
 summary="`event Transfer(address indexed originalOwner, address indexed newOwner);`",
 img="collectible_diagram.png", img_alt="indexed",
 intent="""
> **indexed 인자는 로그의 topic으로 따로 저장되어, "이 주소가 관련된 Transfer만" 같은 필터 검색이 가능해진다.**

| | indexed | indexed 아님 |
|---|---|---|
| 저장 위치 | topics (최대 3개) | data |
| 값으로 검색 | ✔ | ✘ |

ethers에서: `contract.filters.Transfer(null, myAddress)` → 나에게 온 Transfer만.
""",
 files=[("collectible.sol","event-purchase에 **indexed 추가**"),("tests.js","출제 · 채점 (테스트 3개)")],
 solution="""
```solidity
event Deployed(address indexed owner);
event Transfer(address indexed originalOwner, address indexed newOwner);
event ForSale(uint price, uint timestamp);
event Purchase(uint amount, address indexed buyer);
```
""",
 tests="""
```js
artifacts = await hre.artifacts.readArtifact("Collectible");     // 컴파일 결과 (ABI 포함)
const transferEvent = artifacts.abi.find(x => x.name === "Transfer");
assert(transferEvent.inputs[0].indexed);                         // ABI에 indexed: true로 표시됨
```

- 이 테스트는 컨트랙트를 배포하지 않고 **ABI만** 확인한다.
""",
 run="sh tools/sol-test.sh week5/event-indexed", env=ENV_CUT,
 remember=["indexed = 검색 가능한 이벤트 인자 (최대 3개)."]),
]
