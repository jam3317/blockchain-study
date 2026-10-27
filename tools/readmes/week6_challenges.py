ENV = """강의 사이트는 브라우저 안에서 Hardhat으로 컴파일·테스트한다. 로컬에서는 루트의 Hardhat(ethers v5)으로 똑같이 돌린다: `sh tools/sol-test.sh <폴더>`."""
ENV_CUT = ENV + "\n\n화면에서 잘려 보이지 않은 assert 메시지 끝부분은 짐작으로 채웠다 (채점 결과와 무관)."

STAGES = [
dict(dir="week6/party-rsvp", title="Start a Party (Party Split 1단계)",
 problem="""
친구들과 비용을 나눠 내는 파티 컨트랙트.

1. **constructor**: 참가비(`uint256`)를 받아 저장한다.
2. **rsvp** (external, payable): 호출한 주소를 참가자로 기록한다.
3. 🔒 참가비와 **정확히 같은** 금액이 아니면 revert. 이미 참가한 주소가 다시 부르면 revert.
""",
 summary="참가자 목록은 **배열**(나중에 돌면서 환불), 중복 확인은 **mapping**(빠른 조회). 둘을 함께 쓴다.",
 img="Party_diagram.png", img_alt="rsvp",
 intent="""
> **Solidity Challenges: 지금까지 배운 것(payable, require, 배열, mapping)을 조합하는 문제들.**

```
[rsvp] → payBill
 ★ 이 단계  party-pay-bill
```

| 자료구조 | 용도 | 이유 |
|----------|------|------|
| `address[] members` | 참가자 목록 | 나중에 한 명씩 환불하려면 순회가 필요 |
| `mapping(address => bool) hasJoined` | 중복 확인 | 배열을 매번 훑지 않고 O(1)로 확인 |
""",
 files=[("Party.sol","**이번에 완성할 컨트랙트**"),("tests.js","출제 · 채점 (테스트 4개)")],
 solution="""
```solidity
uint256 public deposit;
address[] public members;
mapping(address => bool) public hasJoined;

constructor(uint256 _deposit) {
    deposit = _deposit;
}

function rsvp() external payable {
    require(msg.value == deposit, "Must pay exactly the deposit");
    require(!hasJoined[msg.sender], "Already RSVP'd");

    hasJoined[msg.sender] = true;
    members.push(msg.sender);
}
```
""",
 tests="""
```js
contract = await Party.deploy(parseEther("2"));
await contract.connect(a1).rsvp({ value: deposit });                  // 성공
await contract.connect(a1).rsvp({ value: parseEther("1") });          // 에러가 나야 함
await contract.connect(a1).rsvp({ value: parseEther("3") });          // 에러 (더 많아도 안 됨)
// 같은 계정 두 번 → 에러
```
""",
 wrong=[("`msg.value >= deposit`","3 ETH도 통과 → '더 많이 낸 경우' 테스트 실패")],
 run="sh tools/sol-test.sh week6/party-rsvp", env=ENV_CUT,
 remember=["순회가 필요하면 배열, 빠른 확인은 mapping.","금액은 정확히 `==`."]),

dict(dir="week6/party-pay-bill", title="Pay the Bill (Party Split 2단계)",
 problem="""
external 함수 `payBill(address venue, uint amount)`:

1. 모인 돈으로 가게(venue)에 `amount`를 보낸다 (돈은 충분하다고 가정).
2. 남은 돈을 참가자들에게 **똑같이** 나눠 돌려준다.
""",
 summary="`venue.call{ value: amount }` → `share = address(this).balance / members.length` → 참가자마다 `share` 송금.",
 img="Party_diagram.png", img_alt="payBill",
 intent="""
| 계산서 | 참가비 합계 (4명 × 2 ETH) | 남는 돈 | 1인당 환불 |
|--------|---------------------------|---------|-----------|
| 8 ETH | 8 | 0 | 0 |
| 4 ETH | 8 | 4 | 1 |
| 2 ETH | 8 | 6 | 1.5 |

- 실제 서비스라면 `payBill`을 아무나 부르지 못하게 막아야 한다 (이 문제는 조건에 없음).
- 참가자가 많으면 반복문 송금은 가스 한도를 넘을 수 있다. 실무에서는 각자 찾아가게 하는 **pull 방식**을 쓴다.
""",
 files=[("Party.sol","party-rsvp + **payBill**"),("tests.js","출제 · 채점 (테스트 6개)")],
 solution="""
```solidity
function payBill(address venue, uint amount) external {
    (bool paid, ) = venue.call{ value: amount }("");
    require(paid, "Failed to pay the venue");

    uint share = address(this).balance / members.length;
    for (uint i = 0; i < members.length; i++) {
        (bool sent, ) = members[i].call{ value: share }("");
        require(sent, "Failed to refund");
    }
}
```
""",
 tests="""
```js
const signers = await ethers.getSigners();
friends = signers.slice(1, 5);       // 계정 1~4가 참가
venue = signers[6];
await contract.payBill(venue.address, bill);   // 계정 0이 호출 → 친구들은 가스를 안 내서 잔액 비교가 정확함
const expected = previousBalances[i].add(parseEther("1")).toString();
```
""",
 run="sh tools/sol-test.sh week6/party-pay-bill", env=ENV,
 remember=["남은 돈 = `address(this).balance`.","반복 송금은 인원이 많으면 위험 → pull 방식."]),

dict(dir="week6/dead-mans-switch", title="Dead Man's Switch",
 problem="""
owner가 52주에 한 번은 `ping`해야 하는 컨트랙트. 52주 동안 활동이 없으면 recipient가 돈을 가져갈 수 있다.

1. public payable **constructor**: recipient 주소를 받는다.
2. external **withdraw**: 컨트랙트의 돈을 전부 recipient에게 보낸다.
3. external **ping**: 비활동 기간을 다시 시작한다.
4. 🔒 ping은 owner만. withdraw는 마지막 활동 후 52주가 지나야만.
""",
 summary="마지막 활동 시각 `lastAction = block.timestamp`를 기록하고, `block.timestamp - lastAction >= 52 weeks`로 확인.",
 img="Switch_diagram.png", img_alt="Switch",
 intent="""
> **블록체인에서 시간을 다루는 법: `block.timestamp`(초)와 시간 단위(`seconds`, `minutes`, `hours`, `days`, `weeks`).**

- "dead man's switch" = 사람이 움직이지 않게 되면 자동으로 작동하는 장치. 유산 상속 등에 쓸 수 있다.
- `years`는 윤년 때문에 없다. 그래서 52 weeks.
""",
 files=[("Switch.sol","**이번에 완성할 컨트랙트**"),("tests.js","출제 · 채점 (테스트 7개)")],
 solution="""
```solidity
address owner;
address recipient;
uint lastAction;

constructor(address _recipient) payable {
    owner = msg.sender;
    recipient = _recipient;
    lastAction = block.timestamp;
}

function ping() external {
    require(msg.sender == owner, "Only the owner can ping");
    lastAction = block.timestamp;
}

function withdraw() external {
    require(block.timestamp - lastAction >= 52 weeks, "Owner is still active");
    (bool sent, ) = recipient.call{ value: address(this).balance }("");
    require(sent, "Failed to send ether");
}
```
""",
 tests="""
```js
const passTime = (time) => ethers.provider.send('evm_increaseTime', [time]);   // 테스트 체인 시계를 앞당김
await passTime(oneWeek * 40);
// 40주 → withdraw 실패, 80주 → 성공, 중간에 ping하면 다시 52주 필요

async function assertBalanceChange(address, change, tx, msg) {
    const { gasUsed } = await (await tx()).wait();
    const gasInWei = ethers.utils.parseUnits(gasUsed.toString(), "gwei");   // gasPrice 1 gwei로 보냈으니 가스비 = gasUsed gwei
    assert.equal(change.toString(), balanceAfter.add(gasInWei).sub(balanceBefore).toString(), msg);
}
```
""",
 wrong=[("`> 52 weeks`","정확히 52주째엔 실패하지만, 이 테스트(70·80주)에선 통과한다"),("ping에 owner 확인 없음","recipient가 ping은 못 해도 다른 사람이 ping으로 계속 막을 수 있음 → 'other account' 테스트 실패")],
 run="sh tools/sol-test.sh week6/dead-mans-switch", env=ENV,
 remember=["`block.timestamp` + 시간 단위(`52 weeks`).","테스트에선 `evm_increaseTime`으로 시간을 건너뛴다."]),

dict(dir="week6/hackathon", title="Hackathon (Top Rated Project)",
 problem="external view 함수 `findWinner`: 평점 배열의 **평균**이 가장 높은 프로젝트(`Project`)를 돌려주기.",
 summary="바깥 반복문은 프로젝트, 안쪽 반복문은 평점 합계. 평균이 최고면 그 인덱스를 기억해 두었다가 반환.",
 img="Hackathon_diagram.png", img_alt="findWinner",
 intent="""
> **struct 안의 배열, 이중 반복문, 정수 나눗셈을 함께 다루는 문제.**

| 프로젝트 | 평점 | 평균 (정수 나눗셈) |
|----------|------|-------------------|
| First | 2, 2, 2, 2, 2, 2 | 2 |
| Second | 0, 4 | 2 |
| Winning | 2, 3, 4 | 3 ✔ |
""",
 files=[("Hackathon.sol","**findWinner 추가** (struct, newProject, rate는 주어짐)"),("tests.js","출제 · 채점 (테스트 3개)")],
 solution="""
```solidity
function findWinner() external view returns(Project memory) {
    uint bestIndex;
    uint bestAverage;
    for (uint i = 0; i < projects.length; i++) {
        uint[] storage ratings = projects[i].ratings;
        uint sum;
        for (uint j = 0; j < ratings.length; j++) {
            sum += ratings[j];
        }
        uint average = ratings.length == 0 ? 0 : sum / ratings.length;
        if (average > bestAverage) {
            bestAverage = average;
            bestIndex = i;
        }
    }
    return projects[bestIndex];
}
```

- `uint[] storage ratings = …`: 복사하지 않고 원본을 가리켜서 가스를 아낀다.
- 평점이 없는 프로젝트는 0으로 나누기 에러를 피하려고 평균 0.

```python
best = max(projects, key=lambda p: sum(p.ratings) // len(p.ratings) if p.ratings else 0)
```
""",
 tests="""
```js
await contract.newProject('Winning');
await contract.rate(1, 5);
const winner = await contract.findWinner.call();   // struct → { title, ratings }
assert.equal(winner.title, 'Winning');
```
""",
 wrong=[("평균 대신 합계로 비교","First(12)가 Winning(9)을 이김 → 마지막 테스트 실패")],
 run="sh tools/sol-test.sh week6/hackathon", env=ENV,
 remember=["0으로 나누기 주의.","큰 배열은 storage 참조로 읽기."]),
]
