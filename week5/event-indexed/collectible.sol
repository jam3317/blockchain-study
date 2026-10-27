// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

contract Collectible {
    address owner;
    uint price;   // 0이면 판매 중이 아님

    event Deployed(address indexed owner);
    event Transfer(address indexed originalOwner, address indexed newOwner);
    event ForSale(uint price, uint timestamp);
    event Purchase(uint amount, address indexed buyer);

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

    function markPrice(uint _price) external {
        require(msg.sender == owner, "Only the owner can mark the price");
        price = _price;
        emit ForSale(_price, block.timestamp);
    }

    function purchase() external payable {
        require(price > 0, "Not for sale");
        require(msg.value == price, "Wrong amount");

        address seller = owner;
        owner = msg.sender;
        price = 0;

        (bool success, ) = seller.call{ value: msg.value }("");
        require(success, "Payment failed");

        emit Purchase(msg.value, msg.sender);
    }
}
