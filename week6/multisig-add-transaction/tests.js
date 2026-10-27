const { assert } = require('chai');
describe('MultiSig', function () {
    let contract;
    let accounts;
    let zero = ethers.constants.AddressZero;
    let _required = 2;

    describe('Add Transaction Tests', function () {
        beforeEach(async () => {
            accounts = await ethers.provider.listAccounts();
            const MultiSig = await ethers.getContractFactory("MultiSig");
            contract = await MultiSig.deploy(accounts.slice(0,3), _required);
            await contract.deployed();
        });

        it('should create a new Transaction', async function () {
            await contract.addTransaction(accounts[1], 100);

            // 강의 원본은 `contract.callStatic.transactions;`(호출 괄호 없음)이라 tx[0]이 항상 undefined → 언제나 통과한다.
            // 로컬에서는 실제로 0번 거래를 읽도록 transactions(0)으로 고쳤다.
            let tx = await contract.callStatic.transactions(0);
            let address = tx[0];
            assert.notEqual(address, zero);
        });

        it('should keep count of the amount of transactions', async function () {
            await contract.addTransaction(accounts[1], 100);

            let txCount = await contract.callStatic.transactionCount();
            assert.equal(txCount.toNumber(), 1);
        });

        it('should return a transaction id', async function () {
            await contract.addTransaction(accounts[1], 100);

            let txId = await contract.callStatic.addTransaction(accounts[1], 100);

            assert.equal(txId.toNumber(), 1);
        });
    });
});
