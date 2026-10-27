const { assert } = require('chai');
// 강의 원본은 `await expect(...).to.be.reverted` (Hardhat의 chai 플러그인)를 쓴다.
// 로컬에는 그 플러그인이 없어서 같은 검사를 try/catch로 바꿨다.
// 잘려 보이지 않은 assert 메시지 끝부분은 짐작으로 채웠다 (채점 결과와 무관).
describe('Collectible', function () {
    let deployedEvent, response, collectible, owner, a2;
    before(async () => {
        [owner, a2] = await ethers.provider.listAccounts();
        const Collectible = await ethers.getContractFactory("Collectible");
        collectible = await Collectible.deploy();
        response = await collectible.transfer(a2);

        const receipt = await response.wait();
        const topic = collectible.interface.getEventTopic('Transfer');
        const log = receipt.logs.find(x => x.topics.indexOf(topic) >= 0);
        deployedEvent = collectible.interface.parseLog(log);
    });

    it('should emit a Transfer event', async () => {
        assert(deployedEvent, "Expected a Transfer event to be emitted!");
        assert.equal(deployedEvent.args.length, 2, "Expected 2 event values to be emitted!");
        assert.equal(deployedEvent.args[0], owner, "Expected the first return value to be the original owner");
        assert.equal(deployedEvent.args[1], a2, "Expected the second return value to be the new owner");
    });

    it('should revert if the original owner tries to transfer again', async () => {
        const signer = await ethers.provider.getSigner(owner);
        let ex;
        try { await collectible.connect(signer).transfer(a2); } catch (_ex) { ex = _ex; }
        assert(ex, "Expected the transaction to revert");
    });
});
