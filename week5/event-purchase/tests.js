const chai = require('chai');
const { parseEther } = ethers.utils;
const { assert } = chai;
// 강의 원본의 `expect(...).to.be.reverted`는 로컬에 플러그인이 없어서 expectRevert(try/catch)로 바꿨다.
// 잘려 보이지 않은 assert 메시지 끝부분은 짐작으로 채웠다 (채점 결과와 무관).
async function expectRevert(promise) {
    let ex;
    try { await promise; } catch (_ex) { ex = _ex; }
    assert(ex, "Expected the transaction to revert");
}

describe('Collectible', function () {
    let collectible, oneEther, halfEther, owner, a2, a3;
    before(async () => {
        const Collectible = await ethers.getContractFactory("Collectible");
        collectible = await Collectible.deploy();

        [owner, a2, a3] = await ethers.provider.listAccounts();
        oneEther = parseEther("1.0");
        halfEther = parseEther("0.5");
    });

    it('should revert if a purchase is attempted before the item is marked for sale', async () => {
        const signer = await ethers.provider.getSigner(a2);
        await expectRevert(collectible.connect(signer).purchase());
    });

    describe('after marking a price', () => {
        before(async () => {
            await collectible.markPrice(oneEther);
        });

        it('should revert if a purchase is attempted with less money than the price', async () => {
            const signer = await ethers.provider.getSigner(a2);
            await expectRevert(collectible.connect(signer).purchase({ value: halfEther }));
        });
    });

    describe('after purchasing', () => {
        let response, initialBalance, purchaseEvent;
        before(async () => {
            initialBalance = await ethers.provider.getBalance(owner);

            const signer = await ethers.provider.getSigner(a2);
            response = await collectible.connect(signer).purchase({ value: oneEther });

            const receipt = await response.wait();
            purchaseEvent = receipt.events.find(x => x.event === "Purchase");
        });

        it('should emit a Purchase event', async () => {
            assert(purchaseEvent, "Expected a Purchase event to be emitted!");
            assert.equal(purchaseEvent.args.length, 2, "Expected 2 event values to be emitted!");
            assert.equal(purchaseEvent.args[0].toString(), parseEther("1").toString(), "Expected the first value to be the purchase amount");
            assert.equal(purchaseEvent.args[1], a2, "Expected the second return value to be the buyer");
        });

        it('should pay the owner', async () => {
            const balanceAfter = await ethers.provider.getBalance(owner);
            assert.equal(balanceAfter.sub(initialBalance).toString(), parseEther("1").toString());
        });

        it('should fail on the next purchase attempt', async () => {
            const signer = await ethers.provider.getSigner(a3);
            await expectRevert(collectible.connect(signer).purchase({ value: parseEther("1") }));
        });

        describe('after marking a new price', () => {
            before(async () => {
                const signer = await ethers.provider.getSigner(a2);
                await collectible.connect(signer).markPrice(parseEther("1"));
            });

            it('should allow a purchase', async () => {
                const signer = await ethers.provider.getSigner(a3);
                const response = await collectible.connect(signer).purchase({ value: parseEther("1") });
                const receipt = await response.wait();
                const purchaseEvent = receipt.events.find(x => x.event === "Purchase");
                assert(purchaseEvent, "Expected a Purchase event to be emitted!");
            });
        });
    });
});
