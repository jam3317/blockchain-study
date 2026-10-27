// SPDX-License-Identifier: MIT
pragma solidity 0.8.4;

contract Contract {
    function sum(uint[5] calldata numbers) external pure returns(uint total) {
        for (uint i = 0; i < numbers.length; i++) {
            total += numbers[i];
        }
    }
}
