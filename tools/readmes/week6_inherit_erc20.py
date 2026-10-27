ENV = """강의 사이트는 브라우저 안에서 Hardhat으로 컴파일·테스트한다. 로컬에서는 루트의 Hardhat(ethers v5)으로 똑같이 돌린다: `sh tools/sol-test.sh <폴더>`."""
ENV_HIDDEN = ENV + "\n\n사이트에는 테스트용 컨트랙트(`{name}`)가 숨겨져 있어서, 로컬 실행용으로 같은 역할을 하는 파일을 직접 만들어 두었다."

INHERIT_MAP = """```
heroes → constructor → override → super → ownable → multiple
```"""

STAGES = [
dict(dir="week6/inherit-heroes", title="Make SuperHeroes (Inheritance 1단계)",
 problem="""
`Hero` 컨트랙트(체력 100, `takeDamage`)가 주어진다.

1. `SuperHeroes.sol`에 `Mage`와 `Warrior` 컨트랙트를 만든다.
2. 둘 다 `Hero`를 **상속**해서 체력과 `takeDamage`를 그대로 쓰게 한다.
""",
 summary="`contract Mage is Hero { }` — `is` 한 단어로 부모의 변수와 함수가 전부 따라온다.",
 img="SuperHeroes_diagram.png", img_alt="상속",
 intent="""
> **상속(inheritance): 공통 코드는 부모 컨트랙트에 한 번만 쓰고, 자식은 `is`로 물려받는다.**

""" + INHERIT_MAP + """

| Solidity | Python |
|----------|--------|
| `contract Warrior is Hero { }` | `class Warrior(Hero): pass` |
| 부모의 `health`, `takeDamage` 사용 | 부모의 속성·메서드 사용 |
""",
 files=[("Hero.sol","부모 컨트랙트 (주어짐)"),("SuperHeroes.sol","**이번에 완성할 파일**"),("tests.js","출제 · 채점 (테스트 4개)")],
 solution="""
```solidity
import "./Hero.sol";

contract Mage is Hero { }

contract Warrior is Hero { }
```

배포하면 `Warrior` 하나 안에 `Hero`의 코드가 합쳐져서 컴파일된다. 컨트랙트가 두 개 생기는 게 아니다.
""",
 tests="""
```js
const Warrior = await ethers.getContractFactory("Warrior");
warrior = await Warrior.deploy();
assert.equal((await warrior.health()).toNumber(), 100);   // 부모의 초기값
await warrior.takeDamage(10);                              // 부모의 함수
assert.equal((await warrior.health()).toNumber(), 90);
```
""",
 run="sh tools/sol-test.sh week6/inherit-heroes", env=ENV,
 remember=["`is 부모` = Python의 `class 자식(부모)`.","자식에 아무것도 안 써도 부모 기능을 전부 쓸 수 있다."]),

dict(dir="week6/inherit-constructor", title="Constructor Inheritance (Inheritance 2단계)",
 problem="""
`Hero`에 `constructor(uint _health)`가 생겼다.

1. `Warrior`는 체력 **200**으로 시작한다.
2. `Mage`는 체력 **50**으로 시작한다.
""",
 summary="`contract Warrior is Hero(200) { }` — 상속하는 자리에서 부모 constructor의 인자를 넘긴다.",
 img="SuperHeroes_diagram.png", img_alt="constructor 상속",
 intent="""
> **부모 constructor에 인자가 있으면, 자식이 반드시 값을 정해 줘야 한다.**

| 방법 | 코드 | 언제 |
|------|------|------|
| 상속 목록에서 | `contract Warrior is Hero(200) { }` | 값이 항상 같을 때 (이번 문제) |
| 자식 constructor에서 | `constructor() Hero(200) { }` | 자식 constructor 인자로 값을 계산할 때 |

```python
class Warrior(Hero):
    def __init__(self):
        super().__init__(200)
```
""",
 files=[("Hero.sol","부모 컨트랙트 (constructor 추가됨)"),("SuperHeroes.sol","**이번에 완성할 파일**"),("tests.js","출제 · 채점 (테스트 4개)")],
 solution="""
```solidity
contract Mage is Hero(50) { }

contract Warrior is Hero(200) { }
```
""",
 tests="""
```js
warrior = await Warrior.deploy();          // 배포할 때 인자를 주지 않는다
assert.equal(health.toNumber(), 200);      // 200은 컨트랙트 코드 안에서 정해짐
await warrior.takeDamage(10);  // → 190
// Mage: 50 → 40
```
""",
 wrong=[("`contract Warrior is Hero { }` (인자 없음)","컴파일 에러 `Contract \"Warrior\" should be marked as abstract.` — 부모 constructor 인자를 채우지 않으면 완성되지 않은(abstract) 컨트랙트로 본다")],
 run="sh tools/sol-test.sh week6/inherit-constructor", env=ENV,
 remember=["`is Hero(200)` = Python의 `super().__init__(200)`.","인자를 안 넘기면 abstract 취급 → 배포 불가."]),

dict(dir="week6/inherit-override", title="Virtual Override (Inheritance 3단계)",
 problem="""
`Hero`가 `abstract` 컨트랙트가 되었고, 몸체가 없는 `function attack(address enemy) public virtual;`이 생겼다.

1. `Warrior`와 `Mage`에 `attack`을 `override`로 구현한다.
2. 받은 주소를 `Enemy` 인터페이스로 감싸서 `takeAttack`을 부른다.
3. Warrior는 `Brawl`, Mage는 `Spell` 공격.
""",
 summary="`function attack(address _enemy) public override { Enemy(_enemy).takeAttack(Hero.AttackTypes.Brawl); }`",
 img="SuperHeroes_diagram.png", img_alt="override",
 intent="""
> **`virtual` = 자식이 다시 써도 됨. `override` = 지금 부모 함수를 다시 쓰는 중. 둘 다 적어야 한다.**

| 키워드 | 붙는 곳 | 의미 |
|--------|---------|------|
| `abstract contract` | 부모 | 몸체 없는 함수가 있어 혼자서는 배포 불가 |
| `virtual` | 부모 함수 | 자식이 바꿀 수 있음 |
| `override` | 자식 함수 | 부모 함수를 바꿈 |

Python은 그냥 같은 이름으로 다시 정의하면 끝이지만, Solidity는 실수를 막으려고 양쪽에 표시를 요구한다.

`Enemy(_enemy)`: 주소를 인터페이스 타입으로 바꾸면 그 주소의 컨트랙트 함수를 부를 수 있다. 실제 적 컨트랙트 코드는 몰라도 된다.
""",
 files=[("Hero.sol","abstract 부모 + `Enemy` 인터페이스 (주어짐)"),("SuperHeroes.sol","**이번에 완성할 파일**"),("EnemyContract.sol","로컬 실행용 적 컨트랙트 (사이트에선 숨겨짐)"),("tests.js","출제 · 채점 (테스트 2개)")],
 solution="""
```solidity
contract Mage is Hero(50) {
    function attack(address _enemy) public override {
        Enemy enemy = Enemy(_enemy);
        enemy.takeAttack(Hero.AttackTypes.Spell);
    }
}

contract Warrior is Hero(200) {
    function attack(address _enemy) public override {
        Enemy enemy = Enemy(_enemy);
        enemy.takeAttack(Hero.AttackTypes.Brawl);
    }
}
```

`AttackTypes`는 `Hero` 안에 정의된 enum이라 `Hero.AttackTypes.Brawl`로 쓴다 (상속받았으니 `AttackTypes.Brawl`도 된다).
""",
 tests="""
```js
const tx = await warrior.attack(enemy.address);
receipt = await tx.wait();
const topic = Enemy.interface.getEventTopic("Attacked");   // 적이 남긴 이벤트
const log = receipt.logs.find(x => x.topics[0] === topic);
assert.equal(Number(log.data), ATTACK_TYPES.BRAWL);        // Brawl = 0, Spell = 1
```
""",
 wrong=[("`override` 빼기","컴파일 에러 `Overriding function is missing \"override\" specifier.`"),("`public` → `external`","컴파일 에러 `Overriding function visibility differs.` — 부모와 visibility가 같아야 한다")],
 run="sh tools/sol-test.sh week6/inherit-override", env=ENV_HIDDEN.format(name="EnemyContract"),
 remember=["부모 `virtual`, 자식 `override` — 둘 다 필요.","`인터페이스(주소)`로 다른 컨트랙트 함수 호출."]),

dict(dir="week6/inherit-super", title="Super Call (Inheritance 4단계)",
 problem="""
이제 `Hero.attack`에 몸체가 생겼다: `energy--` (처음 energy는 10).

Warrior와 Mage의 `attack`에서 부모의 `attack`도 함께 실행되게 한다.
""",
 summary="자식 `attack` 끝에 `super.attack(_enemy);` 한 줄.",
 img="SuperHeroes_diagram.png", img_alt="super",
 intent="""
> **override하면 부모 함수는 자동으로 실행되지 않는다. 부모 동작도 원하면 `super`로 직접 불러야 한다.**

```python
class Warrior(Hero):
    def attack(self, enemy):
        enemy.take_attack(BRAWL)
        super().attack(enemy)
```

`super.attack(...)` 대신 `Hero.attack(...)`도 된다. 다중 상속에서는 `super`가 상속 순서를 따라 다음 부모를 찾아간다.
""",
 files=[("Hero.sol","부모 (`attack`이 energy를 줄임)"),("SuperHeroes.sol","**이번에 완성할 파일**"),("EnemyContract.sol","로컬 실행용 적 컨트랙트"),("tests.js","출제 · 채점 (테스트 4개)")],
 solution="""
```solidity
contract Warrior is Hero(200) {
    function attack(address _enemy) public override {
        Enemy enemy = Enemy(_enemy);
        enemy.takeAttack(Hero.AttackTypes.Brawl);
        super.attack(_enemy);
    }
}
// Mage도 같은 모양, Spell
```
""",
 tests="""
```js
it('should use some energy', async () => {
    const energy = await warrior.energy();
    assert.equal(energy, 9);     // 10 → 9 (BigNumber와 9를 ==로 비교해서 통과)
});
```
""",
 wrong=[("`super.attack(_enemy);` 빼기","공격 이벤트 테스트는 통과하지만 `expected BigNumber { value: \"10\" } to equal 9` → energy 테스트 2개 실패")],
 run="sh tools/sol-test.sh week6/inherit-super", env=ENV_HIDDEN.format(name="EnemyContract"),
 remember=["override하면 부모 함수는 실행되지 않는다.","`super.함수()` = Python의 `super().함수()`."]),

dict(dir="week6/inherit-ownable", title="Only Owner (Inheritance 5단계)",
 problem="""
`Collectible is Ownable`이고, `markPrice`에 `onlyOwner`가 붙어 있다. 그런데 `Ownable`이 비어 있다.

1. `Ownable`에 owner(배포자)를 저장한다.
2. `onlyOwner` modifier를 만들어 owner만 `markPrice`를 부를 수 있게 한다.
""",
 summary="`Ownable`에 `owner = msg.sender` constructor와 `modifier onlyOwner { require(msg.sender == owner); _; }`.",
 img="Ownable_diagram.png", img_alt="Ownable",
 intent="""
> **권한 확인 같은 공통 기능은 부모 컨트랙트(유틸리티)로 빼 두고 여러 컨트랙트가 물려받는다.**

- 실무에서는 OpenZeppelin의 `Ownable`을 그대로 import해서 쓴다. 이번 문제는 그걸 직접 만들어 보는 것.
- 부모 constructor는 자식을 배포할 때 자동으로 실행된다. 그래서 `owner`는 Collectible을 배포한 사람이 된다.
""",
 files=[("BaseContracts.sol","**이번에 완성할 파일** (Ownable)"),("Collectible.sol","Ownable을 쓰는 쪽 (주어짐)"),("tests.js","출제 · 채점 (테스트 2개)")],
 solution="""
```solidity
contract Ownable {
    address owner;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner {
        require(msg.sender == owner, "Only the owner can call this");
        _;
    }
}
```
""",
 tests="""
```js
await contract.markPrice(5);                                       // 계정 0 = 배포자 → 성공
await contract.connect(ethers.provider.getSigner(1)).markPrice(5); // 계정 1 → 에러가 나야 통과
```
""",
 run="sh tools/sol-test.sh week6/inherit-ownable", env=ENV,
 remember=["modifier도 상속된다.","부모 constructor는 자식 배포 때 자동 실행."]),

dict(dir="week6/inherit-multiple", title="Multiple Inheritance (Inheritance 6단계)",
 problem="""
`Collectible is Ownable, Transferable`로 바뀌었다. `Transferable`은 아직 없다.

1. `Transferable` 컨트랙트에 `transfer(address newOwner)`를 만든다.
2. 현재 owner만 호출할 수 있고, 호출하면 owner가 newOwner로 바뀐다.
""",
 summary="`contract Transferable is Ownable { function transfer(address newOwner) external onlyOwner { owner = newOwner; } }`",
 img="BaseContracts_diagram.png", img_alt="다중 상속",
 intent="""
> **여러 부모를 쉼표로 나열해서 상속할 수 있다. 순서는 \"가장 기본 → 가장 파생\".**

```
Ownable  ←  Transferable
   ↖           ↖
      Collectible  (is Ownable, Transferable)
```

- `Transferable`이 `owner`와 `onlyOwner`를 쓰려면 자신도 `Ownable`을 상속해야 한다.
- 그래도 `owner` 변수는 하나뿐이다. Solidity가 상속 그래프를 한 줄로 펴서(linearization) 같은 부모를 한 번만 넣는다. Python의 MRO와 같은 개념.
""",
 files=[("BaseContracts.sol","**Transferable 추가**"),("Collectible.sol","is Ownable, Transferable (주어짐)"),("tests.js","출제 · 채점 (테스트 4개)")],
 solution="""
```solidity
contract Transferable is Ownable {
    function transfer(address newOwner) external onlyOwner {
        owner = newOwner;
    }
}
```
""",
 tests="""
```js
await contract.connect(s2).transfer(a2);       // owner가 아님 → 에러
await contract.transfer(a2);                   // owner가 a2에게 넘김
await contract.connect(s2).markPrice(10);      // 이제 a2가 owner → 성공
```
""",
 wrong=[("`is Transferable, Ownable` (순서 반대)","컴파일 에러 `Linearization of inheritance graph impossible` — 더 기본인 Ownable이 앞에 와야 한다")],
 run="sh tools/sol-test.sh week6/inherit-multiple", env=ENV,
 remember=["다중 상속은 기본 → 파생 순서로.","같은 부모는 한 번만 들어간다 (linearization)."]),

dict(dir="week6/erc20-supply", title="Token Supply (Build an ERC-20 1단계)",
 problem="public `uint` 상태 변수 `totalSupply`를 만든다. 값은 기본값 0 그대로 둔다.",
 summary="`uint public totalSupply;` — public 변수는 같은 이름의 읽기 함수 `totalSupply()`가 자동으로 생긴다.",
 img="Token_diagram.png", img_alt="totalSupply",
 intent="""
> **ERC-20 토큰을 처음부터 직접 만든다. 첫 단계는 전체 발행량.**

```
[supply] → config → balances → mint → transfer → events
```

ERC-20 표준은 `totalSupply()`라는 **함수**를 요구한다. public 변수를 만들면 Solidity가 그 함수를 대신 만들어 주므로 이것만으로 표준을 맞춘다.
""",
 files=[("Token.sol","**이번에 완성할 컨트랙트**"),("tests.js","출제 · 채점 (테스트 1개)")],
 solution="""
```solidity
contract Token {
    uint public totalSupply;
}
```
""",
 tests="""
```js
const result = await token.callStatic.totalSupply();
assert.equal(result.toString(), '0');   // BigNumber → 문자열로 비교
```
""",
 run="sh tools/sol-test.sh week6/erc20-supply", env=ENV,
 remember=["public 변수 = 자동 getter 함수.","uint 기본값은 0."]),

dict(dir="week6/erc20-config", title="Configuration (Build an ERC-20 2단계)",
 problem="""
public 상태 변수 세 개:

1. `string name` — 1글자 이상
2. `string symbol` — 3글자
3. `uint8 decimals` — 18
""",
 summary="`name = \"Study Token\"`, `symbol = \"STK\"`, `decimals = 18`.",
 img="Token_diagram.png", img_alt="name symbol decimals",
 intent="""
> **이름·기호·소수 자리는 ERC-20에서 \"선택\" 항목이지만 지갑과 거래소 화면에 보이려면 사실상 필수.**

`decimals = 18`의 뜻: 컨트랙트 안의 숫자 `1000000000000000000`(10^18)을 화면에서는 `1`개로 보여 준다. 이더의 wei ↔ ETH와 같은 관계.

```python
display = raw / 10**18
```
""",
 files=[("Token.sol","supply + **name, symbol, decimals**"),("tests.js","출제 · 채점 (테스트 4개)")],
 solution="""
```solidity
uint public totalSupply;
string public name = "Study Token";
string public symbol = "STK";
uint8 public decimals = 18;
```
""",
 tests="""
```js
assert.isAtLeast(name.length, 1);
assert.equal(sym.length, 3);
assert.equal(decimals, 18);     // uint8은 ethers에서 BigNumber가 아니라 그냥 숫자로 온다
```
""",
 run="sh tools/sol-test.sh week6/erc20-config", env=ENV,
 remember=["decimals 18 = 10^18이 1개.","name/symbol/decimals는 표준상 선택이지만 관례상 넣는다."]),

dict(dir="week6/erc20-balances", title="Balances (Build an ERC-20 3단계)",
 problem="""
1. 주소 → `uint256` mapping으로 잔액을 저장한다.
2. external view 함수 `balanceOf(address)`가 그 주소의 잔액을 돌려준다.
""",
 summary="`mapping(address => uint256) balances;` + `balanceOf`에서 `return balances[account];`.",
 img="Token_diagram.png", img_alt="balanceOf",
 intent="""
> **ERC-20의 핵심 자료구조는 결국 `dict[주소] = 잔액` 하나.**

```python
balances = defaultdict(int)
def balance_of(account): return balances[account]
```

`mapping`을 `public`으로 만들면 getter 이름이 `balances`가 되므로, 표준 이름 `balanceOf`는 함수로 따로 만든다.
""",
 files=[("Token.sol","config + **balances, balanceOf**"),("tests.js","출제 · 채점 (테스트 5개)")],
 solution="""
```solidity
mapping(address => uint256) balances;

function balanceOf(address account) external view returns (uint256) {
    return balances[account];
}
```
""",
 tests="""
```js
const accounts = await ethers.provider.listAccounts();
owner = accounts[0];
const balance = await token.callStatic.balanceOf(owner);
assert.equal(balance.toString(), '0');   // 아직 아무도 토큰이 없다
```
""",
 run="sh tools/sol-test.sh week6/erc20-balances", env=ENV,
 remember=["잔액 = `mapping(address => uint256)`.","없는 키를 읽으면 0."]),

dict(dir="week6/erc20-mint", title="Minting (Build an ERC-20 4단계)",
 problem="""
constructor에서:

1. `totalSupply`를 토큰 **1000개**로 정한다 (decimals 18 반영).
2. 배포자 잔액을 `totalSupply`로 만든다.
""",
 summary="`totalSupply = 1000 * (10 ** decimals); balances[msg.sender] = totalSupply;`",
 img="Token_diagram.png", img_alt="mint",
 intent="""
> **발행(mint) = 토큰을 새로 만들어 누군가의 잔액에 넣는 것. 이번엔 배포할 때 한 번에 전부 배포자에게.**

| 1000개 | 컨트랙트 안의 숫자 |
|--------|-------------------|
| `1000 * 10**18` | `1000000000000000000000` |
| 테스트 쪽 | `ethers.utils.parseEther("1000")` (같은 값) |

실무에서는 OpenZeppelin `ERC20`의 `_mint(msg.sender, amount)`를 쓴다.
""",
 files=[("Token.sol","balances + **constructor**"),("tests.js","출제 · 채점 (테스트 6개)")],
 solution="""
```solidity
constructor() {
    totalSupply = 1000 * (10 ** decimals);
    balances[msg.sender] = totalSupply;
}
```
""",
 tests="""
```js
const totalSupply = ethers.utils.parseEther("1000");   // 1000 * 10^18
assert.equal((await token.balanceOf(owner)).toString(), totalSupply.toString());
assert.equal((await token.balanceOf(a1)).toString(), '0');
```
""",
 wrong=[("`totalSupply = 1000;`","잔액이 `1000`(= 0.000…001개)이라 parseEther(\"1000\")과 달라서 실패")],
 run="sh tools/sol-test.sh week6/erc20-mint", env=ENV,
 remember=["개수 × 10^decimals 로 저장.","배포자 = constructor의 `msg.sender`."]),

dict(dir="week6/erc20-transfer", title="Transfer (Build an ERC-20 5단계)",
 problem="""
public 함수 `transfer(address recipient, uint amount)`:

1. 호출자의 잔액에서 `amount`를 빼고 recipient에 더한다.
2. 성공하면 `true`를 돌려준다.
3. 🔒 호출자 잔액이 모자라면 revert.
""",
 summary="`require(balances[msg.sender] >= amount)` → `-=` / `+=` → `return true`.",
 img="Token_diagram.png", img_alt="transfer",
 intent="""
> **토큰 전송은 돈이 실제로 움직이는 게 아니라, 토큰 컨트랙트 안의 mapping 숫자 두 개를 고치는 것.**

```python
def transfer(sender, recipient, amount):
    assert balances[sender] >= amount
    balances[sender] -= amount
    balances[recipient] += amount
    return True
```
""",
 files=[("Token.sol","mint + **transfer**"),("tests.js","출제 · 채점 (테스트 11개)")],
 solution="""
```solidity
function transfer(address recipient, uint amount) public returns (bool) {
    require(balances[msg.sender] >= amount, "Not enough balance");
    balances[msg.sender] -= amount;
    balances[recipient] += amount;
    return true;
}
```
""",
 tests="""
```js
await token.connect(ownerSigner).transfer(a1, "1");   // owner −1, a1 +1
// 두 번째 transfer 후 owner −2, a1 2
await token.connect(s1).transfer(owner, "1");         // s1은 잔액 0 → 에러가 나야 통과
```
""",
 wrong=[("`require` 줄 빼기","그래도 11개 모두 통과한다. Solidity 0.8은 `0 - 1`처럼 음수가 되는 뺄셈을 자동으로 revert(panic 0x11)하기 때문. 다만 에러 메시지가 없어서 이유를 알기 어렵다 → require를 두는 게 좋다")],
 run="sh tools/sol-test.sh week6/erc20-transfer", env=ENV,
 remember=["잔액 확인 → 빼기 → 더하기 → `return true`.","0.8부터는 언더플로가 자동 revert."]),

dict(dir="week6/erc20-events", title="Transfer Event (Build an ERC-20 6단계)",
 problem="""
1. 이벤트 `Transfer(보낸 주소, 받는 주소, uint256 금액)`을 이 순서로 만든다.
2. `transfer` 안에서 emit한다.
""",
 summary="`event Transfer(address indexed from, address indexed to, uint256 value);` + `emit Transfer(msg.sender, recipient, amount);`",
 img="Token_diagram.png", img_alt="Transfer 이벤트",
 intent="""
> **지갑·거래소·Etherscan은 잔액을 매번 다시 읽지 않고 `Transfer` 이벤트를 구독해서 변화를 안다.**

- `indexed`를 붙인 인자는 검색할 수 있는 topic이 된다 ("이 주소가 받은 Transfer만" 같은 필터).
- 표준 ERC-20의 `Transfer` 시그니처와 똑같이 맞춰야 다른 앱이 알아본다.
""",
 files=[("Token.sol","transfer + **Transfer 이벤트**"),("tests.js","출제 · 채점 (테스트 13개)")],
 solution="""
```solidity
event Transfer(address indexed from, address indexed to, uint256 value);

function transfer(address recipient, uint amount) public returns (bool) {
    require(balances[msg.sender] >= amount, "Not enough balance");
    balances[msg.sender] -= amount;
    balances[recipient] += amount;
    emit Transfer(msg.sender, recipient, amount);
    return true;
}
```
""",
 tests="""
```js
const tx = await token.connect(ownerSigner).transfer(a1, "1");
receipt = await tx.wait();
const transferEvent = receipt.events.find(x => x.event === "Transfer");
assert.equal(transferEvent.args[0], owner);     // from
assert.equal(transferEvent.args[1], a1);        // to
assert.equal(transferEvent.args[2].toString(), "1");
```
""",
 wrong=[("`emit Transfer(recipient, msg.sender, amount)` (순서 반대)","이벤트는 나오지만 from/to가 뒤바뀌어 이벤트 테스트 2개 실패")],
 run="sh tools/sol-test.sh week6/erc20-events", env=ENV,
 remember=["상태를 바꾸면 이벤트로 알린다.","표준 이벤트 이름·인자 순서를 정확히."]),

dict(dir="week6/erc20-treasure-chest", title="ERC-20 Treasure Chest",
 problem="""
여러 ERC-20 토큰이 `Chest` 컨트랙트 주소로 보내져 있다.

external 함수 `plunder(address[] 토큰주소들)`: 각 토큰에서 **Chest가 가진 잔액 전부**를 호출자(`msg.sender`)에게 보낸다.
""",
 summary="토큰 주소마다 `IERC20(addr).balanceOf(address(this))`로 잔액을 읽고 `transfer(msg.sender, 잔액)`.",
 img="Chest_diagram.png", img_alt="plunder",
 intent="""
> **컨트랙트도 토큰을 가질 수 있다. 꺼낼 때는 그 컨트랙트가 직접 토큰 컨트랙트의 `transfer`를 불러야 한다.**

- 토큰 잔액은 Chest 안이 아니라 **각 토큰 컨트랙트의 mapping**에 `balances[Chest 주소]`로 적혀 있다.
- Chest가 `token.transfer(...)`를 부르면 토큰 컨트랙트 입장에서 `msg.sender`는 **Chest**다. 그래서 Chest의 잔액에서 빠져나간다.
- `IERC20` 인터페이스만 있으면 어떤 ERC-20이든 같은 방식으로 다룰 수 있다. 이게 표준의 힘.
""",
 files=[("Chest.sol","**이번에 완성할 컨트랙트**"),("IERC20.sol","ERC-20 인터페이스 (주어짐)"),("ERC20FixedSupply.sol","로컬 실행용 테스트 토큰 (사이트에선 숨겨짐)"),("tests.js","출제 · 채점 (테스트 13개)")],
 solution="""
```solidity
function plunder(address[] calldata tokens) external {
    for (uint i = 0; i < tokens.length; i++) {
        IERC20 token = IERC20(tokens[i]);
        uint balance = token.balanceOf(address(this));
        token.transfer(msg.sender, balance);
    }
}
```

`calldata`: 외부에서 받은 배열을 복사하지 않고 읽기만 해서 가스가 싸다 (`memory`도 통과한다).

```python
for addr in tokens:
    token = IERC20(addr)
    token.transfer(caller, token.balance_of(chest))
```
""",
 tests="""
```js
token1 = await ERC20.deploy(10000);
await token1.connect(coinCreatorSigner).transfer(chest.address, 250);
await token2.connect(coinCreatorSigner).transfer(chest.address, 300);
await chest.connect(hunterSigner).plunder([token2.address]);   // token2만 → token1은 그대로 250
await chest.connect(hunterSigner).plunder([token1.address, token2.address]);   // 둘 다 → chest 0 / 0
```
""",
 wrong=[("`transfer` 대신 `transferFrom(address(this), msg.sender, balance)`","Chest가 자기 자신에게 allowance를 준 적이 없어서 revert → 꺼내는 테스트 실패. 자기 토큰은 `transfer`로 보낸다")],
 run="sh tools/sol-test.sh week6/erc20-treasure-chest", env=ENV_HIDDEN.format(name="ERC20FixedSupply"),
 remember=["토큰 잔액은 토큰 컨트랙트 쪽 mapping에 있다.","컨트랙트가 부르면 `msg.sender` = 그 컨트랙트."]),
]
