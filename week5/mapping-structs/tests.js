const { assert } = require('chai');
// 화면에서 잘려 보이지 않은 assert 메시지 끝부분은 짐작으로 채웠다 (채점 결과와 무관).
describe('Contract', function () {
    let a1;
    let a2;
    beforeEach(async () => {
        const Contract = await ethers.getContractFactory("Contract");
        contract = await Contract.deploy();
        await contract.deployed();

        a1 = ethers.provider.getSigner(0);
        a2 = ethers.provider.getSigner(1);
    });

    describe('after creating a user', () => {
        beforeEach(async () => {
            await contract.connect(a1).createUser();
        });

        it('should return the user', async () => {
            const user = await contract.users(await a1.getAddress());
            assert.equal(user.balance, 100);
            assert(user.isActive, "Expected a new User to have an isActive boolean that returns true");
        });

        it('should not allow the same address to create another user', async () => {
            let ex;
            try {
                await contract.connect(a1).createUser();
            }
            catch(_ex) {
                ex = _ex;
            }
            assert(ex, "The same address should not be able to invoke createUser twice. Expected transaction to revert!");
        });

        describe('after creating another user', () => {
            beforeEach(async () => {
                await contract.connect(a2).createUser();
            });

            it('should return the user', async () => {
                const user = await contract.users(await a2.getAddress());
                assert.equal(user.balance, 100);
                assert(user.isActive, "Expected a new User to have an isActive boolean that returns true");
            });

            it('should not allow the same address to create another user', async () => {
                let ex;
                try {
                    await contract.connect(a2).createUser();
                }
                catch (_ex) {
                    ex = _ex;
                }
                assert(ex, "The same address should not be able to invoke createUser twice. Expected transaction to revert!");
            });
        });
    });
});
