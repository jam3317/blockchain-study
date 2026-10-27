const { assert } = require('chai');
// 강의 원본의 `expect(...).to.be.reverted`는 로컬에 플러그인이 없어서 try/catch로 바꿨다.
// 잘려 보이지 않은 assert 메시지 끝부분은 짐작으로 채웠다 (채점 결과와 무관).
describe('Collectible', function () {
    let deployedEvent, oneEther, collectible, response, blockNumber;
    before(async () => {
        const Collectible = await ethers.getContractFactory('Collectible');
        collectible = await Collectible.deploy();
        oneEther = ethers.utils.parseEther("1.0");
        response = await collectible.markPrice(oneEther);
        const receipt = await response.wait();
        blockNumber = response.blockNumber;

        const topic = collectible.interface.getEventTopic('ForSale');
        const log = receipt.logs.find(x => x.topics.indexOf(topic) >= 0);
        deployedEvent = collectible.interface.parseLog(log);
    });

    it('should revert if a non-owner tries to mark the price', async () => {
        let [owner, a2] = await ethers.provider.listAccounts();
        const signer = await ethers.provider.getSigner(a2);
        let ex;
        try { await collectible.connect(signer).markPrice(oneEther); } catch (_ex) { ex = _ex; }
        assert(ex, "Expected the transaction to revert");
    });

    it('should emit a ForSale event', async () => {
        let block = await ethers.provider.getBlock(blockNumber);
        let blockTimeStamp = block.timestamp;
        assert(deployedEvent, "Expected a ForSale event to be emitted!");
        assert.equal(deployedEvent.args.length, 2, "Expected 2 event values to be emitted!");
        assert.equal(deployedEvent.args[0].toHexString(16), oneEther.toHexString(16), "Expected the first value to be the price");
        assert.equal(deployedEvent.args[1].toNumber(), blockTimeStamp, "Expected the second value to be the block timestamp");
    });
});
