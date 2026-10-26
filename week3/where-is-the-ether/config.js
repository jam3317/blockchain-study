// require('./setup');   ← 강의 사이트의 숨겨진 설정 파일. 로컬에서는 필요 없어서 뺐다.
const { utils } = require('ethers');
const Ganache = require("ganache");   // 강의 사이트는 예전 이름인 ganache-core를 쓴다
const PRIVATE_KEY = "0xf2f48ee19680706196e2e339e5da3491186e0c4c5030670656b0e0164837257d";
const INITIAL_BALANCE = utils.parseEther('10');

// create our test account from the private key, initialize it with 10 ether
const accounts = [].concat([{
    balance: INITIAL_BALANCE.toHexString(),
    secretKey: PRIVATE_KEY,
}]);

const ganacheProvider = Ganache.provider({ accounts, logging: { quiet: true } });

module.exports = {
    INITIAL_BALANCE,
    PRIVATE_KEY,
    ganacheProvider,
}
