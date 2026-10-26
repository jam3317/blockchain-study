// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

contract Contract {
    uint ticks = 10;

    function tick() external {
        ticks--;
        if (ticks == 0) {
            selfdestruct(payable(msg.sender));
        }
    }
}
