const { assert } = require('chai');
const errors = [
    "Make sure to declare a public uint for the transaction count!",
    "Make sure to declare a public mapping for the transactions!",
];
// 강의 원본은 컴파일 결과 파일을 직접 읽는다:
//   const jsonLoc = "./artifacts/contracts/MultiSig.sol/MultiSig.json";
//   const { abi } = JSON.parse(fs.readFileSync(jsonLoc).toString());
// 로컬은 컴파일 결과 위치가 달라서 hre.artifacts.readArtifact로 같은 ABI를 읽는다.
describe('MultiSig', function () {
    let abi;
    before(async () => {
        ({ abi } = await hre.artifacts.readArtifact("MultiSig"));
    });

    it('should define the transaction count', async function () {
        const transactionCount = abi.filter(x => x.name === 'transactionCount')[0];
        assert(transactionCount, errors[0]);
        assert.deepEqual(transactionCount.outputs.map(x => x.type), ['uint256']);
    });

    it('should define a transactions mapping or array', async function () {
        const transactions = abi.filter(x => x.name === 'transactions')[0];
        assert(transactions, errors[1]);
        assert.deepEqual(transactions.inputs.map(x => x.type), ['uint256']);
        assert.deepEqual(transactions.outputs.map(x => x.type), ['address', 'uint256', 'bool']);
    });
});
