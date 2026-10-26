// 강의 사이트에서는 숨겨진 파일이라, 같은 역할로 직접 만들었다.
const ganache = require("ganache");
const { utils } = require("ethers");

const PRIVATE_KEY = "0xf2f48ee19680706196e2e339e5da3491186e0c4c5030670656b0e0164837257d";
const INITIAL_BALANCE = utils.parseEther("10");   // BigNumber

const ganacheProvider = ganache.provider({
    accounts: [{ balance: INITIAL_BALANCE.toHexString(), secretKey: PRIVATE_KEY }],
    logging: { quiet: true },
});

module.exports = { ganacheProvider, PRIVATE_KEY, INITIAL_BALANCE };
