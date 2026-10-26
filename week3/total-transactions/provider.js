const promisify = require("./promisify");
const ganache = require("ganache");   // 강의 사이트는 예전 이름인 ganache-core를 쓴다
const PRIVATE_KEY = "0xf2f48ee19680706196e2e339e5da3491186e0c4c5030670656b0e0164837257d";

// create our test account from the private key, initialize it with 10 ether
const accounts = [].concat([{
    balance: "0x8ac7230489e80000", // 10 ether (새 ganache는 16진수 문자열만 받아서 바꿈. 강의 원본은 "10000000000000000000")
    secretKey: PRIVATE_KEY,
}]);

const provider = ganache.provider({ accounts, logging: { quiet: true } });

provider.send = promisify(provider.send);

module.exports = provider;
