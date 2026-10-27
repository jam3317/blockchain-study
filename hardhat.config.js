// Solidity 문제(week4~)를 단계 폴더마다 테스트하기 위한 설정.
// 사용법: STAGE=week4/booleans npx hardhat test week4/booleans/tests.js
//   STAGE 폴더 안의 .sol 파일을 컴파일하고, 그 폴더의 테스트를 실행한다.
require("@nomiclabs/hardhat-ethers");
const path = require("path");

const stage = process.env.STAGE || "week4";

module.exports = {
    // 문제마다 pragma 버전이 달라서 컴파일러를 여러 개 둔다.
    solidity: { compilers: [{ version: "0.8.20" }, { version: "0.8.17" }, { version: "0.8.4" }, { version: "0.7.5" }] },
    // selfdestruct 문제(week4/self-destruct)가 강의 환경처럼 동작하도록 Cancun 이전 규칙으로 실행한다.
    // Cancun(EIP-6780)부터는 selfdestruct가 컨트랙트 코드를 지우지 않는다.
    networks: { hardhat: { hardfork: "shanghai" } },
    paths: {
        sources: path.join(__dirname, stage),
        tests: path.join(__dirname, stage),
        cache: path.join(__dirname, ".hardhat", "cache", stage),
        artifacts: path.join(__dirname, ".hardhat", "artifacts", stage),
    },
};
