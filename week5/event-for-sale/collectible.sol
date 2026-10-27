// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

contract Collectible {
    address owner;

    event Deployed(address owner);
    event Transfer(address originalOwner, address newOwner);
    event ForSale(uint price, uint timestamp);

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

    function markPrice(uint price) external {
        require(msg.sender == owner, "Only the owner can mark the price");
        emit ForSale(price, block.timestamp);
    }
}
