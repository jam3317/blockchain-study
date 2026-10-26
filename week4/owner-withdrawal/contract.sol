// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

contract Contract {
    address owner;

    constructor() payable {
        require(msg.value >= 1 ether, "Deposit at least 1 ether");
        owner = msg.sender;
    }

    function withdraw() public {
        require(msg.sender == owner, "Only the owner can withdraw");
        (bool success, ) = owner.call{ value: address(this).balance }("");
        require(success, "Withdraw failed");
    }
}
