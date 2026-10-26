// 강의 사이트에서는 숨겨진 파일이라, 같은 역할로 직접 만들었다.
// 테스트 계정(PRIVATE_KEY)에 10 ETH를 넣은 ganache 가짜 노드를 만든다.
const ganache = require("ganache");

const PRIVATE_KEY = "0xf2f48ee19680706196e2e339e5da3491186e0c4c5030670656b0e0164837257d";

const ganacheProvider = ganache.provider({
    accounts: [{ balance: "0x8ac7230489e80000", secretKey: PRIVATE_KEY }],
    logging: { quiet: true },
});

module.exports = { ganacheProvider, PRIVATE_KEY };
