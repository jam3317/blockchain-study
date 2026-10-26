// Solidity 문제(week4~)를 단계 폴더마다 테스트하기 위한 설정.
// 사용법: STAGE=week4/booleans npx hardhat test week4/booleans/tests.js
//   STAGE 폴더 안의 .sol 파일을 컴파일하고, 그 폴더의 테스트를 실행한다.
require("@nomiclabs/hardhat-ethers");
const path = require("path");

const stage = process.env.STAGE || "week4";

module.exports = {
    solidity: "0.8.20",
    paths: {
        sources: path.join(__dirname, stage),
        tests: path.join(__dirname, stage),
        cache: path.join(__dirname, ".hardhat", "cache", stage),
        artifacts: path.join(__dirname, ".hardhat", "artifacts", stage),
    },
};
