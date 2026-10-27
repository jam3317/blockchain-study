const { assert } = require('chai');
// 강의 원본은 ./artifacts/contracts/MultiSig.sol/MultiSig.json 파일을 직접 읽는다. 로컬은 readArtifact로 같은 ABI를 읽는다.
const error = "Make sure to declare a public uint for the confirmations!";
describe('MultiSig', function () {
    let abi;
    before(async () => {
        ({ abi } = await hre.artifacts.readArtifact("MultiSig"));
    });

    it('should define a confirmations mapping', async function () {
        const confirmations = abi.filter(x => x.name === 'confirmations')[0];
        assert(confirmations, error);
        assert.deepEqual(confirmations.inputs.map(x => x.type), ['uint256', 'address']);
        assert.deepEqual(confirmations.outputs.map(x => x.type), ['bool']);
    });
});
