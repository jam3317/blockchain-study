// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

contract Sidekick {
    function makeContact(address hero) external {
        // Hero에 없는 함수 이름으로 부르면 fallback이 실행된다
        (bool success, ) = hero.call(abi.encodeWithSignature("doesNotExist()"));
        require(success);
    }
}
