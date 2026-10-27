// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

contract Party {
    uint256 public deposit;
    address[] public members;
    mapping(address => bool) public hasJoined;

    constructor(uint256 _deposit) {
        deposit = _deposit;
    }

    function rsvp() external payable {
        require(msg.value == deposit, "Must pay exactly the deposit");
        require(!hasJoined[msg.sender], "Already RSVP'd");

        hasJoined[msg.sender] = true;
        members.push(msg.sender);
    }
}
