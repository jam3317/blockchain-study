const promisify = require("./promisify");
const ganache = require("ganache");   // 강의 사이트는 예전 이름인 ganache-core를 쓴다

const provider = ganache.provider({ logging: { quiet: true } });

provider.send = promisify(provider.send);

module.exports = provider;
