// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

contract Collectible {
    address owner;

    event Deployed(address owner);
    event Transfer(address originalOwner, address newOwner);

    constructor() {
        owner = msg.sender;
        emit Deployed(msg.sender);
    }

    function transfer(address recipient) external {
        require(msg.sender == owner, "Only the owner can transfer");
        address originalOwner = owner;
        owner = recipient;
        emit Transfer(originalOwner, recipient);
    }
}
