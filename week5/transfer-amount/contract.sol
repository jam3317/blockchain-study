// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

contract Contract {
    struct User {
        uint balance;
        bool isActive;
    }

    mapping(address => User) public users;

    function createUser() external {
        require(!users[msg.sender].isActive, "User already exists");
        users[msg.sender] = User(100, true);
    }

    function transfer(address recipient, uint amount) external {
        User storage sender = users[msg.sender];
        User storage receiver = users[recipient];
        require(sender.isActive && receiver.isActive, "Both users must be active");
        require(sender.balance >= amount, "Not enough balance");

        sender.balance -= amount;
        receiver.balance += amount;
    }
}
