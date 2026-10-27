// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

// 사이트에는 숨겨져 있는 테스트용 컨트랙트 (로컬 실행용으로 직접 작성)
contract Minter {
    uint public minted;

    function mint(uint amount) external {
        minted += amount;
    }
}
