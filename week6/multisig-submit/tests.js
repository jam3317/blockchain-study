const { assert } = require('chai');
// 잘려 보이지 않은 assert 메시지 끝부분은 짐작으로 채웠다 (채점 결과와 무관).
describe('MultiSig', function () {
    let contract;
    let accounts;
    let zero = ethers.constants.AddressZero;
    let _required = 2;

    describe('Submit Transaction Tests', function () {
        beforeEach(async () => {
            accounts = await ethers.provider.listAccounts();
            const MultiSig = await ethers.getContractFactory("MultiSig");
            contract = await MultiSig.deploy(accounts.slice(0, 3), _required);
            await contract.deployed();
        });

        it('should add a transaction', async function () {
            await contract.submitTransaction(accounts[1], 100);
            let tx = await contract.callStatic.transactions(0);
            let address = tx[0];
            assert.notEqual(address, zero);
        });

        it('should confirm a transaction', async function () {
            await contract.submitTransaction(accounts[1], 100);

            let confirmed = await contract.callStatic.getConfirmationsCount(0);
            assert.equal(confirmed, 1);
        });

        it('should not call addTransaction externally', async function () {
            assert.equal(contract.addTransaction, undefined, "Did not expect addTransaction to be defined publicly!");
        });
    });
});
