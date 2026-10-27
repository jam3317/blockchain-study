ENV = """강의 사이트는 브라우저 안에서 Hardhat으로 컴파일·테스트한다. 로컬에서는 루트의 Hardhat(ethers v5)으로 똑같이 돌린다: `sh tools/sol-test.sh <폴더>`."""

LIB_MAP = """```
is-even → using → console-log → divides-evenly → is-prime → prime-game
```"""
GOV_MAP = """```
proposals → cast-vote → change-vote → events → members → execute
```"""

STAGES = [
dict(dir="week7/library-is-even", title="UInt Library (Libraries 1단계)",
 problem="library `UIntFunctions`에 public pure 함수 `isEven(uint)`를 만든다. 짝수면 `true`.",
 summary="`return x % 2 == 0;` — 상태 변수 없이 입력만으로 답을 내는 함수.",
 img="UIntFunctions_diagram.png", img_alt="isEven",
 intent="""
> **library = 상태(저장 변수)가 없는 \"공용 함수 모음\". 여러 컨트랙트가 같은 코드를 나눠 쓰려고 만든다.**

""" + LIB_MAP + """

| | contract | library |
|---|----------|---------|
| 상태 변수 | O | **X** (컴파일 에러) |
| 이더 받기 · 상속 | O | X |
| 목적 | 앱 로직 | 코드 공유 (예: OpenZeppelin `Math`, `Strings`) |

Python으로 치면 `utils.py` 모듈에 함수만 모아 둔 것.
""",
 files=[("UIntFunctions.sol","**이번에 완성할 library**"),("tests.js","출제 · 채점 (테스트 2개)")],
 solution="""
```solidity
library UIntFunctions {
    function isEven(uint x) public pure returns (bool) {
        return x % 2 == 0;
    }
}
```

`pure`: 블록체인 상태를 읽지도 쓰지도 않는다. library 함수는 상태가 없으니 보통 `pure`나 `view`.
""",
 tests="""
```js
const Library = await ethers.getContractFactory("UIntFunctions");
library = await Library.deploy();            // public 함수가 있는 library는 따로 배포할 수 있다
await library.callStatic.isEven(2);          // true
await library.callStatic.isEven(3);          // false
```
""",
 run="sh tools/sol-test.sh week7/library-is-even", env=ENV,
 remember=["library에는 상태 변수가 없다.","`%`는 나머지 (Python과 같음)."]),

dict(dir="week7/library-using", title="Using Library (Libraries 2단계)",
 problem="""
`Game` 컨트랙트에 constructor를 만든다.

1. `uint` 참가자 수를 받아 `participants`에 저장한다.
2. 참가자 수가 짝수일 때만 `allowTeams = true`.
""",
 summary="`using UIntFunctions for uint;` 를 선언하고 `allowTeams = _participants.isEven();`",
 img="Game_diagram.png", img_alt="using for",
 intent="""
> **library 함수를 부르는 두 가지 방법.**

| 방법 | 코드 |
|------|------|
| 직접 호출 | `UIntFunctions.isEven(x)` |
| `using … for` | `using UIntFunctions for uint;` 선언 후 `x.isEven()` |

`using A for uint`는 uint 값에 A의 함수를 메서드처럼 붙여 준다. 이때 `x`가 첫 번째 인자로 들어간다.

**link(연결)**: library 함수가 `public`이면 library는 따로 배포되고, Game의 바이트코드에는 그 주소가 들어갈 빈칸이 생긴다. 그래서 테스트가 `libraries: { UIntFunctions: library.address }`로 주소를 채워 준다. `internal` 함수만 있으면 Game 안에 코드가 그대로 복사되어 link가 필요 없다.
""",
 files=[("Game.sol","**이번에 완성할 컨트랙트**"),("UIntFunctions.sol","1단계 library"),("tests.js","출제 · 채점 (테스트 12개)")],
 solution="""
```solidity
import "./UIntFunctions.sol";

contract Game {
    using UIntFunctions for uint;

    uint public participants;
    bool public allowTeams;

    constructor(uint _participants) {
        participants = _participants;
        allowTeams = _participants.isEven();
    }
}
```
""",
 tests="""
```js
const Contract = await ethers.getContractFactory("Game", {
    libraries: { UIntFunctions: library.address }   // 배포된 library 주소로 link
});
contract = await Contract.deploy(participants);     // 2, 4, 6 → allowTeams true / 3, 5, 7 → false
```
""",
 wrong=[("library 함수를 `public` → `internal`","Game에 코드가 복사되어 link할 library가 없어짐 → `You tried to link the contract Game with UIntFunctions, which is not one of its libraries.`로 배포 실패 (테스트 6개 실패)")],
 run="sh tools/sol-test.sh week7/library-using", env=ENV,
 remember=["`using L for 타입` → `값.함수()`.","public library 함수 = 따로 배포 + link."]),

dict(dir="week7/library-console-log", title="Console Log (Libraries 3단계)",
 problem="`getSecret(string)`에 전달되는 메시지를 `console.log`로 찍어 보고, 메시지가 시키는 숫자를 return한다.",
 summary="`console.log(_message);`로 메시지를 확인 → \"return 1337\" → `return 1337;`.",
 img="contract_diagram.png", img_alt="console.log",
 intent="""
> **Hardhat의 `console.sol`로 컨트랙트 안에서도 `console.log` 디버깅을 할 수 있다.**

- `import "hardhat/console.sol";`만 하면 `console.log(uint | string | bool | address)`를 쓸 수 있다.
- 값은 Hardhat 로컬 체인 실행 결과(테스트 출력)에 찍힌다. 실제 메인넷에서는 아무것도 출력되지 않는다.
- 이 단계의 메시지는 숨겨진 `secret.js`에서 오므로, 직접 찍어 보는 것 말고는 답을 알 방법이 없게 설계되어 있다.
""",
 files=[("contract.sol","**이번에 완성할 컨트랙트**"),("secret.js","로컬 실행용 비밀 메시지 (사이트에선 숨겨짐)"),("tests.js","출제 · 채점 (테스트 1개)")],
 solution="""
```solidity
import "hardhat/console.sol";

contract Contract {
    function getSecret(string memory _message) public returns(uint) {
        console.log(_message);   // "Hello there! You found the secret message. To pass this stage return 1337"
        return 1337;
    }
}
```
""",
 tests="""
```js
const { secretMessage, secretResponse } = require('./secret');   // 숨겨진 파일
const response = await contract.callStatic.getSecret(secretMessage);
assert(response.toNumber() === secretResponse);
```
""",
 run="sh tools/sol-test.sh week7/library-console-log", env=ENV,
 remember=["`import \"hardhat/console.sol\"` → `console.log`.","로그는 Hardhat 로컬 실행에서만 보인다."]),

dict(dir="week7/library-divides-evenly", title="Base Functions (Libraries 4단계)",
 problem="library `Prime`에 public pure `dividesEvenly(uint x, uint y)`: y가 x를 나누어떨어지게 하면 `true`.",
 summary="`return x % y == 0;`",
 img="Prime_diagram.png", img_alt="dividesEvenly",
 intent="""
> **작은 기본 함수를 먼저 만들고, 다음 단계에서 그걸 조립한다 (DRY: Don't Repeat Yourself).**

| 입력 | 결과 |
|------|------|
| (4, 2) (16, 4) (200, 50) | true |
| (5, 2) (22, 4) (199, 50) | false |
""",
 files=[("Prime.sol","**이번에 완성할 library**"),("test.js","출제 · 채점 (테스트 2개)")],
 solution="""
```solidity
library Prime {
    function dividesEvenly(uint x, uint y) public pure returns (bool) {
        return x % y == 0;
    }
}
```
""",
 tests="""
```js
const [x, y] = pairs[i];     // 배열 구조 분해 = Python의 x, y = pair
await library.callStatic.dividesEvenly(x, y);
```
""",
 run="sh tools/sol-test.sh week7/library-divides-evenly", env=ENV,
 remember=["나누어떨어짐 = 나머지 0.","y가 0이면 `%`에서 revert(0으로 나누기)된다."]),

dict(dir="week7/library-is-prime", title="Is Prime (Libraries 5단계)",
 problem="library `Prime`에 `isPrime(uint)`: 소수면 `true`.",
 summary="2 미만은 false. 2부터 `i * i <= x`까지 `dividesEvenly(x, i)`가 하나라도 true면 false, 아니면 true.",
 img="Prime_diagram.png", img_alt="isPrime",
 intent="""
> **같은 library 안의 함수는 이름만으로 바로 부를 수 있다.**

소수 판별은 √x까지만 나눠 보면 충분하다. 51 = 3 × 17이면 둘 중 작은 3이 반드시 √51(약 7.1) 이하에 있기 때문. Solidity에는 제곱근 함수가 없으니 `i * i <= x`로 같은 효과를 낸다.

```python
def is_prime(x):
    if x < 2: return False
    i = 2
    while i * i <= x:
        if x % i == 0: return False
        i += 1
    return True
```
""",
 files=[("Prime.sol","dividesEvenly + **isPrime**"),("test.js","출제 · 채점 (테스트 2개)")],
 solution="""
```solidity
function isPrime(uint x) public pure returns (bool) {
    if (x < 2) {
        return false;
    }
    for (uint i = 2; i * i <= x; i++) {
        if (dividesEvenly(x, i)) {
            return false;
        }
    }
    return true;
}
```

반복을 줄이는 게 중요한 이유: 컨트랙트에서 실행하면 반복 한 번마다 가스가 든다.
""",
 tests="""
```js
const primes = [5, 17, 47];       // → true
const nonPrimes = [4, 18, 51];    // → false
```
""",
 run="sh tools/sol-test.sh week7/library-is-prime", env=ENV,
 remember=["√x까지만 확인 → `i * i <= x`.","library 안에서는 다른 함수를 이름으로 바로 호출."]),

dict(dir="week7/library-prime-game", title="Prime Block Winner (Libraries 6단계)",
 problem="`PrimeGame` 컨트랙트에 `isWinner()`: 현재 블록 번호가 소수면 `true`.",
 summary="`return Prime.isPrime(block.number);`",
 img="PrimeGame_diagram.png", img_alt="isWinner",
 intent="""
> **전역 변수 `block`으로 현재 블록 정보를 읽을 수 있다.**

| 값 | 뜻 |
|----|----|
| `block.number` | 블록 번호 |
| `block.timestamp` | 블록 시각 (초) |
| `block.coinbase` | 블록을 만든 주소 |
| `block.gaslimit` | 블록 가스 한도 |

block 값은 채굴자/검증자가 어느 정도 고를 수 있어서 진짜 복권의 난수로 쓰면 안 된다. 이 문제는 연습용.
""",
 files=[("PrimeGame.sol","**이번에 완성할 컨트랙트**"),("Prime.sol","5단계 library"),("tests.js","출제 · 채점 (테스트 5개)")],
 solution="""
```solidity
import "./Prime.sol";

contract PrimeGame {
    function isWinner() public view returns (bool) {
        return Prime.isPrime(block.number);
    }
}
```

`block.number`를 읽으니 `pure`가 아니라 `view`.
""",
 tests="""
```js
const mineBlock = () => ethers.provider.send("evm_mine");   // 빈 블록 하나 만들기
// 블록 0, 1, 2는 배포에 쓰임 → mineBlock() 후 블록 3: 당첨
// 4: 꽝, 5: 당첨, 18: 꽝, 19: 당첨
const isWinner = await contract.callStatic.isWinner();
```
""",
 run="sh tools/sol-test.sh week7/library-prime-game", env=ENV,
 remember=["`block.number`, `block.timestamp`.","상태를 읽으면 `view`, 아무것도 안 읽으면 `pure`."]),

dict(dir="week7/gov-proposals", title="Proposals (Basic Governance 1단계)",
 problem="""
1. `Proposal` struct(target, data, yesCount, noCount)의 public 배열 `proposals`를 만든다.
2. external `newProposal(address, bytes)`: 새 Proposal을 찬반 0표로 만들어 배열에 넣는다.
""",
 summary="`proposals.push(Proposal(target, data, 0, 0));`",
 img="Voting_diagram.png", img_alt="newProposal",
 intent="""
> **온체인 거버넌스: 구성원이 \"이 주소에 이 함수 호출을 실행하자\"를 제안하고 투표로 결정한다.**

""" + GOV_MAP + """

| 필드 | 뜻 |
|------|----|
| `target` | 실행할 컨트랙트 주소 |
| `data` | 보낼 calldata (예: `mint(250)`을 인코딩한 바이트) |
| `yesCount` / `noCount` | 찬반 수 |
""",
 files=[("Voting.sol","**이번에 완성할 컨트랙트** (struct는 주어짐)"),("tests.js","출제 · 채점 (테스트 4개)")],
 solution="""
```solidity
Proposal[] public proposals;

function newProposal(address target, bytes calldata data) external {
    proposals.push(Proposal(target, data, 0, 0));
}
```
""",
 tests="""
```js
const interface = new ethers.utils.Interface(["function mint(uint) external"]);
const data = interface.encodeFunctionData("mint", [250]);   // 0x + 함수 선택자 4바이트 + 인자
await voting.newProposal(ethers.constants.AddressZero, data);
proposal = await voting.proposals(0);   // { target, data, yesCount, noCount }
```
""",
 run="sh tools/sol-test.sh week7/gov-proposals", env=ENV,
 remember=["제안 = 실행할 주소 + calldata.","public 배열 getter는 인덱스로 하나씩 읽는다."]),

dict(dir="week7/gov-cast-vote", title="Cast a Vote (Basic Governance 2단계)",
 problem="external `castVote(uint proposalId, bool)`: true면 yesCount, false면 noCount를 1 올린다. (중복 투표는 아직 신경 쓰지 않음)",
 summary="`Proposal storage proposal = proposals[proposalId];` 후 `yesCount++` 또는 `noCount++`.",
 img="Voting_diagram.png", img_alt="castVote",
 intent="""
> **struct를 고칠 때는 `storage` 참조로 받아야 원본이 바뀐다.**

`Proposal memory p = proposals[id]`로 받으면 복사본을 고치는 것이라 저장되지 않는다. Python에는 없는 구분이라 주의.
""",
 files=[("Voting.sol","proposals + **castVote**"),("tests.js","출제 · 채점 (테스트 2개)")],
 solution="""
```solidity
function castVote(uint proposalId, bool support) external {
    Proposal storage proposal = proposals[proposalId];
    if (support) {
        proposal.yesCount++;
    } else {
        proposal.noCount++;
    }
}
```
""",
 tests="""
```js
await voting.connect(voter1).castVote(0, true);
await voting.connect(voter2).castVote(0, true);
await voting.connect(voter3).castVote(0, false);
// yesCount 2, noCount 1
```
""",
 wrong=[("매개변수 이름을 `supports`로","컴파일 에러 `Expected ',' but got reserved keyword 'supports'` — Solidity 예약어라 변수 이름으로 못 쓴다 (사이트에서 실제로 겪은 에러)")],
 run="sh tools/sol-test.sh week7/gov-cast-vote", env=ENV,
 remember=["struct 수정은 `storage` 참조로.","`supports`는 예약어."]),

dict(dir="week7/gov-change-vote", title="Multiple Votes (Basic Governance 3단계)",
 problem="같은 주소가 다시 투표하면 표를 **바꿀** 수 있게 한다. 이전 표는 빼고 새 표를 더한다.",
 summary="`enum VoteStates { Absent, Yes, No }` + `mapping(제안 → mapping(주소 → VoteStates))`로 이전 표를 기억.",
 img="Voting_diagram.png", img_alt="투표 변경",
 intent="""
> **\"누가 무엇에 투표했는지\"를 이중 mapping으로 기록한다.**

| voter1 행동 | 이전 상태 | yes / no |
|-------------|-----------|----------|
| false | Absent | 0 / 1 |
| true | No → 빼고 더함 | 1 / 0 |
| true | Yes → 빼고 더함 | 1 / 0 |

enum의 첫 값(`Absent`)이 기본값이라 \"아직 안 함\"을 자연스럽게 표현할 수 있다. bool 하나로는 \"안 함 / 찬성 / 반대\" 세 상태를 못 나타낸다.
""",
 files=[("Voting.sol","castVote 수정 + **VoteStates**"),("tests.js","출제 · 채점 (테스트 4개)")],
 solution="""
```solidity
enum VoteStates { Absent, Yes, No }
mapping(uint => mapping(address => VoteStates)) voteStates;

function castVote(uint proposalId, bool support) external {
    Proposal storage proposal = proposals[proposalId];
    VoteStates previous = voteStates[proposalId][msg.sender];

    if (previous == VoteStates.Yes) {
        proposal.yesCount--;
    } else if (previous == VoteStates.No) {
        proposal.noCount--;
    }

    if (support) {
        proposal.yesCount++;
    } else {
        proposal.noCount++;
    }
    voteStates[proposalId][msg.sender] = support ? VoteStates.Yes : VoteStates.No;
}
```
""",
 tests="""
```js
await contract.connect(voter1).castVote(0, false);
await contract.connect(voter1).castVote(0, true);
await contract.connect(voter1).castVote(0, true);
await contract.connect(voter2).castVote(0, false);
// yes 1, no 1 — 그리고 제안 1에서 voter1의 첫 투표는 따로 센다 (yes 1, no 0)
```
""",
 wrong=[("마지막 `voteStates[...] = ...` 줄 빼기","이전 표를 기억하지 못해 매번 새 표로 더해짐 → `expected 2 to equal 1`로 2개 실패")],
 run="sh tools/sol-test.sh week7/gov-change-vote", env=ENV,
 remember=["세 가지 상태는 enum으로.","제안별·주소별 기록 = 이중 mapping."]),

dict(dir="week7/gov-events", title="Events (Basic Governance 4단계)",
 problem="""
1. `ProposalCreated(uint)`를 만들고 새 제안을 만들 때 emit한다.
2. `VoteCast(uint, address)`를 만들고 투표할 때마다 emit한다.
""",
 summary="push 전에 `emit ProposalCreated(proposals.length);`, castVote 끝에 `emit VoteCast(proposalId, msg.sender);`.",
 img="Voting_diagram.png", img_alt="이벤트",
 intent="""
> **화면(UI)은 이벤트를 구독해서 새 제안과 투표를 실시간으로 보여 준다.**

새 제안의 id = 배열에 들어갈 자리 = **push 하기 전의** `proposals.length`. push한 뒤라면 `proposals.length - 1`.
""",
 files=[("Voting.sol","**이벤트 2개 추가**"),("tests.js","출제 · 채점 (테스트 5개)")],
 solution="""
```solidity
event ProposalCreated(uint proposalId);
event VoteCast(uint proposalId, address voter);

function newProposal(address target, bytes calldata data) external {
    emit ProposalCreated(proposals.length);
    proposals.push(Proposal(target, data, 0, 0));
}

// castVote 마지막 줄
emit VoteCast(proposalId, msg.sender);
```
""",
 tests="""
```js
const tx = await (await contract.newProposal(target, data1)).wait();
event1 = tx.events.find(x => x.event === "ProposalCreated");
const proposal = await contract.proposals(event1.args[0]);   // 이벤트의 id로 찾은 제안
assert.equal(proposal.data, data1);
```
""",
 run="sh tools/sol-test.sh week7/gov-events", env=ENV,
 remember=["새 id = push 전 length.","이벤트 인자로 UI가 데이터를 다시 조회한다."]),

dict(dir="week7/gov-members", title="Voting Members (Basic Governance 5단계)",
 problem="""
public constructor가 주소 배열을 받는다. 그 주소들과 **배포자**만 제안하고 투표할 수 있다. 다른 주소는 revert.
""",
 summary="`mapping(address => bool) members`에 배포자와 배열 주소를 true로 저장하고 `onlyMember` modifier로 막는다.",
 img="Voting_diagram.png", img_alt="onlyMember",
 intent="""
> **아무나 투표할 수 있으면 주소를 수백 개 만들어 표를 늘릴 수 있다 (Sybil 공격). 그래서 구성원 명단이 필요하다.**

실제 DAO는 명단 대신 **토큰 보유량**으로 표의 무게를 정한다 (다음 가이드의 ERC20 Governor).
""",
 files=[("Voting.sol","**constructor + onlyMember**"),("test.js","출제 · 채점 (테스트 5개)")],
 solution="""
```solidity
mapping(address => bool) members;

constructor(address[] memory _members) {
    members[msg.sender] = true;
    for (uint i = 0; i < _members.length; i++) {
        members[_members[i]] = true;
    }
}

modifier onlyMember {
    require(members[msg.sender], "Only members");
    _;
}

function newProposal(...) external onlyMember { ... }
function castVote(...) external onlyMember { ... }
```

배열 대신 mapping에 넣은 이유: 투표할 때마다 배열을 다 훑지 않고 바로 확인하려고.
""",
 tests="""
```js
contract = await Voting.deploy([await member1.getAddress(), await member2.getAddress()]);
await contract.connect(nonmember).newProposal(target, data);   // 에러가 나야 통과
await contract.connect(owner).castVote(0, false);               // 배포자도 구성원
```
""",
 run="sh tools/sol-test.sh week7/gov-members", env=ENV,
 remember=["배포자도 명단에 넣는다.","명단 확인은 mapping으로 O(1)."]),

dict(dir="week7/gov-execute", title="Execute (Basic Governance 6단계)",
 problem="찬성이 **10표**가 되면 제안을 실행한다: `target`에 `data`를 call로 보낸다. 이미 실행한 제안은 다시 실행하지 않는다.",
 summary="castVote 끝에서 `yesCount == 10 && !executed[id]`이면 `executed[id] = true` 후 `target.call(data)`.",
 img="Voting_diagram.png", img_alt="실행",
 intent="""
> **투표 결과가 사람 손을 거치지 않고 코드로 바로 실행된다. 이게 온체인 거버넌스의 핵심.**

- `target.call(data)`: data 안의 함수 선택자와 인자대로 target 컨트랙트 함수를 부른다. 이번엔 `Minter.mint(250)`.
- `executed`를 call **전에** true로 바꾼다 (Checks-Effects-Interactions). call 도중 다시 들어와도 두 번 실행되지 않게.
- struct에 필드를 추가하지 않고 별도 mapping을 쓴 이유: struct를 바꾸면 `Proposal(target, data, 0, 0)` 생성 코드와 getter 모양도 같이 바뀌기 때문.
""",
 files=[("Voting.sol","**실행 로직 추가**"),("Minter.sol","로컬 실행용 target (사이트에선 숨겨짐)"),("test.js","출제 · 채점 (테스트 2개)")],
 solution="""
```solidity
mapping(uint => bool) executed;

// castVote 마지막
if (proposal.yesCount == 10 && !executed[proposalId]) {
    executed[proposalId] = true;
    (bool success, ) = proposal.target.call(proposal.data);
    require(success, "Execution failed");
}
```
""",
 tests="""
```js
contract = await Voting.deploy(await Promise.all(signers.map(x => x.getAddress())));   // 20개 계정 모두 구성원
await contract.newProposal(minter.address, data);   // data = mint(250)
// 9명 찬성 → minted() 0
// 10번째 찬성 → minted() 250
```
""",
 run="sh tools/sol-test.sh week7/gov-execute", env=ENV,
 remember=["실행 = `target.call(data)`.","상태(executed)를 먼저 바꾸고 외부 호출."]),
]
